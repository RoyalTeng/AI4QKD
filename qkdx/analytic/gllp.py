"""GLLP single-photon asymptotic key rate.

Reference:
- Gottesman, Lo, Lütkenhaus, Preskill 2004. Security of QKD with imperfect
  devices. Quant. Info. Comput. 4:325.
- Lo, Ma, Chen 2005. Decoy State QKD. PRL 94:230504. Eq. (16)-(17).
- Ma, Razavi 2012. PRA 86:062319. Eq. (9)-(10) (MDI-QKD specialisation).

GLLP single-photon asymptotic rate (bit/signal):
    R = p_sift · [1 - H(e_X) - f_ec · H(e_Z)]

where:
    p_sift: sifting probability (0.5 for BB84, 0.25 for ideal MDI, 1/3 for six-state)
    e_X:    QBER in the X (phase-error) basis — used for privacy amplification
    e_Z:    QBER in the Z (bit-error) basis — used for error correction
    f_ec:   error correction efficiency (1.0 = ideal, 1.16 = typical Cascade)
    H:      binary entropy

Special cases:
- Symmetric BB84 (e_X = e_Z = e): R = p_sift · (1 - (1+f_ec)·h(e))
- Symmetric MDI ideal lossless, single-photon, e_X = e_Z = e: same form with p_sift=1/4
"""
from __future__ import annotations

from qkdx.core.entropy import binary_entropy


def gllp_rate(
    p_sift: float,
    qber_Z: float,
    qber_X: float,
    f_ec: float = 1.16,
) -> float:
    """GLLP asymptotic key rate for a single-photon source.

    Args:
        p_sift: sifting probability (survive-rate after basis match + success).
        qber_Z: bit-error rate in Z (key) basis, used by error correction.
        qber_X: phase-error rate in X basis, used by privacy amplification.
        f_ec: error-correction efficiency (typically 1.0 ideal or 1.16 Cascade).

    Returns:
        R in bit/signal. NOT clipped at zero — negative values indicate
        the observed QBER is above threshold.
    """
    if not (0.0 <= p_sift <= 1.0):
        raise ValueError(f"p_sift must be in [0,1], got {p_sift}")
    for name, q in [("qber_Z", qber_Z), ("qber_X", qber_X)]:
        if not (0.0 <= q <= 1.0):
            raise ValueError(f"{name} must be in [0,1], got {q}")

    h_Z = binary_entropy(qber_Z)
    h_X = binary_entropy(qber_X)
    return p_sift * (1.0 - h_X - f_ec * h_Z)


def mdi_ideal_symmetric_rate(qber: float, f_ec: float = 1.16) -> float:
    """Ideal symmetric MDI-QKD asymptotic rate under single-photon assumption.

    Setup: no channel loss (η_A = η_B = 1), symmetric Z/X bases, single-photon
    source. Effective Alice-Bob QBER = qber in both Z and X bases after
    accounting for Charlie's Bell measurement bit-flip correction.

    Sifting: p_sift = 1/4 (basis match 1/2 × Charlie success 1/2).

    Formula:
        R = (1/4) · [1 - (1 + f_ec) · h(qber)]

    This is exactly BB84's per-sift rate scaled by p_sift = 1/4.
    """
    return gllp_rate(p_sift=0.25, qber_Z=qber, qber_X=qber, f_ec=f_ec)
