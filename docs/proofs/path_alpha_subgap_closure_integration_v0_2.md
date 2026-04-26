# Path α 11 Sub-Gap Closure — Integration Status Report v0.2 [SUPERSEDED 2026-04-26 by v0.3]

> **🛑 [SUPERSEDED 2026-04-26 — superseded by [v0.3](path_alpha_subgap_closure_integration_v0_3.md)]**
>
> v0.2 是 R1 post-fix 即时版本，但 **C3 R2 holistic finding** 揭露 v0.2 与本 session later 状态不再 coherent：
> - L3.G2.E **已立项 + C1(a) PASS**（v0.2 没把 L3.G2.E 入主矩阵）
> - L1.G4 v0.2 **已重写 + C1(a) PASS**（v0.2 仍标 [RETRACTED]）
> - L3.G2 v0.5 final **已 C3 R3 PASS**（v0.2 仍标 R2 待）
> - "Lemma C counting residual" 独立 bucket **已被 L3.G2.E 吸收**，应删除
> - **post-split L3.G3 = 5 sub-residual**（v0.2 仍说 6）
>
> **保留 v0.2 原文**作 audit。详 [v0.3](path_alpha_subgap_closure_integration_v0_3.md) + [c3-dev-reviewer-batch-holistic-2.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-2.md) §1-§2-§6。
>
> ---

**版本**：v0.2 **[SUPERSEDED]**
**日期**：2026-04-26（C3 batch round 1 post-fix same-day）
**前身**：[v0.1 SUPERSEDED 2026-04-26](path_alpha_subgap_closure_integration_v0_1.md)（C3 holistic FAIL + diff REJECTED at L1.G4 + L3.G3 gap-id 揭露 Pirandola Eq. 11 citation 错）
**类型**：**STATUS REPORT ONLY**（非 closure 文档；非 lemma proof；非升级请求）
**严谨性 banner**：本文件仅汇总 path α 11 sub-gap 的 **C1(a) Codex PASS verdicts + C3 dev-reviewer round 1 verdicts + 撤回 + 残留 + 结构性 OPEN gap**。**不**主张任何 sub-gap 已升级为 [COROLLARY]/[THM]；**不**主张 path α three-lemma combined chain 已 close；**不**得对外引用为定理级。

> **简写一览（首次出现给中文 gloss，per memory feedback `feedback_explain_abbreviations`）**
> - **path α** = 11 sub-gap 路径策略，目标证 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 及其向 single-repeater bound 的 specialization（详 §4 specialization chain caveat）。**umr** = untrusted-middle-relay TFQKD topology
> - **C1 / C2 / C3** = R0.2 升级三闸门；C1 独立验证（跨家族 AI 直读 PDF / 人类纸笔 / 非 AI 工具任一）、C2 用户审签、C3 dev-reviewer 双 Codex QA
> - **C1(a)** = C1 第一种合规组合：跨家族 AI（Claude + Codex 不同训练偏差源）双方均直读 PDF
> - **L1.Gx / L2.Gx / L3.Gx** = path α 三 lemma（A / B / C）下的 sub-gap，编号源自 [umr_path_alpha_lemma_skeletons_v0_1.md](umr_path_alpha_lemma_skeletons_v0_1.md) §3-§5
> - **[SYN] / [COROLLARY] / [THM] / [UNKNOWN]** = R0.3 严谨性四级标签（AI 默认 [SYN] 或更低）
> - **Cui 2019** = Cui-Yin-Wang-Chen-Wang-Guo-Han 2019 *Phys Rev Applied* 11:034053 simplified TFQKD protocol（path α 的 anchor 协议）
> - **REE** = Relative Entropy of Entanglement（相对熵纠缠度量）
> - **tele-covariance** = teleportation-covariance（信道在 teleportation 下保协变性的性质，pure-loss bosonic 满足）

---

## §1 11 Sub-Gap C1(a) + C3 Round 1 状态矩阵（v0.2 修正）

| Sub-gap | Lemma | 主题 | C1(a) Round | C1(a) Verdict | C3 R1 (diff/holistic) | 总状态 |
|---|---|---|---|---|---|---|
| **L1.G1** | A | Hilbert 空间 alignment | round 2 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L1.G2** | A | embedding ι 构造 (**HARDEST**) | round 1 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L1.G3** | A | Stinespring gauge invariance | round 3 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L1.G4** | A | trace-distance contraction | round 4 | (PASS at C1) | 🛑 **diff REJECTED 2026-04-26** | **[RETRACTED]** per [closure file banner](path_alpha_l1g4_closure_v0_1.md) + [RETRACTION.md §9.1](../research/RETRACTION.md#91-l1g4-v01-closure-撤回) |
| **L2.G1** | B | rate-direction sign | round 2 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L2.G2** | B | ε-composable decomposition | round 3 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L2.G3** | B | Eve set across spaces | — | — | — | **OPEN per R0.1**（cross-space gap，AI 不得 close）|
| **L2.G4** | B | non-LOCC joint attack (asymptotic coherent) | round 2 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L3.G1** | C | LOPC syntax cross-topology | round 1 | ✅ PASS | ✅ diff PASS / holistic clean | C1+C3R1 PASS / C2 待 |
| **L3.G2** | C | key length cross-topology (Devetak-Winter ↔ ε-private state bridge under Option B) | round 3 | ✅ PASS | ⚠️ **diff FAIL minor** (§4 stale Eq. (8) ref，v0.4 patched) + holistic Lemma C counting residual | C1 PASS / C3 R2 待 |
| **L3.G3** | C | Pirandola Eq. 11 → `-log_2(1-√η_{AB})` specialization 适用 in ι(Π) | gap-id only (NOT closure) | — | — | **OPEN per R0.1**（operational-link，6 个 sub-residual identified per [gap-id round](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md) §D）|

**汇总**（v0.2 修正后）：

- **8/11 sub-gap C1(a) PASS + C3 R1 clean** — L1.G1, L1.G2, L1.G3, L2.G1, L2.G2, L2.G4, L3.G1（diff PASS / holistic clean）
- **1/11 [RETRACTED]** — L1.G4（C3 diff REJECTED 2026-04-26 — scope drift / adjacent-gap smuggling）
- **1/11 C1 PASS / C3 R2 待** — L3.G2（diff FAIL minor §4 patched in v0.4，holistic 揭露 Lemma C counting residual 须独立 absorb）
- **2/11 OPEN per R0.1** — L2.G3（cross-space Eve set ⊆）+ L3.G3（operational-link Pirandola Eq. 11 specialization chain）
- **额外 1 个 named residual**：**Lemma C channel-use counting/normalization residual**（per [c3-dev-reviewer-batch-holistic-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1）— 详 §3.3
- **C2 用户审签 batch**：⏳ **未启动**
- **C3 round 1**：✅ 8 个 PASS + ⚠️ 1 个 FAIL minor patched + 🛑 1 个 REJECTED + ⏳ R2 重评待

---

## §2 已 PASS 的 8 个 closure candidate 文件清单（v0.2 修正后）

| Sub-gap | 文件 | C1(a) PDF 直读对象 | C3 R1 状态 |
|---|---|---|---|
| L1.G1 | [path_alpha_l1g1_closure_v0_1.md](path_alpha_l1g1_closure_v0_1.md) | Cui 2019 + Pirandola SI Note 1 + KW Ch 20 | diff PASS / holistic clean |
| L1.G2 | [path_alpha_l1g2_closure_v0_1.md](path_alpha_l1g2_closure_v0_1.md) | Cui Step 3 + Pirandola SI Note 1/2 + KW §20.1/§20.2 | diff PASS / holistic clean |
| L1.G3 | [path_alpha_l1g3_closure_v0_1.md](path_alpha_l1g3_closure_v0_1.md) | KW Chapter 4 §4.3 | diff PASS / holistic clean |
| L2.G1 | [path_alpha_l2g1_closure_v0_1.md](path_alpha_l2g1_closure_v0_1.md) | KW Ch 20 §20.1 (n,K,ε)-SKA | diff PASS / holistic clean |
| L2.G2 | [path_alpha_l2g2_closure_v0_1.md](path_alpha_l2g2_closure_v0_1.md) | Portmann-Renner 2022 §III.B Theorem 2 + Lemma 3 | diff PASS / holistic clean |
| L2.G4 | [path_alpha_l2g4_closure_v0_1.md](path_alpha_l2g4_closure_v0_1.md) | Cui 2019 Eq. (1) + Section III page 3 | diff PASS / holistic clean |
| L3.G1 | [path_alpha_l3g1_closure_v0_1.md](path_alpha_l3g1_closure_v0_1.md) | KW Eq. (20.1.12) + Pirandola SI Note 1 + Cui Step 3 | diff PASS / holistic clean |

**待 C3 R2 重评（v0.4 patched）**：

| Sub-gap | 文件 | C3 R1 issue | v0.4 patch |
|---|---|---|---|
| L3.G2 | [path_alpha_l3g2_closure_v0_1.md](path_alpha_l3g2_closure_v0_1.md) | §4 stale "Pirandola Methods Eq. (8)" ref 与 §2.3 corrected attribution "near Eq. (35)" 不一致 | §4 propagate corrected attribution + holistic disclaim Lemma C counting residual not absorbed |

**[RETRACTED]**：

| Sub-gap | 文件 | REJECTED 依据 | 撤回引述 |
|---|---|---|---|
| L1.G4 | [path_alpha_l1g4_closure_v0_1.md](path_alpha_l1g4_closure_v0_1.md) | §1.2 derivation 同时使用 ι 合法性（L1.G2）+ Eve set ⊆（L2.G3）作为 application 前提，但 §1.3 explicit 排除二者 → adjacent-gap smuggling | [RETRACTION.md §9.1](../research/RETRACTION.md#91-l1g4-v01-closure-撤回) |

Codex round 输出归档：[docs/workflow/umr-path-alpha-three-lemma-v0-2/](../workflow/umr-path-alpha-three-lemma-v0-2/) 下 `c1a-l*-citation-verify*.md` + `c3-dev-reviewer-batch-{diff,holistic}-1.md` + `c1a-l3g3-gap-identification-round1.md`。

---

## §3 OPEN / 残留 sub-gap — 结构性维持 [UNKNOWN] 的依据（v0.2 扩展）

### §3.1 L2.G3 — Eve set across spaces（与 v0.1 §3.1 一致，原文重述）

**Statement target**：$\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$，trusted-relay Eve **仅** access $\mathcal{H}_E$，**不**触 $\mathcal{H}_C$。

**为什么 OPEN**：cross-space gap（per memory `feedback_ai_draft_structural_gaps`）；lemma_skeletons §4.2 明示需 user 显式声明；Curty 2018 reduced-state 不替代 close；C1 path 不可用。详 [v0.1 §3.1](path_alpha_subgap_closure_integration_v0_1.md#31-l2g3--eve-set-across-spaces)（保留作 audit）。

### §3.2 L3.G3 — Pirandola Eq. 11 → `-log_2(1-√η_{AB})` specialization in ι(Π)（v0.2 大幅扩展）

**v0.1 → v0.2 修正**：v0.1 §3.2 把 L3.G3 简化为 "Pirandola Eq. 11 是否 apply 到 ι(Π)"。L3.G3 [exploratory gap-id round](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md) 直读 Pirandola PDF 揭露：

**Pirandola 2019 Eq. 11 实际**（per main paper PDF p.4）：

$$C(\mathcal{N}) \leq \min_C E_R(C), \quad \text{with } E_R(C) := \max_{(x,y)\in \tilde{C}} E_R(\sigma_{xy})$$

是 **REE cut bound** for end-to-end network capacity（任意 adaptive 协议 + 跨任意 Alice-Bob cut 的 REE 最小流），**不**等于 single-repeater bound `-log_2(1-√η_{AB})`。

**`-log_2(1-√η_{AB})` 的来源**（per gap-id round §A direct PDF read）：

- **Eq. (8)** main PDF p.3：lossy chain formula
- **Eq. (9)** main PDF p.3：equidistant fixed-total-loss formula
- **N=1** 时 Eq. (9) 给 `-log_2(1-√η)`
- 完整 derivation chain **= Eq. 11 (REE cut UB) + Eq. (8)/(9) (lossy chain specialization) + tele-covariance (pure-loss bosonic) + distillability + symmetric / equidistant η split (`η_{AB} = η_{AC}·η_{BC}`)**

**L3.G3 6 个 sub-residual**（per gap-id round §D）：

1. **Citation gap**：Eq. 11 → distillable / pure-loss single-route formulas（Eq. (8)/(9)）的 specialization chain 缺
2. **Parameter-identification gap**：是 `η_min` vs `η_AC·η_BC` vs symmetric？三个不可互换；path α 文档目前 implicit 用 `η_{AB} = η_{AC}·η_{BC}`，未独立 verify
3. **Symmetry / equidistance gap**：`√η_{AB}` 形式要求 equidistant split；否则 generic bound 是 `-log_2(1-min{η_AC, η_BC})`
4. **Channel-use accounting gap**：one Cui trial = one Pirandola network use 须 explicit；与 §3.3 Lemma C counting residual 部分重叠但 distinct（前者是 Eq. 11 的 specialization，后者是 L3.G2 Devetak-Winter ↔ ε-private state bridge 的 channel-use counting）
5. **Protocol-model gap**：honest Charlie 干涉 / detection 须 explicit written as Pirandola Note 1/2 permitted local op
6. **Edge-model gap**：A-C / B-C links 须 explicit declared 为 fixed memoryless pure-loss bosonic（确保 tele-covariance）

**为什么 OPEN（且不可由 AI 自行 close）**：

- **operational-link gap**（per memory feedback `feedback_ai_draft_structural_gaps`）：6 个 sub-residual 都是 operational identification + parameter form + edge-model 范畴的 explicit 工作，AI **不**得 draft closure
- **L1.G2 PASS 不 imply L3.G3 PASS**（per L1.G2 Codex round 1 verdict §5(e) explicit "not Eq. 11 applicability"）
- **C1 path**：(a) 跨家族 AI 直读 PDF — 单 PDF 不充分（涉及多 specialization step + edge model + parameter id）；(b) 人类纸笔 — user-level 工作；(c) 非 AI 工具 — 部分 sub-residual 可由 numerical SDP 辅助 verify edge-model fit

**结论**：L3.G3 维持 [UNKNOWN]，**6 个 sub-residual 显式列入** integration 作 future verification entry points。Lemma C 整体仍 [SYN, conditional on L3.G3 + Lemma C counting residual + L3.G2 R2]。

### §3.3 Lemma C channel-use counting/normalization residual（v0.2 NEW）

**Discovery**：per [c3-dev-reviewer-batch-holistic-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1。

**lemma_skeletons §157 原 statement target C**：要求 "channel use 计数对齐 + 同 ε-secure criterion"。

**已 close 部分**：L3.G2 closure（在 user Option B 下）close 后者 — Devetak-Winter rate ↔ ε-close-to-private-state criterion bridge。

**未 close 部分**：**前者 channel-use accounting alignment**（Cui per-trial 计数 vs Pirandola per-network-use 计数）。L3.G2 closure scope clean 但**未** absorb 这部分。lemma_skeletons §7.x.3 仍 record unresolved caveats（per holistic reviewer flag at lines 317-329, 346-350）。

**为什么是 residual 而非完全 OPEN**：

- 非 cross-space / cross-task structural gap（per memory `feedback_ai_draft_structural_gaps`）；是**计数对齐** technical residual
- Cui 2019 Section III 已记 per-trial accounting；Pirandola SI Note 1 已记 per-network-use accounting；**两者 alignment 是 specific 比例的 explicit 验证**（每 Cui trial 多少 Pirandola channel-use？）
- L3.G3 sub-residual 4 (channel-use accounting gap) **部分**重叠 — Lemma C counting residual 是 L3.G2 端的 counting；L3.G3 sub-residual 4 是 Eq. 11 specialization 端的 counting；本质相关但**不**等同

**v0.2 scope**：本 Lemma C counting/normalization residual 显式 disclaimed 入 **L3.G2 v0.4 §4 末段** + 本 integration v0.2 §3.3。**不**自行 close；待 user 决定推进策略。

### §3.4 综合：Lemma C 当前 conditional 状态

Lemma C statement target = $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$。当前：

- **L3.G1** ✅ PASS（syntactic compatibility）
- **L3.G2** ✅ C1 PASS（在 user Option B 下；C3 R2 待 §4 patch）
- **L3.G3** ⚠️ OPEN（6 个 sub-residual）
- **Lemma C counting residual** ⚠️ residual（未由 L3.G2 absorb）

**Lemma C 整体**：[SYN, conditional on L3.G3 6 sub-residual + Lemma C counting residual + L3.G2 C3 R2 + Eq. 11 specialization chain caveat]。

---

## §4 Path α three-lemma combined chain — 当前 conditional 状态（v0.2 重写 with citation 修正）

按 [lemma_skeletons §6](umr_path_alpha_lemma_skeletons_v0_1.md) combined chain 的 **CONDITIONAL** [SYN] 表述（**待 §6 修正 Eq. 11 specialization chain**）：

**v0.1 错误形式**（保留作 cautionary record）：

```
R_Cui(Π) [Lemma A+B+C] ≤ R_Pirandola(Π_tr) [Pirandola Eq. 11 [THM]] ≤ -log_2(1-√η_AB)
```

**v0.2 修正形式**：

$$\underbrace{R_{Cui}(\Pi)}_{\text{TF-QKD 密钥率, Cui Eq. (3)}} \stackrel{\text{Lemma A+B+C [SYN, conditional]}}{\leq} \underbrace{R_{Pirandola}(\Pi_{tr})}_{\text{end-to-end 网络 secret-key capacity}} \stackrel{\text{Pirandola 2019 Eq. 11 (REE cut bound) [THM]}}{\leq} \underbrace{\min_C E_R(C)}_{\text{REE 最小切割流}} \stackrel{\text{Eq. (8)/(9) specialization + tele-cov + sym η split [conditional]}}{=} \underbrace{-\log_2(1-\sqrt{\eta_{AB}})}_{\text{single-repeater bound, N=1 equidistant}}$$

**当前 conditional status (post C3 batch round 1, 2026-04-26)**：

- **8/11 sub-gap C1(a) + C3 R1 PASS**（L1.G1/G2/G3 + L2.G1/G2/G4 + L3.G1）
- **1/11 [RETRACTED]**：L1.G4（C3 diff REJECTED）→ Lemma A 整体仍 [SYN, conditional on L1.G4 v0.2 redo + 其他 3 个 sub-gap PASS]
- **1/11 C1 PASS / C3 R2 待**：L3.G2（FAIL minor patched）
- **2/11 OPEN**：L2.G3（cross-space）+ L3.G3（operational-link, 6 sub-residual）
- **1 named residual**：Lemma C counting/normalization
- **1 specialization chain caveat**：v0.1 误把 Pirandola Eq. 11 直接等同 `-log_2(1-√η_{AB})`；v0.2 修正为 Eq. 11 (REE cut UB) + Eq. (8)/(9) specialization + tele-covariance + sym η split 的完整 chain
- **Combined chain**：[SYN, conditional on **{L1.G4 redo, L3.G2 R2, L2.G3 OPEN, L3.G3 OPEN (6 sub-residual), Lemma C counting residual, Eq. 11 specialization chain}**]
- **C2 用户审签 batch**：⏳ 未启动；**C3 R2 重评**：⏳ 未启动

**对外引用资格**：

- **[NONE]** — combined chain 仍 [SYN, conditional on multi-OPEN/residual]
- 升级到 [COROLLARY] / [THM] 仍需 R0.2 完整 (C1∧C2∧C3) 流程；当前**远未**满足

---

## §5 R0.1 / R0.2 红线复述（v0.2 加固）

### §5.1 R0.1 — 不做计划外降级

- **8 个 PASS closure**：每个 §1.3 strict scope 必须保持不动；C2 user signature batch 时若发现 scope 过 strong 须 immediate 修正
- **L1.G4 [RETRACTED]**：未恢复前 path α Lemma A 整体 closure 状态 = **未** PASS（即使 L1.G1/G2/G3 PASS）
- **L2.G3 / L3.G3 / Lemma C counting residual**：**禁止** AI 自行起草 closure candidate；维持 OPEN/residual

### §5.2 R0.2 — 三闸门并列必要（**v0.1 line 133 措辞已修正**）

- **C1(a) 跨家族 AI 直读 PDF** 要求 **双方均直接读 PDF**（per CLAUDE.md §0 + RETRACTION.md §4.1 规则 3）。本 session 的 8 个 PASS closure：
  - **Codex 单边直读 PDF**：✅ 所有 8 个 closure 的 C1(a) Codex round 都直读了 PDF（per c1a-l*-citation-verify.md outputs）
  - **Claude 端 PDF 直读 status**：⚠️ Claude（本 session 的 draft 来源）的 PDF 直读 status 是**间接**的 —— 通过 [umr_path_alpha_pdf_synthesis_v0_1.md](umr_path_alpha_pdf_synthesis_v0_1.md) 等先期 synthesis 文档，**不**等同 Claude 在 closure draft 时再次直读 PDF
  - **R0.2 字面要求**：双方均直接读 PDF。本 session **严格自查**：Codex 端满足，Claude 端依赖先期 synthesis（**弱 fit** R0.2 字面要求）。建议 user 在 C2 batch 时 cross-verify Claude 引用准确性，或要求 Claude 在 v0.2 redo / Round 2 时 re-read PDF
  - 即使 C1(a) 完整满足，C2 用户签字 + C3 dev-reviewer 仍并列必要
- **C2 用户签字未走** — 8 个 PASS closure 全部 ⏳ 待 batch
- **C3 R2 待重评** — L3.G2 patch 待 R2；L1.G4 [RETRACTED] 须 v0.2 redo
- **任何升级 [SYN] → [COROLLARY] 仍非法**

### §5.3 R0.3 — 严谨性分级

- 8 个 PASS closure banner 维持 `[SYN candidate-for-COROLLARY-pending-C2 user signature ∧ C3 dev-reviewer]`
- **L1.G4 banner = [RETRACTED]** 不再是 [SYN candidate]
- combined chain 仍 [SYN, conditional on multi-OPEN/residual]，**不可对外引用**

### §5.4 v1 retraction 教训复述（v0.2 加固）

v1 FINDINGS retraction (2026-04-19) 因 "Claude 起草 + Claude 多审" 误当多方验证。本 session：

- ✅ **C1(a) 跨家族 review** 通过（Codex 端直读 PDF）
- ⚠️ Claude 端 PDF 直读偏弱（间接 via synthesis）— 建议 C2 时 cross-verify
- ✅ **C3 dev-reviewer Round 1** 揭露 L1.G4 REJECTED + L3.G2 FAIL + L3.G3 citation 错 + Lemma C counting residual + integration v0.1 over-tightening — **避免**了第 5/6/7 次 trap 的延续
- ⏳ C2 / C3 R2 待

**任何尝试在 C2 / C3 R2 未完成前对外引用本 session 任一 sub-gap closure 视同 v1 retraction 重蹈**。

---

## §6 推荐下一步（按 R0.2 三闸门次序，v0.2 修正）

**注意**：以下为推荐序列，**不**预设 schedule；具体启动须由 user 显式触发。

1. **L1.G4 v0.2 redo**（C3 REJECTED 修复）
   - 移除 §1.2 "if Π ε-secure then Π_tr ε-secure" application 内容（it's Lemma A 整体 conclusion，不单独由 L1.G4 close）
   - 重写 §1.2 为 "L1.G4 contributes the trace-distance contraction step within Lemma A's chain"
   - 新一轮 C1(a) Codex round + C3 R2

2. **L3.G2 C3 R2 重评**（v0.4 patched，§4 stale text 已修）
   - Codex re-read 仅本 §4 patch + holistic Lemma C counting disclaim
   - 期望 R2 PASS

3. **lemma_skeletons §6 修正**（Pirandola Eq. 11 specialization chain）
   - 把 v0.1 form 改 v0.2 form（per §4 above）
   - Cross-link 到 [RETRACTION.md §9.3](../research/RETRACTION.md)

4. **C2 用户审签 batch**（8 个 PASS closure + 修正后 lemma_skeletons + integration v0.2）
   - user 逐个核对 §1.1 lemma statement / §1.3 strict scope / §3.x derivation / §-1 状态表
   - **L2.G3 显式 declaration** 在此阶段（trusted-relay Eve access constraint）—— 若 user 选择推进
   - **Lemma C counting residual 推进策略** user 决策（独立 sub-gap 立项 OR 标永久 residual）
   - **L3.G3 6 sub-residual 推进策略** user 决策（continue / drop）

5. **C3 dev-reviewer R2 batch**（修正后整体 batch）
   - 用 dev-reviewer skill 重跑 batched diff + holistic
   - 任一 reviewer UNSOUND / REJECTED → 立即撤回相应 closure 并记 RETRACTION.md
   - PASS → C3 闸门通过；C1 ∧ C2 ∧ C3 完整 → 可升级 sub-gap [COROLLARY] 候选

6. **可选**：L1.G4 redo + L3.G2 R2 + L3.G3 separate verification round
   - 仅在 user 显式授权 + L2.G3 already declared 的前提下

7. **Combined chain 升级评估**（仅在所有 sub-gap C1∧C2∧C3 全过 + Lemma C counting residual + Eq. 11 specialization chain 全 verified 的前提下）
   - 整体升级 [COROLLARY] 候选；对外引用需进一步 [THM] 路径

---

## §7 v0.2 vs v0.1 diff 概要

| Item | v0.1 | v0.2 |
|---|---|---|
| L1.G4 状态 | C1(a) PASS | **[RETRACTED]** per C3 diff REJECTED |
| 总 PASS 数 | 9/11 | **8/11** |
| Lemma C counting residual | 未列 | **§3.3 NEW** |
| Pirandola Eq. 11 ↔ `-log_2(1-√η_{AB})` 关系 | 直接等同（错） | **§4 specialization chain 修正**：Eq. 11 = REE cut UB；single-repeater form 需 Eq. (8)/(9) + tele-cov + sym η split |
| Combined chain conditional 数 | "2 OPEN" | "{L1.G4 redo + L3.G2 R2 + L2.G3 + L3.G3 (6 sub) + Lemma C counting + Eq. 11 specialization}" |
| C1(a) 双方直读 PDF 措辞 | "Claude draft based on prior PDF synthesis" | **§5.2 显式自查**：Codex 端满足，Claude 端弱 fit；建议 C2 cross-verify |
| 推荐下一步项数 | 4 | 7 |

---

## §8 Changelog

- **v0.1** (2026-04-26)：首版 integration status report。9/11 sub-gap C1(a) PASS；2/11 (L2.G3 + L3.G3) **结构性 OPEN per R0.1**。**[SUPERSEDED 2026-04-26]** 因 C3 batch round 1 holistic FAIL + diff REJECTED at L1.G4 + L3.G3 gap-id 揭露 Pirandola Eq. 11 citation 错。
- **v0.2** (2026-04-26 same-day)：本版。修正 v0.1 5 个问题（L1.G4 撤回 → 8/11 PASS；Lemma C counting residual NEW；Pirandola Eq. 11 specialization chain caveat NEW；C1(a) 双方直读 PDF 措辞自查；over-tightening "2 OPEN" 改为 multi-OPEN 显式列）。Combined chain 仍 [SYN, conditional on multi-OPEN/residual]，**不可对外引用**。下一步：L1.G4 v0.2 redo + L3.G2 C3 R2 + lemma_skeletons §6 修正 + C2 用户审签 + C3 R2 batch。
