# Path δ — Relaxed-Trust Upper Bound Strategy

> **[SUPERSEDED 2026-04-25] by path α three-lemma framework (current active version: [v0.3](umr_path_alpha_three_lemma_v0_3.md) [USER-APPROVED PRIORITY])**
>
> 本文件提出的 capacity-level monotonicity 路径（δ.G2: 比较 Eve set 单调性）在 user 2026-04-25 进一步分析后被识别为**与 path α 同型 cross-space transfer 问题** —— path γ v0.2 retraction 的同型 trap。
>
> user 随后转向 **path α 三 lemma 协议级 embedding 路径**（Lemma A/B/C），但需注意：
>
> **重要修正（2026-04-25 v0.3 round 2 之后）**：v0.2 曾主张 path α "不比较 Eve，只比较 protocol class，真正绕开 β.G4" —— **这个 framing 在 v0.3 已被 user + reviewer 共同 disavow**。Path α 的 Lemma B（Security Reduction）仍在 cross-space 范畴（不同 Hilbert 空间的 Eve 集合 / protocol class 比较），**未自动绕开 β.G4 等价问题**。详见 [path α v0.3 §1.3](umr_path_alpha_three_lemma_v0_3.md)。
>
> **当前 active 版本**：[docs/proofs/umr_path_alpha_three_lemma_v0_3.md](umr_path_alpha_three_lemma_v0_3.md) [USER-APPROVED PRIORITY 2026-04-25, NOT C3-passed]
>
> **path α v0.2** ([umr_path_alpha_three_lemma_v0_2.md](umr_path_alpha_three_lemma_v0_2.md)) 永久 [REJECTED round 1]，保留作 cautionary record。
>
> **本文件保留作历史记录** —— §1.4 Eve-set 兼容性洞察（含 δ.G4）已精华提取嵌入 path α scaffolding 11-gap inventory 的 L2.G3。
>
> 全文不再被引用为 active research strategy。
>
> ---

**版本**：v0.1 [SPEC, SUPERSEDED]
**日期**：2026-04-25
**作者**：Claude (autonomous session, user-directed)
**严谨性**：本文件**全文 [SYN] 级**，无任何 [THM]/[COROLLARY] 升级。**不闭合任何 structural gap**，仅做策略陈述 + 文献综述 + 数值复用 + sub-gap 识别。

---

## §-1 R0.1 / R0.2 显式状态声明（**必读**）

### -1.1 本文件**不**做什么

- ❌ **不**声称已严格证明任何 K_umr 上界
- ❌ **不**升级任何已有 [SYN] / [CONJ] 标签到 [COROLLARY] / [THM]
- ❌ **不**绕过 path β/γ 的 4 个 open gap (β.G4 / β.G5 / γ.B.G1 / γ.G3)
- ❌ **不**替代 user 直读 Khatri-Wilde §19 的 PDF 精读工作

### -1.2 本文件**做**什么

- ✅ 形式化陈述 user 2026-04-25 提出的 **relaxed-trust 策略**（详见 conversation log）
- ✅ 把"trusted-relay 容量上界"作为 **K_umr 的 looser 上界** 的逻辑链显式化
- ✅ 复用现有 [pareto_mdi_family.md §3b](../findings/pareto_mdi_family.md) 与 [upper_bound_report.md §11](../findings/upper_bound_report.md) 的数值，**仅重新解读**
- ✅ 识别本策略下**仍存在**的 sub-gap（δ.G1/G2/G3），并显式标记 OPEN
- ✅ 提供 C1/C2/C3 验证路径建议

### -1.3 本策略与 path α/β/γ 的关系

- 本策略**不替代** β/γ —— β/γ 仍是闭合 K_umr 紧上界的**唯一**路径
- 本策略**互补** —— 在 4 个 gap 短期不会闭合的情形下，提供一个**严格的弱版结论**（可发表的次优陈述）
- **重要**：本策略产出的"严格 looser UB"只能作为**对外论文的 hedged framing**，**不**能作为 K_umr 紧界引用

### -1.4 第 6 次 trap 风险预警

memory 记录"AI draft 不得推 structural gaps"。本文件**仍可能踩 trap**，具体风险点：

- **δ.G1 风险**：将 "Pirandola 2019 N=1 严格适用于 trusted-Charlie + TF-protocol 组合" 当成 "literature consensus" 而非 structural gap（实际**仍需 PDF 验证**，详见 §3.3）
- **δ.G2 风险**：将"Eve 受限 → K 增大"的 monotonicity 当成显然（实际**需要**对 trust-relaxation 的 operational definition 严格定义）
- **δ.G3 风险**：将 numerical UB 数值 "$-\log_2(1-\sqrt{\eta})$" 当成 trust-relaxed [THM]，但该数值在 [pareto_mdi_family.md:92](../findings/pareto_mdi_family.md) 现存仍标记 **[CONJ for umr]** —— 即使在 trust-relaxation 下，也仅为 **[SYN] for trusted-relay**，需要单独验证

**所有 sub-gap 在本文件中保持 OPEN**。

---

## §1 策略陈述（user 2026-04-25 提出）

### 1.1 核心想法

> 不直接证明 untrusted-Charlie 拓扑下 K_umr 的紧上界（这需要闭合 4 个 gap）；
> 而是**主动声明**研究范围 **relaxed** 到 trusted-Charlie 拓扑，
> 在该拓扑下应用 Pirandola 2019 N=1 得到一个**严格的、但更松的**上界，
> 然后讨论 TF Pareto LB 与该 looser UB 的 gap。

### 1.2 形式化

定义两个 trust model：

- **T_strict (umr)**：Charlie 完全 untrusted，可被 Eve 任意控制；Eve 策略空间 = 所有 LOPC
- **T_relaxed (honest-Charlie)**：Charlie 执行**协议规定的固定操作**（TF: 单光子干涉 + 检测器宣告；MDI: BSM + outcome 宣告），Eve 仅有**信道环境 access**

对应容量：

- $K_{\text{umr}}(\mathcal{N})$：T_strict 下 secret-key capacity
- $K_{\text{trusted}}(\mathcal{N})$：T_relaxed 下 secret-key capacity

### 1.3 关键单调性 [SYN, sub-gap δ.G2]

**Claim [SYN]**：$K_{\text{umr}}(\mathcal{N}) \leq K_{\text{trusted}}(\mathcal{N})$

**Sketch（非证明）**：T_relaxed 是 T_strict 的 strict subset（Eve 策略空间收缩） → 协议在更弱 Eve 下能取得更高 key rate → sup over protocols also higher。

**δ.G2 OPEN**：上述 sketch **未形式化**。具体 gap：

- "T_relaxed 是 T_strict 的 subset" 需要 operational equivalence 证明
- 不同协议在两个 model 下的 reduction 需要 spec
- 是否所有 LOPC strategy 在 T_relaxed 下都可被 honest-Charlie + Eve 模拟？（**这其实就是 β.G4 的反向问题**）

**实施门槛**：需要 user 直读 Khatri-Wilde §19 LOPC 定义 + 比较 Pirandola 2019 §IV "fixed-channel" 假设。**AI 不能自走**。

### 1.4 Eve-set 兼容性 — path δ 的核心 value（user 2026-04-25 critical refinement）

#### 1.4.1 user 提出的核心 concern

> "TF 的安全性证明都对 EVE 做了限制，那么找上界的时候不对 eve 做这些限制，甚至可能存在找到的这个 UB 比 TF 安全性证明后的密钥率下界还要低的情况。"

**这不是 path δ 的 caveat，而是 path δ 存在的根本理由**。展开：

#### 1.4.2 LB 与 UB 的 Eve-set 兼容性原则（**这是被项目现有 gap framework 隐含忽略的关键约束**）

记：
- $\mathbb{E}_{\text{LB}}$ = TF security proof 推导 LB 时所**允许的** Eve 策略集合（typical: collective attack + 协议 spec 信息 + 有时 phase-reference calibration）
- $\mathbb{E}_{\text{UB}}$ = 上界定理推导 UB 时所**允许的** Eve 策略集合（Pirandola 2019: trusted-relay LOCC; 假定的 umr extension: full LOPC）
- $R_{\text{TF}}|_{\mathbb{E}}$ = TF 在 Eve 集合 $\mathbb{E}$ 下的**最坏 case** 可达率
- $K|_{\mathbb{E}}$ = Eve 集合 $\mathbb{E}$ 下的 capacity = sup over protocols of $R|_{\mathbb{E}}$

**单调性**：$\mathbb{E}_1 \subseteq \mathbb{E}_2 \Rightarrow R_{\text{TF}}|_{\mathbb{E}_1} \geq R_{\text{TF}}|_{\mathbb{E}_2}$ 且 $K|_{\mathbb{E}_1} \geq K|_{\mathbb{E}_2}$

**LB ≤ UB 何时保证？**

只有当 $\mathbb{E}_{\text{LB}} \supseteq \mathbb{E}_{\text{UB}}$（即 UB 在更**窄**或相等 Eve set 下推导，而 LB 在更**宽**或相等 Eve set 下推导）时，
$$R_{\text{TF}}|_{\mathbb{E}_{\text{LB}}} \leq K|_{\mathbb{E}_{\text{LB}}} \leq K|_{\mathbb{E}_{\text{UB}}}$$
其中最后一个 ≤ 用了 $\mathbb{E}_{\text{LB}} \supseteq \mathbb{E}_{\text{UB}}$ → $K|_{\mathbb{E}_{\text{LB}}} \leq K|_{\mathbb{E}_{\text{UB}}}$（Eve 越弱 capacity 越大）。

**反过来不保证**：如果 $\mathbb{E}_{\text{LB}} \subsetneq \mathbb{E}_{\text{UB}}$（LB 在更窄 Eve set，UB 在更宽 Eve set），则**完全可能 UB < LB**，这是 user 指出的反常情形。

#### 1.4.3 反常情形发生时**意味着什么**

**$UB|_{\mathbb{E}_{\text{UB}}} < R_{\text{TF}}|_{\mathbb{E}_{\text{LB}}}$ 不是矛盾，是诊断**：

它说明 **TF 的 security proof 的 Eve 限制对 √η 可达性是 essential 的** —— 即去掉那些限制后，TF protocol 不再保有 √η 速率。这不是 TF 错了，而是 TF 的 √η 结论**有 hidden assumption**。

具体可能发生的形式：
- (i) TF security proof 假设 collective attack；如果 Eve 用 coherent attack（broader），TF rate 可能下降
- (ii) TF security proof 假设 phase reference calibration；如果 Eve 控制 reference，TF rate 可能下降
- (iii) TF security proof 假设 Charlie announce 格式（detector clicks）；full LOPC Eve 可能 announce 任意经典讯息

#### 1.4.4 path δ 如何**结构性**避免这个反常

**Path δ 的设计**：T_relaxed **有意 match TF security proof 的 Eve 限制**（或者更宽松，i.e., $\mathbb{E}_{\text{LB}} \supseteq \mathbb{E}_{\text{T-relaxed}}$）。

- T_relaxed 假设 honest Charlie（按协议执行固定操作）
- TF security proof 也典型假设 honest-or-restricted Charlie（视具体证明而定）
- 如果两者 Eve set 兼容 → **UB^{T_relaxed} ≥ R_TF^{security} 是结构性保证的**

**这是 path δ 的核心 value**：它**把 Eve-set 兼容性显式 enforce 进策略**，反而避免了 path β/γ 隐含面临的"UB Eve set 比 LB 更宽，可能 UB < LB"的反常风险。

#### 1.4.5 对 path β/γ 的**反向影响**（critical observation）

**user 的 insight 也 expose 了 path β/γ 的一个隐藏问题**：

如果 path β/γ 试图证明 $K|_{\text{full LOPC umr}} \leq -\log_2(1-\sqrt{\eta})$，那么这个数值需要与 TF security proof 的 LB 兼容比较。但：
- TF security proof 的 LB 在 $\mathbb{E}_{\text{LB}}$ (restricted) 下推导，**不一定** valid against full LOPC umr
- 项目当前 gap_analysis 把 "TF Pareto LB" 与 "Pirandola N=1 [CONJ for umr] UB" 直接比较，**隐含假设 LB 在 umr 下仍 valid**
- **这个隐含假设需要单独验证**

**新发现的 hidden gap**：项目现有 [docs/findings/gap_shape_g4_1.md](../findings/gap_shape_g4_1.md) 与 [docs/findings/pareto_mdi_family.md §3b](../findings/pareto_mdi_family.md) 的 "LB vs UB" 比较，**Eve-set 兼容性未显式验证**。这不是 immediate retraction-worthy 的错误（数值仍正确），但是一个**应当显式 disclose 的 caveat**。

**建议 Day 5+ action**：在 [gap_shape_g4_1.md](../findings/gap_shape_g4_1.md) 增补 §-disclaimer 章节，显式说明 LB Eve set vs UB Eve set 兼容性 OPEN。**这个修补应由 user approve 后再做，不是 AI 自动 commit**。

#### 1.4.6 新增 sub-gap δ.G4

**δ.G4: TF security-proof Eve set vs T_relaxed Eve set 的精确比对**

- 需要 user 直读 Lucamarini 2018 / Wang 2019 / Cui 2019 / Curras-Lorenzo 2021 的 Eve assumption 章节
- 与 Pirandola 2019 §IV / Khatri-Wilde §19 的 Eve assumption 比对
- 验证 $\mathbb{E}_{\text{LB}} \supseteq \mathbb{E}_{\text{T-relaxed}}$（path δ 严格性所必需）
- **状态**：OPEN，**实施门槛**：user 多份 PDF 直读 + 形式化 Eve assumption 表格

---

## §2 Pirandola 2019 N=1 在 T_relaxed 下的应用

### 2.1 公式

Pirandola 2019 Eq. 9 at N=1（trusted single-relay chain）：

$$K_{\text{trusted}}(\mathcal{N}_{\text{2-segment loss}}) \leq -\log_2(1 - \sqrt{\eta_{AB}})$$

其中 $\eta_{AB}$ 是 Alice-Bob 端到端 transmittance，每段 $\eta_{\text{arm}} = \sqrt{\eta_{AB}}$。

### 2.2 严谨性 [SYN, sub-gap δ.G1]

**Pirandola 2019 §IV** 显式假设 trusted relay node。在 T_relaxed 下，Charlie 是 honest（按协议执行固定操作），所以**前提对接看上去自然**。

**δ.G1 OPEN**：但仍有需要核对的细节：

- Pirandola 假设的 "fixed channel + LOCC at relay" 是否精确包含：
  - TF 协议 Charlie 端的 single-photon interference（**非简单 LOCC**，是 unitary + measurement）
  - TF 的 phase-reference distribution（multi-round protocol element）
  - decoy state announcement structure
- Pirandola 2019 N=1 是否覆盖**非对称** loss（$\eta_A \neq \eta_B$，TF practical 设置）

**实施门槛**：需要 user 直读 Pirandola 2019 §IV + Eq. 9 推导细节，逐项核对 TF protocol 是否在其允许的 protocol class 内。**这一步比 β.G4 容易**（不需对接 untrusted-Charlie），但**仍非自明**。

### 2.3 与 path β/γ 的对比

| 维度 | path β/γ (闭合 K_umr) | path δ (relaxed-trust) |
|---|---|---|
| 目标 | $K_{\text{umr}} \leq -\log_2(1-\sqrt{\eta})$ as [THM] | $K_{\text{trusted}} \leq -\log_2(1-\sqrt{\eta})$ as [SYN], 同时 $K_{\text{umr}} \leq K_{\text{trusted}}$ as [SYN] |
| 主要 gap | β.G4 / β.G5 / γ.B.G1 / γ.G3（**4 个 hard gaps**） | δ.G1（fixed-channel 适用性） + δ.G2（trust-monotonicity）（**2 个 softer gaps**） |
| 数值 UB | 同公式 $-\log_2(1-\sqrt{\eta})$ | 同公式（**数值不变**） |
| 紧界 vs 松界 | 紧（直接对 K_umr） | 松（only K_trusted directly bounded; K_umr 通过 monotonicity 间接） |
| 可发表 framing | "K_umr 紧上界" | "K_trusted 严格上界 + K_umr ≤ K_trusted" |
| AI 自主可推进度 | 全部受 R0.1 阻断 | δ.G1 / δ.G2 仍需 user 直读 PDF，但**门槛更低** |

---

## §3 数值复用与重新解读

### 3.1 数据来源（无新计算）

- [docs/findings/pareto_mdi_family.md §3b.2](../findings/pareto_mdi_family.md)：MDI Pareto LB vs Pirandola N=1 cand UB
- [docs/findings/upper_bound_report.md §11](../findings/upper_bound_report.md)：四信道 UB 层级
- [docs/findings/gap_shape_g4_1.md](../findings/gap_shape_g4_1.md)：gap 定量形状 v0.4
- [docs/research/figures/family_comparison.png](../research/figures/family_comparison.png)：三族 + UB 候选线

### 3.2 重新解读 [SYN]

复用上述数据，但**标签更新**：

- 原标签："Pirandola N=1 [CONJ for umr]"
- 新标签（path δ 下）："Pirandola N=1 [SYN for trusted-relay]，由 monotonicity 给 K_umr 的 [SYN] looser UB"

**数值不变**：

| loss (dB) | TF Pareto LB | path δ looser UB | LB / UB ratio |
|---|---|---|---|
| 0 | (TF 数值) | $\infty$ (η=1 singular) | — |
| 10 | (TF 数值) | 0.5484 | (复用) |
| 20 | (TF 数值) | 0.1520 | (复用) |
| 30 | (TF 数值) | 0.04636 | (复用) |
| 40 | (TF 数值) | 0.01450 | (复用) |
| 50 | (TF 数值) | 4.55e-3 | (复用) |
| 60 | (TF 数值) | 1.43e-3 | (复用) |

> **Note**: TF 实测数值待 sweep_tf_family.py 重新对齐填表（Day 5 工作）

### 3.3 解读：[SYN] 级陈述

**[SYN-δ-1]**: 在 T_relaxed 下，TF-QKD 的可达率与 Pirandola 2019 N=1 上界 **同 √η scaling**，gap 仅在 prefactor 量级（对齐数值待 §3.2 表填表）。

**[SYN-δ-2]**: 任何"超越 TF √η 的协议"如果存在，**必须利用 untrusted-Charlie 比 honest-Charlie 提供的额外结构** —— 因为 K_trusted 已被 √η UB 锁住。

**[SYN-δ-3]**: 这把 PROSPECTUS Sub-Q4 的归因空间**显著缩小**：
- A 因子（UB 松）→ 在 T_relaxed 下被排除（path δ UB 严格 = √η scaling）
- B 因子（协议次优）→ 仍 OPEN，但要求探索者必须 invoke untrusted-Charlie 才能绕过 √η 屏障

---

## §4 sub-gap 显式清单

| sub-gap | 描述 | 状态 | 实施门槛 |
|---|---|---|---|
| **δ.G1** | Pirandola 2019 N=1 在 trusted-Charlie + TF/MDI specific protocol 下的严格适用性 | OPEN | user 直读 Pirandola 2019 §IV / Eq. 9 + 核对 TF/MDI protocol class |
| **δ.G2** | Trust-monotonicity $K_{\text{umr}} \leq K_{\text{trusted}}$ 的形式化 | OPEN | user 写下 trust-model operational equivalence + 比较 LOPC vs honest-Charlie strategy classes |
| **δ.G3** | TF practical（非对称 loss、coherent state、phase reference）在 Pirandola 框架内的覆盖 | OPEN | user 核对 Pirandola 2019 / Khatri-Wilde §19 是否覆盖 |
| **δ.G4** | TF security-proof Eve set $\mathbb{E}_{\text{LB}}$ vs T_relaxed Eve set $\mathbb{E}_{\text{T-relaxed}}$ 的精确比对（**§1.4 critical**） | OPEN | user 直读 Lucamarini 2018 / Wang 2019 / Cui 2019 / Curras-Lorenzo 2021 的 Eve assumption + 与 Pirandola 2019 §IV / KW §19 比对 |

**所有 sub-gap 在 v0.1 保持 OPEN**。**不**做 AI draft 闭合（per memory: AI draft 不得推 structural gaps）。

**特别提示**：δ.G4 是 user 2026-04-25 critical refinement 引入的**新发现 gap**，它**不只**适用于 path δ —— 它**反向暴露**了项目现有 [gap_shape_g4_1.md](../findings/gap_shape_g4_1.md) / [pareto_mdi_family.md §3b](../findings/pareto_mdi_family.md) 中 LB vs UB 比较的**隐含 Eve-set 假设**未显式验证（详见 §1.4.5）。这是**比 path δ 自身更广的发现**。

---

## §5 验证路径建议（C1 / C2 / C3）

### 5.1 升级 path δ 到 [COROLLARY]（target）

**C1 (independent validation)**：
- (a)+(c) 推荐组合：跨家族 AI（Claude + GPT/Codex 双方直读 Pirandola 2019 §IV PDF）+ 数值 SDP 重算 trust-relaxed UB
- 或 (b) 人类研究者纸笔复核 §3 monotonicity argument

**C2 (user 签字)**：user 对 §1 策略陈述、§2 公式适用性、§4 sub-gap 清单**逐项**确认

**C3 (dev-reviewer)**：本文件提交 dev-reviewer 双 Codex 评审，重点 review:
- §-1 R0.1/R0.2 disclosure 是否充分
- §1.3 / §2.2 sub-gap 是否被错误地"draft 闭合"
- §3.3 [SYN] 陈述措辞是否过 strong

### 5.2 短期可推进的工作（**不需要 4 个 main gap 闭合**）

1. **Day 5 (autonomous-acceptable)**：填齐 §3.2 表格，对齐 TF Pareto LB 与 path δ looser UB 在标准 loss grid 上的数值；产出独立 figure
2. **Day 6 (user-required)**：user 直读 Pirandola 2019 §IV + Khatri-Wilde §19 fixed-channel 假设，**判定 δ.G1 是否 closeable**
3. **Day 7 (user-required)**：user 形式化 §1.3 trust-monotonicity argument，**判定 δ.G2 是否 closeable**
4. **Day 8 (autonomous-acceptable)**：基于 user 判定结果 + dev-reviewer 评审，发布 v0.2

### 5.3 长期定位

如果 δ.G1 / δ.G2 / δ.G3 在 user 验证后均 closeable：
- path δ 升级为 [COROLLARY]，对外可引用为 "TF saturate trusted-relay UB up to prefactor"
- 提供 Sub-Q4 答案的**严格弱版**（"在 trusted-relay 还原下 √η 是紧的"）
- 不替代 path β/γ 的强版，但**在 4 个 gap 长期不闭合时构成可发表 fallback**

如果 δ.G1 / δ.G2 / δ.G3 任一**不**可 close：
- 本策略仍可作为 [SYN] 级 hedged framing 写入 future paper introduction
- 但**禁止**单独引用为定理级结论

---

## §6 与现有文档的关系

### 6.1 不修改

- ❌ **不修改** [docs/findings/upper_bound_report.md](../findings/upper_bound_report.md) v0.7（formal record）
- ❌ **不修改** [docs/research/FINDINGS.md](../research/FINDINGS.md) v2（结论 ledger）
- ❌ **不修改** [docs/PHASE_STATUS.md](../PHASE_STATUS.md) main gap 清单
- ❌ **不修改** [docs/proofs/umr_path_beta_*.md](../proofs/) 系列（保留 path β 状态）

### 6.2 新增

- ✅ 本文件（v0.1 SPEC）
- ✅ [docs/findings/pareto_mdi_family.md](../findings/pareto_mdi_family.md) §3b 添加 cross-reference 到本文件（**仅 reference，不改原数据**）—— 留待 user 显式 approve

### 6.3 与 path β/γ 的并行关系

| 时间线 | path β/γ | path δ |
|---|---|---|
| 当前 | β.G4 / β.G5 / γ.B.G1 / γ.G3 OPEN | v0.1 [SPEC] 立项 |
| Day 5-8 | （等 user 直读 KW §19） | δ.G1 / δ.G2 验证（user PDF + 形式化） |
| Day 9+ | （依赖 user 推进） | v0.2 整合 user 判定 |

**两条路并行不冲突**。如果 path β/γ 任一闭合 → path δ 自动成为冗余但**仍是 hedged statement 的良好基础**；如果 4 个 gap 全部长期不闭合 → path δ 是 "next-best honest framing"。

---

## §7 Changelog

- **v0.1** (2026-04-25)：首版立项。response to user 2026-04-25 conversation directive "沿着这个思路继续下面的研究，但是必须把这个情况显示说明出来"。全文 [SYN] 级，3 个 sub-gap 显式 OPEN。

---

## §8 致谢与署名

- **策略 origin**：user 2026-04-25 conversation（明确提出 relaxed-trust 思路）
- **策略 formalization**：Claude autonomous session
- **下一步 action owner**：user（δ.G1 / δ.G2 PDF 验证）

**本文件不构成对外可引用的研究结论**。所有进一步引用前必须经 R0.2 (C1 ∧ C2 ∧ C3) 完整流程。

---

*END OF v0.1.* Sub-gaps δ.G1 / δ.G2 / δ.G3 OPEN. R0.1 不降级 / R0.2 不越权 / R0.3 [SYN] 级保持。
