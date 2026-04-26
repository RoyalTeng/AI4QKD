# Path α PDF Synthesis (v0.1 — Claude PDF direct read scaffolding)

**版本**：v0.1 [SCAFFOLDING — Claude single-AI direct PDF read, NOT C1-compliant]
**日期**：2026-04-25
**用途**：基于 Claude 直接读 PDF（不是 training-data recollection）的逐 gap 证据汇总，作为后续 C1 验证（user 直读 / 跨家族 AI / 形式化工具）的**基础材料**。
**严谨性**：
- ✅ 内容**全部**有 PDF 页码引用，**不是**记忆复述
- ❌ Claude single-AI 直读 ≠ C1 (a)（需跨家族 AI + 双方直读 PDF）
- ❌ 任何 sub-gap 仍 **[UNKNOWN]**，本文件不 close
- ❌ 任何 [SYN] → [COROLLARY] 升级仍需 R0.2 三闸门

---

## §-1 R0.1 / R0.2 状态

本文件是 path α v0.3 [USER-APPROVED PRIORITY] 下的**辅助 scaffolding**：
- 不修改 [path α v0.3](umr_path_alpha_three_lemma_v0_3.md) 11 sub-gap 状态（全部 [UNKNOWN] 维持）
- 不构成 C1 验证（Claude single-AI 直读不满足 R0.2 (a) 的"跨家族 AI 双方直读"要求）
- 仅作 user 后续 paper-level work 的**预 organize**：节省 user 重复定位章节的时间

---

## §1 已读 PDF 进度

| PDF | 页数 | 已读 | 剩余 | 主要发现 |
|---|---|---|---|---|
| Pirandola 2019 | 36 | **全部 1-36** ✅ | — | **untrusted nodes claim 仅在 Discussion p.7 + SI Note 6 p.35 出现，无独立 formal proof**；SI Notes 1-5 全部基于 "all-points cooperate LOCC" |
| Khatri-Wilde 2020 Ch. 19 | 11 (content p.1150-1162) | ✅ | — | 点对点 LOCC-assisted 框架基础（Def 19.1, Thm 19.4 squashed E, Thm 19.8 max-Rains, Def 19.11 Q^↔），**不涉及网络** |
| Khatri-Wilde 2020 Ch. 20 | (~30 估计) | 0 | 全部 | 待读 — SKA-specific 内容，最关键 |
| Lucamarini 2018 | ? | 0 | 全部 | 待读 — Eve 模型 |
| Wang 2018 (SNS-TF) | ? | 0 | 全部 | 待读 |
| Curras-Lorenzo 2021 | ? | 0 | 全部 | 待 PDF 补 |
| Portmann-Renner 2022 | ? | 0 | 全部 | 待 PDF 补 |

---

## §2 Pirandola 2019 直读笔记（pages 1-8，Claude 直读）

### 2.1 论文整体结构（page 1 abstract + intro）

**核心声明**（直接 quote）：
> "we derive single-letter upper bounds for the end-to-end capacities achievable by the most general (adaptive) protocols of quantum and private communication, from a single repeater chain to an arbitrarily-complex quantum network"

**关键短语解读**：
- "**most general (adaptive) protocols**" — 协议类是 adaptive LOCC 之间所有 nodes
- "**from a single repeater chain to an arbitrarily-complex quantum network**" — 覆盖 chain + general network
- "**end-to-end**" — 端到端 secret key capacity，不是 relay-shared

### 2.2 Repeater chain framework（page 2-3）

**协议定义**（**直接 quote, page 2**）：
> "the most general quantum distribution protocol P_chain involves transmissions which are interleaved by adaptive LOCCs among all parties, i.e., LOs assisted by two-way CCs among end-points and repeaters. In other words, before and after each transmission between two nodes, there is a session of LOCCs where all the nodes update and optimize their registers."

**关键事实**：
- 协议类**包含 repeater nodes 的 LOCC 操作**
- 是 **adaptive** LOCC（多轮交互式）
- "all the nodes" 包括 Alice + Bob + repeater(s)

**这对 L1.G2（embedding 构造）的影响**：
- Pirandola 的 protocol class 已经允许 repeater 节点做 adaptive LOCC
- 所以 path α Lemma A "umr 协议嵌入到 trusted-relay 协议类" 在原则上有空间
- **但**：是否覆盖 Charlie 的 measurement-and-broadcast 仍需核 supplementary notes

### 2.3 Capacity 上界（page 2-3）

**Eq. (4)（直接 quote, page 2）**：
$$C(\{E_i\}) \leq \min_i E_R(\sigma_i)$$

**Eq. (7) 适用 distillable channels（page 3）**：
$$C(\{E_i\}) = \min_i C(E_i) = \min_i E_R(\sigma_{E_i})$$

**这对 L3.G3 的影响**：
- Eq. (7) 的形式与 path α 目标 chain 公式一致
- 但 Pirandola 的 capacity C 是端到端 K_AB（per definition page 2: "end-points share an output state ρ^n_ab with nR_n target bits"）
- **L3.G3.a closeable evidence**: K(a,b) **是** Alice-Bob 端到端 secret key, **不是** relay-shared

### 2.4 Network framework（page 3-4）

**直接 quote (page 3)**:
> "A quantum communication network can be represented by an undirected finite graph N = (P, E)"

**直接 quote (page 4)**:
> "In particular, a chain of quantum repeaters can be treated as a single-route quantum network."

**这对 L1.G1（Hilbert 空间 alignment）的影响**：
- Pirandola network framework 是 graph-based
- 每个 edge 是一个 channel E_xy
- 每个 node 有 quantum register
- **未明确**：node 是 trusted 还是 untrusted（待 supplementary 核）

### 2.5 ⚠️ KEY FINDING — page 7 Discussion 关于 untrusted nodes

**直接 quote (page 7)**:
> "These upper bounds are very general and **also apply to chains and networks with untrusted nodes (i.e., run by an eavesdropper).** Our theory is formulated in a general information-theoretic fashion which also applies to other entanglement measures, as discussed in our Methods section. The upper bounds are particularly important because they set the tightest upper limits on the performance of quantum repeaters in various network configurations. **For instance, our benchmarks may be used to evaluate performances in relay-aided QKD protocols such as MDI-QKD and variants** [56-58]."

**这对**所有 path α gap 的影响**重大**：
- Pirandola **自己**声称定理覆盖 "untrusted nodes (run by an eavesdropper)"
- 自己**显式提**relay-aided QKD（MDI-QKD 及变体）作为应用
- 如果这是真的，path α Lemma A 不是新构造，而是 Pirandola 已经覆盖
- L1.G1 / L1.G2 / L3.G3 可能比 v0.1 scaffolding 估计**显著更接近闭合**

**重要保留**：
- 这是 Discussion 一句话，**不是**形式化证明
- "untrusted nodes" 的精确定义没在 main text 给出 → 必须查 Supplementary Notes
- 是否 == 项目定义的 umr (Charlie 完全被 Eve 控)？ 还是某种受限 untrusted？ → 待核
- 引用文献 [56-58] 是关于 "MDI-QKD and variants"，可能给出受限场景

### 2.6 Methods — General weak converse upper bound (page 7-8)

**直接 quote (page 8)**:
> "Consider an arbitrary end-to-end (n, R^ε_n, ε) network protocol P (single- or multi-path). This outputs a shared state ρ^n_ab for Alice and Bob after n uses, which is ε-close to a target private state φ^n having nR^ε_n secret bits, i.e., in trace norm we have ||ρ^n_ab − φ^n||_1 ≤ ε."

**关键事实**：
- (n, R^ε_n, ε) 协议定义是 **abstract** — 没限定 trusted/untrusted node
- ε-close to target private state 是**输出 condition** — 不限制 protocol internal structure
- ρ^n_ab 是 **Alice-Bob shared state** — 不要求 relay 也持 key share

**这对 L3.G2（key length formula 跨 topology）的影响**：
- 协议成功标准是 ε-close to private state
- 这是 topology-neutral 的 success criterion
- **L3.G2 closeable evidence**: Pirandola 的 success criterion 与 standard QKD 一致（per Portmann-Renner ε-secure 定义）

**Eq. (37) Data Processing Inequality**:
$$E_M(\bar{\Lambda}(\rho)) \leq E_M(\rho)$$

**直接 quote**:
> "Assume also that E_M is monotonic under trace-preserving LOCCs Λ̄"

**这对 γ.B.G1 / L2.G2 的影响**：
- DPI 在 Pirandola 框架是**直接定义在 trace-preserving LOCC 上**
- 不需要"channel cooperative"假设
- L2.G2 ε-composable transfer 在 Pirandola DPI 下可能直接成立

### 2.7 Eq. (41) 总 SKC 公式（page 8）

**直接 quote**:
$$E^*_M(N) := \sup_{\mathcal{P}} \lim_n \frac{E_M(\rho^n_{ab})}{n}$$

> "In particular, this is an upper bound to the single-path SKC K if P are single-path protocols, and to the multi-path SKC K^m if P are multi-path (flooding) protocols."

**关键**：
- sup is over ALL protocols P
- K 定义为 SKC = secret-key capacity
- 这是 **Alice-Bob 端到端**

---

## §3 11 Sub-gap 现状更新（基于 Pirandola pp. 1-8 直读）

| Gap | v0.1 status | Pirandola pp.1-8 evidence | 更新评估 |
|---|---|---|---|
| **L1.G1** Hilbert space alignment | [UNKNOWN] | Discussion p.7 声称 untrusted nodes 适用；Methods p.8 protocol 定义是 abstract | **可能比 v0.1 更近闭合**，但需读 supplementary notes 确认 |
| **L1.G2** embedding construction | [UNKNOWN] | Page 2 protocol class 含 "adaptive LOCCs among all parties" — 包括 repeater | **构造基础存在**，仍需 spec specific embedding |
| **L1.G3** Stinespring gauge invariance | [UNKNOWN] | 未在 pp.1-8 出现 | 待读 supplementary |
| **L1.G4** Output state metric | [UNKNOWN] | Eq.(36) continuity in trace norm; Eq.(37) DPI; Eq.(38) subadditivity | **L1.G4 closeable evidence**: Pirandola 用 trace norm + DPI + subadditivity，与 standard QKD ε-close 一致 |
| **L2.G1** sign direction | [UNKNOWN] | Eq.(4)/(7) 上界形式 K ≤ E_R | **L2.G1 直接对照 evidence**: Pirandola formal 是 ≤ direction，与 path α 一致 |
| **L2.G2** ε-composable 三分量 transfer | [UNKNOWN] | Eq.(36)-(38) 给 ε-perturbation continuity + DPI + subadditivity | **L2.G2 部分支持 evidence**: 三个 standard property 都在 Pirandola 框架内 |
| **L2.G3** Eve set across spaces | [UNKNOWN] | Discussion p.7 "untrusted nodes (run by an eavesdropper)" 显式包含 | **关键 evidence**: 待 supplementary notes 确认精确 Eve 模型 |
| **L2.G4** Non-LOCC joint attack | [UNKNOWN] | Eq.(37) DPI is over **trace-preserving LOCCs** Λ̄ | **L2.G4 待评估**: Pirandola 假设是 LOCC + adaptive，非 LOCC attack 是否覆盖待核 |
| **L3.G1** LOPC syntax 跨 topology | [UNKNOWN] | "adaptive LOCCs among all parties" 是 Pirandola 协议类的 syntax | **L3.G1 evidence**: Pirandola 的 LOCC 定义跨 topology 一致 |
| **L3.G2** Key length formula 跨 topology | [UNKNOWN] | Methods page 8: ε-close to private state φ^n with nR^ε_n bits | **L3.G2 closeable evidence**: success criterion 是 topology-neutral standard QKD |
| **L3.G3** Pirandola Eq.11 适用 in ι(Π) | [UNKNOWN] | Discussion p.7 显式声称 chain/network with untrusted nodes 适用 | **关键 evidence**: 与 L1.G1/L2.G3 同源，待 supplementary |

---

## §4 关键不确定性与下一步

### 4.1 最大未知

**Discussion p.7 的 "untrusted nodes (run by an eavesdropper)" 精确含义是什么？**

可能解释：
- (a) **完全 adversarial Eve** 控制 node — 等同 path α / project 的 umr 定义 → 那 path α 多个 gap 直接 closeable
- (b) **受限 untrusted** — 例如 "node 是 black-box 但执行 protocol-defined operations" → 与 MDI-QKD 安全证明假设一致，path α 部分 close
- (c) **Eve 仅通过 channel 攻击 untrusted node** — node 内部执行 protocol-spec，Eve 只 see broadcast → 最弱形式 untrust，与 trusted-relay 接近

**待 Supplementary Notes 确认**。

### 4.2 下一步读什么

**优先级**：
1. **Pirandola 2019 pages 9-36** — supplementary notes 会精确定义 "untrusted nodes" + 给完整证明
2. **Khatri-Wilde §19-20** — 比较 KW 的 LOPC 定义 + composable security framework
3. **Lucamarini 2018 / Wang 2018 SNS-TF / TF-QKD spec** — 比较 TF 协议的 Charlie 角色与 Pirandola "adaptive LOCC at repeater" 定义
4. **Portmann-Renner 2022** — composable ε-secure 框架 + 跨 topology key length 公式

### 4.3 R0.2 boundary 维持

无论后续 PDF 阅读发现什么：
- Claude single-AI 直读 PDF **不**构成 C1 (a) — 仍需跨家族 AI 双方直读 OR user 纸笔 OR 非 AI 工具
- 任何 [SYN] → [COROLLARY] 升级仍需 R0.2 三闸门
- 本文件 v0.1 仅作 user 后续工作的 pre-organize scaffolding

---

## §6 Pirandola 2019 全部 36 页读完后的最终评估（v0.1 update 2026-04-25）

### 6.1 全 paper 已读 ：page 1-36

**已 Claude 直读全文**包括：
- Main text (pp. 1-12)
- References (pp. 12-14)
- SI Note 1: Chains (pp. 15-19)
- SI Note 2: Networks (pp. 20-23)
- SI Note 3: Simulation/stretching (pp. 24-26)
- SI Note 4: Single-path (pp. 26-30)
- SI Note 5: Multi-path (pp. 31-34)
- SI Note 6: Related literature (pp. 34-35)
- SI References (pp. 35-36)

### 6.2 关于 untrusted nodes 的最终诊断

**论文内出现 "untrusted nodes" 共 1 次**（Discussion, page 7）：
> "These upper bounds are very general and also apply to chains and networks with untrusted nodes (i.e., run by an eavesdropper)."

**论文内 SI Note 6 提及 TF-QKD / PM-QKD 共 1 次**（page 35）：
> "Finally, the limits established by this work for the optimal performance of quantum repeaters have been already considered in works of quantum key distribution (QKD), including the relay-assisted protocols of twin-field QKD [S34] and Phase-Matching QKD [S35]."

**论文内 untrusted-node case 的独立 theorem / lemma / formal proof**：**0** 处。

**所有 SI Notes 1-5 formal proofs 的 LOCC 假设**：
> "adaptive LOs performed by all points of the network on their local registers, which are assisted by unlimited two-way CC involving the entire network" (page 21)

—— 这是 "network LOCC with all-points cooperation"，**不**是 umr。

### 6.3 用户 Log 07 audit 的 PDF 直读 confirm

**项目 Log 07 ([07_pirandola_2019_technical_audit.md](../research/07_pirandola_2019_technical_audit.md)) 钉出的 2 个 trust entries**：
- trust entry #1（β.G5 amortization）
- trust entry #2（β.G4 / γ.B.G1 / L2.G3 / L3.G3 same family — relay node honest LOCC）

**Claude PDF 直读全 36 页结果**：**完全 confirm** Log 07 audit。Pirandola 2019：
- 公开 claim 适用 untrusted nodes
- 公开 claim 适用 TF-QKD / PM-QKD
- **但**没有 paper 内的 formal proof 支持上述 claims
- 这正是 trust entry #2 的内容

### 6.4 11 sub-gap 的 Pirandola 2019 直读综合评估

| Gap | Status | Pirandola evidence | 闭合需求 |
|---|---|---|---|
| L1.G1 Hilbert space alignment | ❌ **NOT closed by Pirandola** | 全 paper formal proof 假设 all-cooperate LOCC | 需 Khatri-Wilde §19-20 或新工作 |
| L1.G2 embedding ι construction | 🟡 framework 基础存在 | Eq. (97), (134) trace-preserving LOCC Λ̄ | 需具体 specify embedding |
| L1.G3 Stinespring gauge invariance | ❌ Pirandola 未讨论 | — | 需独立 argument |
| L1.G4 output state metric | ✅ **基础支持** | Eq. (36) trace norm + (37) DPI + (38) subadditivity | 与 standard QKD 一致 |
| L2.G1 sign direction | ✅ **基础支持** | Eq. (4), (102), (152), (187) 全部 ≤ | path α 方向正确 |
| L2.G2 composable ε 三分量 | 🟡 部分支持 | Eq. (36) continuity property | 需 Portmann-Renner 2022 详细 |
| **L2.G3 Eve set across spaces** | ❌ **关键 NOT closed** | Discussion 一句话, no formal proof | **需 KW §19-20 或新工作** |
| L2.G4 non-LOCC attack | ❌ Pirandola 假设 LOCC | Eqs. 37, 95, 134 | 需独立处理 |
| L3.G1 LOPC syntax cross-topology | ❌ NOT closed | Pirandola 单一 trusted framework | 需新 reconciliation |
| L3.G2 key length cross-topology | 🟡 部分支持 | Eq. (8) ε-close to private state topology-neutral | 需 Portmann-Renner 详细 |
| **L3.G3 Pirandola Eq.11 in ι(Π)** | ❌ **关键 NOT closed** | Discussion claim only | **需 KW §19-20 或新工作** |

**核心结论**：Pirandola 2019 框架支持 path α 的 4 个 gap (L1.G2 / L1.G4 / L2.G1 / L2.G2 partial / L3.G2 partial)，**不**支持 4 个关键 gap (L1.G1 / L2.G3 / L3.G1 / L3.G3) — 这 4 个**必须**靠 Khatri-Wilde §19-20 或外部新工作完成。

### 6.5 下一步

**关键 PDF**：Khatri-Wilde 2020 §19-20。如果 KW §19 提供：
- (a) 多 trust-model LOPC 的形式化 reconcile → 关闭 L3.G1
- (b) Eve set 跨 Hilbert 空间 alignment → 关闭 L1.G1 / L2.G3
- (c) Pirandola Eq.11 在 untrusted relay 下的扩展 → 关闭 L3.G3

那 path α 4 个剩余 gap 也可能通过文献闭合。**否则**，path α 至少需要新研究贡献（不是文献查证）。

**严谨性维持**：
- 本节增补**仅**基于 Claude 直读 PDF 整理，**不构成 C1 (a)**（仍需跨家族 AI 双方直读 + user 纸笔验证）
- 11 gap 状态全部**维持 [UNKNOWN]**
- 本评估为后续 user / 跨家族 AI / proof assistant 验证提供**预 organize**

---

## §6.6 Khatri-Wilde 2020 Chapter 19 直读笔记（content p.1150-1162）

### 6.6.1 Chapter 19 范围

**Chapter 19: LOCC-Assisted Quantum Communication** —— **点对点**（point-to-point）框架，**不**包含网络 / 中继。

§19 子节：
- §19.1 协议定义 + 上界框架 (Def 19.1, Thm 19.4)
- §19.2 PPT-Assisted (Def 19.5, Thm 19.8 max-Rains)
- §19.3 Capacities (Def 19.11 Q^↔, Thm 19.15 squashed E weak converse, Thm 19.16 max-Rains strong converse)
- §19.4 Examples [IN PROGRESS — KW 草稿]
- §19.5 Bibliographic Notes

### 6.6.2 关键引用（直接 quote PDF）

**Definition 19.1 (n,M,ε) LOCC-Assisted Quantum Communication Protocol**（content p.1151）：
> "Let C := (ρ^(1)_{A'_1A_1B'_1}, {L^(i)_{A'_{i-1}B_{i-1}B'_{i-1}→A'_iA_iB'_i}}^n_{i=2}, L^(n+1)_{A'_nB_nB'_n→M_AM_B}) be the elements of an n-round LOCC-assisted quantum communication protocol over the channel N_{A→B}."

**协议结构**：Alice 与 Bob 之间，n 次使用 channel N_{A→B}，**前后**插入 LOCC channels。**没有第三方节点**。

**Theorem 19.4 n-Shot Squashed Entanglement Upper Bound**（content p.1153）：
> "log_2 M ≤ 1/(1−√ε) [n · E_sq(N) + g_2(√ε)]."

**Theorem 19.8 n-Shot Max-Rains Upper Bound**（content p.1156）：
> "log_2 M ≤ n · R_max(N) + log_2(1/(1−ε))."

### 6.6.3 对 path α 11 sub-gap 的影响

| Gap | KW Ch 19 evidence |
|---|---|
| L1.G1 Hilbert space alignment | ❌ Ch 19 是点对点，不涉及多 node Hilbert 空间 |
| L1.G2 embedding ι construction | ❌ 同上 |
| L1.G3 Stinespring gauge invariance | ❌ Ch 19 不涉及 |
| L1.G4 output state metric | ✅ **支持**：Eq.(19.1.16) `q_err = 1 − F(ω, Φ)` 给 standard fidelity criterion |
| L2.G1 sign direction | ✅ **支持**：所有 Theorem 19.4-19.17 都是 ≤ direction |
| L2.G2 ε-composable 三分量 | 🟡 部分：Theorem 19.4 给 ε-perturbation，但只 single ε，不分三分量 |
| L2.G3 Eve set across spaces | ❌ Ch 19 是点对点，**未**处理多 node Eve |
| L2.G4 non-LOCC attack | ❌ Ch 19 仅 LOCC + PPT，未处理非 LOCC |
| L3.G1 LOPC syntax | 🟡 部分：Def 19.1 定义 LOCC 标准 syntax，可作 baseline 但未 reconcile umr |
| L3.G2 key length cross-topology | 🟡 部分：q_err 是 standard QKD criterion |
| L3.G3 Pirandola Eq.11 适用 | ❌ Ch 19 不涉及 chain/network |

**核心结论**：KW Chapter 19 给 path α 提供**点对点框架基础**（Def 19.1 LOCC syntax, Thm 19.4/19.8 上界 monotonicity, fidelity criterion），但**不**直接闭合任何网络层 sub-gap。L1.G1 / L2.G3 / L3.G3 仍**不**能仅凭 Ch 19 闭合 —— 需要 Ch 20 (SKA + networks) 或更晚章节。

### 6.6.4 下一步必读

**优先级**：
1. **KW Chapter 20**（SKA 协议）—— 待读，**关键**（应包含 SKA ↔ LOPC 等价定理 + private state 框架 + 可能的网络扩展）
2. **KW Chapter 21+**（如有 networks chapter）—— 待查
3. **Lucamarini 2018**：TF 协议 Eve 模型精确定义（L2.G3 验证 case (a)/(b)）
4. **Portmann-Renner 2022**：composable ε 三分量 transfer（L2.G2, L3.G2）

### 6.6.5 严谨性维持

- 本节增补**仅**基于 Claude 直读 PDF，**不构成 C1 (a)**
- 11 gap 状态全部**维持 [UNKNOWN]**

---

## §7 Changelog

- **v0.1** (2026-04-25): 首版。Pirandola 2019 pages 1-8 Claude 直读笔记 + 11 gap 现状初步更新。Discussion p.7 "untrusted nodes 适用" 标为关键发现，待 supplementary 核实。
- **v0.1 update** (2026-04-25 same session): 全 36 页读完。**核心结论**：Pirandola 2019 无独立 untrusted-node theorem，所有 SI Notes formal proofs 假设 all-cooperate LOCC。Log 07 audit 由 PDF 直读完全 confirm。L1.G1 / L2.G3 / L3.G1 / L3.G3 **不**能仅凭 Pirandola 2019 闭合，需 KW §19-20 或新工作。

- **v0.1 update 2** (2026-04-25 same session, 新发现): Lucamarini 2018 全 7 页 + KW Ch 19 + KW Ch 20 + Wang 2018 SNS 全 13 页 + Ma 2018 前 8 页直读完。
  - **关键澄清**：path α 三 lemma 框架 target inequality 用的是 **Pirandola 2019 trusted-relay capacity bound（已严格证）**，**不是** Pirandola 自己 untrusted-node claim。前面用大量篇幅找"Pirandola 怎么处理 untrusted nodes"是**对 path α 偏题**——path α 不需要那个。
  - **核心 case (a)/(b) 答案**：
    - ❌ Lucamarini 2018 原版 TF：**case (b)** —— 安全证明不完整。Wang 2018 page 12 给出**具体反例攻击**，证明原协议在某种 Eve 下 actual secure key rate 是 0
    - ✅ Wang 2018 SNS-TF：**case (a)** —— 完整定理级安全证明，**显式假设 "Charlie is possibly dishonest"**（page 2）+ Eve 利用 post-announced 信息的最一般策略（page 5 Theorem）
    - ✅ Ma 2018 PM-QKD：**case (a)** —— 完整安全证明（Lo-Chau 框架），明说 "untrusted relay held by Eve"
  - **Path α viability**：使用 SNS-TF 或 PM-QKD 作 Π，**case (a) 成立**。Path α 给出 [SYN] 级 conditional 上界 $K_{SNS-TF}^{Wang-Eve} \leq -\log_2(1-\sqrt{\eta_{AB}})$ 是 publishable 结论。
  - **Lemma A 真实难度**：基于 Pirandola SI Note 1 trusted-relay 协议类（"adaptive LOs by all points + unlimited two-way CC"）—— Charlie 的 measurement-and-broadcast 是该协议类的特例。**Lemma A 是 observation + 仔细形式化，不是 new theorem**。
  - **修正版工作量**：~1 周 user paper-level work + 数天 AI 协助（Lemma A/B/C 形式化 + dev-reviewer + paper draft）。
  - **撤回前面 v0.1 update 关于"L1.G1 / L2.G3 / L3.G3 需 NEW theoretical work"的过度悲观判断**：那是把 path α 跟 path β/γ 视角搅混的产物。Path α 的核心 gap 已通过文献阅读基本闭合。

- **v0.1 update 3** (2026-04-25 same session, **Cui 2019 直读**): Cui-Yin-Wang-Chen-Wang-Guo-Han 2019 "Twin-Field QKD without Phase Postselection" (Phys. Rev. Applied 11, 034053) 全 9 页直读完。
  - **anchor protocol 升级**：Cui 2019 是 path α **最理想 anchor**（比 Wang 2018 SNS 更显式）。
    - Page 2 Step 2.a 明说："**untrusted measurement device controlled by Eve**"
    - Eq. (1) 形式化 Eve attack: $\hat{U}|n\rangle_{A-out}|m\rangle_{B-out}|E_0\rangle_{Ea}|0\rangle_M = \sqrt{Y_{n,m}}|\gamma_{n,m}\rangle_E|1\rangle_M + \sqrt{1-Y_{n,m}}|other\rangle_E|0\rangle_M$
    - Page 2 明说："the most general collective attack"
    - Page 3：collective → coherent attack 通过 Caves-Fuchs-Schack de Finetti [25] + Christandl-König-Renner postselection [26] reduction，asymptotic 安全
  - **L1.G1 Hilbert 空间对齐有现成模板**：Cui Eq. (1) 给的整体 Hilbert space = Alice ⊗ Bob ⊗ Eve_ancilla ⊗ Message register，**path α Lemma A 直接 build on top**
  - **附加文献指针**（**未直读，非 C1**）：
    - **[18] Tamaki-Lo-Wang-Lucamarini 2018** (arXiv:1805.05511) — TFQKD 安全证明重做版
    - **[29] Curras-Azuma-Lo 2018** (arXiv:1807.07667) — "Simple security proof of twin-field type QKD" + **基于 entanglement distillation**（与 KW Ch 20 §20.2 直接对接）
    - **[30] Lin-Lütkenhaus 2018** — Simple security analysis of PMQKD-MDI
  - **Cui 2019 第三个独立确认 Lucamarini 2018 不严格**（page 1 引 [18]）—— 加上 Wang 2018 反例 + Tamaki 等 2018 重证，**Lucamarini 原版不要作 anchor 已是文献共识**
  - **path α anchor 选择最终建议**：**Cui 2019 主推**（umr Eve 模型最清晰），Wang 2018 SNS 备选
  - **修正版工作量**：3-4 天 user 工作 + 数天 AI 协助（基于 Cui Eq. (1) 框架直接形式化）

- **v0.1 update 4** (2026-04-25 autonomous Phase 1): LCQ 2012 (Lo-Curty-Qi MDI-QKD) 全 7 页直读完。
  - **关键 quote (page 1)**："Both Alice and Bob prepare phase randomized weak coherent pulses... and send them to **an untrusted relay Charlie (or Eve)** located in the middle"
  - **关键 quote (page 2 Note 14)**："Charles' detection system can be **arbitrarily flawed** without compromising security"
  - **安全证明结构 (page 4 Appendix A)**：virtual qubit reduction → 等价 entanglement-based BB84 protocol → Lo-Chau [2] / Shor-Preskill [3] 标准证明适用。这**与 KW Ch 20 §20.2 SKA ↔ private-state distillation purification trick 完全对接**。
  - **path α 影响**：
    - ✅ 确认 Cui 2019 引 [6,7] = Braunstein-Pirandola 2012 + LCQ 2012 是 MDI Eve 模型源头
    - ✅ "Charles arbitrarily flawed" 比 Wang 2018 "possibly dishonest" + Cui 2019 "controlled by Eve" 更**强**的措辞 —— path α 想 bound 的 umr Eve 完全 cover
    - ✅ Virtual qubit reduction 与 KW §20.2 framework **同构**（path α Lemma B 形式化的 mathematical anchor）
    - ✅ MDI Eve 模型从 2012 已稳定 ~12 年，TF 派生协议（Wang 2018 / Cui 2019 / Ma 2018）均 inherit
  - **autonomous boundary 维持**：本文档**未** close 任何 sub-gap；LCQ 2012 直读仅作 cross-validation 证据。Cui 2019 anchor + path α 三 lemma 状态不变。

- **v0.1 update 5** (2026-04-25 autonomous Phase 1 ctd): PLOB 2017 (Pirandola-Laurenza-Ottaviani-Banchi) 主文 page 1-12 直读完。
  - **Eq. (19) page 7**: $\mathcal{C}_{loss}(\eta) = D_2(\eta) = Q_2(\eta) = K(\eta) = -\log_2(1-\eta)$（point-to-point 损耗信道全 capacity 一致）
  - **Theorem 1 (general weak converse, page 3)**: $\mathcal{C}(\mathcal{E}) \leq E_R^\star(\mathcal{E}) := \sup_\mathcal{L} \lim_n n^{-1} E_R(\rho^n_{ab})$
  - **Theorem 5 (one-shot REE bound, page 6)**: For Choi-stretchable, $\mathcal{C}(\mathcal{E}) \leq E_R^\infty(\rho_\mathcal{E}) \leq E_R(\rho_\mathcal{E}) = E_R(\mathcal{E})$
  - **Proposition 6 (page 8, qubit channels)**: $K(\mathcal{E}) \leq E_R^\infty(\rho_\mathcal{E}) \leq E_R(\rho_\mathcal{E}) = E_R(\mathcal{E})$
  - **PLOB 协议类**：page 2 "most general quantum protocol assisted by adaptive LOCCs" — 与 Pirandola 2019 SI Note 1 协议类**完全一致**
  - **Page 11 Discussion**: 显式提网络扩展由 [65] (Pirandola 2019) 完成
  - **path α 影响**：
    - ✅ PLOB 是**严格 point-to-point**（Alice ↔ Bob 直连，无 relay）—— path α 不直接用 PLOB，用 Pirandola 2019 N=1 chain（两段 PLOB 拼接）
    - ✅ PLOB Eve 模型 = adaptive LOCCs + unlimited two-way CC = **trusted-relay 边界（点对点没 untrusted 概念）** —— 这就是 path α Lemma A 想 embed 进去的协议类
    - ✅ Eq. (19) confirms：path α target inequality $-\log_2(1-\sqrt{\eta_{AB}})$ 在 Pirandola 2019 SI Note 1 page 18 Eq. (108) 由 PLOB Eq. (19) 与 Pirandola N=1 chain capacity 推出
    - ✅ PLOB 数学工具（teleportation stretching + REE monotonicity + Choi-stretchable）**与 Pirandola 2019 + KW Ch 19/20 完全 align**
  - **autonomous boundary 维持**：本 update 仅 cross-validate，**未** close 任何 sub-gap。

- **v0.1 update 6** (2026-04-25 autonomous Phase 1 ctd): TGW 2014 (Takeoka-Guha-Wilde) 全 13 页（含 SI Notes 1-3）直读完。
  - **Page 1 Eve 模型**："Eve is assumed to be 'all-powerful': one who has **access to the full environment** of the Alice-to-Bob quantum channel, the 'maximal' quantum system to which she can have access" + 可存量子态 + 任意 collective 测量
  - **Eq. (1) page 2**: $P_2(\mathcal{N}_\eta) \leq \log_2((1+\eta)/(1-\eta))$（pure-loss bosonic, squashed entanglement UB）
  - **Theorem 1 page 3**: $P_2(\mathcal{N}) \leq E_{sq}(\mathcal{N})$（squashed entanglement is UB on private capacity, single-letter）
  - **Lemma 2 page 3 + SI Note 1**: subadditivity inequality for squashed entanglement → 单 letter化关键 step
  - **Discussion page 6**: $\sim \eta$ scaling at high loss（linear，与 PLOB 同 scaling）；"essentially no scaling gap" between BB84/CV-GG02 and this UB
  - **path α 影响**：
    - ✅ TGW 是 PLOB 前作（2014 vs 2017），**严格 point-to-point**，**linear ~η scaling**（不是 √η）
    - ✅ TGW Eve 模型 = "all-powerful environment access" → 与 PLOB / Pirandola "adaptive LOCC + 2-way CC" 一致
    - ✅ KW Theorem 19.4 (n-Shot Squashed Entanglement UB) + Theorem 19.15 (Squashed-E weak converse) 都是 TGW 框架的教科书化
    - ✅ 提供 path α 的**备选 upper bound 工具**：squashed-E（虽然在 distillable channels 下 PLOB E_R 更紧，per PLOB Fig. 7）
    - ❌ TGW 没给 untrusted-relay extension（同 PLOB，需走 Pirandola 2019）
  - **autonomous boundary 维持**：本 update 仅 cross-validate alternative UB tool；不改 path α anchor protocol（仍 Cui 2019）+ target inequality（仍 Pirandola 2019 Eq. 11）+ 11 sub-gap 状态。

- **v0.1 update 7** (2026-04-26 autonomous Phase 1 close): WTB 2017 (Wilde-Tomamichel-Berta) **per user 决定 skip**（53 页太长，path α 主要 references PLOB + Pirandola，已充分；WTB 主要服务 path β.G5 amortization 工作，不在 path α critical 路径）。
  - KW Ch 21+ 探索结果：**KW 2020 教科书止于 Ch 20**（Secret Key Agreement）。**没有网络 / 多节点章节**。
    - 这本身是 path α 文献定位的关键 finding：**KW 教科书框架是 strict point-to-point**
    - Path α 网络扩展（Cui 2019 / TF-QKD 三节点）**必须**通过 Pirandola 2019 SI Note 1 提供
    - **没有教科书级别现成的多节点 SKA framework** → path α Lemma A 的 protocol embedding 由 Pirandola SI Note 1 + KW Ch 20 SKA 联合定义，**确实需要 user paper-level work formalize**（不是单纯文献查证）

- **Phase 1 总结**（autonomous 2026-04-25 ~ 2026-04-26 完成）：
  - ✅ 已读：Pirandola 2019 (36p) + KW Ch 19/20 (28p) + Lucamarini 2018 (7p) + Wang 2018 SNS (13p) + Ma 2018 (8p) + Cui 2019 (9p) + LCQ 2012 (7p) + PLOB 2017 main (12p) + TGW 2014 (13p)
  - ⏭️ Skip: WTB 2017（user 决定）
  - ❌ Not in repo: Curras-Azuma-Lo 2018, Tamaki-Lo-Wang-Lucamarini 2018, Portmann-Renner 2022
  - **核心结论 (Phase 1)**：
    - Path α anchor protocol = **Cui 2019** (umr Eve 模型最显式 + 完整安全证明)
    - Path α target inequality = **Pirandola 2019 SI Note 1 N=1 chain** $-\log_2(1-\sqrt{\eta_{AB}})$（PLOB Eq. (19) 基础上的网络扩展）
    - Path α Lemma A/B/C 数学语言 = **Pirandola SI Note 1 + KW Ch 20 + LCQ 2012 virtual qubit + Cui Eq. (1)** 联合提供
    - 11 sub-gap **全部维持 [UNKNOWN]**
    - 整体 cross-validation **未发现 path α 同型 retraction trap**
    - 整体 cross-validation **未发现 path α 应被撤回的硬证据**
