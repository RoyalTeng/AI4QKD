"""Tests for qkdx/core/bell_povm.py — Bell-state measurement channels.

Shared infrastructure for Phase 1 Sub-Q2 MDI Bell POVM upgrade.
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.core.bell_povm import (
    _bell_ket, ideal_bell_bsm, linear_optic_bell_bsm,
)


# ---- Bell kets ---------------------------------------------------------------

@pytest.mark.parametrize("label", ["Phi+", "Phi-", "Psi+", "Psi-"])
def test_bell_ket_unit_norm(label: str) -> None:
    psi = _bell_ket(label)
    assert psi.shape == (4, 1)
    assert np.isclose(np.linalg.norm(psi), 1.0, atol=1e-12)


def test_bell_kets_orthonormal() -> None:
    """4 Bell states form orthonormal basis of C^4."""
    labels = ["Phi+", "Phi-", "Psi+", "Psi-"]
    kets = [_bell_ket(l) for l in labels]
    for i, ki in enumerate(kets):
        for j, kj in enumerate(kets):
            ip = (ki.conj().T @ kj).item()
            expected = 1.0 if i == j else 0.0
            assert np.isclose(ip, expected, atol=1e-12), (
                f"{labels[i]} · {labels[j]} = {ip}, expected {expected}"
            )


def test_bell_ket_unknown_label_raises() -> None:
    with pytest.raises(ValueError, match="unknown Bell label"):
        _bell_ket("Xyz")


# ---- Ideal 4-outcome BSM ------------------------------------------------------

def test_ideal_bsm_kraus_trace_preserving() -> None:
    """Σ K_i† K_i = I_4 (Bell basis completeness)."""
    ch = ideal_bell_bsm()
    total = np.zeros((4, 4), dtype=np.complex128)
    for K in ch.kraus:
        total += K.conj().T @ K
    assert np.allclose(total, np.eye(4), atol=1e-12), f"not trace-preserving: {total}"


def test_ideal_bsm_4_kraus_operators() -> None:
    ch = ideal_bell_bsm()
    assert len(ch.kraus) == 4
    assert ch.dim_in == 4
    assert ch.dim_out == 4
    for K in ch.kraus:
        assert K.shape == (4, 4)


@pytest.mark.parametrize("idx,label", [(0, "Phi+"), (1, "Phi-"), (2, "Psi+"), (3, "Psi-")])
def test_ideal_bsm_applied_to_bell_state(idx: int, label: str) -> None:
    """Applying BSM to |ψ_k⟩⟨ψ_k| should yield |k⟩_C ⟨k|_C (deterministic)."""
    ch = ideal_bell_bsm()
    rho_in = _bell_ket(label) @ _bell_ket(label).conj().T
    rho_out = ch.apply(rho_in)
    assert rho_out.shape == (4, 4)
    expected = np.zeros((4, 4), dtype=np.complex128)
    expected[idx, idx] = 1.0
    assert np.allclose(rho_out, expected, atol=1e-12), (
        f"BSM on |{label}⟩⟨{label}| → {rho_out.diagonal()}, expected p_{idx}=1"
    )


def test_ideal_bsm_applied_to_maximally_mixed() -> None:
    """Maximally mixed state → uniform 1/4 over all 4 Bell outcomes."""
    ch = ideal_bell_bsm()
    rho_in = np.eye(4, dtype=np.complex128) / 4.0
    rho_out = ch.apply(rho_in)
    expected = np.eye(4, dtype=np.complex128) / 4.0
    assert np.allclose(rho_out, expected, atol=1e-12)


# ---- Linear-optic BSM ---------------------------------------------------------

def test_linear_optic_bsm_kraus_trace_preserving() -> None:
    """Σ K_i† K_i = I_4 (Φ+ + Ψ- + Φ- + Ψ+ complete)."""
    ch = linear_optic_bell_bsm()
    total = np.zeros((4, 4), dtype=np.complex128)
    for K in ch.kraus:
        total += K.conj().T @ K
    assert np.allclose(total, np.eye(4), atol=1e-12)


def test_linear_optic_bsm_shape() -> None:
    ch = linear_optic_bell_bsm()
    assert ch.dim_in == 4
    assert ch.dim_out == 3  # success1 / success2 / fail
    assert len(ch.kraus) == 4  # but 2 fail Kraus ops share classical label 2


def test_linear_optic_bsm_phi_plus_success() -> None:
    """Input |Φ+⟩⟨Φ+| → p_0=1 (announcement "Φ+")."""
    ch = linear_optic_bell_bsm()
    rho_in = _bell_ket("Phi+") @ _bell_ket("Phi+").conj().T
    rho_out = ch.apply(rho_in)
    assert np.isclose(rho_out[0, 0].real, 1.0, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 0.0, atol=1e-12)
    assert np.isclose(rho_out[2, 2].real, 0.0, atol=1e-12)


def test_linear_optic_bsm_psi_minus_success() -> None:
    """Input |Ψ-⟩⟨Ψ-| → p_1=1 (announcement "Ψ-")."""
    ch = linear_optic_bell_bsm()
    rho_in = _bell_ket("Psi-") @ _bell_ket("Psi-").conj().T
    rho_out = ch.apply(rho_in)
    assert np.isclose(rho_out[0, 0].real, 0.0, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 1.0, atol=1e-12)
    assert np.isclose(rho_out[2, 2].real, 0.0, atol=1e-12)


@pytest.mark.parametrize("label", ["Phi-", "Psi+"])
def test_linear_optic_bsm_indistinguishable_are_fail(label: str) -> None:
    """Input |Φ-⟩ or |Ψ+⟩ → p_2=1 (announcement "fail")."""
    ch = linear_optic_bell_bsm()
    rho_in = _bell_ket(label) @ _bell_ket(label).conj().T
    rho_out = ch.apply(rho_in)
    assert np.isclose(rho_out[0, 0].real, 0.0, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 0.0, atol=1e-12)
    assert np.isclose(rho_out[2, 2].real, 1.0, atol=1e-12)


def test_linear_optic_bsm_maximally_mixed_half_success() -> None:
    """Maximally mixed 2-qubit state: p_success = 1/2 (Φ+ + Ψ-), p_fail = 1/2."""
    ch = linear_optic_bell_bsm()
    rho_in = np.eye(4, dtype=np.complex128) / 4.0
    rho_out = ch.apply(rho_in)
    # p_0 = ⟨Φ+|I/4|Φ+⟩ = 1/4; p_1 = ⟨Ψ-|I/4|Ψ-⟩ = 1/4; p_2 = 1/4+1/4 = 1/2
    assert np.isclose(rho_out[0, 0].real, 0.25, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 0.25, atol=1e-12)
    assert np.isclose(rho_out[2, 2].real, 0.5, atol=1e-12)


def test_linear_optic_bsm_total_success_rate_is_half_for_separable_input() -> None:
    """For |00⟩⟨00| input (separable): ⟨Φ+|00⟩=1/√2, ⟨Ψ-|00⟩=0
    → p_success = 1/2, actually it's only Φ+ piece = 1/2 from Φ+, 0 from Ψ-,
    but |00⟩ also has |Φ-⟩ overlap 1/√2 → p_fail = 1/2 (all from Φ-).
    Total: p_0 = 1/2, p_1 = 0, p_2 = 1/2.
    """
    ch = linear_optic_bell_bsm()
    ket00 = np.zeros((4, 1), dtype=np.complex128)
    ket00[0, 0] = 1.0
    rho_in = ket00 @ ket00.conj().T
    rho_out = ch.apply(rho_in)
    assert np.isclose(rho_out[0, 0].real, 0.5, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 0.0, atol=1e-12)
    assert np.isclose(rho_out[2, 2].real, 0.5, atol=1e-12)
