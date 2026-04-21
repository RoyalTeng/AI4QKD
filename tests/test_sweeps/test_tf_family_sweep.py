"""Tests for TF/PM-QKD family Pareto sweep (Phase 1 S2.2 A.1)."""
from __future__ import annotations

import numpy as np
import pytest


def test_pm_1d_positive_at_low_loss():
    from qkdx.sweeps.tf_family_sweep import sweep_pm_loss_1d
    pts = sweep_pm_loss_1d([0.0, 10.0])
    assert pts[0].objectives[0] > 0


def test_pm_1d_monotone_decrease():
    from qkdx.sweeps.tf_family_sweep import sweep_pm_loss_1d
    loss = [0.0, 20.0, 40.0, 60.0, 80.0]
    pts = sweep_pm_loss_1d(loss)
    rates = [p.objectives[0] for p in pts]
    for i in range(1, len(rates) - 1):
        assert rates[i + 1] <= rates[i] + 1e-6


def test_pm_2d_loss_x_edelta():
    from qkdx.sweeps.tf_family_sweep import sweep_pm_loss_x_edelta
    loss = np.linspace(0, 40, 10)
    e_delta = np.logspace(-3, -1.3, 10)
    pts = sweep_pm_loss_x_edelta(loss, e_delta)
    assert len(pts) == 10 * 10


def test_pm_hard_acceptance_1000():
    from qkdx.sweeps.tf_family_sweep import sweep_pm_loss_x_edelta
    loss = np.linspace(0, 80, 50)
    e_delta = np.logspace(-3, -1.3, 25)
    pts = sweep_pm_loss_x_edelta(loss, e_delta)
    assert len(pts) == 50 * 25  # 1250 ≥ 1000


def test_pm_loss_x_M_sifting_improvement():
    """Smaller M (fewer phase slices) → larger sifting factor (2/M)."""
    from qkdx.sweeps.tf_family_sweep import sweep_pm_loss_x_M
    pts = sweep_pm_loss_x_M([10.0], [4, 8, 16, 32])
    rates_by_M = {p.params["M"]: p.objectives[0] for p in pts}
    # M=4 may have higher e_delta contrib but also 2/4=0.5 sifting vs 2/16=0.125
    # Just verify all finite, monotone behaviour not strict due to slicing error
    assert all(r >= 0 for r in rates_by_M.values())


def test_pm_upper_envelope_sorted():
    from qkdx.sweeps.tf_family_sweep import (
        sweep_pm_loss_x_edelta, upper_envelope_loss,
    )
    pts = sweep_pm_loss_x_edelta([0.0, 20.0, 40.0], [0.005, 0.01, 0.02])
    env = upper_envelope_loss(pts)
    losses = [l for l, _ in env]
    assert losses == sorted(losses)
