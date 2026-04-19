"""Tests for qkdx/analytic/gllp.py."""
from __future__ import annotations

import pytest

from qkdx.analytic.gllp import gllp_rate, mdi_ideal_symmetric_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate


# ---- GLLP general -------------------------------------------------------------

def test_zero_qber_equals_p_sift() -> None:
    """At QBER=0 in both bases, R = p_sift · 1."""
    for p_sift in [0.1, 0.25, 0.5, 1.0]:
        assert gllp_rate(p_sift, 0.0, 0.0, f_ec=1.0) == pytest.approx(p_sift, abs=1e-12)


def test_gllp_reduces_to_shor_preskill_for_bb84() -> None:
    """Symmetric BB84 (p_sift=0.5, e_Z=e_X=e) → Shor-Preskill."""
    for e in [0.01, 0.03, 0.05, 0.08]:
        gllp = gllp_rate(p_sift=0.5, qber_Z=e, qber_X=e, f_ec=1.0)
        sp = shor_preskill_rate(e, f_ec=1.0)
        assert gllp == pytest.approx(sp, abs=1e-12)


def test_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="p_sift"):
        gllp_rate(-0.1, 0.05, 0.05)
    with pytest.raises(ValueError, match="qber_Z"):
        gllp_rate(0.5, -0.01, 0.05)
    with pytest.raises(ValueError, match="qber_X"):
        gllp_rate(0.5, 0.05, 1.2)


# ---- MDI ideal ---------------------------------------------------------------

def test_mdi_at_zero_qber() -> None:
    assert mdi_ideal_symmetric_rate(0.0, f_ec=1.0) == pytest.approx(0.25, abs=1e-12)


def test_mdi_is_bb84_halved_at_ideal() -> None:
    """Ideal symmetric MDI = BB84 / 2 (from p_sift ratio 0.25/0.5)."""
    for e in [0.0, 0.02, 0.05, 0.08]:
        mdi = mdi_ideal_symmetric_rate(e, f_ec=1.0)
        bb84 = shor_preskill_rate(e, f_ec=1.0)
        assert mdi == pytest.approx(bb84 / 2.0, abs=1e-12)


def test_mdi_threshold_same_as_bb84() -> None:
    """Ideal MDI threshold = BB84 threshold ≈ 11%.

    At e=0.105 both positive; at e=0.115 both negative.
    """
    assert mdi_ideal_symmetric_rate(0.105, f_ec=1.0) > 0.0
    assert mdi_ideal_symmetric_rate(0.115, f_ec=1.0) < 0.0
