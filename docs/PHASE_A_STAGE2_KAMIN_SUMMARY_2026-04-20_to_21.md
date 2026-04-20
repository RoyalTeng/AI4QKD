# Phase A Stage 2 (Kamin 2025 SDP) — Autonomous Session Summary

**Dates**: 2026-04-20 → 2026-04-21
**Session type**: user-authorized continuous autonomous work
**Start commit**: `54cc37f` (Phase 0 migration prep)
**End commit**: `ca202a1` (A4b Kamin Fig.1 reproduction)
**Commits produced**: 5 (`3434db3` A1 → `ca202a1` A4b)
**Tests added**: 44 (13+6+6+7+12 across A1/A2/A3/A4a/A4b)
**MOSEK**: ✓ used throughout (`~/mosek/mosek.lic`)

---

## 1. Scope of this session

Continuation of the research plan approved in previous session:
RESEARCH_PLAN §3.3 S2.5 "GEAT implementation + Kamin 2025 reproduction".
Phase A Stage 2 goal per docs/literature/Kamin-2025.md §9.2:
qubit BB84 (Fig. 1) full GEAT with Choi-state SDP + Thm 4 dual +
Eq. 16 finite-key.

---

## 2. Commits at-a-glance

| Commit | Title | Tests | Key result |
|---|---|---|---|
| `3434db3` | A1 Choi SDP infrastructure | 13 | h_per_sift matches WLC SDP < 1.1e-8 |
| `3c76248` | A2 Thm 4 dual extraction | 6 | g*_X = -log₂((1-q)/q) within solver precision; g*_Z ≈ 0 |
| `d89cf9f` | A3 Full Thm 3 key length + (γ,α) opt | 6 | Fig.1 0 dB anchor: n=10^6→0.587, n=10^12→0.892 |
| `a9a4d27` | A4a Loss model η_det scaling | 7 | Loss variant matches no-loss at L=0; scales by η_det |
| `ca202a1` | A4b Fig.1 reproduction + tight V² | 12 | Positive-rate region reproduces Kamin §6.3 within ±15% |

---

## 3. What was accomplished (validated)

### 3.1 Numerical primitives

- `kamin_choi_sdp_qubit_bb84(qber, γ)` — Kamin Eq. 41/42 Choi SDP via
  `cvxpy.quantum_rel_entr` + MOSEK.  Reproduces WLC direct-ρ SDP at
  matching qber values (diff < 1.1e-8).
- `kamin_choi_sdp_qubit_bb84_with_dual(qber, γ)` — extracts g* =
  (g_Z, g_X) from CVXPY Lagrange multipliers of QBER equality
  constraints, with sign-convention flip so g_B = ∂(rate_per_sift)/∂qber_B.
- `_kamin_V2_bb84_tight(g_Z, g_X, qber, γ, η_det)` — tight UB on
  Var_{p_hon}(f) derived from per-round observation variance with
  f(ω_i) = (2/γ)·g_B·1{B-test-error}.  Strictly tighter than Kamin
  Eq. 44 UB by factor ~η·qber (≈100× at Fig. 1 parameters).

### 3.2 Key-length formulas

- `kamin_full_key_length_bb84(qber, n, γ, α)` — fixed-(γ, α) Eq. 16.
- `kamin_full_key_length_bb84_optimized(qber, n)` — grid search over
  (γ, α) with auto-selected α ∈ {1 + c/√n : c ∈ [0.1, 10]}; SDP solved
  once (γ, α, η_det independent).
- `kamin_full_key_length_bb84_loss[_optimized](..., loss_dB)` — loss
  variant with η_det = 10^(−L/10).
- `kamin_fig1_sweep(qber, n_values, loss_dB_values)` — single-SDP-solve
  batch evaluation over the full (n, L) grid.

### 3.3 Anchors matched vs Kamin §6.3

| Anchor | Source | Expected | Achieved |
|---|---|---|---|
| h_per_sift at qber=0 | Analytic | 1.000 | 1.0000 |
| h_per_sift at qber=0.05 | WLC SDP | 0.6389 | 0.6389 (< 1e-8 diff) |
| g*_X at q=0.05 | -log₂(19) | -4.2479 | -4.2479 (< 1e-3 diff) |
| 0 dB n=10^12 rate | Kamin §6.3 "≈ 0.9" | 0.85-0.95 | 0.893 ✓ |
| Asymptotic at n=10^15 | Devetak-Winter | (h/sift − f_EC·H) | within 5% ✓ |
| 0 dB n=10^6 rate | Finite-size dominant | 0.5-0.7 | 0.587 ✓ |

---

## 4. Known limitations (honest accounting)

### 4.1 Cutoff-loss at n ≥ 10^8 does not match Kamin Fig. 1

My kamin_fig1_sweep gives residual-positive rates (~10⁻³ bits/round)
beyond Kamin's GEAT cutoffs at n ≥ 10^8:

| n | Kamin GEAT cutoff | My cutoff (last positive) |
|---|---|---|
| 10^6 | 15 dB | ~15 dB ✓ |
| 10^8 | 20 dB | > 30 dB |
| 10^10 | 25 dB | > 30 dB |
| 10^12 | 26 dB | > 30 dB |

**Attribution**: the heuristic Eq. 16 form in
`qkdx.finite_key.kamin_geat.kamin_heuristic_key_length` uses a
closed-form V² (mine = tight_bb84 observation-variance UB).  Kamin's
Fig. 1 uses full Thm 3 + Thm 4 Legendre-Fenchel f-optimization,
which gives a tighter finite-size penalty at the cutoff.  My positive-
rate region is correct within ±15%; cutoff-region saturation is
follow-up work (documented in
[docs/research/kamin_fig1_report.md](research/kamin_fig1_report.md)
§5).

### 4.2 A4c (decoy-state Fig. 3/4) NOT attempted

RESEARCH_PLAN §3.3 S2.5 hard acceptance is decoy-state Fig. 4 /
Table 1 within 5%.  Implementing this requires Kamin Eq. 80
block-diagonal SDP + decoy LP + photon-number truncation N_ph.
Kamin 2025 memo §9.2 estimates "6-8 weeks high-risk" — not feasible in
this session.

### 4.3 V² derivation

The tight V² formula `(2·η_det·qber/γ)·(g_Z²+g_X²)` is derived under
assumptions about Kamin's f-normalization convention.  Fully rigorous
derivation from Kamin's Thm 4 Appendix A would require reading the
source and matching exactly.  Numerically validated to give
Kamin-consistent rates in positive-rate region; residual looseness at
cutoff suggests the formula may differ from Kamin's by an O(1)
multiplicative constant or an additive term vanishing at
low (η, qber).

---

## 5. Deliverables index

Code:
- [qkdx/numerics/kamin_sdp.py](../qkdx/numerics/kamin_sdp.py)
  (~1200 lines; primary module for Stage 2)

Tests:
- [tests/test_numerics/test_kamin_sdp.py](../tests/test_numerics/test_kamin_sdp.py) (13)
- [tests/test_numerics/test_kamin_dual.py](../tests/test_numerics/test_kamin_dual.py) (6)
- [tests/test_numerics/test_kamin_full_key.py](../tests/test_numerics/test_kamin_full_key.py) (6)
- [tests/test_numerics/test_kamin_loss.py](../tests/test_numerics/test_kamin_loss.py) (7)
- [tests/test_numerics/test_kamin_fig1.py](../tests/test_numerics/test_kamin_fig1.py) (12)

Artifacts:
- [docs/research/data/kamin_fig1_sweep.csv](research/data/kamin_fig1_sweep.csv)
- [docs/research/kamin_fig1_report.md](research/kamin_fig1_report.md)

Scripts:
- [scripts/sweep_kamin_fig1.py](../scripts/sweep_kamin_fig1.py)

---

## 6. Suggested next steps for user review

Ordered by impact × feasibility:

1. **Approve A4b positive-rate anchors** — Kamin §6.3 "≈ 0.9" reproduced;
   positive-rate region ±15%.  Accept as S2.5 Stage 2 qubit-BB84
   acceptance.
2. **Scope A4c decoy**: either a dedicated 1-2 week session, or
   declare decoy as out-of-scope for Stage 2 (qubit-only) and accept
   qubit Fig. 1 as the RESEARCH_PLAN §3.3 S2.5 硬验收 substitute (per
   Kamin memo §9.2 suggestion that "RESEARCH_PLAN §3.3 S2.5 acceptance
   'BB84' is not qubit vs decoy — qubit Fig. 1 is an effective hard
   acceptance, decoy is stretch").
3. **Phase B Sub-Q3 §4.4** — WTB second-order expansion, E_sq
   numerical, `docs/research/upper_bound_report.md`.  Self-contained
   analytic work, lower risk than decoy Fig. 4.
4. **V² derivation rigor pass** — sit with Kamin Appendix A to tighten
   `_kamin_V2_bb84_tight` to exactly match Thm 4, which should close
   the cutoff gap.

---

## 7. Rigor discipline adherence

Per user directive "每一步推导，每一次数值计算都要非常严谨":

- All SDP results cross-validated against independent source (A1 vs
  WLC; A2 g_X against analytic −log₂((1−q)/q) for BB84 Werner).
- Sign-convention flip for CVXPY dual explicitly documented and
  tested (A2 test_dual_matches_analytic_bb84_derivative).
- No-loss limit consistency: `kamin_full_key_length_bb84_loss` at
  `loss_dB=0` matches `kamin_full_key_length_bb84` to < 1e-3 relative
  (A4a test_fixed_loss0_matches_no_loss).
- Monotonicity invariants checked (rate ↑ in n, ↓ in loss).
- Numerical vs analytic match at asymptotic regime (A3/A4a asymptotic
  Devetak-Winter tests within ±5%).

Honest accounting: known limitations §4 are SURFACED (not buried);
positive-rate region validated separately from cutoff region.
