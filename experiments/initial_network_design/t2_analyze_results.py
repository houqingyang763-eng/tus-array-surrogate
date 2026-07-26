"""Combine literature-geometry candidates with measured CUDA memory probes."""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--study-dir", type=Path, required=True)
    args = parser.parse_args()

    geometry_path = args.study_dir / "geometry_results.json"
    with geometry_path.open(encoding="utf-8") as stream:
        geometry = json.load(stream)

    probe_paths = sorted(glob.glob(str(args.study_dir / "memory_probes" / "*.json")))
    probes = []
    for path in probe_paths:
        with open(path, encoding="utf-8") as stream:
            item = json.load(stream)
        if item.get("status") == "ok":
            probes.append(item)
    if len(probes) < 3:
        raise RuntimeError("At least three successful memory probes are required")

    voxels = np.array([item["voxels"] for item in probes], dtype=float)
    allocated = np.array([item["peak_allocated_gib"] for item in probes], dtype=float)
    reserved = np.array([item["peak_reserved_gib"] for item in probes], dtype=float)
    allocated_slope, allocated_intercept = np.polyfit(voxels, allocated, 1)
    allocated_fitted = allocated_slope * voxels + allocated_intercept
    allocated_r_squared = 1.0 - np.square(allocated - allocated_fitted).sum() / np.square(
        allocated - allocated.mean()
    ).sum()
    reserved_slope, reserved_intercept = np.polyfit(voxels, reserved, 1)
    reserved_fitted = reserved_slope * voxels + reserved_intercept
    reserved_r_squared = 1.0 - np.square(reserved - reserved_fitted).sum() / np.square(
        reserved - reserved.mean()
    ).sum()

    safety_factor = 1.15
    planning_limit_gib = 20.0
    rows = []
    for candidate in geometry["conservative_candidates"]:
        count = candidate["voxels"]
        allocated_estimate = float(allocated_slope * count + allocated_intercept)
        reserved_estimate = float(reserved_slope * count + reserved_intercept)
        planning = float(reserved_estimate * safety_factor)
        medium_mib = count * 4 / 1024**2
        label_mib = count * 2 * 4 / 1024**2
        prediction_bf16_mib = count * 2 * 2 / 1024**2
        passes = bool(planning <= planning_limit_gib)
        rows.append(
            {
                "patch_width_mm": candidate["patch_width_mm"],
                "domain_size_mm_xyz": candidate["domain_size_mm_xyz"],
                "shape_voxels_xyz": candidate["shape_voxels_xyz"],
                "total_voxels": count,
                "medium_fp32_mib": medium_mib,
                "label_reim_fp32_mib": label_mib,
                "prediction_reim_bf16_mib": prediction_bf16_mib,
                "estimated_peak_allocated_gib": allocated_estimate,
                "estimated_peak_reserved_gib": reserved_estimate,
                "planning_reserved_gib_with_15pct_margin": planning,
                "headroom_to_20gib": float(planning_limit_gib - planning),
                "passes_20gib_planning_limit": passes,
            }
        )

    feasible = [row for row in rows if row["passes_20gib_planning_limit"]]
    recommendation = max(feasible, key=lambda row: row["patch_width_mm"]) if feasible else None

    result = {
        "status": "estimated_from_8gb_gpu_probes_not_measured_on_24gb_gpu",
        "probe_architecture": (
            "candidate 3D U-Net, four downsamplings, channels 8/16/32/64/128, "
            "BF16 autocast, FP32 data and Helmholtz-like residual, AdamW"
        ),
        "memory_fit": {
            "allocated_slope_gib_per_million_voxels": float(allocated_slope * 1e6),
            "allocated_intercept_gib": float(allocated_intercept),
            "allocated_r_squared": float(allocated_r_squared),
            "reserved_slope_gib_per_million_voxels": float(reserved_slope * 1e6),
            "reserved_intercept_gib": float(reserved_intercept),
            "reserved_r_squared": float(reserved_r_squared),
            "probe_count": len(probes),
            "largest_probe_voxels": int(voxels.max()),
            "largest_probe_peak_allocated_gib": float(
                allocated[np.argmax(voxels)]
            ),
            "safety_factor": safety_factor,
            "planning_limit_gib": planning_limit_gib,
        },
        "candidate_rows": rows,
        "recommendation": recommendation,
        "decision_rule": (
            "Choose the largest patch whose 15%-margin estimate is <=20 GiB; "
            "do not reduce 0.5 mm spacing, 82 mm path, 0-10 mm offset, or +/-30 deg."
        ),
    }
    (args.study_dir / "t2_recommendation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (args.study_dir / "memory_domain_table.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
                "patch_width_mm",
                "domain_size_mm_xyz",
                "shape_voxels_xyz",
                "total_voxels",
                "medium_fp32_mib",
                "label_reim_fp32_mib",
                "prediction_reim_bf16_mib",
                "estimated_peak_allocated_gib",
                "estimated_peak_reserved_gib",
                "planning_reserved_gib_with_15pct_margin",
                "headroom_to_20gib",
                "passes_20gib_planning_limit",
            ),
        )
        writer.writeheader()
        writer.writerows(rows)

    figure, axis = plt.subplots(figsize=(9, 6))
    axis.scatter(voxels / 1e6, reserved, s=55, label="8 GB GPU reserved measurements")
    line_x = np.linspace(0, max(row["total_voxels"] for row in rows) * 1.05, 200)
    axis.plot(
        line_x / 1e6,
        (reserved_slope * line_x + reserved_intercept) * safety_factor,
        label="reserved fit + 15%",
    )
    for row in rows:
        axis.scatter(
            row["total_voxels"] / 1e6,
            row["planning_reserved_gib_with_15pct_margin"],
            marker="D",
            s=65,
        )
        axis.annotate(
            f"{row['patch_width_mm']:.0f} mm patch",
            (
                row["total_voxels"] / 1e6,
                row["planning_reserved_gib_with_15pct_margin"],
            ),
            xytext=(6, 6),
            textcoords="offset points",
        )
    axis.axhline(planning_limit_gib, color="red", linestyle="--", label="20 GiB limit")
    axis.set_xlabel("Dense-domain voxels (million)")
    axis.set_ylabel("Peak reserved memory planning value (GiB)")
    axis.set_title(
        "Candidate 3D U-Net memory planning\n"
        "24 GB values are extrapolated, not measured on a 24 GB GPU"
    )
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(args.study_dir / "memory_scaling.png", dpi=220)
    plt.close(figure)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
