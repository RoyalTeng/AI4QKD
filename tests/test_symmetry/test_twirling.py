"""Tests for qkdx/symmetry (groups + twirling)."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.core.hilbert import HADAMARD, IDENTITY_2, SIGMA_X, SIGMA_Y, SIGMA_Z
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import (
    build_bb84_protocol, _bb84_conditional_state, _gamma_qber_Z, _gamma_qber_X,
)
from qkdx.symmetry.groups import (
    bb84_pauli_group, bb84_bilateral_group, six_state_bilateral_group, get_group,
)
from qkdx.symmetry.twirling import (
    twirl, werner_state, werner_parameters, check_invariant,
    to_bell_basis, from_bell_basis,
    BELL_PHI_PLUS, BELL_PHI_MINUS, BELL_PSI_PLUS, BELL_PSI_MINUS,
)
from qkdx.utils.solvers import has_mosek


# ---- Groups ------------------------------------------------------------------

def test_pauli_group_has_4_elements() -> None:
    group = bb84_pauli_group()
    assert len(group) == 4
    for U in group:
        assert U.shape == (4, 4)
        # Unitary check
        assert np.allclose(U @ U.conj().T, np.eye(4), atol=1e-10)


def test_bilateral_group_has_8_elements() -> None:
    group = bb84_bilateral_group()
    assert len(group) == 8
    for U in group:
        assert U.shape == (4, 4)
        assert np.allclose(U @ U.conj().T, np.eye(4), atol=1e-10)


def test_get_group_lookup() -> None:
    g = get_group("bb84_bilateral")
    assert len(g) == 8
    with pytest.raises(ValueError, match="Unknown group"):
        get_group("not-a-group")


# ---- Bell basis round-trip ---------------------------------------------------

def test_bell_basis_roundtrip() -> None:
    rho = np.diag([0.3, 0.2, 0.1, 0.4]).astype(np.complex128)
    rho_b = to_bell_basis(rho)
    rho_back = from_bell_basis(rho_b)
    assert np.allclose(rho, rho_back, atol=1e-12)


def test_phi_plus_is_bell_basis_element_0() -> None:
    """In Bell basis, |Φ+⟩ should be e_0."""
    phi_plus = BELL_PHI_PLUS  # (4, 1)
    proj = phi_plus @ phi_plus.conj().T  # (4, 4)
    proj_bell = to_bell_basis(proj)
    # |Φ+⟩⟨Φ+| in Bell basis = diag(1, 0, 0, 0)
    expected = np.diag([1, 0, 0, 0]).astype(np.complex128)
    assert np.allclose(proj_bell, expected, atol=1e-12)


# ---- Twirling --------------------------------------------------------------

def test_twirl_identity_does_nothing() -> None:
    rho = np.diag([0.25, 0.25, 0.25, 0.25]).astype(np.complex128)
    out = twirl(rho, (np.eye(4, dtype=np.complex128),))
    assert np.allclose(rho, out, atol=1e-12)


def test_bell_diag_is_pauli_invariant() -> None:
    """Any Bell-diagonal state is invariant under Pauli bilateral twirling."""
    rho_bell_diag = from_bell_basis(np.diag([0.5, 0.2, 0.2, 0.1]).astype(np.complex128))
    assert check_invariant(rho_bell_diag, bb84_pauli_group(), atol=1e-9)


def test_werner_state_is_bilateral_invariant() -> None:
    """Werner BB84-symmetric state is invariant under full bilateral group."""
    rho = werner_state(F=0.85, mu=0.05)
    assert check_invariant(rho, bb84_bilateral_group(), atol=1e-9)


def test_general_density_becomes_bell_diag_under_pauli_twirl() -> None:
    """A random density matrix twirled by Pauli group becomes Bell-diagonal."""
    np.random.seed(42)
    A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
    rho = A @ A.conj().T
    rho /= np.trace(rho).real
    rho_twirled = twirl(rho, bb84_pauli_group())
    rho_twirled_bell = to_bell_basis(rho_twirled)
    # Off-diagonals should be ≈ 0
    off = rho_twirled_bell - np.diag(np.diag(rho_twirled_bell))
    assert np.max(np.abs(off)) < 1e-10


def test_bilateral_twirl_enforces_phi_minus_equals_psi_plus() -> None:
    """Full bilateral group additionally enforces λ_Φ- = λ_Ψ+."""
    np.random.seed(43)
    A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
    rho = A @ A.conj().T
    rho /= np.trace(rho).real
    rho_twirled = twirl(rho, bb84_bilateral_group())
    F, mu, lam_psi_minus = werner_parameters(rho_twirled, atol=1e-9)
    # By construction all four eigenvalues summed to 1
    assert F + 2 * mu + lam_psi_minus == pytest.approx(1.0, abs=1e-10)


# ---- Werner parameters round-trip -------------------------------------------

def test_werner_roundtrip() -> None:
    F, mu = 0.85, 0.05
    rho = werner_state(F, mu)
    F_back, mu_back, _ = werner_parameters(rho)
    assert F_back == pytest.approx(F, abs=1e-12)
    assert mu_back == pytest.approx(mu, abs=1e-12)


def test_werner_state_invalid_negative_weight() -> None:
    with pytest.raises(ValueError, match="PSD|F"):
        werner_state(F=0.5, mu=0.5)  # λ_Ψ- = 1 - 0.5 - 1 = -0.5 < 0


# ---- BB84 specific: symmetric channel Werner state satisfies constraints ----

@pytest.mark.parametrize("qber", [0.01, 0.05, 0.10])
def test_bb84_werner_state_satisfies_Z_X_constraints(qber: float) -> None:
    """Werner state with F=1-3e/2, μ=e/2 satisfies both Γ_Z=e and Γ_X=e."""
    rho = werner_state(F=1 - 1.5 * qber, mu=0.5 * qber)
    assert np.trace(_gamma_qber_Z() @ rho).real == pytest.approx(qber, abs=1e-12)
    assert np.trace(_gamma_qber_X() @ rho).real == pytest.approx(qber, abs=1e-12)


# ---- Acceptance: WLC SDP on twirled variable matches full SDP ---------------

_FALLBACK_TOL = dict(rel=0.02, abs=1e-3)
_MOSEK_TOL = dict(rel=0.01, abs=5e-4)


@pytest.mark.parametrize("qber", [0.01, 0.05, 0.08])
def test_wlc_bb84_full_matches_werner_analytic(qber: float) -> None:
    """Full WLC SDP on BB84 = D evaluated on the Werner state (analytic closed form).

    This is the M4A hard-acceptance core: the symmetry-reduced 2-parameter
    evaluation gives the same answer as the full 4×4 SDP (to fallback
    tolerance abs=1e-3).
    """
    # Full SDP
    p = build_bb84_protocol(qber=qber)
    obs = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.5}
    r_full = wlc_key_rate(p, obs, f_ec=1.0)

    # Analytic on Werner state: H_six or equivalently BB84 formula 1 - h(e).
    # Because at BB84 symmetric case the Werner state gives D = 1 - h(e).
    from qkdx.core.entropy import binary_entropy
    h_e = binary_entropy(qber)
    H_bits_analytic = 1.0 - h_e
    # Key rate = p_sift * (H - f_ec * h(e)), f_ec=1 → p_sift*(1 - 2h(e))
    R_analytic = 0.5 * (H_bits_analytic - 1.0 * h_e)

    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert r_full.key_rate == pytest.approx(R_analytic, **tol)
