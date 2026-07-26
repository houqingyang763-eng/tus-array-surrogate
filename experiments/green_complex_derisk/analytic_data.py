"""Analytic finite-disc teacher used by the V2 representation gate."""

from __future__ import annotations

import math

import torch


def perpendicular_basis(normal: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    normal = torch.nn.functional.normalize(normal, dim=-1)
    x_axis = torch.zeros_like(normal)
    x_axis[..., 0] = 1.0
    y_axis = torch.zeros_like(normal)
    y_axis[..., 1] = 1.0
    reference = torch.where((normal[..., :1].abs() < 0.9), x_axis, y_axis)
    first = torch.nn.functional.normalize(torch.linalg.cross(normal, reference, dim=-1), dim=-1)
    second = torch.linalg.cross(normal, first, dim=-1)
    return first, second


def disc_quadrature(
    centre_mm: torch.Tensor, normal: torch.Tensor, diameter_mm: float = 10.0, points: int = 32
) -> torch.Tensor:
    """Return deterministic equal-weight sunflower points over each circular element."""
    first, second = perpendicular_basis(normal)
    index = torch.arange(points, device=centre_mm.device, dtype=centre_mm.dtype)
    radius = 0.5 * diameter_mm * torch.sqrt((index + 0.5) / points)
    angle = index * (math.pi * (3.0 - math.sqrt(5.0)))
    offsets = radius[None, :, None] * (
        torch.cos(angle)[None, :, None] * first[:, None, :]
        + torch.sin(angle)[None, :, None] * second[:, None, :]
    )
    return centre_mm[:, None, :] + offsets


def finite_disc_pressure(
    centre_mm: torch.Tensor,
    normal: torch.Tensor,
    query_mm: torch.Tensor,
    *,
    frequency_hz: float = 500_000.0,
    sound_speed_m_s: float = 1500.0,
    pressure_pa: float = 100_000.0,
    reference_distance_mm: float = 100.0,
    quadrature_points: int = 32,
) -> torch.Tensor:
    """Equal-weight Rayleigh-style sum of point Green kernels over a 10 mm disc."""
    element_points = disc_quadrature(centre_mm, normal, points=quadrature_points)
    delta_mm = query_mm[:, None, :] - element_points
    distance_mm = torch.linalg.vector_norm(delta_mm, dim=-1).clamp_min(1.0e-3)
    phase = (2.0 * math.pi * frequency_hz / sound_speed_m_s) * distance_mm * 1.0e-3
    magnitude = reference_distance_mm / distance_mm
    real = torch.mean(magnitude * torch.cos(phase), dim=-1)
    imag = torch.mean(magnitude * torch.sin(phase), dim=-1)
    return pressure_pa * torch.stack((real, imag), dim=-1)


def make_source_split(device: torch.device, seed: int = 20260719) -> dict[str, torch.Tensor]:
    generator = torch.Generator(device="cpu").manual_seed(seed)

    train_yz = torch.empty(64, 2).uniform_(-15.0, 15.0, generator=generator)
    train_centres = torch.cat((torch.ones(64, 1), train_yz), dim=1)
    train_focus = torch.cat((
        torch.empty(64, 1).uniform_(70.0, 120.0, generator=generator),
        torch.empty(64, 2).uniform_(-20.0, 20.0, generator=generator),
    ), dim=1)

    angles = torch.arange(16, dtype=torch.float32) * (2.0 * math.pi / 16.0) + math.pi / 16.0
    radii = torch.linspace(23.0, 29.0, 16)
    test_centres = torch.stack((torch.ones(16), radii * torch.cos(angles), radii * torch.sin(angles)), dim=1)
    test_focus = torch.stack((
        torch.linspace(75.0, 115.0, 16),
        18.0 * torch.sin(angles * 1.7),
        18.0 * torch.cos(angles * 1.3),
    ), dim=1)

    return {
        "train_centres": train_centres.to(device),
        "train_normals": torch.nn.functional.normalize(train_focus - train_centres, dim=-1).to(device),
        "test_centres": test_centres.to(device),
        "test_normals": torch.nn.functional.normalize(test_focus - test_centres, dim=-1).to(device),
    }


def sample_queries(
    centre_mm: torch.Tensor, normal: torch.Tensor, generator: torch.Generator
) -> torch.Tensor:
    first, second = perpendicular_basis(normal)
    count = centre_mm.shape[0]
    axial = torch.empty(count, 1, device=centre_mm.device).uniform_(20.0, 180.0, generator=generator)
    lateral_1 = torch.empty(count, 1, device=centre_mm.device).uniform_(-55.0, 55.0, generator=generator)
    lateral_2 = torch.empty(count, 1, device=centre_mm.device).uniform_(-55.0, 55.0, generator=generator)
    return centre_mm + axial * normal + lateral_1 * first + lateral_2 * second
