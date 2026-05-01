# Path α Lemma B sub-gap L2.G3 — Closure v0.1

**Sub-gap**：L2.G3 — Eve set across spaces（trusted-relay 安全模型中 Eve 对 Charlie 内部 Hilbert 空间 H_C 的访问权限声明）

**版本**：v0.1
**日期**：2026-05-01
**严谨性 banner**：[COROLLARY] — C1(a) ✅ (Log 07 已审计) / C2 ✅ (2026-05-01 user explicit declaration with citation) / C3 ✅

**前身**：
- [path_alpha_subgap_closure_integration_v0_3.md §3.1](path_alpha_subgap_closure_integration_v0_3.md) — OPEN per R0.1，需 user 显式声明
- [Log 07 §1.3](../research/07_pirandola_2019_technical_audit.md) — 首次识别 Pirandola §II-C 中 Eve 不包含 middle node internal registers

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|------|------|
| C1(a) | ✅ Log 07 技术审计已逐字核对 Pirandola 2019 §II-C 原文 |
| C2 | ✅ 2026-05-01 user 显式声明（见 §1.2）+ 要求出处标注 |
| C3 | ✅ 本文件 dev-reviewer 评审通过 |

---

## §1 Closure 内容

### §1.1 文献出处

Pirandola 2019（*Commun. Phys.* 2:51）安全模型中有两处关键定义，共同确立了 trusted-relay 下 Eve 的访问边界：

**出处 1 — §II-C 安全定义**（main paper）：

> Pirandola 2019 §II-C 定义 $\epsilon$-secure key：协议末态 $\rho_{aE}$ 与 ideal key $\chi_{ab} \otimes \rho_E$ 的 trace distance ≤ ε，其中 **$E$ 是 Eve 的系统，被定义为所有 channel 的 purification**（environment of the channels）。

→ Eve 的系统 $E$ **不包含** middle node 的 internal registers。安全定义的 adversary 是"controls the channels, but not the parties"。

**出处 2 — 网络 stretching 的 honest-LOCC 前提**（§IV proof, Step B）：

> 网络 stretching 将 $n$ 轮 adaptive protocol 改写为 non-adaptive protocol，其 LOCC post-processing $\Lambda$ 由**全图节点**执行。证明的关键是：stretching 后的 LOCC 结构要求**所有 middle nodes 参与 honest LOCC**。

→ 若 Charlie 是 adversarial（Eve 能控制 Charlie 的 local operation），则 $\Lambda$ 不再是 honest-LOCC，stretching 定理的结论不能直接声明。因此 Pirandola 的 REE bound（Eq. 11）的证明**内建依赖于**"Charlie 是 honest 协作者"这一前提。

**出处 3 — SI Note 1 协议类定义**（supplementary information）：

> 协议类规定每个网络节点（包括 relay）对自己的 local register 执行 adaptive local operation + 经典广播，节点之间是 honest LOCC 合作关系。"Adaptive LOs performed by all points of the network on their local registers, which are assisted by unlimited two-way CC involving the entire network."

→ 经典广播（two-way CC）Eve 可听，但 Charlie 对自己 local register 执行的 LOs 是 honest 的，不是 Eve 选的。

**引用汇总**：
- Pirandola 2019, *Commun. Phys.* 2:51, §II-C（Eve = channel purifications）
- Pirandola 2019, §IV Step B（network stretching + honest LOCC）
- Pirandola 2019, SI Note 1（protocol class: adaptive LOs by all nodes + CC）
- Log 07 技术审计 §1.3（[07_pirandola_2019_technical_audit.md §1.3](../research/07_pirandola_2019_technical_audit.md)）：首次识别并记录"$E$ 不包含 middle node 的 internal registers"
- Log 07 信任入口 #2（同上 §2.2）：识别 stretching 的 honest-LOCC 前提

### §1.2 User 显式声明

项目负责人确认：

> 在 path α 的目标协议 $\Pi_{tr}$（Pirandola 2019 SI Note 1 型 trusted-relay 协议）中，**沿用 Pirandola 2019 §II-C 的原始安全定义**：窃听者 Eve 的系统 $E$ 被定义为所有信道（Alice-Charlie、Charlie-Bob）的 channel purification，**不包含** Charlie 的内部 Hilbert 空间 $H_C$。Charlie 的内部操作（包括测量和本地经典处理）是 honest LOCC，Eve 不可访问 Charlie 的 quantum registers。Eve 可接触的是：信道环境（$H_E$）+ Alice-Bob-Charlie 之间的公开经典通信（包括 Charlie 的测量结果广播）。

### §1.3 Scope

- **本 sub-gap 闭合的内容**：Pirandola 2019 §II-C 安全模型中 Eve 不访问 Charlie 内部 $H_C$ 的文献出处 + user 显式声明
- **不闭合的**：从"Eve 控 $H_C$"（Cui 2019 umr）到"Eve 不控 $H_C$"（Pirandola trusted-relay）的跨模型迁移合法性的**独立证明**——这一步不是文献推导，而是 user 对协议嵌入 $\iota$ 的物理判断。本文件将其记录为 user 声明，不主张为"从文献定理机械推导"的结论
- **对 combined chain 的影响**：L2.G3 闭合消除了 Lemma B（安全归约）的 Eve-set 结构 gap。但 combined chain 仍 [SYN, conditional on post-split L3.G3 (5 sub-residuals) + Pirandola Eq. 11 specialization chain]

---

## §2 对 Lemma B 其余 sub-gap 的影响

L2.G3 闭合后，Lemma B 四个 sub-gap 全部落地：

| Sub-gap | 状态 |
|---------|------|
| L2.G1 | [COROLLARY] ✅ |
| L2.G2 | [COROLLARY] ✅ |
| L2.G3 | [COROLLARY] ✅（本文件） |
| L2.G4 | [COROLLARY] ✅ |

Lemma B 整体（Eve set 声明 + rate-direction sign + ε-composable decomposition + non-LOCC joint attack）闭合。

---

## §3 Limitations

- 本 closure 的效力限定在 path α 的 trusted-relay 协议模型内
- 若后续考虑"Eve 能部分控制 Charlie"的变体模型（semi-honest relay），Pirandola 的 REE bound 本身不直接适用，需回到 path β/γ 路线
- L2.G3 的"跨模型迁移合法性"是 user 声明而非文献定理推导；本文件如实记录，不升级为独立 [THM]

---

*L2.G3 closure v0.1 结束。2026-05-01 user C2 sign-off with explicit Pirandola §II-C citation.*
