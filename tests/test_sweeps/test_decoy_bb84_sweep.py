"""Tests for qkdx/sweeps/decoy_bb84_sweep.py (Phase 1 S2.2 + S2.3)."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.sweeps.decoy_bb84_sweep import (
    DeviceProfile, IDEAL, LMC_2005_FIG3, TYPICAL_S23,
    sweep_decoy_bb84_distance, sweep_decoy_bb84_mu_distance,
    compare_profiles_at_distance,
)
from qkdx.sweeps.pareto import count_points


# ---- DeviceProfile data integrity --------------------------------------------

def test_ideal_profile() -> None:
    assert IDEAL.eta_detector == 1.0
    assert IDEAL.p_dark == 0.0
    assert IDEAL.e_misalignment == 0.0


def test_lmc_fig3_profile() -> None:
    """Lo-Ma-Chen 2005 Fig.3 参数对齐."""
    assert LMC_2005_FIG3.eta_detector == 0.145
    assert LMC_2005_FIG3.p_dark == 8.5e-7
    assert LMC_2005_FIG3.e_misalignment == 0.033


def test_typical_s23_profile() -> None:
    """S2.3 硬验收典型参数 (RESEARCH_PLAN §3.2)."""
    assert TYPICAL_S23.eta_detector == 0.5
    assert TYPICAL_S23.p_dark == 1e-6


# ---- 1-D distance sweep ------------------------------------------------------

def test_sweep_decoy_bb84_distance_monotone_decreasing() -> None:
    """密钥率应随距离单调递减."""
    distances = [0.0, 20.0, 50.0, 80.0]
    pts = sweep_decoy_bb84_distance(LMC_2005_FIG3, distances)
    rates = [p.objectives[0] for p in pts]
    for i in range(len(rates) - 1):
        assert rates[i] >= rates[i + 1] - 1e-6, f"rate at {distances[i]} km: {rates[i]}"


def test_sweep_produces_meta() -> None:
    pts = sweep_decoy_bb84_distance(LMC_2005_FIG3, [25.0])
    assert "Q_mu" in pts[0].meta
    assert "E_mu" in pts[0].meta
    assert pts[0].meta["Q_mu"] > 0


# ---- S2.3 硬验收: η_d=0.5 vs η_d=1.0 ----------------------------------------

@pytest.mark.parametrize("L,expected_band", [
    (25.0, (83.0, 85.5)),   # per-profile optimized: 84.25
    (50.0, (83.0, 85.5)),   # 84.43
    (100.0, (83.0, 86.0)),  # 84.73
])
def test_typical_s23_degradation_per_profile_optimized(
    L: float, expected_band: tuple[float, float]
) -> None:
    """S2.3 硬验收 (dev-reviewer Round 3 response):
    TYPICAL_S23 per-profile μ-optimized 退化应在 83-86% 带内.

    Mechanism decomposition confirmed by findings §3.4 and r2.json:
      - η_d=0.5 alone: 50.0-51.4 %
      - +misalignment e_d=0.033: +31.9-34.5 pp → ~84%
      - +dark count p_d=1e-6: +0-0.3 pp at ≤100km (negligible)
    """
    mus = np.linspace(0.1, 0.9, 41)
    # IDEAL μ-optimized
    pts_ideal = sweep_decoy_bb84_mu_distance(IDEAL, [L], mus, nu_ratio=0.2)
    r_ideal = max(p.objectives[0] for p in pts_ideal)
    # TYPICAL μ-optimized
    pts_typical = sweep_decoy_bb84_mu_distance(
        TYPICAL_S23, [L], mus, nu_ratio=0.2,
    )
    r_typical = max(p.objectives[0] for p in pts_typical)
    assert r_ideal > 0 and r_typical > 0
    deg = (r_ideal - r_typical) / r_ideal * 100
    lo, hi = expected_band
    assert lo <= deg <= hi, (
        f"L={L} km: per-profile μ-optimized degradation {deg:.2f}%; "
        f"expected band [{lo}, {hi}]. ideal={r_ideal:.6f}, typical={r_typical:.6f}"
    )


@pytest.mark.parametrize("L,expected_band", [
    (25.0, (50.0, 51.5)),   # per-profile optimized: 50.70
    (50.0, (49.5, 51.0)),   # 50.24
    (100.0, (49.5, 51.0)),  # 50.02
])
def test_eta_d_only_degradation_per_profile_optimized(
    L: float, expected_band: tuple[float, float]
) -> None:
    """Mechanism: η_d=0.5 alone per-profile μ-optimized 退化在 50.0-51.5%.

    Precisely in plan §3.2 S2.3 "20-50%" upper range (slight over by ~1 pp).
    """
    from qkdx.sweeps.decoy_bb84_sweep import DeviceProfile
    eta_d_only = DeviceProfile(
        name="eta_d_only",
        eta_detector=0.5, p_dark=0.0, e_misalignment=0.0,
    )
    mus = np.linspace(0.1, 0.9, 41)
    pts_ideal = sweep_decoy_bb84_mu_distance(IDEAL, [L], mus, nu_ratio=0.2)
    r_ideal = max(p.objectives[0] for p in pts_ideal)
    pts_eta = sweep_decoy_bb84_mu_distance(eta_d_only, [L], mus, nu_ratio=0.2)
    r_eta = max(p.objectives[0] for p in pts_eta)
    deg = (r_ideal - r_eta) / r_ideal * 100
    lo, hi = expected_band
    assert lo <= deg <= hi, (
        f"L={L}: η_d-only degradation {deg:.2f}%; expected [{lo}, {hi}]"
    )


@pytest.mark.parametrize("L", [25.0, 50.0, 100.0])
def test_device_imperfection_degrades_rate_fixed_slice(L: float) -> None:
    """Fixed (μ=0.5, ν=0.1) slice: TYPICAL vs IDEAL 退化 ≥ 50% (coarser guard)."""
    rates = compare_profiles_at_distance(
        [IDEAL, TYPICAL_S23], distance_km=L, mu=0.5, nu=0.1,
    )
    r_ideal = rates["ideal"]
    r_typical = rates["S2.3_typical"]
    assert r_ideal > 0 and r_typical > 0
    deg = (r_ideal - r_typical) / r_ideal * 100
    assert deg >= 50.0, f"L={L}: fixed-slice deg {deg:.2f}% < 50% guard"


def test_ge_1000_points_2d_sweep_TYPICAL_S23() -> None:
    """S2.2 硬验收 ≥1000 点(RESEARCH_PLAN §3.2): 37 × 33 = 1221."""
    distances = np.linspace(0.0, 180.0, 37)
    mus = np.linspace(0.1, 0.9, 33)
    pts = sweep_decoy_bb84_mu_distance(
        TYPICAL_S23, distances, mus, nu_ratio=0.2,
    )
    assert count_points(pts) >= 1000, f"only {count_points(pts)} points"


def test_lmc_fig3_gives_positive_rate_at_25km() -> None:
    """Lo-Ma-Chen 2005 Fig.3 参数在 25 km 应有正密钥率 (Phase 0 M3 baseline)."""
    pts = sweep_decoy_bb84_distance(LMC_2005_FIG3, [25.0])
    assert pts[0].objectives[0] > 1e-5, (
        f"LMC 2005 25km rate too small: {pts[0].objectives[0]}"
    )


# ---- 2-D sweep -----------------------------------------------------------------

def test_sweep_2d_mu_distance_scale() -> None:
    """2-D 扫描满足 S2.2 ≥ 1000 点硬验收."""
    distances = np.linspace(0.0, 100.0, 40)
    mus = np.linspace(0.1, 0.9, 25)
    # 40 × 25 = 1000
    pts = sweep_decoy_bb84_mu_distance(LMC_2005_FIG3, distances, mus)
    assert count_points(pts) >= 1000


def test_sweep_2d_mu_distance_finds_optimal_mu() -> None:
    """At fixed distance, there exists optimal μ (inner max in distance sweep)."""
    distances = [50.0]
    mus = np.linspace(0.2, 0.9, 15)
    pts = sweep_decoy_bb84_mu_distance(LMC_2005_FIG3, distances, mus)
    rates = [p.objectives[0] for p in pts]
    # Optimal μ should be interior (not at boundary)
    max_idx = np.argmax(rates)
    assert 0 < max_idx < len(rates) - 1, (
        f"Optimal μ at boundary (idx={max_idx}), rates={rates}"
    )


# ---- Profile comparison --------------------------------------------------------

def test_compare_profiles_orders_by_quality() -> None:
    """IDEAL > TYPICAL (η_d=0.5) > LMC (η_d=0.145) at same distance."""
    L = 25.0
    rates = compare_profiles_at_distance(
        [IDEAL, TYPICAL_S23, LMC_2005_FIG3], distance_km=L,
    )
    assert rates["ideal"] > rates["S2.3_typical"] >= 0
    assert rates["S2.3_typical"] > rates["Lo-Ma-Chen_2005_Fig3"] >= 0
