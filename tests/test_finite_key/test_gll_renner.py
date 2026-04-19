"""Tests for qkdx/finite_key/gll_renner.py (Phase 1 S2.5)."""
from __future__ import annotations

import math

import numpy as np
import pytest

from qkdx.finite_key.gll_renner import (
    variation_bound, delta_smoothing,
    bb84_finite_key_length_analytic,
    bb84_finite_key_rate_per_block,
    bb84_finite_key_rate_per_signal,
    bb84_finite_key_rate_analytic,  # legacy alias
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


def test_bb84_finite_key_length_pairwise_monotone_in_N() -> None:
    """Per-signal rate pairwise increases monotonically with N."""
    per_sig_rates = []
    for N in [10**5, 10**6, 10**7, 10**8, 10**10]:
        m = int(0.1 * N)
        n = int(0.9 * N)
        ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.03, f_EC=1.2)
        per_sig_rates.append(ell / (n + m))
    # Pairwise monotone increase (up to 1e-5 noise for finite precision)
    for i in range(len(per_sig_rates) - 1):
        assert per_sig_rates[i] < per_sig_rates[i+1] + 1e-5, (
            f"Rate non-monotone at index {i}: {per_sig_rates}"
        )


def test_bb84_finite_key_near_threshold_sign_change() -> None:
    """At N=10^10, ℓ changes sign around the BB84 asymptotic threshold.

    At f_EC=1.0 (symmetric case): 1 - 2h(e) = 0 → e ≈ 0.11 (BB84 threshold).
    Check ℓ > 0 at e=0.09, ℓ < 0 at e=0.13.
    """
    N = 10**10
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell_below = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=0.09, f_EC=1.0,
    )
    ell_above = bb84_finite_key_length_analytic(
        n=n, m=m, e_x=0.13, f_EC=1.0,
    )
    assert ell_below > 0, f"e=0.09 f_EC=1.0 N=1e10: ℓ = {ell_below}"
    assert ell_above < 0, f"e=0.13 f_EC=1.0 N=1e10: ℓ = {ell_above}"


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


def test_bb84_finite_key_rate_per_block_wrapper() -> None:
    """bb84_finite_key_rate_per_block = ℓ / (n + m) (per-accepted-round)."""
    N = 10**9
    m = int(0.1 * N)
    n = int(0.9 * N)
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=0.03)
    rate = bb84_finite_key_rate_per_block(n=n, m=m, e_x=0.03)
    assert abs(rate - ell / (n + m)) < 1e-12


def test_bb84_finite_key_rate_per_signal_applies_p_sift() -> None:
    """bb84_finite_key_rate_per_signal = p_sift · (ℓ / (n+m))."""
    N = 10**9
    m = int(0.1 * N)
    n = int(0.9 * N)
    rate_block = bb84_finite_key_rate_per_block(n=n, m=m, e_x=0.03)
    rate_signal_default = bb84_finite_key_rate_per_signal(n=n, m=m, e_x=0.03)
    # Default p_sift = 0.5
    assert abs(rate_signal_default - 0.5 * rate_block) < 1e-12
    # Explicit p_sift = 0.82 (efficient BB84 at p_z=0.9)
    rate_signal_eff = bb84_finite_key_rate_per_signal(
        n=n, m=m, e_x=0.03, p_sift=0.82,
    )
    assert abs(rate_signal_eff - 0.82 * rate_block) < 1e-12


def test_bb84_finite_key_rate_per_signal_invalid_p_sift() -> None:
    with pytest.raises(ValueError, match="p_sift"):
        bb84_finite_key_rate_per_signal(n=1000, m=1000, e_x=0.05, p_sift=0.0)
    with pytest.raises(ValueError, match="p_sift"):
        bb84_finite_key_rate_per_signal(n=1000, m=1000, e_x=0.05, p_sift=1.5)


def test_legacy_rate_analytic_alias() -> None:
    """Backward-compat alias: bb84_finite_key_rate_analytic == per_block."""
    N = 10**9
    m, n = int(0.1 * N), int(0.9 * N)
    r1 = bb84_finite_key_rate_analytic(n=n, m=m, e_x=0.03)
    r2 = bb84_finite_key_rate_per_block(n=n, m=m, e_x=0.03)
    assert abs(r1 - r2) < 1e-15


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


@pytest.mark.parametrize("name,val", [
    ("eps_EC", 0.0),
    ("eps_EC", -1e-9),
    ("eps_EC", 1.0),
    ("eps_EC", 1.5),
    ("eps_PA", 0.0),
    ("eps_PA", 1.0),
    ("eps_PA", 2.0),
])
def test_bb84_finite_key_eps_EC_PA_validation(name: str, val: float) -> None:
    """Round 2 regression (dev-reviewer): ε_EC, ε_PA must be in (0, 1)."""
    kwargs = {"n": 1000, "m": 1000, "e_x": 0.05, name: val}
    with pytest.raises(ValueError, match=name):
        bb84_finite_key_length_analytic(**kwargs)


@pytest.mark.parametrize("name,val", [
    ("eps_PE", 0.0), ("eps_PE", 1.0),
    ("eps_bar", 0.0), ("eps_bar", 1.0),
])
def test_bb84_finite_key_eps_PE_bar_validation(name: str, val: float) -> None:
    """ε_PE, ε_bar validation (already present via internal helpers)."""
    kwargs = {"n": 1000, "m": 1000, "e_x": 0.05, name: val}
    with pytest.raises(ValueError):
        bb84_finite_key_length_analytic(**kwargs)


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
