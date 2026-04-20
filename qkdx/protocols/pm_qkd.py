"""PM-QKD (phase-matching QKD, Ma-Zeng-Zhou 2018) protocol builder — F6 §7.5b.

Reference:
    - Ma, X., Zeng, P., Zhou, H. (2018). Phase-Matching Quantum Key Distribution.
      PRX 8:031043. arXiv:1805.05538v3.
    - docs/literature/TF-QKD.md §4.3
    - docs/msen/pm_qkd_formulation.md (Round-4 formulation with phase register R_A)
    - qkdx/analytic/pm_qkd_decoy.py (§7.5a decoy phase-error UB)

Scope (§7.5b — minimally executable protocol shell):
    * MSEBProtocol registry entry with proper five-tuple structure
    * Analytic rate bridge via pm_rate_with_decoy_phase_error
    * `scope_tag='partial'`: this module does NOT implement the full Fock-
      truncated source state + phase register R_A purification from the Round-4
      formulation (docs/msen/pm_qkd_formulation.md §1.1).  Doing so rigorously
      requires:
        - Fock truncation N_fock in the Hilbert space of A'/B' (not just analytic μ)
        - Phase register R_A of dimension M classical-purifying φ ∈ [0, 2π)
        - A Hilbert-space BS + single-click detection channel as KrausMap
        - A _conditional_alice_bob override projecting out the full (K_A, K_B) post-sift state
      This is §7.5b+ / §7.6+ future work.  For the §7.3/§7.5 analytic path,
      rate computation goes through pm_qkd_rate() which delegates to the
      Ma Eq. 4 + A33 analytic helpers directly.

Not in scope:
    * WLC SDP computation (not meaningful for this protocol without full
      Hilbert-space source/channel — analytic rate is authoritative here)
    * Per-distance μ optimization (use an external sweeper)
    * SNS variant (separate module)
"""
from __future__ import annotations

import numpy as np

from qkdx.analytic.pm_qkd import PmQkdParams
from qkdx.analytic.pm_qkd_decoy import pm_rate_with_decoy_phase_error
from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty,
)


# ---------------------------------------------------------------------------
# Placeholder quantum objects (the real Fock + phase register construction
# is §7.5b+ future work; these are minimal registry-friendly objects).
# ---------------------------------------------------------------------------


def _pm_source_state_placeholder(key_dim: int = 2, signal_dim: int = 2) -> Matrix:
    """Placeholder source state for registry purposes (uniform over key register).

    The true PM-QKD EB source state includes a phase register R_A purifying
    φ ∈ [0, 2π) (Round-4 formulation fix); implementing it in finite Hilbert
    space requires Fock truncation + discrete phase slicing, which is deferred.

    Returns:
        ρ_{KA, A'} = (|0⟩⟨0| + |1⟩⟨1|)/2 ⊗ |0⟩⟨0|_{A'}  for (key_dim=2, signal_dim=2).
        This is a fully classical state with zero signal entropy — sufficient
        for MSEBProtocol structural validation but not meaningful for WLC SDP.
    """
    dim = key_dim * signal_dim
    rho = np.zeros((dim, dim), dtype=np.complex128)
    for k in range(key_dim):
        # |k⟩⟨k| ⊗ |0⟩⟨0| on signal (always in Fock vacuum placeholder)
        idx = k * signal_dim + 0
        rho[idx, idx] = 1.0 / key_dim
    return rho


def _pm_qkd_charlie_network_placeholder() -> PublicQuantumNetwork:
    """Placeholder network: identity on combined 4-dim A' ⊗ B' (dim_in = dim_out = 4).

    Real PM-QKD Charlie channel: 50:50 BS + single-click detection {L, R, fail},
    implemented in Hilbert space would need Fock-truncated BS Kraus operators
    + detector POVMs.  Deferred (§7.5+ future work).
    """
    return PublicQuantumNetwork(channel=KrausMap.identity(4))


def _pm_qkd_sift_keep(outcomes: tuple) -> bool:
    """Sift keep: simplified Alice-Bob basis match placeholder.

    Real PM-QKD sift: Charlie announces r ∈ {L, R, fail} AND Alice/Bob
    announce phase slices j_a, j_b with |j_a − j_b| mod M ∈ {0, M/2}.
    Here we only pin the structure; true sift depends on Charlie's classical
    register which is not modelled in the placeholder network.

    Returns True when all outcomes match (structural check only).
    """
    if len(outcomes) < 2:
        return False
    return outcomes[0] == outcomes[1]


# ---------------------------------------------------------------------------
# Public builder + rate accessor
# ---------------------------------------------------------------------------


def build_pm_qkd_protocol(
    mu: float = 0.3,
    eta_channel: float = 0.5,
    params: PmQkdParams | None = None,
) -> MSEBProtocol:
    """Construct a minimally-executable PM-QKD MS-EB protocol shell (scope='partial').

    Args:
        mu: total Alice-Bob intensity (μ = μ_a + μ_b = 2μ_i), typically 0.1-1.0.
        eta_channel: total Alice-Bob channel transmittance ∈ (0, 1].
        params: PmQkdParams for detector + misalignment + M.  Default uses Ma Fig. 3b.

    Returns:
        MSEBProtocol(name="PM-QKD", scope_tag="partial", ...) — rate computation
        is via the analytic module pm_qkd_rate(p) delegating to
        pm_rate_with_decoy_phase_error.  This protocol is a registry entry;
        full MS-EB state queries (joint_state / executed_state) are out of scope.

    Raises:
        ValueError if mu or eta_channel out of valid range.
    """
    if not (mu > 0.0):
        raise ValueError(f"mu must be > 0, got {mu}")
    if not (0.0 < eta_channel <= 1.0):
        raise ValueError(f"eta_channel must be in (0, 1], got {eta_channel}")
    p = params or PmQkdParams()

    src_A = SourceParty(
        name="Alice",
        key_register_dim=2,
        signal_register_dim=2,
        source_state=_pm_source_state_placeholder(),
    )
    src_B = SourceParty(
        name="Bob",
        key_register_dim=2,
        signal_register_dim=2,
        source_state=_pm_source_state_placeholder(),
    )
    net = _pm_qkd_charlie_network_placeholder()
    ann = AnnouncementRule(sift_keep=_pm_qkd_sift_keep)
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1})

    # Parameter-bearing observables are attached via _observable_builders;
    # for this shell we expose Q_μ and E_μ^Z via the registry (identity 4×4).
    observable_builders: dict[str, object] = {
        "Q_mu": lambda _p: np.eye(4, dtype=np.complex128),
        "E_Z": lambda _p: np.eye(4, dtype=np.complex128),
        # Protocol metadata for pm_qkd_rate dispatch
        "_mu": lambda _p: mu,
        "_eta_channel": lambda _p: eta_channel,
        "_pm_params": lambda _p: p,
    }

    import warnings
    from qkdx.protocol.base import OutOfScopeWarning
    scope_reason = (
        "PM-QKD protocol shell (F6 §7.5b): source_state is placeholder (classical "
        "mixture on key register only); the full Fock-truncated + phase-register-"
        "purified EB source state from docs/msen/pm_qkd_formulation.md §1.1 is "
        "deferred.  Charlie BS + single-click detection is placeholder "
        "(KrausMap.identity(4)).  Rate computation uses the analytic "
        "pm_qkd_rate() → pm_rate_with_decoy_phase_error() path, NOT WLC SDP "
        "(the latter is not meaningful without full Hilbert-space source/channel). "
        "Upgrade to scope_tag='covered' requires: (1) Fock-truncated source state, "
        "(2) phase register R_A of dimension M, (3) Charlie BS as KrausMap, "
        "(4) conditional_alice_bob override consistent with Ma Lemma 1 reduction."
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OutOfScopeWarning)
        protocol = MSEBProtocol(
            name="PM-QKD",
            sources=(src_A, src_B),
            network=net,
            announcement=ann,
            key_map=km,
            observation_keys=("Q_mu", "E_Z"),
            scope_tag="partial",
            scope_reason=scope_reason,
            _observable_builders=observable_builders,  # type: ignore[arg-type]
        )
    return protocol


def pm_qkd_rate(protocol: MSEBProtocol, N_ph_cutoff: int = 20) -> float:
    """Per-pulse PM-QKD rate via the analytic decoy-state phase-error UB.

    Extracts (mu, eta_channel, params) from the protocol metadata and delegates
    to `pm_rate_with_decoy_phase_error` (Ma Eq. 4 + A33).

    Args:
        protocol: MSEBProtocol produced by `build_pm_qkd_protocol`.
        N_ph_cutoff: Ma A33 truncation; default 20.

    Returns:
        Per-pulse key rate (bits), may be negative below threshold.

    Raises:
        ValueError if protocol is not a PM-QKD shell (missing metadata builders).
    """
    if protocol.name != "PM-QKD":
        raise ValueError(f"pm_qkd_rate expects name='PM-QKD', got {protocol.name!r}")
    builders = protocol._observable_builders
    for k in ("_mu", "_eta_channel", "_pm_params"):
        if k not in builders:
            raise ValueError(
                f"pm_qkd_rate: protocol missing metadata key {k!r}; "
                "was it constructed via build_pm_qkd_protocol()?"
            )
    mu = builders["_mu"](protocol)
    eta_channel = builders["_eta_channel"](protocol)
    params = builders["_pm_params"](protocol)
    return pm_rate_with_decoy_phase_error(
        mu=mu, eta_channel=eta_channel, params=params, N_ph_cutoff=N_ph_cutoff,
    )
