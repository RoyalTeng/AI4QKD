# Path α Lemma A sub-gap L1.G4 — Closure Candidate v0.1 [RETRACTED 2026-04-26 — C3 REJECTED]

> **🛑 [RETRACTED 2026-04-26 — C3 dev-reviewer Round 1 REJECTED]**
>
> 本 closure candidate 被 **C3 dev-reviewer 双 Codex 评审 Round 1 (2026-04-26)** diff/scope reviewer **REJECTED**（critical scope drift / adjacent-gap smuggling）。
>
> **REJECTED 依据**（per [c3-dev-reviewer-batch-diff-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-diff-1.md) item 4）：
>
> - §1.2 derivation 同时使用了 (i) `ρ^{Π_tr}_{ABE'} = Tr_C(ρ^{Π}_{ABCE})` 身份（前提是 L2.G3 的 trusted-relay Eve 仅控 H_E）+ (ii) `if Π is ε-secure ... then Π_tr is ε-secure` 结论（前提是 L1.G2 的 ι embedding 合法性）
> - §1.3 同时声明 `❌ 不主张 Π → Π_tr 嵌入 ι 的合法性（依赖 L1.G2）` + `❌ 不主张 trusted-relay Eve 仅控 H_E 不触 H_C 的协议设定（依赖 L1.G1）`
> - **scope contradiction**：§1.2 derivation 实际依赖 §1.3 explicit 排除的 assumption；属于 adjacent-gap smuggling（§3.3 trap 模式：closure 文档不得在 derivation 中暗用未 close 的相邻 sub-gap 结论）
>
> **CLAUDE.md §3.3 hardline**：`REJECTED / UNSOUND：立即撤回，不 defend，不 patch 到上游`。本文件按此规则撤回。
>
> **保留 v0.1 原文**作 cautionary record（per CLAUDE.md §1.2 "撤回必须留痕：不删除原稿文本"）。
>
> **撤回引用**：见 [docs/research/RETRACTION.md](../research/RETRACTION.md) 2026-04-26 C3 batch 条目。
>
> **后续 path**：L1.G4 trace-distance contraction lemma **本身**（§1.1 + §3 数学推导 + §3.4 数值 PASS）**仍然有效**作 standalone partial-trace contraction 引用（KW Theorem 6.3）。但 **§1.2 path α 应用层**（"if Π ε-secure then Π_tr ε-secure"）**不**作为 L1.G4 的 closure 内容；它是 Lemma A 整体（L1.G2 + L2.G3 + L1.G4 jointly）的 conclusion，**不**单独由 L1.G4 close。任何后续 v0.2 须将 §1.2 application 内容**移除**或**重写为 Lemma A integration 的 contributing step**，并经新一轮 C1(a) + C3 评审。
>
> **此撤回不影响**：L1.G1 / L1.G2 / L1.G3 / L2.G1 / L2.G2 / L2.G4 / L3.G1 / L3.G2 的 C1(a) PASS 状态。
>
> ---

**Sub-gap**：L1.G4 — Output state equivalence metric (trace distance / fidelity criterion) for ι-image of umr protocol Π under embedding to trusted-relay Π_tr

**版本**：v0.1 **[RETRACTED]**
**日期**：2026-04-26
**C1 path used**：**C1(c)** non-AI 数值工具（numpy + scipy.linalg）+ C1(a) Codex 引文核对（待启动）
**严谨性 banner**：~~[SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify ∧ C2 user signature]~~ → **[RETRACTED — C3 REJECTED 2026-04-26]**

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(c)** non-AI 数值验证 | ✅ **PASS**（§3，300 trials, 0 violations）|
| **C1(a)** 跨家族 AI 直读 PDF 引文核对 | ✅ **PASS** at Codex round 4（§4，4 轮 citation iterative fix 后）|
| **C1** aggregate（OR over (a)/(b)/(c)）| ✅ **PASS** via C1(a) + C1(c) 双路径 |
| **C2** 用户对本 closure 表述逐项签字 | ⏳ 待 user 审签 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 round（与后续 sub-gap 一起 batch）|

**关键边界**：
- 本文档**仅** close L1.G4
- L1.G1 / L1.G2 / L1.G3 / L2.G1-G4 / L3.G1-G3 维持 [UNKNOWN]
- 升级 [SYN] → [COROLLARY] 仍需 C1 ∧ C2 ∧ C3（C1 至少一条 sub-path PASS；C1(c) 已满足，但 C2 + C3 仍未）

---

## §1 Sub-gap statement (precise)

### 1.1 Lemma L1.G4 statement

**Lemma (L1.G4 — trace distance contraction under partial trace over Charlie's internal Hilbert space)**：

设：
- $\mathcal{H} = \mathcal{H}_A \otimes \mathcal{H}_B \otimes \mathcal{H}_C \otimes \mathcal{H}_E$ where $\mathcal{H}_A, \mathcal{H}_B$ are Alice / Bob systems, $\mathcal{H}_C$ is Charlie's internal Hilbert space (umr Eve controlled), $\mathcal{H}_E$ is umr Eve's environment ancilla
- $\rho, \sigma \in \mathcal{D}(\mathcal{H})$ 是任意密度算子（$\mathcal{D}$ 表示密度算子集合）

**则**：

$$\| \mathrm{Tr}_C(\rho) - \mathrm{Tr}_C(\sigma) \|_1 \;\leq\; \| \rho - \sigma \|_1$$

其中 $\| \cdot \|_1$ 是 Schatten-1 范数（trace norm，迹范数 = 算子奇异值之和）。

### 1.2 Lemma 在 path α Lemma A 中的位置

在 path α Lemma A（协议嵌入）下，umr Eve 在 Π 协议下的 view 是 $\rho^{\Pi}_{ABCE} \in \mathcal{D}(\mathcal{H}_{ABCE})$；trusted-relay Eve 在 ι(Π) = Π_tr 协议下的 view 是 $\rho^{\Pi_{tr}}_{ABE'} \in \mathcal{D}(\mathcal{H}_{ABE'})$，其中 $\mathcal{H}_{E'} = \mathcal{H}_E$（即 trusted-relay Eve 仅控 ancilla，不触 Charlie 内部）。

**关键身份**：

$$\rho^{\Pi_{tr}}_{ABE'} \;=\; \mathrm{Tr}_C(\rho^{\Pi}_{ABCE})$$

将 L1.G4 lemma 应用到 security distance：设 $\sigma^{\text{ideal}}_{AB}$ 是理想目标态（idealized correct + secret Alice-Bob 关键比特态），$\tau_E, \tau_{CE}$ 是 Eve ancilla 的扩展态（满足 $\tau_E = \mathrm{Tr}_C(\tau_{CE})$ 的 consistency）。则：

$$\underbrace{\| \rho^{\Pi_{tr}}_{ABE'} - \sigma^{\text{ideal}}_{AB} \otimes \tau_E \|_1}_{\text{Π_tr security distance}} \;=\; \| \mathrm{Tr}_C(\rho^{\Pi}_{ABCE}) - \mathrm{Tr}_C(\sigma^{\text{ideal}}_{AB} \otimes \tau_{CE}) \|_1 \;\stackrel{\text{L1.G4}}{\leq}\; \underbrace{\| \rho^{\Pi}_{ABCE} - \sigma^{\text{ideal}}_{AB} \otimes \tau_{CE} \|_1}_{\text{Π security distance}}$$

**含义**：if Π is ε-secure（即 umr setting 下 security distance ≤ ε），then Π_tr = ι(Π) is also ε-secure（即 trusted-relay setting 下 security distance ≤ ε）—— ε**不**变大。这就是 L1.G4 在 Lemma A 中的 closure 内容。

### 1.3 严格 scope 声明

- ✅ 本 lemma 是 about: trace distance 在 partial trace 下的 contraction
- ❌ 本 lemma **不**主张 σ_target 的具体形式（依赖 L2.G2 ε-composable 三分量）
- ❌ 本 lemma **不**主张 Π → Π_tr 嵌入 ι 的合法性（依赖 L1.G2）
- ❌ 本 lemma **不**主张 trusted-relay Eve 仅控 H_E 不触 H_C 的协议设定（依赖 L1.G1）

---

## §2 引文（Citation accuracy 核对，pending C1(a) Codex round）

### 2.1 主 citation（v0.2 corrected per [Codex C1(a) round 1 finding](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l1g4-citation-verify.md)）

**Khatri-Wilde 2024**, *Principles of Quantum Communication Theory: A Modern Approach*（arXiv:2011.04672, [PDF](../literature/pdfs/Khatri-Wilde-2024-PrinciplesQuantumCommTheory-arXiv2011.04672.pdf)）：

#### 2.1.a Trace-distance DPI — **Theorem 6.3** (Chapter 6, "Distinguishibility Measures for Quantum States and Channels" — *sic*, KW PDF chapter-title typo) at PDF p.278 / printed p.265

verbatim per Codex direct read：

> "let $\mathcal{N}$ be a positive, trace-non-increasing map" ... (Eq. 6.1.9): $\|\rho - \sigma\|_1 \geq \|\mathcal{N}(\rho) - \mathcal{N}(\sigma)\|_1$

#### 2.1.b Partial trace is CPTP — **§4.4.2 "Trace and Partial-Trace Channels"** (Chapter 4, "Quantum Channels") at PDF p.171 / printed p.158

verbatim per Codex direct read：

> "$\mathrm{Tr}_B$ is completely positive."

Eq. (4.4.7) of KW proves trace-preservation immediately after.

#### 2.1.c L1.G4 即 Theorem 6.3 取 $\mathcal{N} = \mathrm{Tr}_C$ + §4.4.2 partial trace CPTP 的 immediate corollary

**v0.1 → v0.2 fix**：v0.1 误把 trace-distance DPI 引到 Chapter 9（Ch 9 实际是 Entanglement Measures，仅在 PDF p.543 / printed p.530 backward-cite Thm 6.3）。Codex C1(a) round 1 标 FAIL on citation accuracy，但 math claim + lemma scope 均 PASS。本节已 corrected。

### 2.2 辅 citation

**Nielsen-Chuang**, *Quantum Computation and Quantum Information* (Cambridge, 2010), Theorem 9.2 ("Contractivity of the trace distance under trace-preserving quantum operations")

> "For any trace-preserving quantum operation $\mathcal{E}$ and density operators $\rho, \sigma$: $D(\mathcal{E}(\rho), \mathcal{E}(\sigma)) \leq D(\rho, \sigma)$ where $D(\rho, \sigma) = \frac{1}{2} \|\rho - \sigma\|_1$"

**partial trace = CPTP**：standard result（KW Ch 4 / Nielsen-Chuang §8.2）。

### 2.3 Pirandola 2019 Eq. 36 旁证

**Pirandola 2019**, *Nat Commun* 10:1006，Eq. 36：

依 [PDF synthesis v0.1 update 1](umr_path_alpha_pdf_synthesis_v0_1.md)，该等式涉及 partial trace 在 secret-key capacity 上下界中的 contraction structure。**待 Codex 直读 verify**。

---

## §3 数值验证（C1(c) primary）

### 3.1 实施

脚本：[scripts/path_alpha_l1g4_trace_distance_contraction.py](../../scripts/path_alpha_l1g4_trace_distance_contraction.py)

方法：
1. 在 6 组 $(d_A, d_C, d_E)$ 维度组合 $\{(2,2,2), (2,3,2), (3,2,3), (2,4,2), (4,2,4), (3,3,3)\}$ 上各跑 50 trials
2. 每个 trial：生成两个独立 Haar-random 全秩混合密度算子 $\rho, \sigma \in \mathcal{D}(\mathcal{H}_{ACE})$（用 $G G^\dagger / \mathrm{Tr}(G G^\dagger)$，$G$ 为复正态矩阵）
3. 计算 $\|\rho - \sigma\|_1$（trace norm via $\sum |\lambda_i|$ for Hermitian $\rho - \sigma$）
4. 计算 $\rho_{AE} = \mathrm{Tr}_C(\rho)$, $\sigma_{AE} = \mathrm{Tr}_C(\sigma)$（partial trace via 直接 tensor reshape + 求和）
5. 计算 $\|\rho_{AE} - \sigma_{AE}\|_1$
6. 验证 margin = $\|\rho - \sigma\|_1 - \|\rho_{AE} - \sigma_{AE}\|_1 \geq -10^{-10}$（数值 floor）

### 3.2 结果

| 指标 | 值 |
|---|---|
| 总 trial 数 | 300 |
| violations（margin < $-10^{-10}$）| **0** |
| min margin | $3.196689 \times 10^{-1}$ |
| mean margin | $6.635284 \times 10^{-1}$ |
| max observed $\|\rho - \sigma\|_1$ | 1.306 |
| RNG seed | 20260426（reproducible）|
| **PASS** | **✅ True** |

数据：
- [docs/research/data/path_alpha_l1g4_trace_distance_contraction.json](../research/data/path_alpha_l1g4_trace_distance_contraction.json)
- [docs/research/data/path_alpha_l1g4_trace_distance_contraction.csv](../research/data/path_alpha_l1g4_trace_distance_contraction.csv)

### 3.3 数值验证的 strict scope

**这是什么**：300 个 random density operator pair 上 trace distance 在 partial trace 下 contraction 的 empirical 验证。

**这不是什么**：
- ❌ 不是 C1(b) 形式化推导（user 纸笔）
- ❌ 不是 Coq/Lean 形式化证明
- ❌ 不是 ALL density operators 的覆盖证明（"无 counterexample in 300 random samples" 不蕴含 "无 counterexample in 全集"）

**为什么 300 trials 充分**：trace distance contraction 的标准证明（Nielsen-Chuang Thm 9.2）走 quasi-classical decomposition 即可，不依赖 random sample 完备性。**数值验证的角色是 sanity check / regression** —— 若 random sample 中出现 violation 即明示有 implementation 错（partial trace 写错 / trace norm 写错），300/300 PASS = 实施代码本身正确，配合 Nielsen-Chuang 的 textbook proof 即可建立 C1(c) PASS。

---

## §4 C1(a) Codex round 1 + round 2

### §4.1 Round 1 (v0.1) — verdict: FAIL on citation accuracy

**Output**：[c1a-l1g4-citation-verify.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l1g4-citation-verify.md)

| Sub-check | Verdict | Note |
|---|---|---|
| Trace-distance DPI in KW **Ch 9** | **FAIL** | Ch 9 实际是 Entanglement Measures，仅 backward-cite；正确位置是 **Ch 6 Theorem 6.3** |
| Partial trace is CPTP in KW Ch 4 | **PASS** | §4.4.2, PDF p.171 / printed p.158 |
| Combination → L1.G4 | **PASS** | math 正确，仅 citation 错 |
| Lemma scope（不 smuggle 其他 sub-gap）| **PASS** | Codex 确认严格在 trace-distance contraction 范围内 |

**Aggregate verdict round 1**：FAIL（citation accuracy）

### §4.2 v0.2 fix — citation 已 corrected per round 1 finding

§2.1 已重写为 Chapter 6 Theorem 6.3 + Chapter 4 §4.4.2。

### §4.3 Round 2 (v0.2) — pending

**预期 verdict**：PASS（math 已 PASS round 1，仅修 citation accuracy）。**待 Codex round 2 confirm**。

---

## §5 与 path α v0.3 的关系

- v0.3 [USER-APPROVED PRIORITY direction] 维持 active；本 closure 是 v0.3 的细化
- L1.G4 closure **不**蕴含 path α v0.3 整体升级 —— 仍需其余 10 sub-gap closure + C2 user signature + C3 dev-reviewer PASS
- 升级 [SYN candidate-for-COROLLARY] → [COROLLARY] 等到 11 sub-gap 全部 closure + R0.2 三闸门同时通过

---

## §6 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。C1(c) 数值验证 PASS（300 trials）；C1(a) Codex citation round 待启动；C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：C1(a) Codex round 1 verdict = FAIL on citation accuracy（KW Ch 9 → Ch 6）；math + lemma scope 均 PASS。citation 修正为 Theorem 6.3 (Ch 6) + §4.4.2 (Ch 4) per Codex 直读 KW PDF 的 verbatim quote。Round 2 待提交 confirm。
- **v0.3** (2026-04-26 same-day)：C1(a) Codex round 2 verdict = FAIL only because §2.1.a 错填 Ch 6 title 为 "Quantum Information Measures"（实际为 "Distinguishability Measures for Quantum States and Channels"）；math + lemma scope + Thm 6.3 location + §4.4.2 全 PASS。仅修 chapter title。Round 3 待提交 confirm。
- **v0.4** (2026-04-26 same-day)：Codex round 3 verdict = FAIL because KW PDF chapter-title 本身有 typo "Distinguishibility"（缺 a，sic in book）— Codex 要求 verbatim match including typos。citation 改为 "Distinguishibility Measures..." (sic noted)。其余 4 项（theorem 位置、§4.4.2、corollary、scope）round 3 均 PASS。Round 4 待 final confirm。
- **v0.4 final** (2026-04-26 same-day)：**C1(a) Codex round 4 verdict = PASS**。Chapter 6 title verbatim match confirmed (PDF p.275 / printed p.262)，Theorem 6.3 confirmed (PDF p.278)，§4.4.2 partial trace CPTP confirmed (PDF p.171)，corollary + scope clean。**L1.G4 C1 aggregate PASS via C1(a) + C1(c) 双路径**。C2 / C3 待。
