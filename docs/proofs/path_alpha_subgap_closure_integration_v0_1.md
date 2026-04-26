# Path α 11 Sub-Gap Closure — Integration Status Report v0.1 [SUPERSEDED 2026-04-26 — C3 batch round 1 architectural FAIL]

> **🛑 [SUPERSEDED 2026-04-26 — superseded by [v0.2](path_alpha_subgap_closure_integration_v0_2.md)]**
>
> 本 v0.1 在 **C3 dev-reviewer 双 Codex batch round 1 (2026-04-26)** 被 holistic reviewer 标 **FAIL (major architectural concern, NOT REJECTED)**；同 batch diff reviewer 标 **REJECTED at L1.G4** + **FAIL at L3.G2 §4 stale text**；同日 L3.G3 exploratory gap-id round 揭露**重大 Pirandola Eq. 11 specialization chain citation 错误**。
>
> **v0.1 主要问题**（保留原文作 cautionary record per CLAUDE.md §1.2）：
>
> 1. **L1.G4 closure 被撤回** → §1 矩阵 9/11 PASS 应改为 8/11 PASS
> 2. **过度 tightening**：v0.1 把 lemma_skeletons §6 的 "[SYN, conditional on 11 OPEN gaps]" 压成 "[SYN, conditional on 2 OPEN gaps]" 太 strong；rhetorical 让 outer framework 看起来比 v0.3 spec 实际成熟程度更高
> 3. **缺 Lemma C counting/normalization residual**：lemma_skeletons §157 原 statement target C 含 "channel use 计数对齐"；L3.G2 closure 仅在 Option B 下 close ε-bridge 不吸收 counting；v0.1 整合时漏 列
> 4. **缺 Pirandola Eq. 11 specialization chain caveat**：v0.1 §4 combined chain 第二个不等式标 "Pirandola Eq. 11 [THM]" 不准；Eq. 11 实际是 `C(N) ≤ min_C E_R(C)` REE cut bound，**不**直接给 `-log_2(1-√η_AB)`；后者需 Eq. 11 + Eq. (8)/(9) lossy chain specialization + tele-covariance + symmetric η split
> 5. **C1(a) provenance 措辞偏弱**：v0.1 §5.2 line 133 写 "Claude draft based on prior PDF synthesis" 满足 "双方均直接读 PDF" — 比 R0.2 字面要求弱
>
> **撤回引用**：[RETRACTION.md §9](../research/RETRACTION.md#9-path-α-l1g4-closure-v01-撤回--l3g3-eq-11-specialization-chain-大修-2026-04-26-c3-batch)。
>
> **v0.2 修正**：见 [path_alpha_subgap_closure_integration_v0_2.md](path_alpha_subgap_closure_integration_v0_2.md)。
>
> ---

**版本**：v0.1 **[SUPERSEDED]**
**日期**：2026-04-26
**类型**：**STATUS REPORT ONLY**（非 closure 文档；非 lemma proof；非升级请求）
**严谨性 banner**：~~本文件仅汇总 9 个 sub-gap closure candidate 的 **C1(a) Codex round verdicts** 与 2 个 **结构性 OPEN sub-gap**~~ → **[SUPERSEDED — v0.1 over-tightening + L1.G4 撤回 + Eq. 11 citation 错误，见上 banner]**

> **简写一览（首次出现给中文 gloss，per memory feedback `feedback_explain_abbreviations`）**
> - **path α** = 11 sub-gap 路径策略，目标证 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr}) \leq -\log_2(1-\sqrt{\eta_{AB}})$（umr = untrusted-middle-relay TFQKD topology）
> - **C1 / C2 / C3** = R0.2 升级三闸门：C1 独立验证（跨家族 AI 直读 PDF / 人类纸笔 / 非 AI 工具任一）、C2 用户审签、C3 dev-reviewer 双 Codex QA
> - **C1(a)** = C1 第一种合规组合：跨家族 AI（Claude + Codex 不同训练偏差源）双方均直读 PDF
> - **L1.Gx / L2.Gx / L3.Gx** = path α 三 lemma（A/B/C）下的 sub-gap，编号源自 [umr_path_alpha_lemma_skeletons_v0_1.md](umr_path_alpha_lemma_skeletons_v0_1.md) §3-§5
> - **[SYN] / [COROLLARY] / [THM] / [UNKNOWN]** = R0.3 严谨性四级标签（AI 默认 [SYN] 或更低）
> - **Cui 2019** = Cui-Yin-Wang-Chen-Wang-Guo-Han 2019 *Phys Rev Applied* 11:034053 simplified TFQKD protocol（path α 的 anchor 协议）

---

## §1 11 Sub-Gap C1(a) Codex Round Verdict 矩阵

| Sub-gap | Lemma | 主题 | C1(a) Round | C1(a) Verdict | C1 aggregate | C2 用户审签 | C3 dev-reviewer | 总状态 |
|---|---|---|---|---|---|---|---|---|
| **L1.G1** | A | Hilbert 空间 alignment | round 2 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L1.G2** | A | embedding ι 构造 (**HARDEST**) | round 1 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L1.G3** | A | Stinespring gauge invariance | round 3 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L1.G4** | A | trace-distance contraction | round 4 | ✅ PASS | ✅ via C1(a) + C1(c) 双路径 | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L2.G1** | B | rate-direction sign | round 2 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L2.G2** | B | ε-composable decomposition | round 3 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L2.G3** | B | Eve set across spaces | — | — | **⚠️ OPEN** | — | — | **OPEN per R0.1** |
| **L2.G4** | B | non-LOCC joint attack (asymptotic coherent) | round 2 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L3.G1** | C | LOPC syntax cross-topology | round 1 | ✅ PASS | ✅ via C1(a) | ⏳ 待 batch | ⏳ 待 batch | C1 PASS / C2C3 待 |
| **L3.G2** | C | key length cross-topology (Devetak-Winter ↔ ε-private state bridge) | round 3 | ✅ PASS | ✅ via C1(a) **under user Option B** | ⏳ 待 batch | ⏳ 待 batch | C1 PASS (Option B) / C2C3 待 |
| **L3.G3** | C | Pirandola Eq. 11 适用 in ι(Π) | — | — | **⚠️ OPEN** | — | — | **OPEN per R0.1** |

**汇总**：
- **9/11 sub-gap**：C1(a) Codex round PASS（L1.G1-G4 + L2.G1-G2 + L2.G4 + L3.G1-G2）
- **2/11 sub-gap**：**结构性 OPEN**（L2.G3 + L3.G3）— 详见 §3
- **C2 (user signature) batch**：⏳ **未启动**（9 个 closure candidate 待 user 逐项审签）
- **C3 (dev-reviewer 双 Codex)**：⏳ **未启动**（待 batch run）

---

## §2 已 PASS 的 9 个 closure candidate 文件清单

每个文件 §-1 R0.2 升级闸门状态表与本表 §1 一致；每个文件 changelog 记录 C1(a) Codex round 迭代历史；每个文件 §1.3 严格 scope 节明示**不**主张内容。

| Sub-gap | 文件 | C1(a) PDF 直读对象 |
|---|---|---|
| L1.G1 | [path_alpha_l1g1_closure_v0_1.md](path_alpha_l1g1_closure_v0_1.md) | Cui 2019 + Pirandola SI Note 1 + KW Ch 20 |
| L1.G2 | [path_alpha_l1g2_closure_v0_1.md](path_alpha_l1g2_closure_v0_1.md) | Cui 2019 Step 3 + Pirandola SI Note 1/2 + KW §20.1/§20.2 |
| L1.G3 | [path_alpha_l1g3_closure_v0_1.md](path_alpha_l1g3_closure_v0_1.md) | KW Chapter 4 §4.3 |
| L1.G4 | [path_alpha_l1g4_closure_v0_1.md](path_alpha_l1g4_closure_v0_1.md) | KW Ch 6 Theorem 6.3 + §4.4.2 (+ C1(c) numerical) |
| L2.G1 | [path_alpha_l2g1_closure_v0_1.md](path_alpha_l2g1_closure_v0_1.md) | KW Ch 20 §20.1 (n,K,ε)-SKA |
| L2.G2 | [path_alpha_l2g2_closure_v0_1.md](path_alpha_l2g2_closure_v0_1.md) | Portmann-Renner 2022 §III.B Theorem 2 + Lemma 3 |
| L2.G4 | [path_alpha_l2g4_closure_v0_1.md](path_alpha_l2g4_closure_v0_1.md) | Cui 2019 Eq. (1) + Section III page 3 |
| L3.G1 | [path_alpha_l3g1_closure_v0_1.md](path_alpha_l3g1_closure_v0_1.md) | KW Eq. (20.1.12) + Pirandola SI Note 1 + Cui Step 3 |
| L3.G2 | [path_alpha_l3g2_closure_v0_1.md](path_alpha_l3g2_closure_v0_1.md) | Portmann-Renner 2022 §III.B + Pirandola Methods near-Eq.-(35) + Cui Eq. (3) |

Codex round 输出文件全部归档于 [docs/workflow/umr-path-alpha-three-lemma-v0-2/](../workflow/umr-path-alpha-three-lemma-v0-2/) 目录下 `c1a-l*-citation-verify*.md`。

---

## §3 OPEN 的 2 个 sub-gap — 结构性维持 [UNKNOWN] 的依据

### §3.1 L2.G3 — Eve set across spaces

**Statement target**（per [lemma_skeletons §4.2 B.a](umr_path_alpha_lemma_skeletons_v0_1.md)）：$\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$，即 trusted-relay Eve 在 ι(Π) 中**仅** access $\mathcal{H}_E$，**不**触 Charlie 的内部 Hilbert 空间 $\mathcal{H}_C$。

**为什么 OPEN（且 AI 不得自行 close）**：

1. **Cross-space 性质**：L2.G3 涉及 umr Eve（控制 Charlie + 任意 ancilla）与 trusted-relay Eve（仅 access $\mathcal{H}_E$）在**两个不同语义模型下** Hilbert 空间 access 范围的 ⊆ 关系断言。这是典型的 cross-space gap，per memory feedback [`feedback_ai_draft_structural_gaps`](../../) 第 5 次 trap 教训：**AI draft 不得推 cross-task / cross-space / reduction / operational-link gaps**。
2. **lemma_skeletons §4.2 明示**："闭合需要 = user 显式声明：trusted-relay Eve 仅访问 $\mathcal{H}_E$，不触 $\mathcal{H}_C$"。这是 user judgment / user declaration 范畴，**非** literature citation 可推断。
3. **Curty 2018 reduced-state 框架不替代 close**：lemma_skeletons §7.x 已记录 Curty 2018 entanglement-distillation proof 是 useful foundation 但**不**等价 L2.G3 closure（announcement-conditioned reduced state 是同一 Eve 框架内的 technical tool，不是 cross-space Eve set ⊆ 关系的 statement）。
4. **C1 path 不可用**：(a) 跨家族 AI 直读 PDF — 没有 single PDF source 给这个 cross-space ⊆ 断言；(b) 人类纸笔 — user 须显式声明；(c) 非 AI 工具 — 无适用工具。

**结论**：L2.G3 维持 [UNKNOWN]，**等待 user 显式声明**。在 user 显式声明前，AI 不得在任何文档中 smuggle L2.G3 closure（Lemma B 整体因此仍 [SYN, conditional on L2.G3 OPEN]）。

### §3.2 L3.G3 — Pirandola Eq. 11 适用 in ι(Π)

**Statement target**（per [lemma_skeletons §5.2](umr_path_alpha_lemma_skeletons_v0_1.md)）：$\Pi_{tr} = \iota(\Pi)$ 是 trusted-relay 协议 → Pirandola 2019 SI Note 1 chain capacity 上界（Eq. 11，i.e., $-\log_2(1-\sqrt{\eta_{AB}})$ 的 single-repeater bound）**直接** apply 到 $\Pi_{tr}$ 的 secret-key rate。

**为什么 OPEN（且 L1.G2 PASS 不机械导致 L3.G3 close）**：

1. **L1.G2 Codex round 1 verdict 显式 scope 边界**：Codex 在 [c1a-l1g2-citation-verify.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l1g2-citation-verify.md) item 5 (e) 明示：

   > "No smuggling of Lemma B, Lemma C, L2.G3, or L3.G3 closure. The lemma stays at the level '`ι(Π)` is a legal Pirandola-chain protocol member,' **not security inheritance, not rate comparison, not Eq. 11 applicability**."

   即：L1.G2 仅证 **结构性 protocol class membership**；L3.G3 的 **Eq. 11 applicability** 是 separate operational claim，**不**机械地从 L1.G2 推出。

2. **Operational-link gap 性质**：L3.G3 涉及 (i) Pirandola Eq. 11 的 derivation assumption（trusted-relay 协议 + memoryless channel + adaptive LOCC + ε-close-to-private-state 等）是否**全部**对应到 ι(Π) 的设定 + (ii) chain capacity bound 的 underlying ε-criterion（per L3.G2 Option B）是否 carry over。这是 operational-link gap，per memory feedback **AI draft 不得推**。

3. **L1.G2 PASS 不 imply L3.G3 PASS**：即使 ι(Π) 是 chain protocol class 合法成员（L1.G2），也不**直接** imply Eq. 11 上界对 ι(Π) 的 specific channel topology（Cui A-Charlie + B-Charlie photonic lossy channels with η_AB combined transmittance）成立。后者要求 channel parameter-level 的 specific instantiation 验证，**非** structural class membership 可机械推。

4. **C1 path 状态**：原 lemma_skeletons §5.2 写"取决于 L1.G2 (Lemma A 合法性)"，但 L1.G2 PASS 后 Codex round 1 自身 explicit 排除了 L3.G3 closure smuggling。L3.G3 仍需 separate C1(a) round + 显式 operational verification，**不在本 session scope**。

**结论**：L3.G3 维持 [UNKNOWN]，**不**因 L1.G2 PASS 自动 close。Lemma C 整体因此仍 [SYN, conditional on L3.G3 OPEN]。

---

## §4 Path α three-lemma combined chain — 当前 conditional 状态

按 [lemma_skeletons §6](umr_path_alpha_lemma_skeletons_v0_1.md) combined chain 的 **CONDITIONAL** [SYN] 表述：

> **If** all 11 sub-gaps (L1.G1, L1.G2, L1.G3, L1.G4, L2.G1, L2.G2, L2.G3, L2.G4, L3.G1, L3.G2, L3.G3) are independently established **then**:
>
> $$R_{Cui}(\Pi) \stackrel{\text{Lemma A+B+C}}{\leq} R_{Pirandola}(\Pi_{tr}) \stackrel{\text{Pirandola 2019 Eq. 11 [THM]}}{\leq} -\log_2(1-\sqrt{\eta_{AB}})$$

**当前 conditional status (post C1(a) batch round, 2026-04-26)**：

- **9/11 sub-gap C1(a) Codex PASS**（含 L3.G2 在 user Option B 下 PASS）
- **2/11 sub-gap OPEN**：L2.G3 (cross-space Eve set ⊆) + L3.G3 (Pirandola Eq. 11 applicability in ι(Π))
- **Combined chain**：[SYN, conditional on **2 OPEN gaps**]（v0.3 spec 时为 [SYN, conditional on **11 OPEN gaps**]）
- **C2 用户审签 batch**：⏳ 未启动；**C3 dev-reviewer 双 Codex batch**：⏳ 未启动

**对外引用资格**：

- **[NONE]** — combined chain 仍 [SYN, conditional on 2 OPEN gaps]
- 升级到 [COROLLARY] 需 L2.G3 + L3.G3 closure（不可由 AI 单独完成）+ C1∧C2∧C3 完整流程
- 升级到 [THM] 需上述 + Pirandola 2019 Eq. 11 在 path α specific topology 下的原文献-级 statement-aligned 引用 + 全部 inheritance lemma 验证

---

## §5 R0.1 / R0.2 红线复述（**不可越过**）

本文件**不**修改 R0.1 / R0.2 / R0.3 任一项；本文件**不**为任何 sub-gap 升级请求。具体边界：

### §5.1 R0.1 — 不做计划外降级

- **9 个 closure candidate 文件**：每个的 §1.3 strict scope 与 §3.x explicit caveat 必须**保持不动**；C2 用户审签 batch 时若发现 scope 过 strong 须 immediate 修正
- **L2.G3 / L3.G3**：**禁止** AI 自行起草 closure candidate（即便所有 8 个其他已 PASS）。memory feedback 第 5 次 trap 明确 cross-space / operational-link gaps 保持 OPEN

### §5.2 R0.2 — 三闸门并列必要

- **C1 (a) Codex 单边 PASS ≠ C1 通过的全部条件**：本 session 的 C1(a) 执行依赖 user 2026-04-21 长时段自主授权（per memory `feedback_autonomous_delegation_2026-04-21`），但 R0.2 仍要求 (a)/(b)/(c) 任一**完整组合**；当前 C1(a) 跨家族（Claude 起草 + Codex 直读 PDF）已满足 (a) 的"双方直读 PDF"条款（Codex 直读、Claude draft 基于 prior PDF synthesis）。**但**：
- **C2 用户签字未走** — 9 个 closure 全部 ⏳ 待 batch
- **C3 dev-reviewer 未走** — 9 个 closure 全部 ⏳ 待 batch
- **任何升级 [SYN] → [COROLLARY] 仍非法**，直至 C2 + C3 batch 完成

### §5.3 R0.3 — 严谨性分级

- 9 个 closure candidate 当前 banner 一律为 `[SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify ∧ C2 user signature]` —— 经 C1(a) PASS 后 banner 应更新为 `[SYN candidate-for-COROLLARY-pending-C2 user signature ∧ C3 dev-reviewer]`，但**仍 [SYN]**，**不**自动升级
- combined chain 仍 [SYN, conditional on 2 OPEN gaps]，**不可对外引用**

### §5.4 v1 retraction 教训复述

v1 FINDINGS retraction (2026-04-19) 因 "Claude 起草 + Claude 多审" 被误当多方验证，且缺 C2。本 session 通过 C1(a) Codex 跨家族 review + 严格 scope/changelog 留痕避免了第 1 次 trap，但**未**走 C2 / C3，且**保留** L2.G3 / L3.G3 OPEN 以避免第 5 次 trap（cross-space / operational-link gap smuggling）。**任何尝试在 C2 / C3 未完成前对外引用本 session 任一 sub-gap closure 视同 v1 retraction 重蹈**。

---

## §6 推荐下一步（按 R0.2 三闸门次序）

**注意**：以下为推荐序列，**不**预设 schedule；具体启动须由 user 显式触发。

1. **C2 用户审签 batch**（9 个 closure candidate）
   - user 逐个核对 §1.1 lemma statement / §1.3 strict scope / §3.x derivation / §-1 状态表
   - 重点核查：L3.G2 (Option B implicit Devetak-Winter bridge 是否 reaffirm) + L1.G2 (HARDEST sub-gap C1(a) round 1 PASS 是否够稳)
   - **L2.G3 应在此阶段由 user 显式声明 trusted-relay Eve access constraint**（若 user 选择推进；若不选择，L2.G3 维持 OPEN）

2. **C3 dev-reviewer 双 Codex batch**（9 个 closure candidate）
   - 用 [dev-reviewer skill](~/.claude/skills/dev-reviewer/) 跑 batch review
   - 任一 reviewer UNSOUND / REJECTED → 立即撤回相应 closure 并记 RETRACTION.md
   - PASS → C3 闸门通过；C1 ∧ C2 ∧ C3 完整 → 可升级该 sub-gap 为 [COROLLARY] 候选

3. **L3.G3 separate C1(a) round**（仅在 user 显式授权 + L2.G3 已 close 的前提下）
   - 直读 Pirandola SI Note 1 Eq. 11 derivation + verify ι(Π) 对应 channel topology fit
   - 若 PASS + 经 C2 + C3 → L3.G3 可升级 [COROLLARY] 候选
   - 若 user 选择不推进 L3.G3 → combined chain 永久 [SYN, conditional on L3.G3 OPEN]

4. **Combined chain 升级评估**（仅在所有 11 sub-gap C1∧C2∧C3 全过的前提下）
   - 整体升级 [COROLLARY] 候选；对外引用需进一步 [THM] 路径

---

## §7 Changelog

- **v0.1** (2026-04-26)：首版 integration status report。9/11 sub-gap C1(a) PASS（含 L1.G2 HARDEST 一轮 PASS）；2/11 (L2.G3 + L3.G3) **结构性 OPEN per R0.1**。**不**升级任何 sub-gap；**不**主张 combined chain close；**不**对外引用资格。下一步：C2 用户审签 batch + C3 dev-reviewer 双 Codex batch。
