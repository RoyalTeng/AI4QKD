# Sub-Q3 path α (monotonicity reduction) — 三 Lemma scaffolding document

**版本**：v0.1 **[DRAFT, scaffolding only — NOT a proof]**
**日期**：2026-04-22 autonomous session
**RESEARCH_PLAN 映射**：§4.3 U3.6 上界 MS-EB 重写（path α）
**Log 07 对应**：[§4.3 路径 α (monotonicity)](../research/07_pirandola_2019_technical_audit.md)

---

## 0. 重要免责 / 严谨性声明

本文件**不是**一个 proof。本文件**仅**为 path α（monotonicity reduction + Khatri-Wilde §19-20）的三条 lemma 提供**陈述框架 + 已识别 gap 清单**。所有 lemma 陈述均 **[DRAFT 级 stub]**，**没有**任何代数/功能级的 certification。

**本文件禁止**：
- 作为 C1 independent validation 输入（它是 AI 起草 scaffolding）
- 作为 umr 上界升级基础（无 [COROLLARY] 升级路径）
- 对外引用（内部 scaffolding only）

**本文件用途**：
- 给用户 future formalization 提供 **starting material**
- 显式列 **each lemma 的精确 statement target + 已识别 gap**
- 保护项目避免重蹈 path γ v0.2 overclaim 陷阱（通过**不**给 proof，只给 statement）

**触发背景**：
- Log 07 §4.3 明示 path α 需要三条 lemma 明写
- path γ v0.2 (adversarial containment shortcut) 已 retract (2026-04-21)
- 用户 2026-04-21 delegation 授权 autonomous 推进；但 C1(b) 形式化工作**必须**由用户纸笔完成

---

## 1. Context 与 Log 07 映射

### 1.1 Log 07 path α 原文陈述

从 [Log 07 §4.3](../research/07_pirandola_2019_technical_audit.md)：

> "路径 α 的三条 lemma（协议嵌入、安全归约、rate 定义对接）每条看似 trivial，但没写出来就是 informal 漏洞。"

Log 07 明确 path α 的三 lemma 是：
- **L1 协议嵌入**（protocol embedding）
- **L2 安全归约**（security reduction）
- **L3 rate 定义对接**（rate definition alignment）

### 1.2 目标 claim (要 prove 的)

**目标**：$\forall \Pi \in \mathcal{T}_\text{umr}$ (untrusted measurement relay 拓扑的 QKD 协议)：

$$R_\varepsilon(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B))$$

用 monotonicity reduction 从 **Khatri-Wilde 2020 Prop 19.2 / Cor 19.3** + PLOB 2017 直接应用于 trust topology，然后继承到 umr。

### 1.3 为什么 path α 比 path γ 安全

- path γ 需要建立 PLOB 单边 + data-processing lemma 明写（Log 07 §4.5）
- path α 直接 invoke **Khatri-Wilde 教科书** monotonicity framework — 更接近**标准已 published tool**
- path α 的三 lemma 更 surface-level；path γ 的 data-processing step 更subtle

---

## 2. Lemma L1：Protocol Embedding

### 2.1 Statement target (**[DRAFT stub]**)

**Target**：设 $\Pi \in \mathcal{T}_\text{umr}$ 是 any umr protocol。存在一个**协议嵌入** $\iota: \Pi \hookrightarrow \Pi^\text{trust}$ 把 $\Pi$ 在 umr Eve model $\mathcal{A}_\text{umr}$ 下的 execution 嵌入到 trusted relay Eve model $\mathcal{A}_\text{tr}$ 下**同一协议 operations** 的 execution，且满足：
- **L1.a Purification preservation**: $\iota$ 在 Eve workspace 上是 Stinespring isometry（不给 umr Eve 额外 workspace purification）
- **L1.b Output equivalence**: $\iota(\Pi)$ 在 $\mathcal{A}_\text{tr}$ 下输出的 Alice-Bob state 与 $\Pi$ 在 $\mathcal{A}_\text{umr}$ 下 isomorphic

### 2.2 已识别 gap / 未证项

- **Gap L1.G1**: 什么是"$\mathcal{A}_\text{umr}$" 和"$\mathcal{A}_\text{tr}$" 的精确数学定义？Log 07 §II-C 指出 Pirandola 2019 §II-C 定义 Eve system $E$ **只**包含 channel environment purification，**不**含 Charlie 量子 register；umr 中 Charlie 量子 register **在** $E$ 里 — 两个 Eve 在不同 Hilbert 空间。**L1 必须显式 handle 这个空间差**，不能 assume isomorphism
- **Gap L1.G2**: "embedding $\iota$" 的具体构造：是 tensor with dummy workspace? Symmetric unification? **未 specified** — 需用户纸笔 specify
- **Gap L1.G3**: Stinespring isometry 是否 unique up to isometric gauge? 如果有 gauge freedom，安全性 bound 依赖于 gauge — 需 prove gauge-invariance 或 tight over gauge
- **Gap L1.G4**: Output state "isomorphic" 的精确 metric (trace distance / diamond distance / partial-transpose bound?)

**严谨性**：L1 **[DRAFT statement stub]**, **no proof**。2/4 gaps 可能需要 substantive framework (spaces / gauges / metric choices)。

---

## 3. Lemma L2：Security Reduction

### 3.1 Statement target (**[DRAFT stub]**)

**Target**：In L1 的 embedding $\iota$ 下，$\varepsilon$-composable security 的 property 被 preserve：
- **L2.a** ：$R_\varepsilon^{\mathcal{A}_\text{tr}}(\iota(\Pi)) \geq R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi)$（同 ε 下，trust 版本 $\iota(\Pi)$ 的 rate **≥** umr 原版 rate — 即 umr 是 "worse" rate upper bound)
- **L2.b** ：Eve 能力关系：$\mathcal{A}_\text{umr} \supseteq \iota(\mathcal{A}_\text{tr})$ (umr Eve 至少与 trusted Eve 一样强 modulo embedding)

### 3.2 已识别 gap / 未证项

- **Gap L2.G1**: L2.a 的 sign / direction — 应该是 umr rate ≤ trust rate? 还是反向? Careful check required. **v1 FINDINGS** 犯过类似错: 把 min 方向写反 (trusted-relay Pirandola Eq.11 应用到 umr 要求 umr 更 restrictive，给**更低 rate**)
- **Gap L2.G2**: $\varepsilon$-composable security 精确定义 (Portmann-Renner 2022)：$\varepsilon$ 是 secret + correct + complete 三条件合成。L2 需 handle 三个 epsilons 分别 transfer
- **Gap L2.G3**: L2.b 的 $\supseteq$ 在不同 Hilbert 空间**未 well-defined** without specifying a mapping —— 与 Gap L1.G1 同类陷阱 (path γ v0.2 在此犯过)
- **Gap L2.G4**: 非 LOCC 层面 — 如果 umr Eve 能 generate **非 LOCC** 联合 attack，L2.b 的 naive inclusion 不成立

**严谨性**：L2 **[DRAFT stub]**, **no proof**。L2.G3 是 v0.2 retraction 原因；必须小心不重犯。

---

## 4. Lemma L3：Rate Definition Alignment

### 4.1 Statement target (**[DRAFT stub]**)

**Target**：$R_\varepsilon^{\mathcal{A}_\text{tr}}$ 与 $R_\varepsilon^{\mathcal{A}_\text{umr}}$ 在**同一协议 operations + 同一 security definition** 下 operationally 相同：
- **L3.a** ：定义层面：两 rate 函数用**同一** LOPC scheme + **同一** key length formula + **同一** ε-security condition
- **L3.b** ：operational equivalence：在 trust 和 umr 下，能 extract 的 key length 函数于 protocol 的 operations 是**同一个 function** ($R_\varepsilon$ 不是 topology-dependent syntax sugar)

### 4.2 已识别 gap / 未证项

- **Gap L3.G1**: "same LOPC scheme" — LOPC (Local Operations + Public Communication) 在 trust 下 Charlie 是合作方；在 umr 下 Charlie 是 Eve 的部分。LOPC **syntax 在两个 trust model 下不同** —— L3 必须 reconcile
- **Gap L3.G2**: Key length formula ($\ell$ vs composable security $\varepsilon$)：Portmann-Renner 2022 的 $\ell$ definition 是 topology-neutral，但 **verifier** 在 umr 下需要 additional ε 来 account for Charlie's untrustedness — **未** certify equivalence
- **Gap L3.G3**: 如果 L3 成立，则 L1+L2+L3 的 chain 给 $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\mathcal{A}_\text{tr}}(\iota(\Pi)) \leq -\log_2(1-\min(\eta_A, \eta_B))$；**最后一步** inherits Pirandola 2019 Eq.11 — 但 Pirandola Eq.11 在 $\iota(\Pi)$ 的 topology 下是否 apply 还需 check (trusted relay scenario require Charlie cooperative)

**严谨性**：L3 **[DRAFT stub]**, **no proof**。L3.G3 explicit 暴露 path α 的 "继承 PLOB" 步本身 inherits trust assumption — 这是 subtle。

---

## 5. 综合 gap table

| Lemma | Gap ID | 描述 | 升级所需 |
|---|---|---|---|
| L1 | L1.G1 | $\mathcal{A}_\text{umr}$ / $\mathcal{A}_\text{tr}$ 定义 + Hilbert 空间 alignment | 用户 formal specification |
| L1 | L1.G2 | embedding $\iota$ 具体构造 | 用户纸笔构造 |
| L1 | L1.G3 | Stinespring gauge invariance | 技术 proof 或 tightness argument |
| L1 | L1.G4 | Output state equivalence metric | 选择 & 证明合适 distance measure |
| L2 | L2.G1 | 方向 (umr ≤ trust rate) sign check | 小心算 — v1 犯过反 |
| L2 | L2.G2 | Composable ε 三分量 transfer | Portmann-Renner 2022 适配 |
| L2 | L2.G3 | Eve 能力包含 $\mathcal{A}_\text{umr} \supseteq \mathcal{A}_\text{tr}$ **across spaces** | v0.2 retraction 陷阱；必须**避免 naive set-inclusion** |
| L2 | L2.G4 | Non-LOCC 联合 attack 处理 | Portmann-Renner semidefinite framework |
| L3 | L3.G1 | LOPC syntax 在 trust vs umr 下 reconcile | 形式化 operation model |
| L3 | L3.G2 | Key length formula + ε 跨 topology equivalence | Portmann-Renner 2022 详细 |
| L3 | L3.G3 | 最后一步 inherits Pirandola 2019 Eq.11 在 $\iota(\Pi)$ 下的适用 | Check trust assumption 不 breach |

**Total: 11 identified gaps**, all [UNKNOWN] 级。

---

## 6. 与 path γ v0.2 retraction 的 diff

v0.2 用 adversarial containment shortcut 声称 $\mathcal{A}_\text{tr} \subseteq \mathcal{A}_\text{umr}$ without explicit embedding —— 这**等效于**跳过 L1+L2+L3 的三 lemma 全部。Claude audit + Codex audit 双 reviewer 各自 UNSOUND 因为 "两 Eve 集合不在同 Hilbert 空间"（i.e., L1.G1 + L2.G3 违反）。

**v0.3 path γ 若要重启**，必须解决上述 L1.G1 + L2.G3 问题。path α 也面临同类问题 — 所以以上 gap list 同样是 path γ 真版 的**必要** gap。

---

## 7. User action items（若用户选择 path α formalization）

1. **Spec L1 空间 / embedding 构造**：~ 1-2 天
2. **Derive L2 sign + composable ε transfer**：~ 2-3 天
3. **Reconcile L3 LOPC syntax**：~ 2-3 天
4. **全链 integration + 双 reviewer audit** → C1 ∧ C2 ∧ C3：~ 1 周

**Total user 工作量 estimate**: **~ 10-15 人日 全心投入**

---

## 8. 严谨性总结

- 本文件为 **scaffolding**，非 **proof**
- 所有 11 gaps 为 **[UNKNOWN]** 级
- **不**改 FINDINGS v2 / Log 07 / upper bound 状态
- 用户**不应**视此文件为 "部分证明"；它是**未证 statements + gap 清单**
- **不**可作为 C1 验证输入 (AI scaffolding + AI gap identification 仍属 same-family AI)
- 用户 formalization 满足 C1(b) 但仍需 **C2 + C3**

---

## Changelog

- **v0.1** (2026-04-22 autonomous session)：首稿 scaffolding。11 gaps 显式列出。本文件 **[DRAFT]** 级，non-proof，not upgradable to higher rigor without user C1 ∧ C2 ∧ C3。
