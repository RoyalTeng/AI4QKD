# Path α Lemma A sub-gap L1.G1 — Closure Candidate v0.1

**Sub-gap**：L1.G1 — Hilbert 空间对齐（umr 协议 Π 与 trusted-relay 协议 Π_tr = ι(Π) 共享同一全局 Hilbert space，仅 Eve 访问子集不同）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 Cui 2019 + Pirandola SI Note 1 + KW Ch 20
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读多 PDF | ✅ **PASS** at Codex round 2 |
| **C1(c)** non-AI 数值 | 不适用（definitional / framework alignment 无数值 question）|
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch |

**关键边界**：
- 本文档**仅** close L1.G1
- L1.G2, L1.G3 (closed), L1.G4 (closed), L2.G1-G4, L3.G1-G3 状态不变

---

## §1 Sub-gap statement

### 1.1 全局 Hilbert space 定义

设 $\mathcal{H}_{global} = \mathcal{H}_{A_o} \otimes \mathcal{H}_{B_o} \otimes \mathcal{H}_C \otimes \mathcal{H}_E \otimes \mathcal{H}_M$，其中：

- $\mathcal{H}_{A_o}$：Alice 送给 Charlie 的 photonic outbound 模式（Fock space，basis $|n\rangle_{A\text{-out}}$, $n \in \mathbb{N}_0$）
- $\mathcal{H}_{B_o}$：Bob 送给 Charlie 的 photonic outbound 模式（同上）
- $\mathcal{H}_C$：Charlie 的 measurement-device 内部 Hilbert space（用于 implementing measurement-and-broadcast 操作）
- $\mathcal{H}_E$：Eve 的 ancilla
- $\mathcal{H}_M$：Charlie 公开宣告的 classical message register（含 $|0\rangle_M$ failure，$|1\rangle_M$ success，$|L\rangle_M$/$|R\rangle_M$ detector labels）

注：Alice/Bob 的本地 classical key-bit 寄存器 $\mathcal{H}_{A_k}, \mathcal{H}_{B_k}$ **不**在 Charlie 的操作 reach 内（Cui 2019 Step 2.a：Alice/Bob 用 random classical key bit 选 coherent state，key bit 本身保留在本地）。本文档 §1.1 只定义"Charlie reach within 的 Hilbert space" $\mathcal{H}_{global}$。

### 1.2 Lemma L1.G1 statement

**Lemma L1.G1**：协议 Π（umr，Cui 2019）与协议 Π_tr = ι(Π)（trusted-relay，path α 嵌入产物）操作于**同一**全局 Hilbert space $\mathcal{H}_{global}$ 定义如 §1.1。两协议的差别**仅在 Charlie 的操作选择**：

- 在 Π 下：Charlie 的操作 $\hat{U}$ 由 Eve **任选**（任意 unitary on $\mathcal{H}_{global}$，per Cui 2019 Eq. (1) 形式 $\hat{U}|n\rangle_{A_o}|m\rangle_{B_o}|E_0\rangle_{Ea}|0\rangle_M = \sqrt{Y_{n,m}}|\gamma_{n,m}\rangle_E |1\rangle_M + \cdots$）
- 在 Π_tr 下：Charlie 的操作 $\hat{U}^{spec}$ 由协议规定（Cui Step 3 honest single-photon interference detection + classical announcement，per Pirandola SI Note 1 trusted-relay 协议类的 "adaptive LO + classical broadcast"）

**Eve 访问子集**（key 区分）：

- 在 Π 下：Eve 访问 $\mathcal{H}_C \otimes \mathcal{H}_E$（即 Eve 控 Charlie's internal + her ancilla；具体 via 选 $\hat{U}$ 含 $\mathcal{H}_C$ 上的任意作用）
- 在 Π_tr 下：Eve 访问 $\mathcal{H}_E$ only（trusted-relay Eve 不触 Charlie's internal $\mathcal{H}_C$，per Pirandola SI Note 1 + KW Ch 20 §20.1 SKA framework 的 trusted-network-node 假设）

### 1.3 严格 scope

- ✅ 本 lemma 是 **framework alignment claim**：Π / Π_tr Hilbert space 一致
- ❌ 本 lemma **不**主张 ι 嵌入合法性（依赖 L1.G2）
- ❌ 本 lemma **不**主张 Eve set ⊆ 关系（依赖 L2.G3）—— 仅 stating Eve access subset 描述，**不**推 inclusion
- ❌ 本 lemma **不**主张 rate monotonicity（依赖 L2.G1）

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 Π（umr）的 Hilbert space — Cui 2019

**Cui-Yin-Wang-Chen-Wang-Guo-Han 2019**, *Phys Rev Applied* 11:034053 ("Twin-Field QKD without Phase Postselection")，[PDF](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf)，Section II Step 2.a-Step 3 + Eq. (1)（PDF p.2）

verbatim 预期文本（已在 §7.x 早前 C1(a) round verify PASS at point 1, 2）：

> "Eve's most general collective attack to the above simplified TFQKD protocol can be defined as an arbitrary measurement after an arbitrary unitary operation operating on the whole system with her pre-prepared ancilla [4,5]. Under photon-number representation, this collective attack is given by
> $\hat{U}|n\rangle_{A\text{-out}}|m\rangle_{B\text{-out}}|E_0\rangle_{Ea}|0\rangle_M = \sqrt{Y_{n,m}}|\gamma_{n,m}\rangle_E |1\rangle_M + \sqrt{1-Y_{n,m}}|\text{other}\rangle_E |0\rangle_M$"

**含义**：Cui 直接 specify $\mathcal{H}_{global} = \mathcal{H}_{A_o} \otimes \mathcal{H}_{B_o} \otimes \mathcal{H}_{Ea} \otimes \mathcal{H}_M$（这里 Cui 把 $\mathcal{H}_C$ 隐式 absorb 进 $\hat{U}$ 的 dilation —— 但等价于把 $\mathcal{H}_C$ 当作 Eve 内部 ancilla 的一部分，因为 Cui Eve 控 $\hat{U}$ 整个）。**Path α §1.1 explicit 把 $\mathcal{H}_C$ 拆出来作为 Charlie's internal**，对应 Cui $\hat{U}$ 的 Stinespring dilation 中 Charlie-attributed 的部分。

### 2.2 Π_tr（trusted-relay）的 Hilbert space — Pirandola SI Note 1 + KW Ch 20

**Pirandola 2019**, *Nat Commun* 10:1006，Supplementary Note 1（"Network adaptive protocols"），[PDF](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf) PDF p.15

verbatim per Codex C1(a) L1.G1 round 1 direct read：

> "[the protocol] is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"

(后续段落讨论 broadcasts / feedback / local registers per Codex finding。)

**Khatri-Wilde 2024**（已在 §7.x.5.5 C1(a) point 6 retest 部分 confirm）, Chapter 20 §20.1 "n-Shot Secret-Key-Agreement Protocol"，PDF p.1178 / printed p.1165：

verbatim 预期：

> "we suppose that there is a quantum channel $\mathcal{N}_{A \to B}$ connecting the legitimate sender Alice to the legitimate receiver Bob...the quantum eavesdropper has access to the environment system $E$...the eavesdropper has access to all of the classical data exchanged between the legitimate parties."

**Network 推广**：KW §20.1 描述的是 single-channel SKA；扩展到 path α 的 two-channel-via-trusted-relay 即 Pirandola SI Note 1 chain protocol。两者共享 "Eve = environment + public classical data" 的 access 模型。

### 2.3 Hilbert space alignment 推论

由 §2.1 + §2.2：Π 与 Π_tr **operate on** the same Cui Eq. (1) Hilbert space $\mathcal{H}_{global}$，因为：

- Π 是 Cui 2019 simplified TFQKD（umr）—— per Cui Eq. (1) Hilbert space
- Π_tr = ι(Π) 是 Cui 2019 simplified TFQKD with Charlie's $\hat{U}$ replaced by $\hat{U}^{spec}$ —— **同一** Hilbert space，仅 Charlie 的 unitary 不同

**Eve access 区分**（per §1.2）：

- Π：Eve 控整个 $\hat{U}$ → 访问 $\mathcal{H}_C \otimes \mathcal{H}_E$（Pirandola SI Note 1 之 untrusted relay 模型，KW 之 active eavesdropper-controlled-channel 模型）
- Π_tr：Charlie 控 $\hat{U}^{spec}$ → Eve 仅访问 $\mathcal{H}_E$ + announcement（Pirandola SI Note 1 之 trusted-relay node 模型，KW Ch 20 §20.1 之 environment-only Eve）

L1.G1 仅 stating 这一 framework alignment + Eve access 子集差别，**不**主张 inclusion / rate / security 任何 implication。

---

## §3 数学陈述（直接由 §1.1, §1.2）

### §3.1 Hilbert space identity

$$\mathcal{H}_{global}^{\Pi} \;=\; \mathcal{H}_{global}^{\Pi_{tr}} \;=\; \mathcal{H}_{A_o} \otimes \mathcal{H}_{B_o} \otimes \mathcal{H}_C \otimes \mathcal{H}_E \otimes \mathcal{H}_M$$

直接 by 协议定义 + §1.1。

### §3.2 Eve access partition

定义 Eve access subset operator-algebra（Eve 能 implement 的 quantum operations 的 algebra）：

$$\mathcal{A}^{\Pi}_{Eve} \;\subseteq\; \mathcal{B}(\mathcal{H}_C \otimes \mathcal{H}_E) \quad \text{(umr Eve)}$$
$$\mathcal{A}^{\Pi_{tr}}_{Eve} \;\subseteq\; \mathcal{B}(\mathcal{H}_E) \quad \text{(trusted-relay Eve)}$$

$\mathcal{B}(\mathcal{H})$ 是 $\mathcal{H}$ 上有界算子集合。

注意 §3.2 仅 STATE access subset 描述，不 claim $\mathcal{A}^{\Pi_{tr}}_{Eve} \subseteq \mathcal{A}^{\Pi}_{Eve}$（虽然这看起来 obvious，但这是 L2.G3 [UNKNOWN] 的内容，需 separate closure）。

---

## §4 待启动的 C1(a) Codex round

**任务**：让 Codex 跨家族 AI 直读：

1. [Cui 2019 PDF](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf) Section II Step 2.a-3 + Eq. (1)
2. [Pirandola 2019 PDF](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf) SI Note 1 page 15
3. [KW PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf) Chapter 20 §20.1 PDF p.1178

**Verify**：

1. Cui Eq. (1) Hilbert space 描述与 §1.1 / §2.1 一致
2. Pirandola SI Note 1 trusted-relay Hilbert space 与 §2.2 一致
3. KW Ch 20 §20.1 SKA Eve access 与 §2.2 一致
4. §3.1 Hilbert space identity 与上述三者 textually consistent
5. §3.2 Eve access partition 仅 stating 描述，不 smuggle inclusion claim（→ 这是 L2.G3 的工作，本 closure **不**做）
6. Lemma scope clean：L1.G1 仅 framework alignment，不 smuggle L1.G2 / L2.G3 / L2.G1

**预期 verdict**：PASS（这是 framework / definitional alignment，不是 deep theorem）。

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 Cui 2019 Eq. (1) + Pirandola SI Note 1 + KW Ch 20 §20.1。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL only on §2.2 Pirandola verbatim quote 不 match（实际是 "is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"）。其他全部 PASS（§1.1 framework alignment / §1.2 statement / §2.1 Cui / §2.3 alignment 推论 / §3.1 / §3.2 不 smuggle L2.G3 inclusion / §1.3 / §4 scope clean）。仅修 §2.2 verbatim text per Codex direct read。
- **v0.2 final** (2026-04-26 same-day)：**C1(a) Codex round 2 verdict = PASS**。Pirandola SI Note 1 verbatim 已 match；其余 7 项 sub-check 维持 PASS。**L1.G1 C1 aggregate PASS via C1(a)**。C2 / C3 待。
