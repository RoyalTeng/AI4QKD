"""Pareto frontier extraction for QKD parameter sweeps.

Phase 1 S2.2 infrastructure (RESEARCH_PLAN §3.2):
    - Grid/random scan over protocol parameter space
    - Pareto frontier extraction from (objective_1, ..., objective_k) points
    - Maximisation convention: a point X dominates Y iff ∀i: X_i ≥ Y_i, ∃j: X_j > Y_j

Typical QKD usage:
    - objectives = (rate, -qber)                [rate-maximize, qber-minimize]
    - objectives = (rate, -total_signals)       [rate vs finite-key overhead]

Design notes:
    - No external deps (scipy/numpy only) — BO integration (scikit-optimize,
      CMA-ES) deferred to Phase 1 S2.2 Week 4-8 extension
    - Grid scan satisfies S2.2 "每个族能在参数空间扫 ≥ 1000 个点" for
      small parameter dimensions (≤ 3D)
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class ParetoPoint:
    """One point in a Pareto scan.

    Attributes:
        params: dict of parameter values (e.g. {"qber": 0.05, "p_Z": 0.9}).
        objectives: tuple of objective values (maximisation convention).
        meta: optional diagnostics (solver status, timing, etc.).
    """
    params: dict[str, float]
    objectives: tuple[float, ...]
    meta: dict[str, object] = field(default_factory=dict)


def pareto_filter(points: Sequence[ParetoPoint]) -> list[ParetoPoint]:
    """Extract non-dominated points (Pareto frontier) under maximisation.

    A point X is *dominated* iff there exists Y ≠ X with Y_i ≥ X_i ∀i and
    strict > in at least one dim.  Pareto front = undominated points.

    Complexity: O(n²) in the number of points — acceptable for typical
    QKD sweeps (n ≤ 10⁴).  For larger scans, use skyline algorithms or
    dimension-specific shortcuts.

    Args:
        points: candidate points.

    Returns:
        List of non-dominated points, preserving input order.
    """
    n = len(points)
    if n == 0:
        return []
    dim = len(points[0].objectives)
    # Validate dim consistency
    for p in points:
        if len(p.objectives) != dim:
            raise ValueError(
                f"Objective dim mismatch: expected {dim}, got {len(p.objectives)}"
            )
    front: list[ParetoPoint] = []
    for i, p in enumerate(points):
        dominated = False
        for j, q in enumerate(points):
            if i == j:
                continue
            if _dominates(q.objectives, p.objectives):
                dominated = True
                break
        if not dominated:
            front.append(p)
    return front


def _dominates(a: tuple[float, ...], b: tuple[float, ...]) -> bool:
    """True iff a strictly dominates b (maximisation: a_i >= b_i ∀i, a_j > b_j some j)."""
    strict = False
    for ai, bi in zip(a, b):
        if ai < bi:
            return False
        if ai > bi:
            strict = True
    return strict


def grid_scan_1d(
    values: Sequence[float],
    param_name: str,
    evaluator,
    objectives_from_result,
) -> list[ParetoPoint]:
    """Scan a 1-D parameter range, collect objectives.

    Args:
        values: 1-D array of parameter values.
        param_name: name of the parameter (for ParetoPoint.params key).
        evaluator: callable(value) → result object (e.g. WLCResult).
        objectives_from_result: callable(value, result) → tuple[float,...].

    Returns:
        List of ParetoPoint, one per value.
    """
    out = []
    for v in values:
        result = evaluator(v)
        objs = objectives_from_result(v, result)
        out.append(ParetoPoint(params={param_name: float(v)}, objectives=objs))
    return out


def grid_scan_2d(
    values_x: Sequence[float],
    values_y: Sequence[float],
    param_names: tuple[str, str],
    evaluator,
    objectives_from_result,
) -> list[ParetoPoint]:
    """Scan a 2-D grid.

    Args:
        values_x, values_y: 1-D arrays of parameter values.
        param_names: (x_name, y_name).
        evaluator: callable(x, y) → result.
        objectives_from_result: callable(x, y, result) → tuple[float,...].
    """
    out = []
    for x in values_x:
        for y in values_y:
            result = evaluator(x, y)
            objs = objectives_from_result(x, y, result)
            out.append(ParetoPoint(
                params={param_names[0]: float(x), param_names[1]: float(y)},
                objectives=objs,
            ))
    return out


def count_points(points: Sequence[ParetoPoint]) -> int:
    """Count total sweep points (S2.2 hard acceptance: ≥ 1000)."""
    return len(points)


def upper_envelope_1d(
    points: Sequence[ParetoPoint],
    x_key: str,
    y_key_index: int = 0,
) -> list[tuple[float, float]]:
    """Extract (x, max_y) upper envelope over a free parameter x.

    For cases where the Pareto front is the upper envelope in a 1-D
    projection (e.g. "max rate over all p_Z at fixed qber").

    Args:
        points: scan points.
        x_key: param dimension to project onto.
        y_key_index: which objective is the y-axis (default 0).

    Returns:
        List of (x, max_y) tuples sorted by x.
    """
    buckets: dict[float, float] = {}
    for p in points:
        x = p.params[x_key]
        y = p.objectives[y_key_index]
        if x not in buckets or y > buckets[x]:
            buckets[x] = y
    return sorted(buckets.items())
