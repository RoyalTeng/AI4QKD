"""WLC-SDP integration with decoy-state estimates.

Combines:
    * qkdx.analytic.channel:  fibre channel model (Ma 2005 §III)
    * qkdx.analytic.decoy:    decoy-state bounds on Y_1^L, e_1^U (Ma 2005 §IV)
    * qkdx.numerics.wlc:      WLC SDP for H(A|E) on single-photon BB84

The key insight: decoy state produces bounds (Y_1^L, e_1^U) that are then
fed into a *single-photon* WLC SDP.  The SDP is the standard BB84 SDP with
QBER = e_1^U as the observable constraint.  WLC returns the bits-per-sift
conditional entropy lower bound; we combine it with the decoy gain Q_1^L
and the observed signal-intensity gain Q_μ, E_μ for EC leakage:

    R = q · [Q_1^L · H(A|E)_{WLC}(e_1^U)  −  Q_μ · f · h(E_μ)]

where q = 1/2 (BB84 basis sifting).

Reference: GLLP + decoy; standard Ma-Qi-Zhao-Lo 2005 formulation.
"""
from __future__ import annotations

from dataclasses import dataclass

from qkdx.analytic.channel import FibreChannel
from qkdx.analytic.decoy import (
    DecoyEstimates, estimate_decoy_vacuum, estimate_decoy_two,
)
from qkdx.core.entropy import binary_entropy
from qkdx.numerics.wlc import wlc_key_rate, WLCResult
from qkdx.protocols.bb84 import build_bb84_protocol


@dataclass
class DecoyWLCResult:
    """Result of WLC-decoy combined computation."""
    key_rate: float             # R in bit/signal
    estimates: DecoyEstimates   # inferred Y_1^L, e_1^U, Q_1^L
    Q_mu: float                 # signal-intensity total gain
    E_mu: float                 # signal-intensity overall QBER
    h_bits_per_sift: float      # WLC single-photon H(A|E) bound
    wlc_result: WLCResult       # full WLC result (for diagnostics)
    scheme: str                 # "1-decoy-vacuum" or "2-decoy"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def decoy_wlc_rate_one(
    channel: FibreChannel,
    mu: float,
    nu: float,
    solver: str | None = None,
) -> DecoyWLCResult:
    """Decoy-state BB84 key rate using 1-decoy (weak + vacuum).

    Args:
        channel: physical channel + detector parameters
        mu: signal intensity
        nu: decoy intensity (0 < ν < μ)
        solver: override solver selection (default: auto per preferred_solver())

    Returns:
        DecoyWLCResult with fields:
            key_rate: R in bit/signal (NOT clipped at zero)
            estimates: the inferred single-photon decoy bounds
            wlc_result: underlying WLC SDP result for the single-photon BB84
    """
    return _decoy_wlc_common(
        channel, mu, estimates_fn=lambda: estimate_decoy_vacuum(channel, mu, nu),
        scheme="1-decoy-vacuum", solver=solver,
    )


def decoy_wlc_rate_two(
    channel: FibreChannel,
    mu: float,
    nu_1: float,
    nu_2: float,
    solver: str | None = None,
) -> DecoyWLCResult:
    """Decoy-state BB84 key rate using 2-decoy (μ + two non-zero decoys).

    Args:
        mu: signal intensity
        nu_1, nu_2: decoy intensities with 0 < ν₂ < ν₁ < μ and ν₁+ν₂ < μ
    """
    return _decoy_wlc_common(
        channel, mu,
        estimates_fn=lambda: estimate_decoy_two(channel, mu, nu_1, nu_2),
        scheme="2-decoy", solver=solver,
    )


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def _decoy_wlc_common(
    channel: FibreChannel,
    mu: float,
    estimates_fn,
    scheme: str,
    solver: str | None,
) -> DecoyWLCResult:
    """Shared decoy-WLC computation path."""
    est = estimates_fn()
    Q_mu = channel.Q_mu(mu)
    E_mu = channel.E_mu(mu)

    # Call WLC SDP on the single-photon BB84 with QBER = e_1^U
    # f_ec=1.0 below cancels the leak term; we add the decoy EC leak manually
    # using Q_μ and E_μ (not e_1^U) per the GLLP+decoy formula.
    bb84 = build_bb84_protocol(qber=est.e_1_upper)
    obs = {
        "qber_Z": est.e_1_upper,
        "qber_X": est.e_1_upper,
        "p_sift": 0.5,  # placeholder; we apply q and Q_1^L manually below
    }
    wlc_res = wlc_key_rate(bb84, obs, solver=solver, f_ec=1.0)

    H_one_photon = wlc_res.h_bits_per_sift  # bits per single-photon sifted round

    # Final decoy-state rate (bit/signal):
    #     R = q · [Q_1^L · H_one_photon − Q_μ · f_ec · h(E_μ)]
    q_sift = 0.5  # BB84
    privacy = est.Q_1_lower * H_one_photon
    leak_ec = Q_mu * channel.f_ec * binary_entropy(E_mu)
    key_rate = q_sift * (privacy - leak_ec)

    return DecoyWLCResult(
        key_rate=key_rate,
        estimates=est,
        Q_mu=Q_mu,
        E_mu=E_mu,
        h_bits_per_sift=H_one_photon,
        wlc_result=wlc_res,
        scheme=scheme,
    )
