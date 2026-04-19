"""Finite-key analytic formulas (George-Lin-Lütkenhaus 2021 + Renner framework).

Phase 1 S2.5 foundation (RESEARCH_PLAN §3.3):
    Implements the analytic formulas from GLL-2021 (arXiv:2004.11865v2, §II)
    that don't require SDP solving — these provide the "zero-ish cost"
    baseline for any finite-key QKD analysis in the Renner framework.

**Scope note**:
    - Asymptotic numerical method (WLC 2018 SDP) + finite-key SDP (GLL 2021
      Eq. 14) are NOT in this module.  That is full-SDP work deferred until
      Kamin 2025 reproduction path is clarified.
    - This module provides the *parameter-estimation* layer (variation bound
      μ, smooth-entropy correction δ) that is common to any finite-key
      method in Renner framework.

References:
    - George, Lin, Lütkenhaus 2021.  Numerical calculations of the finite
      key rate for general QKD protocols.  PRR 3:013274.
    - Renner 2005.  Security of QKD.  ETH Zürich PhD thesis, Ch. 6.
    - docs/literature/GLL-2021.md §3 (Level 3 memo)
"""
from __future__ import annotations

import math


def variation_bound(
    m: int,
    eps_PE: float,
    alphabet_size: int,
) -> float:
    """Variation-distance upper bound μ between measured frequency and true state.

    GLL-2021 Eq. 4:
        μ = √[ 2·(ln(1/ε_PE) + |Σ| · ln(m+1)) / m ]

    Derived from Lemma 2 of Renner 2005 (via Chernoff-Hoeffding inequality
    applied to the L1 distance of frequency estimates).  For sample size m
    from alphabet of size |Σ|, with probability at least 1 - ε_PE,
        || F_observed - Φ_𝒫(ρ) ||_1 ≤ μ
    for the true state ρ.

    Args:
        m: parameter-estimation sample count (>= 1)
        eps_PE: parameter-estimation failure probability (0 < ε < 1)
        alphabet_size: |Σ| — number of distinct measurement outcomes

    Returns:
        μ > 0 in [0, 2] (variation distance is bounded above by 2)

    Raises:
        ValueError: invalid inputs
    """
    if m < 1:
        raise ValueError(f"m must be ≥ 1, got {m}")
    if not (0.0 < eps_PE < 1.0):
        raise ValueError(f"eps_PE must be in (0, 1), got {eps_PE}")
    if alphabet_size < 1:
        raise ValueError(f"alphabet_size must be ≥ 1, got {alphabet_size}")
    numerator = math.log(1.0 / eps_PE) + alphabet_size * math.log(m + 1.0)
    return math.sqrt(2.0 * numerator / m)


def delta_smoothing(
    eps_bar: float,
    n: int,
    key_alphabet_size: int,
) -> float:
    """Smooth min-entropy vs von Neumann gap (GLL-2021 Eq. 3).

        δ(ε̄) = 2 · log2(d + 3) · √(log2(2/ε̄) / n)

    This term represents the gap (per signal) between the von Neumann
    conditional entropy H(X|E) and the smooth min-entropy H_min^{ε̄}(X|E)
    that actually appears in privacy amplification (Renner 2005 AEP).

    Args:
        eps_bar: smoothing parameter (0 < ε̄ < 1)
        n: key-generation sample count (>= 1)
        key_alphabet_size: d — Alice's key output alphabet size (e.g., BB84 → 2)

    Returns:
        δ ≥ 0 (units: bits per signal)

    Raises:
        ValueError: invalid inputs
    """
    if n < 1:
        raise ValueError(f"n must be ≥ 1, got {n}")
    if not (0.0 < eps_bar < 1.0):
        raise ValueError(f"eps_bar must be in (0, 1), got {eps_bar}")
    if key_alphabet_size < 1:
        raise ValueError(f"key_alphabet_size must be ≥ 1, got {key_alphabet_size}")
    d = key_alphabet_size
    return 2.0 * math.log2(d + 3) * math.sqrt(math.log2(2.0 / eps_bar) / n)


def _h(p: float) -> float:
    """Binary entropy, 0 · log 0 = 0 convention."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def bb84_finite_key_length_analytic(
    n: int,
    m: int,
    e_x: float,
    e_z: float | None = None,
    eps_PE: float = 2.5e-9,
    eps_bar: float = 2.5e-9,
    eps_EC: float = 2.5e-9,
    eps_PA: float = 2.5e-9,
    f_EC: float = 1.2,
    alphabet_size: int = 2,
    key_alphabet_size: int = 2,
) -> float:
    """BB84 finite-key length ℓ (bits), analytic formula per GLL-2021 Eq. 19.

        ℓ = n·[1 - h(e_x + μ/2) - f_EC · h(e_z) - δ(ε̄)]
            - log2(2/ε_EC) - 2·log2(2/ε_PA)

    where:
        - e_x = phase-error rate (X-basis observed)
        - e_z = bit-error rate (Z-basis observed); default e_z = e_x
        - μ = variation bound (Eq. 4) evaluated at (m, ε_PE, alphabet_size)
        - δ(ε̄) = smoothing correction (Eq. 3) evaluated at (ε̄, n, key_alphabet_size)
        - total ε-security: ε = ε_PE + ε̄ + ε_EC + ε_PA ≈ 10^-8 for default args

    Valid for BB84 unique-acceptance PM protocol with Z-basis key generation.
    Phase-error coarse-graining + fine-grained agreement via phase-error POVM
    (GLL-2021 §IV.A, Eq. 18).

    Args:
        n: key-generation sample count
        m: parameter-estimation sample count
        e_x: observed phase-error rate (∈ [0, 0.5])
        e_z: observed bit-error rate (default = e_x, symmetric case)
        eps_PE, eps_bar, eps_EC, eps_PA: ε-security sub-terms (default 2.5e-9
            each → total ε = 10^-8)
        f_EC: error-correction efficiency (≥ 1.0)
        alphabet_size: |Σ| parameter-estimation alphabet (BB84: 2 phase-error bits)
        key_alphabet_size: d Alice's key output alphabet (BB84: 2)

    Returns:
        ℓ in bits (can be negative; clip at 0 for operational use).

    Raises:
        ValueError: invalid input.

    References:
        GLL-2021 Eq. 19 (phase-error analytic formula, unique-acceptance BB84)
        docs/literature/GLL-2021.md §4.1
    """
    if n < 1 or m < 1:
        raise ValueError(f"n and m must be ≥ 1, got n={n}, m={m}")
    if not (0.0 <= e_x <= 0.5):
        raise ValueError(f"e_x must be in [0, 0.5], got {e_x}")
    if e_z is None:
        e_z = e_x
    if not (0.0 <= e_z <= 0.5):
        raise ValueError(f"e_z must be in [0, 0.5], got {e_z}")
    if f_EC < 1.0:
        raise ValueError(f"f_EC must be ≥ 1.0, got {f_EC}")
    for name, val in [("eps_PE", eps_PE), ("eps_bar", eps_bar),
                       ("eps_EC", eps_EC), ("eps_PA", eps_PA)]:
        if not (0.0 < val < 1.0):
            raise ValueError(f"{name} must be in (0, 1), got {val}")

    mu = variation_bound(m, eps_PE, alphabet_size)
    delta = delta_smoothing(eps_bar, n, key_alphabet_size)

    # Phase-error + μ/2 correction (Eq. 19)
    e_x_adjusted = min(e_x + mu / 2.0, 0.5)
    h_phase_error = _h(e_x_adjusted)
    h_bit_error = _h(e_z)

    # Per-signal key rate
    per_signal = 1.0 - h_phase_error - f_EC * h_bit_error - delta

    # Finite-key final-block terms
    leak_EC_log = math.log2(2.0 / eps_EC)
    PA_log = math.log2(2.0 / eps_PA)

    ell = n * per_signal - leak_EC_log - 2.0 * PA_log
    return ell


def bb84_finite_key_rate_per_block(
    n: int,
    m: int,
    e_x: float,
    **kwargs,
) -> float:
    """Per-accepted-round BB84 finite-key rate R_block = ℓ / (n + m).

    **API semantic note** (Round 1 reviewer):
    n + m is the POSTSELECTED/ACCEPTED rounds count (key-gen + PE sample).
    This rate is "bit per accepted round", NOT "bit per transmitted signal".
    For "bit per signal" accounting (matching the rest of this repo's
    convention), use `bb84_finite_key_rate_per_signal()` with an explicit
    `p_sift` argument.

    Does NOT clip at 0 (return negative if infeasible regime).
    """
    ell = bb84_finite_key_length_analytic(n=n, m=m, e_x=e_x, **kwargs)
    return ell / (n + m)


def bb84_finite_key_rate_per_signal(
    n: int,
    m: int,
    e_x: float,
    p_sift: float = 0.5,
    **kwargs,
) -> float:
    """Per-transmitted-signal BB84 finite-key rate R = p_sift · ℓ / (n + m).

    For standard BB84 with unbiased basis choice: p_sift = 0.5.
    For Efficient BB84 (Lo-Chau-Ardehali 2005) with p_z bias:
        p_sift = p_z² + (1-p_z)²  (approaches 1 as bias increases)

    Matches the repo-wide "bit/signal" convention (shor_preskill_rate,
    mdi_ideal_symmetric_rate, etc.).

    Args:
        n, m, e_x: same as bb84_finite_key_length_analytic
        p_sift: sifting probability (∈ (0, 1])

    Raises:
        ValueError: p_sift not in (0, 1].
    """
    if not (0.0 < p_sift <= 1.0):
        raise ValueError(f"p_sift must be in (0, 1], got {p_sift}")
    return p_sift * bb84_finite_key_rate_per_block(
        n=n, m=m, e_x=e_x, **kwargs,
    )


# Legacy alias for backward compat (flagged as deprecated).  Use
# `bb84_finite_key_rate_per_block` or `bb84_finite_key_rate_per_signal` instead.
bb84_finite_key_rate_analytic = bb84_finite_key_rate_per_block


def total_security_parameter(
    eps_PE: float, eps_bar: float, eps_EC: float, eps_PA: float,
) -> float:
    """Total ε for composable security: ε = ε_PE + ε̄ + ε_EC + ε_PA."""
    return eps_PE + eps_bar + eps_EC + eps_PA
