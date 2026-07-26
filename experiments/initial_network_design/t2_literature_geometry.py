"""Literature-based T2 domain geometry when licensed MIDA voxels are unavailable.

The generated figures are explicit schematics, not MIDA anatomical slices.
They use a spherical-cap sensitivity model and show how source placement,
normal variation, propagation length, safety margin, and U-Net divisibility
combine into candidate fixed global domains.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SPACING_MM = 0.5
PATCH_WIDTHS_MM = (80.0, 100.0, 120.0)
CURVATURE_RADII_MM = (80.0, 100.0, 120.0)
SOURCE_OFFSETS_MM = (0.0, 10.0)
PATH_LENGTH_MM = 82.0
NORMAL_HALF_ANGLE_DEG = 30.0
SAFETY_MARGIN_MM = 5.0
NETWORK_MULTIPLE = 16


def round_domain_mm(length_mm: float) -> float:
    step_mm = NETWORK_MULTIPLE * SPACING_MM
    return math.ceil(length_mm / step_mm) * step_mm


def orthonormal_frame(normals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference = np.zeros_like(normals)
    reference[:, 2] = 1.0
    near_parallel = np.abs(normals[:, 2]) > 0.9
    reference[near_parallel] = np.array([1.0, 0.0, 0.0])
    tangent1 = np.cross(normals, reference)
    tangent1 /= np.linalg.norm(tangent1, axis=1, keepdims=True)
    tangent2 = np.cross(normals, tangent1)
    return tangent1, tangent2


def sampled_bounds(patch_width_mm: float, radius_mm: float) -> dict[str, object]:
    radial = np.linspace(0.0, patch_width_mm / 2.0, 25)
    azimuth = np.linspace(0.0, 2.0 * np.pi, 96, endpoint=False)
    rr, aa = np.meshgrid(radial, azimuth, indexing="ij")
    x = (rr * np.cos(aa)).ravel()
    y = (rr * np.sin(aa)).ravel()
    z = radius_mm - np.sqrt(np.maximum(radius_mm**2 - rr.ravel() ** 2, 0.0))
    surface = np.column_stack((x, y, z))

    inward = np.column_stack((-x, -y, radius_mm - z))
    inward /= np.linalg.norm(inward, axis=1, keepdims=True)
    t1, t2 = orthonormal_frame(inward)

    cone_angles = np.deg2rad(np.linspace(0.0, NORMAL_HALF_ANGLE_DEG, 7))
    cone_azimuths = np.linspace(0.0, 2.0 * np.pi, 36, endpoint=False)

    minimum = np.full(3, np.inf)
    maximum = np.full(3, -np.inf)
    endpoint_cloud: list[np.ndarray] = []
    source_cloud: list[np.ndarray] = []

    for offset in SOURCE_OFFSETS_MM:
        sources = surface - offset * inward
        minimum = np.minimum(minimum, sources.min(axis=0))
        maximum = np.maximum(maximum, sources.max(axis=0))
        if offset == max(SOURCE_OFFSETS_MM):
            source_cloud.append(sources[::24])

        for alpha in cone_angles:
            ca, sa = math.cos(alpha), math.sin(alpha)
            for beta in cone_azimuths:
                directions = (
                    ca * inward
                    + sa * math.cos(beta) * t1
                    + sa * math.sin(beta) * t2
                )
                endpoints = sources + PATH_LENGTH_MM * directions
                minimum = np.minimum(minimum, endpoints.min(axis=0))
                maximum = np.maximum(maximum, endpoints.max(axis=0))
                if (
                    offset == max(SOURCE_OFFSETS_MM)
                    and math.isclose(alpha, cone_angles[-1])
                    and beta in cone_azimuths[::6]
                ):
                    endpoint_cloud.append(endpoints[::24])

    raw_min = minimum - SAFETY_MARGIN_MM
    raw_max = maximum + SAFETY_MARGIN_MM
    raw_size = raw_max - raw_min
    rounded_size_mm = np.array([round_domain_mm(value) for value in raw_size])
    shape_voxels = np.rint(rounded_size_mm / SPACING_MM).astype(int)

    return {
        "patch_width_mm": patch_width_mm,
        "curvature_radius_mm": radius_mm,
        "raw_min_mm": raw_min.tolist(),
        "raw_max_mm": raw_max.tolist(),
        "raw_size_mm": raw_size.tolist(),
        "rounded_size_mm_xyz": rounded_size_mm.tolist(),
        "shape_voxels_xyz": shape_voxels.tolist(),
        "voxels": int(np.prod(shape_voxels)),
        "surface": surface,
        "inward": inward,
        "sources_plot": np.concatenate(source_cloud),
        "endpoints_plot": np.concatenate(endpoint_cloud),
    }


def conservative_candidates(results: list[dict[str, object]]) -> list[dict[str, object]]:
    candidates = []
    for width in PATCH_WIDTHS_MM:
        matching = [item for item in results if item["patch_width_mm"] == width]
        union_min = np.array([item["raw_min_mm"] for item in matching]).min(axis=0)
        union_max = np.array([item["raw_max_mm"] for item in matching]).max(axis=0)
        union_size = union_max - union_min
        conservative_size = np.array([round_domain_mm(value) for value in union_size])
        extra = conservative_size - union_size
        padded_min = union_min - extra / 2.0
        padded_max = union_max + extra / 2.0
        shape = np.rint(conservative_size / SPACING_MM).astype(int)
        contains_all = all(
            np.all(np.array(item["raw_min_mm"]) >= padded_min - 1e-9)
            and np.all(np.array(item["raw_max_mm"]) <= padded_max + 1e-9)
            for item in matching
        )
        candidates.append(
            {
                "patch_width_mm": width,
                "curvature_model": "union over spherical-cap radii 80/100/120 mm",
                "domain_min_mm_xyz": padded_min.tolist(),
                "domain_max_mm_xyz": padded_max.tolist(),
                "domain_size_mm_xyz": conservative_size.tolist(),
                "shape_voxels_xyz": shape.tolist(),
                "voxels": int(np.prod(shape)),
                "all_sampled_envelopes_contained": contains_all,
                "all_axes_divisible_by_16": bool(np.all(shape % NETWORK_MULTIPLE == 0)),
            }
        )
    return candidates


def save_slices(result: dict[str, object], output: Path) -> None:
    surface = result["surface"]
    sources = result["sources_plot"]
    endpoints = result["endpoints_plot"]
    raw_min = np.array(result["raw_min_mm"])
    raw_max = np.array(result["raw_max_mm"])

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    panels = (
        (0, 1, "Axial schematic (x-y)", "x (mm)", "y (mm)"),
        (0, 2, "Coronal schematic (x-z)", "x (mm)", "depth z (mm)"),
        (1, 2, "Sagittal schematic (y-z)", "y (mm)", "depth z (mm)"),
    )
    for axis, (i, j, title, xlabel, ylabel) in zip(axes, panels):
        axis.scatter(surface[::8, i], surface[::8, j], s=2, c="0.55", label="scalp cap")
        axis.scatter(sources[:, i], sources[:, j], s=4, c="#2a6fbb", label="source shell")
        axis.scatter(
            endpoints[:, i],
            endpoints[:, j],
            s=3,
            c="#d64b3c",
            alpha=0.45,
            label="82 mm cone endpoints",
        )
        rectangle = plt.Rectangle(
            (raw_min[i], raw_min[j]),
            raw_max[i] - raw_min[i],
            raw_max[j] - raw_min[j],
            fill=False,
            edgecolor="black",
            linewidth=1.5,
            label="minimum box + 5 mm",
        )
        axis.add_patch(rectangle)
        axis.set_title(title)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_aspect("equal", adjustable="box")
        axis.grid(alpha=0.2)
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4)
    fig.suptitle(
        "Literature-based geometry schematic - not an anatomical MIDA slice\n"
        f"patch={result['patch_width_mm']:.0f} mm, curvature radius="
        f"{result['curvature_radius_mm']:.0f} mm"
    )
    fig.tight_layout(rect=(0, 0.08, 1, 0.9))
    fig.savefig(output, dpi=220)
    plt.close(fig)


def save_3d(result: dict[str, object], output: Path) -> None:
    surface = result["surface"]
    sources = result["sources_plot"]
    endpoints = result["endpoints_plot"]
    raw_min = np.array(result["raw_min_mm"])
    raw_max = np.array(result["raw_max_mm"])

    fig = plt.figure(figsize=(10, 8))
    axis = fig.add_subplot(111, projection="3d")
    axis.scatter(surface[::10, 0], surface[::10, 1], surface[::10, 2], s=2, c="0.6")
    axis.scatter(sources[:, 0], sources[:, 1], sources[:, 2], s=5, c="#2a6fbb")
    axis.scatter(
        endpoints[:, 0],
        endpoints[:, 1],
        endpoints[:, 2],
        s=3,
        c="#d64b3c",
        alpha=0.35,
    )

    corners = np.array(
        [
            [x, y, z]
            for x in (raw_min[0], raw_max[0])
            for y in (raw_min[1], raw_max[1])
            for z in (raw_min[2], raw_max[2])
        ]
    )
    edges = (
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7),
    )
    for start, end in edges:
        axis.plot(*zip(corners[start], corners[end]), color="black", linewidth=1)

    axis.set_xlabel("x (mm)")
    axis.set_ylabel("y (mm)")
    axis.set_zlabel("depth z (mm)")
    axis.invert_zaxis()
    axis.set_title(
        "Placement and 82 mm / +/-30 deg envelope\n"
        "Literature-based schematic, not measured MIDA geometry"
    )
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results = [
        sampled_bounds(width, radius)
        for width in PATCH_WIDTHS_MM
        for radius in CURVATURE_RADII_MM
    ]
    candidates = conservative_candidates(results)

    serializable = []
    for item in results:
        serializable.append(
            {
                key: value
                for key, value in item.items()
                if key not in {"surface", "inward", "sources_plot", "endpoints_plot"}
            }
        )

    payload = {
        "status": "literature_estimate_not_mida_measurement",
        "assumptions": {
            "spacing_mm": SPACING_MM,
            "patch_widths_mm": PATCH_WIDTHS_MM,
            "curvature_radii_mm": CURVATURE_RADII_MM,
            "source_offset_mm": [min(SOURCE_OFFSETS_MM), max(SOURCE_OFFSETS_MM)],
            "path_length_mm": PATH_LENGTH_MM,
            "normal_half_angle_deg": NORMAL_HALF_ANGLE_DEG,
            "safety_margin_mm": SAFETY_MARGIN_MM,
            "network_multiple": NETWORK_MULTIPLE,
        },
        "sensitivity_results": serializable,
        "conservative_candidates": candidates,
    }
    (args.output_dir / "geometry_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (args.output_dir / "candidate_domains.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
                "patch_width_mm",
                "domain_x_mm",
                "domain_y_mm",
                "domain_z_mm",
                "voxels_x",
                "voxels_y",
                "voxels_z",
                "total_voxels",
            ),
        )
        writer.writeheader()
        for candidate in candidates:
            mm = candidate["domain_size_mm_xyz"]
            vox = candidate["shape_voxels_xyz"]
            writer.writerow(
                {
                    "patch_width_mm": candidate["patch_width_mm"],
                    "domain_x_mm": mm[0],
                    "domain_y_mm": mm[1],
                    "domain_z_mm": mm[2],
                    "voxels_x": vox[0],
                    "voxels_y": vox[1],
                    "voxels_z": vox[2],
                    "total_voxels": candidate["voxels"],
                }
            )

    representative = next(
        item
        for item in results
        if item["patch_width_mm"] == 100.0 and item["curvature_radius_mm"] == 100.0
    )
    save_slices(representative, args.output_dir / "literature_estimate_slices.png")
    save_3d(representative, args.output_dir / "placement_path_envelope_3d.png")
    print(json.dumps(payload["conservative_candidates"], indent=2))


if __name__ == "__main__":
    main()
