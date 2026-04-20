# Phase 1 Retrospective Review — Workflow Log

**Mode**: review-only
**Base**: cf79b00^ (= f8929f1, feat(analytic): Ma-Razavi 2012 Stage C/D)
**Head**: HEAD (= 2092890, docs(msen): PM-QKD MS-EB formulation v0.1)
**Scope**: 5 commits covering S2.4 GEAT memo → S2.5 Stage 1 Kamin impl → F6 TF-QKD + PM-QKD docs

## Commits under review

- cf79b00 GEAT-2024 Level 4 memo (S2.4)
- 537870d Kamin-2025 Level 3-4 memo (S2.5 准备)
- 98fd2a7 kamin_geat.py + 29 tests (S2.5 Stage 1)
- 95f5b24 TF-QKD 三变体 Level 3 memo (F6 §7.1)
- 2092890 PM-QKD MS-EB formulation v0.1 (F6 §7.2)

## Patch summary (v1)

- 7 files, 2015 insertions, 0 deletions
- code: qkdx/finite_key/kamin_geat.py (335 lines), tests/test_finite_key/test_kamin_geat.py (286 lines)
- docs: GEAT-2024.md, Kamin-2025.md, TF-QKD.md, pm_qkd_formulation.md + PHASE1_LOG.md updates

## Round 1

- [x] Agent 1 diff review (JSON) — `review-diff-1.json`
- [x] Agent 2 holistic review (MD) — `review-holistic-1.md`
- [x] Merge verdict

### Verdict: **REJECTED** (2 critical + 3 major issues)

#### Critical (must fix before treating Stage 1 as a valid Thm 3 implementation)

**C1. EC leakage double-counted** (kamin_geat.py:194-231, 275-281)
- `bb84_qubit_asymptotic_rate()` already includes `-f_EC·h(Q)`, but `lambda_EC = n·(1-γ)²·η_det·f_EC·h(Q)` is subtracted again in `kamin_theorem3_key_length()`.
- Impact: every Stage-1 number shifted down by `n·(1-γ)²·η_det·f_EC·h(Q)` per round.
- Root cause of the 10 dB premature cutoff at n≥10^10, not (only) `Var(f)=1`.
- Fix: split into pre-EC entropy helper `(1-γ)²·η_det·[1-h(Q)]` → Thm 3 `h`; keep `lambda_EC` separate.

**C2. Missing min-tradeoff optimization** (kamin_geat.py:146-186, 247-257)
- Code treats unique-acceptance as if `T_α(f)` reduces to just the variance penalty. Kamin Eq. 11/41/42 still require (a) a valid affine min-tradeoff g and (b) the infimum over admissible p/J.
- Unique-acceptance removes `Δ_com`, not the min-tradeoff inf.
- Current code is a **heuristic Stage-1 estimator**, not a faithful Thm 3 implementation — module/docs/tests overclaim theorem-level correctness.
- Fix options: (a) implement Eq. 41/42 optimization path with crossover min-tradeoff g / FW, OR (b) rename + document as heuristic pre-SDP approximation.

#### Major

**M1. PM-QKD source_state formulation problem** (pm_qkd_formulation.md:42-50)
- Averaging over random phase then keeping only classical κ register makes optical marginal independent of κ → key bit not carried by emitted state.
- Ma treats phase announcement as the hard step precisely because one cannot collapse to phase-randomized Fock mixture after announcements.
- Fix: rewrite source in explicit phase-register / EB form; apply parity/photon-number reductions only after preserving ancilla-phase correlations.

**M2. Tests miss pre-EC vs post-EC semantics** (test_kamin_geat.py:167-286)
- Tests codify the same post-EC formula as implementation → cannot catch C1/C2.
- Benchmark tolerances too loose to see ~0.05 bits/signal systematic error.
- Fix: regression tests that separately check Eq. 59 `H(S|YI)`, pre-EC entropy `(1-γ)²η_det[1-h(Q)]`, and final D-W rate with tight tolerances.

**M3. PHASE1_LOG gap explanation incomplete** (PHASE1_LOG.md:612-620)
- Blames only `Var(f)=1`, misses the C1 double-count and C2 missing optimization.
- Fix: after C1/C2 fixed, reclassify Stage 1 outputs as heuristic/pre-SDP; separate conservative caveat from actual formula mismatches.

#### Additional findings (holistic review)

- **H1. [MR22] citation error** (GEAT-2024.md): says "same arXiv number" but MR22 is distinct paper.
- **H2. PM-QKD naming collision**: Kamin-2025.md uses "PM-QKD" for prepare-and-measure; F6 uses it for phase-matching. Collision costly in this codebase.
- **H3. Kamin Table 1 overclaim** (Kamin-2025.md, PHASE1_LOG.md): paper DOES have a Table 1 (notation table p.5) — my "论文不含 Table 1" wording is too absolute.
- **H4. TF-QKD.md SNS coherent-attack claim unsupported** (line ~223): attributes round-independence limitation to Wang-Yu-Hu that reviewer could not substantiate from the paper.
- **H5. Plan alignment overstatement** (PHASE1_LOG.md:494): "qubit Fig. 1 亦可满足 S2.5 的字面约束" too generous; plan text is more specific.

#### Next round recommendation (from Codex)

> Fix the Eq. 16 decomposition first: separate pre-EC entropy from EC leakage, stop presenting the current shortcut as a valid Theorem 3 implementation, then regenerate the BB84 benchmarks/docs and tighten the tests around pre-EC vs post-EC semantics.

---

## Round 2 (fix)

User instruction: proceed per A1 plan. Round 2 addressed all Round-1 findings:
- C1 fix: bb84_qubit_preEC_entropy / bb84_qubit_leak_EC_per_round split; bb84_qubit_finite_key_length now uses pre-EC h.
- C2 fix: rename kamin_theorem3_key_length → kamin_heuristic_key_length with DeprecationWarning alias; disclose no min-tradeoff optimization.
- M1 fix: pm_qkd_formulation.md §1.1 rewritten with phase register R_A.
- M2 fix: +10 regression tests covering pre-EC/post-EC decomposition (29 → 39).
- M3 fix: PHASE1_LOG §4.8 rewritten with Round-2 cautions; Round-1 plan-alignment overclaim H5 retracted.
- H1 fix: GEAT-2024.md arXiv number corrected (2203.04989 vs MR22 2203.04993).
- H2 fix: Kamin-2025.md "PM-QKD" → "prepare-and-measure QKD" (F6 phase-matching naming collision).
- H3 fix: Kamin Table 1 claim softened (paper has notation Table 1).
- H4 fix: TF-QKD.md SNS coherent-attack claim retracted.
- H5 fix: PHASE1_LOG S2.5 plan-alignment overclaim removed.

Tests: 384 passed + 10 skipped (was 374+10 at Round 1).

## Round 2 review

Verdict: **FAIL** (upgraded from REJECTED). 2 residual issues:
- Major M6: pm_qkd_formulation.md "Fock 对角化 on announcement" still conflates conditioning with tracing.
- Minor: kamin_geat.py docstring said "underestimate at small n" which is only justified for Var(f)=1, not for missing inf_{p,J}.

## Round 3 (fix)

- M6 fix: explicit two-case split in §1.1 — conditioning on announced φ gives coherent state; only tracing/averaging over R_A gives Poisson/Fock mixture.
- Minor fix: kamin_geat.py docstring now separates Var(f)=1 (known conservative) from missing inf_{p,J} (sign undetermined).

## Round 3 review

Verdict: **FAIL**. 1 residual:
- Major M6 residual: closing sentence in §1.1 review note still said "只在公告后才有条件化 Poisson 退化", contradicting the corrected body.

## Round 4 (fix)

- Rewrote closing sentence + §1.1 implementation warning to match the two-case split.
- Consistency sweep: Ma Lemma 1 scope note tied to "Eve's QND photon measurement" / tracing over R_A, not φ-conditioning.

## Round 4 review

Verdict: **PASS** ✓. 1 minor (non-blocking):
- §1.1 attributed φ announcement to "Charlie" instead of Alice/Bob. Fixed post-review.

## Final status

4 rounds total (1 initial + 3 fix rounds). Verdict: **PASS**.
Tests: 384 passed + 10 skipped. No regression.

Path taken: A1 (Stage-1 kept as heuristic pre-SDP anchor; Stage 2 SDP deferred to dedicated session).
Stage 2 (Kamin Thm 4 SDP + Frank-Wolfe + min-tradeoff dual extraction) remains the defensible-S2.5 work item.

