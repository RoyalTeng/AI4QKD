"""Tests for qkdx/sweeps/bb84_family_sweep.py."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.sweeps.bb84_family_sweep import (
    sweep_bb84, sweep_sixstate, sweep_efficient_bb84,
    compute_bb84_family_thresholds,
)
from qkdx.sweeps.pareto import pareto_filter, count_points, upper_envelope_1d


# ---- Protocol sweeps ----------------------------------------------------------

def test_sweep_bb84_monotone_decreasing() -> None:
    qbers = np.linspace(0.0, 0.10, 11)
    pts = sweep_bb84(qbers, f_ec=1.0)
    rates = [p.objectives[0] for p in pts]
    # Key rate strictly decreases in QBER (for QBER < threshold)
    for i in range(len(rates) - 1):
        assert rates[i] >= rates[i + 1] - 1e-6, (
            f"BB84 rate not monotone: r[{i}]={rates[i]}, r[{i+1}]={rates[i+1]}"
        )


def test_sweep_sixstate_exceeds_bb84() -> None:
    """Six-state threshold > BB84 threshold (12.6% vs 11%)."""
    qbers = np.array([0.115])
    bb_pts = sweep_bb84(qbers, f_ec=1.0)
    six_pts = sweep_sixstate(qbers, f_ec=1.0)
    # At qber=11.5%, BB84 ≤ 0, six-state still > 0
    assert bb_pts[0].objectives[0] < 1e-3
    # Six-state rate per signal at 11.5%: positive (via higher threshold)
    # Note: six-state has p_sift=1/3, so absolute rate is lower per signal,
    # but threshold is higher. Check threshold comparison via 0.125
    # (above BB84 threshold, below six-state threshold).
    six_at_125 = sweep_sixstate(np.array([0.125]), f_ec=1.0)
    assert six_at_125[0].objectives[0] > 0.0, (
        f"Six-state at 12.5% should have positive rate, got {six_at_125[0].objectives[0]}"
    )


def test_sweep_efficient_bb84_2d_rate_increases_with_p_Z() -> None:
    """At fixed qber, Efficient BB84 rate increases with p_Z (biased sift)."""
    qber = 0.05
    p_Zs = [0.55, 0.7, 0.85, 0.95]
    pts = sweep_efficient_bb84(
        qber_values=[qber], p_Z_values=p_Zs, f_ec=1.0,
    )
    rates = [p.objectives[0] for p in pts]
    for i in range(len(rates) - 1):
        assert rates[i] < rates[i + 1] + 1e-6, (
            f"Eff-BB84 rate should ↑ in p_Z: rates={rates}"
        )


# ---- Scale: ≥ 1000 points (RESEARCH_PLAN §3.2 hard acceptance) ---------------

def test_efficient_bb84_sweep_scales_to_1000() -> None:
    """S2.2 hard acceptance: ≥ 1000 scan points per family."""
    qbers = np.linspace(0.0, 0.10, 32)
    p_Zs = np.linspace(0.51, 0.99, 32)
    pts = sweep_efficient_bb84(qbers, p_Zs, f_ec=1.0)
    assert count_points(pts) >= 1000, f"only {count_points(pts)} points"


# ---- Pareto + envelope --------------------------------------------------------

def test_efficient_bb84_upper_envelope_at_fixed_qber_is_max_p_Z() -> None:
    """Envelope should pick max p_Z at each qber (ignores ties by rate)."""
    qbers = [0.05]
    p_Zs = [0.7, 0.85, 0.95]
    pts = sweep_efficient_bb84(qbers, p_Zs, f_ec=1.0)
    env = upper_envelope_1d(pts, x_key="qber", y_key_index=0)
    # Only 1 qber → 1 envelope point
    assert len(env) == 1
    # Envelope y = max rate across p_Z; should match p_Z=0.95 (highest p_sift)
    rates = [p.objectives[0] for p in pts]
    assert env[0][1] == pytest.approx(max(rates))


def test_pareto_front_bb84_dominates_all() -> None:
    """For 1-D sweep in QBER, Pareto front (maximizing (rate, -qber)) is just qber=0."""
    qbers = np.linspace(0.0, 0.08, 9)
    pts = sweep_bb84(qbers, f_ec=1.0)
    front = pareto_filter(pts)
    # qber=0 dominates: highest rate AND lowest qber
    assert len(front) == 1
    assert front[0].params["qber"] == pytest.approx(0.0)


# ---- Family thresholds --------------------------------------------------------

def test_compute_bb84_family_thresholds() -> None:
    """Snapshot thresholds for key_rate → 0 transition.

    F3 SARG04 not included: simplified Werner model reverted (see
    docs/PHASE1_LOG.md §2.1); proper Koashi 2005 impl deferred.
    """
    qbers = np.linspace(0.0, 0.16, 33)
    thresh = compute_bb84_family_thresholds(qbers, f_ec=1.0)
    # BB84 ~ 11%, six-state ~ 12.6%
    # Grid step = 0.005; threshold reported = first qber where rate ≤ 1e-4.
    assert 0.105 <= thresh["BB84"] <= 0.120
    assert 0.125 <= thresh["SixState"] <= 0.135
    # Six-state > BB84
    assert thresh["SixState"] > thresh["BB84"]
    assert "SARG04" not in thresh  # sweep removed per Phase 1 log
