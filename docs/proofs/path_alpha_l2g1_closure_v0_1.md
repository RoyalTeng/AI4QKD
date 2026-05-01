# Path α Lemma B sub-gap L2.G1 — Closure Candidate v0.1

**Sub-gap**：L2.G1 — rate-direction sign（avoid v1 retraction sign-flip trap）：given $\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$ (L2.G3 [UNKNOWN]) AND 同 rate 定义 (L3.G2 [UNKNOWN])，then $R^{\Pi_{tr}}_{tr} \geq R^{\Pi}_{Cui}$

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 KW Ch 20 §20.1
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 KW Ch 20 §20.1 + Devetak-Winter framework | ✅ **PASS** at Codex round 2 |
| **C1(c)** non-AI 数值 | 不适用 |
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ✅ **PASS at R3**（R2 diff FAIL #5 stale Eq. 11 specialization → v0.3 patch → R3 A 项 PASS；详 [R3 review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-r3.md)）|

**关键边界**：
- 本文档**仅** close L2.G1 sign-direction lemma
- L2.G1 是 **条件性** closure：基于 L2.G3 + L3.G2 [UNKNOWN] 两个前提条件
- L1.G1 / L1.G3 / L1.G4 (closed)，L1.G2 / L2.G2 / L2.G3 / L2.G4 / L3.G1 / L3.G2 / L3.G3 状态不变

---

## §1 Sub-gap statement

### 1.1 Lemma L2.G1 statement

**Lemma L2.G1 (rate monotonicity under adversary-set restriction)**：

设：
- $\Pi$ 是某 QKD 协议（在 path α 应用中是 Cui 2019 simplified TFQKD with umr Eve）
- $\Pi_{tr} = \iota(\Pi)$ 是同协议在 trusted-relay 嵌入下的版本（path α Lemma A 嵌入产物）
- $\mathbb{E}_{Cui}$, $\mathbb{E}_{tr}$ 是两组 Eve 攻击操作集合（per L2.G3 描述）
- $R(\Pi, \mathbb{E}; \mathcal{R}) = $ 协议 $\Pi$ 在 Eve 攻击集 $\mathbb{E}$ 下、用某 rate 定义 $\mathcal{R}$ 评估的 secret-key rate

**前提条件**：

- **(P1)** $\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$ —— L2.G3 [UNKNOWN]
- **(P2)** $R$ 在 Π 与 Π_tr 上用**同一** rate 定义 $\mathcal{R}$ 评估（e.g., 都用 KW Ch 20 §20.1 (n,K,ε)-SKA framework, or 都用 Devetak-Winter formula）—— L3.G2 [UNKNOWN]

**结论**：

$$R(\Pi_{tr}, \mathbb{E}_{tr}; \mathcal{R}) \;\geq\; R(\Pi, \mathbb{E}_{Cui}; \mathcal{R})$$

——即 trusted-relay 协议对受限 Eve 集的 rate **不小于** umr 协议对 Cui Eve 集的 rate。

**重点**：sign 方向 = "更小 Eve set → 更高 rate"（min-over-set 单调性）。这避免 v1 retraction sign-flip trap（v1 把 sign 写反了）。

### 1.2 Lemma 在 path α Lemma B 中的位置

Path α 的 scaling 上界目标：$K_{\Pi, umr} \leq -\log_2(1 - \sqrt{\eta_{AB}})$。

证明链（per [lemma_skeletons §6](umr_path_alpha_lemma_skeletons_v0_1.md) v0.2 corrected combined chain，**特别**注意 Eq. 11 specialization chain caveat）：

$$K_{\Pi, umr} \stackrel{\text{Lemma B + L2.G1}}{\leq} K_{\Pi_{tr}, tr} \stackrel{\text{Lemma C + Eq. 11 (REE cut UB) [THM]}}{\leq} \min_C E_R(C) \stackrel{\substack{\text{Eq. (8)/(9) specialization} \\ \text{+ tele-cov + sym η split [conditional]}}}{=} -\log_2(1 - \sqrt{\eta_{AB}})$$

**v0.3 corrected note (post C3 R2 diff finding #5)**：v0.1/v0.2 误把 Pirandola 2019 Eq. 11 直接等同 `-\log_2(1-\sqrt{\eta_{AB}})` 这个 single-repeater bound。**实际** Eq. 11 是 `C(N) ≤ min_C E_R(C)`（REE cut bound, main paper p.4）；`-\log_2(1-\sqrt{\eta_{AB}})` 形式来自 Eq. (8)/(9) lossy chain specialization（main p.3），需要 (i) tele-covariance（pure-loss bosonic）+ (ii) distillability + (iii) symmetric / equidistant η split (`η_{AB} = η_{AC}·η_{BC}`)。详 [RETRACTION.md §9.3](../research/RETRACTION.md#93-l3g3-gap-id-round-揭露重大-pirandola-eq-11-citationspecialization-错误)。

L2.G1 给中间不等式的**方向** —— umr rate ≤ trusted-relay rate（即 sign 是 ≤ 不是 ≥）。**注意**：这里是 RATE 而非 SECURITY DISTANCE 的方向。Rate ≤ 是 capacity-monotonicity 在 adversary-set 角度的体现。本 L2.G1 lemma **仅** close 第一个不等式的方向；第二个不等式（Eq. 11 generic UB）+ specialization chain（→ specific η-form）由 Lemma C + post-split L3.G3 5 项 sub-residual jointly 处理（L3.G3 全部 OPEN per R0.1）。

### 1.3 严格 scope

- ✅ 本 lemma 是 **条件性** closure（依赖 P1 from L2.G3 + P2 from L3.G2 两个 [UNKNOWN]）
- ✅ 关闭的是：sign-direction（即 ≥ 而非 ≤），非 inclusion 本身
- ❌ 本 lemma **不**主张 P1 / P2 的 closure（这两个仍 [UNKNOWN]）
- ❌ 本 lemma **不**主张 absolute rate 数值

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 KW Ch 20 §20.1 — n-shot SKA framework

**Khatri-Wilde 2024**, *Principles of Quantum Communication Theory: A Modern Approach*（arXiv:2011.04672, [PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)）, Chapter 20 ("Secret Key Agreement") §20.1 ("n-Shot Secret-Key-Agreement Protocol")

**Definition 20.1 (n,K,ε) SKA Protocol** at PDF p.1182 / printed p.1169：直接定义 (n,K,ε) SKA protocol 是 privacy error $p_{err}(\mathcal{C}) \leq \varepsilon$ 的 protocol code。

privacy error 定义 Eq. (20.1.17)：

$$p_{err}(\mathcal{C}) = 1 - F(\omega_{K_A K_B E_1^n Y_1^{n+1}}, \Phi_{K_A K_B} \otimes \sigma_{E_1^n Y_1^{n+1}})$$

其中 $\sigma_{E_1^n Y_1^{n+1}}$ 是 "some state of the eavesdropper's systems"（per KW PDF p.1181 verbatim）。

**关键观察（path α conditional 应用框架，非 KW Definition 20.1 直接陈述）**：要把 KW Definition 20.1 应用到 path α 的 capacity-vs-Eve-set 比较，需 SKA 容量的标准 capacity-as-max-rate 表述（即 max over protocol family s.t. $p_{err} \leq \varepsilon$ for the considered Eve model）。当我们在不同 Eve 模型间比较时（umr vs trusted-relay），"$p_{err} \leq \varepsilon$" 的具体语义随 Eve 模型变化，对应 §2.2 min-over-set 单调性 argument。**这是 path α conditional 应用层语义，**不在** KW Definition 20.1 直接表述。

### 2.2 Min-over-set 单调性（elementary）

设 $f: \mathbb{E} \to \mathbb{R}$ 是 Eve 攻击集 $\mathbb{E}$ 上的某函数（e.g., Eve guessing probability）。则对任意 $\mathbb{E}' \subseteq \mathbb{E}$：

$$\inf_{e \in \mathbb{E}} f(e) \;\leq\; \inf_{e \in \mathbb{E}'} f(e)$$
$$\sup_{e \in \mathbb{E}} f(e) \;\geq\; \sup_{e \in \mathbb{E}'} f(e)$$

——由 inf / sup 在 set inclusion 下的单调性直接得到（取下确界 over 较小 set 不小于 over 较大 set）。

**应用到 SKA capacity**：rate $R(\Pi, \mathbb{E})$ 通常定义为 max protocol over min-over-Eve 的最大 ε-secure rate（e.g., $R = \max_{\Pi'} \inf_{e \in \mathbb{E}} R_{secure}(\Pi', e)$）。所以：

$$\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui} \implies \inf_{e \in \mathbb{E}_{tr}} R_{secure}(\Pi, e) \geq \inf_{e \in \mathbb{E}_{Cui}} R_{secure}(\Pi, e)$$

——即 rate against smaller adversary set is at least rate against larger adversary set。

### 2.3 KW §20.1 isometric extension 旁证（与 L1.G3 一致）

KW PDF p.1181-1182（已 partial verbatim by Codex during L1.G3 round 3 verify）：

> "Due to the isometric invariance of the fidelity and the fact that all isometric extensions of a channel are related by an isometry acting on the environment system, the privacy error in (20.1.17) is invariant under any choice of an isometric channel U_N_{A→BE}..."

**含义**：privacy error（即 ε in (n,K,ε)）本身是 well-defined（不依赖 Eve 表征选择）—— 这与 L1.G3 Stinespring gauge invariance 一致。

---

## §3 数学推导

由 §2.2 elementary min-over-set monotonicity：

设 $\mathcal{R}$ 是任意 rate 定义 satisfying min-over-Eve 形式 (e.g., $\mathcal{R}(\Pi, \mathbb{E}) = \max_{\text{protocol family}} \min_{e \in \mathbb{E}} R_{secure}(\Pi, e)$)。则给定 (P1) $\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$ + (P2) 同 rate 定义 $\mathcal{R}$：

$$
\begin{aligned}
\mathcal{R}(\Pi_{tr}, \mathbb{E}_{tr})
&= \max_{\text{protocol family for } \Pi_{tr}} \min_{e \in \mathbb{E}_{tr}} R_{secure}(\Pi_{tr}, e) \\
&\stackrel{(*)}{\geq} \max_{\text{protocol family for } \Pi_{tr}} \min_{e \in \mathbb{E}_{Cui}} R_{secure}(\Pi_{tr}, e) \\
&\stackrel{(\dagger)}{\geq} \max_{\text{protocol family for } \Pi} \min_{e \in \mathbb{E}_{Cui}} R_{secure}(\Pi, e) \\
&= \mathcal{R}(\Pi, \mathbb{E}_{Cui})
\end{aligned}
$$

- $(*)$ 由 min-over-set 单调性 ($\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$ → min over $\mathbb{E}_{tr}$ ≥ min over $\mathbb{E}_{Cui}$)
- $(\dagger)$ 由 Π_tr = ι(Π) 与 Π 共享同 protocol family（per L1.G1 Hilbert space alignment + L1.G2 ι 嵌入合法性 [UNKNOWN]）—— 严格地说，**$(\dagger)$ 步条件依赖 L1.G2** [UNKNOWN]，所以 §3 完整推导是 L1.G2 + L2.G3 + L3.G2 三个 [UNKNOWN] 都成立的 conditional consequence

**严格 scope final check**：本 §3 数学推导中 $(*)$ 是 **unconditional**（纯 min-over-set 单调性，elementary set theory）。$(\dagger)$ 依赖 L1.G2 [UNKNOWN]。

**L2.G1 closure 的实际内容**：是 $(*)$ 这一步的 sign 验证（trusted Eve set ⊆ umr Eve set → trusted rate ≥ umr rate，**不是反向**）。这就 close 了 sign-direction sub-gap，避免 v1 retraction 的 sign-flip trap。

---

## §4 待启动的 C1(a) Codex round

**任务**：让 Codex 跨家族 AI 直读 KW PDF Ch 20 §20.1 + Eq. (20.1.17)-(20.1.18) verify：

1. KW Definition 20.1 (n,K,ε) SKA framework 描述与 §2.1 一致
2. KW privacy error definition Eq. (20.1.17) 及其 Eve-state σ optimization 形式
3. §2.2 min-over-set 单调性是 elementary 标准事实（不需要 KW 引用，但 Codex 需 confirm 推导无误）
4. §3 数学推导 $(*)$ 步是 unconditional sign-direction 验证；$(\dagger)$ 步显式标注 conditional on L1.G2
5. **CRITICAL**: §1.1 P1, P2 前提显式标注 [UNKNOWN]; §1.3 严格 scope 不 smuggle L2.G3 / L3.G2 / L1.G2 closure
6. Lemma scope clean

**预期 verdict**：PASS（min-over-set 单调性是 elementary; conditional framing 正确）

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 KW Ch 20 §20.1 (n,K,ε)-SKA framework + elementary min-over-set monotonicity。L2.G1 closure 是 conditional on L2.G3 + L3.G2 [UNKNOWN]，本身仅 close sign-direction（避免 v1 retraction sign-flip trap）。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL only on §2.1 加了 "worst-case over Eve / sup over Eve states-strategies" 不在 KW Definition 20.1 原文。其余全 PASS。修：明示 capacity-vs-Eve-set 比较语义是 path α conditional application 层，非 KW Definition 20.1 直接陈述。
- **v0.2 final** (2026-04-26 same-day)：**C1(a) Codex round 2 verdict = PASS**。全部 sub-check 通过。**L2.G1 C1 aggregate PASS via C1(a)**。C2 / C3 待。
- **v0.3** (2026-04-26 same-day, C3 R2 diff finding #5 patch)：**C3 dev-reviewer Round 2 diff verdict = FAIL only on stale specialization citation** ([review item #5](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-diff-2.md))。§1.2 §证明链显示 "Lemma C + Pirandola Eq. 11 [THM] ≤ -log_2(1-√η_AB)" 不准；实际 Eq. 11 是 REE cut UB，specific η-form 需 Eq. (8)/(9) + tele-cov + sym η split specialization（per [RETRACTION.md §9.3](../research/RETRACTION.md#93-l3g3-gap-id-round-揭露重大-pirandola-eq-11-citationspecialization-错误)）。修：§1.2 改 chain 显示 Eq. 11 → min_C E_R(C) → specialization → -log_2 形式分两步，加 "v0.3 corrected note" 说明 + cross-link 到 RETRACTION.md §9.3。L2.G1 主体 sign-direction closure 维持 PASS；本次仅 chain-citation accuracy 修补。
- **v0.3 final** (2026-04-26 same-day)：**C3 dev-reviewer Round 3 verdict = PASS** for A 项（[R3 review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-r3.md)）："§1.2 now uses the two-step `Eq. 11 -> min_C E_R(C) -> specialization -> -log_2` chain, with the v0.3 corrected note and `RETRACTION §9.3` cross-link present"。**L2.G1 C1 + C3 R3 PASS via C1(a)**；C2 待。
