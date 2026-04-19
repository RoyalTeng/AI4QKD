"""MS-EB framework data types: Π = (P, E, A, T, K)."""
from __future__ import annotations

import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap


class OutOfScopeWarning(UserWarning):
    """Raised when an MS-EB protocol is marked out-of-scope.

    Emitted at protocol construction time.  Solvers (e.g. wlc_key_rate) must
    additionally HARD-BLOCK out_of_scope protocols via `OutOfScopeError`;
    see RESEARCH_PLAN §2.1 R1.4 hard-acceptance.
    """


class OutOfScopeError(RuntimeError):
    """Raised by solvers when an out_of_scope protocol is submitted for analysis.

    The construction-time OutOfScopeWarning is informational; this error is
    the hard gate that prevents an out_of_scope protocol from silently
    producing a numeric key rate.  R1.4 requires that automatic SDP
    derivation be blocked for out_of_scope tags.
    """


class MultiSourceNotImplementedError(NotImplementedError):
    """Reserved for future use — multi-source state construction is now implemented.

    Phase 0 retrospective review (2026-04-19) introduced this exception to
    gate multi-source `joint_state()` / `executed_state()`.  Phase 1 Sub-Q2
    (commit — 2026-04-19) replaces the raises with a proper tensor-product
    + joint-channel implementation; see `MSEBProtocol.executed_state`.

    The class is retained because downstream code may still need to signal
    *other* multi-source limitations (e.g. when a specific channel model
    doesn't support the joint-signal dimension mismatch).  Currently not
    raised from the base class itself.
    """


@dataclass(frozen=True)
class SourceParty:
    """One party (Alice / Bob) in the EB representation.

    Attributes:
        name: "Alice", "Bob", etc.
        key_register_dim: dimension of the key/announcement register A.
        signal_register_dim: dimension of the signal register A' sent to channel.
        source_state: density matrix ρ_{AA'} (key_register_dim*signal_register_dim square).
    """
    name: str
    key_register_dim: int
    signal_register_dim: int
    source_state: Matrix  # shape (k*s, k*s)


@dataclass(frozen=True)
class PublicQuantumNetwork:
    """Quantum channel from Alice's signal register to Bob.

    Attributes:
        channel: KrausMap representing ℰ_{ch}: A' → B.
    """
    channel: KrausMap


@dataclass(frozen=True)
class AnnouncementRule:
    """Public announcement and sifting logic.

    Attributes:
        sift_keep: callable that takes a tuple of outcome integers
                   (one per source party) and returns True if the round is kept.
    """
    sift_keep: Callable[..., bool]


@dataclass(frozen=True)
class KeyMap:
    """Maps the key party's announcement register to the final key bit.

    Attributes:
        key_party: name of the party holding the key register.
        bitmap: {register_outcome: key_bit}, e.g. {0: 0, 1: 1, 2: 0, 3: 1}.
    """
    key_party: str
    bitmap: dict[int, int]


@dataclass(frozen=True)
class MSEBProtocol:
    """MS-EB five-tuple Π = (P, E, A, T, K).

    Pure data class + read-only query methods.  Solve logic lives in numerics/wlc.py.
    """
    name: str
    sources: tuple[SourceParty, ...]
    network: PublicQuantumNetwork
    announcement: AnnouncementRule
    key_map: KeyMap
    observation_keys: tuple[str, ...]
    symmetry_group: str | None = None
    scope_tag: Literal["covered", "partial", "out_of_scope"] = "covered"
    scope_reason: str | None = None  # required when scope_tag != "covered"
    # Internal: observable builder registry injected by protocols.
    _observable_builders: dict[str, Callable[["MSEBProtocol"], Matrix]] = field(
        default_factory=dict, compare=False, hash=False, repr=False
    )

    def __post_init__(self) -> None:
        expected_dim_in = int(np.prod([s.signal_register_dim for s in self.sources]))
        if self.network.channel.dim_in != expected_dim_in:
            raise ValueError(
                f"network.channel.dim_in ({self.network.channel.dim_in}) != "
                f"prod(signal_register_dim) ({expected_dim_in})"
            )
        party_names = {s.name for s in self.sources}
        if self.key_map.key_party not in party_names:
            raise ValueError(
                f"key_map.key_party {self.key_map.key_party!r} not in sources {party_names}"
            )
        if not self.observation_keys:
            raise ValueError("observation_keys must be non-empty")

        valid_tags = {"covered", "partial", "out_of_scope"}
        if self.scope_tag not in valid_tags:
            raise ValueError(f"scope_tag must be one of {valid_tags}, got {self.scope_tag!r}")

        if self.scope_tag != "covered" and self.scope_reason is None:
            raise ValueError(
                f"scope_reason is required when scope_tag={self.scope_tag!r}"
            )

        if self.scope_tag == "out_of_scope":
            warnings.warn(
                f"Protocol {self.name!r} is out_of_scope for MS-EB WLC SDP: "
                f"{self.scope_reason}. "
                "Automatic SDP derivation is blocked.",
                OutOfScopeWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def joint_state(self) -> Matrix:
        """Return the normalised joint EB state |ψ⟩ as a column vector.

        For N pure sources:  |ψ⟩ = |ψ_1⟩ ⊗ |ψ_2⟩ ⊗ ... ⊗ |ψ_N⟩

        The per-source ket is extracted as the max-eigenvalue eigenvector of
        each ρ_i (pure state → rank-1 → one eigenvalue ≈ 1).
        """
        psis = []
        for src in self.sources:
            eigvals, eigvecs = np.linalg.eigh(src.source_state)
            idx = np.argmax(eigvals)
            psi_i = eigvecs[:, idx : idx + 1]
            psi_i = psi_i / np.linalg.norm(psi_i)
            psis.append(psi_i)
        psi_joint = psis[0]
        for psi_i in psis[1:]:
            psi_joint = np.kron(psi_joint, psi_i)
        # Renormalise (tensor of unit vectors should already be unit, but be safe)
        return psi_joint / np.linalg.norm(psi_joint)

    def executed_state(self) -> Matrix:
        """Full density matrix after channel, before sifting.

        For N sources with key dims (k_1..k_N) and signal dims (s_1..s_N):
            1. Form ρ_joint = ρ_1 ⊗ ρ_2 ⊗ ... ⊗ ρ_N on
               (K_1 ⊗ S_1 ⊗ K_2 ⊗ S_2 ⊗ ... ⊗ K_N ⊗ S_N)
            2. Permute tensor axes to (K_1 ⊗ K_2 ⊗ ... ⊗ K_N) ⊗ (S_1 ⊗ ... ⊗ S_N)
            3. Apply (I_{K_all} ⊗ ℰ) to map combined signal register → B

        Returns ρ of shape (prod(k_i) * d_B, prod(k_i) * d_B).

        Phase 1 Sub-Q2 implementation (2026-04-19) — replaces earlier
        MultiSourceNotImplementedError path.  See docs/PHASE1_LOG.md §3.
        """
        # 1. Tensor-product source states
        rho_joint = self.sources[0].source_state
        for src in self.sources[1:]:
            rho_joint = np.kron(rho_joint, src.source_state)
        # rho_joint shape: (prod k_i s_i, prod k_i s_i)

        # 2. Reorder tensor axes: (K_1 S_1 K_2 S_2 ...) → (K_1 K_2 ... S_1 S_2 ...)
        N = len(self.sources)
        dims_per_source = []
        for src in self.sources:
            dims_per_source.extend([src.key_register_dim, src.signal_register_dim])
        # Reshape matrix to 4N-rank tensor
        # Full shape: (dims_per_source) ⊕ (dims_per_source) for ρ and ρ†
        rho_tensor = rho_joint.reshape(dims_per_source + dims_per_source)
        # Axis permutation: interleave (K, S, K, S, ...) → (K, K, ..., S, S, ...)
        key_axes = list(range(0, 2 * N, 2))      # 0, 2, 4, ..., 2N-2
        signal_axes = list(range(1, 2 * N, 2))   # 1, 3, 5, ..., 2N-1
        perm_row = key_axes + signal_axes
        perm_col = [p + 2 * N for p in perm_row]
        perm = perm_row + perm_col
        rho_perm = rho_tensor.transpose(perm)
        # Flatten back to matrix with (keys, signals) ordering
        d_keys = int(np.prod([s.key_register_dim for s in self.sources]))
        d_signals = int(np.prod([s.signal_register_dim for s in self.sources]))
        rho_matrix = rho_perm.reshape(d_keys * d_signals, d_keys * d_signals)

        # 3. Apply (I_{K_all} ⊗ ℰ): signal registers → B
        ch = self.network.channel
        if ch.dim_in != d_signals:
            raise ValueError(
                f"channel.dim_in ({ch.dim_in}) != prod(signal_register_dim) "
                f"({d_signals})"
            )
        d_b = ch.dim_out
        out = np.zeros((d_keys * d_b, d_keys * d_b), dtype=np.complex128)
        I_keys = np.eye(d_keys, dtype=np.complex128)
        for K in ch.kraus:
            IK = np.kron(I_keys, K)
            out += IK @ rho_matrix @ IK.conj().T
        return out

    def conditional_alice_bob(self) -> Matrix:
        """Sifted state ρ conditioned on sift_keep=True (renormalised).

        Protocols may register a '_conditional_alice_bob' builder to override
        the default sift-projection logic and return the correct reduced matrix.
        """
        override = self._observable_builders.get("_conditional_alice_bob")
        if override is not None:
            return override(self)  # type: ignore[return-value]
        # Default: project full executed_state with _sift_projector
        builder = self._observable_builders.get("_sift_projector")
        if builder is not None:
            P_sift = builder(self)
            rho_full = self.executed_state()
            rho_sifted = P_sift @ rho_full @ P_sift.conj().T
            p = np.trace(rho_sifted).real
            if p > 1e-12:
                return rho_sifted / p
        # Fallback: return full state (p_sift=1 case)
        return self.executed_state()

    def conditional_alice_bob_dim(self) -> int:
        """Dimension d of conditional_alice_bob(); avoids constructing the matrix."""
        builder = self._observable_builders.get("_cond_dim")
        if builder is not None:
            return int(builder(self))  # type: ignore[arg-type]
        # Fallback: infer from source + channel
        return self.sources[0].key_register_dim * self.network.channel.dim_out

    def observable(self, key: str) -> Matrix:
        """Return observable Γ_k (Hermitian, d×d) for measurement constraint."""
        if key not in self.observation_keys:
            raise ValueError(
                f"Unknown observable key {key!r}. "
                f"Protocol supports: {self.observation_keys}"
            )
        builder = self._observable_builders.get(key)
        if builder is None:
            raise ValueError(f"No observable builder registered for key {key!r}")
        return builder(self)
