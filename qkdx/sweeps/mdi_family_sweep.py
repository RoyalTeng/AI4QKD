"""MDI-QKD family Pareto sweep (Phase 1 S2.2, A.1).

Reference:
    - Ma-Razavi 2012, PRA 86:062319 (MDI-QKD decoy-state analysis)
    - qkdx/analytic/mdi_decoy.py (Ma-Razavi formulas)
    - docs/families/mdi_family.md

Scan WLC-level analytic MDI-QKD decoy-state key rate over:
    - 1D: loss_dB_total (symmetric, asymptotic, μ internally optimized)
    - 2D: (loss_dB_total, e_d) — optical misalignment axis
    - 2D: (loss_dB_total, p_d) — detector dark count axis

Hard acceptance (RESEARCH_PLAN §3.2):
    - ≥ 1000 points per sweep
    - Pareto upper envelope recorded

Note on "Pareto" for MDI: the 2D Pareto front collapses because all points
at fixed loss have the same μ*-optimized rate.  What we track is the
"operational Pareto" — upper envelope of rate vs loss at the best
detector-parameter fixed settings.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

import numpy as np

from qkdx.analytic.mdi_decoy import MdiDecoyParams, mdi_original_rate_optimised
from qkdx.sweeps.pareto import ParetoPoint, grid_scan_1d, grid_scan_2d


def sweep_mdi_loss_1d(
    loss_dB_total_values: Sequence[float],
    params: MdiDecoyParams | None = None,
) -> list[ParetoPoint]:
    """1D sweep: MDI asymptotic key rate vs total two-arm loss (dB).

    Args:
        loss_dB_total_values: total loss (Alice-Charlie + Bob-Charlie) in dB
        params: MdiDecoyParams (defaults = Ma-Razavi Table I)
    """
    if params is None:
        params = MdiDecoyParams()

    def evaluate(loss_dB):
        eta_fibre = 10.0 ** (-loss_dB / 20.0)  # symmetric per-arm
        eta_a = params.eta_det * eta_fibre
        eta_b = params.eta_det * eta_fibre
        rate = mdi_original_rate_optimised(eta_a, eta_b, params)

        class Result:
            def __init__(self, r):
                self.key_rate = r
                self.status = "ok"
        return Result(rate)

    def objectives(loss_dB, result):
        return (float(result.key_rate), -float(loss_dB))

    return grid_scan_1d(
        loss_dB_total_values, "loss_dB_total", evaluate, objectives,
    )


def sweep_mdi_loss_x_edeviation(
    loss_dB_total_values: Sequence[float],
    e_d_values: Sequence[float],
    params: MdiDecoyParams | None = None,
) -> list[ParetoPoint]:
    """2D sweep: loss × optical misalignment e_d.

    Pareto axes: (rate, -loss, -e_d).
    """
    if params is None:
        params = MdiDecoyParams()

    def evaluate(loss_dB, e_d):
        params_local = replace(params, e_d=e_d)
        eta_fibre = 10.0 ** (-loss_dB / 20.0)
        eta_a = params_local.eta_det * eta_fibre
        eta_b = params_local.eta_det * eta_fibre
        rate = mdi_original_rate_optimised(eta_a, eta_b, params_local)

        class Result:
            def __init__(self, r):
                self.key_rate = r
                self.status = "ok"
        return Result(rate)

    def objectives(loss_dB, e_d, result):
        return (float(result.key_rate), -float(loss_dB), -float(e_d))

    return grid_scan_2d(
        loss_dB_total_values, e_d_values,
        ("loss_dB_total", "e_d"),
        evaluate, objectives,
    )


def sweep_mdi_loss_x_pdark(
    loss_dB_total_values: Sequence[float],
    p_dark_values: Sequence[float],
    params: MdiDecoyParams | None = None,
) -> list[ParetoPoint]:
    """2D sweep: loss × dark-count probability p_d.

    Pareto axes: (rate, -loss, -p_d).
    """
    if params is None:
        params = MdiDecoyParams()

    def evaluate(loss_dB, p_d):
        params_local = replace(params, p_d=p_d)
        eta_fibre = 10.0 ** (-loss_dB / 20.0)
        eta_a = params_local.eta_det * eta_fibre
        eta_b = params_local.eta_det * eta_fibre
        rate = mdi_original_rate_optimised(eta_a, eta_b, params_local)

        class Result:
            def __init__(self, r):
                self.key_rate = r
                self.status = "ok"
        return Result(rate)

    def objectives(loss_dB, p_d, result):
        return (float(result.key_rate), -float(loss_dB), -float(p_d))

    return grid_scan_2d(
        loss_dB_total_values, p_dark_values,
        ("loss_dB_total", "p_d"),
        evaluate, objectives,
    )


def upper_envelope_loss(points: list[ParetoPoint]) -> list[tuple[float, float]]:
    """Extract upper envelope of (rate vs -loss_dB_total) Pareto points.

    Returns sorted list [(loss_dB, best_rate), ...] over all other-axis
    parameters.  Useful for plotting the operational Pareto envelope.
    """
    # Group by loss_dB (first-axis primary key)
    best_at_loss: dict[float, float] = {}
    for p in points:
        loss = p.params.get("loss_dB_total")
        if loss is None:
            continue
        rate = p.objectives[0] if p.objectives else 0.0
        if loss not in best_at_loss or rate > best_at_loss[loss]:
            best_at_loss[loss] = rate
    return sorted(best_at_loss.items(), key=lambda x: x[0])
