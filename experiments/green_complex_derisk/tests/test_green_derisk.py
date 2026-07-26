import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytic_data import disc_quadrature, finite_disc_pressure
from green_model import GreenComplexNet
from metrics import complex_metrics


class GreenDeriskTests(unittest.TestCase):
    def test_frozen_model_shapes_and_finite_output(self):
        model = GreenComplexNet()
        centre = torch.tensor([[1.0, 0.0, 0.0], [1.0, 2.0, 3.0]])
        normal = torch.tensor([[1.0, 0.0, 0.0], [1.0, 0.1, -0.1]])
        query = torch.tensor([[64.0, 0.0, 0.0], [80.0, 4.0, -2.0]])
        pressure, transfer = model(centre, normal, query)
        self.assertEqual(tuple(pressure.shape), (2, 2))
        self.assertEqual(tuple(transfer.shape), (2, 2))
        self.assertTrue(torch.isfinite(pressure).all())

    def test_disc_quadrature_is_on_disc_plane(self):
        centre = torch.tensor([[1.0, 2.0, 3.0]])
        normal = torch.tensor([[1.0, 0.0, 0.0]])
        points = disc_quadrature(centre, normal)
        self.assertEqual(tuple(points.shape), (1, 32, 3))
        self.assertTrue(torch.allclose(points[..., 0], torch.ones(1, 32), atol=1e-6))
        self.assertLessEqual(float(torch.linalg.vector_norm(points - centre[:, None], dim=-1).max()), 5.0)

    def test_analytic_teacher_and_exact_metrics(self):
        centre = torch.tensor([[0.0, 0.0, 0.0]])
        normal = torch.tensor([[1.0, 0.0, 0.0]])
        query = torch.tensor([[100.0, 0.0, 0.0]])
        pressure = finite_disc_pressure(centre, normal, query)
        self.assertTrue(torch.isfinite(pressure).all())
        metric = complex_metrics(pressure, pressure)
        self.assertAlmostEqual(metric["complex_relative_l2"], 0.0, places=7)
        self.assertAlmostEqual(metric["phase_mae_deg_above_minus20db"], 0.0, places=7)


if __name__ == "__main__":
    unittest.main()
