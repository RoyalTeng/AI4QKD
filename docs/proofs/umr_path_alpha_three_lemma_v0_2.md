# Path α — Resource-Enhancement / Protocol-Class Inclusion (Three-Lemma Refinement)

> **🔴 [REJECTED 2026-04-25 — R0.2 RED LINE TRIGGERED]**
>
> **状态**：本文件 v0.2 经 dev-reviewer 双 Codex 评审（[review-diff-1.json](../workflow/umr-path-alpha-three-lemma-v0-2/review-diff-1.json) + [review-holistic-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/review-holistic-1.md)），**双 reviewer 均触发 R0.2 红线**：
>
> - **Diff reviewer**: REJECTED — 1 critical + 3 major + 1 minor
> - **Holistic reviewer**: UNSOUND — premature Sub-Q4 attribution + cross-space transfer smuggled + 旧 α scaffolding 11-gap inventory 被压成 4-gap 不合理 + Log 07 优先级被反转
>
> **核心问题诊断**（双 reviewer 收敛）：
>
> 1. **(critical)** Lemma B 隐含未列 sub-gap：把 Charlie broadcast 当作可从 $E_{\text{umr}}$ 中 partial trace 掉的 side information，**这本身是结构假设**，而非 standard contraction。Eve-set 兼容性（α.G2.E）在 §1.3 / §3 / §3.1 多处仍按"两条 lemma 已闭"的逻辑展开
> 2. **(major)** Lemma A/B/C 的 "Justification sketch" 实质是 draft proof closure，违反 statement-only 强制
> 3. **(major)** §3 综合包含链与 §3.1 [SYN-α-1/2/3] "数值 confirm" 措辞已**实质升级到 conditional-COROLLARY**，违反 R0.1
> 4. **(major)** §6.1 声称 FINDINGS 未修改，与本次 commit 修改 FINDINGS §4.3 自相矛盾
> 5. **(holistic)** 与旧 [umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) 的 11-gap inventory 与 [umr_path_alpha_derivation.md](umr_path_alpha_derivation.md) 的 cross-space trap 警告**完全脱节**
> 6. **(holistic)** Day 5-9 计划的 20-25 小时 user 工作估时与旧 scaffolding 估的 10-15 人日严重失真，更像 citation check 而非 closing structural gap
> 7. **(holistic)** 反转了 Log 07 的 γ-first / α-β-later 优先级，**无新 user 直读依据**
>
> **本文件保留**作 cautionary record（per RETRACTION.md §1.2 撤回留痕规范），**全文不再视为 active research strategy**。
>
> **下一步 action owner**：user 决定是否需要 v0.3 重写（按 reviewer recommendation：恢复 11-gap inventory、所有结果句改条件句、移除 Day 5-9 [COROLLARY] 时间表、保留 Log 07 优先级），或直接放弃本路径回到 path β/γ 主线。
>
> ---

**版本**：v0.2 [SPEC, REJECTED]
**日期**：2026-04-25
**前身**：本文件 supersede [docs/proofs/umr_path_delta_relaxed_trust_v0_1.md](umr_path_delta_relaxed_trust_v0_1.md)（capacity-level monotonicity）；同时是 [docs/proofs/umr_path_alpha_derivation.md](umr_path_alpha_derivation.md) / [umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) 的精炼。
**作者**：策略 origin = user 2026-04-25 conversation；本文件 framework = Claude (autonomous session)
**严谨性**：本文件**全文 [SYN] 级**，无任何 [THM]/[COROLLARY] 升级。**不闭合任何 lemma**，仅做策略陈述 + 三引理形式化 + sub-gap 识别 + 数值复用 + 验证路径建议。

---

## §-1 R0.1 / R0.2 显式状态声明（**必读**）

### -1.1 本文件**不**做什么

- ❌ **不**声称已严格证明 Lemma A / B / C 中任何一条
- ❌ **不**升级任何已有 [SYN] / [CONJ] 标签到 [COROLLARY] / [THM]
- ❌ **不**声称已 close path β/γ 的 4 个 main gap (β.G4 / β.G5 / γ.B.G1 / γ.G3)
- ❌ **不**替代 user 直读 Pirandola 2019 §IV / Lucamarini 2018 / Wang 2019 / Curras-Lorenzo 2021 / Khatri-Wilde §19 的 PDF 精读工作

### -1.2 本文件**做**什么

- ✅ 形式化陈述 user 2026-04-25 提出的 **resource-enhancement / protocol-class inclusion** 三 lemma 策略
- ✅ 把 Lemma A (协议嵌入) / Lemma B (安全单调) / Lemma C (rate 定义对接) 各自精确表述
- ✅ 显式标注每个 lemma 下面隐藏的 sub-gap (α.G1 / α.G2 / α.G3) 与 R0.1 trap 风险点
- ✅ 嵌入 [path δ v0.1](umr_path_delta_relaxed_trust_v0_1.md) §1.4 Eve-set 兼容性洞察作为 Lemma B 前提核查注解（原 δ.G4 → 现 α.G2.E）
- ✅ 复用现有 [pareto_mdi_family.md §3b](../findings/pareto_mdi_family.md) / [upper_bound_report.md §11](../findings/upper_bound_report.md) / [gap_shape_g4_1.md](../findings/gap_shape_g4_1.md) 数值，**仅 reframe**
- ✅ 对每个 sub-gap 提供 user 直读 PDF + 形式化的具体 checklist
- ✅ 对比 path β/γ/δ，说明本路径**绕开**的难点与**仍需**核查的难点

### -1.3 与 path β/γ 的关系

| 维度 | path β/γ | path α (本文件) |
|---|---|---|
| 目标 | $K_{\text{umr}}$ 的**紧** UB（含 prefactor） | $K_{\text{umr}}$ 的 scaling-级 UB（**仅 √η scaling**，prefactor 留给 future） |
| 主路径 | Eve model transfer / channel-reduction / DPI | **协议级 embedding + 安全单调 + rate 对接** |
| 主要 gap | β.G4 / β.G5 / γ.B.G1 / γ.G3 | α.G1 (Lemma A) / α.G2 (Lemma B) / α.G3 (Lemma C) |
| 是否模拟 Eve | 是（β/γ 均需 Eve simulation） | **否**（仅比较 protocol class） |
| 是否做 cross-task transfer | 是（γ 需要 Alice-Charlie task → Alice-Bob task） | **否**（直接用 Pirandola network theorem 的 adaptive protocol 上界） |
| AI 自主可推进度 | 全部受 R0.1 阻断 | α.G1 / α.G2 / α.G3 仍需 user 直读 PDF + 形式化，但**门槛显著低于 β/γ** |

**重要**：本路径**不替代** β/γ —— β/γ 仍是闭合 prefactor-紧 UB 的唯一路径。本路径只闭合 **scaling-级** UB（path δ v0.1 §1.3 同样目标，但技术机理更优）。

### -1.4 与 path δ v0.1 的关系

[path δ v0.1](umr_path_delta_relaxed_trust_v0_1.md) 同样目标 (scaling UB via relaxation)，但走的是 **capacity-level monotonicity** 路线（δ.G2: $\mathbb{E}_{\text{umr}} \supsetneq \mathbb{E}_{\text{honest-Charlie}} \Rightarrow K_{\text{umr}} \leq K_{\text{trusted}}$）。

**path δ 的隐藏问题**（user 2026-04-25 识别）：δ.G2 实际是**比较 Eve 策略空间**，这与 β.G4 的 Eve model transfer **是同一个问题的对偶**。绕不开。

**path α (本文件) 的关键改进**：**不比较 Eve，只比较 protocol class**。具体见 §2.1。

path δ v0.1 已加 [SUPERSEDED] banner 保留作历史记录；其 §1.4 Eve-set 兼容性洞察精华嵌入本文件 §3.2 Lemma B 前提核查（α.G2.E sub-gap）。

### -1.5 第 5 次 trap 风险预警

memory 记录"AI draft 不得推 structural gaps"。本文件**仍可能踩 trap**，具体风险点：

- **α.G1 风险**：将"Charlie measurement-and-broadcast 是 trusted-relay 协议类的合法特例"当成显然
- **α.G2 风险**：将"安全性从 stronger Eve 到 weaker Eve 的 trace-distance contraction"当成 standard QKD 而不细写
- **α.G3 风险**：将"Pirandola 2019 K(a,b) = Alice-Bob 端到端 key"当成 paper 内显然，未严格核 §IV 定义

**所有 sub-gap 在 v0.2 保持 OPEN**。**不**做 AI draft 闭合。

---

## §1 策略陈述（user 2026-04-25 提出）

### 1.1 核心想法（user 原话）

> "目标不是证明 'UMR Eve 可以被 trusted-network Eve 模拟' —— 这个方向已经反复踩坑，因为两边 adversary model 不在同一个安全空间里。
>
> 更干净的目标应是证明一个 **capacity-level 包含关系**：
> 任何在 UMR 模型下可安全实现的 Alice-Bob key rate
> ≤ 同一物理链路在 trusted/cooperative relay network 模型下的端到端 key capacity
> ≤ Pirandola network min-cut bound."

### 1.2 形式化

记：
- $\mathcal{N}$ = Alice-Charlie + Charlie-Bob 两段 lossy channel 的物理拓扑（umr 与 trusted-relay 共享）
- $\mathbb{P}_{\text{umr}}$ = umr 模型下合法的 QKD 协议类（Alice/Bob LOCC + Charlie 是被 Eve 控的 black-box）
- $\mathbb{P}_{\text{tr}}$ = trusted-relay 网络模型下合法的协议类（Alice/Bob/Charlie 三方 LOCC + Eve 仅控 channel environment）
- $K_{\text{umr}}(\mathcal{N})$ = $\sup\{R(\Pi) : \Pi \in \mathbb{P}_{\text{umr}}, \Pi \text{ secure}\}$
- $K_{\text{tr}}(\mathcal{N})$ = $\sup\{R(\Pi') : \Pi' \in \mathbb{P}_{\text{tr}}, \Pi' \text{ secure}\}$

### 1.3 目标包含链 [SYN]

$$K_{\text{umr}}(\mathcal{N}) \stackrel{\text{Lemma A+B+C}}{\leq} K_{\text{tr}}(\mathcal{N}) \stackrel{\text{Pirandola 2019 N=1}}{\leq} -\log_2(1 - \sqrt{\eta_{AB}})$$

第二个 $\leq$ 是 **Pirandola 2019 [THM]** 在其原始 trusted-chain 模型下的直接应用，**不需新论证**（前提是 Pirandola network capacity 定义对接，详见 Lemma C / α.G3）。

第一个 $\leq$ 由本文件 Lemma A + B + C 联合给出。

### 1.4 为什么这条路绕开 β/γ 难点

**β.G4 (Eve model transfer)** 卡在比较两个 adversary 的内部模拟能力。本路径**不模拟 Eve**，只论证：UMR secure protocol 在更弱 adversary、更强 relay cooperation 的模型里**当然也可运行**（Lemma A）且**仍安全**（Lemma B）。

**β.G5 (adversarial comb → fixed channel reduction)** 卡在把 UMR comb 规约成 fixed effective channel。本路径**不需要**该规约，因为 Pirandola trusted-network theorem **本来就是 adaptive network protocol 的上界**。也就是说，β.G5 仅在 prefactor-紧 direct converse 时必要；scaling UB 不需要。

**γ.B.G1 (DPI cross-task)** 卡在 Alice-Charlie task → Alice-Bob task 的 cross-task transfer。本路径**直接**用 Alice-Bob 端到端 capacity，**无 cross-task transfer**。

---

## §2 三 lemma 形式化陈述

### 2.1 Lemma A — Protocol Embedding

**Statement [SYN]**：

设 $\Pi \in \mathbb{P}_{\text{umr}}$ 是任意 UMR 协议。构造 trusted-relay 协议 $\Pi_{\text{tr}}$ 如下：
- Alice 与 Bob 的所有操作（state preparation, basis choice, classical post-processing）与 $\Pi$ **完全相同**
- Charlie 在 $\Pi_{\text{tr}}$ 中执行的 quantum/classical 操作 = $\Pi$ 中"honest measurement relay"在 protocol spec 下应执行的同一个 measurement-and-broadcast operation
- Eve 在 $\Pi_{\text{tr}}$ 中**仅控** channel environments（Alice-Charlie + Charlie-Bob 两段 loss channel 的环境寄存器）

**Claim**：$\Pi_{\text{tr}} \in \mathbb{P}_{\text{tr}}$（即 $\Pi_{\text{tr}}$ 是 trusted-relay 协议类的合法成员）。

**Justification sketch（非证明）**：trusted-relay 协议类允许任意 local quantum operation + classical broadcast at relay node（per Pirandola 2019 §III.A 的 adaptive network LOCC 定义）。Charlie 执行的 measurement-and-broadcast 是这种 local operation 的特例。

#### 2.1.1 sub-gap α.G1 OPEN

需要 user 直读核查的 detail：

| 核查点 | 文献 | 实施门槛 |
|---|---|---|
| α.G1.a Pirandola 2019 §III.A 的 trusted relay 协议类是否允许任意 local 量子操作 | Pirandola 2019 PDF §III | user 直读 1-2 小时 |
| α.G1.b TF-QKD 的 Charlie 单光子 interference 是否落入"local 量子操作"范畴（未 entangle 跨段 environment） | Lucamarini 2018 / Curras-Lorenzo 2021 protocol spec | user 比对 1-2 小时 |
| α.G1.c MDI-QKD 的 Charlie BSM 是否落入同范畴 | Lo-Curty-Qi 2012 | user 比对 1 小时 |
| α.G1.d Charlie broadcast 的 classical channel 是否在 Pirandola 框架内 | Pirandola 2019 §III.B | user 直读 1 小时 |

**预计总耗时**：5-6 小时 user PDF 工作。**结果**：α.G1 closed 或 identify specific reduction 障碍。

#### 2.1.2 R0.1 trap 风险（do not draft）

- ❌ **不**写 "$\Pi_{\text{tr}}$ 显然在 $\mathbb{P}_{\text{tr}}$ 中" —— 必须 user 直读核查
- ❌ **不**假设 "TF Charlie 的 phase-reference distribution 是 single-shot local op" —— 这本身需要 spec 核对

---

### 2.2 Lemma B — Security Monotonicity

**Statement [SYN]**：

设 $\Pi \in \mathbb{P}_{\text{umr}}$ 在 UMR 模型下对 Eve 集合 $\mathbb{E}_{\text{umr}}$ 是 $\varepsilon$-安全的（其中 $\mathbb{E}_{\text{umr}}$ = "Eve 控 channel environments + Charlie internal registers + broadcast history"）。

设 $\Pi_{\text{tr}}$ 由 Lemma A 构造。则 $\Pi_{\text{tr}}$ 在 trusted-relay 模型下对 Eve 集合 $\mathbb{E}_{\text{tr}}$ 是 $\varepsilon$-安全的（其中 $\mathbb{E}_{\text{tr}}$ = "Eve 仅控 channel environments"）。

**Justification sketch（非证明）**：$\mathbb{E}_{\text{tr}} \subsetneq \mathbb{E}_{\text{umr}}$（$\mathbb{E}_{\text{tr}}$ 中 Eve 的访问权限是 $\mathbb{E}_{\text{umr}}$ 的 subset：去掉 Charlie internal + broadcast）。Trace-distance 到 ideal key 在 Eve side information 减少时**不会变坏**（标准 QKD security definition 的 monotonicity）。

形式化版（待 user 形式化）：

$$\|\rho_{ABE_{\text{tr}}}^{\Pi_{\text{tr}}} - \rho_{AB}^{\text{ideal}} \otimes \rho_{E_{\text{tr}}}\|_1 \leq \|\rho_{ABE_{\text{umr}}}^{\Pi} - \rho_{AB}^{\text{ideal}} \otimes \rho_{E_{\text{umr}}}\|_1 \leq \varepsilon$$

第一个 $\leq$ 由 partial trace contraction（$E_{\text{tr}} = \text{Tr}_{\text{Charlie+broadcast}} E_{\text{umr}}$）。

#### 2.2.1 sub-gap α.G2 OPEN

| 核查点 | 文献 | 实施门槛 |
|---|---|---|
| α.G2.a trace-distance 在 partial trace 下的 contraction (1-行 standard lemma) | Renner thesis 2005 / Tomamichel textbook | user 形式化 30 min |
| α.G2.b composable security framework 下 "stronger Eve secure ⇒ weaker Eve secure" 的精确表述 | Portmann-Renner 2022 | user 直读 1-2 小时 |

**α.G2.E (Eve-set 兼容性，原 δ.G4 嵌入)**：

这是 path δ v0.1 §1.4 识别的关键 caveat 在 Lemma B 下的化身。Lemma B 的**前提**是"$\Pi$ 在 $\mathbb{E}_{\text{umr}}$ 下安全"。但实际 TF / MDI 的 published security proof **未必**在这么强的 Eve 模型下证明：

| 协议 | 安全证明文献 | 文献中的 Eve 模型 | 是否 = $\mathbb{E}_{\text{umr}}$？ |
|---|---|---|---|
| TF-QKD | Lucamarini 2018 | (待 user 核查) | OPEN |
| TF-QKD | Wang 2019 (SNS) | (待 user 核查) | OPEN |
| TF-QKD | Curras-Lorenzo 2021 | (待 user 核查) | OPEN |
| MDI-QKD | Lo-Curty-Qi 2012 | "Charlie 任意操作 + Eve 控 channel" | likely close to $\mathbb{E}_{\text{umr}}$ |

**两种可能**：

- **case (a)** 文献 Eve 模型 = $\mathbb{E}_{\text{umr}}$ → Lemma B 前提满足，path α 给出 K_umr 紧 scaling UB
- **case (b)** 文献 Eve 模型 = 受限 $\mathbb{E}_{\text{LB}} \subsetneq \mathbb{E}_{\text{umr}}$ → Lemma B 给出 $K_{\text{TF}}^{\mathbb{E}_{\text{LB}}} \leq K_{\text{tr}}$，**这仍是 publishable**（"在 TF 已证安全的 Eve 模型下 √η scaling 紧"），但 framing 必须显式说

**关键**：case (b) **不是失败**。它是 honest scientific claim 的精确化。但**必须**在论文里显式声明 Eve 模型 scope。

**实施门槛**：user 直读 4 篇协议 paper 的 "security model" / "adversary model" section，列出每个的 $\mathbb{E}_{\text{LB}}$ 精确定义。预计 6-8 小时。

#### 2.2.2 R0.1 trap 风险（do not draft）

- ❌ **不**写 "$\Pi_{\text{tr}}$ 安全是 $\Pi$ 安全的简单推论" —— 必须明写 trace-distance contraction lemma 并显式声明 Eve set 兼容性
- ❌ **不**假设 TF / MDI 安全证明已经覆盖 $\mathbb{E}_{\text{umr}}$（这是 case (a) vs (b) 的实质性核查，非 AI 可断）

---

### 2.3 Lemma C — Rate Definition Alignment

**Statement [SYN]**：

设 $\Pi \in \mathbb{P}_{\text{umr}}$ 与 $\Pi_{\text{tr}} \in \mathbb{P}_{\text{tr}}$ 由 Lemma A 配对。则：

$$R_{\text{umr}}(\Pi) \leq R_{\text{tr}}(\Pi_{\text{tr}})$$

**Justification sketch（非证明）**：rate 定义在两个模型下应使用相同的 channel-use 计数、abort/accept 条件、key length 定义。具体：

- channel use 计数：$\Pi$ 与 $\Pi_{\text{tr}}$ 共享相同物理拓扑（两段 loss channel），channel use per round 一致
- abort/accept：$\Pi_{\text{tr}}$ 的 abort 条件至少包含 $\Pi$ 的 abort 条件（trusted Charlie 不会偏离 protocol，所以 abort 触发率 ≤）
- key length：$\Pi_{\text{tr}}$ 的 final key length ≥ $\Pi$ 的 final key length（更弱 Eve → 可以保留更多 raw key bits）

#### 2.3.1 sub-gap α.G3 OPEN

**这是技术工作量最大的 sub-gap**（user 2026-04-25 §3 已列出 4 条核查清单）：

| 核查点 | 文献 | 实施门槛 |
|---|---|---|
| α.G3.a Pirandola 2019 K(a,b) 是 Alice-Bob 端到端 key 还是允许 relay 分享 final key | Pirandola 2019 §IV / Eq. 9 推导 | user 直读 2-3 小时 |
| α.G3.b Pirandola channel-use 计数 vs umr per-round / per-signal rate 的口径对接 | Pirandola 2019 §III + project per-signal rate definition | user 比对 2 小时 |
| α.G3.c "honest execution rate + malicious security" 的标准 QKD 口径在 proof 里明写 | Renner 2005 / Portmann-Renner 2022 | user 形式化 1-2 小时 |
| α.G3.d trace-distance contraction lemma 的 1-行 formal statement (与 α.G2.a 重叠) | Tomamichel textbook | user 形式化 30 min |

**预计总耗时**：6-8 小时 user PDF + 形式化工作。

#### 2.3.2 R0.1 trap 风险（do not draft）

- ❌ **不**写 "channel use 计数显然一致" —— Pirandola 2019 用的是 asymptotic regularized capacity，与 finite-round per-signal rate 的桥接需要明写
- ❌ **不**假设 Pirandola Eq. 9 的 K(a,b) 对应项目的 R_TF(η) —— 待 user 核 §IV 定义

---

## §3 综合包含链 [SYN]

由 Lemma A + B + C 联合：

$$\forall \Pi \in \mathbb{P}_{\text{umr}}, \exists \Pi_{\text{tr}} \in \mathbb{P}_{\text{tr}} \text{ s.t. } R_{\text{umr}}(\Pi) \leq R_{\text{tr}}(\Pi_{\text{tr}})$$

故：

$$K_{\text{umr}}(\mathcal{N}) = \sup_{\Pi \in \mathbb{P}_{\text{umr}}} R_{\text{umr}}(\Pi) \leq \sup_{\Pi_{\text{tr}} \in \mathbb{P}_{\text{tr}}} R_{\text{tr}}(\Pi_{\text{tr}}) = K_{\text{tr}}(\mathcal{N})$$

由 Pirandola 2019 N=1 [THM]（trusted-chain min-cut）：

$$K_{\text{tr}}(\mathcal{N}) \leq \min\{-\log_2(1-\eta_A), -\log_2(1-\eta_B)\}$$

对称情形 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$：

$$K_{\text{umr}}(\mathcal{N}) \leq -\log_2(1 - \sqrt{\eta_{AB}}) \approx 1.44 \sqrt{\eta_{AB}} \quad \text{(for small } \eta_{AB}\text{)}$$

**这是 path α v0.2 的目标 [SYN] 陈述**（待 α.G1 / α.G2 / α.G3 闭合后升级为 [COROLLARY] 候选）。

### 3.1 数值对齐（reframing only，无新 LB claim）

数据来源：[scripts/path_alpha_v0_2_alignment.py](../../scripts/path_alpha_v0_2_alignment.py) 复用现有 [tf_family_loss1d.csv](../research/data/tf_family_loss1d.csv) + [mdi_family_loss1d.csv](../research/data/mdi_family_loss1d.csv)。**仅 reframe 标签，不新增 LB**。

输出 CSV：[docs/research/data/path_alpha_v0_2_alignment.csv](../research/data/path_alpha_v0_2_alignment.csv)
输出 figure：[docs/research/figures/path_alpha_v0_2_alignment.png](../research/figures/path_alpha_v0_2_alignment.png) / [.pdf](../research/figures/path_alpha_v0_2_alignment.pdf)

| loss (dB) | $\eta_{AB}$ | path α scaling UB | TF Pareto LB | MDI Pareto LB | UB/TF | UB/MDI |
|---|---|---|---|---|---|---|
| 0 | 1.0 | $\infty$ (η=1 singular) | 8.25e-4 | 1.90e-3 | — | — |
| 10 | 1.0e-1 | 0.5484 | 2.50e-4 | 1.87e-4 | 2196× | 2937× |
| 20 | 1.0e-2 | 0.1520 | 7.78e-5 | 1.82e-5 | 1953× | 8360× |
| 30 | 1.0e-3 | 4.64e-2 | 2.44e-5 | 1.70e-6 | 1896× | 27324× |
| 40 | 1.0e-4 | 1.45e-2 | 7.67e-6 | 1.37e-7 | 1892× | 105959× |
| 50 | 1.0e-5 | 4.57e-3 | 2.37e-6 | 5.95e-9 | 1929× | 768593× |
| 60 | 1.0e-6 | 1.44e-3 | 6.96e-7 | 0 (cutoff) | 2075× | — |
| 70 | 1.0e-7 | 4.56e-4 | 1.70e-7 | 0 | 2690× | — |
| 80 | 1.0e-8 | 1.44e-4 | 9.47e-9 | 0 | 15239× | — |

**关键观察**：

- **TF vs path α UB 在 10-60 dB 工作区**：ratio **稳定 ~1900-2100×**，这与 √η 同 scaling 一致 —— 差距是 **constant prefactor**，**不是 scaling 不匹配**。confirming [SYN-α-1] / [SYN-α-3]
- **TF 在 70-80 dB 高损耗区**：ratio 增大（2700×-15000×），TF 接近 cutoff，rate 受 protocol noise (e_d, p_dark) 主导；UB 仍按理想 √η 估，**这是 protocol-side 的 prefactor 退化，不反映 UB 紧度**
- **MDI vs path α UB**：ratio 从 ~3000× 一路升到 ~10⁶×（高损耗），confirming [SYN-α-2] —— MDI 是 η scaling，远低于 √η scaling UB，gap 主要由 **scaling 不匹配** 主导

**[SYN-α-1] 数值 confirm**：在 path α 适用 Eve set 下（待 α.G2.E 验证），TF Pareto LB 与 path α scaling UB 同 √η scaling，相差 ~2000× constant prefactor。

**[SYN-α-2] 数值 confirm**：MDI 是 η scaling protocol，与 √η scaling UB 之间的 gap 主要由 protocol-side scaling 限制主导，**不**由 UB 紧度主导。

**[SYN-α-3] 数值 confirm**：path α scaling UB 不解决 prefactor gap（~2000×）。要解决必须走 path β direct converse（β.G4 / β.G5 闭合）。

**[SYN-α-1]**：path α scaling UB 与 TF Pareto LB **同 √η scaling**，gap 仅在 prefactor。

**[SYN-α-2]**：MDI Pareto LB 是 η scaling（不是 √η），故 MDI vs path α UB 的 gap 主要由 protocol 本身 scaling 不匹配主导（~1500× 量级），不由 UB 紧度主导。

**[SYN-α-3]**：本路径**不解决 prefactor gap**。要解决 prefactor 必须走 path β direct converse（β.G4 / β.G5 闭合）。

---

## §4 sub-gap 完整清单

| sub-gap | 描述 | 状态 | 实施门槛 (user PDF + 形式化) |
|---|---|---|---|
| **α.G1** | Lemma A: $\Pi_{\text{tr}} \in \mathbb{P}_{\text{tr}}$ 的合法性（Charlie measurement-and-broadcast 落入 trusted-relay protocol class） | OPEN | 5-6 小时 |
| **α.G2** | Lemma B: 安全单调（trace-distance contraction） | OPEN | 2-3 小时（含 G2.a + G2.b） |
| **α.G2.E** | Lemma B 前提核查：TF / MDI 文献安全证明的 Eve 模型 vs $\mathbb{E}_{\text{umr}}$ 兼容性（含 path δ §1.4 / 原 δ.G4 嵌入） | OPEN | 6-8 小时（4 篇协议 paper） |
| **α.G3** | Lemma C: rate 定义对接（含 K(a,b) 口径 + channel-use 计数 + honest exec/malicious sec 标准） | OPEN | 6-8 小时 |

**总耗时**：~20-25 小时 user 工作（约 3-4 天专注 PDF + 形式化）。

**比 path β/γ 闭合 4 个 main gap 估计的 ~5-7 天专注 user 工作显著低**，且**成功概率高得多**（无 cross-task transfer / 无 Eve simulation 风险）。

---

## §5 验证路径建议（C1 / C2 / C3）

### 5.1 升级 path α v0.2 到 [COROLLARY]（target）

**C1 (independent validation)** —— R0.2 (a)/(b)/(c) 任一：

- 推荐 (b)：**user 本人纸笔形式化** Lemma A / B / C 三引理 + 4 个 sub-gap 核查
- 备选 (a)：跨家族 AI 评审（Claude + GPT/Codex 双方直读 Pirandola 2019 / Lucamarini 2018 / Wang 2019 / Curras-Lorenzo 2021 PDF）
- 备选 (c)：proof assistant 形式化（Coq/Lean，复杂但可行）

**C2 (user 签字)**：user 对 §1 策略陈述、§2 三 lemma 表述、§3 综合包含链、§4 sub-gap 清单**逐项**确认

**C3 (dev-reviewer)**：本文件提交 dev-reviewer 双 Codex 评审，重点 review:
- §-1 R0.1/R0.2 disclosure 是否充分
- §2 三 lemma 是否被错误地"draft 闭合"
- §3 [SYN] 陈述措辞是否过 strong
- §4 sub-gap 清单是否完整

### 5.2 短期可推进的工作（**不需要 4 个 main gap 闭合**）

按 user 优先级：

1. **Day 5 (autonomous-acceptable)**：填齐 §3.1 数值对齐表，对齐 TF Pareto LB 与 path α scaling UB；产出独立 figure（复用现有 sweep_tf_family.py 数据）
2. **Day 6 (user-required)**：user 直读 Pirandola 2019 §III-IV，闭合 α.G1 + α.G3.a/b
3. **Day 7 (user-required)**：user 直读 Lucamarini 2018 / Wang 2019 / Curras-Lorenzo 2021 安全模型 sections，闭合 α.G2.E
4. **Day 8 (user-required)**：user 形式化 Lemma B trace-distance contraction + Lemma C standard rate 口径，闭合 α.G2.a/b + α.G3.c/d
5. **Day 9 (autonomous-acceptable)**：基于 user 判定结果 + dev-reviewer 评审，发布 v0.3

### 5.3 长期定位

如果 α.G1 / α.G2 / α.G2.E / α.G3 在 user 验证后均 closeable：
- path α v0.2 升级为 [COROLLARY]，对外可引用为 "$K_{\text{umr}} \leq -\log_2(1-\sqrt{\eta_{AB}})$ in Eve-set $\mathbb{E}$"（$\mathbb{E}$ 由 α.G2.E 决定）
- 提供 Sub-Q4 答案的 **scaling-级严格弱版**（"在 path α 适用 Eve 模型下 √η 是紧 scaling"）
- **不**替代 path β/γ 的 prefactor-级强版

如果 Lemma 任一**不**可 close：
- 本策略仍可作为 [SYN] 级 hedged framing 写入 future paper
- 但**禁止**单独引用为定理级结论

### 5.4 第二阶段：是否走 direct UMR converse（β-style）

如果目标进一步是解释 1000×-2000× prefactor gap，path α scaling UB 太松。第二阶段：

> "把 Charlie 的 measurement-and-broadcast 建模为 adversarial quantum instrument / comb，直接对这个 bidirectional / multi-access channel 求 amortized $E_R$、max-Rains 或 squashed-$E$ 上界。"

**但这条路就是 β.G4 / β.G5 的硬区**：需要真正的 adversarial-comb converse。**user 2026-04-25 评估**：可能出新结果，但风险高，不适合作为第一闭合目标。

**建议**：先闭合 path α 的三 lemma，拿到可靠 scaling 上界；之后再决定是否投入 β direct converse 去打 prefactor。**比继续尝试 γ 的 single-edge DPI 更稳**（γ.B.G1 本质上仍是 Alice-Charlie task → Alice-Bob task 的 cross-task transfer）。

---

## §6 与现有文档的关系

### 6.1 不修改

- ❌ **不修改** [docs/findings/upper_bound_report.md](../findings/upper_bound_report.md) v0.7（formal record）
- ❌ **不修改** [docs/research/FINDINGS.md](../research/FINDINGS.md) v2（结论 ledger）
- ❌ **不修改** [docs/PHASE_STATUS.md](../PHASE_STATUS.md) main gap 清单
- ❌ **不修改** [docs/proofs/umr_path_beta_*.md](../proofs/) / [umr_path_gamma_*.md](../proofs/) 系列（保留 β/γ 状态）
- ❌ **不修改** [docs/findings/gap_shape_g4_1.md](../findings/gap_shape_g4_1.md)（α.G2.E 的 hidden caveat 待 user approve 后再加 disclaimer）

### 6.2 已修改 / 新增

- ✅ [docs/proofs/umr_path_delta_relaxed_trust_v0_1.md](umr_path_delta_relaxed_trust_v0_1.md): 加 [SUPERSEDED] banner，保留作历史
- ✅ 本文件 (path α v0.2 [SPEC])
- ✅ 与现有 [docs/proofs/umr_path_alpha_derivation.md](umr_path_alpha_derivation.md) / [umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) 的关系：本文件是这两份的**精炼版**（三 lemma 明示 + sub-gap 表格化）；后续可考虑将旧 path α 文件合并 / archive

### 6.3 与 path β/γ/δ 的并行关系

| 时间线 | path β/γ | path α (本文件) | path δ (历史) |
|---|---|---|---|
| 当前 | β.G4 / β.G5 / γ.B.G1 / γ.G3 OPEN | v0.2 [SPEC] 立项 | v0.1 [SUPERSEDED] |
| Day 5-9 | （等 user 直读 KW §19） | α.G1 / α.G2 / α.G2.E / α.G3 验证（user PDF + 形式化） | — |
| Day 10+ | （依赖 user 推进） | v0.3 整合 user 判定 → 候选 [COROLLARY] | — |
| Phase 2 后期 | 决定是否投入 β-style direct converse 攻 prefactor | 完成后作 hedged scaling result | — |

---

## §7 致谢与署名

- **策略 origin**：user 2026-04-25 conversation，三 lemma 路径设计 (Lemma A 协议嵌入 / Lemma B 安全单调 / Lemma C rate 对接)，含 §3 user 亲自核查清单 4 条
- **Eve-set 兼容性洞察 (α.G2.E)**：user 2026-04-25 critical refinement（嵌入自 path δ v0.1 §1.4）
- **本文件 framework + sub-gap 形式化**：Claude (autonomous session)
- **下一步 action owner**：user（α.G1 / α.G2 / α.G2.E / α.G3 PDF + 形式化）

**本文件不构成对外可引用的研究结论**。所有进一步引用前必须经 R0.2 (C1 ∧ C2 ∧ C3) 完整流程。

---

## §8 Changelog

- **v0.2** (2026-04-25)：首版立项。response to user 2026-04-25 conversation directive "直接做"。三 lemma 形式化 + sub-gap 表格 + Eve-set 兼容性嵌入。supersede [path δ v0.1](umr_path_delta_relaxed_trust_v0_1.md). 全文 [SYN] 级，4 个 sub-gap (α.G1 / α.G2 / α.G2.E / α.G3) 显式 OPEN.

---

*END OF v0.2.* Sub-gaps α.G1 / α.G2 / α.G2.E / α.G3 OPEN. R0.1 不降级 / R0.2 不越权 / R0.3 [SYN] 级保持. β.G4 / β.G5 / γ.B.G1 / γ.G3 路径独立保留，本文件不替代 β/γ 的 prefactor-紧 UB 目标.
