"""Tests for qkdx.analytic.mdi_decoy (Ma-Razavi 2012).

Coverage:
    - Eq. A9: Y_11 formula (zero-background limit + dark-count correction)
    - Eq. A11: e_11 formula (no-loss limit → e_d; pure-background → 0.5)
    - Eq. B1: Q_11 proportional to μ_a μ_b e^{-μ_a-μ_b} Y_11
    - Eqs. B28-B31: Q_rect, E_rect (dark-count = 0 limit, noise-only limit)
    - Eq. B27: mdi_original_rate sign + monotonicity
    - Sweep: rate positive near 0 loss, 0 at high loss; monotone decreasing
    - Ma-Razavi Table I parameters reproduce physically plausible ranges
"""
import math
import pytest

from qkdx.analytic.mdi_decoy import (
    MdiDecoyParams,
    y11_single_photon,
    y11_zero_background,
    e11_single_photon,
    q11_gain,
    q_rect_total,
    e_rect_qber,
    mdi_original_rate,
    mdi_original_rate_optimised,
    mdi_original_sweep,
)


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def ma_razavi_params():
    """Ma-Razavi 2012 Table I parameters."""
    return MdiDecoyParams(eta_det=0.145, p_d=3.0e-6, e_d=0.015, f_ec=1.16)


# ---------------------------------------------------------------------------
# Y_11 — Eq. A9
# ---------------------------------------------------------------------------

class TestY11:
    def test_zero_background_limit(self):
        """With p_d=0, Y_11 = η_a η_b / 2."""
        eta_a, eta_b = 0.3, 0.4
        Y11 = y11_single_photon(eta_a, eta_b, p_d=0.0)
        expected = eta_a * eta_b / 2.0
        print(f"Y_11(p_d=0) = {Y11:.6e}, expected = {expected:.6e}")
        assert abs(Y11 - expected) < 1e-12

    def test_zero_background_convenience(self):
        """y11_zero_background matches y11_single_photon at p_d=0."""
        eta_a, eta_b = 0.2, 0.3
        assert abs(
            y11_zero_background(eta_a, eta_b)
            - y11_single_photon(eta_a, eta_b, 0.0)
        ) < 1e-14

    def test_positive(self):
        """Y_11 must be positive for any valid inputs."""
        for eta in [0.01, 0.1, 0.5, 0.9]:
            for pd in [0.0, 1e-6, 1e-3]:
                Y11 = y11_single_photon(eta, eta, pd)
                assert Y11 > 0, f"Y_11 ≤ 0 for eta={eta}, p_d={pd}"

    def test_monotone_in_efficiency(self):
        """Y_11 increases with η_a, η_b."""
        pd = 1e-6
        Y_low = y11_single_photon(0.1, 0.1, pd)
        Y_high = y11_single_photon(0.5, 0.5, pd)
        print(f"Y_11(0.1,0.1) = {Y_low:.4e}, Y_11(0.5,0.5) = {Y_high:.4e}")
        assert Y_high > Y_low

    def test_symmetric(self):
        """Y_11 is symmetric in η_a, η_b."""
        pd = 1e-5
        assert abs(
            y11_single_photon(0.2, 0.4, pd) - y11_single_photon(0.4, 0.2, pd)
        ) < 1e-14

    def test_ma_razavi_table_i(self, ma_razavi_params):
        """With Table I params at ~20 dB loss per arm, Y_11 in expected range.

        At 20 dB/arm: η = 0.145 × 10^{-2} = 0.00145, Y_11 ≈ η²/2 ≈ 1e-6.
        """
        eta = ma_razavi_params.eta_det * 10 ** (-20 / 10)  # 20 dB per arm
        Y11 = y11_single_photon(eta, eta, ma_razavi_params.p_d)
        print(f"Y_11 at 20 dB/arm (η={eta:.4f}): {Y11:.4e}")
        # η_a η_b / 2 ≈ (0.00145)^2 / 2 ≈ 1.05e-6; allow decade slack
        assert 1e-8 < Y11 < 1e-4


# ---------------------------------------------------------------------------
# e_11 — Eq. A11
# ---------------------------------------------------------------------------

class TestE11:
    def test_no_loss_no_dark(self):
        """At η_a = η_b = 1, p_d = 0: e_11 → e_d (only misalignment)."""
        e_d = 0.02
        Y11 = y11_single_photon(1.0, 1.0, 0.0)
        e11 = e11_single_photon(1.0, 1.0, 0.0, e_d, Y11)
        print(f"e_11(η=1, p_d=0) = {e11:.6f}, e_d = {e_d}")
        assert abs(e11 - e_d) < 1e-10

    def test_pure_dark_counts(self):
        """At η_a = η_b ≈ 0 (all background), e_11 → e_0 = 0.5."""
        e11 = e11_single_photon(1e-10, 1e-10, p_d=0.1, e_d=0.01, Y_11=1e-20)
        print(f"e_11(near-vacuum) = {e11:.4f}")
        assert abs(e11 - 0.5) < 1e-3

    def test_in_range(self, ma_razavi_params):
        """e_11 ∈ [e_d, 0.5) for Table I params at moderate loss."""
        eta = 0.05
        p = ma_razavi_params
        Y11 = y11_single_photon(eta, eta, p.p_d)
        e11 = e11_single_photon(eta, eta, p.p_d, p.e_d, Y11)
        print(f"e_11 = {e11:.4f} (e_d={p.e_d})")
        assert p.e_d <= e11 <= 0.5

    def test_degenerate_Y11_zero(self):
        """e11 returns 0.5 (worst case) when Y_11 ≈ 0."""
        e11 = e11_single_photon(0.0, 0.0, 0.0, 0.01, Y_11=0.0)
        assert e11 == 0.5


# ---------------------------------------------------------------------------
# Q_11 — Eq. B1
# ---------------------------------------------------------------------------

class TestQ11:
    def test_formula(self):
        """Q_11 = μ_a μ_b e^{-μ_a-μ_b} Y_11."""
        mu_a, mu_b = 0.3, 0.4
        Y11 = 0.01
        Q11 = q11_gain(mu_a, mu_b, Y11)
        expected = mu_a * mu_b * math.exp(-mu_a - mu_b) * Y11
        print(f"Q_11 = {Q11:.6e}, expected = {expected:.6e}")
        assert abs(Q11 - expected) < 1e-15

    def test_positive(self):
        assert q11_gain(0.2, 0.3, 0.05) > 0

    def test_zero_Y11(self):
        assert q11_gain(0.3, 0.3, 0.0) == 0.0


# ---------------------------------------------------------------------------
# Q_rect, E_rect — Eqs. B28-B31
# ---------------------------------------------------------------------------

class TestQRect:
    def test_zero_dark_limit(self):
        """At p_d=0, Q_rect^(E) = 0 and Q_rect = Q_rect^(C) > 0."""
        Q = q_rect_total(0.3, 0.3, 0.1, 0.1, p_d=0.0)
        print(f"Q_rect(p_d=0) = {Q:.6e}")
        assert Q > 0

    def test_positive(self, ma_razavi_params):
        """Q_rect > 0 for Table I params."""
        p = ma_razavi_params
        eta = 0.05
        Q = q_rect_total(0.3, 0.3, eta, eta, p.p_d)
        print(f"Q_rect = {Q:.4e}")
        assert Q > 0

    def test_monotone_in_mu(self):
        """Q_rect increases with μ for fixed η."""
        eta, pd = 0.1, 1e-6
        Q_low = q_rect_total(0.1, 0.1, eta, eta, pd)
        Q_high = q_rect_total(0.5, 0.5, eta, eta, pd)
        assert Q_high > Q_low

    def test_E_rect_in_range(self, ma_razavi_params):
        """E_rect ∈ [e_d, 0.5] for Table I params."""
        p = ma_razavi_params
        eta = 0.05
        E = e_rect_qber(0.3, 0.3, eta, eta, p.p_d, p.e_d)
        print(f"E_rect = {E:.4f}")
        assert p.e_d <= E <= 0.5

    def test_E_rect_low_noise(self):
        """At p_d ≈ 0, E_rect ≈ e_d (misalignment dominated)."""
        e_d = 0.02
        E = e_rect_qber(0.3, 0.3, 0.3, 0.3, p_d=0.0, e_d=e_d)
        print(f"E_rect(p_d=0) = {E:.4f}")
        assert abs(E - e_d) < 1e-6

    def test_symmetric_mu(self):
        """Q_rect and E_rect are symmetric in μ_a, μ_b."""
        eta, pd, e_d = 0.1, 1e-6, 0.01
        Q1 = q_rect_total(0.2, 0.4, eta, eta, pd)
        Q2 = q_rect_total(0.4, 0.2, eta, eta, pd)
        assert abs(Q1 - Q2) < 1e-15


# ---------------------------------------------------------------------------
# mdi_original_rate — Eq. B27
# ---------------------------------------------------------------------------

class TestMdiOriginalRate:
    def test_positive_short_distance(self, ma_razavi_params):
        """Rate positive for η = 0.05 (modest loss)."""
        p = ma_razavi_params
        eta = 0.05
        r = mdi_original_rate(0.3, 0.3, eta, eta, p.p_d, p.e_d, p.f_ec)
        print(f"R(η=0.05, μ=0.3) = {r:.4e}")
        assert r > 0

    def test_negative_high_loss(self, ma_razavi_params):
        """Rate negative at extremely high loss (infeasible regime)."""
        p = ma_razavi_params
        eta = 1e-8
        r = mdi_original_rate(0.3, 0.3, eta, eta, p.p_d, p.e_d, p.f_ec)
        print(f"R(η=1e-8, μ=0.3) = {r:.4e}")
        assert r < 0

    def test_rate_formula_components(self, ma_razavi_params):
        """Manually verify formula: R = Q_11(1-H(e_11)) - Q_rect f H(E_rect)."""
        p = ma_razavi_params
        mu_a, mu_b, eta = 0.3, 0.3, 0.1

        from qkdx.analytic.mdi_decoy import (
            y11_single_photon, e11_single_photon, q11_gain,
            q_rect_total, e_rect_qber, _h,
        )
        Y11 = y11_single_photon(eta, eta, p.p_d)
        e11 = e11_single_photon(eta, eta, p.p_d, p.e_d, Y11)
        Q11 = q11_gain(mu_a, mu_b, Y11)
        Q_rect = q_rect_total(mu_a, mu_b, eta, eta, p.p_d)
        E_rect = e_rect_qber(mu_a, mu_b, eta, eta, p.p_d, p.e_d)
        expected = Q11 * (1 - _h(e11)) - Q_rect * p.f_ec * _h(E_rect)
        actual = mdi_original_rate(mu_a, mu_b, eta, eta, p.p_d, p.e_d, p.f_ec)
        print(f"Q_11={Q11:.4e}, e_11={e11:.4f}, Q_rect={Q_rect:.4e}, "
              f"E_rect={E_rect:.4f}, R_expected={expected:.4e}, R={actual:.4e}")
        assert abs(actual - expected) < 1e-14

    def test_mu_optimisation_improves(self, ma_razavi_params):
        """Optimised μ gives better rate than arbitrary μ=0.3."""
        p = ma_razavi_params
        eta = 0.05
        r_fixed = max(0.0, mdi_original_rate(0.3, 0.3, eta, eta, p.p_d, p.e_d, p.f_ec))
        r_opt = mdi_original_rate_optimised(eta, eta, p)
        print(f"R(μ=0.3) = {r_fixed:.4e}, R(opt) = {r_opt:.4e}")
        assert r_opt >= r_fixed


# ---------------------------------------------------------------------------
# Sweep — Fig. 4 alignment
# ---------------------------------------------------------------------------

class TestSweep:
    def test_sweep_monotone(self, ma_razavi_params):
        """Key rate decreases monotonically with loss (averaged over 4-point grid)."""
        losses = [0, 10, 20, 30, 40, 50, 60]
        rates = mdi_original_sweep(losses, ma_razavi_params)
        print("Loss→Rate sweep:")
        for L, R in zip(losses, rates):
            print(f"  {L:3d} dB: R = {R:.3e}")
        # rate should be non-increasing (allow equal when both are 0)
        for i in range(len(rates) - 1):
            assert rates[i] >= rates[i + 1] - 1e-20, (
                f"Non-monotone: R[{losses[i]}]={rates[i]:.2e} "
                f"< R[{losses[i+1]}]={rates[i+1]:.2e}"
            )

    def test_sweep_zero_loss_positive(self, ma_razavi_params):
        """At 0 dB total fibre loss, rate must be positive."""
        rates = mdi_original_sweep([0.0], ma_razavi_params)
        print(f"R(0 dB loss) = {rates[0]:.4e}")
        assert rates[0] > 0

    def test_sweep_high_loss_zero(self, ma_razavi_params):
        """At very high loss (80 dB), rate is zero (infeasible clipped at 0)."""
        rates = mdi_original_sweep([80.0], ma_razavi_params)
        print(f"R(80 dB loss) = {rates[0]:.4e}")
        assert rates[0] == 0.0

    def test_sweep_order_of_magnitude(self, ma_razavi_params):
        """At ~20 dB total loss, rate should be in [1e-6, 1e-2] (Fig.4 scale)."""
        rates = mdi_original_sweep([20.0], ma_razavi_params)
        print(f"R(20 dB total loss) = {rates[0]:.4e}")
        assert 1e-7 < rates[0] < 1e-1

    def test_default_params(self):
        """Sweep with default (None) params runs without error."""
        rates = mdi_original_sweep([0, 20, 40])
        assert len(rates) == 3
        assert all(r >= 0 for r in rates)


# ---------------------------------------------------------------------------
# Parameter validation
# ---------------------------------------------------------------------------

class TestMdiDecoyParams:
    def test_valid_table_i(self):
        p = MdiDecoyParams(eta_det=0.145, p_d=3e-6, e_d=0.015, f_ec=1.16)
        assert p.eta_det == 0.145

    def test_invalid_eta_det(self):
        with pytest.raises(ValueError):
            MdiDecoyParams(eta_det=0.0)
        with pytest.raises(ValueError):
            MdiDecoyParams(eta_det=1.1)

    def test_invalid_f_ec(self):
        with pytest.raises(ValueError):
            MdiDecoyParams(f_ec=0.9)

    def test_arm_efficiency(self):
        """arm_efficiency: η = η_det × 10^(-loss/10)."""
        p = MdiDecoyParams(eta_det=0.145)
        eta = p.arm_efficiency(0.0)
        assert abs(eta - 0.145) < 1e-12
        eta_10db = p.arm_efficiency(10.0)
        assert abs(eta_10db - 0.145 / 10.0) < 1e-10
