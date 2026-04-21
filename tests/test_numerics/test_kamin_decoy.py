"""Tests for Kamin 2025 decoy-state SDP (S2.5 Stage 2 A4c).

Reference:
    - Kamin et al. 2025 §7 (decoy protocol), §7.3 Fig. 3
    - docs/literature/Kamin-2025.md §7

Scope (phase 1):
    - Poisson photon-number distribution (analytic)
    - Honest yields Y_n^{ab} for WCP + per-photon loss + misalignment
    - Kamin Eq. 79 SDP infrastructure (one-step, block-diagonal)
    - Trivial-limit consistency: at θ=0, η=1, single-intensity, recovers
      single-photon qubit BB84 at qber=0.

Future (phase 2):
    - Multi-intensity decoy optimization (full Fig. 3 reproduction)
    - WL22 beamsplitter-loss model for Fig. 3 exact match
    - Eq. 82 finite-key key length + (γ, α) optimization
"""
from __future__ import annotations

import math
import os

import numpy as np
import pytest

_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_MOSEK_LIC):
    os.environ.setdefault("MOSEKLM_LICENSE_FILE", _MOSEK_LIC)

try:
    import cvxpy as cp
    _MOSEK_AVAILABLE = "MOSEK" in cp.installed_solvers()
except Exception:
    _MOSEK_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _MOSEK_AVAILABLE, reason="MOSEK required for Kamin decoy SDP"
)


class TestPoisson:
    """Poisson PMF helpers."""

    def test_poisson_pmf_normalization(self):
        from qkdx.numerics.kamin_decoy_sdp import poisson_pmf_vec
        for mu in [0.01, 0.1, 0.5, 1.0, 2.0]:
            pmf = poisson_pmf_vec(mu, N_ph=30)
            # At N_ph=30, μ ≤ 2 gives near-complete coverage
            assert pmf.sum() == pytest.approx(1.0, abs=1e-10)

    def test_poisson_mean(self):
        """Σ n·P(n|μ) = μ (mean of Poisson)."""
        from qkdx.numerics.kamin_decoy_sdp import poisson_pmf_vec
        for mu in [0.1, 0.9, 2.0]:
            pmf = poisson_pmf_vec(mu, N_ph=30)
            mean = sum(n * pmf[n] for n in range(len(pmf)))
            assert mean == pytest.approx(mu, rel=1e-8)

    def test_poisson_tail(self):
        from qkdx.numerics.kamin_decoy_sdp import poisson_tail, poisson_pmf_vec
        mu = 0.5
        pmf_all = poisson_pmf_vec(mu, N_ph=5)
        tail = poisson_tail(mu, N_ph=5)
        assert pmf_all.sum() + tail == pytest.approx(1.0, abs=1e-10)

    def test_vacuum_pmf(self):
        from qkdx.numerics.kamin_decoy_sdp import poisson_pmf
        # At μ=0, all mass at n=0
        assert poisson_pmf(0.0, 0) == 1.0
        assert poisson_pmf(0.0, 1) == 0.0
        assert poisson_pmf(0.0, 5) == 0.0


class TestHonestYields:
    """Honest yields Y_n^{ab} for WCP + loss + misalignment."""

    def test_vacuum_no_detect(self):
        """Y_0^{a,b} = 1 at no-det, 0 elsewhere (vacuum → no clicks)."""
        from qkdx.numerics.kamin_decoy_sdp import honest_yields_wcp_per_photon
        Y = honest_yields_wcp_per_photon(
            N_ph=2, eta_det=0.5, theta_misalign=0.1, bob_gamma=0.5,
        )
        assert Y.shape == (3, 2, 5)
        # n=0: all mass at no-det (index 4)
        assert np.allclose(Y[0, :, :4], 0.0)
        assert np.allclose(Y[0, :, 4], 1.0)

    def test_single_photon_no_loss_no_misalign(self):
        """At η=1, θ=0: single-photon Y_1^{D,X-D}=γ/2 (Bob X, correct),
        Y_1^{D,Z-0}=(1-γ)/2 (Bob Z on X-state → uniform), etc."""
        from qkdx.numerics.kamin_decoy_sdp import honest_yields_wcp_per_photon
        bob_gamma = 0.5
        Y = honest_yields_wcp_per_photon(
            N_ph=1, eta_det=1.0, theta_misalign=0.0, bob_gamma=bob_gamma,
        )
        # n=1: Alice sends |D⟩ (a=0)
        # Bob X-basis: D→D w.p. 1 (no misalign)
        assert Y[1, 0, 0] == pytest.approx(bob_gamma * 1.0, abs=1e-12)  # X-D
        assert Y[1, 0, 1] == pytest.approx(bob_gamma * 0.0, abs=1e-12)  # X-A
        # Bob Z-basis on X-state: uniform 1/2 each
        assert Y[1, 0, 2] == pytest.approx((1 - bob_gamma) * 0.5, abs=1e-12)
        assert Y[1, 0, 3] == pytest.approx((1 - bob_gamma) * 0.5, abs=1e-12)
        # no-det: 0
        assert Y[1, 0, 4] == pytest.approx(0.0, abs=1e-12)

    def test_single_photon_misalign_cos2(self):
        """At η=1, θ ≠ 0: X-error prob = sin²(θ)."""
        from qkdx.numerics.kamin_decoy_sdp import honest_yields_wcp_per_photon
        theta = 0.2
        bob_gamma = 1.0  # Bob always X
        Y = honest_yields_wcp_per_photon(
            N_ph=1, eta_det=1.0, theta_misalign=theta, bob_gamma=bob_gamma,
        )
        # Alice |D⟩: p(X=D)=cos²(θ), p(X=A)=sin²(θ)
        assert Y[1, 0, 0] == pytest.approx(math.cos(theta) ** 2, abs=1e-12)
        assert Y[1, 0, 1] == pytest.approx(math.sin(theta) ** 2, abs=1e-12)

    def test_multi_photon_loss_scaling(self):
        """Y_n no-det = (1-η)^n (per-photon independent loss)."""
        from qkdx.numerics.kamin_decoy_sdp import honest_yields_wcp_per_photon
        eta = 0.3
        Y = honest_yields_wcp_per_photon(
            N_ph=5, eta_det=eta, theta_misalign=0.0, bob_gamma=0.5,
        )
        for n in range(1, 6):
            # Y_n^{a, no-det} = (1-η)^n for any a
            expected = (1.0 - eta) ** n
            assert Y[n, 0, 4] == pytest.approx(expected, abs=1e-12)
            assert Y[n, 1, 4] == pytest.approx(expected, abs=1e-12)


class TestHonestQDistribution:
    def test_q_mu_marginal(self):
        """Σ_{a,b} q^μ_{ab} ≈ p(μ|t)·(1 − P(tail))."""
        from qkdx.numerics.kamin_decoy_sdp import (
            honest_q_per_intensity, poisson_pmf_vec, poisson_tail,
        )
        mu = 0.9
        p_mu_given_t = 0.5
        N_ph = 10
        q_mu = honest_q_per_intensity(
            mu=mu, N_ph=N_ph, eta_det=0.5, theta_misalign=0.1,
            bob_gamma=0.5, p_mu_given_t=p_mu_given_t,
        )
        total = q_mu.sum()
        tail = poisson_tail(mu, N_ph)
        assert total == pytest.approx(p_mu_given_t * (1.0 - tail), rel=1e-6)


class TestDecoySDPInfrastructure:
    """Smoke tests for Kamin Eq. 79 SDP: runs, returns finite result."""

    def test_sdp_runs_trivial_case(self):
        """Single intensity (no real decoy), no loss, no misalign: SDP
        should return a finite positive single-photon privacy for small μ."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity,
        )
        mu = 0.05  # small μ so single-photon dominates
        N_ph = 3
        p_mu_given_t = 1.0
        q_mu = honest_q_per_intensity(
            mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=0.0,
            bob_gamma=0.5, p_mu_given_t=p_mu_given_t,
        )
        result = kamin_decoy_choi_sdp(
            intensities=(mu,),
            p_mu_given_t=(p_mu_given_t,),
            q_hon_per_mu={mu: q_mu},
            N_ph=N_ph,
            gamma=0.01,
        )
        assert result["status"] in ("optimal", "optimal_inaccurate")
        assert math.isfinite(result["r_cross"])
        # At θ=0 (no misalign), Y_1 should reflect perfect BB84;
        # W(ρ_{J_1}^g) > 0 since positive privacy available.
        assert result["r_cross"] > 0, (
            f"r_cross should be positive at trivial setup, got {result['r_cross']}"
        )

    def test_sdp_scales_with_p_1_mu(self):
        """r_cross ∝ p(1|μ_sig) in the objective; lower μ → higher p(1|μ)
        relative to total."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity, poisson_pmf,
        )
        N_ph = 3
        results = {}
        for mu in [0.05, 0.2, 0.5]:
            q_mu = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=0.0,
                bob_gamma=0.5, p_mu_given_t=1.0,
            )
            r = kamin_decoy_choi_sdp(
                intensities=(mu,), p_mu_given_t=(1.0,),
                q_hon_per_mu={mu: q_mu}, N_ph=N_ph, gamma=0.01,
            )
            results[mu] = r
            print(f"μ={mu}: p(1|μ)={poisson_pmf(mu, 1):.4f}, "
                  f"r_cross={r['r_cross']:.6f}")
        # r_cross = p(1|μ)·(1-γ)²·W(ρ_{J_1}^g); W is μ-independent-ish
        # at θ=0, η=1.  Roughly r_cross scales with p(1|μ) = μ·e^{-μ}.
        for mu in [0.05, 0.2, 0.5]:
            p1 = poisson_pmf(mu, 1)
            W_est = results[mu]["r_cross"] / (p1 * (1 - 0.01) ** 2)
            # W should be ≈ 1 bit per sift (BB84 perfect)
            assert 0.5 < W_est < 1.1, (
                f"At μ={mu}: W estimate {W_est:.4f} outside [0.5, 1.1]"
            )


class TestDecoyMultiIntensity:
    """Multi-intensity decoy (3 intensities) — Kamin Fig.3 configuration."""

    def test_three_intensity_kamin_fig3_params(self):
        """Kamin Fig.3 parameters: μ_sig=0.9, μ_2=0.02, μ_3=0.001, N_ph=10.
        At no-loss, no-misalign: should give positive r_cross.
        """
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 10
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=0.0,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        result = kamin_decoy_choi_sdp(
            intensities=intensities,
            p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu,
            N_ph=N_ph, gamma=0.01,
        )
        assert result["status"] in ("optimal", "optimal_inaccurate")
        assert result["r_cross"] > 0

    def test_three_intensity_with_misalignment(self):
        """θ_misalign=sin⁻¹(0.1) ≈ Kamin Fig.3 model.
        At no-loss, rate should still be positive (reduced by misalign)."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity, poisson_pmf,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 10
        theta = math.asin(0.1)
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        result = kamin_decoy_choi_sdp(
            intensities=intensities,
            p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu,
            N_ph=N_ph, gamma=0.01,
        )
        assert result["status"] in ("optimal", "optimal_inaccurate")
        assert result["r_cross"] > 0, (
            f"With misalignment θ=sin⁻¹(0.1), rate should still be positive, "
            f"got {result['r_cross']}"
        )
        # Compare to no-misalignment: with qber ≈ sin²(θ) = 0.01, single-
        # photon BB84 W ≈ 1 - H(0.01) ≈ 0.92.
        # r_cross ≈ p(1|μ_sig)·(1-γ)²·0.92 ≈ 0.366·0.98·0.92 ≈ 0.33
        p1_sig = poisson_pmf(0.9, 1)
        expected_W = 1.0 - (
            -0.01 * math.log2(0.01) - 0.99 * math.log2(0.99)
        )
        expected_r = p1_sig * (1 - 0.01) ** 2 * expected_W
        # With finite N_ph and multi-intensity tightening, expect within 30%
        ratio = result["r_cross"] / expected_r
        assert 0.7 < ratio < 1.3, (
            f"r_cross = {result['r_cross']:.4f} vs expected {expected_r:.4f} "
            f"(ratio {ratio:.3f})"
        )

    def test_decoy_loss_dependence(self):
        """Sweep losses, verify PER-ROUND rate decreases monotonically.

        Note on SDP output vs per-round rate:
            SDP returns r_cross = p(1|μ_sig)·(1-γ)²·W_conditional(J_1) where
            W is evaluated CONDITIONAL on single-photon detection.  That
            quantity is η-INVARIANT in the honest regime (detected ratios
            don't depend on total detection prob).  The PER-ROUND rate is
            obtained by multiplying by η_1:
                R_per_round = η_1 · r_cross_sdp

        This test checks the per-round rate monotonically decreases as loss
        increases, matching Kamin Fig. 3 shape.
        """
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 10
        theta = math.asin(0.1)
        rates_per_round = {}
        for loss_dB in [0.0, 3.0, 10.0, 20.0]:
            eta = 10 ** (-loss_dB / 10.0)
            q_per_mu = {}
            for mu, p in zip(intensities, p_mu_given_t):
                q_per_mu[mu] = honest_q_per_intensity(
                    mu=mu, N_ph=N_ph, eta_det=eta, theta_misalign=theta,
                    bob_gamma=0.5, p_mu_given_t=p,
                )
            r = kamin_decoy_choi_sdp(
                intensities=intensities,
                p_mu_given_t=p_mu_given_t,
                q_hon_per_mu=q_per_mu,
                N_ph=N_ph, gamma=0.01,
                eta_1_calib=eta,
            )
            rate_per_round = eta * r["r_cross"]
            rates_per_round[loss_dB] = rate_per_round
            print(f"loss={loss_dB} dB: η={eta:.4f}, r_cross={r['r_cross']:.4f}, "
                  f"rate_per_round={rate_per_round:.4e}")
        # Monotone: loss ↑ → rate ↓
        losses = sorted(rates_per_round.keys())
        for i in range(len(losses) - 1):
            assert rates_per_round[losses[i + 1]] < rates_per_round[losses[i]], (
                f"Non-monotone: {rates_per_round}"
            )

    def test_dual_extraction_returned(self):
        """SDP returns g_star tensor (|intensities|, 2, 5) with finite values."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 5
        theta = math.asin(0.1)
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_choi_sdp(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, gamma=0.01, eta_1_calib=1.0,
        )
        assert "g_star" in r
        assert r["g_star"].shape == (len(intensities), 2, 5)
        assert np.all(np.isfinite(r["g_star"]))


class TestDecoyFiniteKey:
    """Kamin Eq. 82 finite-key formula for decoy."""

    def test_finite_key_positive_at_large_n_optimized(self):
        """At n=10^12, 0 dB, (γ, α) optimized rate > 0 and near asymptotic."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_full_key_length_optimized, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 5
        theta = math.asin(0.1)
        eta = 1.0
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=eta, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_full_key_length_optimized(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, n=10**12, loss_dB=0.0,
            theta_misalign=theta,
        )
        print(f"Optimized: ell={r['ell_star']:.4e}, rate={r['rate_star']:.4f}, "
              f"γ*={r['gamma_star']}, α*={r['alpha_star']:.10f}")
        assert r["ell_star"] > 0
        # At large n, rate should be in [0.15, 0.45] (finite-size penalty
        # from 30-cell decoy V² is larger than qubit)
        assert 0.15 < r["rate_star"] < 0.45, (
            f"Rate at n=10^12 0 dB optimized expected 0.15-0.45, got "
            f"{r['rate_star']:.4f}"
        )

    def test_finite_key_negative_at_small_n(self):
        """At n=100, finite-size penalty dominates → ℓ < 0."""
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_full_key_length, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 5
        theta = math.asin(0.1)
        eta = 1.0
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=eta, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_full_key_length(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, n=100, loss_dB=0.0,
            theta_misalign=theta, gamma=0.01, alpha=1.1,
        )
        assert r["ell"] < 0

    def test_thm4_closes_loss_finite_key_gap(self):
        """Kamin Thm 4 τ-slack SDP gives POSITIVE rate at 10 dB n=10^12.

        Hard-constraint mode (kamin_decoy_full_key_length) gives −∞ at
        loss > 5 dB due to large g inflating V².  Thm 4 (τ-slack absorbs
        slack into s(Στ/2) penalty) trades off V² internally → positive.
        """
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_thm4_key_length_optimized, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1/3, 1/3, 1/3)
        N_ph = 5
        theta = math.asin(0.1)
        eta = 0.1  # 10 dB
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=eta, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_thm4_key_length_optimized(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, n=10**12, loss_dB=10.0,
            theta_misalign=theta,
        )
        print(f"Thm 4 n=10^12 10dB: rate={r['rate_star']:.5f}, γ*={r['gamma_star']:.3f}")
        assert r["rate_star"] > 0, (
            f"Thm 4 should give positive rate at 10 dB n=10^12, got {r['rate_star']}"
        )
        # Kamin Fig. 3 GEAT at 10 dB n=10^12 ≈ 0.03.  Our model gives ~0.01
        # (factor ~3 lower).  Attributable to per-photon vs WL22 beamsplitter
        # honest model.  Test loose range allowing that.
        assert 0.003 < r["rate_star"] < 0.1, (
            f"rate {r['rate_star']:.4f} outside [0.003, 0.1] "
            f"(Kamin Fig.3 GEAT ~0.03, my ~3x lower due to per-photon model)"
        )

    def test_fig3_anchor_0dB_optimized(self):
        """Kamin Fig.3 GEAT finite-n at n=10^12 0 dB.

        At n=10^12 0 dB, Kamin Fig.3 GEAT rate ≈ 0.3.  My rate from
        Eq. 82 formula with 2-DoF g should be in [0.15, 0.45].

        Note (documented gap): at loss > 0, the 2-DoF dual g_star has large
        magnitude (|g| ~ 10³-10⁴) because per-cell constraint sensitivity
        scales as 1/η.  This inflates V² via Eq. 38 and the finite-key
        formula goes negative.  Closing this gap requires implementing
        Kamin Thm 4 Legendre-Fenchel g*-optimization (Eq. 46-55) — same
        underlying need as for qubit Fig.1 n=10^12 residual cutoff.
        """
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_full_key_length_optimized, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 5
        theta = math.asin(0.1)
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_full_key_length_optimized(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, n=10**12, loss_dB=0.0,
            theta_misalign=theta,
        )
        print(f"n=10^12 0 dB optimized: rate={r['rate_star']:.4f}, "
              f"γ*={r['gamma_star']}, α*-1={r['alpha_star']-1:.2e}")
        assert 0.15 < r["rate_star"] < 0.45, (
            f"n=10^12 0 dB rate {r['rate_star']:.4f} outside [0.15, 0.45] "
            f"(Kamin Fig.3 anchor ≈ 0.3)"
        )

    def test_decoy_asymptotic_matches_kamin_fig3_0dB(self):
        """Kamin Fig.3 at 0 dB, asymptotic: rate ≈ 0.35 (visible from plot).

        Asymptotic (n=10^12 GEAT) at 0 dB:
            Kamin Fig. 3 shows rate ≈ 0.3–0.4.
        My per-round rate = η_1·p(1|μ_sig)·(1-γ)²·W_conditional.
            At η=1, μ_sig=0.9, θ=sin⁻¹(0.1), γ=0.01:
                p(1|μ_sig) = 0.9·e^{-0.9} ≈ 0.366
                (1-γ)² ≈ 0.98
                W_conditional ≈ 1 - H(0.01) ≈ 0.919
                expected rate ≈ 1·0.366·0.98·0.919 ≈ 0.330
        """
        from qkdx.numerics.kamin_decoy_sdp import (
            kamin_decoy_choi_sdp, honest_q_per_intensity,
        )
        intensities = (0.9, 0.02, 0.001)
        p_mu_given_t = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
        N_ph = 10
        theta = math.asin(0.1)
        q_per_mu = {}
        for mu, p in zip(intensities, p_mu_given_t):
            q_per_mu[mu] = honest_q_per_intensity(
                mu=mu, N_ph=N_ph, eta_det=1.0, theta_misalign=theta,
                bob_gamma=0.5, p_mu_given_t=p,
            )
        r = kamin_decoy_choi_sdp(
            intensities=intensities, p_mu_given_t=p_mu_given_t,
            q_hon_per_mu=q_per_mu, N_ph=N_ph, gamma=0.01,
            eta_1_calib=1.0,
        )
        rate = r["r_cross"]  # η=1 so per-round rate = r_cross
        # Kamin Fig.3 at 0 dB asymptotic ≈ 0.3; allow ±40% for honest-model
        # simplification (per-photon loss vs WL22 beamsplitter)
        assert 0.2 < rate < 0.5, (
            f"Expected 0.2 < rate < 0.5 at 0 dB asymptotic, got {rate:.4f}"
        )
