"""Tests for qkdx/numerics/decoy.py (WLC + decoy integration)."""
from __future__ import annotations

import pytest

from qkdx.analytic.channel import FibreChannel
from qkdx.analytic.decoy import (
    estimate_decoy_vacuum, decoy_rate_gllp,
)
from qkdx.numerics.decoy import (
    decoy_wlc_rate_one, decoy_wlc_rate_two,
)


_FALLBACK_TOL = dict(rel=0.02, abs=1e-3)


# ---- WLC decoy matches analytic decoy+GLLP (single-photon BB84 equivalence) --

@pytest.mark.parametrize("length_km", [10.0, 50.0, 100.0])
def test_wlc_decoy_matches_analytic_single_photon(length_km: float) -> None:
    """Consistency: WLC-decoy rate = analytic decoy_rate_gllp.

    Both use the same (Y_1^L, e_1^U) from decoy estimation; the difference is
    whether we use the WLC SDP or the analytic BB84 formula 1-h(e) for the
    single-photon H(A|E).  In the symmetric case they are equivalent.
    """
    ch = FibreChannel(length_km=length_km)
    mu, nu = 0.5, 0.1

    wlc_res = decoy_wlc_rate_one(ch, mu, nu)

    # Analytic GLLP using the same estimates
    est = estimate_decoy_vacuum(ch, mu, nu)
    Q_mu = ch.Q_mu(mu)
    E_mu = ch.E_mu(mu)
    analytic = decoy_rate_gllp(est, Q_mu, E_mu, f_ec=ch.f_ec)

    assert wlc_res.key_rate == pytest.approx(analytic, **_FALLBACK_TOL), (
        f"L={length_km}: WLC={wlc_res.key_rate:.6e}, analytic={analytic:.6e}"
    )


# ---- Short distance: R > 0 ---------------------------------------------------

def test_wlc_decoy_positive_at_50km() -> None:
    ch = FibreChannel(length_km=50.0)
    res = decoy_wlc_rate_one(ch, mu=0.5, nu=0.1)
    assert res.key_rate > 0.0


# ---- Long distance: R < 0 ----------------------------------------------------

def test_wlc_decoy_negative_at_300km() -> None:
    ch = FibreChannel(length_km=300.0)
    res = decoy_wlc_rate_one(ch, mu=0.5, nu=0.1)
    assert res.key_rate < 0.0


# ---- Distance monotonicity ---------------------------------------------------

def test_wlc_decoy_monotone_decreasing_in_length() -> None:
    rates = []
    for L in [0.0, 25.0, 50.0, 100.0, 150.0]:
        ch = FibreChannel(length_km=L)
        res = decoy_wlc_rate_one(ch, mu=0.5, nu=0.1)
        rates.append(res.key_rate)
    for prev, curr in zip(rates, rates[1:]):
        assert curr <= prev + 1e-9


# ---- 2-decoy: consistency with 1-decoy at overlapping intensity --------------

def test_2decoy_close_to_1decoy_numerically() -> None:
    """WLC-2decoy with ν₂ → 0 ≈ WLC-1decoy (both approach single-photon limit)."""
    ch = FibreChannel(length_km=50.0)
    r1 = decoy_wlc_rate_one(ch, mu=0.5, nu=0.1)
    r2 = decoy_wlc_rate_two(ch, mu=0.5, nu_1=0.1, nu_2=1e-4)
    assert r2.key_rate == pytest.approx(r1.key_rate, rel=0.05)


# ---- Result metadata ---------------------------------------------------------

def test_result_metadata_populated() -> None:
    ch = FibreChannel(length_km=50.0)
    res = decoy_wlc_rate_one(ch, mu=0.5, nu=0.1)
    assert res.scheme == "1-decoy-vacuum"
    assert res.Q_mu > 0
    assert 0 <= res.E_mu <= 0.5
    assert res.estimates.Y_1_lower >= 0
    assert 0 <= res.estimates.e_1_upper <= 0.5
    assert res.h_bits_per_sift >= 0
