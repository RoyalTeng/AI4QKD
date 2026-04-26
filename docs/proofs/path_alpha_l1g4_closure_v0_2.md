# Path α Lemma A sub-gap L1.G4 — Closure Candidate v0.2

**Sub-gap**：L1.G4 — Trace distance contraction under partial trace over Charlie's internal Hilbert space（迹距离在对 Charlie 内部空间取偏迹后的收缩性）

**版本**：v0.2（2026-04-26 same-day）
**前身**：[v0.1 RETRACTED](path_alpha_l1g4_closure_v0_1.md)（2026-04-26 C3 dev-reviewer Round 1 diff REJECTED — §1.2 application 段 smuggled L1.G2 + L2.G3 closure，与 §1.3 explicit scope 矛盾）
**日期**：2026-04-26（v0.1 撤回当天 redo）
**C1 path used**：**C1(c)** non-AI 数值（v0.1 已 PASS, 300 trials）+ **C1(a)** 跨家族 AI 直读 PDF（v0.1 已 PASS at round 4）；本 v0.2 仅修 §1.2 application 段，main citation + math + numerical 维持 v0.1 verified status
**严谨性 banner**：[SYN candidate-for-COROLLARY-pending-C2 user signature ∧ C3 R2 dev-reviewer]

---

## §-1 v0.2 redo 范围（与 v0.1 [RETRACTED] 的差异）

### -1.1 v0.1 [RETRACTED] 触发原因

**C3 dev-reviewer Round 1 diff 评审**（2026-04-26，[c3-dev-reviewer-batch-diff-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-diff-1.md) item 4）verdict = REJECTED。critical 依据：

- v0.1 §1.2 derivation 同时使用了：
  - (i) `ρ^{Π_tr}_{ABE'} = Tr_C(ρ^{Π}_{ABCE})` 身份（前提是 L2.G3 trusted-relay Eve 仅控 H_E）
  - (ii) "if Π is ε-secure ... then Π_tr is ε-secure" 结论（前提是 L1.G2 ι embedding 合法性）
- v0.1 §1.3 同时声明：
  - `❌ 不主张 Π → Π_tr 嵌入 ι 的合法性（依赖 L1.G2）`
  - `❌ 不主张 trusted-relay Eve 仅控 H_E 不触 H_C 的协议设定（依赖 L1.G1）`
- **scope contradiction**：§1.2 derivation 实际依赖 §1.3 explicit 排除的 assumption；属于 adjacent-gap smuggling

### -1.2 v0.2 修复策略

- **保留有效部分**（v0.1 的 §1.1 lemma 数学陈述 + §3 数值 PASS + §2 KW Theorem 6.3 + §4.4.2 引文 verbatim）
- **重写 §1.2**：移除 application 段（"if Π ε-secure then Π_tr ε-secure"）；改为"L1.G4 在引理 A 推导链中的贡献步骤"——明确只 close 局部 contraction 数学事实，**不**主张 application 层结论（后者由引理 A 整体在所有 sub-gap close 后才成立）
- **加固 §1.3**：scope 声明再加一条 `❌ 不主张 Π / Π_tr 任一具体 ε 数值上界`
- **新增 §1.4**：明示与 L1.G2 / L2.G3 的依赖关系，避免任何 smuggling 误读

### -1.3 v0.2 vs v0.1 diff 概要

| 章节 | v0.1 (RETRACTED) | v0.2 |
|---|---|---|
| §1.1 lemma statement | 抽象 trace distance contraction | 同（保留）|
| §1.2 path α 中的位置 | 写 "if Π ε-secure then Π_tr ε-secure" application chain | **重写**：仅 stating "L1.G4 是引理 A 的 contributing step；application 层结论由 L1.G2 + L2.G3 + L1.G4 jointly 后续 close" |
| §1.3 严格 scope | 4 条 disclaim | **加强**到 5 条（多加一条数值上界 disclaim）|
| §1.4 NEW | — | **新增**：与 L1.G2 / L2.G3 / L1.G1 依赖关系明示 |
| §2 引文 | KW Theorem 6.3 + §4.4.2（C1(a) round 4 PASS）| 同（保留）|
| §3 数值 | 300 trials, 0 violations（C1(c) PASS）| 同（保留）|
| §4 round history | C1(a) round 1-4 history | 加 §4.4 v0.2 redo + 待 C3 R2 |

---

## §1 Sub-gap statement (precise, v0.2)

### 1.1 Lemma L1.G4 statement（与 v0.1 一致，保留）

**Lemma (L1.G4 — trace distance contraction under partial trace over Charlie's internal Hilbert space)**：

设：
- $\mathcal{H} = \mathcal{H}_A \otimes \mathcal{H}_B \otimes \mathcal{H}_C \otimes \mathcal{H}_E$ 是任意 four-fold 张量积希尔伯特空间
- $\rho, \sigma \in \mathcal{D}(\mathcal{H})$ 是任意密度算子（$\mathcal{D}$ 表示密度算子集合）

**则**：

$$\| \mathrm{Tr}_C(\rho) - \mathrm{Tr}_C(\sigma) \|_1 \;\leq\; \| \rho - \sigma \|_1$$

其中 $\| \cdot \|_1$ 是 Schatten-1 范数（迹范数 = 算子奇异值之和）。

**严格 scope of statement**：lemma 仅 about partial trace 这一 specific CPTP map under Schatten-1 norm 的 contraction property。**完全 abstract**，不涉及 path α 任何 protocol-specific assumption。

### 1.2 L1.G4 在引理 A 推导链中的贡献步骤（v0.2 重写）

**v0.2 设计原则**：本 §1.2 仅 stating L1.G4 在引理 A（path α 协议嵌入引理）整体推导链中的**位置 + 角色**；**不**主张该链已 close，**不**主张任何 application 层（如"if Π ε-secure then Π_tr ε-secure"）结论。

**引理 A 整体目标**（per [umr_path_alpha_lemma_skeletons_v0_1.md](umr_path_alpha_lemma_skeletons_v0_1.md) §3）：在 path α 协议嵌入下，从 umr 协议 Π 的 ε-secure 出发，得 ι(Π) = Π_tr 在 trusted-relay 模型下也 ε-secure。

**引理 A 由 4 个 sub-gap jointly close**：
- **L1.G1**：Hilbert 空间 alignment（将 umr Eve 的 H_C ⊗ H_E 与 trusted-relay Eve 的 H_E' alignment）
- **L1.G2**：embedding ι 合法性（Π_tr 是合法的 trusted-relay 协议 class 成员）
- **L1.G3**：Stinespring gauge invariance（Eve 内部 dilation 的 gauge 选择不影响 channel output）
- **L1.G4**（本 lemma）：trace distance 在 partial trace 下的 contraction 这一**纯数学事实**

**L1.G4 的角色**：仅提供"if 我有 ρ 与 σ 在 H = H_A ⊗ H_B ⊗ H_C ⊗ H_E 上的 trace distance bound，then 取 Tr_C 后的 trace distance bound 不会变大"这一 abstract 数学事实。

**L1.G4 的角色不包括**：
- ❌ 不主张 ρ = ρ^Π_ABCE 这种 path α 具体设定（那是 L1.G1 + L1.G2 工作）
- ❌ 不主张 Tr_C(ρ^Π_ABCE) = ρ^Π_tr_ABE'（即 trusted-relay Eve 仅控 H_E 这一 protocol-level 等同性，那是 L2.G3 工作）
- ❌ 不主张 ε 在 Π → Π_tr 之间的传递（那是 L1.G1 + L1.G2 + L2.G3 + L1.G4 全部 close 后引理 A 整体的 conclusion）
- ❌ 不主张 σ_target（理想态）在 Π 与 Π_tr 框架下 consistent（那是 L2.G2 ε-composable 三分量）

### 1.3 严格 scope 声明（v0.2 加强为 5 条）

- ✅ 本 lemma 是 about: trace distance 在 partial trace（一个 specific CPTP map）下的 contraction 这一 abstract 数学事实
- ❌ 本 lemma **不**主张 σ_target 的具体形式（依赖 L2.G2 ε-composable 三分量）
- ❌ 本 lemma **不**主张 Π → Π_tr 嵌入 ι 的合法性（依赖 L1.G2）
- ❌ 本 lemma **不**主张 trusted-relay Eve 仅控 H_E 不触 H_C 的协议设定（依赖 L2.G3，注意：v0.1 错把它依赖到 L1.G1，v0.2 corrected 为 L2.G3）
- ❌ **NEW v0.2**：本 lemma **不**主张 Π / Π_tr 任一具体 ε 数值上界（依赖 Cui 2019 Eq. (3) Devetak-Winter 分析 + L2.G4，本 lemma 仅给 partial-trace 下 trace distance 单调性 sign）

### 1.4 与 L1.G2 / L2.G3 / L1.G1 依赖关系明示（v0.2 NEW，避免 smuggling 误读）

**显式声明**（v0.2 防 v0.1 REJECTED 重蹈）：

L1.G4 的**纯 abstract 数学陈述**（§1.1）**完全独立**于 path α 协议-specific assumption。但**任何**把 L1.G4 应用到 path α security inheritance 的尝试，都需要 jointly invoke：

| 调用 | 提供的事实 | sub-gap 状态 |
|---|---|---|
| L1.G1 | Hilbert 空间 H_C ⊗ H_E（umr）与 H_E'（trusted-relay）alignment | ✅ C1+C3 R1 PASS |
| L1.G2 | ι : Π → Π_tr 是合法 trusted-relay 协议 class 嵌入 | ✅ C1+C3 R1 PASS |
| L2.G3 | trusted-relay Eve 仅 access H_E（not H_C）→ ρ^Π_tr_ABE = Tr_C(ρ^Π_ABCE) 是 well-defined identity | **OPEN per R0.1**（cross-space gap，user 显式声明范畴）|
| **L1.G4** | partial trace 下 trace distance 不变大 | **本 lemma**，C1 PASS / C2/C3 R2 待 |

**结论**：L1.G4 alone 是 abstract 数学事实，**无**实质 path α scope dependency；但 L1.G4 在引理 A 整体推导中**不**单独 close 任何 application 层结论；application 层（如 ε security inheritance）由 L1.G1 + L1.G2 + L2.G3 + L1.G4 **jointly** 在 L2.G3 close 后实现，**不**由 L1.G4 单独承担。

---

## §2 引文（与 v0.1 一致，保留 C1(a) round 4 PASS 状态）

详见 [v0.1 §2](path_alpha_l1g4_closure_v0_1.md#§2-引文citation-accuracy-核对pending-c1a-codex-round)，本 v0.2 引文部分**未改**，仍指向：

- **2.1.a** Trace-distance DPI（数据处理不等式）—— **Khatri-Wilde 2024 Theorem 6.3**（Chapter 6 "Distinguishibility Measures for Quantum States and Channels" — *sic*, KW PDF chapter-title typo），at PDF p.278 / printed p.265，verbatim Eq. (6.1.9)：$\|\rho - \sigma\|_1 \geq \|\mathcal{N}(\rho) - \mathcal{N}(\sigma)\|_1$ for any positive trace-non-increasing map $\mathcal{N}$
- **2.1.b** Partial trace is CPTP —— Khatri-Wilde 2024 §4.4.2 "Trace and Partial-Trace Channels" at PDF p.171 / printed p.158，verbatim "$\mathrm{Tr}_B$ is completely positive."
- **2.1.c** L1.G4 即 Theorem 6.3 取 $\mathcal{N} = \mathrm{Tr}_C$ + §4.4.2 partial trace CPTP 的 immediate corollary
- **2.2** 辅 citation：Nielsen-Chuang 2010 Theorem 9.2

**注意（v0.2 加固）**：v0.1 §2.3 "Pirandola 2019 Eq. 36 旁证" 标 "待 Codex 直读 verify"。该引用作为**辅助旁证**（非 main citation），且 v0.2 not 依赖 Pirandola Eq. 36。**v0.2 strict scope**：移除 §2.3 的 Pirandola Eq. 36 旁证 dependency；本 lemma 仅 cite KW Theorem 6.3 + §4.4.2 这一 main citation 路径。这也回应 [c3-dev-reviewer-batch-holistic-1.md §4 trap (3)](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) 标记的 "still carries a Pirandola Eq. 36 side-citation marked '待 Codex 直读 verify'" cleanup 项。

---

## §3 数值验证（与 v0.1 一致，保留 C1(c) PASS）

详见 [v0.1 §3](path_alpha_l1g4_closure_v0_1.md#§3-数值验证c1c-primary)：

- 300 trials over 6 dimension combinations，0 violations，min margin = $3.197 \times 10^{-1}$，PASS
- 数据：[csv](../research/data/path_alpha_l1g4_trace_distance_contraction.csv) + [json](../research/data/path_alpha_l1g4_trace_distance_contraction.json)
- 脚本：[scripts/path_alpha_l1g4_trace_distance_contraction.py](../../scripts/path_alpha_l1g4_trace_distance_contraction.py)
- RNG seed = 20260426（reproducible）

**v0.2 数值 strict scope**（与 v0.1 §3.3 一致）：sanity check / regression role，不替代 Nielsen-Chuang Thm 9.2 textbook proof。

---

## §4 R0.2 升级闸门状态（v0.2 redo）

| 闸门 | 状态 |
|---|---|
| **C1(c)** non-AI 数值验证 | ✅ **PASS**（v0.1 §3, 300 trials, 0 violations）|
| **C1(a)** 跨家族 AI 直读 PDF 引文核对 | ✅ **PASS** at v0.1 Codex round 4（main citation: Theorem 6.3 + §4.4.2）|
| **C1** aggregate（OR over (a)/(b)/(c)）| ✅ **PASS** via C1(a) + C1(c) 双路径 |
| **C2** 用户对本 v0.2 表述逐项签字 | ⏳ 待 user 审签（v0.2 重写 §1.2 + 加 §1.4 + §1.3 加强后 sign-off 重启）|
| **C3** dev-reviewer 双 Codex 评审 | ⏳ Round 2 待（v0.2 redo 后 batch run with L3.G2 v0.4 + 其他 7 个 PASS closure + L3.G2.E 新立项）|

**关键边界**：

- 本文档**仅** close L1.G4（abstract 迹距离 contraction 数学事实）
- L1.G1 / L1.G2 / L1.G3 / L2.G1-G2 / L2.G4 / L3.G1-G2 维持各自独立 PASS 状态
- L2.G3 / L3.G3 维持 OPEN per R0.1（cross-space / operational-link，AI 不得 close）
- Lemma C counting/normalization residual 维持 OPEN（详见 [path_alpha_subgap_closure_integration_v0_2.md](path_alpha_subgap_closure_integration_v0_2.md) §3.3 + 即将立项的 L3.G2.E 新 closure）
- 升级 [SYN] → [COROLLARY] 仍需 C1 ∧ C2 ∧ C3 完整流程

---

## §5 待启动 C3 R2（v0.2 redo 评审）

让 Codex（diff + holistic 双 reviewer）确认：

1. v0.2 §1.2 重写**完全移除**了 v0.1 的 application 段（"if Π ε-secure then Π_tr ε-secure"），改为 "L1.G4 仅 contributing step；application 层由 L1.G2 + L2.G3 + L1.G4 jointly close"
2. v0.2 §1.3 加强到 5 条 disclaim（特别是新加的"不主张数值 ε 上界"）
3. v0.2 §1.4 新增依赖关系表 explicit 列 L1.G1 / L1.G2 / L2.G3 / L1.G4 各自角色，避免 smuggling 误读
4. v0.2 §2 main citation（KW Theorem 6.3 + §4.4.2）维持 v0.1 Codex round 4 PASS 状态；§2.3 Pirandola Eq. 36 side-citation 已移除
5. v0.2 §3 数值 PASS 维持 v0.1 状态
6. **CRITICAL scope check**：v0.2 是否真的不再 smuggle L1.G2 / L2.G3 任何 application 层结论？是否任何"if Π ε-secure then Π_tr ε-secure"措辞已彻底删除？

**预期 verdict**：PASS（v0.1 REJECTED 触发的具体 scope contradiction 已 explicitly 修复；其他 6 项原 v0.1 已 PASS 维持）

---

## §6 Changelog

- **v0.1** (2026-04-26)：首版 closure；**[RETRACTED 2026-04-26]** per C3 dev-reviewer Round 1 diff REJECTED（§1.2 application 段 smuggled L1.G2 + L2.G3 closure，与 §1.3 explicit scope 矛盾）。原稿保留作 cautionary record。详 [RETRACTION.md §9.1](../research/RETRACTION.md#91-l1g4-v01-closure-撤回)。
- **v0.2** (2026-04-26 same-day)：本版。redo per A1 user authorization (2026-04-26 session 内显式 "重写")。修复策略：保留 §1.1 + §2 + §3（已 PASS 部分），重写 §1.2 移除 application 段，§1.3 加强到 5 条 disclaim，新增 §1.4 依赖关系表，移除 §2.3 Pirandola Eq. 36 side-citation。**C1 维持 v0.1 PASS via (a)+(c)**；C2 + C3 R2 待。
