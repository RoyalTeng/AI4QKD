"""Tests for PLOB / Pirandola / TGW upper-bound numerical tools (Sub-Q3 §4.4).

Reference:
    - PLOB 2017 Eq. 19 (docs/literature/PLOB-2017.md)
    - Pirandola 2019 Eq. 9 (docs/literature/Pirandola-2019.md)
    - TGW 2014 Eq. 1 (docs/literature/TGW-2014.md)
    - Topology applicability lemma (docs/msen/topology_applicability.md)

Scope:
    - Closed-form upper bounds for distillable channels (lossy, amplifier,
      dephasing, erasure)
    - Protocol-family → bound mapping via topology (Lemma 1)
    - Gap analysis helpers (PM-QKD actual vs Pirandola N=1)
"""
from __future__ import annotations

import math

import pytest

from qkdx.numerics.e_r_upper import (
    bound_by_topology,
    bound_comparison_lossy,
    e_r_dephasing,
    e_r_erasure,
    e_r_lossy_point_to_point,
    e_r_lossy_repeater_chain,
    e_r_ql_amplifier,
    e_r_tgw_lossy,
    gap_ratio,
    topology_type_of_protocol,
)


class TestELossyPointToPoint:
    """PLOB Eq. 19: C(η) = -log_2(1 - η) for lossy channel."""

    def test_closed_form(self):
        eta = 0.5
        expected = -math.log2(1 - eta)
        assert e_r_lossy_point_to_point(eta) == pytest.approx(expected, rel=1e-12)

    def test_high_loss_approx(self):
        # η = 10^{-4}: -log_2(1-10^{-4}) ≈ 1.44×10^{-4}
        eta = 1e-4
        val = e_r_lossy_point_to_point(eta)
        assert val == pytest.approx(eta / math.log(2), rel=1e-3)

    def test_eta_zero_is_zero(self):
        assert e_r_lossy_point_to_point(0.0) == 0.0

    def test_eta_one_is_infinite(self):
        # η → 1: -log_2(0) = +∞
        assert math.isinf(e_r_lossy_point_to_point(1.0))

    def test_invalid_eta_raises(self):
        with pytest.raises(ValueError):
            e_r_lossy_point_to_point(-0.1)
        with pytest.raises(ValueError):
            e_r_lossy_point_to_point(1.5)


class TestELossyRepeaterChain:
    """Pirandola 2019 Eq. 9: C_loss(η, N) = -log_2(1 - η^{1/(N+1)})."""

    def test_N_zero_equals_plob(self):
        # N=0 no repeater → PLOB direct-link
        eta = 0.01
        assert e_r_lossy_repeater_chain(eta_total=eta, N_repeaters=0) == pytest.approx(
            e_r_lossy_point_to_point(eta), rel=1e-12
        )

    def test_N_one_tfqkd_bound(self):
        # N=1: TF-QKD bound -log_2(1 - √η)
        eta = 1e-4
        val = e_r_lossy_repeater_chain(eta_total=eta, N_repeaters=1)
        expected = -math.log2(1 - math.sqrt(eta))
        assert val == pytest.approx(expected, rel=1e-12)

    def test_chain_monotone_in_N(self):
        # More repeaters → higher rate (tighter bound for chains)
        eta = 1e-6
        c_0 = e_r_lossy_repeater_chain(eta, N_repeaters=0)
        c_1 = e_r_lossy_repeater_chain(eta, N_repeaters=1)
        c_10 = e_r_lossy_repeater_chain(eta, N_repeaters=10)
        assert c_0 < c_1 < c_10

    def test_ma_fig3a_100km_pirandola_n1(self):
        # 100 km total = 20 dB → η = 10^-2, √η = 0.1
        # -log_2(1-0.1) = log_2(1/0.9) ≈ 0.152 bit/use
        eta = 1e-2
        val = e_r_lossy_repeater_chain(eta, N_repeaters=1)
        assert val == pytest.approx(0.152, rel=1e-2)

    def test_invalid_N_raises(self):
        with pytest.raises(ValueError):
            e_r_lossy_repeater_chain(eta_total=0.1, N_repeaters=-1)


class TestELossyTGW:
    """TGW 2014 Eq. 1: P_2(N_η) ≤ log_2[(1+η)/(1-η)]."""

    def test_closed_form(self):
        eta = 0.5
        expected = math.log2((1 + eta) / (1 - eta))
        assert e_r_tgw_lossy(eta) == pytest.approx(expected, rel=1e-12)

    def test_looser_than_plob(self):
        # TGW bound is 2× looser than PLOB at η ≪ 1
        for eta in [1e-3, 1e-2, 1e-1, 0.5]:
            plob = e_r_lossy_point_to_point(eta)
            tgw = e_r_tgw_lossy(eta)
            assert tgw > plob, f"At η={eta}: TGW {tgw:.4e} should exceed PLOB {plob:.4e}"

    def test_high_loss_approx_2_88_eta(self):
        # TGW at η ≪ 1: ≈ 2η/ln 2 ≈ 2.88η
        eta = 1e-4
        val = e_r_tgw_lossy(eta)
        assert val == pytest.approx(2 * eta / math.log(2), rel=1e-3)


class TestEQLAmplifier:
    """PLOB Eq. 28: C(g) = -log_2(1 - 1/g) for QL amplifier with gain g."""

    def test_gain_two(self):
        g = 2.0
        expected = -math.log2(1 - 1.0 / g)
        assert e_r_ql_amplifier(g) == pytest.approx(expected, rel=1e-12)

    def test_large_gain_approaches_zero(self):
        # g → ∞: -log_2(1 - 1/g) → 0
        val = e_r_ql_amplifier(1e6)
        assert val < 0.01

    def test_gain_one_infinite(self):
        # g = 1 (no amplification): -log_2(0) = +∞
        assert math.isinf(e_r_ql_amplifier(1.0))

    def test_gain_below_one_raises(self):
        with pytest.raises(ValueError):
            e_r_ql_amplifier(0.5)


class TestEDephasing:
    """PLOB Eq. 39: C = 1 - H_2(p) for dephasing prob p ∈ [0, 0.5]."""

    def test_zero_dephasing_one_bit(self):
        # p=0: no dephasing → perfect qubit
        assert e_r_dephasing(0.0) == pytest.approx(1.0, rel=1e-12)

    def test_half_dephasing_zero(self):
        # p=0.5: max dephasing → no key
        assert e_r_dephasing(0.5) == pytest.approx(0.0, abs=1e-12)

    def test_p_above_half_same_as_reflected(self):
        # p > 0.5: C = 1 - H_2(p) = 1 - H_2(1-p) (symmetric)
        for p in [0.3, 0.4]:
            c_low = e_r_dephasing(p)
            c_high = e_r_dephasing(1.0 - p)
            assert c_low == pytest.approx(c_high, rel=1e-12)


class TestEErasure:
    """PLOB Eq. 43: C = 1 - p for erasure prob p ∈ [0, 1]."""

    def test_no_erasure_one_bit(self):
        assert e_r_erasure(0.0) == pytest.approx(1.0, rel=1e-12)

    def test_full_erasure_zero(self):
        assert e_r_erasure(1.0) == pytest.approx(0.0, rel=1e-12)

    def test_linear_interpolation(self):
        assert e_r_erasure(0.3) == pytest.approx(0.7, rel=1e-12)


class TestTopologyTypeOfProtocol:
    """Topology applicability Lemma 1: protocol family → Type A / B."""

    def test_bb84_is_type_a(self):
        assert topology_type_of_protocol("BB84") == "A"
        assert topology_type_of_protocol("bb84") == "A"  # case insensitive

    def test_mdi_is_type_b(self):
        assert topology_type_of_protocol("MDI") == "B"
        assert topology_type_of_protocol("MDI-QKD") == "B"

    def test_tf_family_is_type_b(self):
        for name in ["TF-QKD", "SNS-TF", "PM-QKD", "PM", "SNS"]:
            assert topology_type_of_protocol(name) == "B", f"{name} should be Type B"

    def test_six_state_is_type_a(self):
        assert topology_type_of_protocol("six-state") == "A"

    def test_unknown_protocol_raises(self):
        with pytest.raises(ValueError):
            topology_type_of_protocol("unknown-protocol")


class TestBoundByTopology:
    """Apply correct upper bound based on protocol type."""

    def test_bb84_uses_plob(self):
        eta = 1e-2
        b = bound_by_topology("BB84", eta_channel=eta)
        assert b == pytest.approx(e_r_lossy_point_to_point(eta), rel=1e-12)

    def test_tfqkd_uses_pirandola_n1(self):
        eta = 1e-2
        b = bound_by_topology("TF-QKD", eta_channel=eta)
        assert b == pytest.approx(
            e_r_lossy_repeater_chain(eta, N_repeaters=1), rel=1e-12
        )

    def test_pm_qkd_uses_pirandola_n1(self):
        eta = 1e-4
        b = bound_by_topology("PM-QKD", eta_channel=eta)
        assert b == pytest.approx(
            -math.log2(1 - math.sqrt(eta)), rel=1e-12
        )

    def test_mdi_uses_pirandola_n1(self):
        # MDI Type B → Pirandola N=1 bound applies (as upper bound, even though
        # MDI achieves η rather than √η scaling, the bound is -log_2(1-√η))
        eta = 1e-2
        b = bound_by_topology("MDI", eta_channel=eta)
        assert b == pytest.approx(-math.log2(1 - math.sqrt(eta)), rel=1e-12)


class TestBoundComparisonLossy:
    """Compare PLOB, Pirandola N=1, TGW at same η for sanity."""

    def test_comparison_dict(self):
        eta = 1e-2
        d = bound_comparison_lossy(eta)
        assert "plob_direct" in d
        assert "pirandola_n1" in d
        assert "tgw" in d
        # Ordering: TGW > PLOB (TGW looser); Pirandola N=1 > PLOB (different topology)
        assert d["tgw"] > d["plob_direct"]
        assert d["pirandola_n1"] > d["plob_direct"]


class TestGapRatio:
    """PM-QKD actual rate vs Pirandola N=1 upper bound."""

    def test_gap_positive_when_bound_gt_actual(self):
        # Pirandola N=1 at η=0.01 is ~0.152; any actual rate < that
        ratio = gap_ratio(actual_rate=1e-3, upper_bound=0.152)
        assert 150 < ratio < 153

    def test_gap_inf_when_actual_zero(self):
        assert math.isinf(gap_ratio(actual_rate=0.0, upper_bound=0.152))

    def test_gap_invalid_negative_raises(self):
        with pytest.raises(ValueError):
            gap_ratio(actual_rate=-0.1, upper_bound=0.152)
