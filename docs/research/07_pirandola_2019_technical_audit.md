# Log 07:Pirandola 2019 技术精读 + 信任节点在 proof 中出现位置的逐步核查

**日期**:2026-04-19
**作者**:项目负责人(用户),基于自己对 Pirandola 2019 §II + §IV 的直接精读
**归档**:Claude(只读归档,未做 AI 二次加工)
**定位**:**Sub-Q3 Phase 2 实质性精读**(非 AI literature synthesis)。直接诊断 FINDINGS v1 "直接套用 Eq. 11" 的失效位置,并提出三条修复路径 α/β/γ。
**状态**:**当前权威**。本文件的技术诊断取代 Log 03/Log 04 中由 AI 合成的"Pirandola 2019 适用性"论述。

> **⚠️ 给未来 reviewer**:本文件中的定理号(Theorem 3 / 5 等)仍有 [RECALLED] 标记,需要在正式论文引用时核对原文编号。但本文件的**证明流程诊断**(Step A-E)是结构性的,不依赖具体编号。

---

## 一、§II 的**定义层审计**

### 1.1 Network 的对象定义

Pirandola 2019 §II-A 定义的 quantum communication network 是一个多重图 $\mathcal{N} = (P, E)$,其中 $P$ 是点集(每个点是一方 quantum party),$E$ 是边集(每条边 $(i,j)$ 承载一个 quantum channel $\mathcal{E}_{ij}$)。两个 end-user 是 Alice ($a$) 和 Bob ($b$),其余节点称为 **relay nodes** 或 **middle nodes**。

这里有一个**定义上的、容易被忽略的"前提条件"**:每个节点被建模为**一方(party)**,即具备做任意 local quantum operation + LOCC 的能力。这不是"trust"的同义词,但是"trust"的**必要前置**。

### 1.2 Protocol class:LOCC-assisted adaptive network protocols

§II-B(**这个小节是关键**,请核查原文)定义了 $\Pi$ 为:所有节点之间 LOCC-assisted 的自适应协议。具体允许:

(a) 任意 LO(local quantum operations)由**每个节点**执行,包括 middle nodes。
(b) 任意 classical communication 在所有节点之间进行(**全图广播能力**,不限于与端用户)。
(c) 可使用私有随机性、量子存储(这里 Pirandola 允许 unlimited quantum memory,这是网络 capacity 的定义层面,与 AI4QKD PROSPECTUS 的"no quantum memory"约束不同)。

**[RECALLED]** 这里已经出现第一处"信任假设"的痕迹:条件 (a) 让 middle node $c$ 对自己手上的 quantum register **做任意 quantum operation**,包括 ancilla、测量、Pauli 校正、unitary、甚至 quantum error correction。**这不是一个 adversarial Eve 会拥有的行为集合在某个方向上的约束** —— 恰恰相反,是合作方能力。

### 1.3 Secret-key 的定义:$\epsilon$-close to ideal,against whom?

Pirandola 2019 §II-C(**强烈建议复核**)定义 $\epsilon$-secure key:协议末态 $\rho_{aE}$ 与 ideal key $\chi_{ab} \otimes \rho_E$ 的 trace distance ≤ ε,其中 **$E$ 是 Eve 的系统,被定义为所有 channel 的 purification**(environment of the channels)。

注意 $E$ **不包含 middle node 的 internal registers**。也就是说,安全定义的 adversary 是 "controls the channels, but not the parties"。这正是"trusted network"的核心:relay node 的 quantum register 对 Eve 不可达。

→ 这是 FINDINGS v1 撤回的真正源头。PROSPECTUS §1 的 $\mathcal{T}_{\text{umr}}$ 要求的 adversary 是 "Eve 可控制 Charlie",直接违反 Pirandola 2019 §II-C 的安全模型。**§II 的适用性差异在此,不是 §IV 的公式里**。

---

## 二、§IV Eq. 11 单路径 min-cut 公式

### 2.1 定理陈述

**[RECALLED]** §IV Theorem 3(编号可能是 Theorem 5 或 2,核查原文),单路径端到端 capacity 的 converse bound:

$$\mathcal{K}(a, b) \leq \min_{C \in \mathcal{C}(a,b)} \sum_{(i,j) \in C} E_R(\mathcal{E}_{ij}) \quad \text{(Eq. 11 或附近)}$$

其中 $\mathcal{C}(a,b)$ 是所有将 $a, b$ 分离的 cut 的集合,$E_R(\mathcal{E})$ 是 channel 的 relative entropy of entanglement(the REE channel capacity,以 Choi state $\rho_{\mathcal{E}}$ 的 $E_R$ 取 regularized sup)。

### 2.2 proof 的五步骨架(逐步标注信任入口)

**Step A:Channel simulation via LOCC + resource state**

每个 channel $\mathcal{E}_{ij}$ 被 Stinespring-扩展为 $U_{ij}: A \to B \otimes E$,其 output purification 包含 Eve 的环境。对 teleportation-covariant channel(包括 pure-loss bosonic),可以进一步改写为 LOCC simulation:

$$\mathcal{E}_{ij}(\rho) = \mathcal{T}_{ij}(\rho \otimes \sigma_{ij})$$

其中 $\sigma_{ij}$ 是 resource state(Choi state),$\mathcal{T}_{ij}$ 是 **endpoint $i, j$ 之间的 LOCC**。

> **信任入口 #1**:$\mathcal{T}_{ij}$ 要求 endpoint $i$ 和 $j$ 都能做 local operation + two-way CC。如果 $j$ 是 untrusted relay,$j$ 的"local operation"可能由 Eve 选择 —— $\mathcal{T}_{ij}$ 不再是合法的 LOCC simulation(because Eve's operations are not the simulator's to choose)。

**Step B:Protocol stretching across the network**

**[RECALLED / Lemma 2 或 Theorem 1,核查原文]**:$n$ 轮 adaptive network protocol $\Pi_n$ 被 "stretch" 为一个 non-adaptive protocol,其输入为 $\bigotimes_{(i,j) \in E} \sigma_{ij}^{\otimes n_{ij}}$(所有 channel 的 resource states 总共 $\sum n_{ij} = n$ 份),其 LOCC post-processing 由一个**全图 LOCC** 实现。

> **信任入口 #2**(严重):这个"全图 LOCC"要求**所有 middle nodes 参与 honest LOCC**。证明的关键是:stretching 后的 LOCC 结构 $\Lambda$ 作用在 $\bigotimes \sigma_{ij}^{\otimes n_{ij}}$ 上产生协议末态。若某个 middle node(Charlie)是 adversarial,那么 Charlie 在 stretching 中贡献的 "local operation" 由 Eve 选取,$\Lambda$ 不再是 honest-LOCC,**stretching 定理的结论不能直接声明**。

**Step C:Cut-based state partition**

对任意 cut $C$ 分离 $a$ 在 $A_C$,$b$ 在 $B_C$。把 stretching 后的资源状态按 cut 分组:

- Cut 内(cross-edge)的 $\sigma_{ij}$:$i \in A_C, j \in B_C$(或反之)。这些 $\sigma_{ij}$ 是"双边"资源状态。
- Cut 两侧内(intra-cut):$\sigma_{ij}$ 两端同侧,这些在一侧作为 **local resource** 被消耗。

关键 trick:intra-cut $\sigma_{ij}$ **被吸收到一侧的 LOCC 中**(因为边在一侧两端,整个状态可由那一侧 local prepare)。所以末态 $\rho_{ab}^n$ 变成:

$$\rho_{ab}^n = \Lambda^{(A|B)}\left[\bigotimes_{(i,j) \in C} \sigma_{ij}^{\otimes n_{ij}}\right]$$

其中 $\Lambda^{(A|B)}$ 是 $A_C$-side 和 $B_C$-side 之间的**两侧 LOCC**。

> **信任入口 #3**(最致命):Step C 的 "intra-cut $\sigma_{ij}$ 吸收到一侧 LOCC" **要求那一侧的所有节点对该侧 end-user 合作**。在 umr 拓扑中,无论把 Charlie 划到哪一侧:
>
> - Charlie 在 Alice 侧:那么 $\sigma_{1} = \rho_{\mathcal{E}_1}$(Alice-Charlie edge)变成 "Alice 侧 intra-cut",由 Alice 和 Charlie **合作** prepare。但 Charlie 是 Eve,不会合作。
> - Charlie 在 Bob 侧:对称问题。
> - 把 $\sigma_1, \sigma_2$ 都划成 cut-edge(要求 cut 切两条边):这是 $\{a, b\}$ 同侧 vs $\{c\}$ 在另一侧 —— **不是一个 $(a,b)$-separating cut**,Step C 不承认这类 cut。

**Step D:Relative entropy upper bound on two-party state**

对末态 $\rho_{ab}^n$ 应用 Horodecki et al. 的 key-REE bound:

$$K(\rho_{ab}^n) \leq E_R(\rho_{ab}^n) \leq E_R\left(\bigotimes_{(i,j) \in C} \sigma_{ij}^{\otimes n_{ij}}\right) \leq \sum_{(i,j) \in C} n_{ij} E_R(\sigma_{ij})$$

第二个 ≤ 由 $E_R$ 在 LOCC 下 non-increasing;第三个 ≤ 由 $E_R$ subadditive。**这两个性质本身与 trust 无关**,是 state-level inequality。

**Step E:Minimize over cuts + normalize by total channel uses**

取 cut 最小值,$n \to \infty$ 后 $n_{ij}/n \to p_{ij}$,得到 $\mathcal{K}(a, b) \leq \min_C \sum_{(i,j) \in C} E_R(\mathcal{E}_{ij})$。

---

## 三、**替换为 umr 时,哪些步骤失效 —— 精确清单**

| Step | Pirandola 论证需要的条件 | umr 能否满足 | 修复方案 |
|------|------------------------|-------------|---------|
| A(LOCC simulation) | $i,j$ 两端皆为合作方 | 若 $j$ = Charlie, **失效**(Eve 控制 $j$ 的操作) | 可用 **monotonicity 包裹**:证明 umr 是 trust 的特例 |
| B(network stretching) | 全图节点 honest LOCC | **失效**(Charlie 不 honest) | 证明 stretching 对 adversarial middle node 是 **loose upper bound**(容易) |
| C(cut partition) | 每侧 intra-cut 节点合作 | **核心失效**(Charlie 无法合作放任一侧) | 不能修复;需绕开 —— 见下文 |
| D(REE on final ρ) | state-level,无 trust 依赖 | **通过** | —— |
| E(min over cuts) | cut-level,无 trust 依赖 | **通过**(假设 C 被修复) | —— |

### 3.1 Step C 的不可修复性 → 绕开路径

Step C 的 "intra-cut 吸收到一侧" 直接失效。有两条绕开路径:

**路径 α:Monotonicity reduction(FINDINGS v1 隐含使用)**

> Lemma(需要形式化):$\mathcal{K}_{\text{umr}}(\mathcal{T}_{\text{umr}}) \leq \mathcal{K}_{\text{trust}}(\mathcal{T}_{\text{umr}})$

这条 lemma 说:umr 协议是 trust-network 协议的特例(把 Charlie 限制到 measure-and-broadcast 是 LO 的特例;umr 安全 ⇒ trust 安全因 Eve 模型更弱)。

**[SYN/CONJ]** 这条 lemma "**方向上**"是对的,**但它不是 Pirandola 2019 的结果**。原论文既没有声明也没有证明它。把它作为"显然的"推演是 FINDINGS v1 的硬错。

真要证,至少需要:

- 协议层:umr 的 measure-and-broadcast 可嵌入为 general LOCC 的特例 —— **对**,显然。
- 安全层:umr-$\epsilon$-security $\Rightarrow$ trust-$\epsilon$-security —— **对**,因 trust 的 adversary 更弱(Eve 只控 channel,不控 Charlie)。两个安全定义的 ε 参数相同时可直接对接。
- Capacity 定义层:umr 的 rate 定义(只算 Alice-Bob 端对端 key)$\leq$ trust 的 rate 定义(可包含 relay-held intermediate keys)—— **可能对,但 Pirandola 2019 Sec II-C 的 key 是否包括 relay-held shares,需要逐字核对**。我的记忆里他的定义是 Alice-Bob 端到端 key,不包括 relay-held key,那这一条是 trivial。

**路径 β:Direct umr converse via channel-reduction**

另一条路:**不用 Pirandola 2019,直接把 $\mathcal{T}_{\text{umr}}$ 建模成单个 "effective channel"**:

$$\tilde{\mathcal{M}}: \mathcal{H}_A \otimes \mathcal{H}_B \to \mathcal{H}_A \otimes \mathcal{H}_B \otimes \mathcal{C}_{\text{broadcast}}$$

Alice 和 Bob 各送模式通过 $\mathcal{E}_1, \mathcal{E}_2$,Charlie 的测量 + 广播被吸收成 channel 的一部分(broadcast 是 classical 公开输出,等价于 Eve 可读)。

然后对 $\tilde{\mathcal{M}}$ 直接应用 **PLOB 2017 + two-way channel 的 converse**(Wilde-Tomamichel-Berta 2017 扩展)。这给出一个 **single-channel** converse,不再依赖网络 min-cut。

**[CONJ]** 这条路径的优点:完全避开 trust assumption。缺点:$\tilde{\mathcal{M}}$ 的 $E_R$ capacity 不等于 $\min\{E_R(\mathcal{E}_1), E_R(\mathcal{E}_2)\}$,可能更大(broadcast 降低了 Eve 的有效 noise,让 bound 变松)也可能更小(测量投影减少可提取关联)。需要真算。

---

## 四、核心结论(给 Sub-Q3 人类研究者)

### 4.1 Pirandola 2019 §II-C 的安全模型与 $\mathcal{T}_{\text{umr}}$ **定义不兼容**

不是"公式推广"的问题,是 **Eve 模型不一样**。FINDINGS v1 的 "直接套用 Eq. 11" 在**第一步就滑出了原论文的适用范围**,而这在 Phase R/V 的所有环节都没被警报,因为 AI 训练语料中的 QKD 综述普遍把 "min-cut = √η 上界" 当作常识复述,没标注 trust 模型。

### 4.2 Proof 失效在 Step C,不在 Step A/B/D/E

Step C(cut partition)的 intra-cut 吸收是**唯一**依赖"relay 对某侧端用户合作"的步骤。Step A/B 虽然也形式上需要 honest LOCC,但那是 representation-level,可以通过 monotonicity argument 转化为 upper bound;Step D/E 是纯 state-level 不等式,与 trust 无关。所以 **Sub-Q3 的精读报告应以 Step C 为核心展开**,用 30-50 页讨论的就是 "how to replace the cut-partition argument"。

### 4.3 路径 α(monotonicity)是正确路径,但需要**写出来**

路径 α 的三条 lemma(协议嵌入、安全归约、rate 定义对接)每条看似 trivial,但没写出来就是 informal 漏洞。这正是 RETRACTION §4.3 说的 "training-bias blindspot" —— codex 和 Claude 都把这三条当"常识",V1-V4 审计都没 flag。

### 4.4 路径 β(direct channel converse)可能给出**更紧的** bound

因为 umr 约束 Charlie 为 measure-only,实际 capacity 应该 **严格小于** trust capacity。Pirandola min-cut 给出的 $-\log(1-\sqrt\eta)$ 在 umr 下可能是 loose 的。Sub-Q4 的 gap analysis 若走路径 β,可能拿到一个 $\mathcal{K}_{\text{umr}} \leq f(\eta)$ 的新上界,$f(\eta) < -\log(1-\sqrt\eta)$ —— 这才是 TF-QKD prefactor gap 是"物理必要"还是"协议次优"的真正答案。

### 4.5 Scaling exponent 的上界(**最弱的可靠判断**)

唯一不依赖 trust assumption 的 scaling 结论:

- TF-QKD achievability ⇒ $\mathcal{K}_{\text{umr}} \geq c_1 \sqrt{\eta}$
- 单 channel PLOB on $\mathcal{E}_1$ alone ⇒ $\mathcal{K}_{\text{umr}} \leq -\log(1-\sqrt{\eta}) \leq c_2 \sqrt{\eta}$(**这一步只需 Alice-单独看 $\mathcal{E}_1$,不用网络 min-cut**)

等一下 —— 第二步实际不需要 Pirandola 2019,只需 PLOB 2017 应用在 Alice-Charlie 这一条 channel 上,然后注意"Alice 送出去的信息最多被 Charlie 接收",Eve 把 Charlie 做的事当做 additional attack,不能增加 Alice-Bob 的 correlation。

**[CONJ]** 如果这个直观正确,那 scaling-tight 结论(情况 A in the scaling sense)可能**不需要 Pirandola 2019**,直接从 PLOB 2017 + data-processing inequality 就够了。这会大幅简化 Sub-Q3 的核心 lemma。但需要严格写出 data-processing 那一步 —— 特别是"Eve 对 Alice→Charlie 的 mode 做任意后续操作(包括联合 Bob 的 mode 做 BSM)不会增加 Alice-Bob mutual information 的上界"的精确形式。这是 Sub-Q3 最值得优先尝试的**最小可信步骤**。

---

## 五、审计结论(本文件层)

RETRACTION 对 FINDINGS v1 的判决正确。Pirandola 2019 的 min-cut 不是 umr-free 的公式,它的 proof 从 **Step C** 开始依赖合作 relay,需要额外 lemma 才能合法跨入 umr。路径 α 可救回相同 scaling 结论,路径 β 可能给更紧的 bound。**scaling tight(情况 A of PROSPECTUS)** 的最小可信证明可能只依赖 PLOB 2017 + 单向 data-processing(**路径 γ**,见 §4.5),这一路径值得 Sub-Q3 优先尝试,作为"低风险的可信 baseline",再在其上讨论 prefactor gap。

---

## 六、对项目其他文档的影响(归档者 Claude 补)

本 Log 07 **取代**以下 AI 合成的旧论述:

- [Log 03 B.8](03_network_extension.md#b8):"untrusted 不放松上界" 的 [SYN] 级陈述 —— 被 §一.3 证明 Pirandola 2019 安全模型与 umr **定义不兼容**,不是"更紧"问题。
- [Log 04 B.1 H3](04_upper_bound_for_untrusted_relay.md#b1-定理陈述):Step 5 "H5 无存储单调继承" —— 真正的问题不是 H2(无存储),而是 Eve 模型错配,Log 04 需要补此诊断。
- [FINDINGS.md §4.1 A1](FINDINGS.md#a1) "Sub-Q3 工作重心":原写"找 DV-QKD-specific converse",正确改写为"按 Log 07 路径 α/β/γ 展开"。

本日志本身标 **[THM-LEVEL AUDIT]**(不是 AI [SYN]),因为它是项目负责人直接对原文进行的证明流程诊断。

---

## Changelog

- **v1.0**(2026-04-19):首次落盘。用户对 Pirandola 2019 §II + §IV 的精读审计,Claude 只做归档,不做 AI 二次加工。

---

*Log 07 结束。Sub-Q3 Phase 2 起点。*
