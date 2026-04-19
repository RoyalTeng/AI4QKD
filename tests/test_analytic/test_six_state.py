"""Tests for qkdx/analytic/six_state.py."""
from __future__ import annotations

import math

import pytest

from qkdx.analytic.six_state import (
    six_state_conditional_entropy, six_state_rate,
)


# ---- Boundary values ----------------------------------------------------------

def test_zero_qber_full_key() -> None:
    """At QBER=0: H(A|E) = 1 bit/sift, R = p_sift × 1 = 1/3 bit/signal."""
    assert six_state_conditional_entropy(0.0) == pytest.approx(1.0, abs=1e-12)
    assert six_state_rate(0.0, f_ec=1.0) == pytest.approx(1.0 / 3.0, abs=1e-12)


def test_qber_two_thirds_boundary() -> None:
    """At e=2/3: Werner coefficient 1-3e/2 = 0, formula should still be finite."""
    e = 2.0 / 3.0
    # λ_Φ+ = 0, 3 other = 2/3 total split into 3 equal = 2/9 each?
    # Actually 3·(e/2) = 3·(1/3) = 1, so λ_other = 1/3 each. Check normalization:
    # 0 + 3·(1/3) = 1 ✓
    H = six_state_conditional_entropy(e)
    # Expected H(Z(G(ρ*))) with e=2/3:
    #   diagonal ((1-e)/2, e/2, e/2, (1-e)/2) = (1/6, 1/3, 1/3, 1/6)
    #   H = 2·(1/6)·log2(6) + 2·(1/3)·log2(3)
    #     = (1/3)·log2(6) + (2/3)·log2(3)
    # Expected H(ρ*) = 3·(1/3)·log2(3) = log2(3)
    # So H_six = (1/3)log2(6) + (2/3)log2(3) - log2(3) = (1/3)log2(6) - (1/3)log2(3)
    #         = (1/3)log2(2) = 1/3
    assert H == pytest.approx(1.0 / 3.0, abs=1e-9)


# ---- Hand-computed reference (from docs/literature/six-state.md §4) ----------

def test_qber_0_05_matches_hand_computation() -> None:
    """QBER=0.05, f_ec=1.0: hand-computed R = 0.165605 bit/signal (±1e-5).

    See docs/literature/six-state.md §4: H_six = 0.783213, R = (1/3)·(H - h(e)).
    """
    R = six_state_rate(0.05, f_ec=1.0)
    assert R == pytest.approx(0.165605, abs=1e-5)


def test_qber_0_05_conditional_entropy() -> None:
    """QBER=0.05: hand-computed H(A|E) = 0.783213 bits/sift (±1e-5)."""
    H = six_state_conditional_entropy(0.05)
    assert H == pytest.approx(0.783213, abs=1e-5)


# ---- Threshold behaviour ------------------------------------------------------

def test_threshold_around_12_62_percent() -> None:
    """Six-state threshold (f_ec=1.0, Lo 2001) is ~12.62%.

    At e=0.125: R > 0
    At e=0.130: R < 0
    """
    assert six_state_rate(0.125, f_ec=1.0) > 0.0
    assert six_state_rate(0.130, f_ec=1.0) < 0.0


def test_rate_decreases_with_qber() -> None:
    """R should be monotonically decreasing in e over [0, threshold]."""
    values = [six_state_rate(e, f_ec=1.0) for e in [0.0, 0.02, 0.05, 0.08, 0.10, 0.12]]
    for prev, curr in zip(values, values[1:]):
        assert curr < prev


# ---- Relationship to BB84 -----------------------------------------------------

def test_six_state_below_bb84_at_low_qber() -> None:
    """Per-signal rate: BB84 > six-state at low QBER (higher p_sift dominates)."""
    from qkdx.analytic.shor_preskill import shor_preskill_rate
    bb84 = shor_preskill_rate(0.05, f_ec=1.0)
    six = six_state_rate(0.05, f_ec=1.0)
    assert bb84 > six


def test_six_state_per_sift_above_bb84_at_same_qber() -> None:
    """Per sifted bit: six-state ≥ BB84 (stricter Eve constraint).

    Sifted rate = R / p_sift. Six-state p_sift=1/3, BB84 p_sift=1/2.
    """
    from qkdx.analytic.shor_preskill import shor_preskill_rate
    qber = 0.08
    bb84_per_sift = shor_preskill_rate(qber, f_ec=1.0) / 0.5
    six_per_sift = six_state_rate(qber, f_ec=1.0) / (1.0 / 3.0)
    assert six_per_sift > bb84_per_sift


# ---- Input validation ---------------------------------------------------------

def test_negative_qber_raises() -> None:
    with pytest.raises(ValueError, match="QBER"):
        six_state_rate(-0.01)


def test_qber_above_two_thirds_raises() -> None:
    with pytest.raises(ValueError, match="QBER"):
        six_state_rate(0.70)
