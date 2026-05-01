# Path α Lemma B sub-gap L2.G2 — Closure Candidate v0.1

**Sub-gap**：L2.G2 — ε-composable 三分量分解（Π 整体 ε security 是否分解为 secret / correct / complete 三独立分量，per Portmann-Renner 2022 framework）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 Portmann-Renner 2022 RMP §III
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 Portmann-Renner 2022 PDF | ✅ **PASS** at Codex round 3 |
| **C1(c)** non-AI 数值 | 不适用（formal definitional 框架，无数值 question）|
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch |

---

## §1 Sub-gap statement

### 1.1 Lemma L2.G2 statement (corrected per Codex round 1 PDF direct read)

**Lemma L2.G2 (ε-composable security 由 soundness + completeness 两 orthogonal criteria 描述)**：

设 $\Pi$ 是 QKD 协议。Portmann-Renner 2022 RMP framework 区分**两个独立的安全性 criteria**（**非** additive decomposition）：

#### (i) Soundness — adversarial setting 下 Eve-vs-ideal distance

Per Portmann-Renner 2022 **Theorem 2** at PDF p.17：soundness ε 满足 **additive 2-component decomposition**：

$$\boxed{\varepsilon_{\text{sound}} \;\leq\; \varepsilon_{\text{secret}} + \varepsilon_{\text{correct}}}$$

其中（per Eq. (8) trace-distance form）：
- $\varepsilon_{\text{secret}}$ — Eve 与 Alice 密钥共享的 conditioned-on-no-abort trace-distance to ideal $\Phi^{ideal}_{K_A} \otimes \rho_E$
- $\varepsilon_{\text{correct}}$ — conditioned-on-no-abort $K_A \neq K_B$ 概率

#### (ii) Completeness / Robustness — no-adversary/noisy-channel setting 下 honest abort 概率

Per Portmann-Renner 2022 **§III.B.4 + Lemma 3** at PDF p.18：completeness $\varepsilon_0$ 是**独立** criterion（**非** soundness 的 additive component）：

$$\varepsilon_{\text{complete}} \;:=\; \Pr[\text{abort} \mid \text{honest execution, no Eve}]$$

**Lemma 3 关系**（per PDF p.18）：在 matching-parameter δ assumption 下，completeness failure $\varepsilon_0$ **bounded by** soundness failure。但这是 **conditional 约束**，**非** "ε_complete 是 ε_sound 的一部分"。

### 1.1.bis 与 v0.1 错误的对比

**v0.1 错误**（v0.2 已 corrected）：

```
ε ≤ ε_secret + ε_correct + ε_complete  ← 这是 v0.1 wrong form
```

把 completeness 当作 additive 第三分量。这**不是** Portmann-Renner 的 formulation。Portmann-Renner 把 completeness 作为**独立 criterion**（i.e., 两个 separate ε bound：soundness ε ≤ ε_s + ε_c，completeness ε_0 ≤ ...），不是 additive 三 sum。

**v0.2 corrected form**：上述 §1.1 (i) + (ii) 两 orthogonal criteria 表述。

### 1.2 Lemma 在 path α Lemma B 中的位置

Path α Lemma B 主张：if Π is ε-secure (umr Eve), then Π_tr = ι(Π) is ε-secure (trusted-relay Eve). L2.G2 给的是 ε 的内部结构（三分量），useful when 我们需要 separately bound 不同安全性 component（例如 secret 用 Cui Eq. (3) Devetak-Winter 分析，correct + complete 由 protocol structure 直接 bound）。

**严格 scope**：本 lemma 仅 close ε 的三分量分解 form；**不**主张 Π_tr 继承 Π 的 ε-secure 整体 conclusion（那是 L2.G3 + L2.G1 + L1.G2 共同蕴含的）。

### 1.3 严格 scope

- ✅ 本 lemma 是 **definitional decomposition**（Portmann-Renner framework 的标准 form）
- ❌ 本 lemma **不**主张 Π / Π_tr 任一具体 ε 的 numerical 上界
- ❌ 本 lemma **不**主张 Π 的 ε-secure conclusion（依赖 Cui 2019 Section III + L2.G4 [UNKNOWN]）
- ❌ 本 lemma **不**主张 Π_tr 继承 Π 的 ε-secure conclusion（依赖 L2.G3 / L1.G2 [UNKNOWN]）

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 主 citation

**Portmann-Renner 2022**, *Reviews of Modern Physics* "Security in quantum cryptography"（arXiv:2102.00021v2, [PDF](../literature/pdfs/Portmann-Renner-2022-SecurityQuantumCryptography-arXiv2102.00021.pdf), 63 pages）：

- **§III.B.3 "Correctness & secrecy"** — give ε = ε_secret + ε_correct decomposition (待 Codex direct read confirm verbatim formula + page)
- **§III.B.4 "Robustness"** — give ε_complete/robust as third component (待 Codex direct read confirm)
- **§III.A.3 "Security"** — Composable security definition framework
- **§III.B.1 "Trace distance"** + **§III.B.2 "Simulator"** — reduction to trace-distance criterion

### 2.2 Path α Π 的 ε 来源（Cui 2019 Section III）

Cui 2019 Section III 用 Devetak-Winter rate formula + de Finetti / postselection 论证 asymptotic security against coherent attacks。这给 path α Π 的 ε（per L2.G4 + 用户 Option B accept implicit composable bridge per §7.x.5.4 of lemma_skeletons_v0_1.md）；具体 ε 数值 **不**在本 lemma scope 内。

---

## §3 数学陈述

### §3.1 Soundness 2-additive 分解 form（Portmann-Renner Theorem 2, PDF p.17）

**High-level form**：

$$\boxed{\varepsilon_{\text{sound}} \;\leq\; \varepsilon_{\text{secret}} + \varepsilon_{\text{correct}}}$$

**精确 conditioned-on-no-abort trace-distance form**：见 Portmann-Renner 2022 Eq. (8) + Eq. (11)–(14) + footnote 22 直接（具体含 $(1 - p_\perp)$ prefactor 和 conditioned-on-no-abort 处理 per PDF p.16-17）。本 closure **不**做精确 form 重述（避免 over-paraphrase）；仅 cite high-level 2-additive structure。

### §3.2 Completeness 独立 criterion form（Portmann-Renner §III.B.4 + Lemma 3, PDF p.18）

$$\varepsilon_{\text{complete}} \;:=\; \Pr[\text{abort} \mid \text{honest execution, no Eve}]$$

**Lemma 3** 给在 matching-parameter δ assumption 下，Eq. (15) 的 distinguishing failure 由 soundness distinguishing distance bound（**非** 简单 scalar $\varepsilon_{\text{complete}} \leq \varepsilon_{\text{sound}}$；具体 form 见 Portmann-Renner Lemma 3 PDF p.18 directly）。

**关键**：$\varepsilon_{\text{complete}}$ 是**独立** criterion，**非** $\varepsilon_{\text{sound}}$ 的 additive component。两者由 Lemma 3 的 conditional/parameterized bound **关联**，但形式上是 separate ε bounds。本 closure **不**重述 Lemma 3 精确 form（避免 over-paraphrase）。

### §3.3 不做 closure

本 §3 仅给 form。具体 path α 各 component bounds（Cui 2019 + path α Lemma A/B/C 综合后）**不**在本 closure 范围。

---

## §4 待启动的 C1(a) Codex round

让 Codex 直读 [Portmann-Renner 2022 PDF](../literature/pdfs/Portmann-Renner-2022-SecurityQuantumCryptography-arXiv2102.00021.pdf) §III.B verify：

1. §III.B.3 "Correctness & secrecy" 给的 ε = ε_secret + ε_correct decomposition formula 的 verbatim 位置 + page
2. §III.B.4 "Robustness" 给的 ε_complete/robust 第三分量 + verbatim 位置
3. §3.1 boxed inequality 是 Portmann-Renner 框架的 standard formulation
4. **CRITICAL scope check**: §1.1 / §3 不 smuggle Π / Π_tr 的具体 ε numerical bound; 不主张 ε-secure conclusion
5. Lemma scope clean

**预期 verdict**：PASS（standard composable security decomposition）

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 Portmann-Renner 2022 RMP §III.B.3 + §III.B.4 三分量框架。L2.G2 closure 是 form-level decomposition，**不**给 path α 各 component numerical bound。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL on substantive form 错。原 v0.1 误把 completeness 当作 additive 第三分量；实际 Portmann-Renner formulation 是 **soundness (= ε_secret + ε_correct, additive 2-component, Theorem 2 PDF p.17) + completeness (ε_0, 独立 criterion, §III.B.4 + Lemma 3 PDF p.18)** 两 orthogonal criteria。trace-distance 用 conditioned-on-no-abort 而非 unconditioned。重写 §1.1 + §3.1/§3.2 修正 form。
- **v0.3** (2026-04-26 same-day)：Codex round 2 verdict = FAIL on (a) §3.2 Lemma 3 paraphrase 太 strong (实际是 Eq. (15) 失败 distinguishing distance bound under matching-δ，非 scalar ε_complete ≤ ε_sound); (b) §3.1 trace-distance form 缺 (1-p⊥) prefactor (per Eq. (14) + footnote 22)。修：soften §3.1/§3.2 到 high-level 2-additive structure for soundness + 独立 criterion for completeness, 不重述精确 form 避免 over-paraphrase。
- **v0.3 final** (2026-04-26 same-day)：**C1(a) Codex round 3 verdict = PASS**。全部 sub-check 通过（§1.1 (i) 高层正确 / §1.1 (ii) 高层正确 / §3.1 boxed 正确 + 推延精确 form / §3.2 不再 overstate Lemma 3 / scope clean）。**L2.G2 C1 aggregate PASS via C1(a)**。C2 / C3 待。
