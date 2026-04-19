"""Runtime solver availability guards."""
from __future__ import annotations


def has_mosek() -> bool:
    """Return True if MOSEK is installed and importable."""
    try:
        import mosek  # noqa: F401
        return True
    except ImportError:
        return False


def preferred_solver() -> str:
    """Return the best available SDP solver name for CVXPY."""
    if has_mosek():
        return "MOSEK"
    try:
        import clarabel  # noqa: F401
        return "CLARABEL"
    except ImportError:
        return "SCS"
