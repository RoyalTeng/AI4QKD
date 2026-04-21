"""Kamin 2025 decoy-state block-diagonal SDP (S2.5 Stage 2 A4c).

Reference:
    - Kamin et al. 2025, arXiv:2406.10198v3, §7 (decoy-state protocol)
    - §7.2 general decoy formulation (Eq. 71–79)
    - §7.3 Fig. 3 numerical results
    - docs/literature/Kamin-2025.md §7

Core formulation (Kamin Eq. 79, one-step):
    r_cross(q) ≥ inf_{J_1, Y_0, …, Y_{N_ph}, δ^μ}  p(1|μ_sig)·W(ρ_{J_1}^g)
    s.t.
      p(μ|t)·(Σ_{n≤N_ph} p_μ(n)·Y_n + δ^μ) = q^μ    ∀μ ∈ intensities   (Eq. 79a)
      0 ≤ δ^μ ≤ 1 − p_tot(μ)                          ∀μ               (Eq. 79b)
      p(μ|t)·Y_1 = p(μ|t)·Φ[ρ_{J_1}^{t,μ}]          ∀μ               (Eq. 79c)
      Σ_b Y_n^{ab} = p(a|t, n)                        ∀a, ∀n          (Eq. 79d)

Variables:
    J_1: 2-qubit Choi matrix for single-photon channel (4×4 Hermitian PSD)
    Y_n: yield matrix for n-photon, indexed by (a, b):
         a ∈ {|D⟩, |A⟩}  (Alice test-round X-basis signals)
         b ∈ {(X,D), (X,A), (Z,0), (Z,1), no-det}  (Bob outcomes)
    δ^μ: photon-cutoff remainder per intensity μ (same (a, b) indexing)

Honest model (simpler than WL22):
    - WCP source at intensity μ: Poisson(μ) photon number
    - Per-photon loss η_det (each photon independently lost with prob 1-η)
    - Per-photon misalignment rotation θ_misalign (X-basis rotated)
    - NO dark counts (ignore in this pass)

Scope of this module (S2.5 Stage 2 A4c):
    - Scaffolding + unit tests for Poisson / honest yields / SDP structure
    - Reproduction of Kamin Fig.3 at key anchors (follow-up commits)

Honest-distribution approximations vs Kamin §7.3:
    - Kamin Fig.3 uses WL22 beamsplitter-loss + misalignment model with
      θ_misalign = sin⁻¹(0.1).  My per-photon loss is simpler; Fig.3
      matching requires WL22-exact model (documented follow-up).
"""
from __future__ import annotations

import math
import os
from typing import Any

import cvxpy as cp
import numpy as np

# Reuse helpers from kamin_sdp
from qkdx.numerics.kamin_sdp import (
    partial_trace_B,
    partial_trace_A_prime,
    partial_transpose_A_prime,
    rho_J_from_choi,
    rho_J_from_choi_cvxpy,
    partial_trace_B_cvxpy,
    _bb84_G_Z_expressions,
)

_DEFAULT_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_DEFAULT_MOSEK_LIC) and "MOSEKLM_LICENSE_FILE" not in os.environ:
    os.environ["MOSEKLM_LICENSE_FILE"] = _DEFAULT_MOSEK_LIC


# ---------------------------------------------------------------------------
# Poisson photon-number distribution
# ---------------------------------------------------------------------------

def poisson_pmf(mu: float, n: int) -> float:
    """Poisson(μ) probability mass at n: e^{-μ}·μ^n / n!."""
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if n < 0:
        raise ValueError(f"n must be ≥ 0, got {n}")
    if mu == 0.0:
        return 1.0 if n == 0 else 0.0
    return math.exp(-mu) * mu ** n / math.factorial(n)


def poisson_pmf_vec(mu: float, N_ph: int) -> np.ndarray:
    """Vector [P(0|μ), P(1|μ), ..., P(N_ph|μ)]."""
    if N_ph < 0:
        raise ValueError(f"N_ph must be ≥ 0, got {N_ph}")
    return np.array([poisson_pmf(mu, n) for n in range(N_ph + 1)])


def poisson_tail(mu: float, N_ph: int) -> float:
    """Tail probability 1 − Σ_{n ≤ N_ph} P(n|μ) = Σ_{n > N_ph} P(n|μ)."""
    return max(0.0, 1.0 - float(poisson_pmf_vec(mu, N_ph).sum()))


# ---------------------------------------------------------------------------
# Observation alphabet for decoy BB84 (per-intensity)
# ---------------------------------------------------------------------------

# On a test round (Alice X-basis, intensity μ): observation = (a, b)
#   a ∈ {0, 1}: Alice's X-basis signal; 0 ↔ |D⟩, 1 ↔ |A⟩
#   b ∈ {0, 1, 2, 3, 4}: Bob's outcome
#       0 ↔ (X, D-click), 1 ↔ (X, A-click)
#       2 ↔ (Z, 0-click), 3 ↔ (Z, 1-click)
#       4 ↔ no-detect
# So Y_n^{a,b} is a (2, 5) matrix for each photon number n.

N_ALICE_SIGNALS = 2    # a ∈ {|D⟩, |A⟩}
N_BOB_OUTCOMES = 5     # b ∈ {X-D, X-A, Z-0, Z-1, no-det}
_IDX_XD, _IDX_XA, _IDX_Z0, _IDX_Z1, _IDX_NOD = 0, 1, 2, 3, 4


def _single_photon_unitary_rotation(theta: float) -> np.ndarray:
    """2×2 unitary rotating by θ in the Z-basis, applied to X-basis states
    after loss.  Implements misalignment rotation.
    """
    return np.array(
        [[math.cos(theta), -math.sin(theta)],
         [math.sin(theta),  math.cos(theta)]],
        dtype=np.complex128,
    )


def _wcp_click_probs_n_photon(
    n: int, a: int, eta_det: float, theta_misalign: float,
    bob_gamma: float,
) -> np.ndarray:
    """Probability vector over Bob outcomes (5 cells) given Alice sent
    n-photon X-basis signal a ∈ {0 (|D⟩), 1 (|A⟩)} under per-photon loss
    η_det and misalignment θ_misalign, with Bob measuring X w.p. bob_gamma
    and Z w.p. 1−bob_gamma.

    Model (per-photon independent):
        - Each photon passes loss η_det (prob (1-η)^n that all are lost).
        - Conditional on ≥1 detected photon, Bob measures his basis on
          ONE surviving photon and reads the (correct) single-photon
          outcome prob.
        - Misalignment: correct-outcome prob = cos²(θ); error = sin²(θ).
        - Bob X-measurement:
              send |D⟩: p(X=D)=cos²(θ), p(X=A)=sin²(θ)
              send |A⟩: p(X=D)=sin²(θ), p(X=A)=cos²(θ)
        - Bob Z-measurement:
              send |D⟩=(|0⟩+|1⟩)/√2 → uniform over (0, 1): 1/2 each
              (Z-basis measures on X-signal is uniform-mismatch, as expected)

    Vacuum (n=0) → always no-detect.
    """
    if n == 0:
        return np.array([0.0, 0.0, 0.0, 0.0, 1.0])  # all no-detect

    p_no_det = (1.0 - eta_det) ** n
    p_detected = 1.0 - p_no_det

    # Conditional on detection: Bob measures X w.p. bob_gamma, Z w.p. 1-γ
    c2 = math.cos(theta_misalign) ** 2
    s2 = math.sin(theta_misalign) ** 2

    # p(X=D|send a)
    pXD = c2 if a == 0 else s2
    pXA = s2 if a == 0 else c2

    # p(Z=0|send X-state): uniform
    pZ0 = 0.5
    pZ1 = 0.5

    probs = np.zeros(N_BOB_OUTCOMES)
    probs[_IDX_XD] = p_detected * bob_gamma * pXD
    probs[_IDX_XA] = p_detected * bob_gamma * pXA
    probs[_IDX_Z0] = p_detected * (1.0 - bob_gamma) * pZ0
    probs[_IDX_Z1] = p_detected * (1.0 - bob_gamma) * pZ1
    probs[_IDX_NOD] = p_no_det
    return probs


def honest_yields_wcp_per_photon(
    N_ph: int, eta_det: float, theta_misalign: float, bob_gamma: float,
) -> np.ndarray:
    """Per-photon-number honest yields Y_n^{a,b} for WCP BB84 with loss +
    misalignment.

    Args:
        N_ph: photon cutoff (compute yields for n = 0, 1, ..., N_ph)
        eta_det: per-photon detection/transmittance ∈ (0, 1]
        theta_misalign: misalignment rotation angle (radians)
        bob_gamma: Bob's X-measurement probability

    Returns:
        Y: array shape (N_ph+1, N_ALICE_SIGNALS, N_BOB_OUTCOMES).
           Y[n, a, b] = P(Bob outcome b | Alice sent signal a, n photons).
    """
    if N_ph < 0:
        raise ValueError(f"N_ph must be ≥ 0, got {N_ph}")
    if not (0.0 < eta_det <= 1.0):
        raise ValueError(f"eta_det must be in (0, 1], got {eta_det}")
    if not (0.0 <= bob_gamma <= 1.0):
        raise ValueError(f"bob_gamma must be in [0, 1], got {bob_gamma}")

    Y = np.zeros((N_ph + 1, N_ALICE_SIGNALS, N_BOB_OUTCOMES))
    for n in range(N_ph + 1):
        for a in range(N_ALICE_SIGNALS):
            Y[n, a, :] = _wcp_click_probs_n_photon(
                n=n, a=a, eta_det=eta_det, theta_misalign=theta_misalign,
                bob_gamma=bob_gamma,
            )
    return Y


def honest_q_per_intensity(
    mu: float,
    N_ph: int,
    eta_det: float,
    theta_misalign: float,
    bob_gamma: float,
    p_mu_given_t: float,
    p_a_given_t_n: np.ndarray | None = None,
) -> np.ndarray:
    """Honest observation distribution q^μ = p(μ|t)·Σ_n P(n|μ)·Y_n^{ab}.

    Normalization: Σ_{a,b} q^μ_{ab} = p(μ|t) (i.e., marginal probability
    that a test round uses intensity μ).

    Args:
        mu: intensity
        N_ph: photon cutoff
        eta_det, theta_misalign, bob_gamma: honest channel params
        p_mu_given_t: probability that a test round uses intensity μ
        p_a_given_t_n: shape (N_ph+1, 2); Alice's signal prob | n-photon.
                       Default = uniform (1/2, 1/2) over (|D⟩, |A⟩).

    Returns:
        q_mu: shape (N_ALICE_SIGNALS, N_BOB_OUTCOMES) = (2, 5).
    """
    Y = honest_yields_wcp_per_photon(
        N_ph=N_ph, eta_det=eta_det,
        theta_misalign=theta_misalign, bob_gamma=bob_gamma,
    )
    if p_a_given_t_n is None:
        p_a_given_t_n = np.full((N_ph + 1, N_ALICE_SIGNALS), 0.5)

    p_n_mu = poisson_pmf_vec(mu, N_ph)  # P(n|μ) for n ≤ N_ph
    # q^μ_{ab} = p(μ|t) · Σ_n p_μ(n) · p(a|t,n) · Y_n^{a,b}
    q_mu = np.zeros((N_ALICE_SIGNALS, N_BOB_OUTCOMES))
    for n in range(N_ph + 1):
        for a in range(N_ALICE_SIGNALS):
            q_mu[a, :] += p_mu_given_t * p_n_mu[n] * p_a_given_t_n[n, a] * Y[n, a, :]

    # Tail (n > N_ph): assumed to give all no-detect in honest model + ignoring
    # (upper-bounded by δ^μ in the SDP).  For Σ normalization:
    #   Σ_{a,b} q^μ_{ab} = p(μ|t)·(1 − P(tail|μ)) in honest model.
    # SDP accepts this via δ^μ up to 1−p_tot(μ).
    return q_mu


# ---------------------------------------------------------------------------
# Kamin Eq. 79 decoy-state SDP
# ---------------------------------------------------------------------------

def _gamma_X_test_error_projector() -> np.ndarray:
    """Projector onto "error" outcomes when Alice sent X-basis |D⟩ and Bob
    measured X-basis, getting |A⟩ (anticorrelated).  For the 4×4 A⊗B rep
    in the EB picture, the X-error projector.

    Used by the SDP to constrain Tr[ρ_{J_1}^{t,μ} · (X-error)] = observation.
    """
    # |±⟩ = (|0⟩ ± |1⟩)/√2
    plus = np.array([1.0, 1.0]) / math.sqrt(2.0)
    minus = np.array([1.0, -1.0]) / math.sqrt(2.0)
    # Error: (D,A) and (A,D) — Alice sent X+ and Bob got X-, or vice versa
    proj_pm = np.outer(np.kron(plus, minus), np.kron(plus, minus).conj())
    proj_mp = np.outer(np.kron(minus, plus), np.kron(minus, plus).conj())
    return (proj_pm + proj_mp).astype(np.complex128) / 2.0  # γ_X · 1/2 sym


def kamin_decoy_choi_sdp(
    intensities: tuple[float, ...],
    p_mu_given_t: tuple[float, ...],
    q_hon_per_mu: dict[float, np.ndarray],
    N_ph: int,
    gamma: float = 0.01,
    eta_1_calib: float = 1.0,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Kamin 2025 Eq. 79 one-step block-diagonal decoy SDP.

    Solves:
        min_{J_1, Y_0..Y_{N_ph}, δ^μ}  p(1|μ_sig) · W(ρ_{J_1}^g)
        s.t. (per Eq. 79 a–d)

    where J_1 is the single-photon Choi matrix (qubit→qubit) for privacy
    computation CONDITIONAL on detection, and W(ρ_J^g) is the
    BB84 single-photon privacy per Eq. 60.

    Calibrated-detector standpoint (`eta_1_calib`):
        My dim_B=2 single-photon Choi represents a CPTP channel (trace-
        preserving, no loss-absorbed degree of freedom in the output).
        To interface with loss without extending Bob's Hilbert space to
        dim_B=3 (explicit no-det outcome), we pass the single-photon
        detection probability `η_1` as a calibrated parameter:
            Y_1[a, detected b] = η_1 · Φ_ab(ρ_{J_1})     ∀detected b
            Y_1[a, no-det]     = (1/2) · (1 − η_1)
        Honest channel: η_1 = η_det.  The SDP then optimizes J_1 (privacy)
        given the detected observations.  This is consistent with
        trusted-detector security proofs where η_det is characterized.

    Args:
        intensities: tuple of μ values (e.g., (0.9, 0.02, 0.001))
        p_mu_given_t: tuple of p(μ_i | t) matching intensities
        q_hon_per_mu: dict mapping μ → (2, 5) honest observation matrix
        N_ph: photon-number cutoff (Kamin Fig.3 uses 10)
        gamma: test-round probability
        eta_1_calib: calibrated single-photon detection probability (∈ (0, 1]).
            Should match the honest channel's η_det.
        solver, epsilon_regularization, verbose: as for kamin_choi_sdp_qubit_bb84

    Returns:
        dict with:
            r_cross: optimal objective value (bits/sift)
            h_per_sift_eq42_single_photon: p(1|μ_sig) · W(ρ_{J_1}^g)
            J_1: optimal single-photon Choi
            Y: optimal yield tensor (N_ph+1, 2, 5)
            delta: optimal remainder per μ (|intensities|, 2, 5)
            eta_1_calib: echo of calibrated η_1
            status: solver status
    """
    if len(intensities) != len(p_mu_given_t):
        raise ValueError(
            f"intensities and p_mu_given_t length mismatch: "
            f"{len(intensities)} vs {len(p_mu_given_t)}"
        )
    if set(q_hon_per_mu.keys()) != set(intensities):
        raise ValueError(
            f"q_hon_per_mu keys {set(q_hon_per_mu.keys())} don't match "
            f"intensities {set(intensities)}"
        )
    if N_ph < 1:
        raise ValueError(f"N_ph must be ≥ 1 (need single-photon), got {N_ph}")
    if not (0.0 < eta_1_calib <= 1.0):
        raise ValueError(f"eta_1_calib must be in (0, 1], got {eta_1_calib}")

    mu_sig = intensities[0]  # Convention: first intensity is μ_sig
    p_mu_sig_given_t = p_mu_given_t[0]

    dim_A = dim_A_prime = dim_B = 2

    # Source state for single-photon test rounds: |ξ^t⟩ = (|00⟩ + |11⟩)/√2
    xi = np.zeros(dim_A * dim_A_prime, dtype=np.complex128)
    xi[0] = 1.0 / math.sqrt(2)
    xi[3] = 1.0 / math.sqrt(2)
    xi_xi = np.outer(xi, xi.conj())
    xi_xi_T = partial_transpose_A_prime(
        xi_xi, dim_A=dim_A, dim_A_prime=dim_A_prime,
    )
    xi_xi_T_kron_I = np.kron(xi_xi_T, np.eye(dim_B, dtype=np.complex128))

    # J_1: 4×4 Hermitian PSD (single-photon Choi)
    D_J = dim_A_prime * dim_B
    J_1 = cp.Variable((D_J, D_J), hermitian=True)

    # Yield tensor Y_n^{ab}: real variable, shape (N_ph+1, 2, 5)
    Y = cp.Variable((N_ph + 1, N_ALICE_SIGNALS, N_BOB_OUTCOMES))

    # δ^μ remainder: shape (|intensities|, 2, 5)
    n_mu = len(intensities)
    delta = cp.Variable((n_mu, N_ALICE_SIGNALS, N_BOB_OUTCOMES))

    constraints: list[cp.Constraint] = []

    # J_1 PSD
    constraints.append(J_1 >> 0)
    # Trace-preserving: Tr_B(J_1) = I_{A'}
    tr_B_J1 = partial_trace_B_cvxpy(J_1, dim_A=dim_A_prime, dim_B=dim_B)
    constraints.append(tr_B_J1 == np.eye(dim_A_prime, dtype=np.complex128))

    # ρ_{J_1}^{t,μ} (4×4 on A⊗B) as linear expression in J_1
    # For test rounds on single-photon, source is |ξ^t⟩.
    rho_J1_t = rho_J_from_choi_cvxpy(
        J_expr=J_1, xi_xi_T_kron_I_const=xi_xi_T_kron_I,
        dim_A=dim_A, dim_A_prime=dim_A_prime, dim_B=dim_B,
    )

    # ---- Eq. 79d: Σ_b Y_n^{ab} = p(a|t,n) (source marginalization) ----
    # For uniform Alice signal choice p(a|t,n) = 1/2 (both |D⟩, |A⟩ equiprob)
    for n in range(N_ph + 1):
        for a in range(N_ALICE_SIGNALS):
            constraints.append(cp.sum(Y[n, a, :]) == 0.5)
    # Also non-negativity of yields
    constraints.append(Y >= 0)

    # ---- Eq. 79c: Y_1 = Φ[ρ_{J_1}^{t,μ}] ----
    # Φ[ρ] gives the observation distribution induced by ρ under the
    # POVM set indexed by (a, b).  For single-photon qubit BB84 test:
    #   Alice's X-basis measurement on her A register (source-replacement):
    #     M^A_0 = |+⟩⟨+|, M^A_1 = |−⟩⟨−|    (EB representation)
    #   Bob's POVM (X-basis on test, prob γ_B; Z-basis, prob 1−γ_B):
    #     M^B_{X,D} = γ_B · |+⟩⟨+|
    #     M^B_{X,A} = γ_B · |−⟩⟨−|
    #     M^B_{Z,0} = (1-γ_B) · |0⟩⟨0|
    #     M^B_{Z,1} = (1-γ_B) · |1⟩⟨1|
    #     M^B_{no-det} = 0 (no-detect is NOT observed on single-photon
    #                        when η_det=1; for Y_1 SDP treatment it is 0.
    #                        At honest loss, Y_1 no-det reflects loss.)
    # For the single-photon CONDITIONAL SDP (conditional on detection),
    # no-det = 1 - detection prob = per-photon loss 1-η_det effectively
    # absorbed into Y_1 as a scalar "slack".  In our simple implementation
    # the constraint Y_1[*, no-det] is unrestricted (via the SDP setting
    # p(a|t,1)=1/2 marginal including no-det).
    #
    # Here we SIMPLIFY: since Y_1 is an affine function of the SDP Choi
    # matrix, we identify Y_1 directly with Φ[ρ_{J_1}^{t,μ}] values.
    # Kamin §7.2 notes yields are independent of intensity μ (since Eve
    # cannot distinguish based on photon number [LL20]).  So a single
    # Y_1 applies across all μ.
    _plus = np.array([1.0, 1.0]) / math.sqrt(2)
    _minus = np.array([1.0, -1.0]) / math.sqrt(2)
    _e0 = np.array([1.0, 0.0])
    _e1 = np.array([0.0, 1.0])
    bob_gamma_cvx = 0.5  # placeholder; Kamin uses same γ here for simplicity

    def _povm(a_vec, b_vec):
        return np.outer(np.kron(a_vec, b_vec), np.kron(a_vec, b_vec).conj())

    # Alice POVM: |+⟩⟨+|, |−⟩⟨−| on A
    MA_D = _povm(_plus, _e0) + _povm(_plus, _e1)  # sum over Bob identity on A
    # Actually let me build properly: M^{A,a} ⊗ M^{B,b} acting on A⊗B
    MA_D_full = np.kron(np.outer(_plus, _plus.conj()), np.eye(2))
    MA_A_full = np.kron(np.outer(_minus, _minus.conj()), np.eye(2))

    MB_XD = np.kron(np.eye(2), np.outer(_plus, _plus.conj()))
    MB_XA = np.kron(np.eye(2), np.outer(_minus, _minus.conj()))
    MB_Z0 = np.kron(np.eye(2), np.outer(_e0, _e0.conj()))
    MB_Z1 = np.kron(np.eye(2), np.outer(_e1, _e1.conj()))

    # Φ[ρ]_{a,b} = Tr[ρ · M^A_a ⊗ M^B_b]
    # For Bob X/Z split with prob bob_gamma / (1-bob_gamma):
    def _phi_ab(rho_expr, MA_full, MB_full, weight):
        return weight * cp.real(cp.trace(cp.Constant(MA_full @ MB_full) @ rho_expr))

    # Y_1 constraint — link to J_1 via η_1·Φ[ρ_{J_1}^{t,μ}]  (calibrated detector)
    # Kamin Eq. 79c with calibrated-η_1 interpretation:
    #     Y_1[a, detected b] = η_1 · Φ_ab(ρ_{J_1}^{t,μ})  ∀ detected b
    #     Y_1[a, no-det]     = (1/2)·(1-η_1)  (forced by marginalization)
    # This allows single-photon loss η_1 < 1 without extending dim_B=3.
    MA_list = [MA_D_full, MA_A_full]
    MB_list_XZ = [
        (MB_XD, bob_gamma_cvx),
        (MB_XA, bob_gamma_cvx),
        (MB_Z0, 1.0 - bob_gamma_cvx),
        (MB_Z1, 1.0 - bob_gamma_cvx),
    ]
    for a in range(N_ALICE_SIGNALS):
        for b_idx, (MB_full, w) in enumerate(MB_list_XZ):
            constraints.append(
                Y[1, a, b_idx]
                == eta_1_calib * _phi_ab(rho_J1_t, MA_list[a], MB_full, w)
            )
        # Y_1[a, no-det] = (1/2)·(1 - η_1) pinned by calibration
        constraints.append(
            Y[1, a, _IDX_NOD] == 0.5 * (1.0 - eta_1_calib)
        )

    # ---- Eq. 79a: p(μ|t)·(Σ_n p_μ(n)·Y_n + δ^μ) = q^μ ----
    # Track these constraints for Lagrange dual extraction.
    # Each cell (μ, a, b) → one equality → one dual g^{μ,a,b}.
    q_constraints: dict[tuple[float, int, int], cp.Constraint] = {}
    for i_mu, mu in enumerate(intensities):
        p_n_mu = poisson_pmf_vec(mu, N_ph)  # shape (N_ph+1,)
        for a in range(N_ALICE_SIGNALS):
            for b in range(N_BOB_OUTCOMES):
                lhs = p_mu_given_t[i_mu] * (
                    sum(p_n_mu[n] * Y[n, a, b] for n in range(N_ph + 1))
                    + delta[i_mu, a, b]
                )
                c = lhs == float(q_hon_per_mu[mu][a, b])
                q_constraints[(mu, a, b)] = c
                constraints.append(c)

    # ---- Eq. 79b: 0 ≤ δ^μ ≤ 1 − p_tot(μ) ----
    constraints.append(delta >= 0)
    for i_mu, mu in enumerate(intensities):
        p_tot_mu = float(poisson_pmf_vec(mu, N_ph).sum())
        constraints.append(delta[i_mu, :, :] <= (1.0 - p_tot_mu))

    # ---- Objective: p(1|μ_sig) · W(ρ_{J_1}^g) ----
    # For generation rounds, source is |ξ^g⟩ = |ξ^t⟩ = Bell state (here
    # they coincide because BB84 source-replacement gives the same EB state).
    # So ρ_{J_1}^g = ρ_{J_1}^{t,μ} in this qubit protocol.
    rho_J1_g = rho_J1_t

    d_X = dim_A * dim_B
    tau_I = np.eye(d_X, dtype=np.complex128) / d_X
    X_expr, Y_expr = _bb84_G_Z_expressions(rho_J1_g)
    X_reg = (1.0 - epsilon_regularization) * X_expr + cp.Constant(
        epsilon_regularization * tau_I
    )
    X_aux = cp.Variable((d_X, d_X), hermitian=True)
    Y_aux = cp.Variable((d_X, d_X), hermitian=True)
    constraints.append(X_aux == X_reg)
    constraints.append(Y_aux == Y_expr)

    p_1_mu_sig = poisson_pmf(mu_sig, 1)
    objective = cp.Minimize(
        p_1_mu_sig * (1.0 - gamma) ** 2 * cp.quantum_rel_entr(X_aux, Y_aux)
    )

    prob = cp.Problem(objective, constraints)
    mosek_params = {
        "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-7,
        "MSK_DPAR_INTPNT_CO_TOL_PFEAS": 1e-7,
        "MSK_DPAR_INTPNT_CO_TOL_DFEAS": 1e-7,
        "MSK_IPAR_INTPNT_MAX_ITERATIONS": 2000,
    }
    prob.solve(solver=solver, verbose=verbose,
               mosek_params=mosek_params if solver == "MOSEK" else {})

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(
            f"Kamin decoy SDP failed: status={prob.status}, value={prob.value}"
        )

    # Objective is in "bits·(1-γ)²·p(1|μ_sig)"; divide by ln 2 for bits if
    # quantum_rel_entr gave nats (CVXPY returns nats).
    r_cross_nats = float(prob.value)
    r_cross_bits = r_cross_nats / math.log(2.0)

    # ---- Dual extraction for Kamin Eq. 82 finite-key ----
    # Sign convention (validated against A2 BB84 qubit): CVXPY dual for
    # equality constraint lhs == rhs has sign -∂(objective)/∂(rhs).
    # We flip sign so g_c = ∂(r_cross)/∂(q^μ_c).
    g_star = np.zeros(
        (len(intensities), N_ALICE_SIGNALS, N_BOB_OUTCOMES), dtype=float,
    )
    for i_mu, mu in enumerate(intensities):
        for a in range(N_ALICE_SIGNALS):
            for b in range(N_BOB_OUTCOMES):
                dual_nat = float(q_constraints[(mu, a, b)].dual_value)
                # CVXPY: dual value is in nats for quantum_rel_entr (obj in nats).
                # Flip sign + convert to bits.
                g_star[i_mu, a, b] = -dual_nat / math.log(2.0)

    return {
        "r_cross": r_cross_bits,
        "r_cross_nats": r_cross_nats,
        "J_1": np.asarray(J_1.value),
        "Y": np.asarray(Y.value),
        "delta": np.asarray(delta.value),
        "g_star": g_star,
        "status": prob.status,
        "mu_sig": mu_sig,
        "p_1_mu_sig": p_1_mu_sig,
        "gamma": gamma,
        "eta_1_calib": eta_1_calib,
        "intensities": tuple(intensities),
        "p_mu_given_t": tuple(p_mu_given_t),
    }


# ---------------------------------------------------------------------------
# Kamin Eq. 38 exact variance for decoy (multi-intensity)
# ---------------------------------------------------------------------------

def kamin_decoy_V2_eq39(
    g_star: np.ndarray,
    q_hon_per_mu: dict[float, np.ndarray],
    intensities: tuple[float, ...],
    p_mu_given_t: tuple[float, ...],
    gamma: float,
    d_A: int = 2,
    kappa: int = 1,
) -> float:
    """Kamin 2025 Eq. 38 exact variance + Eq. 39 wrapper for decoy protocol.

    Construction of the test-conditional distribution q (Σ q = 1):
        q_{μ,a,b} (test-cond) = q_hon^μ_{a,b} / p(μ|t)  (from normalization
            Σ_{a,b} q_hon^μ = p(μ|t) in our honest model).
        Weighting across intensities: p(μ|t)·q_{μ|test,μ} = q_hon^μ giving
        q_{μ,a,b} (per-round-test) = q_hon^μ_{a,b}.
        Sum Σ_{μ,a,b} q = Σ_μ p(μ|t) = 1 ✓.

    Apply Eq. 38:
        Var(p, f) = Σ_{c≠⊥} (q_c/γ)·(max(g) - g_c)² - (max(g) - g·q)²
    where c ranges over (μ, a, b).

    Ṽ² from Eq. 39:
        Ṽ² = (log₂(1 + 2·d_A^κ) + √(2 + Var))²
    """
    # Flatten g and q into 1-D vectors
    g_flat = np.zeros(len(intensities) * N_ALICE_SIGNALS * N_BOB_OUTCOMES)
    q_flat = np.zeros_like(g_flat)
    idx = 0
    for i_mu, mu in enumerate(intensities):
        q_mu = q_hon_per_mu[mu]
        for a in range(N_ALICE_SIGNALS):
            for b in range(N_BOB_OUTCOMES):
                g_flat[idx] = g_star[i_mu, a, b]
                q_flat[idx] = float(q_mu[a, b])
                idx += 1

    # Verify q sums to (1 - γ) approximately (missing = ⊥ = 1-γ prob)
    # q is per-round test-outcome distribution; Σ q = γ (prob of test).
    # For Eq. 38 we need q as test-conditional: Σ q = 1.
    q_sum = float(q_flat.sum())
    if q_sum > 0:
        q_flat = q_flat / q_sum  # normalize to test-conditional

    max_g = float(g_flat.max())
    g_dot_q = float(np.dot(g_flat, q_flat))
    # Eq. 38
    Var = float(np.sum(q_flat / gamma * (max_g - g_flat) ** 2)) \
        - (max_g - g_dot_q) ** 2
    if Var < 0.0:
        Var = 0.0
    # Eq. 39
    V_inner = math.log2(1.0 + 2.0 * d_A ** kappa) + math.sqrt(2.0 + Var)
    return V_inner ** 2


# ---------------------------------------------------------------------------
# Kamin Eq. 82 finite-key formula for decoy protocol
# ---------------------------------------------------------------------------

def kamin_decoy_full_key_length(
    intensities: tuple[float, ...],
    p_mu_given_t: tuple[float, ...],
    q_hon_per_mu: dict[float, np.ndarray],
    N_ph: int,
    n: int,
    loss_dB: float,
    theta_misalign: float,
    gamma: float,
    alpha: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
    qber_key_basis: float | None = None,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Kamin Eq. 82 finite-key length for decoy-state qubit BB84.

    Implements:
        ℓ ≤ n·(inf_J (p(1)·W + g·(q_hon − Φ) − β·ln2/2·Ṽ) − Δ_com)
          − n·β²·K(α) − λ_EC − ⌈log(1/ε_EV)⌉ − (α/(α-1))·log(1/ε_PA) + 2

    Per-round rate scales additionally by η_det (calibrated single-photon
    detection); the SDP computes the η-invariant conditional contribution.

    Unique-acceptance assumption: Δ_com = 0.  Honest state's f = g·q_hon
    (tight min-tradeoff at honest point).

    Args:
        intensities, p_mu_given_t, q_hon_per_mu, N_ph: as for kamin_decoy_choi_sdp
        n: number of signal rounds
        loss_dB: channel loss in dB (enters via η_1 = 10^(-L/10))
        theta_misalign: for K(α) span computation
        gamma, alpha: test probability + Rényi parameter
        eps_secure, f_EC: security + EC efficiency
        qber_key_basis: for λ_EC computation (default = sin²(θ_misalign))

    Returns:
        dict with ell, r_cross, V_squared, K_alpha, lambda_EC, eps_{PA,EV},
             g_star, sdp_status.
    """
    if n < 1:
        raise ValueError(f"n must be ≥ 1, got {n}")
    if loss_dB < 0.0:
        raise ValueError(f"loss_dB must be ≥ 0, got {loss_dB}")
    eta_1 = 10.0 ** (-loss_dB / 10.0)
    if qber_key_basis is None:
        qber_key_basis = math.sin(theta_misalign) ** 2

    # 1) Solve decoy SDP → r_cross + g_star
    sdp = kamin_decoy_choi_sdp(
        intensities=intensities, p_mu_given_t=p_mu_given_t,
        q_hon_per_mu=q_hon_per_mu, N_ph=N_ph, gamma=gamma,
        eta_1_calib=eta_1, solver=solver,
        epsilon_regularization=epsilon_regularization, verbose=verbose,
    )
    r_cross = sdp["r_cross"]  # p(1|μ_sig)·(1-γ)²·W_conditional
    g_star = sdp["g_star"]

    # 2) Ṽ² via Kamin Eq. 39 with exact Var from Eq. 38
    V_squared = kamin_decoy_V2_eq39(
        g_star=g_star, q_hon_per_mu=q_hon_per_mu,
        intensities=intensities, p_mu_given_t=p_mu_given_t, gamma=gamma,
    )

    # 3) K(α) via Kamin Eq. 11
    from qkdx.finite_key.kamin_geat import (
        kamin_K_alpha, optimal_eps_parameters, kamin_heuristic_key_length,
    )
    # span = κ·log(d_A) + max(g) - min_Σ(g)
    # d_A = 2 for qubit, κ = 1
    max_f = max(float(g_star.max()), 0.0)
    min_sigma_f = min(float(g_star.min()), 0.0)
    K_val = kamin_K_alpha(
        alpha=alpha, d_A=2, max_f=max_f, min_sigma_f=min_sigma_f, kappa=1,
    )

    # 4) ε-split via Eq. 57
    eps_PA, eps_EV = optimal_eps_parameters(eps_secure=eps_secure, alpha=alpha)

    # 5) λ_EC: error correction leak per sifted round × η_1 · (1-γ)² · n
    # H(S|YI)_hon = (1-γ)²·η_1·f_EC·H_2(qber_key_basis)
    if qber_key_basis <= 0 or qber_key_basis >= 1:
        H_qber = 0.0
    else:
        H_qber = (
            -qber_key_basis * math.log2(qber_key_basis)
            - (1 - qber_key_basis) * math.log2(1 - qber_key_basis)
        )
    # For decoy, λ_EC leak is across all sifted rounds (all photon numbers);
    # sift prob ≈ (1-γ)²·Q_μ_sig where Q_μ_sig is total detection rate for
    # μ_sig.  Approximate Q_μ_sig ≈ 1 - e^{-μ_sig·η_1} for WCP with per-photon
    # loss; for small eta_1·μ_sig: Q ≈ η_1·μ_sig·(1-γ)².
    # Simpler approximation: use Q_sift = η_1·μ_sig·(1-γ)² for single-photon-
    # dominated rate (conservative for multi-photon contribution).
    mu_sig = intensities[0]
    Q_sift_approx = eta_1 * mu_sig * (1.0 - gamma) ** 2
    lambda_EC = n * Q_sift_approx * f_EC * H_qber

    # 6) Per-round rate with η scaling
    # r_cross_sdp is conditional; multiply by η_1 for per-round single-photon
    # contribution.  Total per-round: R = η_1·r_cross (multi-photon absorbed in
    # decoy LP via Y_n; those contribute 0 to W).
    R_per_round = eta_1 * r_cross

    # 7) Kamin Eq. 82 key length via heuristic helper (uses V² from Eq. 39)
    ell = kamin_heuristic_key_length(
        n=n, h=R_per_round, V_squared=V_squared, K_alpha=K_val,
        alpha=alpha, lambda_EC=lambda_EC, eps_EV=eps_EV, eps_PA=eps_PA,
    )

    return {
        "ell": ell,
        "rate_per_round": ell / n,
        "R_per_round_asymp": R_per_round,
        "r_cross_sdp": r_cross,
        "V_squared": V_squared,
        "K_alpha": K_val,
        "lambda_EC": lambda_EC,
        "eps_PA": eps_PA,
        "eps_EV": eps_EV,
        "g_star": g_star,
        "eta_1": eta_1,
        "sdp_status": sdp["status"],
    }


def _decoy_ell_from_sdp_cached(
    r_cross: float,
    g_star: np.ndarray,
    intensities: tuple[float, ...],
    p_mu_given_t: tuple[float, ...],
    q_hon_per_mu: dict[float, np.ndarray],
    n: int,
    eta_1: float,
    gamma: float,
    alpha: float,
    eps_secure: float,
    f_EC: float,
    qber_key_basis: float,
    mu_sig: float,
) -> float:
    """Compute Kamin Eq. 82 ℓ from CACHED SDP result; used in (γ, α) sweep.

    Note: r_cross depends on γ (through (1-γ)² factor) and g_star depends on
    γ through the Eq. 79a LHS.  For a cached SDP we treat these as
    approximately γ-invariant at the honest point.  In practice gain from
    γ-grid is modest; this cached helper is for α-sweep primarily.
    """
    from qkdx.finite_key.kamin_geat import (
        kamin_K_alpha, optimal_eps_parameters, kamin_heuristic_key_length,
    )
    V_squared = kamin_decoy_V2_eq39(
        g_star=g_star, q_hon_per_mu=q_hon_per_mu,
        intensities=intensities, p_mu_given_t=p_mu_given_t, gamma=gamma,
    )
    max_f = max(float(g_star.max()), 0.0)
    min_sigma_f = min(float(g_star.min()), 0.0)
    K_val = kamin_K_alpha(
        alpha=alpha, d_A=2, max_f=max_f, min_sigma_f=min_sigma_f, kappa=1,
    )
    eps_PA, eps_EV = optimal_eps_parameters(eps_secure=eps_secure, alpha=alpha)
    if qber_key_basis <= 0 or qber_key_basis >= 1:
        H_qber = 0.0
    else:
        H_qber = (
            -qber_key_basis * math.log2(qber_key_basis)
            - (1 - qber_key_basis) * math.log2(1 - qber_key_basis)
        )
    Q_sift_approx = eta_1 * mu_sig * (1.0 - gamma) ** 2
    lambda_EC = n * Q_sift_approx * f_EC * H_qber
    R_per_round = eta_1 * r_cross
    return kamin_heuristic_key_length(
        n=n, h=R_per_round, V_squared=V_squared, K_alpha=K_val,
        alpha=alpha, lambda_EC=lambda_EC, eps_EV=eps_EV, eps_PA=eps_PA,
    )


def kamin_decoy_full_key_length_optimized(
    intensities: tuple[float, ...],
    p_mu_given_t: tuple[float, ...],
    q_hon_per_mu: dict[float, np.ndarray],
    N_ph: int,
    n: int,
    loss_dB: float,
    theta_misalign: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
    qber_key_basis: float | None = None,
    gamma_grid: tuple[float, ...] = (
        0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5,
    ),
    alpha_grid: tuple[float, ...] | None = None,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Grid-optimize (γ, α) for Kamin Eq. 82 decoy finite-key length.

    For efficiency, the SDP is solved once per γ (γ enters Eq. 79 objective
    via (1-γ)² factor, but only mildly).  α sweep is cached.  Auto alpha_grid
    logarithmic around 1 + 1/√n.
    """
    if not qber_key_basis:
        qber_key_basis = math.sin(theta_misalign) ** 2
    eta_1 = 10.0 ** (-loss_dB / 10.0)
    mu_sig = intensities[0]
    if alpha_grid is None:
        inv_sqrt_n = 1.0 / math.sqrt(n)
        alpha_grid = tuple(
            1.0 + scale * inv_sqrt_n
            for scale in (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0)
            if 1.0 + scale * inv_sqrt_n < 1.5
        )

    best_ell = -math.inf
    best_gamma = gamma_grid[0]
    best_alpha = alpha_grid[0]
    best_sdp_result = None

    for gamma in gamma_grid:
        sdp = kamin_decoy_choi_sdp(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_hon_per_mu, N_ph=N_ph, gamma=gamma,
            eta_1_calib=eta_1, solver=solver,
            epsilon_regularization=epsilon_regularization, verbose=verbose,
        )
        r_cross = sdp["r_cross"]
        g_star = sdp["g_star"]
        for alpha in alpha_grid:
            try:
                ell = _decoy_ell_from_sdp_cached(
                    r_cross=r_cross, g_star=g_star,
                    intensities=intensities, p_mu_given_t=p_mu_given_t,
                    q_hon_per_mu=q_hon_per_mu, n=n, eta_1=eta_1,
                    gamma=gamma, alpha=alpha, eps_secure=eps_secure,
                    f_EC=f_EC, qber_key_basis=qber_key_basis, mu_sig=mu_sig,
                )
            except (ValueError, OverflowError):
                continue
            if ell > best_ell:
                best_ell = ell
                best_gamma = gamma
                best_alpha = alpha
                best_sdp_result = sdp

    return {
        "ell_star": best_ell,
        "rate_star": best_ell / n,
        "gamma_star": best_gamma,
        "alpha_star": best_alpha,
        "eta_1": eta_1,
        "r_cross_sdp": best_sdp_result["r_cross"] if best_sdp_result else None,
        "g_star": best_sdp_result["g_star"] if best_sdp_result else None,
        "sdp_status": best_sdp_result["status"] if best_sdp_result else "none",
    }
