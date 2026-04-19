"""MS-EB framework data types: Π = (P, E, A, T, K)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap


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

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def joint_state(self) -> Matrix:
        """Return the normalised joint EB state |ψ⟩_{AA'} as a column vector."""
        # For a single source, return its purification (dominant eigenvector of source_state)
        src = self.sources[0]
        rho = src.source_state
        # rho = |ψ⟩⟨ψ| for a pure source; extract ket
        eigvals, eigvecs = np.linalg.eigh(rho)
        idx = np.argmax(eigvals)
        psi = eigvecs[:, idx : idx + 1]
        # Normalise
        psi = psi / np.linalg.norm(psi)
        return psi

    def executed_state(self) -> Matrix:
        """Full density matrix ρ_{AB} after channel, before sifting."""
        src = self.sources[0]
        d_a = src.key_register_dim
        d_signal = src.signal_register_dim

        rho_aa_prime = src.source_state  # (d_a * d_signal, d_a * d_signal)
        ch = self.network.channel

        # Partial trace over A' then apply channel: keep A, map A' → B
        # ρ_{AB} = (I_A ⊗ ℰ)(ρ_{AA'})
        d_b = ch.dim_out
        out = np.zeros((d_a * d_b, d_a * d_b), dtype=np.complex128)
        for K in ch.kraus:
            # (I_A ⊗ K) ρ_{AA'} (I_A ⊗ K†)
            IK = np.kron(np.eye(d_a, dtype=np.complex128), K)
            out += IK @ rho_aa_prime @ IK.conj().T
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
