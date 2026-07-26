"""Create a PPT-ready geometry figure for the current T2 candidate.

The drawing is a coordinate/coverage schematic, not measured MIDA anatomy.
It intentionally avoids inventing scalp, skull, or brain thickness.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, Polygon, Rectangle


DOMAIN_HALF_MM = 72.0
DOMAIN_Z_MIN_MM = -12.0
DOMAIN_Z_MAX_MM = 132.0
PLACEMENT_RADIUS_MM = 60.0
HEAD_RADIUS_PROXY_MM = 100.0
SOURCE_OFFSET_MIN_MM = 0.5
SOURCE_OFFSET_MAX_MM = 5.0
FOCUS_DISTANCE_MIN_MM = 55.0
FOCUS_DISTANCE_REF_MM = 82.0
FOCUS_DISTANCE_MAX_MM = 125.0
FOCUS_HALF_ANGLE_DEG = 25.0
ORIENTATION_HALF_ANGLE_DEG = 30.0
EXAMPLE_APERTURE_MM = 96.0


def surface_profile(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    radius = HEAD_RADIUS_PROXY_MM
    z = radius - np.sqrt(radius**2 - x**2)
    inward_x = -x / radius
    inward_z = (radius - z) / radius
    return z, inward_x, inward_z


def sector_polygon(origin_z: float) -> np.ndarray:
    angle = np.deg2rad(
        np.linspace(-FOCUS_HALF_ANGLE_DEG, FOCUS_HALF_ANGLE_DEG, 181)
    )
    outer = np.column_stack(
        (
            FOCUS_DISTANCE_MAX_MM * np.sin(angle),
            origin_z + FOCUS_DISTANCE_MAX_MM * np.cos(angle),
        )
    )
    inner = np.column_stack(
        (
            FOCUS_DISTANCE_MIN_MM * np.sin(angle[::-1]),
            origin_z + FOCUS_DISTANCE_MIN_MM * np.cos(angle[::-1]),
        )
    )
    return np.vstack((outer, inner))


def add_axes(axis: plt.Axes, origin: tuple[float, float], length: float = 14.0) -> None:
    ox, oz = origin
    axis.annotate(
        "",
        xy=(ox + length, oz),
        xytext=(ox, oz),
        arrowprops={"arrowstyle": "-|>", "color": "#222222", "lw": 1.5},
    )
    axis.annotate(
        "",
        xy=(ox, oz + length),
        xytext=(ox, oz),
        arrowprops={"arrowstyle": "-|>", "color": "#222222", "lw": 1.5},
    )
    axis.text(ox + length + 1.5, oz, "x", va="center", fontsize=11)
    axis.text(ox, oz + length + 1.5, "z", ha="center", fontsize=11)
    axis.text(ox - 2.5, oz - 2.0, "O", fontsize=11, weight="bold")


def create_figure(output_dir: Path) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.linewidth": 0.8,
            "svg.fonttype": "none",
        }
    )
    colors = {
        "domain": "#2b2b2b",
        "surface": "#5c6670",
        "placement": "#1779ba",
        "focus": "#ef7b45",
        "reference": "#c63c32",
        "grid": "#d8dde3",
    }

    figure = plt.figure(figsize=(15.5, 8.4), facecolor="white")
    grid = GridSpec(
        1,
        2,
        figure=figure,
        width_ratios=(1.55, 1.0),
        wspace=0.20,
    )
    side = figure.add_subplot(grid[0, 0])
    top = figure.add_subplot(grid[0, 1])

    # Sagittal/coronal geometry section.
    side.add_patch(
        Rectangle(
            (-DOMAIN_HALF_MM, DOMAIN_Z_MIN_MM),
            2 * DOMAIN_HALF_MM,
            DOMAIN_Z_MAX_MM - DOMAIN_Z_MIN_MM,
            fill=False,
            edgecolor=colors["domain"],
            linewidth=2.1,
            zorder=6,
        )
    )
    x = np.linspace(-PLACEMENT_RADIUS_MM, PLACEMENT_RADIUS_MM, 601)
    z, inward_x, inward_z = surface_profile(x)
    outer_x = x - SOURCE_OFFSET_MAX_MM * inward_x
    outer_z = z - SOURCE_OFFSET_MAX_MM * inward_z
    inner_x = x - SOURCE_OFFSET_MIN_MM * inward_x
    inner_z = z - SOURCE_OFFSET_MIN_MM * inward_z
    shell_x = np.concatenate((outer_x, inner_x[::-1]))
    shell_z = np.concatenate((outer_z, inner_z[::-1]))
    side.add_patch(
        Polygon(
            np.column_stack((shell_x, shell_z)),
            closed=True,
            facecolor=colors["placement"],
            edgecolor="none",
            alpha=0.28,
            zorder=3,
        )
    )
    side.plot(x, z, color=colors["surface"], linewidth=2.4, zorder=4)
    side.scatter(
        outer_x[::30],
        outer_z[::30],
        s=18,
        color=colors["placement"],
        edgecolors="white",
        linewidths=0.4,
        zorder=5,
    )

    source_z = -2.75
    side.add_patch(
        Polygon(
            sector_polygon(source_z),
            closed=True,
            facecolor=colors["focus"],
            edgecolor=colors["focus"],
            linewidth=1.4,
            alpha=0.23,
            zorder=2,
        )
    )
    for sign in (-1.0, 1.0):
        theta = np.deg2rad(sign * ORIENTATION_HALF_ANGLE_DEG)
        side.plot(
            [0, FOCUS_DISTANCE_MAX_MM * np.sin(theta)],
            [source_z, source_z + FOCUS_DISTANCE_MAX_MM * np.cos(theta)],
            color=colors["placement"],
            linestyle=(0, (4, 4)),
            linewidth=1.1,
            alpha=0.9,
            zorder=1,
        )

    ref_depth = source_z + FOCUS_DISTANCE_REF_MM
    side.scatter([0], [source_z], s=55, color=colors["placement"], zorder=7)
    side.scatter([0], [ref_depth], s=65, color=colors["reference"], zorder=7)
    side.plot(
        [0, 0],
        [source_z, ref_depth],
        color=colors["reference"],
        linewidth=1.2,
        alpha=0.65,
        zorder=6,
    )
    add_axes(side, (0, 0))

    side.annotate(
        "Ø120",
        xy=(0, -7.8),
        ha="center",
        va="center",
        color=colors["placement"],
        fontsize=12,
        weight="bold",
    )
    side.annotate(
        "0.5–5 mm",
        xy=(52, 11),
        xytext=(35, -5),
        arrowprops={"arrowstyle": "-", "color": colors["placement"], "lw": 1.2},
        color=colors["placement"],
        fontsize=11,
    )
    side.annotate(
        "55–125 mm",
        xy=(31, 102),
        color=colors["focus"],
        fontsize=12,
        weight="bold",
    )
    side.annotate(
        "≤25°",
        xy=(39, 57),
        color=colors["focus"],
        fontsize=12,
        weight="bold",
    )
    side.annotate(
        "82 mm",
        xy=(0, ref_depth),
        xytext=(8, ref_depth + 2),
        color=colors["reference"],
        fontsize=11,
    )
    side.annotate(
        "144 mm",
        xy=(-DOMAIN_HALF_MM, 60),
        xytext=(-DOMAIN_HALF_MM - 10, 60),
        ha="center",
        va="center",
        rotation=90,
        fontsize=11,
    )
    side.set_xlim(-88, 78)
    side.set_ylim(-17, 137)
    side.invert_yaxis()
    side.set_aspect("equal", adjustable="box")
    side.set_xticks([-72, -36, 0, 36, 72])
    side.set_yticks([-12, 24, 60, 96, 132])
    side.grid(color=colors["grid"], linewidth=0.7, alpha=0.65)
    side.set_xlabel("x (mm)")
    side.set_ylabel("inward z (mm)")
    side.set_title("Side view", loc="left", weight="bold", pad=10)

    # Axial footprint.
    top.add_patch(
        Rectangle(
            (-DOMAIN_HALF_MM, -DOMAIN_HALF_MM),
            2 * DOMAIN_HALF_MM,
            2 * DOMAIN_HALF_MM,
            fill=False,
            edgecolor=colors["domain"],
            linewidth=2.1,
        )
    )
    top.add_patch(
        Circle(
            (0, 0),
            PLACEMENT_RADIUS_MM,
            facecolor=colors["placement"],
            edgecolor=colors["placement"],
            alpha=0.22,
            linewidth=1.6,
        )
    )
    top.add_patch(
        Circle(
            (0, 0),
            EXAMPLE_APERTURE_MM / 2.0,
            fill=False,
            edgecolor=colors["placement"],
            linestyle=(0, (5, 4)),
            linewidth=1.6,
        )
    )
    focus_radius_82 = FOCUS_DISTANCE_REF_MM * np.sin(
        np.deg2rad(FOCUS_HALF_ANGLE_DEG)
    )
    top.add_patch(
        Circle(
            (0, 0),
            focus_radius_82,
            facecolor=colors["focus"],
            edgecolor=colors["focus"],
            alpha=0.22,
            linewidth=1.5,
        )
    )
    top.scatter([0], [0], s=60, color=colors["reference"], zorder=6)
    top.annotate(
        "Ø120",
        xy=(0, 61),
        ha="center",
        va="bottom",
        color=colors["placement"],
        fontsize=12,
        weight="bold",
    )
    top.annotate(
        "Ø96",
        xy=(0, -49),
        ha="center",
        va="top",
        color=colors["placement"],
        fontsize=11,
    )
    top.annotate(
        "r = 34.7 mm @ 82 mm",
        xy=(focus_radius_82 * 0.72, focus_radius_82 * 0.72),
        xytext=(17, 48),
        arrowprops={"arrowstyle": "-", "color": colors["focus"], "lw": 1.2},
        color=colors["focus"],
        fontsize=10,
    )
    top.annotate(
        "",
        xy=(22, 0),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "-|>", "color": "#222222", "lw": 1.5},
    )
    top.annotate(
        "",
        xy=(0, 22),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "-|>", "color": "#222222", "lw": 1.5},
    )
    top.text(24, 0, "x", va="center", fontsize=11)
    top.text(0, 24, "y", ha="center", fontsize=11)
    top.text(-5, -5, "O", fontsize=11, weight="bold")
    top.set_xlim(-80, 80)
    top.set_ylim(-80, 80)
    top.set_aspect("equal", adjustable="box")
    top.set_xticks([-72, -36, 0, 36, 72])
    top.set_yticks([-72, -36, 0, 36, 72])
    top.grid(color=colors["grid"], linewidth=0.7, alpha=0.65)
    top.set_xlabel("x (mm)")
    top.set_ylabel("y (mm)")
    top.set_title("Top view", loc="left", weight="bold", pad=10)

    figure.text(
        0.50,
        0.018,
        "Domain 144 × 144 × 144 mm³   |   grid 288³ @ 0.5 mm   |   "
        "placement Ø120 mm   |   conservative focus: 55–125 mm / ≤25°",
        ha="center",
        fontsize=11.5,
        color="#333333",
    )
    figure.subplots_adjust(left=0.075, right=0.975, top=0.93, bottom=0.105)

    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_dir / "t2_domain_geometry_ppt.png",
        dpi=240,
        facecolor="white",
        bbox_inches="tight",
    )
    figure.savefig(
        output_dir / "t2_domain_geometry_ppt.svg",
        facecolor="white",
        bbox_inches="tight",
    )
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    create_figure(args.output_dir)


if __name__ == "__main__":
    main()
