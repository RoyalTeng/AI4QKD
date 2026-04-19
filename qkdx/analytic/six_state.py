"""Six-state QKD asymptotic key rate (symmetric depolarizing channel).

Reference:
- Bruss 1998, PRL 81:3018 (original six-state protocol)
- Lo 2001, QIC 1:81-94 (unconditional security + ~12.62% threshold)
- Scarani et al. 2009, RMP 81:1301, §III.D.1

Derivation (see docs/literature/six-state.md §3.4):

Under symmetric depolarizing channel with QBER_Z = QBER_X = QBER_Y = e,
the WLC-optimal state on A_key ⊗ B is the Bell-diagonal Werner state
    ρ* = (1-3e/2)|Φ+⟩⟨Φ+| + (e/2)(|Φ−⟩⟨Φ−| + |Ψ+⟩⟨Ψ+| + |Ψ−⟩⟨Ψ−|)

Applying G=identity + Z-pinching on key register:

    H(Z(G(ρ*))) = 1 + h(e)
    H(G(ρ*))   = -(1-3e/2)·log2(1-3e/2) - 3·(e/2)·log2(e/2)

Thus:
    H_six(A|E) = D(G(ρ*) ‖ Z(G(ρ*))) = H(Z(G(ρ*))) - H(G(ρ*))
               = 1 + h(e) + (1-3e/2)·log2(1-3e/2) + (3e/2)·log2(e/2)

And the Devetak-Winter asymptotic key rate (bit/signal):
    R_six(e, f_ec) = p_sift · (H_six(A|E) - f_ec·h(e)),  p_sift = 1/3

Acceptance (RESEARCH_PLAN §2.2 R2.3):
- Must match WLC SDP on symmetric six-state to abs=5e-4, rel=0.01 (MOSEK)
- At e=0: R = 1/3 bit/signal
- At e ≈ 12.62%: R ≈ 0 (Lo 2001 threshold)
"""
from __future__ import annotations

import math

from qkdx.core.entropy import binary_entropy


def _safe_xlog2x(x: float) -> float:
    """Return x·log2(x), with the convention 0·log2(0) = 0."""
    if x <= 0.0:
        return 0.0
    return x * math.log2(x)


def six_state_conditional_entropy(qber: float) -> float:
    """Asymptotic H(A|E) lower bound for symmetric six-state [bits/sift].

    H_six(A|E) = 1 + h(e) + (1-3e/2)·log2(1-3e/2) + (3e/2)·log2(e/2)

    Args:
        qber: QBER e ∈ [0, 2/3]. Beyond 2/3, the Werner-state coefficient
              1-3e/2 turns negative and the formula is unphysical.

    Returns:
        H_six(A|E) in bits per sifted round.
    """
    if qber < 0.0 or qber > 2.0 / 3.0:
        raise ValueError(f"QBER must be in [0, 2/3] for six-state, got {qber}")

    e = qber
    lam_phi_plus = 1.0 - 1.5 * e
    lam_other = 0.5 * e  # λ on |Φ−⟩,|Ψ+⟩,|Ψ−⟩ individually

    # H(Z(G(ρ*))) = 1 + h(e)  (pinched diagonal gives uniform-ish 4 eigenvalues
    # with pairwise equal entries (1-e)/2 and e/2)
    h_pinched = 1.0 + binary_entropy(e)

    # H(G(ρ*)) = -λ_Φ+ log2(λ_Φ+) - 3·λ_other log2(λ_other)
    h_rho_star = -(_safe_xlog2x(lam_phi_plus) + 3.0 * _safe_xlog2x(lam_other))

    return h_pinched - h_rho_star


def six_state_rate(qber: float, f_ec: float = 1.16) -> float:
    """Asymptotic key rate R = p_sift · [H_six(A|E) - f_ec · h(e)] [bit/signal].

    p_sift = 1/3 for symmetric six-state (uniform basis choice from 3 MUBs).

    At f_ec = 1.0 (ideal EC):
    - R(0)      = 1/3  bit/signal
    - R(0.05)   ≈ 0.1657 bit/signal (hand-computed in docs/literature/six-state.md §4)
    - R(0.126)  ≈ 0     bit/signal (Lo 2001 threshold)

    No max(0, ...) clip: negative values below threshold are returned as-is,
    for fair numerical comparison with WLC SDP (§ the Shor-Preskill convention).
    """
    p_sift = 1.0 / 3.0
    h_cond = six_state_conditional_entropy(qber)
    leak_ec = f_ec * binary_entropy(qber)
    return p_sift * (h_cond - leak_ec)
