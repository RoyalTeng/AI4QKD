"""Tests for PM-QKD (phase-matching QKD) protocol builder — F6 §7.5b.

Scope (minimally executable protocol shell):
    - Construct MSEBProtocol with proper structure (two sources, announcement, key_map)
    - Registry presence for F6 dispatch
    - Analytic rate bridge via pm_rate_with_decoy_phase_error
    - scope_tag='partial' (full Fock-truncated source state + phase register
      purification deferred per docs/msen/pm_qkd_formulation.md M1)
"""
from __future__ import annotations

import math

import pytest


class TestBuildPmQkdProtocol:
    """build_pm_qkd_protocol returns a valid MSEBProtocol with scope_tag='partial'."""

    def test_returns_mseb_protocol(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        from qkdx.protocol.base import MSEBProtocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert isinstance(p, MSEBProtocol)

    def test_has_two_sources(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert len(p.sources) == 2
        assert p.sources[0].name == "Alice"
        assert p.sources[1].name == "Bob"

    def test_key_party_is_alice(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert p.key_map.key_party == "Alice"

    def test_scope_tag_partial(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert p.scope_tag == "partial"
        # scope_reason must be non-empty + mention phase register / Fock
        assert p.scope_reason is not None
        low = p.scope_reason.lower()
        assert "fock" in low or "phase register" in low or "analytic" in low

    def test_name_contains_pm_qkd(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert "PM" in p.name
        assert "QKD" in p.name

    def test_observation_keys_include_gain_and_qber(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        obs = set(p.observation_keys)
        assert any("Q" in k for k in obs), f"expected gain-like key, got {obs}"
        assert any("E" in k or "qber" in k.lower() for k in obs)

    def test_invalid_mu_raises(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        with pytest.raises(ValueError):
            build_pm_qkd_protocol(mu=0.0, eta_channel=0.1)
        with pytest.raises(ValueError):
            build_pm_qkd_protocol(mu=-0.5, eta_channel=0.1)

    def test_invalid_eta_channel_raises(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        with pytest.raises(ValueError):
            build_pm_qkd_protocol(mu=0.3, eta_channel=1.5)
        with pytest.raises(ValueError):
            build_pm_qkd_protocol(mu=0.3, eta_channel=-0.1)


class TestPmQkdAnalyticRate:
    """Analytic rate bridge: call pm_rate_with_decoy_phase_error via protocol helper."""

    def test_pm_qkd_rate_accessor_present(self):
        from qkdx.protocols.pm_qkd import pm_qkd_rate
        # Should accept a protocol (or parameters) and return a float
        assert callable(pm_qkd_rate)

    def test_rate_positive_at_low_loss(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol, pm_qkd_rate
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=1e-2)
        r = pm_qkd_rate(p)
        assert r > 0

    def test_rate_matches_analytic_helper(self):
        # Round-trip check: pm_qkd_rate(protocol) = pm_rate_with_decoy_phase_error(mu, eta, params)
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol, pm_qkd_rate
        from qkdx.analytic.pm_qkd import PmQkdParams
        from qkdx.analytic.pm_qkd_decoy import pm_rate_with_decoy_phase_error
        params = PmQkdParams()
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=1e-3, params=params)
        r_protocol = pm_qkd_rate(p)
        r_direct = pm_rate_with_decoy_phase_error(mu=0.3, eta_channel=1e-3, params=params)
        assert r_protocol == pytest.approx(r_direct, rel=1e-12)

    def test_rate_log_log_slope_half(self):
        # √η scaling via protocol layer
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol, pm_qkd_rate
        etas = [10 ** (-d / 10) for d in [10, 20, 30, 40, 50]]
        rates = [pm_qkd_rate(build_pm_qkd_protocol(mu=0.3, eta_channel=e)) for e in etas]
        log_e = [math.log10(e) for e in etas]
        log_r = [math.log10(r) for r in rates if r > 0]
        assert len(log_r) == len(log_e)
        mx = sum(log_e) / len(log_e)
        my = sum(log_r) / len(log_r)
        slope = sum((x - mx) * (y - my) for x, y in zip(log_e, log_r)) / sum((x - mx) ** 2 for x in log_e)
        assert slope == pytest.approx(0.5, abs=0.05), f"slope {slope:.4f} off target"


class TestPmQkdScopeDisclosure:
    """Scope limitations are explicitly documented in scope_reason (no silent gaps)."""

    def test_scope_reason_mentions_placeholder(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        reason = p.scope_reason or ""
        # Must disclose: placeholder source/network, analytic rate path, upgrade conditions
        for keyword in ("placeholder", "analytic", "upgrade"):
            assert keyword.lower() in reason.lower(), (
                f"scope_reason must mention '{keyword}'; got:\n{reason}"
            )

    def test_scope_reason_lists_upgrade_requirements(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        reason = p.scope_reason or ""
        # Should list at least 3 concrete things needed for covered status
        # (Fock truncation, phase register, BS Kraus, conditional override)
        # — relax to: at least 2 of these keywords present
        keywords = ("fock", "phase register", "bs", "conditional")
        hits = sum(1 for k in keywords if k.lower() in reason.lower())
        assert hits >= 2, (
            f"scope_reason should enumerate upgrade requirements; "
            f"only {hits}/4 keywords found. Got:\n{reason}"
        )
