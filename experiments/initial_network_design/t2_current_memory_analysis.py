"""Fit current five-downsampling memory probes and update the planning chart."""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--study-dir", type=Path, required=True)
    args = parser.parse_args()

    probe_paths = sorted(
        glob.glob(str(args.study_dir / "memory_probes_5down" / "*.json"))
    )
    probes = []
    for path in probe_paths:
        with open(path, encoding="utf-8") as stream:
            item = json.load(stream)
        if item.get("status") == "ok":
            probes.append(item)
    if len(probes) < 3:
        raise RuntimeError("At least three successful probes are required")

    voxels = np.array([item["voxels"] for item in probes], dtype=float)
    reserved = np.array([item["peak_reserved_gib"] for item in probes], dtype=float)
    slope, intercept = np.polyfit(voxels, reserved, 1)
    fitted = slope * voxels + intercept
    r_squared = 1.0 - np.square(reserved - fitted).sum() / np.square(
        reserved - reserved.mean()
    ).sum()

    safety_factor = 1.15
    planning_limit_gib = 20.0
    target_shape = (288, 288, 288)
    target_voxels = int(np.prod(target_shape))
    target_reserved = float(slope * target_voxels + intercept)
    target_planning = target_reserved * safety_factor

    result = {
        "status": "extrapolated_not_measured_on_24gb_gpu",
        "architecture": (
            "five downsamplings, channels 8/16/32/64/128/128, "
            "BF16 autocast, FP32 losses, batch size 1"
        ),
        "probe_count": len(probes),
        "largest_probe_voxels": int(voxels.max()),
        "reserved_slope_gib_per_million_voxels": float(slope * 1e6),
        "reserved_intercept_gib": float(intercept),
        "reserved_r_squared": float(r_squared),
        "safety_factor": safety_factor,
        "planning_limit_gib": planning_limit_gib,
        "target_shape_dhw": list(target_shape),
        "target_voxels": target_voxels,
        "target_reserved_gib": target_reserved,
        "target_planning_gib_with_15pct_margin": target_planning,
        "headroom_to_20gib": planning_limit_gib - target_planning,
    }
    (args.study_dir / "t2_current_memory.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    figure, axis = plt.subplots(figsize=(9.2, 5.8))
    axis.scatter(
        voxels / 1e6,
        reserved,
        s=58,
        color="#2563A6",
        edgecolor="white",
        linewidth=0.8,
        label="8 GB GPU measurements",
        zorder=3,
    )
    line_x = np.linspace(0, target_voxels * 1.06, 240)
    axis.plot(
        line_x / 1e6,
        (slope * line_x + intercept) * safety_factor,
        color="#2563A6",
        linewidth=2.0,
        label="reserved-memory fit + 15%",
    )
    axis.scatter(
        target_voxels / 1e6,
        target_planning,
        marker="D",
        s=86,
        color="#D97706",
        edgecolor="#7C2D12",
        linewidth=0.8,
        zorder=4,
    )
    axis.annotate(
        f"Current 288³ design: {target_planning:.2f} GiB",
        (target_voxels / 1e6, target_planning),
        xytext=(-8, 10),
        textcoords="offset points",
        ha="right",
        fontsize=10,
    )
    axis.axhline(
        planning_limit_gib,
        color="#991B1B",
        linestyle="--",
        linewidth=1.5,
        label="20 GiB planning limit",
    )
    axis.set_xlim(left=0)
    axis.set_ylim(0, 21)
    axis.set_xlabel("Dense-domain voxels (million)")
    axis.set_ylabel("Peak reserved-memory planning value (GiB)")
    axis.set_title(
        "Five-downsampling 3D U-Net memory planning\n"
        "288³ value is extrapolated from 8 GB probes, not measured on a 24 GB GPU"
    )
    axis.grid(alpha=0.2)
    axis.legend(loc="upper left", frameon=False)
    figure.tight_layout()
    figure.savefig(args.study_dir / "memory_scaling.png", dpi=240)
    figure.savefig(args.study_dir / "memory_scaling.svg")
    plt.close(figure)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
