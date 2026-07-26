"""Frozen coordinate network for a finite-aperture element's complex response."""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class GreenModelConfig:
    frequency_hz: float = 500_000.0
    reference_sound_speed_m_s: float = 1500.0
    reference_pressure_pa: float = 100_000.0
    reference_distance_mm: float = 100.0
    fourier_levels: int = 6
    source_width: int = 128
    query_width: int = 128
    fusion_width: int = 256
    residual_blocks: int = 4


class ResidualBlock(nn.Module):
    def __init__(self, width: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(width, width),
            nn.SiLU(),
            nn.Linear(width, width),
        )
        self.activation = nn.SiLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.activation(x + self.net(x))


class GreenComplexNet(nn.Module):
    """Map element centre/normal and query coordinate to absolute Re/Im pressure.

    All coordinates are in millimetres. The learned output is a dimensionless
    complex correction T. Absolute pressure is recovered as
    P = P_ref * (r_ref/r) * exp(i*k*r) * T.
    """

    def __init__(self, config: GreenModelConfig | None = None) -> None:
        super().__init__()
        self.config = config or GreenModelConfig()
        self.register_buffer("domain_center_mm", torch.tensor([100.0, 0.0, 0.0]))
        self.register_buffer("domain_half_extent_mm", torch.tensor([100.0, 80.0, 80.0]))
        self.register_buffer("relative_scale_mm", torch.tensor([200.0, 160.0, 160.0]))

        self.source_encoder = nn.Sequential(
            nn.Linear(6, self.config.source_width),
            nn.SiLU(),
            nn.Linear(self.config.source_width, self.config.source_width),
            nn.SiLU(),
        )

        # raw absolute xyz, relative xyz, distance, cosine = 8;
        # Fourier features for absolute and relative xyz = 2*3*2*levels.
        query_input_width = 8 + 12 * self.config.fourier_levels
        self.query_encoder = nn.Sequential(
            nn.Linear(query_input_width, self.config.query_width),
            nn.SiLU(),
            nn.Linear(self.config.query_width, self.config.query_width),
            nn.SiLU(),
        )
        self.fusion_in = nn.Sequential(
            nn.Linear(self.config.source_width + self.config.query_width, self.config.fusion_width),
            nn.SiLU(),
        )
        self.residual = nn.Sequential(
            *[ResidualBlock(self.config.fusion_width) for _ in range(self.config.residual_blocks)]
        )
        self.output = nn.Linear(self.config.fusion_width, 2)

    def _normalise_source(self, centre_mm: torch.Tensor, normal: torch.Tensor) -> torch.Tensor:
        centre = (centre_mm - self.domain_center_mm) / self.domain_half_extent_mm
        normal = torch.nn.functional.normalize(normal, dim=-1)
        return torch.cat((centre, normal), dim=-1)

    def encode_source(self, centre_mm: torch.Tensor, normal: torch.Tensor) -> torch.Tensor:
        return self.source_encoder(self._normalise_source(centre_mm, normal))

    def _fourier(self, coordinates: torch.Tensor) -> torch.Tensor:
        frequencies = (2.0 ** torch.arange(
            self.config.fourier_levels, device=coordinates.device, dtype=coordinates.dtype
        )) * math.pi
        phases = coordinates.unsqueeze(-1) * frequencies
        return torch.cat((torch.sin(phases), torch.cos(phases)), dim=-1).flatten(-2)

    def _query_features(
        self, centre_mm: torch.Tensor, normal: torch.Tensor, query_mm: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        relative_mm = query_mm - centre_mm
        distance_mm = torch.linalg.vector_norm(relative_mm, dim=-1, keepdim=True).clamp_min(1.0e-3)
        direction = relative_mm / distance_mm
        unit_normal = torch.nn.functional.normalize(normal, dim=-1)
        cosine = torch.sum(unit_normal * direction, dim=-1, keepdim=True)
        absolute = (query_mm - self.domain_center_mm) / self.domain_half_extent_mm
        relative = relative_mm / self.relative_scale_mm
        raw = torch.cat((absolute, relative, distance_mm / 200.0, cosine), dim=-1)
        return torch.cat((raw, self._fourier(absolute), self._fourier(relative)), dim=-1), distance_mm

    def _carrier(self, distance_mm: torch.Tensor) -> torch.Tensor:
        distance_m = distance_mm * 1.0e-3
        wavenumber = 2.0 * math.pi * self.config.frequency_hz / self.config.reference_sound_speed_m_s
        phase = wavenumber * distance_m
        magnitude = self.config.reference_distance_mm / distance_mm
        return torch.cat((magnitude * torch.cos(phase), magnitude * torch.sin(phase)), dim=-1)

    def forward_from_embedding(
        self,
        source_embedding: torch.Tensor,
        centre_mm: torch.Tensor,
        normal: torch.Tensor,
        query_mm: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        query_features, distance_mm = self._query_features(centre_mm, normal, query_mm)
        query_embedding = self.query_encoder(query_features)
        fused = self.fusion_in(torch.cat((source_embedding, query_embedding), dim=-1))
        transfer = self.output(self.residual(fused))
        carrier = self._carrier(distance_mm)
        pressure_re = carrier[:, 0] * transfer[:, 0] - carrier[:, 1] * transfer[:, 1]
        pressure_im = carrier[:, 0] * transfer[:, 1] + carrier[:, 1] * transfer[:, 0]
        pressure = self.config.reference_pressure_pa * torch.stack((pressure_re, pressure_im), dim=-1)
        return pressure, transfer

    def forward(
        self, centre_mm: torch.Tensor, normal: torch.Tensor, query_mm: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        source_embedding = self.encode_source(centre_mm, normal)
        return self.forward_from_embedding(source_embedding, centre_mm, normal, query_mm)


def parameter_count(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters())
