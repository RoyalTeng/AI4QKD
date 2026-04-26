# Workflow Log — path α v0.2 three-lemma framework review

**Feature**: `umr-path-alpha-three-lemma-v0-2`
**Started**: 2026-04-25 (autonomous session)
**Skill**: dev-reviewer (R0.2 C3 gate)

## 评审目标

对刚立项的 [docs/proofs/umr_path_alpha_three_lemma_v0_2.md](../../proofs/umr_path_alpha_three_lemma_v0_2.md) 三 lemma 框架做 R0.2 C3 级双 Codex 评审。

**关键约束**：
- 严格按 R0.2 多方验证：任一 reviewer verdict UNSOUND/REJECTED → 立即 retract path α v0.2（R0.2 红线）
- 不容忍任何隐含 [SYN] → [COROLLARY] / [THM] 升级
- 第 5 次 trap memory：AI draft 不得推 structural gaps

## Changeset (v1)

文件（新增 + 修改）：
- `docs/proofs/umr_path_alpha_three_lemma_v0_2.md` (新增, [SPEC] v0.2)
- `docs/proofs/umr_path_delta_relaxed_trust_v0_1.md` (新增, 顶部加 [SUPERSEDED] banner)
- `docs/proofs/umr_path_gamma_4_5_cheatsheet.md` (新增, 早前 session)
- `scripts/path_alpha_v0_2_alignment.py` (新增, reframing only)
- `docs/research/data/path_alpha_v0_2_alignment.csv` (新增, 数值对齐)
- `docs/research/figures/path_alpha_v0_2_alignment.png` + `.pdf` (新增, figure)
- `docs/research/FINDINGS.md` (修改, 新增 §4.3 strategy update pointer)

## Round 1 — 2026-04-25

### Diff reviewer (gpt-5.4, xhigh reasoning)

**Verdict**: **REJECTED**

Issues:
1. **CRITICAL** [umr_path_alpha_three_lemma_v0_2.md:142](../../proofs/umr_path_alpha_three_lemma_v0_2.md): Lemma B 把 `E_tr = Tr_{Charlie+broadcast} E_umr` 当作 standard partial-trace contraction，未列 transcript-side-information sub-gap，**这本身是隐藏结构假设**
2. **MAJOR** [umr_path_alpha_three_lemma_v0_2.md:95](../../proofs/umr_path_alpha_three_lemma_v0_2.md): §1.4 "也当然可运行" + Lemma A/B/C "Justification sketch" 实质是 draft proof closure，违反 statement-only
3. **MAJOR** [umr_path_alpha_three_lemma_v0_2.md:174](../../proofs/umr_path_alpha_three_lemma_v0_2.md): α.G2.E 在 §1.3 / §3 / §3.1 / 摘要中**不一致** —— 时而列入 4 gaps，时而被 case (a)/(b) 化简掉，weakens 升级闸门
4. **MAJOR** [umr_path_alpha_three_lemma_v0_2.md:263](../../proofs/umr_path_alpha_three_lemma_v0_2.md): §3.1 "confirming / 数值 confirm" 对 [SYN] 文档过 strong；MDI gap 被压成 ~1500× 与表格 ~2937×+ 不符
5. **MINOR** [umr_path_alpha_three_lemma_v0_2.md:352](../../proofs/umr_path_alpha_three_lemma_v0_2.md): §6.1 声称 FINDINGS 未修改，与本次 commit 修改 §4.3 矛盾

### Holistic reviewer (gpt-5.4, high reasoning)

**Verdict**: **UNSOUND**

主要 concerns:
- **STRATEGY_FIT**: 已提前做了 Sub-Q4 gap 归因，与 FINDINGS v2 §4.2 "Sub-Q4 归因应在 Sub-Q3 完成后重启" 冲突
- **RETRACTION_RISK**: 与旧 [umr_path_alpha_scaffolding.md](../../proofs/umr_path_alpha_scaffolding.md) 的 11-gap inventory 完全脱节；与 [umr_path_alpha_derivation.md](../../proofs/umr_path_alpha_derivation.md) §4 已识别的 cross-space transfer trap 直接冲突
- **PATH_RELATIONSHIPS**: §5.4 "比继续尝试 γ 更稳" 反转 Log 07 优先级，无新 user 直读依据
- **ALIGNMENT_WITH_LOG_07**: 低估了三 lemma 自身 gap 的重量级（Log 07 只说"要写出来"，旧 scaffolding 已展开成 11 个 [UNKNOWN]，本文件压回 4 个）
- **COMPLETENESS**: 时间估计严重失真（20-25h vs 旧 scaffolding 10-15 人日）；Day 5-9 计划与 R0.2 timing 不可能兼容
- **RECOMMENDATIONS**: 建议先撤回当前 v0.2 作 active strategy，改成 scaffolding-only / cautionary v0.3，恢复与旧 α scaffolding 一致性，所有结果句改条件句

### 撤回 action（per R0.2 红线 + dev-reviewer skill REJECTED protocol）

立即执行：

1. ✅ 在 [docs/proofs/umr_path_alpha_three_lemma_v0_2.md](../../proofs/umr_path_alpha_three_lemma_v0_2.md) 顶部加 **[REJECTED 2026-04-25 — R0.2 RED LINE TRIGGERED]** banner，列双 reviewer 7 条核心问题
2. ✅ 在 [docs/research/FINDINGS.md §4.3](../../research/FINDINGS.md) 改写为 "[REJECTED 2026-04-25]" 留痕，记录撤回时序 + 核心 trap 模式 + 第 6 次 trap 教训
3. ✅ 数值对齐脚本 + CSV + figure **保留**（仅 reframe，无新 LB claim），但使用时显式说明 path α v0.2 已 REJECTED
4. ✅ 路径 δ v0.1 banner **维持** [SUPERSEDED]（δ 的 capacity-monotonicity 路径同样被 α 撤回理由间接驳回）
5. ⏸️  **不**进入 Round 2 修复 —— per dev-reviewer skill protocol "REJECTED → 停止，报告 critical issues"
6. ⏸️ 是否启动 v0.3 重写**等 user 决策**

### 第 6 次 trap memory 教训

**本 session 实例**：AI autonomous "立项 → 数值 + ledger 同步 → C3 评审" **完整闭环**，但**仍在 statement-only spec 文档里 smuggling structural gap closure**：
- "Justification sketch" 包装下的 proof closure
- 综合包含链写成无条件 [SYN] 而非 conditional
- 11-gap inventory 被压成 4-gap
- 旧 scaffolding 警告完全脱节

**dev-reviewer 双 Codex 是有效 C3 闸门**（双 reviewer 独立给出 REJECTED + UNSOUND，互相验证）。但**autonomous workflow 在 framework intent 层仍需 user 显式 review** 才能避免 statement-only 文档里的 silent upgrade。

## Round 2 — 2026-04-25 (post-user-directive)

User directive 2026-04-25 (PHASE_STATUS §4.5) 反转 Log 07 优先级，user 理由："我手头时间紧迫，γ 估计需要更长精读周期，先看 α 能否在更短周期出 scaling-级结论"。

启动 v0.3 重写 + round 2 dev-reviewer。

### Diff reviewer round 2 (gpt-5.4, xhigh)

**Verdict**: **REJECTED** (1 major + 1 minor)

Trap fix verification（7 个 round-1 trap）:
| Trap | Round 2 status |
|---|---|
| T1 partial-trace closure | ✅ FIXED |
| T2 Justification sketch | ✅ FIXED |
| T3 综合链 conditional | ✅ FIXED |
| T4 数值 confirm | ✅ FIXED (replaced with "is consistent with finite grid") |
| T5 ledger 一致性 | ❌ **NOT FIXED** (path δ banner 残留 + §6.1 与 patch 范围不符) |
| T6 short timetable | ✅ FIXED |
| T7 priority reversal user-driven | ✅ FIXED |

Remaining issues:
- **MAJOR** [umr_path_alpha_three_lemma_v0_3.md:99 + path_δ banner](../../proofs/umr_path_delta_relaxed_trust_v0_1.md): T5 仍未修；path δ banner 仍指向 v0.2 + 留有 "α 真正绕开 β.G4" 等 v0.3 disavow 的 framing
- **MINOR** [umr_path_alpha_three_lemma_v0_3.md:169](../../proofs/umr_path_alpha_three_lemma_v0_3.md): §3.1 mapping L1.G3 / L1.G4 未在 v0.2 4-gap 中有 antecedent 说明

**Reviewer 显式援引 §7.3**："Under the user's stated red lines, that keeps round 2 at REJECTED and triggers the §7.3 rollback condition."

### Holistic reviewer round 2 (gpt-5.4, high)

**Verdict**: **FAIL** (round 3 needed)

Issues:
- **MAJOR** "user-directive-approved" 措辞 (§-1.3 / §1) 与 §-1.4 directive boundary 矛盾 (smuggle approval)
- **MAJOR** 11-gap inventory 不是"完整恢复" — v0.3 加了 qualifiers / examples / trap annotations
- **MAJOR** PHASE_STATUS §4.5 反转优先级，但 §5.1 queue 仍以 β.G4 为"最高优先级"（repo-level inconsistency）
- **PARTIAL FAIL** §-1.4 verbatim 引用：user reason 部分 verbatim 准确，但 directive scope 是 project transcription 不是 verbatim
- **PARTIAL FAIL** §7.3 rollback 条件 "同型陷阱" 触发器过宽

### §7.3 Rollback 触发

按 v0.3 §7.3 rule:
> "v0.3 dev-reviewer round 2 再 REJECTED → user-directive 失效，回到 Log 07 γ-first 顺序"

**Round 2 diff verdict = REJECTED**, 触发 rollback。

### Rollback action

立即执行：

1. ✅ [umr_path_alpha_three_lemma_v0_3.md](../../proofs/umr_path_alpha_three_lemma_v0_3.md) 顶部加 [REJECTED round 2 — §7.3 ROLLBACK 触发] banner，列 5 个 remaining issues
2. ✅ [PHASE_STATUS.md §4.5](../../PHASE_STATUS.md) 标 [ROLLED BACK 2026-04-25] + §5 queue 顺序声明回到 Log 07 γ-first
3. ✅ [FINDINGS.md §4.3](../../research/FINDINGS.md) 改写为 [ROLLED BACK 2026-04-25 — v0.2 + v0.3 双 round REJECTED]，保留 v0.2 历史记录为 §4.3.bak
4. ⏸️  **不**进入 round 3 — per §7.3 rule + user 自设的 rollback condition
5. ⏸️ user override 选项保留：可显式 authorize round 3 快速修补 5 个 cleanup issue (≤ 30 min wallclock)

### 第 6 次 trap memory 更新

本次 round 2 是个 mixed signal:
- **6/7 trap substantively 修好** —— 显示 v0.3 在结构 rigor 上有真实进展
- **T5 ledger 一致性 + 新发现 cross-document banner 残留** —— autonomous workflow 的盲点：单文档严谨不代表 repo-level 一致

教训：autonomous session 写新文档时，**必须 sweep 所有 cross-reference banner 与 ledger 是否同步**。本次 path δ banner 仍指 v0.2 + 留 v0.3 disavow 的"绕开 β.G4" framing，是经典的 stale cross-reference。

### Round 3 cleanup (post-user-override 2026-04-25)

**User override**（autonomous session 同回合）："如果和红线违背，那就以我的 approve 为准 ... 我已经经过反复论证了，我的 approve 没问题"

**Override scope 严格界定**：
- ✅ approve direction + v0.3 维持 active draft
- ❌ **不**等价 C3 PASS（C3 verdict 留痕 REJECTED）
- ❌ **不**等价 [SYN] → [COROLLARY] 升级
- ❌ **不**得对外引用为定理级

**Round 3 cleanup actions** (5 个 round 2 issues，全部 ≤ 30 min wallclock，无新 round 3 dev-reviewer)：

1. ✅ [v0.3](../../proofs/umr_path_alpha_three_lemma_v0_3.md) 顶部 banner: [REJECTED round 2] → [USER-APPROVED PRIORITY 2026-04-25, NOT C3-passed]，明列 override scope + R0.2 硬红线维持
2. ✅ [v0.3 §-1.3 + §1](../../proofs/umr_path_alpha_three_lemma_v0_3.md): "user-directive-approved" → "for the user-directed path α workstream"（Codex round 2 holistic major #1）
3. ✅ [v0.3 §3](../../proofs/umr_path_alpha_three_lemma_v0_3.md): label 改 "annotated restoration of scaffolding v0.1 §5"，说明 qualifiers 是 annotation 不是 substance change（Codex round 2 holistic major #2）
4. ✅ [v0.3 §3.1](../../proofs/umr_path_alpha_three_lemma_v0_3.md): mapping 加 L1.G3 / L1.G4 "无 v0.2 antecedent，从 scaffolding v0.1 直接 restore" 说明（Codex round 2 minor）
5. ✅ [v0.3 §6.1](../../proofs/umr_path_alpha_three_lemma_v0_3.md): 改"累积 ledger" label，列全部 6 个修改文件（Codex round 2 critical T5）
6. ✅ [v0.3 §7.3](../../proofs/umr_path_alpha_three_lemma_v0_3.md): rollback trigger 改 operationalized T-7.3.1/2/3/4，删"同型陷阱"过宽措辞（Codex round 2 minor）
7. ✅ [path δ banner](../../proofs/umr_path_delta_relaxed_trust_v0_1.md): 指向 v0.3 + 删 "α 真正绕开 β.G4" 等 v0.3 disavow 的 framing（Codex round 2 critical T5）
8. ✅ [PHASE_STATUS §4.5](../../PHASE_STATUS.md): ROLLED BACK → USER-APPROVED PRIORITY (override §7.3)
9. ✅ [PHASE_STATUS §5.1](../../PHASE_STATUS.md): queue 顺序 path α first（Codex round 2 holistic major #3 — repo-level consistency）
10. ✅ [FINDINGS §4.3](../../research/FINDINGS.md): ROLLED BACK → USER-APPROVED PRIORITY，记录 user override scope + 诚实风险记录

### Final Status (post-user-override): **path α 维持 USER-APPROVED PRIORITY**

**永久留痕**：
- v0.2 [REJECTED round 1]: critical + 3 major + UNSOUND
- v0.3 [REJECTED round 2]: 1 major + 1 minor + FAIL（6/7 round-1 trap 已修）
- v0.3 [USER-APPROVED PRIORITY post-override]: cleanup-level issues 已修，C3 verdict 仍 REJECTED 留痕
- user override 性质：direction-level only，非 C3 PASS，非升级

**总耗时**: round 1 ~15 min + round 2 ~20 min + round-3 cleanup ~30 min = ~65 min wallclock
**测试**: N/A
**风险记录**: user override Codex C3 verdict 在 spec 文档层为**首次先例**。后续 v0.3 衍生材料若触发 T-7.3.1/2/3 → 按 retraction 流程处理，**override 失效**。

**下一步**: user 可启动 path α 三 lemma 11 sub-gap 的 paper-level work（Pirandola 2019 §III-IV / Khatri-Wilde §19-20 / Lucamarini 2018 / Wang 2019 / Curras-Lorenzo 2021 / Portmann-Renner 2022 直读 + 形式化）。任何 [SYN] → [COROLLARY] 升级仍需 R0.2 (C1 ∧ C2 ∧ C3) 完整流程。

---

## Round 3 + Round 4 — 2026-04-26 (continuation session)

### 触发：user 直读 PDF 后授权三件事

User message 2026-04-26: "1、前者；2、这是要提交codex审核吗，那提交吧；3、启动" 对应：
1. user 已直读 Pirandola SI Note 1 + Cui 2019 原文 → §7.x.1 标 C1(b) cross-reference candidate evidence
2. submit dev-reviewer round 3
3. launch C1(a) cross-family AI direct-PDF verification

### Changeset (v3)

`docs/proofs/umr_path_alpha_lemma_skeletons_v0_1.md` 新增 §7.x append（user verification 响应记录 + Curty-Azuma-Lo 2018 PDF 11 页 Claude 直读 + Cui Eq. (3) recheck）。

### Round 3 — 2026-04-26 10:53 (3 reviewers in parallel)

#### Diff reviewer (gpt-5.4, xhigh) — verdict: **FAIL** (2 majors)
1. major correctness: §7.x.1 "C2 已满足" 越权（direction-level approval ≠ C2 升级闸门满足）
2. major correctness: §7.x.2 5.5 "直接支持 Lemma A protocol embedding 的合法性" 在 untrusted-Charlie picture 内部 smuggle cross-space bridge

#### Holistic reviewer (gpt-5.4, high) — verdict: **FAIL** (concurring + 1 minor)
- Convergent on diff issues (C2 over-claim + Curty wording drift)
- New minor: §7.x.5 placeholder 引用但 section 不存在
- All R0.1/R0.2/R0.3 红线 + 5th/6th trap memory PASS

#### C1(a) cross-family direct-PDF verification (gpt-5.4 xhigh, Codex 直读 PDF via pdftotext) — verdict: **PARTIAL**
- 5 PASS (1, 2, 3, 5, 7) / 2 FAIL (4, 8) / 1 UNCERTAIN (6)
- **Substantive divergence**：points 4 + 8（ε-composable / private-state 等价性）—— Codex 直读 Cui 原文**未** find explicit ε / composable / trace-norm / private-state criterion. User "是" / "等价" 判断与 Codex 直读结果分歧；recommendation 是追加 primary citation（Portmann-Renner 2022 / Tomamichel 2016）explicitly bridge
- Point 6 UNCERTAIN: KW Ch 20 §20.2 PDF unavailable
- Point 7 PASS but with caveat: Pirandola 实际语言 "per chain use"（非 "per bottleneck-link use"）— Claude 之前的措辞是 inference

### Round 3 fixes (applied 2026-04-26 10:55-11:00)

1. ✅ §7.x.1: "C2 已满足" → "C2-relevant evidence, NOT gate-satisfied"; "可标 C1(b) PASS" → "C1(b) cross-reference candidate evidence only"
2. ✅ §7.x.2 5.5: 改写为严格 untrusted-Charlie picture 内部，明示 Curty 2018 **不**走 Π → ι(Π) = Π_tr 嵌入，**不**支持 Lemma A 嵌入合法性
3. ✅ §7.x.3: "per bottleneck-link use" 替换为 "per chain use"（per C1(a) Codex finding：Pirandola SI Note 1 实际语言）
4. ✅ §7.x.5 实际写入：所有 3 reviewer verdicts + divergence 诚实记录

### Round 4 — 2026-04-26 11:00 (verification of fixes)

#### Diff reviewer (gpt-5.4, xhigh) — verdict: **PASS**
- "Round 3 fixes are present and correctly scoped"
- Empty issues array
- "round_recommendation: None - ready to commit"

#### Holistic reviewer (gpt-5.4, high) — verdict: **PASS**
- All 3 Round 3 fix items PASS
- C1(a) integration PASS（per chain use language adopted; PARTIAL verdict honestly recorded; recommendations preserved）
- Architecture / Prospectus / R0.1-R0.3 / trap memory / phase status / completeness 全部 PASS
- "review-pass on the fixes, not an upgrade-pass under R0.2"
- Document still correctly says upgrade path remains closed pending full C1 ∧ C2 ∧ C3

### Final Status (continuation session C3 cycle)

**Round 3 → Round 4 转换**: REJECTED → FAIL → PASS（2 rounds）

**C3 gate 状态**: 
- Round 3 dev-reviewer FAIL 留痕（2 majors: C2 over-claim + Curty 5.5 cross-space smuggle）
- Round 3 fixes applied + verified clean by Round 4 PASS
- Round 4 dev-reviewer **PASS** = C3 gate **satisfied** for the §7.x append baseline

**C1(a) gate 状态**: **PARTIAL** (5/8) — **NOT** satisfied
- Substantive divergence at points 4, 8 (ε-composable definition not in Cui original text)
- Point 6 KW Ch 20 unavailable
- Recommendation: add primary citation for ε-composable security mapping

**C1(b) gate 状态**: cross-reference candidate evidence (8 textual alignment checks 层面)，**NOT** sub-gap closure 层面 PASS
- User direct PDF read confirmed 2026-04-26
- 远不够 sub-gap closure-level pen-and-paper formalization

**C2 gate 状态**: direction-level approval（USER-APPROVED PRIORITY 2026-04-25）—— **NOT** itemized lemma-statement signoff
- User has not separately signed off on §3-§5 specific lemma statements/scope/grading

**11 sub-gaps**: **全部维持 [UNKNOWN]**

**升级 path α 是否开通**: **NO**（C1(a) PARTIAL + C1(b) 仅 cross-reference 层面 + C2 仅 direction-level）

**总耗时**: Round 3 + 4 ≈ 25 min wallclock（3 parallel agents + 1 fix cycle + 2 parallel verifying agents）

**风险记录**: 
- 用户 "是" 判断（点 4, 8）与 Codex 直读 Cui 原文 textually 分歧 — 需 user 决定是否（a）追加 primary citation 补 explicit ε-composable bridge；（b）维持当前 cross-reference candidate evidence status；（c）撤回 "是" 判断
- 此分歧**不**自动触发 retraction，但**必须**显式记录（已在 §7.x.5 完成）

**下一步**: user 决定如何处理 C1(a) 分歧的 3 选项；同时 11 sub-gap closure 的 paper-level work 仍待启动。

---

### Round 5 — 2026-04-26 user 处置 + 点 6 retest

**用户决定**（message 2026-04-26 后续）：
- 点 4：选项 B（接受 Cui 原文未 explicit 的 ε-composable bridge 作为 implicit Devetak-Winter framework 内部假设）
- 点 4 reviewer directive：未来 Codex 评审**不**应再以 "Cui 原文无 explicit composable security textual support" 为由把点 4 列为 issue（与 v0.3 §7.3 USER-APPROVED PRIORITY 同性质 user-issued reviewer scope 限制）
- 点 6：按 Claude plan 执行 — 下载 KW arXiv preprint 让 Codex 重测

**执行：**
1. ✅ 下载 [Khatri-Wilde arXiv:2011.04672 preprint](../../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)（1240 页 *Principles of Quantum Communication Theory*）
2. ✅ 启动 Codex point-6-retest（背景任务 b733j11qk，xhigh reasoning）
3. ✅ 完成 retest verdict — see [c1a-codex-pdf-verification-point6-retest.md](c1a-codex-pdf-verification-point6-retest.md)

**Round 5 retest verdict — UNCERTAIN narrowed**：
- ✅ **6(i) SKA ↔ private-state distillation purification equivalence textually present in KW §20.2**：Codex 引 KW PDF p.1184 / p.1188 verbatim 三处 confirm
- ❌ **6(ii) Cui Eve 模型适配 NOT settled by §20.2 alone**：KW SKA framework 用 single-channel $\mathcal{N}_{A\to B}$ + LOPC，§20.2.4 generalize 到 public separable channels，**未** cover Cui-style untrusted-relay arbitrary 联合 unitary topology

**与 path α sub-gap inventory 的对应**：

Codex 指出"需 extra embedding/reduction argument beyond KW §20.2"正好是 **L1.G2** (Lemma A 嵌入 $\iota$ 具体构造) 这一 sub-gap 的 substantive content —— path α 11 sub-gap inventory 在 textual evidence 上获得 independent 验证（L1.G2 是 substantive 而非 redundant）。

**对 sub-gap 状态**：**11 sub-gaps 仍全部 [UNKNOWN]**。L1.G2 的 [UNKNOWN] 被 KW retest **independently 确认 substantive**。

**对 C1(a) gate 状态**：仍 PARTIAL（5 PASS + 1 user-accepted Option B + 1 narrowed-UNCERTAIN + 1 FAIL）—— **未**满足 C1 完整性

**Round 3-5 总耗时**: ~50 min wallclock（4 parallel Codex agents in 3 rounds + 1 fix cycle + 1 KW download + 1 retest + 多次 doc 更新）

**最终 path α 状态**（2026-04-26 cycle close）：[USER-APPROVED PRIORITY direction, Round 4 C3-passed, NOT upgrade-eligible] —— C1(a) 5/8 textually + Option B（点 4）+ 点 6 narrowed + 点 8 FAIL；C1(b) cross-reference 层；C2 direction-level；C3 PASS。**11 sub-gaps 全部 [UNKNOWN] 维持**。
