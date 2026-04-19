# Phase 0 Retrospective Review — Workflow Log

**Skill**: dev-reviewer (并行双 Codex Agent 迭代闭环,max 5 轮)
**Base**: `981c5f7` (Phase 0 初封装)
**Head (final)**: `01a963d`
**Date**: 2026-04-19

## 轮次汇总

| 轮次 | Agent 1 (diff, xhigh) | Agent 2 (holistic, high) | 修复 Commit | 测试 |
|------|-------|-------|-------|-------|
| R1 | REJECTED (1 crit + 4 major) | FAIL (3 major) | `20f9029` + `b5b34c9` | 131 → 150 passed |
| R2 | FAIL (3 major) | FAIL (同步) | `ec1f3cb` | 155 passed |
| R3 | FAIL (1 major §6.1 counts) | — | `48333f8` | 155 passed |
| R4 | **PASS** | FAIL (1 major M2 closure) | `21f226d` | 155 passed |
| R5 (cap) | FAIL (1 major terminology) | — | `01a963d` | 155 passed |

## 修复总计

**R1 code (commit 20f9029):**
- CRITICAL: `wlc_key_rate` 漏检 `scope_tag='out_of_scope'` → 加 `OutOfScopeError` 硬门禁
- MAJOR×4: MDI scope 不一致 / Frank-Wolfe 可行点污染 / facial reduction 静默失败 / decoy 测试未固定

**R1 docs (commit b5b34c9):** Agent 2 额外 3 项
- WLC MOSEK 正则化 `G(ρ)+ε·τ` → `(1-ε)G(ρ)+ε·τ`
- RESEARCH_PLAN §2.1 MDI covered → partial
- `_mdi_sift_keep` 新增 3 回归测试

**R2 (commit ec1f3cb):**
- MDI partial 传播到 framework_coverage.md + PHASE0_REPORT.md
- `epsilon_regularization` 加 [0,1) 校验
- 加 convex-combo 回归测试 (MOSEK + parametric negative eps)
- `_mdi_sift_keep` 虚拟-EB 语义 docstring

**R3 (commit 48333f8):** framework_coverage §6.1 计数修正 covered=5→4

**R4 (commit 21f226d):** M2 Ma-Razavi Fig.3 硬验收拆分为 GLLP ideal (已达标) + Ma-Razavi (Phase 1 Sub-Q2 延后)

**R5 (commit 01a963d):** M2 闭合术语统一("M2 CLOSED with deferred follow-up")

## 最终状态

- **155 passed, 10 skipped** (MOSEK 未装)
- Agent 1 Round 4 PASS
- 5 轮上限,评审闭环,所有 critical/major 已处理

## 剩余 suggestions(非阻塞)

- **架构**:协议注入 solver-private hooks (`_observable_builders`) 是设计权衡,Agent 2 R1 标 FAIL 但未给修复方案 — 留作 Phase 1 架构 review 输入
- **CLARABEL 正则化回归**:`test_wlc_regularization_uses_convex_combination` 需要 MOSEK,CLARABEL 路径等价测试可追加
