"""Tests for MDI family Pareto sweeps (Phase 1 S2.2 A.1).

Reference: qkdx/sweeps/mdi_family_sweep.py
"""
from __future__ import annotations

import numpy as np
import pytest


def test_sweep_mdi_loss_1d_monotone_decrease():
    """Rate monotonically decreases with loss (after the bump crossover)."""
    from qkdx.sweeps.mdi_family_sweep import sweep_mdi_loss_1d
    loss_values = [0.0, 10.0, 20.0, 40.0, 60.0, 80.0]
    points = sweep_mdi_loss_1d(loss_values)
    assert len(points) == len(loss_values)
    rates = [p.objectives[0] for p in points]
    # Ma-Razavi MDI can have a very low rate at very low loss; beyond
    # crossover, rate should decrease.  Check global monotone non-increase
    # from 20 dB onwards (where single-photon contribution dominates).
    for i in range(2, len(rates) - 1):
        assert rates[i + 1] <= rates[i] + 1e-6, (
            f"non-monotone at loss idx {i}: {rates[i]:.2e} -> {rates[i+1]:.2e}"
        )


def test_sweep_mdi_loss_1d_positive_at_low_loss():
    """At 0 dB, MDI should give positive key rate (Ma-Razavi Fig. 4 left edge)."""
    from qkdx.sweeps.mdi_family_sweep import sweep_mdi_loss_1d
    points = sweep_mdi_loss_1d([0.0])
    assert points[0].objectives[0] > 0, (
        f"MDI rate at 0 dB should be positive, got {points[0].objectives[0]}"
    )


def test_sweep_mdi_loss_x_edev_2d_grid_size():
    """2D sweep returns |loss| × |e_d| points."""
    from qkdx.sweeps.mdi_family_sweep import sweep_mdi_loss_x_edeviation
    loss_vals = np.linspace(0, 40, 10)
    e_d_vals = np.linspace(0.005, 0.05, 10)
    points = sweep_mdi_loss_x_edeviation(loss_vals, e_d_vals)
    assert len(points) == 10 * 10


def test_sweep_mdi_loss_x_pdark_2d():
    """2D sweep over loss × p_dark, verify infrastructure works."""
    from qkdx.sweeps.mdi_family_sweep import sweep_mdi_loss_x_pdark
    loss_vals = [0.0, 20.0, 40.0]
    p_d_vals = [1e-7, 1e-6, 1e-5]
    points = sweep_mdi_loss_x_pdark(loss_vals, p_d_vals)
    assert len(points) == 3 * 3
    # Higher p_d should monotonically decrease rate at fixed loss
    # (collect rates by loss, check monotone)
    from collections import defaultdict
    by_loss = defaultdict(list)
    for p in points:
        by_loss[p.params["loss_dB_total"]].append(
            (p.params["p_d"], p.objectives[0])
        )
    for loss, tups in by_loss.items():
        tups.sort(key=lambda x: x[0])  # sort by p_d
        rates = [r for _, r in tups]
        for i in range(len(rates) - 1):
            assert rates[i + 1] <= rates[i] + 1e-10, (
                f"At loss={loss}, non-monotone in p_d: {rates}"
            )


def test_sweep_hard_acceptance_1000_points():
    """RESEARCH_PLAN §3.2 hard acceptance: ≥ 1000 sweep points per family."""
    from qkdx.sweeps.mdi_family_sweep import sweep_mdi_loss_x_edeviation
    loss_vals = np.linspace(0, 80, 50)
    e_d_vals = np.linspace(0.005, 0.05, 25)
    points = sweep_mdi_loss_x_edeviation(loss_vals, e_d_vals)
    assert len(points) == 50 * 25
    assert len(points) >= 1000


def test_upper_envelope_loss():
    """Upper envelope extraction: pick max rate at each loss."""
    from qkdx.sweeps.mdi_family_sweep import (
        sweep_mdi_loss_x_edeviation, upper_envelope_loss,
    )
    loss_vals = [0.0, 10.0, 20.0]
    e_d_vals = [0.005, 0.015, 0.030]
    points = sweep_mdi_loss_x_edeviation(loss_vals, e_d_vals)
    env = upper_envelope_loss(points)
    assert len(env) == len(loss_vals)
    # Envelope should be sorted by loss
    losses = [l for l, _ in env]
    assert losses == sorted(losses)
    # At each loss, envelope should pick the BEST rate (should match e_d=0.005)
    for (loss, rate), expected_loss in zip(env, sorted(loss_vals)):
        assert loss == pytest.approx(expected_loss)
        # Max rate at this loss across e_d values
        rates_here = [
            p.objectives[0] for p in points
            if p.params["loss_dB_total"] == expected_loss
        ]
        assert rate == max(rates_here)
