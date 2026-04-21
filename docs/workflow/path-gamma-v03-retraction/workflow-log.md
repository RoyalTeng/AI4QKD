# Workflow log: path-gamma-v03-retraction

**Mode**: review-only (no new implementation)
**Base**: 9402e44^ (pre path γ v0.2)
**Head**: 2583ffc (HEAD, Codex verdict correction + WTB numbering fix)
**Scope**: path γ retraction cycle (v0.2 → v0.3 [CONJ]) + WTB 编号修正 + user manual edits

## Round 1 — SETUP done 2026-04-21

- Patch: `changes-v1.patch` (6687 lines)
- Commits in scope:
  - 9402e44 path γ v0.2 [COROLLARY pending]
  - 6369e34 v0.2 → v0.3 [CONJ] retraction (Claude audit UNSOUND-RETRACT)
  - 2583ffc Codex verdict confirmed UNSOUND + WTB Thm 26→12 / Thm 47→19 全局修正
- User manual edits (linter): gap_shape_g4_1.md 10 dB 行、pareto_tf_family.md 10 dB 行
- Review focus (user instruction): 验证推导 + 计算准确性

## Review rounds log

### Round 1 — 2026-04-21

**Agent 1 (diff review)**: `REJECTED`
- CRITICAL: AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md §4/§5 still frames path γ v0.2 as pending-review / active branch after announcing retraction
- MAJOR: WTB Thm 47 / Thm 26 remnants in PHASE1_LOG.md:471 and conclusions:151
- MAJOR: pareto_tf_family.md §3 PM-QKD rate column at 10/20/40/60 dB inconsistent with §2.1 (2.50e-4 vs 3.80e-4 etc.)
- MINOR: gap_shape_g4_1.md + pareto_tf_family.md reproducibility paths wrong (`data/` vs actual `../research/data/`)

**Agent 2 (holistic review)**: MAJOR issues overlap with Agent 1 (retraction cascade not cleaned; scope caveat needs stronger placement).

**Decision**: enter Round 2 FIX.

### Round 2 — 2026-04-21 FIX (this commit)

**Files modified**:
- `docs/AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md`:
  - §4 rewritten: path γ v0.2 审阅项全部 CLOSED（retraction 后不再占用户 queue），重写为非 path-γ 审阅事项
  - §5 rewritten: "若 v0.2 通过 → [COROLLARY]" 分支终结；列出未来重启 umr 上界升级时必须避免 v0.2 adversarial containment 简化 + Log 07 §3.3 三 lemma 要求
  - WTB Thm 47 → Thm 19 (第 151 行原文)
- `docs/PHASE1_LOG.md:471`: Thm 26 → Thm 12 with audit note
- `docs/findings/pareto_tf_family.md`:
  - §3 PM-QKD rate 列 sync 自 CSV (10 dB 2.50e-4, 20 dB 7.78e-5, 40 dB 7.67e-6, 60 dB 6.96e-7)
  - 交叉点描述从 "30-40 dB" → "40-50 dB" 匹配 sync 后的数据
  - 数据 / 图表链接从 `data/` / `figures/` → `../research/data/` / `../research/figures/`
- `docs/findings/gap_shape_g4_1.md`: 同样的相对路径修正
- `docs/research/06_gap_structure.md`: 顶部加 [RETRACTED / ARCHIVAL ONLY] banner（Round 1 已做）
- `docs/research/03_network_extension.md`: 顶部加 [PARTIALLY RETRACTED] banner（Round 1 已做）

**Patch**: `changes-v2.patch` (296 lines)

**Decision**: Round 1 CRITICAL + MAJOR 全部修复。因用户指示 Max 轮次=2（Round 1 PASS 停；FAIL 则修复一轮后 Round 2），本 Round 2 直接 FINALIZE（commit 后不再发起 Round 3 Codex review）。

## Final outcome

- Retraction cycle complete: v0.2 [COROLLARY pending] → v0.3 [CONJ]，双 reviewer 独立 UNSOUND
- Documentation state aligned with FINDINGS v2 §1.1 / CLAUDE.md R2.3
- User review queue reduced from 5 items (4-5 day) to 3 items (1-1.5 day)，path γ v0.2 三项 CLOSED
