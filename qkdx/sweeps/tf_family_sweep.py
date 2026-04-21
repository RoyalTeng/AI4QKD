"""TF-QKD / PM-QKD family Pareto sweep (Phase 1 S2.2 A.1).

Reference:
    - Ma-Zeng-Zhou 2018, PRX 8:031043 (phase-matching QKD)
    - qkdx/analytic/pm_qkd.py, qkdx/analytic/pm_qkd_decoy.py
    - docs/families/tfqkd_family.md

Scan PM-QKD family (representative of TF family in MS-EB) Pareto over:
    - 1D: loss_dB_total (μ internally optimized per distance)
    - 2D: (loss_dB_total, e_delta) — misalignment + phase-slice error
    - 2D: (loss_dB_total, p_d) — detector dark count
    - 2D: (loss_dB_total, M) — phase-slice count (TF-QKD sifting factor)

Hard acceptance (RESEARCH_PLAN §3.2): ≥ 1000 points.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

import numpy as np

from qkdx.analytic.pm_qkd import PmQkdParams
from qkdx.analytic.pm_qkd_decoy import pm_optimal_mu
from qkdx.sweeps.pareto import ParetoPoint, grid_scan_1d, grid_scan_2d


def _rate_at(loss_dB: float, params: PmQkdParams, N_ph_cutoff: int = 20) -> float:
    """Helper: optimize μ at given loss and return rate."""
    eta = 10.0 ** (-loss_dB / 10.0)
    _mu_star, rate_star = pm_optimal_mu(
        eta_channel=eta, params=params, N_ph_cutoff=N_ph_cutoff,
    )
    return max(0.0, rate_star)


class _Result:
    def __init__(self, rate):
        self.key_rate = rate
        self.status = "ok"


def sweep_pm_loss_1d(
    loss_dB_total_values: Sequence[float],
    params: PmQkdParams | None = None,
) -> list[ParetoPoint]:
    """1D sweep: PM-QKD asymptotic key rate vs total loss (dB).

    Note: "loss_dB_total" is end-to-end Alice-Bob transmission loss, via
    √η per arm for TF topology.
    """
    if params is None:
        params = PmQkdParams()

    def evaluate(loss_dB):
        return _Result(_rate_at(loss_dB, params))

    def objectives(loss_dB, result):
        return (float(result.key_rate), -float(loss_dB))

    return grid_scan_1d(
        loss_dB_total_values, "loss_dB_total", evaluate, objectives,
    )


def sweep_pm_loss_x_edelta(
    loss_dB_total_values: Sequence[float],
    e_delta_values: Sequence[float],
    params: PmQkdParams | None = None,
) -> list[ParetoPoint]:
    """2D sweep: loss × e_delta (phase-slice + misalignment error)."""
    if params is None:
        params = PmQkdParams()

    def evaluate(loss_dB, e_delta):
        params_local = replace(params, e_delta=e_delta)
        return _Result(_rate_at(loss_dB, params_local))

    def objectives(loss_dB, e_delta, result):
        return (float(result.key_rate), -float(loss_dB), -float(e_delta))

    return grid_scan_2d(
        loss_dB_total_values, e_delta_values,
        ("loss_dB_total", "e_delta"),
        evaluate, objectives,
    )


def sweep_pm_loss_x_pdark(
    loss_dB_total_values: Sequence[float],
    p_dark_values: Sequence[float],
    params: PmQkdParams | None = None,
) -> list[ParetoPoint]:
    """2D sweep: loss × p_d (detector dark count)."""
    if params is None:
        params = PmQkdParams()

    def evaluate(loss_dB, p_d):
        params_local = replace(params, p_d=p_d)
        return _Result(_rate_at(loss_dB, params_local))

    def objectives(loss_dB, p_d, result):
        return (float(result.key_rate), -float(loss_dB), -float(p_d))

    return grid_scan_2d(
        loss_dB_total_values, p_dark_values,
        ("loss_dB_total", "p_d"),
        evaluate, objectives,
    )


def sweep_pm_loss_x_M(
    loss_dB_total_values: Sequence[float],
    M_values: Sequence[int],
    params: PmQkdParams | None = None,
) -> list[ParetoPoint]:
    """2D sweep: loss × M (number of phase slices, TF-QKD sifting factor)."""
    if params is None:
        params = PmQkdParams()

    def evaluate(loss_dB, M):
        params_local = replace(params, M=int(M))
        return _Result(_rate_at(loss_dB, params_local))

    def objectives(loss_dB, M, result):
        return (float(result.key_rate), -float(loss_dB), -float(M))

    return grid_scan_2d(
        loss_dB_total_values, M_values,
        ("loss_dB_total", "M"),
        evaluate, objectives,
    )


def upper_envelope_loss(points: list[ParetoPoint]) -> list[tuple[float, float]]:
    """Extract upper envelope rate vs loss from a 2D sweep."""
    best_at_loss: dict[float, float] = {}
    for p in points:
        loss = p.params.get("loss_dB_total")
        if loss is None:
            continue
        rate = p.objectives[0] if p.objectives else 0.0
        if loss not in best_at_loss or rate > best_at_loss[loss]:
            best_at_loss[loss] = rate
    return sorted(best_at_loss.items(), key=lambda x: x[0])
