# Path α Lemma A sub-gap L1.G3 — Closure Candidate v0.1

**Sub-gap**：L1.G3 — Stinespring gauge invariance（Charlie 的 specified honest measurement $\hat{U}^{spec}$ 的 Stinespring dilation 选择不影响 Eve-marginal）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 KW PDF Chapter 4
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 KW PDF Ch 4 | ✅ **PASS** at Codex round 3（3 轮 substantive math + citation 校对完成）|
| **C1(c)** non-AI 数值（可选 add-on）| 不适用（结构性 lemma，无数值 question）|
| **C1** aggregate（OR over (a)/(b)/(c)）| ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待（与后续 sub-gap batch）|

**关键边界**：
- 本文档**仅** close L1.G3
- L1.G1, L1.G2, L1.G4 (已 closed), L2.G1-G4, L3.G1-G3 状态不变

---

## §1 Sub-gap statement (precise)

### 1.1 Abstract lemma statement (general Stinespring gauge invariance)

**Lemma L1.G3 (abstract)**：设 $\mathcal{N}: \mathcal{L}(\mathcal{H}_{A_{in}}) \to \mathcal{L}(\mathcal{H}_{A_{out}})$ 是 CPTP（completely positive trace-preserving）map。设 $V_1: \mathcal{H}_{A_{in}} \to \mathcal{H}_{A_{out}} \otimes \mathcal{H}_{E_1}$ 与 $V_2: \mathcal{H}_{A_{in}} \to \mathcal{H}_{A_{out}} \otimes \mathcal{H}_{E_2}$ 是 $\mathcal{N}$ 的两个 Stinespring isometric extensions。

**Conclusion 1（不假设维度排序的 well-defined output marginal）**：对任意 input $X \in \mathcal{L}(\mathcal{H}_{A_{in}})$：

$$\mathrm{Tr}_{E_1}(V_1 X V_1^\dagger) \;=\; \mathrm{Tr}_{E_2}(V_2 X V_2^\dagger) \;=\; \mathcal{N}(X) \in \mathcal{L}(\mathcal{H}_{A_{out}})$$

这是 Stinespring 表征定义本身的直接 consequence —— 任意 dilation 必须 reproduce $\mathcal{N}$（即 KW Theorem 4.3 (4) 的 defining property $\mathcal{N}(X) = \mathrm{Tr}_E[V X V^\dagger]$）。**Conclusion 1 不依赖 isometry-relating 的额外结构**。

**Conclusion 2（dimensional-ordered Stinespring isometry-relating，KW (4.3.3)-(4.3.7) 风格）**：**WLOG 设** $d_{E_1} \leq d_{E_2}$（否则交换 $V_1, V_2$ 角色）。则存在 isometry $W: \mathcal{H}_{E_1} \to \mathcal{H}_{E_2}$（即 $W^\dagger W = \mathbb{1}_{E_1}$）使得

$$V_2 = (\mathbb{1}_{A_{out}} \otimes W) V_1$$

——即 lower-dimensional dilation $V_1$ 通过 isometric embedding $W$ "扩展"到 higher-dimensional dilation $V_2$。

**Note**：Conclusion 1 即 channel output gauge-invariance，**不**需要 Conclusion 2 的 isometry-relating 结构（直接 by definition）。Conclusion 2 是 finer-grained 结构性结果（KW (4.3.3)-(4.3.7) 风格），用于 §3.2 path α application 中对 Eve internal env 的 partial trace consistency。

**严格 scope of abstract lemma**：本 lemma 仅是 KW Theorem 4.3 + Eq. (4.3.3)-(4.3.7) 的 Stinespring uniqueness corollary。**不**涉及任何 path α 协议结构。

### 1.2 Application to path α Lemma A — separate claim

将 §1.1 abstract lemma 应用到 path α 嵌入 ι(Π) = Π_tr 中 Charlie 的 honest CPTP map $\hat{N}^{spec}: \mathcal{H}_{A_o} \otimes \mathcal{H}_{B_o} \to \mathcal{H}_M$（其中 $A_o, B_o$ 是 Alice/Bob 送给 Charlie 的 photonic outbound 模式 —— per Cui 2019 Eq. (1) 的 $|n\rangle_{A\text{-out}}, |m\rangle_{B\text{-out}}$ 模式 —— 这两个模式被 Charlie 操作 absorb；$M$ 是 Charlie 的 announcement register）。

**Application claim**：取 $\mathcal{N} = \hat{N}^{spec}$ in §1.1 abstract lemma。则任意两个 Stinespring dilations $V_1: A_o B_o \to M \otimes E_{C,1}$ 和 $V_2: A_o B_o \to M \otimes E_{C,2}$ 在 announcement register 上的 marginal 相同：$\mathrm{Tr}_{E_{C,i}}(V_i X V_i^\dagger) = \hat{N}^{spec}(X)$ on $\mathcal{H}_M$。

**Implication for path α Π_tr 安全分析**（**conditional on** L1.G1 Hilbert 空间对齐 + L1.G2 ι 嵌入合法性 + L2.G3 Eve-set 跨空间 ⊆ 关系，这些都**仍 [UNKNOWN]**）：trusted-relay Eve 在 Π_tr 的 view 限于 announcement $M$ + Eve's own ancilla $E_{Eve}$（**不**包括 Charlie 的 specified internal env $E_{C,i}$）。给定那些 sub-gap 都已 close 的 hypothetical 状态，Eve 的 view marginal $\rho_{M E_{Eve}}$ 不依赖 dilation 选择 $E_{C,i}$ —— 这是**条件性**陈述，不是 stand-alone closure。

### 1.3 严格 scope 声明（重写后更明确）

- ✅ §1.1 abstract Stinespring uniqueness lemma：是 stand-alone closure（仅依赖 KW Theorem 4.3）
- ⚠️ §1.2 application to path α：是**条件性**陈述（依赖 L1.G1 / L1.G2 / L2.G3 [UNKNOWN]）
- ❌ 本 lemma **不**主张 ι 嵌入合法性
- ❌ 本 lemma **不**主张 Eve 的具体 access 模型（依赖 L2.G3）

---

## §2 引文（Citation accuracy 核对，pending C1(a) Codex round）

### 2.1 主 citation

**Khatri-Wilde 2024**, *Principles of Quantum Communication Theory: A Modern Approach*（arXiv:2011.04672, [PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)）

#### 2.1.a Stinespring 表征 — **Theorem 4.3** "Characterizations of Quantum Channels"（Chapter 4 §4.3 "Characterizations of Channels: Choi, Kraus, Stinespring"）at PDF p.158 / printed p.145

verbatim 预期文本（待 Codex 直读 confirm）：

> "**Stinespring**: There exists an isometry $V_{A \to BE}$, called an isometric extension, with $d_E \geq \mathrm{rank}(\Gamma^N_{AB})$, such that $\mathcal{N}(X_A) = \mathrm{Tr}_E[V X_A V^\dagger]$ for every linear operator $X_A$."

#### 2.1.b Kraus uniqueness up to isometry — KW (4.3.3)-(4.3.7) at PDF p.159 / printed p.146

verbatim 预期文本（待 Codex 直读 confirm）：

> "if $\{K_i\}^r$ and $\{K'_i\}^s$ are two sets of Kraus operators that realize the same quantum channel, then they are related by an isometry as in (4.3.3). This is a dynamical version of the statement made earlier in Section 3.2.5, the statement there being that all purifications of a state are related by an isometry acting on the purifying system."

#### 2.1.c Stinespring uniqueness 直接推论

由 §2.1.a Stinespring + §2.1.b Kraus uniqueness（注意 Kraus 与 Stinespring 通过 $V = \sum_i K_i \otimes |i\rangle_E$ 一一对应）：两个 Stinespring dilations $V_1, V_2$ of same channel 相关于 isometry $W$ on environment 即 $V_2 = (\mathbb{1}_B \otimes W) V_1$。

### 2.2 §3.2.5 purification gauge static analog

KW §3.2.5 给 static 版本：任意两个 purifications of a given state 由作用在 purifying system 上的 isometry 关联。**注意**：上一节 §2.1.b 段尾的"all purifications of a state are related by an isometry acting on the purifying system" 是 KW §4.3 段尾对 §3.2.5 的 paraphrase reference，**非** §3.2.5 verbatim quote。

L1.G3（dynamical Stinespring 版本）是 §3.2.5 的 channel-level analog；KW §4.3 显式 invoke 这一类比。

---

## §3 数学推导

### §3.1 Abstract lemma proof

#### §3.1.a Conclusion 1 — direct from Stinespring defining property

KW Theorem 4.3 (4)（PDF p.158）的 Stinespring 表征 explicitly 要求 dilation $V$ 满足

$$\mathcal{N}(X) = \mathrm{Tr}_E[V X V^\dagger] \quad \text{for all } X.$$

任意 dilation $V_1, V_2$ 都按定义满足这一恒等式 with their respective $E_1, E_2$。所以

$$\mathrm{Tr}_{E_1}(V_1 X V_1^\dagger) = \mathcal{N}(X) = \mathrm{Tr}_{E_2}(V_2 X V_2^\dagger)$$

直接 by definition。**Conclusion 1 QED**。

#### §3.1.b Conclusion 2 — dimensional-ordered isometry-relating

WLOG 设 $d_{E_1} \leq d_{E_2}$。

由 KW Theorem 4.3 + KW Eq. (4.3.3)-(4.3.7) + §4.3 段尾给的 Kraus uniqueness up to isometry（PDF p.159）：两个 Kraus reps $\{K_i^{(1)}\}_{i=1}^{r_1}$, $\{K_j^{(2)}\}_{j=1}^{r_2}$ of same channel（with $r_1 \leq r_2$）by an isometric matrix $V_{ji}$（$r_2 \times r_1$，即 $\sum_j V_{ji}^* V_{jk} = \delta_{ik}$）满足 $K_j^{(2)} = \sum_i V_{ji} K_i^{(1)}$。

将 Kraus rep 通过 $V = \sum_i K_i \otimes |i\rangle_E$ 转译到 Stinespring rep（with $|i\rangle_E$ orthonormal basis of $E$，$d_E = r$）：

$$V_2 = \sum_j K_j^{(2)} \otimes |j\rangle_{E_2} = \sum_{j,i} V_{ji} K_i^{(1)} \otimes |j\rangle_{E_2} = \sum_i K_i^{(1)} \otimes \left(\sum_j V_{ji} |j\rangle_{E_2}\right) = (\mathbb{1}_{A_{out}} \otimes W) V_1$$

其中 $W: \mathcal{H}_{E_1} \to \mathcal{H}_{E_2}$ 定义为 $W |i\rangle_{E_1} = \sum_j V_{ji} |j\rangle_{E_2}$，即 $W$ 的 matrix elements $\langle j | W | i \rangle = V_{ji}$。由 isometric 矩阵条件 $\sum_j V_{ji}^* V_{jk} = \delta_{ik}$ 得 $W^\dagger W = \mathbb{1}_{E_1}$。**Conclusion 2 QED**。

**结论**：**Conclusion 1**（channel output gauge-invariance）和 **Conclusion 2**（dimensional-ordered isometry-relating）都成立。Conclusion 1 直接 by Stinespring definition；Conclusion 2 由 KW (4.3.3)-(4.3.7) Kraus uniqueness 转译。**§1.1 abstract lemma QED**。

### §3.2 Application to path α (conditional, NOT stand-alone closure)

§1.2 给的 application 陈述是**条件性**：取 $\mathcal{N} = \hat{N}^{spec}_{A_o B_o \to M}$（Charlie's honest measurement-and-broadcast，per Cui Eq. (1) 的 $|n\rangle_{A\text{-out}} |m\rangle_{B\text{-out}} \to |1\rangle_M$ 等结构 reduce 到 $A_o B_o \to M$ 的 CPTP）。则 §3.1 abstract lemma 直接给出：

$$\mathrm{Tr}_{E_{C,i}}(V_i X V_i^\dagger) \;=\; \hat{N}^{spec}(X) \in \mathcal{L}(\mathcal{H}_M) \quad \text{for any } X \in \mathcal{L}(\mathcal{H}_{A_o B_o}), \text{ any dilation } i$$

**Eve-view 在 path α Π_tr 的 gauge invariance 是 conditional**：要把"announcement marginal 不依赖 dilation"扩到"Eve 全局 view 不依赖 dilation"，需额外承诺 Eve 的 access 模型 = $(M, E_{Eve})$ 而非 $(M, E_{Eve}, E_{C,i})$。这一 access 模型 commitment 是 L2.G3（Eve set across spaces，**仍 [UNKNOWN]**）的内容，不在本 closure 范围。

**严格表述**：本 §3 只 close 了 §1.1 abstract Stinespring uniqueness lemma；§1.2 application 是 conditional consequence，待 L2.G3 closure 后才 unconditional。

---

## §4 待启动的 C1(a) Codex round

**任务**：让 Codex 跨家族 AI 直读 [KW PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf) Chapter 4，verify §2 列出的 textual support：

1. KW Theorem 4.3 (4) 给 Stinespring 表征 at PDF p.158
2. KW Eq. (4.3.3)-(4.3.7) + 后续段落给 Kraus uniqueness up to isometry at PDF p.159
3. KW §3.2.5 purification gauge analog 引用
4. §3 数学推导是上述的 immediate corollary

**预期 verdict**：PASS（教材级 Stinespring 标准结果）。

**lemma scope check**：本 closure **不** smuggle 其他 sub-gap closure。

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 KW Ch 4 §4.3 Theorem 4.3 + (4.3.3)-(4.3.7)。C1(a) Codex citation round 待启动。C1(c) 不适用（结构性 lemma 无数值 claim）。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL。Substantive 修复：(1) 把 V_i 的 input/output Hilbert space 写清（V_i: $A_{in} \to A_{out} \otimes E_i$，$A_{in}$ absorbed by V，$A_{out}$ 是 channel output）；(2) §3 数学推导用 partial trace identity $\mathrm{Tr}_{E_2}(W \cdot W^\dagger) = \mathrm{Tr}_{E_1}(\cdot W^\dagger W)$ 替代之前不正确的 cyclicity argument；(3) 拆分 §1.1 abstract stand-alone lemma 与 §1.2 conditional application to path α，明示后者依赖 L2.G3 [UNKNOWN]；(4) §2.2 修正 §3.2.5 引文 attribution（KW §4.3 paraphrase, 非 §3.2.5 verbatim）。
- **v0.3** (2026-04-26 same-day)：Codex round 2 verdict = FAIL on Stinespring uniqueness statement 缺 dimensional ordering。修复：拆分为 Conclusion 1（channel output gauge-invariance，直接 by Stinespring defining property，**不**需要 isometry-relating 结构）+ Conclusion 2（dimensional-ordered isometry-relating $W: E_1 \to E_2$ with $d_{E_1} \leq d_{E_2}$ WLOG，由 KW (4.3.3)-(4.3.7) Kraus uniqueness 转译）。Conclusion 1 已足够 path α gauge invariance 的核心 claim；Conclusion 2 给 finer-grained 结构（path α §3.2 application 用）。
- **v0.3 final** (2026-04-26 same-day)：**C1(a) Codex round 3 verdict = PASS**。全部 6 项 sub-check（Conclusion 1 数学 + Conclusion 2 数学 + §2.1.a citation + §2.1.b citation + scope cleanliness + §2.2 attribution）通过。**L1.G3 C1 aggregate PASS via C1(a)**。C2 / C3 待。
