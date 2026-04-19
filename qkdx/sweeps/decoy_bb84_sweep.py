"""Decoy-state BB84 Pareto sweep with device imperfections.

Phase 1 S2.2-S2.3 实现 (RESEARCH_PLAN §3.2):
    - S2.2 Pareto 前沿数值化: 每个族扫 ≥ 1000 点
    - S2.3 器件不完美: η_d, p_d, e_misalignment 参数化
    - 硬验收 S2.3: η_d=0.5, p_d=1e-6 下 BB84 族 rate 对比理想应体现 20-50% 退化

方法:
    - 复用 qkdx.analytic.channel.FibreChannel (Ma 2005 §III 模型)
    - 复用 qkdx.numerics.decoy.decoy_wlc_rate_one (1-decoy + vacuum WLC)
    - 固定距离/强度网格扫描 (grid scan, 避免 scikit-optimize 外部依赖)

References:
    - Lo-Ma-Chen 2005, PRL 94:230504 (decoy-state security + Fig.3 benchmark)
    - Ma-Qi-Zhao-Lo 2005, PRA 72:012326 (数值基线, Y_1^L/e_1^U 公式)
    - docs/PHASE1_LOG.md §3 (Phase 1 S2.2 决策记录)
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from qkdx.analytic.channel import FibreChannel
from qkdx.numerics.decoy import decoy_wlc_rate_one
from qkdx.sweeps.pareto import ParetoPoint


@dataclass(frozen=True)
class DeviceProfile:
    """器件参数集合(固定 α, f_ec;变 η_d / p_d / e_d)."""
    name: str
    eta_detector: float
    p_dark: float
    e_misalignment: float
    alpha_db_per_km: float = 0.21
    f_ec: float = 1.22


# -- 典型器件档位 -----------------------------------------------------------------

IDEAL = DeviceProfile(
    name="ideal",
    eta_detector=1.0,
    p_dark=0.0,
    e_misalignment=0.0,
)

LMC_2005_FIG3 = DeviceProfile(
    name="Lo-Ma-Chen_2005_Fig3",
    eta_detector=0.145,
    p_dark=8.5e-7,
    e_misalignment=0.033,
)

# RESEARCH_PLAN §3.2 S2.3 硬验收典型参数
TYPICAL_S23 = DeviceProfile(
    name="S2.3_typical",
    eta_detector=0.5,
    p_dark=1e-6,
    e_misalignment=0.033,
)


def sweep_decoy_bb84_distance(
    profile: DeviceProfile,
    distance_km_values: Sequence[float],
    mu: float = 0.5,
    nu: float = 0.1,
    solver: str | None = None,
) -> list[ParetoPoint]:
    """1-D distance sweep at fixed (μ, ν) and device profile.

    Args:
        profile: device imperfection profile
        distance_km_values: fibre distances to sweep
        mu: signal intensity (default 0.5, near-optimal for LMC 2005)
        nu: decoy intensity (0 < ν < μ)
        solver: optional override

    Returns:
        List of ParetoPoint with params={"distance_km": L, "mu": mu, "nu": nu},
        objectives=(key_rate, -distance_km).
    """
    points = []
    for L in distance_km_values:
        ch = FibreChannel(
            eta_detector=profile.eta_detector,
            p_dark=profile.p_dark,
            e_misalignment=profile.e_misalignment,
            alpha_db_per_km=profile.alpha_db_per_km,
            f_ec=profile.f_ec,
            length_km=float(L),
        )
        res = decoy_wlc_rate_one(ch, mu=mu, nu=nu, solver=solver)
        points.append(ParetoPoint(
            params={"distance_km": float(L), "mu": mu, "nu": nu,
                    "profile": profile.name},
            objectives=(float(res.key_rate), -float(L)),
            meta={"Q_mu": res.Q_mu, "E_mu": res.E_mu,
                  "Y_1_lower": res.estimates.Y_1_lower,
                  "e_1_upper": res.estimates.e_1_upper,
                  "h_bits_per_sift": res.h_bits_per_sift},
        ))
    return points


def sweep_decoy_bb84_mu_distance(
    profile: DeviceProfile,
    distance_km_values: Sequence[float],
    mu_values: Sequence[float],
    nu_ratio: float = 0.2,
    solver: str | None = None,
) -> list[ParetoPoint]:
    """2-D sweep over (distance, μ) at fixed ν/μ ratio.

    For each (L, μ): set ν = nu_ratio · μ; run decoy_wlc_rate_one.

    Satisfies S2.2 hard acceptance (≥ 1000 points with reasonable grid).
    """
    points = []
    for L in distance_km_values:
        for mu in mu_values:
            nu = nu_ratio * mu
            ch = FibreChannel(
                eta_detector=profile.eta_detector,
                p_dark=profile.p_dark,
                e_misalignment=profile.e_misalignment,
                alpha_db_per_km=profile.alpha_db_per_km,
                f_ec=profile.f_ec,
                length_km=float(L),
            )
            res = decoy_wlc_rate_one(ch, mu=mu, nu=nu, solver=solver)
            points.append(ParetoPoint(
                params={"distance_km": float(L), "mu": float(mu),
                        "nu": float(nu), "profile": profile.name},
                objectives=(float(res.key_rate), -float(L)),
                meta={"Q_mu": res.Q_mu, "E_mu": res.E_mu},
            ))
    return points


def compare_profiles_at_distance(
    profiles: Sequence[DeviceProfile],
    distance_km: float,
    mu: float = 0.5,
    nu: float = 0.1,
    solver: str | None = None,
) -> dict[str, float]:
    """Compare key rates across device profiles at a single (distance, μ, ν).

    Returns:
        dict mapping profile.name → key_rate (clipped at 0 for display).
    """
    out = {}
    for profile in profiles:
        pts = sweep_decoy_bb84_distance(
            profile, [distance_km], mu=mu, nu=nu, solver=solver,
        )
        rate = pts[0].objectives[0]
        out[profile.name] = max(0.0, rate)
    return out
