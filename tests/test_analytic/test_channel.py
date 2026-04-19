"""Tests for qkdx/analytic/channel.py."""
from __future__ import annotations

import math

import pytest

from qkdx.analytic.channel import FibreChannel, DEFAULT_ALPHA_DB_PER_KM


# ---- Validation ---------------------------------------------------------------

def test_defaults_match_lo_ma_chen_2005() -> None:
    ch = FibreChannel()
    assert ch.eta_detector == 0.145
    assert ch.p_dark == 8.5e-7
    assert ch.e_misalignment == 0.033
    assert ch.alpha_db_per_km == DEFAULT_ALPHA_DB_PER_KM
    assert ch.f_ec == 1.22


def test_negative_params_raise() -> None:
    with pytest.raises(ValueError):
        FibreChannel(eta_detector=-0.1)
    with pytest.raises(ValueError):
        FibreChannel(p_dark=1.5)
    with pytest.raises(ValueError):
        FibreChannel(length_km=-5.0)
    with pytest.raises(ValueError):
        FibreChannel(f_ec=0.5)


# ---- Transmissivity ----------------------------------------------------------

def test_zero_length_transmissivity() -> None:
    ch = FibreChannel(length_km=0.0)
    assert ch.line_transmissivity() == pytest.approx(1.0, abs=1e-12)
    assert ch.total_transmissivity() == pytest.approx(0.145, abs=1e-12)


def test_100km_transmissivity() -> None:
    ch = FibreChannel(length_km=100.0, alpha_db_per_km=0.2)
    expected = 10 ** (-20.0 / 10.0)  # 0.01
    assert ch.line_transmissivity() == pytest.approx(expected, rel=1e-10)


# ---- Yields ------------------------------------------------------------------

def test_Y_0_is_dark_count_OR() -> None:
    p_dc = 1e-5
    ch = FibreChannel(p_dark=p_dc)
    expected_Y0 = 1 - (1 - p_dc) ** 2  # ≈ 2·p_dc for small p_dc
    assert ch.Y_0() == pytest.approx(expected_Y0, rel=1e-10)


def test_Y_1_formula() -> None:
    """Y_1 = 1 - (1-Y_0)(1-η) (Ma 2005 Eq. 16 n=1)."""
    ch = FibreChannel(length_km=50.0)
    eta = ch.total_transmissivity()
    Y0 = ch.Y_0()
    expected = 1 - (1 - Y0) * (1 - eta)
    assert ch.Y_n(1) == pytest.approx(expected, rel=1e-12)


def test_Y_n_monotonic_in_n() -> None:
    ch = FibreChannel(length_km=50.0)
    for n in range(5):
        assert ch.Y_n(n + 1) > ch.Y_n(n) - 1e-15  # non-decreasing


# ---- QBERs -------------------------------------------------------------------

def test_e_0_is_half() -> None:
    ch = FibreChannel()
    assert ch.e_n(0) == 0.5


def test_e_n_matches_ma_2005_eq_17() -> None:
    ch = FibreChannel(length_km=50.0, eta_detector=0.145, p_dark=8.5e-7, e_misalignment=0.033)
    eta = ch.total_transmissivity()
    Y0 = ch.Y_0()
    n = 2
    Y_n = 1 - (1 - Y0) * (1 - eta) ** n
    expected = (0.5 * Y0 + 0.033 * (1 - (1 - eta) ** n)) / Y_n
    assert ch.e_n(n) == pytest.approx(expected, rel=1e-12)


# ---- Gain Q_μ: closed-form check ---------------------------------------------

def test_Q_mu_closed_form() -> None:
    """Q_μ = 1 - (1-Y_0)·exp(-η·μ) (analytic result)."""
    ch = FibreChannel(length_km=30.0)
    for mu in [0.01, 0.1, 0.5, 1.0, 2.0]:
        eta = ch.total_transmissivity()
        Y0 = ch.Y_0()
        expected = 1 - (1 - Y0) * math.exp(-eta * mu)
        assert ch.Q_mu(mu) == pytest.approx(expected, rel=1e-12)


def test_E_mu_Q_mu_closed_form() -> None:
    """E_μ · Q_μ = e_0·Y_0 + e_d·(1 - exp(-η·μ))."""
    ch = FibreChannel(length_km=30.0)
    for mu in [0.1, 0.5, 1.0]:
        eta = ch.total_transmissivity()
        Y0 = ch.Y_0()
        expected = 0.5 * Y0 + 0.033 * (1 - math.exp(-eta * mu))
        assert ch.E_mu_times_Q_mu(mu) == pytest.approx(expected, rel=1e-12)


def test_Q_mu_matches_sum_over_n() -> None:
    """Q_μ closed form must match explicit Σ p(n;μ) Y_n up to truncation."""
    ch = FibreChannel(length_km=30.0)
    for mu in [0.1, 0.5, 1.0, 2.0]:
        explicit = 0.0
        for n in range(100):
            p_n = mu ** n * math.exp(-mu) / math.factorial(n)
            explicit += p_n * ch.Y_n(n)
        assert ch.Q_mu(mu) == pytest.approx(explicit, abs=1e-10)


# ---- Physical boundary behaviour ---------------------------------------------

def test_zero_intensity_gives_Y_0() -> None:
    ch = FibreChannel()
    assert ch.Q_mu(0.0) == pytest.approx(ch.Y_0(), abs=1e-12)


def test_zero_intensity_E_μ_is_e_0() -> None:
    ch = FibreChannel()
    assert ch.E_mu(0.0) == pytest.approx(ch.e_zero_photon, abs=1e-9)


def test_long_distance_large_QBER() -> None:
    """At very long distance η → 0, so Q_μ → Y_0 and E_μ → 0.5 (dark-dominated)."""
    ch = FibreChannel(length_km=500.0)
    assert ch.Q_mu(0.5) == pytest.approx(ch.Y_0(), rel=1e-3)
    assert ch.E_mu(0.5) == pytest.approx(0.5, rel=1e-2)
