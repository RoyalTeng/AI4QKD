# Path α Lemma C sub-gap L3.G1 — Closure Candidate v0.1

**Sub-gap**：L3.G1 — LOPC syntax 跨 topology（Cui per-trial single-direction Charlie announcement 是 KW §20.1.12 LOPC channel + Pirandola SI Note 1 two-way CC 的 syntactic 特例）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 KW Ch 20 §20.1 + Pirandola SI Note 1 + Cui 2019 Step 3
**严谨性 banner**：[SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify ∧ C2 user signature]

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读多 PDF | ✅ **PASS** at Codex round 1 |
| **C1(c)** non-AI 数值 | 不适用 |
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch |

---

## §1 Sub-gap statement

### 1.1 Lemma L3.G1 statement

**Lemma L3.G1 (LOPC syntactic compatibility)**：

Cui 2019 Step 3 的 Charlie per-trial single-direction announcement (Charlie → Alice + Bob 经典广播) 在 syntax 层面**符合**（即可以被表达为）KW Ch 20 §20.1 LOPC channel framework Eq. (20.1.12) 的 special case，并 consistent with Pirandola 2019 SI Note 1 chain protocol 的 "unlimited two-way CC" classical communication assumption。

具体：
- KW §20.1.12 LOPC channel form: $\mathcal{L}^{(i)} = \sum_{y_i} \mathcal{E}^{y_i}_A \otimes \mathcal{F}^{y_i}_B \otimes |y_i\rangle\langle y_i|_{Y_i}$，其中 $Y_i$ 是 "eavesdropper's copy of the classical data exchanged"（KW PDF p.1167-1168 verbatim）
- Cui Step 3 per-trial announcement 可以 embed 为 KW 框架下 $Y_i$ 的具体实现（Charlie 的 measurement outcome 作为 round i 的 classical data）
- Pirandola SI Note 1 "unlimited two-way CC involving all the points in the chain" 涵盖单向 announcement（more permissive includes less permissive）

**严格 scope**：本 lemma 仅 close **syntactic compatibility**；**不**主张 rate equivalence（依赖 L3.G2）或 security inheritance（依赖 L1.G2 / L2.G3）。

### 1.2 Lemma 在 path α Lemma C 中的位置

Path α Lemma C 主张 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$。这要求 Cui 的 per-trial rate definition 与 Pirandola 的 chain rate definition 在 syntactic + semantic level 都对齐。L3.G1 close 的是 **syntactic** layer——即 Cui announcement protocol 可以表述为 LOPC framework 下的合法 protocol。Semantic layer (rate definition + Devetak-Winter ↔ private-state criterion) 是 L3.G2 [UNKNOWN]。

### 1.3 严格 scope

- ✅ 本 lemma 仅 syntactic / structural compatibility
- ❌ 本 lemma **不**主张 rate 数值相等
- ❌ 本 lemma **不**主张 Π_tr 继承 Π 的 security
- ❌ 本 lemma **不**主张 KW SKA framework 直接 cover Cui 2019 untrusted-relay topology（per §7.x.5.5 point 6 retest, KW §20.2 framework 用 single-channel N_{A→B}; path α 的 two-channel-via-relay topology 需 separate embedding argument, 是 L1.G2 工作）

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 KW §20.1.12 LOPC channel form

**Khatri-Wilde 2024**, [PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf), Chapter 20 §20.1 PDF p.1167-1168:

verbatim Eq. (20.1.12)（直接 from PDF extract）:

$$\mathcal{L}^{(i)}_{A'_{i-1} B_{i-1} B'_{i-1} \to A'_i A_i B'_i Y_i} = \sum_{y_i} \mathcal{E}^{y_i}_{A'_{i-1} \to A'_i A_i} \otimes \mathcal{F}^{y_i}_{B_{i-1} B'_{i-1} \to B'_i} \otimes |y_i\rangle\langle y_i|_{Y_i}$$

其中 KW PDF p.1168（待 Codex direct read confirm verbatim）：

> "The classical system $Y_i$ represents the eavesdropper's copy of the classical data exchanged by Alice and Bob in this round of LOPC."

### 2.2 Pirandola SI Note 1 chain CC

**Pirandola 2019**, SI Note 1 page 15（已在 L1.G1 round 2 verify PASS for verbatim "is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"）：

verbatim:

> "[the protocol] is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"

### 2.3 Cui Step 3 per-trial announcement

**Cui-Yin-Wang-Chen-Wang-Guo-Han 2019**, Section II Step 3 PDF p.2 (per L1.G1 round 2 verify; verbatim待 Codex round confirm):

> "For each trial, the middle receiver Eve must publicly announce a successful message $|1\rangle_M$ or a failure message $|0\rangle_M$ to Alice and Bob..."

### 2.4 Syntactic embedding 推导

由 §2.1 + §2.2 + §2.3：

- KW §20.1.12 把 round i 的 classical data $Y_i$ 设为 "eavesdropper's copy"，且 LOPC 包括 任意 sum over $y_i$ 的 CP map decomposition
- Cui Step 3 per-trial announcement = Charlie 把 $|y\rangle$ ($y \in \{|0\rangle_M, |1\rangle_M, |L\rangle_M, |R\rangle_M\}$) 公开广播 → 这就是 KW 框架下 round i 的 $Y_i$
- Pirandola SI Note 1 "unlimited two-way CC" 比 Cui 的 "single-direction Charlie → A,B" 更 permissive（包含后者）

所以 Cui 协议的 announcement structure 是 KW §20.1.12 + Pirandola SI Note 1 framework 下的 **valid special case**。

**注意**：embedding 仅是 syntactic compatibility（"Cui can be re-expressed in KW form"），**不**主张 KW SKA capacity formula（针对 single-channel topology）直接 apply 到 Cui 协议（multi-channel-via-relay topology）。后者是 L1.G2 / L3.G2 工作。

---

## §3 数学陈述

L3.G1 是 **structural syntactic** lemma，**无**独立数学推导。closure 内容 = §2.4 的 syntactic embedding 论证。

---

## §4 待启动的 C1(a) Codex round

让 Codex 直读：

1. KW PDF Ch 20 §20.1 PDF p.1167-1168 verify Eq. (20.1.12) verbatim form + $Y_i$ 描述
2. Pirandola SI Note 1 page 15 verbatim "two-way CC involving all the points in the chain"（已 verify）
3. Cui 2019 PDF Section II Step 3 verbatim "publicly announce a successful message"
4. §2.4 syntactic embedding 论证 valid（不 smuggle rate / security claim）
5. **CRITICAL**: §1.3 严格 scope — L3.G1 不 close L1.G2 / L2.G3 / L3.G2

**预期 verdict**：PASS（standard syntactic embedding；syntactically more permissive framework 包含 less permissive special case）

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 KW §20.1.12 LOPC channel form + Pirandola SI Note 1 chain CC + Cui Step 3 per-trial announcement。L3.G1 是 syntactic / structural compatibility lemma。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.1 final** (2026-04-26 same-day)：**C1(a) Codex round 1 verdict = PASS**。全 6 项 sub-check 通过；Codex 提一个 minor notation caveat（公共符号 alphabet 应为 `{0,(1,L),(1,R)}`）但不影响 PASS。**L3.G1 C1 aggregate PASS via C1(a)**。C2 / C3 待。
