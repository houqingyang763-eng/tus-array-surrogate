"""Complex-field metrics shared by analytic and skull gates."""

from __future__ import annotations

import math

import torch


def complex_metrics(prediction: torch.Tensor, target: torch.Tensor) -> dict[str, float]:
    error_power = torch.sum((prediction.float() - target.float()) ** 2)
    target_power = torch.sum(target.float() ** 2).clamp_min(1.0e-12)
    complex_l2 = torch.sqrt(error_power / target_power)

    pred_amplitude = torch.linalg.vector_norm(prediction.float(), dim=-1)
    true_amplitude = torch.linalg.vector_norm(target.float(), dim=-1)
    amplitude_l2 = torch.linalg.vector_norm(pred_amplitude - true_amplitude) / torch.linalg.vector_norm(
        true_amplitude
    ).clamp_min(1.0e-12)
    strong = true_amplitude >= true_amplitude.max() * 0.1
    if torch.any(strong):
        pred_phase = torch.atan2(prediction[strong, 1].float(), prediction[strong, 0].float())
        true_phase = torch.atan2(target[strong, 1].float(), target[strong, 0].float())
        phase_difference = torch.atan2(torch.sin(pred_phase - true_phase), torch.cos(pred_phase - true_phase))
        phase_mae_deg = torch.mean(torch.abs(phase_difference)) * (180.0 / math.pi)
    else:
        phase_mae_deg = torch.tensor(float("nan"), device=target.device)
    return {
        "complex_relative_l2": float(complex_l2.item()),
        "amplitude_relative_l2": float(amplitude_l2.item()),
        "phase_mae_deg_above_minus20db": float(phase_mae_deg.item()),
        "strong_point_fraction": float(strong.float().mean().item()),
    }
