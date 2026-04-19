"""BB84 family Pareto sweep (Phase 1 S2.2 Week 4-8).

Scan WLC SDP key rate over BB84 family parameter spaces:
    - F1 BB84:          (qber,)         1-D, Pareto collapses to threshold function
    - F2 Six-state:     (qber,)         1-D
    - F4 Efficient BB84: (qber, p_Z)    2-D, true Pareto in p_Z at each qber

F3 SARG04 deferred: proper implementation requires an announcement classical
register in MS-EB A (Alice's pair choice), which is not currently supported.
The simplified Werner model tried in commit a6e8192 was reverted in the
subsequent commit because its ~14.1% threshold does not match Koashi 2005
exact ~9.68% — see docs/PHASE1_LOG.md §2.1 for full rationale.

Hard acceptance (RESEARCH_PLAN §3.2):
    - Each family scan ≥ 1000 points
    - Pareto upper envelope recorded in docs/findings/pareto_<family>.md
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.protocols.efficient_bb84 import build_efficient_bb84_protocol
from qkdx.protocols.sixstate import build_sixstate_protocol
from qkdx.sweeps.pareto import ParetoPoint, grid_scan_1d, grid_scan_2d


def sweep_bb84(qber_values: Sequence[float], f_ec: float = 1.0) -> list[ParetoPoint]:
    """F1 BB84 sweep over QBER axis."""
    def evaluate(qber: float):
        p = build_bb84_protocol(qber)
        obs = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.5}
        return wlc_key_rate(p, obs, f_ec=f_ec)

    def objectives(qber: float, result) -> tuple[float, ...]:
        return (float(result.key_rate), -float(qber))

    return grid_scan_1d(qber_values, "qber", evaluate, objectives)


def sweep_sixstate(qber_values: Sequence[float], f_ec: float = 1.0) -> list[ParetoPoint]:
    """F2 Six-state sweep over QBER axis."""
    def evaluate(qber: float):
        p = build_sixstate_protocol(qber)
        # Six-state p_sift = 1/3 (3-basis match)
        obs = {"qber_Z": qber, "qber_X": qber, "qber_Y": qber, "p_sift": 1.0 / 3.0}
        return wlc_key_rate(p, obs, f_ec=f_ec)

    def objectives(qber: float, result) -> tuple[float, ...]:
        return (float(result.key_rate), -float(qber))

    return grid_scan_1d(qber_values, "qber", evaluate, objectives)


def sweep_efficient_bb84(
    qber_values: Sequence[float],
    p_Z_values: Sequence[float],
    f_ec: float = 1.0,
) -> list[ParetoPoint]:
    """F4 Efficient BB84 2-D sweep over (QBER, p_Z).

    Note: p_Z must be in (0.5, 1.0) strictly (build_efficient_bb84_protocol validates).
    """
    def evaluate(qber: float, p_Z: float):
        p = build_efficient_bb84_protocol(qber=qber, p_Z=p_Z)
        p_sift = p_Z ** 2 + (1 - p_Z) ** 2
        obs = {"qber_Z": qber, "qber_X": qber, "p_sift": p_sift}
        return wlc_key_rate(p, obs, f_ec=f_ec)

    def objectives(qber: float, p_Z: float, result) -> tuple[float, ...]:
        return (float(result.key_rate), -float(qber))

    return grid_scan_2d(
        qber_values, p_Z_values, ("qber", "p_Z"),
        evaluate, objectives,
    )


def compute_bb84_family_thresholds(
    qber_values: Sequence[float],
    f_ec: float = 1.0,
) -> dict[str, float]:
    """Find QBER at which each protocol's key rate first drops to 0.

    F3 SARG04 not included: see module docstring + docs/PHASE1_LOG.md §2.1.

    Returns:
        dict mapping protocol name → threshold QBER (np.nan if not found in sweep).
    """
    out: dict[str, float] = {}
    for name, sweep_fn in [
        ("BB84", sweep_bb84),
        ("SixState", sweep_sixstate),
    ]:
        pts = sweep_fn(qber_values, f_ec=f_ec)
        threshold = float("nan")
        for p in pts:
            if p.objectives[0] <= 1e-4:  # rate effectively zero
                threshold = p.params["qber"]
                break
        out[name] = threshold
    return out
