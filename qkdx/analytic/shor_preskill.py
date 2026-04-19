"""Shor-Preskill asymptotic key rate for BB84."""
from __future__ import annotations

from qkdx.core.entropy import binary_entropy


def shor_preskill_rate(qber: float, f_ec: float = 1.16) -> float:
    """Asymptotic key rate R = p_sift * (1 - f_ec*h(e) - h(e)) [bit/signal].

    Uses the symmetric depolarising model: qber_Z = qber_X = e.

    Under the Shor-Preskill reduction (Bennett et al. 1996 + Lo-Chau 1999),
    for a symmetric depolarising channel with QBER e:

        R = p_sift · [1 - h(e) - f_ec · h(e)]   [bit/signal]

    where p_sift = 0.5 for BB84 (Z-basis sifting, perfect detectors).

    This equals the WLC SDP lower bound under the symmetric state assumption:
        R = p_sift · D(𝒢(ρ) ‖ 𝒵(𝒢(ρ))) - p_sift · f_ec · h(e)

    At f_ec=1 (ideal EC): R = p_sift * (1 - 2*h(e)).
    The standard f_ec=1.16 (Cascade efficiency) shifts the threshold slightly.
    """
    if qber < 0.0 or qber > 1.0:
        raise ValueError(f"QBER must be in [0,1], got {qber}")
    p_sift = 0.5
    h_e = binary_entropy(qber)
    r_per_sift = 1.0 - h_e - f_ec * h_e  # = 1 - (1+f_ec)*h(e)
    # No max(0) clip: return raw value for fair comparison with WLC (which also doesn't clip).
    # Negative values indicate QBER above threshold (no key can be generated).
    return p_sift * r_per_sift
