"""M1 verification: WLC SDP vs Shor-Preskill analytic bound (§4.6 / §5).

MOSEK tests are skipped if MOSEK is unavailable; CLARABEL fallback is always run.
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.utils.solvers import has_mosek

# ---------------------------------------------------------------------------
# MOSEK parametric suite (M1 hard acceptance)
# ---------------------------------------------------------------------------

pytestmark_mosek = pytest.mark.skipif(
    not has_mosek(), reason="MOSEK unavailable; see docs/SOLVER_SUPPORT.md"
)


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(20260418)


@pytest.mark.parametrize(
    "qber",
    [0.00, 0.01, 0.02, 0.05, 0.08, 0.10],
    ids=lambda x: f"qber_{x:.3f}",
)
@pytestmark_mosek
def test_wlc_bb84_matches_shor_preskill(qber: float) -> None:
    """WLC SDP ≈ Shor-Preskill: rel=0.01, abs=5e-4 (MOSEK)."""
    protocol = build_bb84_protocol(qber=qber)
    R_num = wlc_key_rate(
        protocol,
        observations={"qber_Z": qber, "qber_X": qber, "p_sift": 0.5},
    ).key_rate
    R_ana = shor_preskill_rate(qber)
    assert R_num == pytest.approx(R_ana, rel=0.01, abs=5e-4)


@pytestmark_mosek
def test_wlc_bb84_above_threshold_gives_zero() -> None:
    """QBER > 11% → key_rate ≤ 5e-4 (MOSEK)."""
    protocol = build_bb84_protocol(qber=0.13)
    R = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.13, "qber_X": 0.13, "p_sift": 0.5},
    ).key_rate
    assert R <= 5e-4


@pytest.mark.slow
@pytestmark_mosek
def test_wlc_bb84_qber_exact_zero_with_facial_reduction() -> None:
    """QBER=0 requires facial reduction; result ≈ 1.0 bit/signal (MOSEK)."""
    protocol = build_bb84_protocol(qber=0.0)
    result = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.0, "qber_X": 0.0, "p_sift": 0.5},
    )
    assert result.primal_status in {"optimal", "optimal_inaccurate"}
    assert result.key_rate == pytest.approx(1.0, rel=0.01, abs=5e-4)


@pytestmark_mosek
def test_wlc_solver_status_is_optimal_or_inaccurate() -> None:
    """Standard QBER=0.05 must be accepted by MOSEK."""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
    )
    assert result.primal_status in {"optimal", "optimal_inaccurate"}
    if np.isfinite(result.duality_gap):
        assert result.duality_gap < 1e-4


# ---------------------------------------------------------------------------
# CLARABEL fallback (always runs)
# ---------------------------------------------------------------------------

@pytest.mark.fallback_solver
def test_wlc_fallback_to_clarabel() -> None:
    """CLARABEL fallback: rel=0.02, abs=1e-3 (CLARABEL fallback)."""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
        solver="CLARABEL",
    )
    R_ana = shor_preskill_rate(0.05)
    assert result.key_rate == pytest.approx(R_ana, rel=0.02, abs=1e-3)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_wlc_observable_key_missing_raises() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="missing observation"):
        wlc_key_rate(protocol, observations={"qber_Z": 0.05, "p_sift": 0.5})


@pytest.mark.parametrize("eps", [-0.01, -1e-10, 1.0, 1.5, 2.0])
def test_wlc_epsilon_regularization_out_of_range_raises(eps: float) -> None:
    """epsilon_regularization must be in [0, 1) for convex-combo form."""
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="epsilon_regularization must be in"):
        wlc_key_rate(
            protocol,
            observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
            epsilon_regularization=eps,
        )


@pytestmark_mosek
def test_wlc_regularization_uses_convex_combination() -> None:
    """MOSEK path: X_reg = (1-ε)G(ρ)+ε·τ. Visible at moderate ε.

    Regression: prior code did G(ρ)+ε·τ. For eps=0.05 on QBER=0.05, the
    convex form yields a measurable shift; the old (additive) form would
    further inflate the rate by ~0.05*log2 factors.  Pin the convex result.
    """
    protocol = build_bb84_protocol(qber=0.05)
    r_small = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
        epsilon_regularization=1e-9,
    ).key_rate
    r_moderate = wlc_key_rate(
        protocol,
        observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
        epsilon_regularization=0.01,
    ).key_rate
    # Convex-combo: r_moderate should be close to but smaller than r_small
    # (regularization pulls toward maximally mixed → reduces rate slightly).
    # Additive (bug) form would let r_moderate drift more erratically.
    assert r_moderate < r_small + 1e-3, (
        f"Regularization not acting as convex combo: r_small={r_small}, "
        f"r_moderate={r_moderate}"
    )
    assert r_moderate > r_small - 0.05, (
        f"Regularization too aggressive: r_small={r_small}, r_moderate={r_moderate}"
    )


def test_wlc_observable_key_unknown_raises() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="unknown observation"):
        wlc_key_rate(
            protocol,
            observations={
                "qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5,
                "typo_key": 0.5,
            },
        )


# ---------------------------------------------------------------------------
# Frank-Wolfe feasibility invariant (Agent 1 retrospective review fix)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("qber", [0.0, 0.02, 0.05, 0.08, 0.10])
@pytest.mark.fallback_solver
def test_frank_wolfe_keeps_iterate_feasible(qber: float) -> None:
    """FW iterate must remain on the affine observation constraint set.

    Previously `_init_feasible` added 1e-8·I + renormalized, perturbing the
    equality constraints to ~1e-8 residual; then the FW loop mixed that
    infeasible point with feasible subproblem solutions, making the
    duality_gap a non-certificate.  After the fix, residuals should be at
    CLARABEL tolerance (~1e-10 to 1e-14) and duality_gap >= -tol.
    """
    protocol = build_bb84_protocol(qber=qber)
    result = wlc_key_rate(
        protocol,
        observations={"qber_Z": qber, "qber_X": qber, "p_sift": 0.5},
        solver="CLARABEL",
    )
    # Constraint residual must be tight (machine precision from CLARABEL)
    assert result.max_constraint_residual is not None, (
        "FW path must report constraint residual"
    )
    assert result.max_constraint_residual < 1e-6, (
        f"QBER={qber}: residual={result.max_constraint_residual:.2e} too large; "
        "FW iterate off feasible set"
    )
    # Duality gap should be near zero (allowing small negative roundoff at exit)
    assert result.duality_gap > -1e-6, (
        f"QBER={qber}: duality_gap={result.duality_gap:.2e} unacceptably negative"
    )
