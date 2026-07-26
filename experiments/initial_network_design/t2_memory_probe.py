"""Engineering-only CUDA memory probe for the current candidate 3D U-Net.

This script does not evaluate scientific accuracy. It measures one complete
training step (forward, FP32 data/Helmholtz-like losses, backward, AdamW step)
for the five-downsampling, base-width-8, bottleneck-width-128 V0 candidate.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, 3, padding=1, bias=False),
            nn.GroupNorm(8, out_channels),
            nn.LeakyReLU(0.01, inplace=True),
            nn.Conv3d(out_channels, out_channels, 3, padding=1, bias=False),
            nn.GroupNorm(8, out_channels),
            nn.LeakyReLU(0.01, inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class CandidateUNet3D(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        channels = (8, 16, 32, 64, 128, 128)
        self.enc0 = DoubleConv(1, channels[0])
        self.enc1 = DoubleConv(channels[0], channels[1])
        self.enc2 = DoubleConv(channels[1], channels[2])
        self.enc3 = DoubleConv(channels[2], channels[3])
        self.enc4 = DoubleConv(channels[3], channels[4])
        self.bottleneck = DoubleConv(channels[4], channels[5])
        self.pool = nn.MaxPool3d(2)

        self.geometry_projection = nn.Sequential(
            nn.Linear(6, channels[5]),
            nn.ReLU(inplace=True),
            nn.Linear(channels[5], channels[5]),
        )
        self.geometry_fusion = nn.Sequential(
            nn.Conv3d(2 * channels[5], channels[5], 1, bias=False),
            nn.GroupNorm(8, channels[5]),
            nn.ReLU(inplace=True),
        )

        self.up4 = nn.ConvTranspose3d(channels[5], channels[4], 2, stride=2)
        self.dec4 = DoubleConv(2 * channels[4], channels[4])
        self.up3 = nn.ConvTranspose3d(channels[4], channels[3], 2, stride=2)
        self.dec3 = DoubleConv(2 * channels[3], channels[3])
        self.up2 = nn.ConvTranspose3d(channels[3], channels[2], 2, stride=2)
        self.dec2 = DoubleConv(2 * channels[2], channels[2])
        self.up1 = nn.ConvTranspose3d(channels[2], channels[1], 2, stride=2)
        self.dec1 = DoubleConv(2 * channels[1], channels[1])
        self.up0 = nn.ConvTranspose3d(channels[1], channels[0], 2, stride=2)
        self.dec0 = DoubleConv(2 * channels[0], channels[0])
        self.output = nn.Conv3d(channels[0], 2, 3, padding=1)

    def forward(self, medium: torch.Tensor, geometry: torch.Tensor) -> torch.Tensor:
        e0 = self.enc0(medium)
        e1 = self.enc1(self.pool(e0))
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))
        z = self.bottleneck(self.pool(e4))

        g = self.geometry_projection(geometry)
        g = g[:, :, None, None, None].expand(-1, -1, *z.shape[2:])
        z = self.geometry_fusion(torch.cat((z, g), dim=1))

        d4 = self.dec4(torch.cat((self.up4(z), e4), dim=1))
        d3 = self.dec3(torch.cat((self.up3(d4), e3), dim=1))
        d2 = self.dec2(torch.cat((self.up2(d3), e2), dim=1))
        d1 = self.dec1(torch.cat((self.up1(d2), e1), dim=1))
        d0 = self.dec0(torch.cat((self.up0(d1), e0), dim=1))
        return self.output(d0)


def laplacian_kernel(device: torch.device) -> torch.Tensor:
    kernel = torch.zeros((2, 1, 3, 3, 3), dtype=torch.float32, device=device)
    kernel[:, 0, 1, 1, 1] = -6.0
    kernel[:, 0, 0, 1, 1] = 1.0
    kernel[:, 0, 2, 1, 1] = 1.0
    kernel[:, 0, 1, 0, 1] = 1.0
    kernel[:, 0, 1, 2, 1] = 1.0
    kernel[:, 0, 1, 1, 0] = 1.0
    kernel[:, 0, 1, 1, 2] = 1.0
    return kernel


def run_probe(shape: tuple[int, int, int]) -> dict[str, object]:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this probe")
    if any(size % 32 for size in shape):
        raise ValueError(f"Each spatial dimension must be divisible by 32: {shape}")

    torch.manual_seed(20260725)
    device = torch.device("cuda")
    model = CandidateUNet3D().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    medium = torch.randn((1, 1, *shape), dtype=torch.float32, device=device)
    target = torch.randn((1, 2, *shape), dtype=torch.float32, device=device)
    geometry = torch.randn((1, 6), dtype=torch.float32, device=device)
    kernel = laplacian_kernel(device)

    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(device)
    start = time.perf_counter()
    optimizer.zero_grad(set_to_none=True)

    with torch.autocast("cuda", dtype=torch.bfloat16):
        prediction = model(medium, geometry)

    prediction_fp32 = prediction.float()
    data_loss = F.mse_loss(prediction_fp32, target)
    residual = F.conv3d(prediction_fp32, kernel, padding=1, groups=2)
    physics_loss = residual.square().mean()
    loss = data_loss + 1e-3 * physics_loss
    loss.backward()
    optimizer.step()
    torch.cuda.synchronize()

    elapsed = time.perf_counter() - start
    allocated = torch.cuda.max_memory_allocated(device)
    reserved = torch.cuda.max_memory_reserved(device)
    params = sum(parameter.numel() for parameter in model.parameters())

    return {
        "status": "ok",
        "shape_dhw": list(shape),
        "voxels": int(shape[0] * shape[1] * shape[2]),
        "batch_size": 1,
        "architecture": (
            "five downsamplings, channels 8/16/32/64/128/128, "
            "two 3x3x3 convolutions per level"
        ),
        "dtype_network": "BF16 autocast",
        "dtype_losses": "FP32",
        "parameter_count": params,
        "loss": float(loss.detach().cpu()),
        "elapsed_seconds": elapsed,
        "peak_allocated_gib": allocated / 1024**3,
        "peak_reserved_gib": reserved / 1024**3,
        "gpu": torch.cuda.get_device_name(device),
        "gpu_total_gib": torch.cuda.get_device_properties(device).total_memory / 1024**3,
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "scientific_scope": "engineering memory probe only",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", nargs=3, type=int, required=True, metavar=("D", "H", "W"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = run_probe(tuple(args.shape))
    except torch.OutOfMemoryError as error:
        result = {
            "status": "oom",
            "shape_dhw": args.shape,
            "voxels": int(args.shape[0] * args.shape[1] * args.shape[2]),
            "error": str(error),
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        }

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
