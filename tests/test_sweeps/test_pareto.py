"""Tests for qkdx/sweeps/pareto.py (Phase 1 S2.2 infrastructure)."""
from __future__ import annotations

import pytest

from qkdx.sweeps.pareto import (
    ParetoPoint, pareto_filter, _dominates,
    grid_scan_1d, grid_scan_2d, count_points, upper_envelope_1d,
)


# ---- ParetoPoint + dominance --------------------------------------------------

def test_dominates_basic() -> None:
    assert _dominates((2.0, 3.0), (1.0, 2.0)) is True
    assert _dominates((1.0, 2.0), (2.0, 3.0)) is False
    assert _dominates((1.0, 2.0), (1.0, 2.0)) is False  # equal, no strict


def test_dominates_weak_edge() -> None:
    # Same in one coord, strictly > in other
    assert _dominates((1.0, 3.0), (1.0, 2.0)) is True
    # Mixed
    assert _dominates((2.0, 1.0), (1.0, 2.0)) is False


# ---- pareto_filter ------------------------------------------------------------

def test_pareto_filter_empty() -> None:
    assert pareto_filter([]) == []


def test_pareto_filter_single_point() -> None:
    p = ParetoPoint(params={"x": 1.0}, objectives=(1.0,))
    assert pareto_filter([p]) == [p]


def test_pareto_filter_all_dominated_by_one() -> None:
    pts = [
        ParetoPoint(params={"x": 1}, objectives=(1.0, 1.0)),
        ParetoPoint(params={"x": 2}, objectives=(2.0, 2.0)),  # dominates all
        ParetoPoint(params={"x": 3}, objectives=(0.5, 0.5)),
    ]
    front = pareto_filter(pts)
    assert len(front) == 1
    assert front[0].params["x"] == 2


def test_pareto_filter_two_incomparable() -> None:
    """Two points differing in trade-off direction should both be on front."""
    pts = [
        ParetoPoint(params={"x": 1}, objectives=(1.0, 2.0)),
        ParetoPoint(params={"x": 2}, objectives=(2.0, 1.0)),
        ParetoPoint(params={"x": 3}, objectives=(0.5, 0.5)),  # dominated
    ]
    front = pareto_filter(pts)
    assert len(front) == 2
    xs = {p.params["x"] for p in front}
    assert xs == {1, 2}


def test_pareto_filter_dim_mismatch_raises() -> None:
    pts = [
        ParetoPoint(params={"x": 1}, objectives=(1.0, 2.0)),
        ParetoPoint(params={"x": 2}, objectives=(1.0,)),  # wrong dim
    ]
    with pytest.raises(ValueError, match="dim mismatch"):
        pareto_filter(pts)


# ---- grid_scan_1d -------------------------------------------------------------

def test_grid_scan_1d() -> None:
    """y = -x² evaluator, extract Pareto."""
    def evaluate(x: float) -> float:
        return -x ** 2

    def objectives(x: float, result: float) -> tuple[float, ...]:
        return (result,)

    values = [-2.0, -1.0, 0.0, 1.0, 2.0]
    pts = grid_scan_1d(values, "x", evaluate, objectives)
    assert len(pts) == 5
    # Pareto: x=0 gives y=0, dominates all others
    front = pareto_filter(pts)
    assert len(front) == 1
    assert front[0].params["x"] == 0.0


# ---- grid_scan_2d + count_points ---------------------------------------------

def test_grid_scan_2d_point_count() -> None:
    def evaluate(x: float, y: float) -> tuple[float, float]:
        return (x + y, x * y)

    def objectives(x: float, y: float, result: tuple) -> tuple[float, ...]:
        return result

    xs = [0.0, 0.5, 1.0]
    ys = [0.0, 0.5, 1.0]
    pts = grid_scan_2d(xs, ys, ("x", "y"), evaluate, objectives)
    assert count_points(pts) == 9


def test_grid_scan_2d_scale_to_1000() -> None:
    """S2.2 hard acceptance: each family can scan ≥ 1000 points."""
    def evaluate(x: float, y: float) -> float:
        return x + y  # cheap

    def objectives(x, y, r) -> tuple[float, ...]:
        return (r,)

    xs = list(range(40))
    ys = list(range(40))  # 40×40 = 1600 > 1000
    pts = grid_scan_2d(xs, ys, ("x", "y"), evaluate, objectives)
    assert count_points(pts) >= 1000


# ---- upper_envelope_1d --------------------------------------------------------

def test_upper_envelope_1d_picks_max_per_x() -> None:
    pts = [
        ParetoPoint(params={"x": 1.0, "z": 1}, objectives=(0.5,)),
        ParetoPoint(params={"x": 1.0, "z": 2}, objectives=(0.8,)),  # max at x=1
        ParetoPoint(params={"x": 2.0, "z": 1}, objectives=(0.3,)),
        ParetoPoint(params={"x": 2.0, "z": 2}, objectives=(0.9,)),  # max at x=2
    ]
    env = upper_envelope_1d(pts, x_key="x", y_key_index=0)
    assert env == [(1.0, 0.8), (2.0, 0.9)]
