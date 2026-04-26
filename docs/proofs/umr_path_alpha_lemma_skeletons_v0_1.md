# Path α Lemma Skeletons (v0.1 — Statement-Stub Only, Anchor: Cui 2019)

**版本**：v0.1 [SCAFFOLDING — statement-only stubs, NO proof drafts]
**日期**：2026-04-25
**前身 / 关系**：
- 派生自 [path α v0.3 [USER-APPROVED PRIORITY]](umr_path_alpha_three_lemma_v0_3.md)
- 基于 [PDF synthesis v0.1](umr_path_alpha_pdf_synthesis_v0_1.md) §6.6 + v0.1 update 3 (Cui 2019 直读)
- 引用 [path α scaffolding v0.1](umr_path_alpha_scaffolding.md) 11-gap inventory

**严谨性**：
- ✅ 全文 [SYN] / [DRAFT statement-stub]
- ❌ **不**含任何 lemma proof / Justification sketch
- ❌ **不**升级任何 sub-gap 状态
- ❌ Claude single-AI 直读 ≠ C1 (a)；本文档**不**构成 R0.2 升级证据

---

## §-1 R0.1 / R0.2 显式状态声明

### -1.1 这份文档**不**做什么

- ❌ **不**证明 Lemma A / B / C 任一
- ❌ **不**含 "Justification sketch" / "non-proof argument" 等中间态措辞（v0.2 round 1 trap 教训）
- ❌ **不**升级 [SYN] 到 [COROLLARY]
- ❌ **不**主张 sub-gap 已闭合 —— 全部 11 个 [scaffolding v0.1](umr_path_alpha_scaffolding.md) §5 的 sub-gap **维持 [UNKNOWN]**

### -1.2 这份文档**做**什么

- ✅ 把 path α 三 lemma 的 **statement target** 用 Cui 2019 Eq. (1) Hilbert 空间框架 + Pirandola 2019 SI Note 1 trusted-relay 协议类**精确表述**
- ✅ 标注每个 sub-gap 在新框架下的**精确位置**（哪个步骤需要补什么）
- ✅ 标识可作 C1 验证 entry point 的**具体公式**

### -1.3 与 path α v0.3 banner 的对应

[path α v0.3](umr_path_alpha_three_lemma_v0_2.md) banner 显示：
- ✅ user-approved direction（[PHASE_STATUS §4.5](../PHASE_STATUS.md)）
- ❌ 不等价 C3 PASS（dev-reviewer round 1/2 REJECTED 留痕）

本文档**不**改变上述状态。本文档是 user-approved direction 下的**进一步 scaffolding**，需要 user/cross-family AI/non-AI tool 验证后才能升级。

---

## §1 Anchor Protocol：Cui-Yin-Wang-Chen-Wang-Guo-Han 2019

**选 Cui 2019 作 anchor 的理由**：
1. Page 2 Step 2.a **直接声明** untrusted measurement device controlled by Eve — 这就是 path α 想 bound 的 umr Eve
2. Eq. (1) **形式化整个 Hilbert 空间**结构（Alice ⊗ Bob ⊗ Eve ancilla ⊗ Message）
3. Section III + Appendix A 给出**完整安全证明** against general collective attack
4. Page 3 通过 de Finetti / postselection reduction **延伸到 asymptotic coherent attack**

**备选 anchor**：[Wang 2018 SNS](../literature/pdfs/WangYuHu-2018-SendingOrNotSending.pdf)（"Charlie possibly dishonest"）或 [Ma 2018 PM-QKD](../literature/pdfs/MaZengZhou-2018-PhaseMatchingQKD.pdf)（"untrusted relay held by Eve"）。

**禁用 anchor**：Lucamarini 2018 原版（自己承认 + Wang 2018 给反例 + Cui 2019 引 Tamaki 等 2018 重证）。

---

## §2 Notation & Formal Setup

记号沿用 Cui 2019 Eq. (1) + Pirandola 2019 SI Note 1。

### 2.1 Hilbert space (来自 Cui 2019 Eq. (1))

- $\mathcal{H}_A$：Alice 输出 Fock space (光子数 base $|n\rangle_{A-out}$)
- $\mathcal{H}_B$：Bob 输出 Fock space (光子数 base $|m\rangle_{B-out}$)
- $\mathcal{H}_C$：Charlie's measurement device 局部 Hilbert space
- $\mathcal{H}_E$：Eve ancilla
- $\mathcal{H}_M$：Charlie 公开宣告的 classical message register（含 $|0\rangle_M, |1\rangle_M, |L\rangle_M, |R\rangle_M$ 等态）

### 2.2 UMR 协议 $\Pi$ 的形式化（对应 Cui 2019 Eq. (1)）

UMR 协议下 Charlie 执行的操作是**任意 unitary** $\hat{U}$（由 Eve 选择）后接 measurement：

$$\hat{U}^{\Pi_{umr}}|n\rangle_{A-out}|m\rangle_{B-out}|E_0\rangle_{Ea}|0\rangle_M = \sqrt{Y_{n,m}}|\gamma_{n,m}\rangle_E|1\rangle_M + \sqrt{1-Y_{n,m}}|other\rangle_E|0\rangle_M$$

**$\hat{U}$ 选择 Eve 控制** —— 这就是 umr。

### 2.3 Trusted-Relay 协议 $\Pi_{tr}$ 的形式化（对应 Pirandola 2019 SI Note 1）

Pirandola SI Note 1 page 15 trusted-relay 协议类定义：
> "adaptive LOs performed by all points of the network on their local registers, which are assisted by unlimited two-way CC involving the entire network"

这意味着 Charlie 这个 trusted node 执行**协议规定的固定** local quantum operation $\hat{U}^{spec}$ + classical broadcast。

**Path α 的 embedding 构造**：取 Cui 2019 protocol-specified honest Charlie 操作（即 Cui 2019 Section II Step 3 描述的 honest single-photon interference detection + announcement）作 $\hat{U}^{spec}$；声明 $\Pi_{tr}$ 中 Charlie 执行 $\hat{U}^{spec}$（不再被 Eve 控制）。

---

## §3 Lemma A — Protocol Embedding [DRAFT statement-stub]

### 3.1 Statement target

设 $\Pi$ 是 Cui 2019 simplified TFQKD 协议（in umr setting，Charlie 由 Eve 控制）。定义 $\iota(\Pi) := \Pi_{tr}$ 如下：
- (a) Alice 与 Bob 的 state preparation 和 classical post-processing 操作**与 $\Pi$ 完全相同**
- (b) Charlie 执行 Cui 2019 Section II Step 3 描述的 honest measurement + announcement (即 $\hat{U}^{spec}$ 而非 Eve-chosen $\hat{U}$)
- (c) 声明 $\Pi_{tr}$ 中 Charlie 是 trusted-network node，符合 Pirandola SI Note 1 的"adaptive LOs by all points"协议类

**Statement target**：$\iota(\Pi) = \Pi_{tr}$ 是 Pirandola 2019 SI Note 1 (page 15) 定义的 trusted-relay 协议类的合法成员。

### 3.2 Sub-gap reduction（继承 [scaffolding v0.1](umr_path_alpha_scaffolding.md) §5）

| Sub-gap | 在 §3.1 statement 中的位置 | 闭合需要 |
|---|---|---|
| **L1.G1** $\mathcal{A}_{umr}$ vs $\mathcal{A}_{tr}$ Hilbert 空间对齐 | $\Pi$ 与 $\Pi_{tr}$ 共享 $\mathcal{H}_A \otimes \mathcal{H}_B \otimes \mathcal{H}_C \otimes \mathcal{H}_E \otimes \mathcal{H}_M$；Eve 在 $\Pi$ 控 $\mathcal{H}_C \otimes \mathcal{H}_E$，在 $\Pi_{tr}$ 仅控 $\mathcal{H}_E$ | user 形式化"同一 Hilbert space，不同 Eve access 子集"声明 |
| **L1.G2** embedding $\iota$ 具体构造 | §3.1 (a)/(b)/(c) 三条声明 | user 验证 (b) Cui 2019 honest Charlie operation $\hat{U}^{spec}$ 是 well-defined CPTP / measurement |
| **L1.G3** Stinespring gauge invariance | $\hat{U}^{spec}$ 的 Stinespring dilation 选择 | 标准 quantum information argument |
| **L1.G4** Output state equivalence metric | trace distance / fidelity criterion | 标准（Pirandola Eq. 36 + KW §20.1.17 已支持） |

**所有 4 个 L1 gap 维持 [UNKNOWN]**。**不**做 closure。

### 3.3 关键验证点（user 直读 Pirandola SI Note 1 + Cui 2019 时核对）

- **核对 1**：Cui 2019 Step 3 描述的 Charlie operation（single-photon interference + classical announcement）是否符合 Pirandola "local quantum operation + classical broadcast"
- **核对 2**：Pirandola SI Note 1 "adaptive LOs by all points" 是否覆盖 Charlie 的 measurement + 经典 broadcast (vs 仅 unitary + 经典 communication)
- **核对 3**：$\Pi_{tr}$ 的 channel definitions $\mathcal{E}_{A-C}, \mathcal{E}_{C-B}$ 是否符合 Pirandola SI Note 1 "memoryless quantum channels along edges"

---

## §4 Lemma B — Security Reduction [DRAFT statement-stub]

### 4.1 Statement target

设 $\Pi$ 是 Cui 2019 protocol，已证（per Cui 2019 Section III + Appendix A）对 Cui Eq. (1) 形式 Eve 是 $\varepsilon$-secure。设 $\Pi_{tr} = \iota(\Pi)$。则 $\Pi_{tr}$ 在 trusted-relay 模型下对 Pirandola SI Note 1 / KW §20.1 形式 Eve 也是 $\varepsilon$-secure。

### 4.2 Eve set 关系（继承 path δ §1.4 / α.G2.E）

记：
- $\mathbb{E}_{Cui}$ := Cui 2019 Eq. (1) Eve 集合 = arbitrary unitary on $\mathcal{H}_A \otimes \mathcal{H}_B \otimes \mathcal{H}_C \otimes \mathcal{H}_E$ + measurement on $\mathcal{H}_M$
- $\mathbb{E}_{tr}$ := Pirandola/KW §20.1 trusted-relay Eve = isometric extension on $\mathcal{H}_E$ only + classical access to $\mathcal{H}_M$

**Statement target B.a**：$\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$（trusted Eve 是 umr Eve 的 strict subset）

**Statement target B.b**：trace distance contraction: $\|\rho^{\Pi_{tr}}_{ABE_{tr}} - \overline{\Phi}_{AB} \otimes \sigma_{E_{tr}}\|_1 \leq \|\rho^{\Pi}_{ABE_{Cui}} - \overline{\Phi}_{AB} \otimes \sigma_{E_{Cui}}\|_1$（partial trace contraction）

### 4.3 Sub-gap reduction

| Sub-gap | §4.2 中的位置 | 闭合需要 |
|---|---|---|
| **L2.G1** rate-direction sign | $\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$ → $R^{\Pi_{tr}}_{tr} \geq R^{\Pi}_{Cui}$ | user 显式核对方向（避免 v1 retraction sign-flip trap） |
| **L2.G2** ε-composable 三分量 | 是 $\Pi$ 整体 ε security 还是 secret/correct/complete 分别 | Portmann-Renner 2022 standard |
| **L2.G3** Eve set across spaces | §4.2 B.a 的 ⊆ 关系 | user 显式声明：trusted-relay Eve 仅访问 $\mathcal{H}_E$，**不**触 $\mathcal{H}_C$ |
| **L2.G4** non-LOCC joint attack | Cui Eq. (1) 已是 most general collective + asymptotic coherent (page 3) | Cui 2019 已 cover；finite-key 留待后续 |

**所有 4 个 L2 gap 维持 [UNKNOWN]**。L2.G3 由 Cui 2019 Eq. (1) 框架显著简化（umr Eve 与 trusted-relay Eve 在同一 Hilbert space，仅 access 子集不同）。

### 4.4 关键验证点

- **核对 4**：Cui 2019 Section III 安全 statement 是否 ε-composable（vs ε on fidelity only）
- **核对 5**：Curras-Azuma-Lo 2018 [arXiv:1807.07667] 的 entanglement-distillation-based proof 是否给 Lemma B partial trace argument 直接 citation（**待 user 补 PDF**）
- **核对 6**：KW §20.2 SKA ↔ private-state distillation purification trick 在 Cui 2019 Eve 模型下是否直接适用

---

## §5 Lemma C — Rate Definition Alignment [DRAFT statement-stub]

### 5.1 Statement target

设 $R_{Cui}(\Pi)$ = Cui 2019 Eq. (3) 给出的 secret key rate，$R_{Pirandola}(\Pi_{tr})$ = Pirandola 2019 SI Note 1 trusted-chain capacity rate。则：

**Statement target C**：在 channel use 计数对齐 + 同 ε-secure criterion 下，$R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$

### 5.2 Sub-gap reduction

| Sub-gap | §5.1 中的位置 | 闭合需要 |
|---|---|---|
| **L3.G1** LOPC syntax 跨 topology | Cui Step 3 announcement vs Pirandola "two-way CC" | user 显式 reconcile（KW §20.1.12 LOPC channel 公式是 baseline） |
| **L3.G2** Key length cross-topology | Cui Eq. (3) Devetak-Winter rate vs Pirandola Eq. 8 ε-close to private state | Portmann-Renner 2022 standard |
| **L3.G3** Pirandola Eq. 11 适用 in $\iota(\Pi)$ | $\Pi_{tr}$ 是 trusted-relay 协议 → Pirandola Eq. 11 直接 apply | 取决于 L1.G2 (Lemma A 合法性) |

**所有 3 个 L3 gap 维持 [UNKNOWN]**。

### 5.3 关键验证点

- **核对 7**：Cui Eq. (3) channel use 计数（"per trial"）是否对齐 Pirandola "n channel uses"
- **核对 8**：Cui 安全 ε（implicit in Devetak-Winter formula）与 Pirandola ε-close to private state 是否等价

---

## §6 Combined Chain — **CONDITIONAL** [SYN]（v0.3 修正：post-split L3.G3 + L3.G2.E + Pirandola Eq. 11 specialization chain）

**严格条件句**（v0.3 修正 per 2026-04-26 C3 R2 holistic finding：原 v0.2 form 还引"Lemma C counting residual"作独立项，但该 residual 已被 newly opened sub-gap **L3.G2.E** 吸收）：

**If** all **12 sub-gaps** —— 即 11 原 sub-gaps (L1.G1, L1.G2, L1.G3, L1.G4, L2.G1, L2.G2, L2.G3, L2.G4, L3.G1, L3.G2, L3.G3) **PLUS L3.G2.E**（newly opened 2026-04-26，从原 L3.G3 sub-residual 4 "channel-use accounting" split-out 而来；详 [path_alpha_l3g2e_closure_v0_1.md](path_alpha_l3g2e_closure_v0_1.md)）—— **with post-split L3.G3 reduced to 5 sub-residuals**（citation specialization / parameter-id / symmetry / protocol-model / edge-model）**AND** Pirandola Eq. 11 specialization chain (Eq. (8)/(9) lossy chain + tele-covariance + symmetric η split) are independently established **then**:

$$\underbrace{R_{Cui}(\Pi)}_{\text{TF-QKD 密钥率, Cui Eq. (3)}} \stackrel{\text{Lemma A+B+C [SYN, conditional]}}{\leq} \underbrace{R_{Pirandola}(\Pi_{tr})}_{\text{end-to-end 网络 secret-key capacity}} \stackrel{\text{Pirandola 2019 Eq. 11 (REE cut bound) [THM]}}{\leq} \underbrace{\min_C E_R(C)}_{\text{REE 最小切割流, Eq. 10/11}} \stackrel{\substack{\text{Eq. (8)/(9) lossy chain specialization} \\ \text{+ tele-covariance + sym η split [conditional]}}}{=} \underbrace{-\log_2(1-\sqrt{\eta_{AB}})}_{\text{single-repeater bound, N=1 equidistant}}$$

**v0.1 → v0.2 错误修正**（per [c1a-l3g3-gap-identification-round1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md) §A direct PDF read + [RETRACTION.md §9.3](../research/RETRACTION.md#93-l3g3-gap-id-round-揭露重大-pirandola-eq-11-citationspecialization-错误)）：

**v0.1 form (错)**：

```
... ≤ R_Pirandola(Π_tr) [Pirandola Eq. 11 [THM]] ≤ -log_2(1-√η_AB)
```

**错在**：直接把 Pirandola Eq. 11 等同 `-log_2(1-√η_{AB})` single-repeater bound。**实际** Pirandola 2019 Eq. 11 是 `C(N) ≤ min_C E_R(C)`（REE cut bound; main PDF p.4），**不**直接给 specific η-form。`-log_2(1-√η_{AB})` 来自 Eq. (8)/(9) lossy chain specialization（main PDF p.3），需要 (i) tele-covariance（pure-loss bosonic）+ (ii) distillability + (iii) symmetric / equidistant η split (`η_{AB} = η_{AC}·η_{BC}`)。

**v0.2 form (修正)**：上式分两步：(a) Pirandola Eq. 11 给 REE cut UB `min_C E_R(C)` [THM]；(b) Eq. (8)/(9) specialization 给 `-log_2(1-√η_{AB})` [conditional on tele-cov + sym η split]。

**Status**（v0.3 修正后）：[SYN, conditional on **{12 sub-gaps with post-split L3.G3 = 5 sub-residuals + Eq. 11 specialization chain}**]（**post-2026-04-26 C3 R2 holistic state**：原 v0.2 form 引"Lemma C counting residual"作独立项，但该 residual 已被 newly opened sub-gap **L3.G2.E** 吸收 → 12 sub-gaps + Eq. 11 specialization chain；v0.1 form 误为 11 OPEN）

**Strict scope**：在 Cui 2019 anchor 协议下，bosonic-asymptotic 区间，asymptotic（finite-key 不在 scope）+ Cui's A-Charlie + B-Charlie pure-loss bosonic edges (assumed for tele-covariance) + symmetric η split (`η_{AB} = η_{AC}·η_{BC}`)

**对外引用资格**：[NONE] until R0.2 (C1 ∧ C2 ∧ C3) 完整流程 + 全部 **12 sub-gap** PASS（含 newly opened L3.G2.E）+ post-split L3.G3 5 sub-residual close + Eq. 11 specialization chain verify

**Cross-link**：详 [path_alpha_subgap_closure_integration_v0_3.md](path_alpha_subgap_closure_integration_v0_3.md) §4（v0.2 已 [SUPERSEDED]）。

---

## §7 验证 entry points 清单（user 直读 PDF 时的具体核对项）

按 §3-§5 的 8 个 "关键验证点"汇总，user 在 paper-level work 时应在以下文献位置对照核对：

| 核对点 | 引用位置（user 直读时核对） |
|---|---|
| 1, 2, 3 (Lemma A) | [Pirandola 2019 SI Note 1, page 15](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf) + [Cui 2019 Section II Step 3](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf) |
| 4, 5, 6 (Lemma B) | [Cui 2019 Section III + Appendix A Eq. (A1)-(A7)](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf) + KW Ch 20 §20.2 (purification trick) + Curras-Azuma-Lo 2018 (待补 PDF) |
| 7, 8 (Lemma C) | [Cui 2019 Eq. (3)-(4)](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf) + Pirandola 2019 SI Note 1 Eq. (91)-(92) + KW Ch 20 §20.1 Eq. (20.1.17)-(20.1.18) |

---

## §7.x 用户验证响应记录（2026-04-26 session）

**Banner**：本节记录 user 对 §7 八个核对点（§3.3 + §4.4 + §5.3）的判断响应。**这是 user judgment**，**不**等价 R0.2 C1(b) 直读 PDF 形式化验证（除非 user 单独显式声明已直读 PDF 并形式化核对）。**所有 11 sub-gaps 维持 [UNKNOWN]**。

### §7.x.1 用户响应汇总（user message 2026-04-26 verbatim）

> "1、是；2、是；3、是；4、是；5、你下载pdf，然后精度找支持的点；6、是；7、这个你再核对一下；8、等价"

| 核对点 | 用户判断 | Claude 后续动作 |
|---|---|---|
| 1. Cui Step 3 honest Charlie ⊆ Pirandola "local quantum operation + classical broadcast" | **是** | 记录为 user judgment；待 C1(b) 直读 PDF 二次确认 |
| 2. Pirandola "adaptive LOs by all points" 覆盖 Charlie measurement + 经典 broadcast | **是** | 同上 |
| 3. $\Pi_{tr}$ channel definitions 符合 Pirandola "memoryless quantum channels along edges" | **是** | 同上 |
| 4. Cui Section III 安全 statement ε-composable | **是** | 同上 |
| 5. Curras-Azuma-Lo 2018 给 Lemma B partial trace argument 直接 citation | **user 委托 Claude 下载 PDF 找支持点** | **§7.x.2 已执行** |
| 6. KW §20.2 SKA ↔ private-state purification trick 在 Cui Eve 模型下适用 | **是** | 记录为 user judgment；待 C1(b) 二次确认 |
| 7. Cui Eq. (3) per-trial 与 Pirandola "n channel uses" 对齐 | **user 要求 Claude recheck** | **§7.x.3 已执行** |
| 8. Cui ε（Devetak-Winter）与 Pirandola ε-close to private state 等价 | **等价** | 记录为 user judgment；待 C1(b) 二次确认 |

**严格 caveat（R0.2 红线维持）**：

- 上述 user 判断在 R0.2 框架下（**仅 evidence 层面，非 gate 满足层面**）：
  - **C2 (user signature) — RELEVANT EVIDENCE, NOT GATE-SATISFIED**：user "是" / "等价" 响应是 user explicit position，但**仅 direction-level**（v0.3 banner = USER-APPROVED PRIORITY direction；user **未**对 §3-§5 具体 lemma statement / scope / grading 单独签字）。**C2 升级闸门未满足** —— 升级 [SYN] → [COROLLARY] 仍需 user 对 §3-§5 三 lemma 表述 + §6 conditional chain + §7 验证点**逐项**显式签字（per §8.2 C2 条款）
  - **C1(b) — CROSS-REFERENCE CANDIDATE EVIDENCE ONLY [USER-CONFIRMED DIRECT-PDF READ 2026-04-26]**：user 后续显式确认（message: "1、前者"）"是" 判断基于**直读 PDF 原文**（Pirandola SI Note 1 + Cui 2019 + KW Ch 20）。这构成 **C1(b) cross-reference candidate evidence**（针对 8 个 textual alignment checks 层面），**不**构成 sub-gap closure 层面的 C1(b) PASS（后者要求 user 本人对每个 sub-gap 做完整 pen-and-paper formalization，远超 cross-reference checks 范围）
  - **C1(a) — RUNNING**：跨家族 AI 双方直读 PDF 已启动（Codex 直读 Cui 2019 + Pirandola SI Note 1 + Curty 2018；results pending，will be recorded at §7.x.5 once complete）
  - **C3 — RUNNING**：dev-reviewer round 3 已启动（diff + holistic parallel Codex review；results pending，will be recorded at §7.x.5 once complete）
- **关键限制（不可跨越）**：
  - "Cross-reference textual alignment evidence" ≠ "sub-gap closure pen-and-paper formalization"
  - 11 sub-gaps 各自 closure 仍需**独立**完整 formalization 工作
  - 任何 sub-gap **不因本节 user 响应闭合** —— [UNKNOWN] 维持
  - 升级 [SYN] → [COROLLARY] 需 (C1 ∧ C2 ∧ C3) 三闸门在 sub-gap 层面**同时**通过；本节仅记录 cross-reference 层 evidence accumulation

### §7.x.2 核对点 5：Curty-Azuma-Lo 2018 PDF 直读结果

**PDF**：[Curty-Azuma-Lo-2018-SimpleSecurityTwinField.pdf](../literature/pdfs/Curty-Azuma-Lo-2018-SimpleSecurityTwinField.pdf) (arXiv:1807.07667v2, 2018-12-18, 11 pages)

**Claude 直读 11 页全文** —— 提取与 Lemma B partial trace argument 相关支持点：

**支持点 5.1：Eve 完全控制 node C 的形式化（page 3, "Security proof of Protocol 3"）**

> "without loss of generality, we shall assume that the node C is under the full control of an eavesdropper, Eve. After a QKD run, Alice and Bob can estimate the conditional probability distribution $p_{ZZ}(k_c, k_d|β_A, β_B)$..."

**与 path α 关系**：直接对应 Cui 2019 Eq. (1) 的 untrusted-Charlie 设定。Curty 2018 与 Cui 2019 在 Eve 模型层面**完全一致**。

**支持点 5.2：Virtual entanglement state 框架（page 4, around Eq. (10)）**

> "if Alice and Bob choose the X basis in step (i'') of Protocol 3, Eve cannot distinguish this step from the following fictitious step: Alice (Bob) prepares an optical pulse a (b) and a qubit A (B) in an entangled state $|\psi_X\rangle_{Aa} = (|+\rangle_A|\alpha\rangle_a + |-\rangle_A|-\alpha\rangle_a)/\sqrt{2}$"
>
> "By running this fictitious step together with steps (ii)-(iv) in order, Alice and Bob obtain a state $|\chi_{k_c,k_d}\rangle_{Aa'Bb'} := \hat{M}^{ab}_{k_c,k_d}|\psi_X\rangle_{Aa}|\psi_X\rangle_{Bb} / \sqrt{p_{XX}(k_c,k_d)}$"

**与 path α Lemma B 关系**：Curty 2018 用**reduced state after Charlie's announcement** $|\chi_{k_c,k_d}\rangle_{Aa'Bb'}$ 作 phase-error rate 计算基础。这是 Lemma B partial trace argument 的**直接 textual analog**：从 umr Eve 视角的全局 state $\rho^\Pi_{ABCE}$，partial trace 掉 Charlie 的 ancilla，得到 announcement-conditioned reduced state。

**支持点 5.3：Phase-error rate 公式（Eq. 11）**

$$e_{Z,k_c,k_d} = \sum_{i,j=0,1} \|_{AB}\langle jj\| \chi_{k_c,k_d}\rangle_{Aa'Bb'}\|^2$$

**与 path α 关系**：phase-error rate 直接由 announcement-conditioned reduced state 决定，**无需** trust Charlie 的内部 unitary $\hat{U}$ —— 这就是"trace out Eve-controlled $\mathcal{H}_C$"的具体实现。

**支持点 5.4：√η scaling claim（Abstract + Conclusion）**

> Abstract: "the secret key rate of our protocol has a square-root improvement over the point-to-point private capacity"
>
> Page 4 right column: "the net transmittance of the signal is thus of order $\sqrt{\eta}$, which leads to a very high key rate for TF-type QKD at long distances"

**与 path α 关系**：Curty 2018 与 Cui 2019 共同支持 "TF-type per-trial rate scales as $\sqrt{\eta}$" 这一结论。

**支持点 5.5：MDI-QKD inheritance 声明（page 5, Conclusion）**

> "this protocol could also be regarded as a phase-encoding MDI-QKD scheme with single-photon interference. Indeed, it inherits the major advantage of standard MDI-QKD, *i.e.*, it is robust against any side channel in the measurement unit."

**与 path α 关系**（**严格在 untrusted-Charlie picture 内部**）：Curty 2018 这一段表明 announcement-conditioned reduced-state 框架在 measurement-unit 受 Eve 控制下仍能 quantify phase-error。这是**untrusted-Charlie internal robustness** 的 technical 旁证，**不**直接支持 Lemma A protocol embedding 合法性 —— Curty 2018 自己**未**走 path α 想做的 $\Pi \to \iota(\Pi) = \Pi_{tr}$ 嵌入路径，全证明仅在 umr Eve picture 下完成，**未** invoke "trusted-relay protocol class"概念。Lemma A 嵌入合法性 closure 仍需独立工作（L1.G2 [UNKNOWN] 维持）。

**支持点 5.6：与 Koashi 2009 / Azuma's inequality 的 framework alignment（page 5）**

> "(...) is a convex function over probabilities that can be obtained by performing positive operator-valued measure (POVM) measurements on a quantum state realized in a virtual scenario. This is enough [43] to prove the security of Protocol 3 against coherent attacks, thanks to Azuma's inequality [44]."

**与 path α 关系**：Curty 2018 用 Koashi 2009 complementarity-based proof + Azuma's inequality 把 collective attack 推广到 coherent attack。Cui 2019 用 de Finetti / postselection。**两条路径独立**给出 asymptotic coherent security，path α Lemma B 在此选 Cui 2019 anchor 时**无需** Curty 路径的具体技术，但 Curty 路径是**独立旁证**。

**核对点 5 verdict（Claude judgment，需 user / cross-family AI 二次确认）**：

- ✅ Curty 2018 在 **untrusted-Charlie picture 内部**为 announcement-conditioned reduced-state 框架（Lemma B partial-trace argument 的技术 foundation）提供 textual citation —— Eq. (10)-(11)
- ✅ Curty 2018 支持 √η scaling claim 与 MDI-style measurement-unit-robustness 声明（仍在 untrusted-Charlie picture 内部）
- ⚠️ Curty 2018 **不**给"trusted-relay reduction" claim —— 全证明在 untrusted-Charlie picture 下完成，**未** invoke "trusted-relay protocol class"，**未**走 $\Pi \to \iota(\Pi) = \Pi_{tr}$ 嵌入路径
- ⚠️ 因此 Curty 2018 仅是 **Lemma B 内部 technical foundation citation**（announcement-conditioned reduced-state 框架），**不**等价：(i) Lemma A protocol embedding 合法性 (L1.G2)；(ii) Lemma B Eve-set ⊆ 关系 (L2.G3)；(iii) Lemma C rate alignment (L3.G1-G3)。任何 cross-space / cross-task 转移仍 [UNKNOWN]

**对 sub-gap 状态的影响**：**无**。L2.G3 (Eve set across spaces) 仍 [UNKNOWN]。Curty 2018 的 reduced state 框架是**有用的 foundation**，但 path α 嵌入论证仍需独立 close。

### §7.x.3 核对点 7：Cui Eq. (3) 与 Pirandola "channel use" 对齐 recheck

**user 要求 recheck**。Claude 重读 Cui 2019 page 2 + Pirandola 2019 SI Note 1 page 15：

**Cui 2019 Eq. (3) 计数单位（page 2 verbatim）**：

> "According to Devetak-Winter's bound [24], the secret key rate **per trial** in a code mode is then given by $R = Q_\mu[1 - fh(e_\mu, 1-e_\mu)] - I^u_{AE}$"

**"trial" 定义（Cui page 2, Step 1-3）**：每个 trial = (a) Alice/Bob 各选 code/decoy mode；(b) Alice/Bob 各送一个 pulse 给 Eve；(c) Eve 公开 announce $|1\rangle_M$ (success) 或 $|0\rangle_M$ (failure)，及 success 时 announce $|L\rangle_M$/$|R\rangle_M$。

**所以**：每个 trial 使用 quantum channels 的次数 = 1 次 A→Charlie + 1 次 B→Charlie = 2 次 (但是 in parallel；不是 2 次同一 channel)。

**Pirandola 2019 SI Note 1 chain bound（per [PDF synthesis v0.1 update 1](umr_path_alpha_pdf_synthesis_v0_1.md)，并经 §7.x.5 C1(a) Codex 直读 SI Note 1 p.15 Eq. (91)-(92) 校正）**：

- 对 N+1-channel chain（N=1 即 single-repeater 即 A-C-B）：chain capacity ≤ $-\log_2(1 - \eta_{min})$
- **Pirandola 实际语言**：rate 定义为 "**bits per chain use**" / "per sequential use of the network"（per C1(a) Codex direct-PDF read）。SI Note 1 **未** explicitly 表述 "per bottleneck-link use" — 这是 N=1 lockstep counting inference，**非** Pirandola 原文术语
- 对称 umr setting：$\eta_{AC} = \eta_{BC} = \sqrt{\eta_{AB}}$，所以 $\eta_{min} = \sqrt{\eta_{AB}}$，chain bound = $-\log_2(1 - \sqrt{\eta_{AB}})$ per chain use

**对齐方式（Claude recheck 后表述，corrected per C1(a) Codex finding）**：

每个 Cui trial → **1 次 chain use**（即 A-C 与 B-C 各用 1 次，lockstep 同步）。所以：

$$R_{Cui}\text{ (per trial)} \stackrel{\text{每 trial = 1 次 chain use (N=1 lockstep)}}{\equiv} R_{Cui}\text{ (per chain use)} \stackrel{\text{Pirandola chain bound}}{\leq} -\log_2(1 - \sqrt{\eta_{AB}})$$

**关键技术 caveat（path α v0.3 §6 sub-gap L3.G2 涉及；C1(a) Codex finding 已合并）**：

1. **"per trial" = "per chain use" 仅在 N=1 lockstep 对称 setting 下直接成立**：
   - "per total use" 计数下，每 trial = 2 次 quantum channel use（A-C + B-C），**非** 1 次
   - "per chain use" counting 把 1 次 trial 视为 "1 次 network sequential use"，**这是 N=1 lockstep 的特殊情形**
   - **不对称 case**（$\eta_{AC} \neq \eta_{BC}$）或非-lockstep 使用下需重新核对
2. **Pirandola SI Note 1 实际语言**（per C1(a) Codex direct-PDF read 校正）：
   - 原文用 "bits per chain use" / "per sequential use of the network"，**非** "per bottleneck-link use"
   - "per bottleneck-link use" 措辞是 Claude 此前的 inference，**不**严格等价 Pirandola 原文；本节已替换为 "per chain use"
   - SI Note 1 Eq. (91)-(92) 的具体计数定义对齐**仍需 user 二次直读**
3. **Devetak-Winter rate 与 capacity rate 的 limiting alignment**：
   - Cui Eq. (3) 是**asymptotic per-trial rate**（从 Devetak-Winter formula 推）
   - Pirandola chain bound 是 **n→∞ 极限 capacity**（per chain use）
   - 这两个 "asymptotic limit" 的具体定义 + 收敛意义对齐需 user / cross-family AI 直读 Pirandola SI Note 1 page 15 公式 (91)-(92) 二次确认

**Cui Fig 1 自洽性（独立旁证）**：

Cui 2019 page 3 Fig 1 caption：

> "the linear key rate bound (blue) [16] and the bound with a single repeater (dotted blue) [27] are also shown in the figure"

Cui 2019 page 3 正文：

> "Note that the slope of the key rate in our protocol is the same as the linear bound with a single repeater [27] when the fiber loss is less than 60 dB"

**含义**：Cui 2019 作者**自己**就在 Fig 1 把自己的 per-trial rate 与 single-repeater bound（即 Pirandola single-repeater chain bound 的 [27] = Pirandola-Laurenza-Ottaviani-Banchi 2017）直接做横坐标-纵坐标比较，**默认**计数单位对齐（"per trial" vs "per channel use" 在 horizontal axis "Loss [-10 log10(η)] Alice-Bob (dB)" 下做直接 visual 比较）。

**这是 path α §3.1 数值 simulation 的依据** —— Cui 自己已在文献中做这一对齐。但 user 直读 + 显式形式化核对**仍有必要**（Cui Fig 1 是 visualization，**不**等价 formal alignment statement）。

**核对点 7 verdict（Claude recheck，C1(a) Codex direct-PDF finding 已合并）**：

- ✅ "per trial = per chain use" 对齐**在 N=1 对称 umr + lockstep 使用前提下成立**（per C1(a) Codex point 7 PASS）
- ⚠️ "per bottleneck-link use" **非** Pirandola 原文术语 —— Pirandola 用 "bits per chain use" / "per sequential use of the network"。前者是 Claude 此前的 inference，已在本节替换为后者
- ✅ Cui 2019 Fig 1 自身已 implicit 做 "per trial vs single-repeater bound" 比较（独立旁证）
- ⚠️ Pirandola SI Note 1 Eq. (91)-(92) 的"chain use"显式计数定义**仍需 user 二次直读**
- ⚠️ 不对称 case（$\eta_{AC} \neq \eta_{BC}$）或非-lockstep 使用的对齐**未在 path α v0.3 scope 内**，留作 future extension

**对 sub-gap 状态的影响**：**无**。L3.G2 (Key length cross-topology) 仍 [UNKNOWN]。但本 recheck 给 user 直读 Pirandola SI Note 1 page 15 时**精确定位**应核对的具体公式（Eq. (91)-(92)）。

### §7.x.4 当前进度小结（2026-04-26 session）

**已完成**：
- 8/8 核对点有响应（6 user "是" + 1 Claude PDF 直读 + 1 Claude recheck）
- Curty-Azuma-Lo 2018 PDF 已下载并 11 页全文直读，技术支持点提取
- Cui Eq. (3) "per trial" 与 Pirandola chain bound "per channel use" 对齐已重做

**未变更**：
- 11 sub-gaps **全部维持 [UNKNOWN]**
- path α v0.3 banner（[USER-APPROVED PRIORITY 2026-04-25, NOT C3-passed]）维持
- FINDINGS / PHASE_STATUS / RETRACTION **未**编辑
- 没有 [SYN] → [COROLLARY] 升级
- dev-reviewer round 3 **未**自主提交

**已记录的 user 决定（2026-04-26 message: "1、前者；2、这是要提交codex审核吗，那提交吧；3、启动"）**：

1. user 已直读 Pirandola SI Note 1 + Cui 2019 原文 → §7.x.1 已记为 **C1(b) cross-reference candidate evidence**（**仅** cross-reference 层面，**不**等价 sub-gap closure 层面 PASS；后者需 user 本人对每个 sub-gap 做完整 pen-and-paper formalization）
2. dev-reviewer round 3 已提交：parallel diff (xhigh) + holistic (high) Codex review
3. C1(a) 跨家族直读 PDF 已启动：Codex 直读 Cui 2019 + Pirandola SI Note 1 + Curty 2018，pdftotext 提取 + per-point PASS/FAIL/UNCERTAIN verdict

**已完成的 review 结果**（详见 §7.x.5）：
- dev-reviewer round 3 diff + holistic verdict（C3 gate）
- C1(a) Codex direct-PDF 8 点 verdict（C1(a) gate）

### §7.x.5 Review 结果汇总（2026-04-26 同日完成）

#### §7.x.5.1 dev-reviewer round 3 — C3 gate

**Round 3 输入**：v0.3 文档 + 本节 §7.x.1 - §7.x.4 增量

**Diff Reviewer (Codex gpt-5.4 xhigh)** verdict: **FAIL**（2 majors，0 critical）— see [review-diff-3.json](../workflow/umr-path-alpha-three-lemma-v0-2/review-diff-3.json)

| Issue | Severity | Location | Description |
|---|---|---|---|
| C2 over-claim | major | §7.x.1 line 226 | 原文 "C2 已满足" 越权；direction-level approval **不**等价 C2 升级闸门满足 |
| Curty 5.5 wording smuggle | major | §7.x.2 line 274 | 原文 "直接支持 Lemma A protocol embedding 的合法性" 在 untrusted-Charlie picture 内部 smuggle 了 cross-space bridge |

**Holistic Reviewer (Codex gpt-5.4 high)** verdict: **FAIL**（concurring）— see [review-holistic-3.md](../workflow/umr-path-alpha-three-lemma-v0-2/review-holistic-3.md)

- Convergent issues：(1) C2 over-claim；(2) Curty wording drift
- New minor：§7.x.5 placeholder 引用但当时 section 不存在（**本 §7.x.5 现已实际写入，minor resolved**）
- All trap memory checks PASS（5th + 6th）
- All R0.1/R0.2/R0.3 红线 PASS（11 sub-gaps [UNKNOWN] 维持，no autonomous upgrade）
- v0.3 banner intact

**Round 3 fixes applied**（同 session）：
- §7.x.1 重写 C2 / C1(b) wording → "evidence not gate-satisfied" / "cross-reference candidate evidence only"
- §7.x.2 5.5 重写 → 严格在 untrusted-Charlie picture 内部 + 明示 Curty **不**走 Π → Π_tr 嵌入
- §7.x.5 实际写入

**Round 4 dev-reviewer 状态**：待提交（基于本节 fixes 后的最新 baseline）

#### §7.x.5.2 C1(a) cross-family direct-PDF verification — Codex gpt-5.4 xhigh

**Reviewer**：Codex（独立于 Claude，跨 AI 家族）— see [c1a-codex-pdf-verification.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-codex-pdf-verification.md)

**PDFs read directly via pdftotext**：
- Cui 2019 pp.1-6（Section II Step 3 / Section III / Eq. (1) / Eq. (3) / Appendix A）
- Pirandola 2019 pp.2-3, 7-8, 15-21（Eq. (11) / Eq. (36) / SI Note 1 Eq. (91)-(92) / SI Note 2 network model）
- Curty-Azuma-Lo 2018 pp.3-5（Eq. (10) / Eq. (11) / Conclusion）

**Per-point verdict**（aggregate: **PARTIAL**，5 PASS / 2 FAIL / 1 UNCERTAIN）：

| 点 | Codex Verdict | Codex Cite/Comment |
|---|---|---|
| 1 | **PASS** | Cui p.2 Step 3 "publicly announce" + Pirandola SI Note 1 p.15 "broadcasts classical information" + "conditional LOs" → textual alignment 直接 |
| 2 | **PASS** | Pirandola SI Note 1 p.15 "adaptive LOs by all points + broadcast/feedback" 覆盖 Charlie measurement+broadcast at LOCC level（"NOT just unitary+CC" 是 inference, 非原文显式对比） |
| 3 | **PASS** | Pirandola SI Note 2 p.20 "memoryless quantum channels along edges" + chain channels $E_i$ → trusted A-C-B chain 符合 |
| 4 | **FAIL** | Cui Section III 仅声称"asymptotic security against coherent attacks"；Appendix A 用 Holevo/Devetak-Winter，**未** explicit 写 ε / composable / trace-norm / private-state criterion |
| 5 | **PASS** | Curty p.3 "full control of node C" + p.4 announcement-conditioned $\|\chi_{k_c,k_d}\rangle$ + Eq. (11) phase-error rate from reduced state → direct citation for Lemma B partial-trace argument |
| 6 | **UNCERTAIN** | KW Ch 20 §20.2 PDF **不在** docs/literature/pdfs/；Cui/Pirandola/Curty 中**未**找到等价 SKA ↔ private-state purification trick textual statement |
| 7 | **PASS** | Cui p.2 Eq. (3) per trial + Pirandola SI Note 1 p.15 "bits per chain use" Eq. (91) → N=1 lockstep 下对齐成立。**但** Pirandola **未** explicit 写 "per bottleneck-link use" — 那是 inference |
| 8 | **FAIL** | Cui Eq. (3) / Eq. (A6) 用 asymptotic Devetak-Winter/Holevo rate；Pirandola Methods pp.7-8 用 trace-norm ε-closeness to private state。Cui **未** textually equate 两者 |

**Trap memory cross-check by C1(a) Codex**：

- ✅ **5th trap PASS**：Curty 2018 stays in untrusted-Charlie picture，**未** textually walk Π → ι(Π) = Π_tr
- ⚠️ **6th trap WARNING**：Pirandola 显式定义 "bits per chain use" / "per sequential use of network"，**未** explicit "per bottleneck-link use" — Claude 之前的措辞是 inference，已在 §7.x.3 corrected

**C1(a) Recommendations 给 user**：
1. Π → Π_tr 结构嵌入仍需 human paper-based formalization；Curty 2018 不闭合此 gap
2. 点 4 + 8 的 ε-composable / private-state-equivalence 在 Cui 原文**无** textual 直接 support。需要追加 primary citation（如 Portmann-Renner 2022 / Tomamichel 2016）explicitly map Cui-style asymptotic security 到 ε-composable definition；或暂时把这两点视为 unsupported
3. 点 6 SKA ↔ private-state purification trick 需 KW Ch 20 PDF 或其他 primary source
4. 计数对齐严格表述为 "per trial = per chain use"（N=1 lockstep），**避免** "per bottleneck-link use" 措辞除非另行 formalize（已在 §7.x.3 corrected）
5. **所有 11 path α sub-gaps 维持 [UNKNOWN]** —— 本 C1(a) 通过**未** upgrade 任何 [SYN] 或 close 任何 lemma

#### §7.x.5.3 三 reviewer verdict 综合

| Reviewer | Verdict | Critical Findings |
|---|---|---|
| Round 3 diff | FAIL | C2 over-claim + Curty 5.5 smuggle (both fixed) |
| Round 3 holistic | FAIL | Concurring + minor §7.x.5 missing (now written) |
| C1(a) Codex direct-PDF | PARTIAL (5/8 PASS) | Points 4 + 8 unsupported by Cui text；Point 6 KW Ch 20 unavailable；Point 7 wording corrected |

**对 sub-gap 状态的影响**：**11 sub-gaps 全部维持 [UNKNOWN]**。**关键新发现**：

- 用户 "是" 判断（点 4）/ "等价" 判断（点 8）与 Codex 直读 Cui 原文 textual 结果**有分歧** —— 这**不**等于用户判断错误，而是说明 ε-composable security 在 Cui 2019 原文中**不显式**
- 点 6 仍 [UNKNOWN]（KW Ch 20 PDF 缺失）
- 点 7 措辞已 corrected per C1(a) finding（"per chain use" 替代 "per bottleneck-link use"）

#### §7.x.5.4 用户对 C1(a) PARTIAL 分歧的处置决定（2026-04-26 same-day）

用户消息 2026-04-26（继续 review 后）：
> "点4:选项B；点6按你说的来"
> "点4让codex后面评审的时候不要再提出这个质疑"

**点 4（Cui Section III ε-composable）— 用户决定：选项 B (USER-ACCEPTED IMPLICIT BRIDGE)**

- **用户接受**：Cui 2019 原文未 explicit 写 ε / composable / trace-norm / private-state criterion，但**接受** "Devetak-Winter framework 内部隐含 composable security" 的标准量子信息论假设作为 working position
- **状态**：作为 USER-ACCEPTED implicit bridge 留痕；**非** sub-gap closure
- **future work item**：若需 paper-level publish-grade 证据，仍可追加 Portmann-Renner 2022 / Tomamichel 2016 等 primary citation 把 Devetak-Winter asymptotic rate explicitly bridge 到 ε-composable / private-state criterion
- **CODEX REVIEWER DIRECTIVE [USER-ISSUED 2026-04-26]**：未来 dev-reviewer 评审**不**应再以 "Cui 原文无 explicit composable security textual support" 为由把点 4 列为 issue。此为 user-accepted Option B，与 v0.3 §7.3 USER-APPROVED PRIORITY 同性质 user-issued reviewer scope 限制
  - **directive 边界**（**不**可 user-override）：
    - 若**新文档**（非本节范围）声称 Cui 已 explicit ε-composable → 仍需 Codex 标 issue（这是另一类 upgrade attempt，与本 directive 无关）
    - 若 path α 任一 sub-gap 试图基于 "implicit composable bridge" 自行 close → 仍是 R0.2 越权（C1 ∧ C2 ∧ C3 不满足）
    - 本 directive 仅 silence "点 4 textual support 缺失" 这一具体 issue 不在 future Codex review 中 re-raise

**点 8（Cui ε ↔ Pirandola ε-close-to-private-state）**：

- 用户**未**对点 8 作 explicit 处置
- 维持 C1(a) FAIL 状态（Codex 直读 Cui Eq. (3) / Eq. (A6) 用 asymptotic Devetak-Winter，Pirandola Methods 用 trace-norm ε-closeness，textual 不直接 equate）
- **future work item**：与点 4 同类问题，需 primary citation bridge

**点 6（KW Ch 20 §20.2 SKA ↔ private-state distillation purification trick）— 用户决定："按你说的来"**

- 用户接受 Claude 的处置 plan：尝试获取 Khatri-Wilde 教科书的 arXiv 开源 preprint（arXiv:2011.04672 *Principles of Quantum Communication Theory: A Modern Approach*），让 Codex 重测点 6
- 执行结果**已录**（见 §7.x.5.5）：UNCERTAIN narrowed —— 6(i) SKA-PSD equivalence 文本上 confirmed，6(ii) Cui Eve 模型适配性需额外 embedding argument

#### §7.x.5.5 点 6 retest 结果（KW arXiv:2011.04672 Ch 20 §20.2 已下载）

**PDF**：[Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)（1240 页 freely available preprint，2024-02-13 版本）

**Reviewer**：Codex (gpt-5.4 xhigh, independent of Claude) — see [c1a-codex-pdf-verification-point6-retest.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-codex-pdf-verification-point6-retest.md)

**点 6 verdict**：**UNCERTAIN**（earlier UNCERTAIN-due-to-missing-PDF → narrowed-but-still-UNCERTAIN）

**6(i) SKA ↔ private-state distillation purification equivalence textually present**：✅ **CONFIRMED**

KW PDF p.1184（printed p.1171）verbatim：

> "There is a deep and powerful equivalence between a secret-key-agreement protocol as described above and a protocol that uses LOCC assistance to distill a bipartite private state."
>
> "The main idea behind this equivalence is to apply the purification principle to a secret-key-agreement protocol and then examine the consequences."

KW PDF p.1188（printed p.1175）verbatim：

> "Thus, starting with a tripartite secret-key-agreement protocol, we can apply the purification principle, then trace over the systems of the eavesdropper, and the result is a bipartite private-state distillation protocol assisted by LOCC."
>
> "Alternatively, this reasoning can go in the opposite direction."

**结论**：SKA ↔ PSD purification trick 本身**确实**在 KW §20.2 textually 建立。

**6(ii) 适用 Cui 2019 Eve 模型**：❌ **§20.2 单独 NOT settled**

**KW §20.2 formal setup（PDF p.1178）**：
- 单一 quantum channel $\mathcal{N}_{A\to B}$（Alice → Bob 直连），Eve 通过 environment system $E$ + public classical register 接入
- $n$-round LOPC（Local Operations + Public Communication）assisted

**KW §20.2.4 推广**：只 generalize 到 "public separable channels"

**Cui 2019 Eve（per Cui Eq. (1)）**：在 Alice/Bob 两条 outbound channels 上做 **arbitrary 联合 unitary** $\hat{U}$ + measurement on classical message register —— **untrusted relay topology**，**非** single-channel $\mathcal{N}_{A\to B}$

**Codex 关键判断**（PDF page-cited）：

> "Section 20.2.4 only generalizes to public separable channels, not to an arbitrary joint untrusted-relay unitary on both outbound quantum modes. So Cui coverage needs an extra embedding/reduction argument beyond KW §20.2."

**与 path α sub-gap 的精确对应**：

这正好揭示 **L1.G2**（Lemma A embedding $\iota$ 具体构造）的 substantive 内涵 —— 把 Cui untrusted-relay 协议 $\Pi$ 通过 $\iota$ 映射到 KW SKA framework 适用的 trusted-network 协议 $\Pi_{tr}$，**就是**这一 "extra embedding/reduction argument" 的 formalization。换言之：

- 点 6 retest 把"应该走 KW §20.2"这一 cross-reference claim 验证到 textually-explicit ✅
- 但同时**显式**揭示：从 KW SKA 直接覆盖 Cui Eve 还需 L1.G2 sub-gap 的 paper-level closure
- 这**不**是 path α 的新缺陷，而是**现有 11 sub-gap inventory 在 textual evidence 上的 confirmation** —— L1.G2 仍 [UNKNOWN]，需独立 paper-level 工作

**对 sub-gap 状态的影响**：**11 sub-gaps 全部维持 [UNKNOWN]**。L1.G2 的 [UNKNOWN] 状态被 KW §20.2 retest **independently 验证为 substantive**（不是冗余条目）。

#### §7.x.5.6 final C1(a) 状态汇总（含点 4 + 点 6 user 处置 + retest）

| 点 | 内容 | 最终状态 |
|---|---|---|
| 1 | Cui Step 3 ⊆ Pirandola "local quantum operation + classical broadcast" | **PASS** |
| 2 | Pirandola "adaptive LOs" 覆盖 Charlie measurement+broadcast | **PASS** |
| 3 | $\Pi_{tr}$ channel definitions 符合 "memoryless quantum channels along edges" | **PASS** |
| 4 | Cui Section III ε-composable | **USER-ACCEPTED Option B (implicit Devetak-Winter bridge)** + Codex reviewer directive: 不再 re-raise as issue |
| 5 | Curty 2018 Eq. (10)-(11) for Lemma B partial trace | **PASS** |
| 6 | KW Ch 20 §20.2 SKA ↔ PSD purification trick under Cui Eve | **UNCERTAIN narrowed** —— 6(i) PSD equivalence textually confirmed；6(ii) Cui Eve 适配 NOT settled by §20.2 alone（需 extra embedding argument，正好对应 L1.G2 sub-gap）|
| 7 | Cui Eq. (3) per-trial = Pirandola per-chain-use (N=1 lockstep) | **PASS** （with "per chain use" wording correction） |
| 8 | Cui ε ↔ Pirandola ε-close-to-private-state | **FAIL** （Cui 原文未 textually equate；同点 4 性质 — future work item）|

**Aggregate C1(a) verdict（updated）**：**5 PASS** + 1 USER-ACCEPTED + 1 UNCERTAIN narrowed + 1 FAIL = **PARTIAL** （**仍不**满足 C1 完整性）

**升级 path α 的当前状态（含用户 2026-04-26 处置决定）**：

- C1(a) **PARTIAL** —— 5 PASS（1, 2, 3, 5, 7）+ 1 USER-ACCEPTED implicit bridge（4，B 选项）+ 1 FAIL（8）+ 1 pending 重测（6）；**仍不**满足 C1 完整性（4 点的 user-accepted bridge **不**自动 promote 到 C1(a) PASS；5/8 点 PASS 维持）
- C1(b) cross-reference 层面（user 直读 PDF），5/8 textually 支持 + 点 4 user-accepted —— **远**不够 sub-gap closure 层面
- C2 direction-level only + 点 4 specific user decision recorded
- C3 Round 4 PASS（Round 3 FAIL 留痕 + Round 4 fixes verified）

**结论（更新）**：path α v0.3 维持 [USER-APPROVED PRIORITY direction, Round 4 C3-passed, NOT upgrade-eligible]。**任何 [SYN] → [COROLLARY] 升级路径**（per CLAUDE.md R0.2）**仍未开通** —— 用户 Option B 处置点 4 仅 silence future Codex 重提，**不**等价点 4 PASS，更**不**等价 sub-gap closure。

---

## §8 升级路径（R0.2 三闸门）

### 8.1 升级 v0.1 → [SYN] v0.2 / [COROLLARY] candidate

**C1 (independent validation)**：
- (a) 跨家族 AI（Claude + GPT/Codex 双方直读 Cui 2019 + Pirandola SI Note 1）
- (b) user 本人纸笔形式化 Lemma A/B/C
- (c) Coq/Lean 形式化（复杂但可行）

**C2 (user 签字)**：user 对 §3-§5 三 lemma 表述 + §6 conditional chain + §7 验证点**逐项**确认

**C3 (dev-reviewer)**：本文档 v0.1 → 提交 dev-reviewer round 3（基于 v0.3 cleanup 后的最新基线）

### 8.2 不做的事

- ❌ 不预设短期时间表（per v0.2 round 1 trap fix）
- ❌ 不主张"path α 比 γ 更稳"
- ❌ 不在外稿 / 论文引用本文档为 [COROLLARY]

---

## §9 Changelog

- **v0.1** (2026-04-25)：首版。基于 [PDF synthesis v0.1 update 3](umr_path_alpha_pdf_synthesis_v0_1.md) 的 Cui 2019 直读，把三 lemma statement target 用 Cui Eq. (1) Hilbert 空间 + Pirandola SI Note 1 协议类**精确表述**。所有 11 sub-gap [UNKNOWN] 维持。8 个 user 直读核对点列出。**未**做任何 lemma proof / closure。
- **v0.1 + §7.x append** (2026-04-26)：附加 §7.x 用户验证响应记录（user message 2026-04-26）。核对点 1-4/6/8 user "是"/等价（标为 user judgment，**不**等价 C1(b)）。核对点 5 Claude 直读 [Curty-Azuma-Lo 2018 PDF](../literature/pdfs/Curty-Azuma-Lo-2018-SimpleSecurityTwinField.pdf) 11 页全文，提取 6 项支持点。核对点 7 Claude recheck Cui Eq. (3) per-trial 与 Pirandola chain bound 对齐。**11 sub-gaps 全部维持 [UNKNOWN]，无升级，无 closure，无 FINDINGS/PHASE_STATUS 编辑**。
- **v0.1 + §7.x.5 review-results append** (2026-04-26 same-day)：完成三 reviewer 平行审查后附加。dev-reviewer round 3 diff + holistic **均 FAIL**（2 majors converging on C2 over-claim + Curty 5.5 cross-space smuggle）；C1(a) Codex direct-PDF **PARTIAL**（5/8 PASS，points 4+8 FAIL 因 Cui 原文无 explicit ε-composable / private-state textual support，point 6 UNCERTAIN 因 KW Ch 20 PDF 缺失）。Round 3 fixes 已 apply：§7.x.1 C2/C1(b) wording 严格降级到 "evidence not gate-satisfied" / "cross-reference candidate evidence only"；§7.x.2 5.5 改写为严格 untrusted-Charlie 内部 + 明示 Curty **不**走 Π → Π_tr 嵌入；§7.x.3 "per bottleneck-link use" 替换为 Pirandola 实际语言 "per chain use"。**11 sub-gaps 仍全部 [UNKNOWN]，path α v0.3 维持 [USER-APPROVED PRIORITY, NOT C3-passed, NOT upgrade-eligible]**。
- **v0.1 + §7.x.5.4-6 user disposition + point 6 retest append** (2026-04-26 same-day continuation)：用户处置 C1(a) PARTIAL 分歧。点 4 Option B（user-accepted implicit Devetak-Winter ↔ ε-composable bridge）+ Codex reviewer directive（不再 re-raise 点 4）。点 6 按 Claude plan 下载 [Khatri-Wilde arXiv:2011.04672 preprint](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)（1240 页）让 Codex 重测，verdict = UNCERTAIN narrowed —— 6(i) SKA ↔ PSD purification trick textually confirmed in KW §20.2，6(ii) Cui Eve 模型适配 NOT settled by §20.2 alone（需 extra embedding argument, 正好对应 L1.G2 sub-gap 的 substantive content）。**Round 4 dev-reviewer C3 PASSED**（diff + holistic 均 PASS）。**11 sub-gaps 仍全部 [UNKNOWN]，path α 升级闸门仍未开通**（C1(a) PARTIAL + C1(b) cross-reference only + C2 direction-only + C3 PASSED）。

---

*END OF v0.1.* 11 sub-gaps OPEN. R0.1 不降级 / R0.2 不越权 / R0.3 [SYN] 维持. Cui 2019 anchor 选定. user-directive 2026-04-25 priority 维持. 任何升级仍需 R0.2 三闸门.
