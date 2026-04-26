# Path α Lemma C sub-gap L3.G2 — Closure Candidate v0.1

**Sub-gap**：L3.G2 — Key length cross-topology（Cui Eq. (3) Devetak-Winter rate ↔ Pirandola Methods ε-close-to-private-state criterion (near Eq. (35)) 的标准 bridge）

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 Portmann-Renner 2022 RMP §III + Pirandola 2019 Methods + Cui 2019 Eq. (3) **+ user Option B implicit Devetak-Winter bridge per [lemma skeletons §7.x.5.4](umr_path_alpha_lemma_skeletons_v0_1.md)**
**严谨性 banner**：[SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify ∧ C2 user signature]

---

## §-1 R0.2 升级闸门状态 + 用户 directive

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读多 PDF | ✅ **PASS** at Codex round 3 |
| **C1(c)** non-AI 数值 | 不适用 |
| **C1** aggregate | ✅ **PASS** via C1(a) (under user Option B implicit Devetak-Winter bridge) |
| **C2** 用户审签 | ⏳ 待（user Option B for point 4 已提供 partial C2 evidence；具体 lemma 表述 sign-off 仍待）|
| **C3** dev-reviewer 双 Codex 评审 | ✅ **PASS at Round 3**（R1 FAIL minor §4 stale text → v0.4 patch；R2 FAIL on cross-link target → v0.5 fix → R3 PASS）|

**Codex reviewer directive [USER-ISSUED 2026-04-26]** (per [lemma skeletons §7.x.5.4](umr_path_alpha_lemma_skeletons_v0_1.md))：

> 用户 Option B：accept "Cui 2019 用 Devetak-Winter framework 内部隐含 composable security" 作 implicit bridge。Future Codex 评审**不**应再以 "Cui 原文无 explicit composable / private-state textual support" 为由把点 4 / L3.G2 列为 issue。

**Directive 边界**（不可 user-override）：
- 若**新文档** claim Cui 已 explicit composable（而非 implicit Devetak-Winter bridge）→ 仍是 issue
- 若试图基于 implicit bridge 自行 close 其他 sub-gap → 仍是 R0.2 越权

---

## §1 Sub-gap statement

### 1.1 Lemma L3.G2 statement

**Lemma L3.G2 (Devetak-Winter rate ↔ Portmann-Renner ε-composable criterion bridge)**：

设：
- $R_{Cui}(\Pi) = Q_\mu[1 - fh(e_\mu, 1-e_\mu) - I^u_{AE}]$ 是 Cui 2019 Eq. (3) per-trial Devetak-Winter rate
- $R_{ε\text{-pri}}(\Pi)$ 是 Pirandola Methods（near Eq. (35) 的 unnumbered condition）ε-close-to-private-state criterion 下的 secret-key rate（即 Portmann-Renner 2022 framework 的 composable secret-key rate）

**Lemma**（per **user Option B implicit Devetak-Winter bridge**）：

$$R_{Cui}(\Pi) \;\sim\; R_{ε\text{-pri}}(\Pi) \quad \text{in asymptotic regime}$$

通过标准 quantum information theory bridge：Devetak-Winter rate 配合 **leftover hash lemma**（Renner 2008 thesis / Tomamichel 2016）后接 **classical post-processing**（privacy amplification）得到的 final key 满足 trace-distance ε-close-to-private-state criterion；这就是 Portmann-Renner 2022 §III "reduction to trace distance criterion" 框架的标准内容。

### 1.2 Lemma 在 path α Lemma C 中的位置

Path α Lemma C 主张 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$。要让这一比较 well-defined，需 RHS Pirandola rate 与 LHS Cui rate 用同一 underlying secret-key criterion（即 ε-close-to-private-state 或等价 composable secret-key）。L3.G2 close 的就是这一 underlying criterion bridge。

### 1.3 严格 scope

- ✅ 本 lemma 在 **user Option B (implicit Devetak-Winter bridge)** 假设下 close
- ❌ 本 lemma **不**主张 Cui 原文 textually explicit ε-composable（per §7.x.5.4 user Option B 接受 implicit bridge）
- ❌ 本 lemma **不**主张 absolute 数值 rate 相等
- ❌ 本 lemma **不**主张 Π_tr 继承 Π 的 security（依赖 L2.G3 / L1.G2）

---

## §2 引文

### 2.1 Cui Eq. (3) — Devetak-Winter per-trial rate

**Cui 2019**, Section III, PDF p.2 (per L1.G1 + L2.G4 round verifies)：

> "According to Devetak-Winter's bound [24], the secret key rate per trial in a code mode is then given by $R = Q_\mu [1 - fh(e_\mu, 1-e_\mu) - I^u_{AE}]$"

verbatim per Codex direct read confirm: brackets 包住整个 $[1 - fh - I^u_{AE}]$（v0.1 把 $I^u_{AE}$ 写在括号外是错；v0.2 已修）。

Cui Ref. [24] = Devetak-Winter 2005 "The private classical capacity and quantum capacity of a quantum channel" (Proc. R. Soc. A 461:207).

### 2.2 Portmann-Renner §III.B — composable trace-distance criterion

**Portmann-Renner 2022**, [PDF](../literature/pdfs/Portmann-Renner-2022-SecurityQuantumCryptography-arXiv2102.00021.pdf)：

- §III.B "Reduction to the trace distance criterion" PDF p.15-17 — composable security reduces to trace-distance bound
- §III.B.5 "Variations of the trace distance criterion" — covers various equivalent ε formulations including ε-close-to-private-state
- §III.B.3 "Correctness & secrecy" + Theorem 2 — soundness 2-additive decomposition (per L2.G2 already verified)

### 2.3 Pirandola — ε-close-to-private-state benchmark (Methods, near Eq. (35))

**Pirandola 2019**, [PDF](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf), Methods 部分（在 weak-converse block，**紧邻 Eq. (35) 之前**的 unnumbered condition statement，per Codex direct read）：

> $\rho^n_{ab}$ is $\varepsilon$-close to a target private state ... $\|\rho^n_{ab} - \phi^n\|_1 \leq \varepsilon$

定义 secret-key benchmark 为 trace-norm ε-closeness to a target private state。

**重要 caveat**：上述 ε-close-to-private-state criterion 是 unnumbered condition statement（**紧邻 Eq. (35) 之前**）；Eq. (35) 本身是 $E_M(\phi^n) \geq n R^\varepsilon_n$（不同的 entropy-bound formula）。本 closure 引用的是 Eq. (35) 之前的 unnumbered ε-close condition 文本，**非** Eq. (35) 公式本身。

**v0.1 / v0.2 错误修正**：v0.1 误写为 Pirandola Eq. (8)；v0.2 误写为 Eq. (35) 公式本身；**v0.3 corrected**：仅引用 Eq. (35) 紧邻前的 unnumbered ε-close-to-private-state condition 文本，不 mis-cite specific Eq. number。

### 2.4 Bridge — standard QC IT

由 §2.1 + §2.2 + §2.3 + **user Option B** (implicit Devetak-Winter bridge, [§7.x.5.4](umr_path_alpha_lemma_skeletons_v0_1.md))：

Devetak-Winter rate 是 standard quantum information theory 的 secret-key achievability rate。配合：
1. **Leftover hash lemma**（Renner 2008 PhD thesis Theorem 5.5.1 / Tomamichel 2016 *Quantum Information Processing with Finite Resources* Ch 6）—— 给具体 finite-key 上界
2. **Privacy amplification** classical post-processing ——把 raw key 转成 final key
3. **Asymptotic limit** —— 给 ε → 0 as n → ∞

得到的 final key state 满足 trace-distance ε-close-to-private-state criterion (per Pirandola Methods near-Eq.-(35) condition / Portmann-Renner §III.B trace distance)。这是 standard QC IT 已建立的 bridge。

**user Option B 的边界**：本 closure **不**主张 Cui 2019 原文显式 prove this bridge（Cui 仅 invoke Devetak-Winter rate formula via Ref. [24]）。bridge 的 explicit text 在 Renner 2008 thesis / Tomamichel 2016 / Portmann-Renner 2022 等独立文献。**user 已 explicit accept 这一 implicit bridge**（per §7.x.5.4）。

---

## §3 数学陈述

L3.G2 是 framework-level bridge lemma，无独立数学推导。closure 内容：

- §2.4 standard QC IT bridge（Devetak-Winter rate → ε-close-to-private-state via leftover hash + privacy amplification + asymptotic limit）
- 配合 user Option B implicit bridge directive
- 推 $R_{Cui}(\Pi) \sim R_{ε\text{-pri}}(\Pi)$ 在 asymptotic regime

---

## §4 已 PASS 的 C1(a) Codex round（archive）+ 待 C3 round 2

**v0.4 (2026-04-26 C3 batch round 1 patch)**：C1(a) Round 3 已 PASS at v0.3 final（per §-1 状态表）；本节作 **archive**。**C3 dev-reviewer Round 1 (2026-04-26)** 标 FAIL minor on 本节 stale text "Pirandola Methods Eq. (8) — ε-close-to-private-state form"，与 §2.3 round 2 corrected attribution "near Eq. (35) unnumbered condition" 不一致。本节 v0.4 修正以 propagate §2.3 final attribution。

C1(a) round verbatim 直读对象（v0.3 final PASS）：

1. Cui 2019 PDF Section III page 2 Eq. (3) verbatim（已在 L2.G4 round 2 verify PASS）
2. Portmann-Renner 2022 PDF §III.B PDF p.15-17 — composable framework, including trace distance reduction (§III.B.1) + correctness/secrecy (§III.B.3) + variations (§III.B.5)
3. **Pirandola 2019 PDF Methods 紧邻 Eq. (35) 之前的 unnumbered condition statement**（per §2.3 v0.3 final corrected attribution；**不**是 Eq. (8)，**不**是 Eq. (35) 本身）

**CRITICAL Codex directive reminder**（v0.3 final + C3 round 1 复述）：本 closure 假设 user Option B implicit bridge（per §7.x.5.4）。**不**应以 "Cui 原文无 explicit ε-composable" 为由 raise issue。仅 verify：
- §2 引文 verbatim accuracy（含 §2.3 attribution 准确性）
- §2.4 standard QC IT bridge logical chain reasonable（Devetak-Winter + leftover hash + privacy amplification → trace distance）
- §1.3 严格 scope: 不 smuggle path α 其他 sub-gap closure
- bridge 在 user Option B + Portmann-Renner framework 下 well-defined

**v0.3 final verdict**：PASS（standard QC IT bridge under user-accepted Option B）

**v0.4 (本次) verdict 待**：C3 dev-reviewer Round 2 重评（仅 §4 stale text patch；§1-§3 + §5 未改）

**holistic FAIL caveat (2026-04-26 C3 round 1)**：lemma_skeletons §157 原 statement target C 含 "channel use 计数对齐 + 同 ε-secure criterion"。L3.G2 closure 在 user Option B 下仅 close 后者（Devetak-Winter ↔ ε-private state bridge）；前者（per-trial vs per-chain-use channel-use accounting）**未**被本 closure 吸收，残留作 **Lemma C counting/normalization residual**（per [c3-dev-reviewer-batch-holistic-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1）。本 closure scope 须显式 disclaim：

- ❌ 本 lemma **不**主张 channel-use accounting 对齐（即 Cui per-trial 与 Pirandola per-network-use 计数对齐）
- 该 residual 已记入 [RETRACTION.md §9.4](../research/RETRACTION.md#94-holistic-fail--lemma-c-countingnormalization-residual) + [integration v0.2 §3.3](path_alpha_subgap_closure_integration_v0_2.md) 作 named residual sub-gap，且**已立项独立 sub-gap L3.G2.E**（[path_alpha_l3g2e_closure_v0_1.md](path_alpha_l3g2e_closure_v0_1.md) v0.1，2026-04-26 立项），**不**由 L3.G2 close

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 user Option B implicit Devetak-Winter bridge + Portmann-Renner 2022 §III.B + Cui Eq. (3) + Pirandola Methods Eq. (35) standard QC IT bridge。L3.G2 是 framework-level bridge lemma。C1(a) Codex round 待启动（含 user directive 提醒）。C1(c) 不适用。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL only on 2 citation 错: (a) Cui Eq. (3) verbatim 应是 R = Q_μ[1 - fh - I^u_AE]（全 in brackets），非 v0.1 误写的 outside; (b) Pirandola ε-close-to-private-state 实际是 Methods Eq. (35) 非 Eq. (8)。User directive (Option B) 维持 respected；bridge claim 本身 acceptable per Codex。仅修 §2.1 + §2.3 引文 accuracy。
- **v0.3** (2026-04-26 same-day)：Codex round 2 verdict = FAIL only on §2.3 still mis-cite —— Eq. (35) 本身是 $E_M(\phi^n) \geq nR^\varepsilon_n$（不同的 entropy-bound formula），ε-close-to-private-state criterion 实际是 Eq. (35) 紧邻**前**的 unnumbered condition statement。修：§2.3 改为引用 "near Eq. (35) 的 unnumbered condition"，**不**直接 attribute 给 Eq. (35)。Cui Eq. (3) round 2 PASS。其余维持。
- **v0.3 final** (2026-04-26 same-day)：**C1(a) Codex round 3 verdict = PASS**。Pirandola near-Eq.-(35) attribution 准确，Cui Eq. (3) verbatim 准确，§2.4 bridge 在 user Option B 下 acceptable，scope clean。**L3.G2 C1 aggregate PASS via C1(a) (under user Option B)**。C2 / C3 待。
- **v0.4** (2026-04-26 same-day, C3 batch round 1 patch)：**C3 dev-reviewer Round 1 verdict = FAIL minor only on §4 stale text**（[diff review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-diff-1.md) item 9）—— §4 仍写 "Pirandola Methods Eq. (8)"，与 §2.3 v0.3 final corrected attribution "near Eq. (35) unnumbered condition" 不一致。仅修 §4 propagate。§1-§3 + §5（除本条）未改。**Holistic FAIL** ([review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1) 揭露 Lemma C counting/normalization residual：本 closure 仅在 user Option B 下 close Devetak-Winter ↔ ε-private state bridge，**不**主张 channel-use counting 对齐；该 residual 显式 disclaim 入 §4（v0.4 末段）。**C3 Round 2 待**重评 §4 patch；记入 [RETRACTION.md §9](../research/RETRACTION.md#9-path-α-l1g4-closure-v01-撤回--l3g3-eq-11-specialization-chain-大修-2026-04-26-c3-batch)。L3.G2 主体 C1 aggregate PASS via C1(a) 维持；C2 仍待；C3 Round 2 待。
- **v0.5** (2026-04-26 same-day, C3 R2 cross-link fix)：**C3 dev-reviewer Round 2 verdict = FAIL only on cross-link target** ([R2 review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-l3g2-v0_4-r2.md) item B) —— v0.4 §4 末段写 "integration v0.2" 但 link 指向 `path_alpha_subgap_closure_integration_v0_1.md`（已撤稿）。仅修 §4 末段 cross-link 指向正确的 v0.2 文件 + 加 forward reference 到 newly opened L3.G2.E。其余维持。
- **v0.5 final** (2026-04-26 same-day)：**C3 dev-reviewer Round 3 verdict = PASS** ([R3 review](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-l3g2-v0_4-r3.md))。Cross-link 正确指向 integration v0.2 §3.3 + L3.G2.E forward reference well-formed + 无 scope drift。**L3.G2 C3 aggregate PASS at Round 3**。C1 PASS（C1(a) round 3, under user Option B）+ C3 PASS at R3 维持；**C2 user signature 仍待**。
