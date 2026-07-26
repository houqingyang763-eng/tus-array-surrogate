"""Recheck T2 source placement and inward coverage without MIDA anatomy.

This is a geometry-only schematic. It deliberately does not draw scalp
thickness, skull thickness, or a brain boundary because licensed MIDA voxels
have not yet been measured.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PLACEMENT_WIDTH_MM = 120.0
CAP_RADII_MM = (80.0, 100.0, 120.0)
SOURCE_OFFSETS_MM = (0.5, 2.0)
FOCAL_DISTANCE_MM = 82.0
JANG_ROI_START_MM = 50.0
JANG_ROI_LENGTH_MM = 75.0
DEEP_COVERAGE_MM = JANG_ROI_START_MM + JANG_ROI_LENGTH_MM
NORMAL_HALF_ANGLE_DEG = 30.0
SAFETY_MARGIN_MM = 5.0
GRID_SPACING_MM = 0.5
NETWORK_MULTIPLE = 16


def frame(normals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference = np.zeros_like(normals)
    reference[:, 2] = 1.0
    near_parallel = np.abs(normals[:, 2]) > 0.9
    reference[near_parallel] = np.array([1.0, 0.0, 0.0])
    tangent_1 = np.cross(normals, reference)
    tangent_1 /= np.linalg.norm(tangent_1, axis=1, keepdims=True)
    tangent_2 = np.cross(normals, tangent_1)
    return tangent_1, tangent_2


def cap(radius_mm: float) -> tuple[np.ndarray, np.ndarray]:
    radial = np.linspace(0.0, PLACEMENT_WIDTH_MM / 2.0, 49)
    azimuth = np.linspace(0.0, 2.0 * np.pi, 192, endpoint=False)
    rr, aa = np.meshgrid(radial, azimuth, indexing="ij")
    x = (rr * np.cos(aa)).ravel()
    y = (rr * np.sin(aa)).ravel()
    z = radius_mm - np.sqrt(np.maximum(radius_mm**2 - rr.ravel() ** 2, 0.0))
    surface = np.column_stack((x, y, z))
    inward = np.column_stack((-x, -y, radius_mm - z))
    inward /= np.linalg.norm(inward, axis=1, keepdims=True)
    return surface, inward


def envelope_bounds() -> tuple[np.ndarray, np.ndarray]:
    global_min = np.full(3, np.inf)
    global_max = np.full(3, -np.inf)
    cone_angles = np.deg2rad(np.linspace(0.0, NORMAL_HALF_ANGLE_DEG, 7))
    cone_azimuths = np.linspace(0.0, 2.0 * np.pi, 72, endpoint=False)

    for radius_mm in CAP_RADII_MM:
        surface, inward = cap(radius_mm)
        tangent_1, tangent_2 = frame(inward)
        for offset_mm in SOURCE_OFFSETS_MM:
            sources = surface - offset_mm * inward
            clouds = [sources, sources + DEEP_COVERAGE_MM * inward]
            for alpha in cone_angles:
                for beta in cone_azimuths:
                    direction = (
                        math.cos(alpha) * inward
                        + math.sin(alpha) * math.cos(beta) * tangent_1
                        + math.sin(alpha) * math.sin(beta) * tangent_2
                    )
                    clouds.append(sources + FOCAL_DISTANCE_MM * direction)
            points = np.vstack(clouds)
            global_min = np.minimum(global_min, points.min(axis=0))
            global_max = np.maximum(global_max, points.max(axis=0))

    raw_min = global_min - SAFETY_MARGIN_MM
    raw_max = global_max + SAFETY_MARGIN_MM
    raw_size = raw_max - raw_min
    step_mm = GRID_SPACING_MM * NETWORK_MULTIPLE
    rounded_size = np.ceil(raw_size / step_mm) * step_mm
    extra = rounded_size - raw_size
    return raw_min - extra / 2.0, raw_max + extra / 2.0


def save_cross_section(domain_min: np.ndarray, domain_max: np.ndarray, output: Path) -> None:
    radius_mm = 100.0
    x = np.linspace(-PLACEMENT_WIDTH_MM / 2.0, PLACEMENT_WIDTH_MM / 2.0, 401)
    z = radius_mm - np.sqrt(radius_mm**2 - x**2)
    inward_x = -x / radius_mm
    inward_z = (radius_mm - z) / radius_mm

    fig, axis = plt.subplots(figsize=(11, 8))
    axis.plot(x, z, color="0.25", linewidth=3, label="outer-head surface proxy")

    for offset_mm, color in zip(SOURCE_OFFSETS_MM, ("#1f77b4", "#004c8c")):
        source_x = x - offset_mm * inward_x
        source_z = z - offset_mm * inward_z
        axis.plot(
            source_x,
            source_z,
            color=color,
            linewidth=2,
            label=f"allowed point-source shell: {offset_mm:g} mm outside surface",
        )

    central_source_z = -1.0
    axis.scatter([0], [central_source_z], s=70, color="#004c8c", zorder=5)
    axis.annotate(
        "example point source\n1 mm outside surface",
        xy=(0, central_source_z),
        xytext=(-48, -7),
        arrowprops={"arrowstyle": "->", "color": "#004c8c"},
        fontsize=10,
    )

    for distance_mm, label, color in (
        (JANG_ROI_START_MM, "Jang ROI starts: 50 mm", "#9467bd"),
        (FOCAL_DISTANCE_MM, "focus distance: 82 mm", "#d62728"),
        (DEEP_COVERAGE_MM, "Jang ROI far end: 125 mm", "#2ca02c"),
    ):
        depth = central_source_z + distance_mm
        axis.scatter([0], [depth], s=55, color=color, zorder=5)
        axis.annotate(
            label,
            xy=(0, depth),
            xytext=(12, depth),
            arrowprops={"arrowstyle": "->", "color": color},
            fontsize=10,
            color=color,
        )

    roi_top = central_source_z + JANG_ROI_START_MM
    roi = plt.Rectangle(
        (-20, roi_top),
        40,
        JANG_ROI_LENGTH_MM,
        facecolor="#9467bd",
        edgecolor="#6f42a5",
        alpha=0.12,
        linewidth=2,
        label="Jang axial ROI scale: 40 x 75 mm",
    )
    axis.add_patch(roi)

    domain = plt.Rectangle(
        (domain_min[0], domain_min[2]),
        domain_max[0] - domain_min[0],
        domain_max[2] - domain_min[2],
        fill=False,
        edgecolor="black",
        linewidth=2,
        label="rechecked geometry box",
    )
    axis.add_patch(domain)

    axis.axhspan(0, domain_max[2], color="#f2c6a0", alpha=0.08)
    axis.text(
        domain_min[0] + 3,
        domain_max[2] - 5,
        "inward side; actual scalp / skull / brain boundaries require MIDA",
        fontsize=10,
        va="bottom",
    )
    axis.text(
        domain_min[0] + 3,
        domain_min[2] + 4,
        "No anatomical thickness is drawn",
        fontsize=10,
        va="top",
        color="0.3",
    )

    axis.set_xlim(domain_min[0] - 5, domain_max[0] + 5)
    axis.set_ylim(domain_min[2] - 5, domain_max[2] + 5)
    axis.invert_yaxis()
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("lateral x (mm)")
    axis.set_ylabel("inward depth z (mm)")
    axis.set_title(
        "Placement recheck: closer source and deeper inward coverage\n"
        "Geometry schematic only - not measured MIDA anatomy",
        pad=16,
    )
    axis.grid(alpha=0.2)
    axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=9)
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    domain_min, domain_max = envelope_bounds()
    size_mm = domain_max - domain_min
    voxels = np.rint(size_mm / GRID_SPACING_MM).astype(int)
    save_cross_section(domain_min, domain_max, args.output_dir / "placement_recheck.png")

    print(
        {
            "status": "geometry_recheck_not_mida_measurement",
            "source_offset_mm": SOURCE_OFFSETS_MM,
            "deep_coverage_mm": DEEP_COVERAGE_MM,
            "domain_min_mm_xyz": domain_min.tolist(),
            "domain_max_mm_xyz": domain_max.tolist(),
            "domain_size_mm_xyz": size_mm.tolist(),
            "shape_voxels_xyz": voxels.tolist(),
            "total_voxels": int(np.prod(voxels)),
        }
    )


if __name__ == "__main__":
    main()
