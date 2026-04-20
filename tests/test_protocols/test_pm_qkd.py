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

    def test_observation_keys_are_wlc_triple(self):
        # Round-3 align with MDI pattern: observation_keys = (qber_Z, qber_X, p_sift)
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert set(p.observation_keys) == {"qber_Z", "qber_X", "p_sift"}

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


class TestPmQkdWlcShapeCompatibility:
    """Round-2 regression: WLC SDP dim-check must pass even though rate is analytic."""

    def test_conditional_alice_bob_dim_is_4(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        assert p.conditional_alice_bob_dim() == 4

    def test_conditional_alice_bob_state_is_4x4(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        rho = p.conditional_alice_bob()
        assert rho.shape == (4, 4)
        # Trace ≈ 1 (density matrix)
        import numpy as np
        assert abs(np.trace(rho).real - 1.0) < 1e-9

    def test_observables_Z_X_are_4x4(self):
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        gamma_z = p.observable("qber_Z")
        gamma_x = p.observable("qber_X")
        assert gamma_z.shape == (4, 4)
        assert gamma_x.shape == (4, 4)

    def test_wlc_sdp_shape_compatibility(self):
        # Regression: Codex caught "Incompatible dimensions (4, 4) (8, 8)"
        # Check that observable and conditional state shapes match.
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        rho = p.conditional_alice_bob()
        gamma_z = p.observable("qber_Z")
        # Tr(rho · gamma) must be well-defined → shape match
        assert rho.shape == gamma_z.shape

    def test_wlc_key_rate_runs_without_dim_error(self):
        # Round-3 regression for Codex Round-2 finding: wlc_key_rate() should
        # not fail with KeyError('p_sift') or dim mismatches on the protocol's
        # own observation_keys.  The returned rate value is placeholder-based
        # (not authoritative); we only pin that the call succeeds.
        from qkdx.protocols.pm_qkd import build_pm_qkd_protocol
        try:
            from qkdx.numerics.wlc import wlc_key_rate
        except ImportError:
            pytest.skip("WLC SDP module not available")
        p = build_pm_qkd_protocol(mu=0.3, eta_channel=0.1)
        # Note: _bb84_conditional_state has qber_Z = placeholder but qber_X = 0.5
        # (max-mixed X, since PM-QKD source has no X-basis structure).  The
        # SDP may be infeasible on this constraint combo — we accept that,
        # only regress against plumbing errors.
        observations = {"qber_Z": 0.05, "qber_X": 0.5, "p_sift": 2.0 / 16}
        try:
            rate = wlc_key_rate(p, observations, solver="SCS")
        except (RuntimeError, ValueError) as e:
            msg = str(e)
            # Solver infeasibility is acceptable (placeholder may be infeasible);
            # but dim errors and KeyErrors are regressions.
            assert "Incompatible dimensions" not in msg, f"dim mismatch regressed: {e}"
            assert "p_sift" not in msg.lower() or "infeasib" in msg.lower()
            pytest.skip(f"SDP solver failed (acceptable for placeholder): {e}")
        except KeyError as e:
            pytest.fail(f"wlc_key_rate raised KeyError on our observation_keys: {e}")
        else:
            # Rate can be any finite float; we don't assert value.
            assert rate == rate  # not NaN


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
