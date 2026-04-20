"""PLOB / Pirandola / TGW upper bounds for QKD two-way secret-key capacity.

Phase 2 Sub-Q3 §4.4 numerical tool.

References:
    - PLOB 2017 (Nat Comm 8:15043)     → docs/literature/PLOB-2017.md
    - Pirandola 2019 (Comm Phys 2:51)  → docs/literature/Pirandola-2019.md
    - TGW 2014 (Nat Comm 5:5235)       → docs/literature/TGW-2014.md
    - WTB 2017 (IEEE TIT 63:1792)      → docs/literature/WTB-2017.md
    - Topology applicability Lemma 1   → docs/msen/topology_applicability.md

Scope:
    * Closed-form upper bounds for distillable channels (lossy, amplifier,
      dephasing, erasure)
    * TGW-style squashed-entanglement bound (historical / non-distillable)
    * Topology-aware dispatch: protocol family → correct upper bound
    * Gap analysis helpers for Sub-Q3 §4.3 data

Not in scope (future §4.4+):
    * Full E_R numerical computation (REE optimization over separable states)
    * E_sq(N) numerical for non-Gaussian channels
    * Second-order expansion (needs per-channel relative entropy variance)
    * Network max-flow multi-path capacities (Pirandola §multi-path)
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# Closed-form upper bounds for distillable channels
# ---------------------------------------------------------------------------

def e_r_lossy_point_to_point(eta: float) -> float:
    """PLOB 2017 Eq. 19: C(η) = -log_2(1 - η) for pure-loss channel.

    Applies to Type A protocols (BB84, six-state, Efficient BB84, SARG04).
    WTB 2017 Thm 26 strengthens this to strong converse.

    Args:
        eta: transmittance ∈ [0, 1].

    Returns:
        Upper bound in bits per channel use.  ∞ at η = 1.

    Raises:
        ValueError on invalid η.
    """
    if not (0.0 <= eta <= 1.0):
        raise ValueError(f"eta must be in [0, 1], got {eta}")
    if eta == 1.0:
        return float("inf")
    return -math.log2(1.0 - eta)


def e_r_lossy_repeater_chain(eta_total: float, N_repeaters: int) -> float:
    """Pirandola 2019 Eq. 9: C_loss(η, N) = -log_2(1 - η^{1/(N+1)}).

    Equispaced repeater chain (N internal nodes; each link transmittance
    η_link = η_total^{1/(N+1)}).

    Applies to:
    - N = 0: point-to-point (= PLOB direct-link)
    - N = 1: TF-QKD / PM-QKD / MDI Type B topology, C = -log_2(1 - √η_total)

    The upper bound applies even if the relay is untrusted (Pirandola
    §Discussion).

    Args:
        eta_total: end-to-end Alice-Bob transmittance.
        N_repeaters: number of internal (possibly untrusted) repeater nodes.
                     N=0 for direct link, N=1 for TF/PM/MDI.

    Returns:
        Upper bound in bits per channel use.
    """
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if N_repeaters < 0:
        raise ValueError(f"N_repeaters must be ≥ 0, got {N_repeaters}")
    if eta_total == 1.0:
        return float("inf")
    eta_link = eta_total ** (1.0 / (N_repeaters + 1))
    return -math.log2(1.0 - eta_link)


def e_r_tgw_lossy(eta: float) -> float:
    """TGW 2014 Eq. 1: log_2[(1+η)/(1-η)] squashed-entanglement upper bound.

    Looser than PLOB by 2× at η ≪ 1 (2.88η vs 1.44η).
    Kept for historical reference and for non-distillable-channel extension
    (where squashed-E may be tighter than REE; Sub-Q3 §4.4 future work).
    """
    if not (0.0 <= eta < 1.0):
        raise ValueError(f"eta must be in [0, 1), got {eta}")
    return math.log2((1.0 + eta) / (1.0 - eta))


def e_r_ql_amplifier(g: float) -> float:
    """PLOB 2017 Eq. 28: C(g) = -log_2(1 - 1/g) for quantum-limited amplifier."""
    if g < 1.0:
        raise ValueError(f"gain must be ≥ 1, got {g}")
    if g == 1.0:
        return float("inf")
    return -math.log2(1.0 - 1.0 / g)


def _binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def e_r_dephasing(p: float) -> float:
    """PLOB 2017 Eq. 39: C = 1 - H_2(p) for single-qubit dephasing prob p."""
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    return 1.0 - _binary_entropy(p)


def e_r_erasure(p: float) -> float:
    """PLOB 2017 Eq. 43: C = 1 - p for single-qubit erasure prob p."""
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    return 1.0 - p


# ---------------------------------------------------------------------------
# Topology dispatch (Lemma 1 of docs/msen/topology_applicability.md)
# ---------------------------------------------------------------------------

_TYPE_A_PROTOCOLS = frozenset({
    "bb84", "six-state", "sixstate", "efficient-bb84", "efficient_bb84",
    "sarg04",
})
_TYPE_B_PROTOCOLS = frozenset({
    "mdi", "mdi-qkd", "mdiqkd",
    "tf", "tf-qkd", "tfqkd",
    "sns", "sns-tf", "sns-tfqkd", "sns-tf-qkd",
    "pm", "pm-qkd", "pmqkd",
})


def topology_type_of_protocol(name: str) -> str:
    """Map protocol name → topology type per Lemma 1.

    Args:
        name: protocol name (case-insensitive); e.g. "BB84", "PM-QKD", "MDI".

    Returns:
        "A" (point-to-point direct) or "B" (untrusted-relay single-chain).

    Raises:
        ValueError for unknown protocol name.
    """
    lo = name.strip().lower()
    if lo in _TYPE_A_PROTOCOLS:
        return "A"
    if lo in _TYPE_B_PROTOCOLS:
        return "B"
    raise ValueError(
        f"Unknown protocol {name!r}. "
        f"Known Type A: {sorted(_TYPE_A_PROTOCOLS)}. "
        f"Known Type B: {sorted(_TYPE_B_PROTOCOLS)}."
    )


def bound_by_topology(protocol_name: str, eta_channel: float) -> float:
    """Apply correct upper bound based on protocol family.

    Type A (direct-link):  -log_2(1 - η)           [PLOB]
    Type B (N=1 relay):    -log_2(1 - √η)          [Pirandola Eq. 9 at N=1]

    Args:
        protocol_name: protocol family name.
        eta_channel: total Alice-Bob transmittance.

    Returns:
        Upper bound in bits/channel use.
    """
    topo = topology_type_of_protocol(protocol_name)
    if topo == "A":
        return e_r_lossy_point_to_point(eta_channel)
    elif topo == "B":
        return e_r_lossy_repeater_chain(eta_channel, N_repeaters=1)
    else:
        raise RuntimeError(f"unexpected topology type {topo}")


# ---------------------------------------------------------------------------
# Comparison + gap analysis helpers
# ---------------------------------------------------------------------------

def bound_comparison_lossy(eta: float) -> dict[str, float]:
    """Compare PLOB direct / Pirandola N=1 / TGW at same η.

    Returns dict with keys: plob_direct, pirandola_n1, tgw.
    Useful for Sub-Q3 §4.3 sanity tables.
    """
    return {
        "plob_direct": e_r_lossy_point_to_point(eta),
        "pirandola_n1": e_r_lossy_repeater_chain(eta, N_repeaters=1),
        "tgw": e_r_tgw_lossy(eta),
    }


def gap_ratio(actual_rate: float, upper_bound: float) -> float:
    """Ratio upper_bound / actual_rate.

    Sub-Q4 gap-attribution primitive: large gap → B (lower bound loose) or C.

    Args:
        actual_rate: protocol achievable rate (e.g., from pm_rate_with_decoy_phase_error).
        upper_bound: theoretical upper bound (e.g., Pirandola N=1).

    Returns:
        Gap ratio (dimensionless).  +∞ if actual_rate ≤ 0.

    Raises:
        ValueError if actual_rate < 0 or upper_bound < 0.
    """
    if actual_rate < 0.0:
        raise ValueError(f"actual_rate must be ≥ 0, got {actual_rate}")
    if upper_bound < 0.0:
        raise ValueError(f"upper_bound must be ≥ 0, got {upper_bound}")
    if actual_rate <= 0.0:
        return float("inf")
    return upper_bound / actual_rate
