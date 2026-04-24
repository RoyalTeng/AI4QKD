# Workflow log: day4-bug-fix-AD-KD-hierarchy-review

**Mode**: review-only (评审已 commit 的 Day 4 改动)
**Date**: 2026-04-24
**Scope**: 5 commits 的代码 + 文档变更

## SETUP

**Patch**: changes-v1.patch (655 lines)
**Files in scope**:
- qkdx/numerics/upper_bound.py (bug fix + K_D_AD function)
- tests/test_numerics/test_upper_bound.py (4 new tests)
- docs/findings/upper_bound_report.md (v0.5 §11)
- docs/findings/qubit_E_R_PPT_hierarchy_2026-04-23.md
- docs/findings/log_neg_msEB_application_2026-04-23.md
- docs/findings/pareto_bb84_family.md (v0.2)
- docs/findings/gap_shape_g4_1.md (v0.3)
- scripts/gap_shape_analysis.py (candidate D)

**Day 4 commits in scope** (from b4efaae~1 to HEAD):
- b4efaae: e_r_depolarizing_analytic bug fix (d²-1 vs d-1)
- 5579e0f: docs(tightness) update
- 01935fa: BB84 真 E_R 紧化
- 73bd18f: AD K_D = Q analytic
- c0531a7: Plenio 不等式 4 信道扩展
- ea7868d: session epilogue v0.2
- a049de0: upper_bound_report v0.5
- 2c565cc: gap_shape v0.3 candidate D
- 008710e: pareto_bb84_family v0.2

## Round 1

**Status**: Codex agents launched (PIDs 26899/26900, gpt-5.4 xhigh effort). Review files pending.

**Launched**: 2026-04-24 00:23
**Output expected**: review-diff-1.json + review-holistic-1.md
**Action on completion**: Read verdict, apply R0.2 C3 rules (PASS/FAIL/REJECTED)
