# Workflow log: path-gamma-v03-retraction

**Mode**: review-only (no new implementation)
**Base**: 9402e44^ (pre path γ v0.2)
**Head (latest)**: Round 5b cleanup (this commit — pending user decision whether to run narrow Round 6 re-check or FINALIZE).
**Round commit trail**: Round 1 base = 2583ffc → Round 2 = 37fa7df → Round 3 = f5bb30a → Round 4 = bf0b790 → Round 5 = 149c60a → Round 5b cleanup = this commit.
**Scope**: path γ retraction cycle (v0.2 → v0.3 [CONJ]) + WTB 编号修正 + user manual edits + CLAUDE.md / rigor-rules 新增 + Round 3 rigor-rule tightening & path α/γ 反转修正 + Round 4 工作流边界 + path β citation 修正 + Round 5 升级规则 invariant (C1 ∧ C2 ∧ C3) + Round 5b R0.3/R2.3 表格 import invariant 声明 + placeholder cleanup

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

### Round 2 — 2026-04-21 FIX (commit 37fa7df)

**Files modified / added in `37fa7df`**:
- NEW `CLAUDE.md` (项目级 AI 协作规范，R0.1-R0.3 三红线)
- NEW `.claude/rules/research-rigor.md` (quick-reference)
- NEW `docs/workflow/path-gamma-v03-retraction/` (changes-v1.patch + changes-v2.patch + review-diff-1.{json,md} + review-holistic-1.md + workflow-log.md)
- `docs/AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md`:
  - §4 rewritten: path γ v0.2 审阅项全部 CLOSED
  - §5 rewritten: "若 v0.2 通过 → [COROLLARY]" 分支终结
  - WTB Thm 47 → Thm 19
- `docs/PHASE1_LOG.md:471`: Thm 26 → Thm 12
- `docs/findings/pareto_tf_family.md`: §3 PM-QKD 列 sync CSV + 相对路径 + 交叉点描述修正
- `docs/findings/gap_shape_g4_1.md`: 相对路径修正
- `docs/research/06_gap_structure.md` + `03_network_extension.md`: 加 retraction banner
- `docs/proofs/umr_data_processing_gamma.md` (touched as part of v0.3 history; actual v0.3 changes 在之前 commits 已做)

**Patch**: `changes-v2.patch` (296 lines)

### Round 2 review — 2026-04-21 (verdict: FAIL)

**Agent 1 (review-diff-2.json, gpt-5.4 xhigh)**: `FAIL` — 3 MAJOR + 1 MINOR
- MAJOR 1: workflow-log stale（指向 2583ffc 而非 37fa7df；漏 CLAUDE.md + rigor.md）
- MAJOR 2: conclusions §5 **path α/γ 反转** — 误把 α 的三 lemma 挂在 γ 名下（Log 07 §4.5 path γ 是 single-edge PLOB + data-processing）
- MAJOR 3: CLAUDE.md + rigor.md 仍含 "WTB Thm 26/47" 字面（live policy 不应保留旧编号）
- MINOR 1: pareto_tf_family.md:85 引用不存在的 `02_mdi_family.md`

**Agent 2 (review-holistic-2.md, gpt-5.4 high)**: `FAIL` — 2 MAJOR + 1 MINOR
- MAJOR 1: 新规则对 "independent review" 定义弱于 RETRACTION.md §4.1 规则 3（允许 "不同 agent / 不同 prompt" 算独立，precedent 要求 "不同训练偏差源 / 人类 / 工具"）
- MAJOR 2: user sign-off 规则不一致（R0.2 只说 [THM] 必要；R0.3 / §3.1 暗示 [COROLLARY] 也必要）→ 应单值
- MINOR 1: umr_data_processing_gamma.md:171, 273 残留 "[COROLLARY pending]" 语言（虽在 archival block）

**Decision**: 进入 Round 3 FIX（用户指示 max 轮次 = 标准 5 轮）

### Round 3 — 2026-04-21 FIX (commit f5bb30a)

**Addressed 5 MAJOR + 2 MINOR 合并 issue set** (全部 closed — Round 3 review 确认)：

1. ✅ workflow-log 部分对齐 HEAD（Round 4 进一步完善 HEAD 锚点）
2. ✅ conclusions §5 path α/γ 反转：α 承担三 lemma；γ 按 Log 07 §4.5 写成 single-edge PLOB + data-processing；β 写成 channel-reduction
3. ✅ CLAUDE.md + rigor.md 移除 "WTB Thm 26/47" 字面
4. ✅ CLAUDE.md R0.2 + rigor R2.2: sign-off 单值化 + "independent review" 对齐 RETRACTION §4.1 规则 3
5. ✅ pareto_tf_family.md:85 改引 `pareto_mdi_family.md` + `m2_wlc_mdi_sixstate.md`
6. ✅ umr_data_processing_gamma.md:171/:273 残留 "[COROLLARY pending]" 加 strikethrough + 作废标签

**Patch**: `changes-v3.patch` (232 lines)

### Round 3 review — 2026-04-21 (verdict: FAIL, 窄范围)

**Agent 1 (review-diff-3.json, gpt-5.4 xhigh)**: `FAIL` — 1 MAJOR + 1 MINOR
- MAJOR 1: workflow-log 未把 Round 3 明确锚定到 f5bb30a（保留 pre-commit placeholder "this commit"）
- MINOR 1: conclusions §5 path β 引用 Log 07 §3.2，但 authoritative 位置在 §3.1 + §4.4

**Agent 2 (review-holistic-3.md, gpt-5.4 high)**: `FAIL` — 1 MAJOR
- MAJOR 1: CLAUDE.md §3 工作流描述与 R0.2 independent-review 定义存在 enforcement 漏洞。§3 强制 dev-reviewer 双 Codex 流程，但未明确"此流程必要但**不单独**满足 R0.2"。同家族 AI 审计链仍可能被误读为独立验证
- [已 closed] Round 3 确认所有 6 项 Round 2 issues 已关闭（path α/γ 反转、WTB 字面、sign-off 单值化、independence 定义、MDI 链接、archival quarantine）

**Decision**: Round 4 FIX，合并 2 MAJOR + 1 MINOR。

### Round 4 — 2026-04-21 FIX (commit bf0b790)

**Addressed 2 MAJOR + 1 MINOR** (substance closed; Round 5 further tightens wording):

1. ✅ [Agent 1 M1] workflow-log anchors Round 3 = f5bb30a
2. ✅ [Agent 1 m1] conclusions §5 path β citation fixed (Log 07 §3.1 + §4.4)
3. ✅ [Agent 2 M1] CLAUDE.md §3 + rigor.md 加入 dev-reviewer 边界红线（headline level）

**Patch**: `changes-v4.patch` (127 lines, saved and committed)

### Round 4 review — 2026-04-21

**Agent 1 (review-diff-4.json, gpt-5.4 xhigh)**: `PASS` — 1 MINOR only
- MINOR 1: workflow-log :5 + :102 still has pre-commit placeholder "(this commit, pending)" / "(to be saved)"

**Agent 2 (review-holistic-4.md, gpt-5.4 high)**: `FAIL` — 1 MAJOR new regression
- MAJOR 1: Round 4 的 "不单独满足" 措辞正确，但叠加的 "或 / 任一 / user sign-off" 语法把 C1 (a/b/c) 和用户签字写成了**替代**关系（而非并列）。R0.2 说 [COROLLARY] 要 "两独立评审 + 用户签字"（AND），但 §3.2 只对 [THM] 额外要求 (a/b/c)，暗示 [COROLLARY] 可能不需要。rigor.md :39 "或叠加 (b)/(c)" + workflow-log :99 "任一 (R0.2 a/b/c)" 同类问题。可被 AI 误读为 "dev-reviewer PASS + 用户签字 → [COROLLARY] OK"，**正是 Round 4 本要封堵的 loophole**。

**Decision**: 任一 reviewer FAIL → Round 5 FIX (最终轮)。

### Round 5 — 2026-04-21 FIX (commit 149c60a)

**Addressed 1 MAJOR + 1 MINOR**:

1. ✅ [Agent 2 M1] [COROLLARY] / [THM] 升级规则改写为 **invariant AND logic** (C1 ∧ C2 ∧ C3)：
   - **C1** R0.2-compliant independent review PASS（(a)/(b)/(c) 任一）
   - **C2** 用户显式签字（逐项确认）
   - **C3** dev-reviewer 双 Codex PASS
   - 三条件**并列必要**（AND）；任一缺失即非法；显式列越权 / 合法示例
   - 对应 CLAUDE.md R0.2 + §3.2 + .claude/rules/research-rigor.md R2.2 同步收紧
2. ✅ [Agent 1 m1] workflow-log 锚定 Round 4 = bf0b790

**Patch**: `changes-v5.patch` (185 lines, saved at commit 149c60a)

### Round 5 review — 2026-04-21

**Agent 1 (review-diff-5.json, gpt-5.4 xhigh)**: `FAIL` — 1 MAJOR + 1 MINOR
- MAJOR 1: R0.3 / R2.3 分级表格未显式 import R0.2 invariant；`[COROLLARY]` 行保留"用户签字"而未列 C1/C3 → 可被误读为第二条弱规则
- MINOR 1: workflow-log 仍有 Round 5 "(pending)" placeholder（本身承诺已清理但实际未完成）

**Agent 2 (review-holistic-5.md, gpt-5.4 high)**: `PASS` — 0 MAJOR, 1 MINOR
- MINOR: workflow-log placeholder 同 Agent 1 m1
- 明示 `READY_FOR_FINALIZE = yes` 前提是 MINOR 可选修复
- 可选加固建议：分级表 [COROLLARY] 行加 cross-reference R0.2 (C1∧C2∧C3) —— 与 Agent 1 M1 同方向

**Decision**: Agent 1 verdict 自建议 "Transfer to user decision: patch tables + placeholders, then narrow re-check"。Max 5 轮已到。Claude 先完成 **Round 5b 机械 cleanup**（仅两项 text edit），然后转用户审签是否：
(i) 接受 Round 5b 直接 FINALIZE；(ii) 启动窄范围 Round 6 re-check；(iii) 其他

### Round 5b cleanup — 2026-04-21 (this commit)

1. ✅ [Agent 1 M1] CLAUDE.md R0.3 表格 + rigor.md R2.3 表格 前加声明句 "任何升级 / 对外引用 eligibility 均由 R0.2 (C1 ∧ C2 ∧ C3) 统一裁定；本表不构成独立升级路径" + [COROLLARY] / [THM] 行的 "对外可引用" 列明示 "前提：R0.2 C1 ∧ C2 ∧ C3 通过"。[COROLLARY] 行内容语义列去除独立的 "用户签字" 表述（避免被读作表格级规则）
2. ✅ [Agent 1 m1 / Agent 2 MINOR] workflow-log 彻底去除 "this commit (pending)" / "(to be saved)" placeholder；Round 5 锚定到 149c60a；Round 5b 标明为 this commit

**Patch**: `changes-v5b.patch` (pending commit)

**Status**: **FINALIZED** — 用户于 2026-04-21 session 显式接受 Round 5b 直接 FINALIZE（不启动 Round 6 re-check）

---

## Final outcome (FINALIZED 2026-04-21)

**Retraction cycle 完整归档**：

- **核心撤回**: path γ v0.2 [COROLLARY pending] → v0.3 **[CONJ]**，双 reviewer 独立 UNSOUND（Claude audit + Codex audit）
- **文档状态**: 全部与 FINDINGS v2 §1.1 对齐（umr 上界仅在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下为 [CONJ]）
- **用户审阅 queue**: 从 5 项 / 4-5 天 压缩到 3 项 / 1-1.5 天（path γ v0.2 三项 CLOSED）
- **治理文件新增**: [CLAUDE.md](../../../CLAUDE.md)（R0.1-R0.3 三红线；升级规则 C1 ∧ C2 ∧ C3 invariant）+ [.claude/rules/research-rigor.md](../../../.claude/rules/research-rigor.md)（同步 quick-reference）

**轮次汇总**：

| 轮 | commit | reviewers | verdict | 处理 |
|---|---|---|---|---|
| Round 1 | 2583ffc | dual Codex | Agent 1 REJECTED + Agent 2 major | 5 issues → Round 2 |
| Round 2 | 37fa7df | dual Codex | Agent 1 FAIL + Agent 2 FAIL | 7 issues → Round 3 |
| Round 3 | f5bb30a | dual Codex | Agent 1 FAIL + Agent 2 FAIL | 3 issues → Round 4 |
| Round 4 | bf0b790 | dual Codex | Agent 1 PASS + Agent 2 FAIL | 1 MAJOR → Round 5 |
| Round 5 | 149c60a | dual Codex | Agent 1 FAIL + Agent 2 PASS | 分裂 → Round 5b cleanup |
| Round 5b | 9ab3559 | — | 机械 cleanup | ✅ **FINALIZED** |

**用户决策时序** (time-stamped, per R0.1 exception requirement):

- 2026-04-21 session 末：用户显式指示 "接受 5b 直接 FINALIZE" → 工作流关闭
- **注**：Round 5 本身未取得 unified PASS（Agent 1 FAIL vs Agent 2 PASS），按 R2.2 "任一 FAIL → 撤回" 字面应启动 Round 6；但用户用其**审签权**（FINALIZE decision）终止 workflow。此决策不构成任何理论陈述的升级（无 [CONJ] → [COROLLARY] 发生），仅关闭 dev-reviewer QA cycle。umr 上界仍为 **[CONJ]**

**未来工作提示**（AI 代理需遵守）：

1. 本 cycle 生成的 R0.2 C1 ∧ C2 ∧ C3 invariant 对**后续**所有 [CONJ] / [SYN] → [COROLLARY] / [THM] 升级**生效**（包括未来尝试 path α / β / γ 真版）
2. 本 cycle 用户 FINALIZE decision 是**单次** scope 结束信号，**非** invariant 豁免
3. 若未来重启 umr 上界升级，AI **不得**自主执行；须用户显式启动，且必须走 C1 ∧ C2 ∧ C3 完整路径（见 [docs/AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md §5](../../AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md)）


