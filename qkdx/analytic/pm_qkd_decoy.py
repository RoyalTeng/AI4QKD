"""PM-QKD decoy-state phase-error upper bound (Ma Appendix A.5) — F6 §7.5a.

Reference:
    - Ma, X., Zeng, P., Zhou, H. (2018). Phase-Matching Quantum Key Distribution.
      PRX 8:031043. arXiv:1805.05538v3. Appendix A.5 + B.
    - docs/literature/TF-QKD.md §4.3
    - Previous layer: qkdx/analytic/pm_qkd.py (§7.3 heuristic fallback)

Ma Appendix A.5 core formulas:
    - Eq. A33: E^X ≤ Σ_k q_{2k+1}·e_{2k+1}^Z + Σ_k q_{2k}·(1 − e_{2k}^Z)
    - Eq. A34: q_k^μ = P^μ(k) · Y_k / Q_μ  (k-photon fraction of detected signals)
    - Eq. B13: Y_k = 1 − (1 − 2·p_d)·(1 − η)^k  (honest-behavior k-photon yield)
    - Eq. B20: e_k^Z ≈ (p_d·(1-η)^k + e_δ·(1-(1-η)^k)) / Y_k
              (honest-behavior k-photon Z-basis error rate)

Infinite-decoy limit:
    When Alice uses arbitrary multi-intensity decoy states, she can extract Y_k
    and e_k^Z for each k; substituting into A33 gives the tightest possible
    phase-error UB given channel + detector (no attack-specific assumptions
    beyond those in Ma's security proof).  This module implements this limit
    numerically by truncating at N_ph and using the honest-behavior B13 / B20.

    Finite-decoy (few μ values) LP inversion is §7.5+ future work.

Scope (§7.5a):
    * Ma Eq. A33 evaluation at infinite-decoy limit (truncated honest values)
    * pm_rate_with_decoy_phase_error: Eq. 4 with A33-based UB

Not in scope:
    * Multi-intensity finite-decoy LP inversion (§7.5 later)
    * qkdx/protocols/pm_qkd.py protocol builder (§7.5b)
"""
from __future__ import annotations

import math

from qkdx.analytic.pm_qkd import (
    PmQkdParams,
    pm_charlie_gain,
    pm_k_photon_yield,
    pm_vacuum_yield,
)


def _binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def pm_k_photon_error_rate_honest(
    k: int,
    eta_total: float,
    p_d: float,
    e_delta: float,
) -> float:
    """Ma Appendix B Eq. B20 — honest-behavior k-photon Z-basis error rate:

        e_k^Z ≈ [ p_d · (1 − η)^k + e_δ · (1 − (1 − η)^k) ] / Y_k

    Physical interpretation:
        - (1 − η)^k · p_d fraction: k-photon state is NOT detected
          (all absorbed to environment), but dark-count contributes a click
          with probability ~p_d (error = 1 because vacuum-like click is random
          but Ma's B20 approximation uses the simpler structure here).
        - [1 − (1 − η)^k] fraction: at least one photon is detected;
          phase-slice misalignment induces error at rate e_δ.
        - Normalized by Y_k = 1 − (1-2p_d)·(1-η)^k (Ma Eq. B13).

    Limits:
        - k = 0: e_0^Z = p_d / Y_0 = p_d / (2·p_d) = 1/2 (random)
        - k large, η > 0: e_k^Z → e_δ · 1 / 1 = e_δ
        - η = 0: e_k^Z = p_d / (2·p_d) = 1/2 (no signal, pure dark)

    Args:
        k: photon number (≥ 0).
        eta_total: effective per-click efficiency η = η_arm · η_det.
        p_d: dark-count probability per detector per pulse.
        e_delta: effective signal QBER (phase-slice + misalignment).

    Returns:
        e_k^Z ∈ [0, 0.5].

    Raises:
        ValueError on invalid k or parameters.
    """
    if k < 0:
        raise ValueError(f"k must be ≥ 0, got {k}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    if not (0.0 <= e_delta <= 0.5):
        raise ValueError(f"e_delta must be in [0, 0.5], got {e_delta}")

    Y_k = pm_k_photon_yield(k=k, eta_total=eta_total, p_d=p_d)
    if Y_k <= 0.0:
        return 0.5  # degenerate; max entropy

    one_minus_eta_k = (1.0 - eta_total) ** k
    numerator = p_d * one_minus_eta_k + e_delta * (1.0 - one_minus_eta_k)
    return min(max(numerator / Y_k, 0.0), 0.5)


def pm_decoy_q_k_fraction(k: int, mu: float, Y_k: float, Q_mu: float) -> float:
    """Ma Eq. A34: q_k^μ = P^μ(k) · Y_k / Q_μ.

    Fraction of k-photon events among detected clicks at intensity μ.

    Args:
        k: photon number.
        mu: signal intensity.
        Y_k: k-photon yield.
        Q_mu: total gain at μ.

    Returns:
        q_k ∈ [0, 1].
    """
    if k < 0:
        raise ValueError(f"k must be ≥ 0, got {k}")
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if Q_mu <= 0.0:
        return 0.0
    p_k = math.exp(-mu) * mu ** k / math.factorial(k)
    return p_k * Y_k / Q_mu


def pm_decoy_phase_error_upper(
    mu: float,
    eta_total: float,
    params: PmQkdParams = PmQkdParams(),
    N_ph_cutoff: int = 20,
) -> float:
    """Ma Eq. A33 phase-error upper bound at infinite-decoy limit.

        E^X ≤ Σ_{k=0}^{N_ph} q_{2k+1}·e_{2k+1}^Z
               + Σ_{k=0}^{N_ph} q_{2k}·(1 − e_{2k}^Z)

    Evaluated with honest-behavior Y_k (Ma Eq. B13) and e_k^Z (Ma Eq. B20),
    truncated at N_ph_cutoff photons.  This is the infinite-decoy limit
    (arbitrary multi-intensity inversion can in principle extract Y_k for each
    k); for finite-decoy bounds see §7.5 future work.

    **Internal Q_μ convention (Round-2 fix for Codex §7.5a review)**:
        `Q_μ` used inside this function is the **truncated exact** form
        `Σ_{k=0}^{N_ph} P^μ(k)·Y_k`, which satisfies Ma A34/A35 self-consistency
        (`Σ_k q_k = 1` up to truncation error).  It is NOT `pm_charlie_gain`
        (Ma B14 approximation), which carries an extra `(1-p_d)` factor coming
        from B14's further approximation step and breaks A34 normalization at
        non-zero p_d (e.g., `Σ q_k ≈ 1/(1-p_d) > 1` at moderate p_d).

    **Physical interpretation of A33**:
        - Odd-photon components (k = 2m+1) carry phase information faithfully
          (Ma Lemma 1); their Z-basis error rate e_{2m+1}^Z bounds the X-basis
          phase error contribution.
        - Even-photon components (k = 2m) erase the key bit; their contribution
          to phase error is (1 − e_{2m}^Z) (the fraction that does NOT cancel).
        - Sum over all k weighted by q_k (fraction of k-photon detection events).

    Args:
        mu: total intensity.
        eta_total: effective per-click efficiency η = η_arm · η_det.
        params: PmQkdParams (uses p_d, e_delta).
        N_ph_cutoff: truncation N_ph (larger → tighter); default 20 is enough
                     for μ ∈ [0.1, 1.0] (Poisson tail at k>20 is numerically zero).

    Returns:
        E^X ∈ [0, 0.5] upper bound.

    Raises:
        ValueError on invalid inputs.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if N_ph_cutoff < 1:
        raise ValueError(f"N_ph_cutoff must be ≥ 1, got {N_ph_cutoff}")

    if mu <= 0.0 or eta_total <= 0.0:
        # μ = 0: all vacuum, E^X = 1/2 (uniform).  η = 0: no signal, E^X = 1/2.
        return 0.5

    p_d = params.p_d
    e_delta = params.e_delta

    # Precompute Y_k and P^μ(k) over the truncation window.
    Y_ks = [pm_k_photon_yield(k=k, eta_total=eta_total, p_d=p_d) for k in range(N_ph_cutoff + 1)]
    # P^μ(k) = e^{-μ} μ^k / k!
    p_mu = [math.exp(-mu) * mu ** k / math.factorial(k) for k in range(N_ph_cutoff + 1)]

    # Ma A35 exact (truncated) Q_μ: Σ P^μ(k)·Y_k
    Q_mu_truncated = sum(p_k * Y_k for p_k, Y_k in zip(p_mu, Y_ks))
    if Q_mu_truncated <= 0.0:
        return 0.5

    # Accumulate A33 sum using self-consistent q_k (so Σ q_k = 1 exactly).
    total = 0.0
    for k in range(N_ph_cutoff + 1):
        q_k = p_mu[k] * Y_ks[k] / Q_mu_truncated
        e_k = pm_k_photon_error_rate_honest(
            k=k, eta_total=eta_total, p_d=p_d, e_delta=e_delta,
        )
        if k % 2 == 1:
            # odd photon: phase info, contributes e_{2m+1}^Z
            total += q_k * e_k
        else:
            # even photon: phase erased, contributes (1 − e_{2m}^Z)
            total += q_k * (1.0 - e_k)

    return min(max(total, 0.0), 0.5)


def pm_decoy_q_mu_exact(
    mu: float,
    eta_total: float,
    p_d: float,
    N_ph_cutoff: int = 20,
) -> float:
    """Ma A35 exact (truncated) total gain: Q_μ = Σ_{k=0}^{N_ph} P^μ(k)·Y_k.

    This differs from `pm_charlie_gain` (Ma B14 approximation form) by a factor
    (1-p_d) coming from B14's further approximation.  Use this form for any
    A34-consistent decoy calculation where Σ_k q_k = 1 must hold exactly.

    Returns:
        Q_μ ∈ [0, 1].
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if N_ph_cutoff < 1:
        raise ValueError(f"N_ph_cutoff must be ≥ 1, got {N_ph_cutoff}")
    total = 0.0
    for k in range(N_ph_cutoff + 1):
        Y_k = pm_k_photon_yield(k=k, eta_total=eta_total, p_d=p_d)
        P_k = math.exp(-mu) * mu ** k / math.factorial(k)
        total += P_k * Y_k
    return min(max(total, 0.0), 1.0)


def pm_rate_with_decoy_phase_error(
    mu: float,
    eta_channel: float,
    params: PmQkdParams = PmQkdParams(),
    N_ph_cutoff: int = 20,
) -> float:
    """Ma Eq. 4 per-pulse rate with Ma Eq. A33 decoy-state phase-error UB.

        R_PM ≥ (2/M) · Q_μ · [1 − H(E^X_decoy) − f_EC · H(E_μ^Z)]

    Replaces the heuristic `pm_phase_error_upper` fallback with the tighter
    decoy-state `pm_decoy_phase_error_upper` evaluation (Ma Eq. A33).

    **Round-2 fix**:  Q_μ in this path is the exact truncated Σ P^μ(k)·Y_k
    (via `pm_decoy_q_mu_exact`), self-consistent with the q_k normalization
    in `pm_decoy_phase_error_upper`.  Earlier version used the B14 approximation
    from `pm_charlie_gain`, which is off by a factor (1-p_d) from the A35 exact
    form.  For the default p_d=8e-8 the numerical difference is <10^{-7}, but
    at higher p_d the gap grows.  The bit-error rate `E_μ^Z` still uses the
    Ma B22 closed-form approximation (a known heuristic noted in Ma §V); full
    self-consistency here would require a matching A35 reformulation for E_Z,
    which is §7.5+ follow-up.

    Args:
        mu: intensity.
        eta_channel: total Alice-Bob channel transmittance (per-arm = √η_channel).
        params: PmQkdParams.
        N_ph_cutoff: truncation for A33 sum.

    Returns:
        Per-pulse key rate (bits), may be negative.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_channel <= 1.0):
        raise ValueError(f"eta_channel must be in [0, 1], got {eta_channel}")

    # Import here to avoid circular refs with qkdx.analytic.pm_qkd
    from qkdx.analytic.pm_qkd import pm_bit_error_rate

    eta_arm = math.sqrt(eta_channel)
    eta_eff = eta_arm * params.eta_det

    # Self-consistent Q_μ matching A34/A35 (Round-2 fix): exact truncated sum
    Q_mu = pm_decoy_q_mu_exact(
        mu=mu, eta_total=eta_eff, p_d=params.p_d, N_ph_cutoff=N_ph_cutoff,
    )
    E_Z = pm_bit_error_rate(
        mu=mu, eta_total=eta_eff, p_d=params.p_d, e_delta=params.e_delta,
    )
    E_X = pm_decoy_phase_error_upper(
        mu=mu, eta_total=eta_eff, params=params, N_ph_cutoff=N_ph_cutoff,
    )

    privacy = 1.0 - _binary_entropy(E_X)
    leak_ec = params.f_ec * _binary_entropy(E_Z)
    per_sift_net = privacy - leak_ec

    return (2.0 / params.M) * Q_mu * per_sift_net
