"""Standard fibre channel + detector model for QKD decoy-state analysis.

Reference: Ma, Qi, Zhao, Lo (2005). Practical decoy state for QKD.
PRA 72:012326, §III (their Eq. 15-19).

Model assumptions:
    * Single-mode fibre with wavelength-dependent attenuation α [dB/km].
    * Passive Bob with photon-number-resolving detector (effective OR of
      two threshold detectors; independent dark counts).
    * Bit-flip misalignment e_d (independent of photon number).
    * Dark count rate p_dc per pulse (per detector in Ma-convention;
      Y_0 = 2·p_dc - p_dc² ≈ 2·p_dc to first order).
    * Ignores after-pulsing and dead-time effects (not in M3 scope).
"""
from __future__ import annotations

import math
from dataclasses import dataclass


DEFAULT_ALPHA_DB_PER_KM = 0.21  # Lo-Ma-Chen 2005 Fig.3 convention


@dataclass(frozen=True)
class FibreChannel:
    """Fibre channel + Bob-detector parameters.

    Defaults reproduce Lo-Ma-Chen 2005 Fig.3.  All probabilities are per
    transmitted pulse / per detection event.
    """
    eta_detector: float = 0.145           # Bob's detector efficiency
    p_dark: float = 8.5e-7                # dark count per pulse per detector
    e_misalignment: float = 0.033         # intrinsic optical misalignment
    alpha_db_per_km: float = DEFAULT_ALPHA_DB_PER_KM
    f_ec: float = 1.22                    # error-correction efficiency
    e_zero_photon: float = 0.5            # QBER on vacuum detection
    length_km: float = 0.0                # fibre length

    def __post_init__(self) -> None:
        for name, val in [
            ("eta_detector", self.eta_detector),
            ("p_dark", self.p_dark),
            ("e_misalignment", self.e_misalignment),
        ]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"{name} must be in [0,1], got {val}")
        if self.alpha_db_per_km < 0:
            raise ValueError(f"alpha_db_per_km must be ≥ 0, got {self.alpha_db_per_km}")
        if self.length_km < 0:
            raise ValueError(f"length_km must be ≥ 0, got {self.length_km}")
        if self.f_ec < 1.0:
            raise ValueError(f"f_ec must be ≥ 1.0, got {self.f_ec}")

    # -- channel transmissivities --------------------------------------

    def line_transmissivity(self) -> float:
        """η_l = 10^(-α L / 10)."""
        return 10.0 ** (-self.alpha_db_per_km * self.length_km / 10.0)

    def total_transmissivity(self) -> float:
        """η = η_d · η_l (detection-conditional transmission per photon)."""
        return self.eta_detector * self.line_transmissivity()

    # -- n-photon yields and QBERs (Ma 2005 Eq. 16-17) -----------------

    def Y_n(self, n: int) -> float:
        """Yield of n-photon signals: 1 - (1-Y_0)(1-η)^n.

        For n=0: Y_0 = 2·p_dc - p_dc² ≈ 2·p_dc (Ma 2005 below Eq. 15).
        """
        if n < 0:
            raise ValueError("n must be ≥ 0")
        Y0 = self.Y_0()
        eta = self.total_transmissivity()
        return 1.0 - (1.0 - Y0) * (1.0 - eta) ** n

    def Y_0(self) -> float:
        """Vacuum yield = dark count rate (OR of two detectors)."""
        # Y_0 = 1 - (1-p_dc)^2 ≈ 2·p_dc for small p_dc
        return 1.0 - (1.0 - self.p_dark) ** 2

    def e_n(self, n: int) -> float:
        """QBER for n-photon signal (Ma 2005 Eq. 17).

            e_n = [e_0 · Y_0 + e_d · (1 - (1-η)^n)] / Y_n
        """
        if n < 0:
            raise ValueError("n must be ≥ 0")
        if n == 0:
            return self.e_zero_photon
        Y_n = self.Y_n(n)
        if Y_n < 1e-15:
            return self.e_zero_photon
        eta = self.total_transmissivity()
        num = (self.e_zero_photon * self.Y_0()
               + self.e_misalignment * (1.0 - (1.0 - eta) ** n))
        return num / Y_n

    # -- observable gains Q_μ and QBER E_μ at intensity μ ---------------

    def Q_mu(self, mu: float, max_n: int = 50) -> float:
        """Overall gain at intensity μ: Q_μ = Σ p(n;μ) Y_n.

        Analytic closed form:
            Q_μ = 1 - (1-Y_0)·e^(-η·μ) ·  (Taylor-sum 1 term for Y_n formula)

        Actually Q_μ = Σ_n (μ^n e^-μ / n!) · [1 - (1-Y_0)(1-η)^n]
                     = Σ_n p(n;μ) - (1-Y_0) Σ_n p(n;μ) (1-η)^n
                     = 1 - (1-Y_0) · e^(-μη)
        """
        if mu < 0:
            raise ValueError("mu must be ≥ 0")
        Y0 = self.Y_0()
        eta = self.total_transmissivity()
        return 1.0 - (1.0 - Y0) * math.exp(-eta * mu)

    def E_mu_times_Q_mu(self, mu: float) -> float:
        """E_μ · Q_μ = Σ p(n;μ) Y_n e_n = e_0 Y_0 + e_d (1 - e^(-η μ)).

        Analytic closed form (Ma 2005 Eq. 19).
        """
        if mu < 0:
            raise ValueError("mu must be ≥ 0")
        eta = self.total_transmissivity()
        return (self.e_zero_photon * self.Y_0()
                + self.e_misalignment * (1.0 - math.exp(-eta * mu)))

    def E_mu(self, mu: float) -> float:
        """Observed QBER at intensity μ = (E_μ Q_μ) / Q_μ."""
        Q = self.Q_mu(mu)
        if Q < 1e-15:
            return self.e_zero_photon
        return self.E_mu_times_Q_mu(mu) / Q

    # -- single-photon gain (convenient for decoy formulas) ------------

    def Q_1(self, mu: float) -> float:
        """Q_1 = μ e^-μ Y_1 — gain contribution from single-photon pulses."""
        return mu * math.exp(-mu) * self.Y_n(1)
