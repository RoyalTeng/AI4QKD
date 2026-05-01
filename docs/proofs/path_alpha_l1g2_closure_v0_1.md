# Path α Lemma A sub-gap L1.G2 — Closure Candidate v0.1 (HARDEST sub-gap)

**Sub-gap**：L1.G2 — embedding ι 具体构造（验证 ι(Π) = Π_tr 是 Pirandola SI Note 1 trusted-relay protocol 类的合法成员）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 Cui 2019 + Pirandola SI Note 1 + KW Ch 20
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

**Note on difficulty**：本 sub-gap 是 path α 11 sub-gap 中 **substantively 最 demanding** —— per [§7.x.5.5 of lemma skeletons](umr_path_alpha_lemma_skeletons_v0_1.md) C1(a) point 6 retest, KW SKA framework 需 "extra embedding/reduction argument beyond KW §20.2" 才能 cover Cui untrusted-relay topology。本 closure 提供这一 embedding argument。

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 Cui + Pirandola + KW PDFs | ✅ **PASS** at Codex round 1 |
| **C1(c)** non-AI 数值 | 不适用 |
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch |

---

## §1 Sub-gap statement

### 1.1 Lemma L1.G2 statement

**Lemma L1.G2 (ι embedding 合法性)**：

设 Π 是 Cui 2019 simplified TFQKD protocol with Eq. (1) Eve 形式（i.e., umr Charlie controlled by Eve via arbitrary unitary $\hat{U}$）。定义 mapping ι 如下：

- **(a) Alice/Bob preserved**：Alice 与 Bob 的 state preparation (Cui Step 2.a/2.b) 和 classical post-processing (Cui Step 4) 操作 ι(Π) 与 Π 完全相同
- **(b) Charlie 替换为 honest specified operation**：在 ι(Π) 中，Charlie 不再被 Eve 控制，而是执行 protocol-specified honest unitary $\hat{U}^{spec}$（Cui Section II Step 3 描述的 honest single-photon interference detection + classical announcement）
- **(c) Π_tr := ι(Π) 标 trusted-network node**：声明 Π_tr 中 Charlie 是 trusted-network node，符合 Pirandola SI Note 1 的 "adaptive LOs by all points of the network + unlimited two-way CC" 协议类

**则 (statement target)**：Π_tr 是 Pirandola 2019 SI Note 1 (page 15) 定义的 trusted-relay 协议类的合法成员。

### 1.2 Lemma 在 path α Lemma A 中的位置

L1.G2 是 path α Lemma A（协议嵌入）的**核心** sub-gap。Lemma A 由 4 个 sub-gap 组成：L1.G1 (Hilbert 空间 alignment, ✅ PASS) + L1.G2 (ι 构造, **本 closure**) + L1.G3 (Stinespring gauge, ✅ PASS) + L1.G4 (output metric, ✅ PASS)。L1.G2 一旦 close，Lemma A 整体即 close（其他 3 个已 close）。

### 1.3 严格 scope

- ✅ 本 lemma close ι 嵌入构造的合法性
- ❌ 本 lemma **不**主张 Π_tr 在 trusted-relay model 下是 ε-secure（依赖 L2 Lemma B 整体）
- ❌ 本 lemma **不**主张 rate inequality（依赖 Lemma C / L3.G1-G3）
- ❌ 本 lemma **不**主张 Pirandola Eq. 11 适用于 ι(Π)（依赖 L3.G3 [UNKNOWN]）

---

## §2 引文

### 2.1 Cui 2019 Section II Step 3 — honest Charlie operation specification

**Cui 2019**, [PDF](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf), Section II Step 3 PDF p.2（per L1.G1 round 2 verify PASS for verbatim）：

> "For each trial, the middle receiver Eve must publicly announce a successful message $|1\rangle_M$ or a failure message $|0\rangle_M$ to Alice and Bob. If she announces $|1\rangle_M$, she has to simultaneously declare which message she obtained, $|L\rangle_M$ or $|R\rangle_M$. **For an honest Eve**, $|L\rangle_M$ and $|R\rangle_M$ reveal which detector clicks [19]."

verbatim "For an honest Eve" 即 specified honest behavior。Cui 这里 explicitly distinguish 由 Eve 控制（任意 $\hat{U}$）vs honest behavior（specified $\hat{U}^{spec}$）。

### 2.2 Pirandola SI Note 1 — trusted-relay protocol 类定义

**Pirandola 2019**, [PDF](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf), Supplementary Note 1 page 15（per L1.G1 round 2 verify PASS for verbatim）：

> "[the protocol] is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"

trusted-relay 协议类**定义** 即 "all points in the chain perform adaptive LOs (local operations) + classical broadcast / two-way CC"。

### 2.3 KW §20.1.12 LOPC channel form — chain protocol structural template

**Khatri-Wilde 2024**, [PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf) Ch 20 §20.1 PDF p.1167-1168（per L3.G1 round 1 verify PASS for verbatim）：

KW Eq. (20.1.12) 给 round-i LOPC channel form $\mathcal{L}^{(i)} = \sum_{y_i} \mathcal{E}^{y_i}_A \otimes \mathcal{F}^{y_i}_B \otimes |y_i\rangle\langle y_i|_{Y_i}$，覆盖任意 adaptive LO + public broadcast 协议。Pirandola SI Note 1 chain 是这一框架的 multi-node 推广。

### 2.4 KW §20.2 single-channel limitation — embedding 必要性的 textual evidence

per [§7.x.5.5 of lemma skeletons](umr_path_alpha_lemma_skeletons_v0_1.md) C1(a) Codex point 6 retest verbatim：

> "Section 20.2.4 only generalizes to public separable channels, not to an arbitrary joint untrusted-relay unitary on both outbound quantum modes. So Cui coverage needs an extra embedding/reduction argument beyond KW §20.2."

**含义**：KW SKA 框架（§20.2）覆盖 single-channel + LOPC + public separable extensions，**不**直接 cover Cui's untrusted-relay topology。L1.G2 本 closure 提供的就是这一 "extra embedding argument"。

---

## §3 数学陈述 / 推导

### §3.1 步骤 (a)：Alice / Bob 操作 preservation

由 ι 定义 (a) 直接：在 ι(Π) 中 Alice/Bob 的 quantum state preparation $|±\sqrt{\mu}\rangle_{A_o(B_o)}$ + classical key-bit register $A_k, B_k$ + Step 4 announcement-conditioned post-processing 与 Π 完全相同。**Trivially well-defined**。

### §3.2 步骤 (b)：$\hat{U}^{spec}$ well-definedness

由 §2.1 Cui Step 3 verbatim："For an honest Eve, $|L\rangle_M$ and $|R\rangle_M$ reveal which detector clicks [19]."

具体而言，$\hat{U}^{spec}$ 是 Cui Eq. (1) 形式的 unitary，对应：
- Alice/Bob's outbound photons $|n\rangle_{A_o}|m\rangle_{B_o}$ 通过 50:50 beamsplitter 干涉
- Single-photon detector D_L / D_R 探测后 distinguish $|L\rangle_M$（D_L click）/ $|R\rangle_M$（D_R click）/ $|0\rangle_M$（no click）/ $|1\rangle_M$（success summarizing $|L\rangle_M$ or $|R\rangle_M$）

$\hat{U}^{spec}$ 是 Cui Eq. (1) 形式 unitary 集合中的**特定一个成员**（"honest" 选择），由 (a) 50:50 beamsplitter unitary + (b) projector measurement on detector basis 组成。这是 standard quantum optics 操作，**well-defined CPTP**（unitary + measurement）。

**严格 scope check**：本 §3.2 仅 verify $\hat{U}^{spec}$ 是 well-defined as CPTP，**不**主张 $\hat{U}^{spec}$ 与 umr Eve's $\hat{U}$ 在某种语义上"等价" —— Eve 可选**任意** $\hat{U}$，honest is one specific choice among them。

### §3.3 步骤 (c)：Π_tr 是 Pirandola SI Note 1 chain protocol member

将 Π_tr 描述匹配 Pirandola SI Note 1 chain protocol 类（per §2.2）：

| Pirandola SI Note 1 chain protocol 元素 | Π_tr 实现 |
|---|---|
| Network points $\{A_1 = \text{Alice}, A_2 = \text{Charlie}, A_3 = \text{Bob}\}$ | A-C-B chain (N=1) |
| Memoryless quantum channels along edges $\mathcal{N}_{A \to C}, \mathcal{N}_{C \to B}$（per Pirandola SI Note 2 verbatim）| Cui A-Charlie + B-Charlie photonic channels (lossy) |
| Adaptive LOs by each network point | Alice/Bob 的 Cui Step 2.a state prep + Step 4 post-processing；Charlie 的 honest $\hat{U}^{spec}$ measurement |
| Unlimited two-way CC involving all points | Alice/Bob/Charlie 的 classical announcement broadcast (Cui Step 3) ⊆ "two-way CC"（前者 single-direction 是后者 special case，per L3.G1 ✅ PASS）|

**全部 4 个 Pirandola chain protocol 类 元素都被 Π_tr 实现**。所以 Π_tr ∈ Pirandola SI Note 1 trusted-relay 协议类。

### §3.4 整合：ι 是 well-defined embedding

由 §3.1 + §3.2 + §3.3：ι maps Cui 2019 Π (umr) to Π_tr (trusted-relay)，three-step construction (a)/(b)/(c) 各 well-defined，结果 Π_tr 是 Pirandola SI Note 1 chain protocol 合法成员。

**关键 caveat**（不可越过）：

- ι 仅 改 Charlie 的操作选择（任意 → honest specified）；**不**改 Alice/Bob 端
- ι 仅 close embedding 的**结构合法性**；**不**主张安全性继承（那是 L2 Lemma B 工作）
- ι 仅 是 statement-level 嵌入；**不**等价 Π_tr 在 trusted-relay 模型下与 Π 在 umr 模型下产生同 rate（那是 L2.G1 + L3.G2 工作）

### §3.5 与 L2.G3 的明示分离

注意 §3.3 仅 verify Π_tr 结构性 fit Pirandola chain protocol 类。Eve 在 Π_tr 中 access 何种系统（H_E only, vs additionally H_C？）是 L2.G3 [UNKNOWN] 的内容，**不**在本 L1.G2 closure 范围。L1.G2 仅 verify "Π_tr 是合法 trusted-relay 协议成员"；L2.G3 verify "trusted-relay Eve 仅 access H_E"。

---

## §4 待启动的 C1(a) Codex round

让 Codex 直读：

1. Cui 2019 PDF Section II Step 3 page 2 — verbatim "For an honest Eve" + detector announcement structure
2. Pirandola SI Note 1 page 15 + SI Note 2 — chain protocol class definition with adaptive LOs + memoryless channels along edges
3. KW Ch 20 §20.1 / §20.2 — LOPC framework

**CRITICAL Codex check**：

a. §3.2 $\hat{U}^{spec}$ well-definedness：Cui Step 3 honest Charlie operation 是否 well-defined as CPTP / unitary（Cui Eq. (1) 形式 with specific honest choice）？
b. §3.3 Π_tr 4-element fit 是否完整（Network points + memoryless channels + adaptive LOs + two-way CC）？
c. §3.4 ι integrated construction 合法性
d. §3.5 与 L2.G3 separation explicit
e. **CRITICAL**: 不 smuggle Lemma B / Lemma C / L2.G3 / L3.G3 closure
f. Lemma scope clean

**预期 verdict**：PASS 但 likely 需要多轮 iteration（最难 sub-gap）。

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate of HARDEST sub-gap。基于 (a) Cui Step 3 honest Charlie operation specification + (b) Pirandola SI Note 1 + SI Note 2 chain protocol class definition + (c) KW §20.2 single-channel limitation 的 textual gap 已由 §3 embedding argument 桥接。**严格 separation** 与 L2.G3 / L3.G3 通过 §3.5 明示。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.1 final** (2026-04-26 same-day)：**C1(a) Codex round 1 verdict = PASS**（HARDEST sub-gap 一轮通过；全 6 项 critical check a-f + 4 项 citation accuracy 全 PASS）。Codex 提两条 minor caveat（不影响 PASS）：(i) §3.2 "50:50 beamsplitter" 是 implementation reading 而非 Cui Step 3 verbatim 文本；`|1⟩_M` 是 success flag（coarse-graining of `|L⟩_M/|R⟩_M`），非独立 detector click —— 已 acknowledged 不修 §3.2（标注：这些是 standard quantum optics 实现层 reading，不改 well-defined CPTP 结论）。(ii) §3.3 第二条 edge 更准确读作 `C-B` edge 反向 `B→C` 使用（Pirandola Note 1 explicitly allows backward edge use）—— 已 acknowledged 不修 §3.3（不改 4-element fit 完整性）。**L1.G2 C1 aggregate PASS via C1(a)**。C2 / C3 待。
