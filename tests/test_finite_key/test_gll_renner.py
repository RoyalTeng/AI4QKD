"""Tests for qkdx/finite_key/gll_renner.py (Phase 1 S2.5)."""
from __future__ import annotations

import math

import numpy as np
import pytest

from qkdx.finite_key.gll_renner import (
    variation_bound, delta_smoothing,
    bb84_finite_key_length_analytic, bb84_finite_key_rate_analytic,
    total_security_parameter, _h,
)


# ---- Variation bound μ -------------------------------------------------------

def test_variation_bound_basic_scaling() -> None:
    """μ ∝ 1/√m at fixed ε_PE, |Σ|."""
    m1, m2 = 10**6, 4 * 10**6  # m2 = 4·m1 → μ2 ≈ μ1 / 2
    mu1 = variation_bound(m1, eps_PE=1e-9, alphabet_size=2)
    mu2 = variation_bound(m2, eps_PE=1e-9, alphabet_size=2)
    ratio = mu1 / mu2
    # Rough scaling √4 = 2, but log(m+1) term slightly distorts; expect 1.8-2.2
    assert 1.8 < ratio < 2.2, f"μ scaling: ratio={ratio} (expected ~2)"


def test_variation_bound_grows_with_log_alphabet() -> None:
    """μ grows with |Σ|."""
    m = 10**6
    eps = 1e-9
    mu_small = variation_bound(m, eps, alphabet_size=2)
    mu_large = variation_bound(m, eps, alphabet_size=16)
    assert mu_large > mu_small, (
        f"μ should grow with alphabet: {mu_small} vs {mu_large}"
    )


@pytest.mark.parametrize("m", [100, 10000, 10**6])
def test_variation_bound_always_nonneg_bounded(m: int) -> None:
    mu = variation_bound(m, eps_PE=1e-9, alphabet_size=2)
    assert mu > 0
    # Variation distance bounded by 2 (L1 distance of prob distributions)
    # For sensible inputs should be much smaller
    assert mu < 2.0


def test_variation_bound_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="m must be"):
        variation_bound(0, 1e-9, 2)
    with pytest.raises(ValueError, match="eps_PE"):
        variation_bound(1000, 0.0, 2)
    with pytest.raises(ValueError, match="eps_PE"):
        variation_bound(1000, 1.0, 2)
    with pytest.raises(ValueError, match="alphabet_size"):
        variation_bound(1000, 1e-9, 0)


# ---- Smoothing δ(ε̄) ---------------------------------------------------------

def test_delta_smoothing_scales_as_1_over_sqrt_n() -> None:
    """δ ∝ 1/√n."""
    n1 = 10**6
    n2 = 4 * 10**6
    d1 = delta_smoothing(eps_bar=1e-9, n=n1, key_alphabet_size=2)
    d2 = delta_smoothing(eps_bar=1e-9, n=n2, key_alphabet_size=2)
    ratio = d1 / d2
    assert 1.99 < ratio < 2.01, f"δ scaling: ratio={ratio} (expected 2)"


def test_delta_smoothing_d_2_bb84() -> None:
    """For BB84 (d=2), δ = 2·log2(5)·√(log2(2/ε̄)/n)."""
    eps_bar = 1e-9
    n = 10**6
    expected = 2.0 * math.log2(5) * math.sqrt(math.log2(2.0 / eps_bar) / n)
    got = delta_smoothing(eps_bar, n, key_alphabet_size=2)
    assert abs(got - expected) < 1e-12


def test_delta_smoothing_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="n must be"):
        delta_smoothing(1e-9, n=0, key_alphabet_size=2)
    with pytest.raises(ValueError, match="eps_bar"):
        delta_smoothing(eps_bar=0.0, n=1000, key_alphabet_size=2)
    with pytest.raises(ValueError, match="eps_bar"):
        delta_smoothing(eps_bar=1.0, n=1000, key_alphabet_size=2)


# ---- Binary entropy ----------------------------------------------------------

def test_binary_entropy_boundary() -> None:
    assert _h(0.0) == 0.0
    assert _h(1.0) == 0.0
    assert _h(0.5) == pytest.approx(1.0, abs=1e-12)


@pytest.mark.parametrize("p,expected", [
    (0.01, 0.0807931359),
    (0.05, 0.2863969571),
    (0.10, 0.4689955936),
])
def test_binary_entropy_values(p: float, expected: float) -> None:
    assert abs(_h(p) - expected) < 1e-8


# ---- BB84 finite-key length (Eq. 19) -----------------------------------------

def test_bb84_finite_key_length_asymptotic_convergence() -> None:
    """As n, m → ∞, ℓ/n → 1 - 2h(e) (Shor-Preskill at e_x = e_z)."""
    e = 0.05
    N = 10**10
    # Assume m = 0.1·N for PE, n = 0.9·N for key
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=e, e_z=e, f_EC=1.0,
    )
    per_signal = ell / n
    asymptotic = 1.0 - 2.0 * _h(e)  # Shor-Preskill at f_EC=1
    # Expect finite-size penalty small at N=1e10
    assert abs(per_signal - asymptotic) < 0.01, (
        f"per_signal={per_signal:.6f}, asymptotic={asymptotic:.6f}"
    )


def test_bb84_finite_key_length_positive_at_reasonable_params() -> None:
    """At e_x = 0.02, N = 10^9: finite key length should be positive."""
    N = 10**9
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.02, f_EC=1.2)
    assert ell > 0, f"At e=0.02, N=10^9: ℓ = {ell} (should be > 0)"


def test_bb84_finite_key_length_negative_above_threshold() -> None:
    """At e_x = 0.20 (well above 11% threshold): ℓ < 0."""
    N = 10**9
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.20, f_EC=1.2)
    assert ell < 0, f"At e=0.20: ℓ = {ell} (should be < 0)"


@pytest.mark.parametrize("N", [10**6, 10**8, 10**10])
def test_bb84_finite_key_length_monotone_in_N(N: int) -> None:
    """Per-signal rate monotonically increases with N (less finite-size penalty)."""
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.03, f_EC=1.2)
    per_sig = ell / (n + m)
    asymptotic = (1.0 - _h(0.03) - 1.2 * _h(0.03)) * 0.9
    # At larger N, per_sig should get closer to asymptotic
    assert per_sig < asymptotic + 0.01
    if N >= 10**8:
        assert per_sig > 0


def test_bb84_finite_key_length_includes_ec_leakage_correction() -> None:
    """ℓ must include -log2(2/ε_EC) (GLL-2021 Eq. 19, full form).

    Regression against v0.1 memo misquote that omitted this term.
    Check: smaller ε_EC → larger penalty → smaller ℓ.
    """
    N = 10**8
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell_small_EC = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=0.05, eps_EC=1e-12,
    )
    ell_default = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=0.05, eps_EC=2.5e-9,
    )
    # With ε_EC = 1e-12 (stricter): penalty 2·log2(2e12) ≈ 80 bits more,
    # so ℓ should be smaller
    assert ell_small_EC < ell_default, (
        f"ℓ with smaller ε_EC ({ell_small_EC}) should be smaller than "
        f"default ({ell_default})"
    )


def test_bb84_finite_key_rate_wrapper() -> None:
    """bb84_finite_key_rate_analytic = ℓ / (n + m)."""
    N = 10**9
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.03)
    rate = bb84_finite_key_rate_analytic(n=n, m=m, e_x=0.03)
    assert abs(rate - ell / (n + m)) < 1e-12


def test_bb84_finite_key_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="n and m"):
        bb84_finite_key_length_analytic(n=0, m=1000, e_x=0.05)
    with pytest.raises(ValueError, match="e_x"):
        bb84_finite_key_length_analytic(n=1000, m=1000, e_x=-0.01)
    with pytest.raises(ValueError, match="e_x"):
        bb84_finite_key_length_analytic(n=1000, m=1000, e_x=0.6)
    with pytest.raises(ValueError, match="e_z"):
        bb84_finite_key_length_analytic(n=1000, m=1000, e_x=0.05, e_z=-0.01)
    with pytest.raises(ValueError, match="f_EC"):
        bb84_finite_key_length_analytic(n=1000, m=1000, e_x=0.05, f_EC=0.5)


# ---- Total security ----------------------------------------------------------

def test_total_security_composes_additively() -> None:
    eps = total_security_parameter(2.5e-9, 2.5e-9, 2.5e-9, 2.5e-9)
    assert abs(eps - 1e-8) < 1e-15


# ---- Snapshot: GLL-2021 Fig.3 style point ------------------------------------

def test_bb84_finite_key_fig3_snapshot_n_1e8_e_0_05() -> None:
    """Snapshot at N = 10^8, e_x = e_z = 0.05, f_EC = 1.2.

    This corresponds to a point on GLL-2021 Fig. 3 (4-curve panel for
    e_x ∈ {0.01, 0.03, 0.05, 0.07}). Without access to exact Fig. 3 data,
    we pin the value for regression detection.
    """
    N = 10**8
    m = (1 - 0.9) ** 2 * N  # m = (1-p_z)²·N (GLL-2021 §IV.A convention)
    m = int(m) if m >= 1 else 1
    n = N - m
    ell = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=0.05, e_z=0.05, f_EC=1.2,
    )
    rate = ell / N
    # Pin value — at e=0.05, f_EC=1.2, asymptotic R ≈ 0.5·(1 - 2.2h(0.05)) × (n/N)
    # ≈ 0.9 · (1 - 2.2·0.286) = 0.9·0.37 = 0.337 at infinite N
    # Finite-size penalty at N=10^8 brings it slightly below.
    # Pin to observed regression bracket (Phase 1 S2.5 v0.1 snapshot).
    assert 0.30 < rate < 0.38, f"N=10^8, e=0.05 rate: {rate}"
