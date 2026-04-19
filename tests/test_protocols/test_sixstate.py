"""Tests for qkdx/protocols/sixstate.py + WLC SDP on six-state."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.analytic.six_state import six_state_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocol.base import MSEBProtocol
from qkdx.protocols.sixstate import (
    build_sixstate_protocol, sixstate_alice_source, _gamma_qber_Y,
)
from qkdx.utils.solvers import has_mosek


# ---- Protocol construction ----------------------------------------------------

def test_protocol_has_six_state_metadata() -> None:
    p = build_sixstate_protocol(qber=0.05)
    assert isinstance(p, MSEBProtocol)
    assert p.name == "SixState"
    assert p.scope_tag == "covered"
    assert p.sources[0].key_register_dim == 6
    assert p.sources[0].signal_register_dim == 2
    assert p.conditional_alice_bob_dim() == 4


def test_observation_keys_include_qber_Y() -> None:
    p = build_sixstate_protocol(qber=0.05)
    assert set(p.observation_keys) == {"qber_Z", "qber_X", "qber_Y", "p_sift"}


def test_observables_are_hermitian_4x4() -> None:
    p = build_sixstate_protocol(qber=0.05)
    for key in ("qber_Z", "qber_X", "qber_Y"):
        Gamma = p.observable(key)
        assert Gamma.shape == (4, 4)
        assert np.allclose(Gamma, Gamma.conj().T, atol=1e-10), f"{key} not Hermitian"


def test_source_state_is_density() -> None:
    """Pure 12x12 source state must be PSD, trace 1, rank 1."""
    src = sixstate_alice_source(qber=0.05)
    rho = src.source_state
    assert rho.shape == (12, 12)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10)
    # Pure state → one eigenvalue ≈ 1, rest ≈ 0
    assert np.isclose(eigvals[-1], 1.0, atol=1e-9)
    assert np.isclose(eigvals[-2], 0.0, atol=1e-9)


# ---- Gamma_Y correctness ------------------------------------------------------

def _werner_state(e: float) -> Matrix:
    """Bell-diagonal Werner state for symmetric depolarising channel.

        ρ_W = (1-3e/2)|Φ+⟩⟨Φ+| + (e/2)(|Φ−⟩⟨Φ−| + |Ψ+⟩⟨Ψ+| + |Ψ−⟩⟨Ψ−|)

    In standard basis {|00⟩,|01⟩,|10⟩,|11⟩}:
        diagonal = ((1-e)/2, e/2, e/2, (1-e)/2)
        off-diagonal (0,3) = (3,0) = (1-2e)/2
    """
    rho = np.diag([(1 - e) / 2, e / 2, e / 2, (1 - e) / 2]).astype(np.complex128)
    rho[0, 3] = (1 - 2 * e) / 2
    rho[3, 0] = (1 - 2 * e) / 2
    return rho


def test_gamma_Y_agrees_with_werner_state() -> None:
    """Tr(Γ_Y · ρ_Werner) = e for symmetric depolarising channel.

    (The BB84 Z-basis sifted state is fully diagonal and does NOT satisfy
    the Γ_Y = e constraint; Γ_Y probes off-diagonal coherence absent after
    Z-projection.  The physical reference is the pre-measurement Werner state.)
    """
    Gamma_Y = _gamma_qber_Y()
    for e in [0.01, 0.05, 0.1]:
        rho = _werner_state(e)
        value = np.trace(Gamma_Y @ rho).real
        assert value == pytest.approx(e, abs=1e-12), f"Γ_Y·ρ_W(e={e}) = {value}"


def test_gamma_Z_X_agree_with_werner_state() -> None:
    """Sanity: Γ_Z and Γ_X should also give e on ρ_Werner."""
    from qkdx.protocols.bb84 import _gamma_qber_Z, _gamma_qber_X
    for e in [0.01, 0.05, 0.1]:
        rho = _werner_state(e)
        assert np.trace(_gamma_qber_Z() @ rho).real == pytest.approx(e, abs=1e-12)
        assert np.trace(_gamma_qber_X() @ rho).real == pytest.approx(e, abs=1e-12)


# ---- WLC SDP vs analytic: acceptance criterion --------------------------------

_FALLBACK_TOL = dict(rel=0.02, abs=1e-3)  # CLARABEL fallback acceptance (RESEARCH_PLAN §1.2)
_MOSEK_TOL = dict(rel=0.01, abs=5e-4)     # MOSEK primary acceptance


@pytest.mark.parametrize("qber", [0.01, 0.02, 0.05, 0.08, 0.10])
def test_wlc_sixstate_matches_analytic(qber: float) -> None:
    """WLC SDP six-state key rate matches analytic formula within acceptance.

    Acceptance (§1.2 fallback track, CLARABEL Frank-Wolfe):
        rel=0.02, abs=1e-3
    Acceptance (MOSEK primary — when available):
        rel=0.01, abs=5e-4
    """
    p = build_sixstate_protocol(qber=qber)
    obs = {"qber_Z": qber, "qber_X": qber, "qber_Y": qber, "p_sift": 1.0 / 3.0}
    result = wlc_key_rate(p, obs, f_ec=1.0)

    analytic = six_state_rate(qber, f_ec=1.0)
    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert result.key_rate == pytest.approx(analytic, **tol), (
        f"QBER={qber}: WLC={result.key_rate:.6f}, analytic={analytic:.6f}, "
        f"|diff|={abs(result.key_rate - analytic):.2e}, solver={result.solver}"
    )


def test_wlc_sixstate_zero_qber() -> None:
    """At QBER=0: WLC should give R = p_sift × 1 = 1/3 bit/signal."""
    p = build_sixstate_protocol(qber=0.0)
    obs = {"qber_Z": 0.0, "qber_X": 0.0, "qber_Y": 0.0, "p_sift": 1.0 / 3.0}
    result = wlc_key_rate(p, obs, f_ec=1.0)
    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert result.key_rate == pytest.approx(1.0 / 3.0, **tol)


def test_wlc_sixstate_above_bb84_per_sift() -> None:
    """At moderate QBER, WLC six-state per-sift rate > WLC BB84 per-sift rate.

    Adding the Γ_Y constraint strictly tightens the feasible set ⇒ higher
    min objective ⇒ higher H(A|E).
    """
    from qkdx.protocols.bb84 import build_bb84_protocol
    qber = 0.08

    p6 = build_sixstate_protocol(qber=qber)
    obs6 = {"qber_Z": qber, "qber_X": qber, "qber_Y": qber, "p_sift": 1.0 / 3.0}
    r6 = wlc_key_rate(p6, obs6, f_ec=1.0)
    h6_per_sift = r6.key_rate / (1.0 / 3.0) + 1.0 * np.log2(np.e) * 0  # fine: direct rate / p_sift

    pb = build_bb84_protocol(qber=qber)
    obsb = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.5}
    rb = wlc_key_rate(pb, obsb, f_ec=1.0)
    hb_per_sift = rb.key_rate / 0.5

    assert h6_per_sift > hb_per_sift, (
        f"six-state per-sift {h6_per_sift:.5f} should exceed BB84 {hb_per_sift:.5f}"
    )


# ---- Input validation ---------------------------------------------------------

def test_invalid_qber_raises() -> None:
    with pytest.raises(ValueError, match="QBER"):
        build_sixstate_protocol(qber=-0.01)
    with pytest.raises(ValueError, match="QBER"):
        build_sixstate_protocol(qber=0.70)


def test_missing_observation_raises() -> None:
    """Omitting qber_Y must raise."""
    p = build_sixstate_protocol(qber=0.05)
    obs = {"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 1.0 / 3.0}  # missing qber_Y
    with pytest.raises(ValueError, match="qber_Y"):
        wlc_key_rate(p, obs, f_ec=1.0)
