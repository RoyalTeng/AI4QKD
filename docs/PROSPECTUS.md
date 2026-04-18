# Research Prospectus v3.0

**无中继离散变量 QKD 的根本极限:统一框架、严格评估与 Gap 刻画**

**版本**:v3.0
**日期**:2026-04-17
**作者**:[用户] + Claude (Opus 4.7) 协作规划
**前置版本**:v1.0(2026-04-17 早些时候)

> **与 [REFACTORING_PLAN.md](REFACTORING_PLAN.md) 的关系**:
> 本文档是**研究地图**(WHY — 主问题、约束、Sub-Q1→Sub-Q5 子问题序列);
> REFACTORING_PLAN.md 是**函数级实施规范**(HOW — 每个模块的 API、测试、里程碑硬验收、运营控制)。
> 当工期/里程碑结构数字不一致时,**以 REFACTORING_PLAN.md §5 为准**
> (该文档经 2026-04-18 codex 六轮审计硬化)。

---

## 修订说明

本文档是对 v1.0 的**结构性重写**,不是增量更新。两者的关键区别:

- **v1.0 的定位**:项目管理文档 —— 包含 T1/T2/T3 目标分层、概率评估、期待管理、失败模式承诺、过程性指标等。假设研究者需要显式的目标阶梯和心理预期管理。
- **v3.0 的定位**:研究地图 —— 只包含问题陈述、方法、可验证的子问题序列。假设研究者由学术好奇心驱动,不需要外部期待管理。

**为什么修订**:v1.0 假设的驱动力(部分功利、需要阶段性激励)与研究者真实驱动力(纯粹学术好奇心,想要知道真相)不符。v1.0 的很多结构对好奇心驱动的研究无用甚至有害 —— 例如 "T3 概率 < 5%" 这类估计反复出现会制造不必要的噪音。

**v1.0 历史归档,不再作为 active 文档**。

---

## 1. 主问题

**核心问题**:在无量子中继、无量子存储、使用离散变量载体的约束下,两方之间通过(至多一个)untrusted measurement relay 建立共享密钥的**信息论极限**是什么?

这个问题的答案有三种结构性可能:

- **情况 A**:$\sqrt{\eta}$ 标度是紧上界。TF-QKD 族达到了根本极限,无中继无存储 DV-QKD 的故事已经讲完
- **情况 B**:存在 $\eta^\alpha$($1/2 < \alpha < 1$)的上界,且这个上界可达。TF-QKD 之后还有空间,某种新协议结构能利用这个空间
- **情况 C**:存在 $\eta^\alpha$ 的上界但不可达。标度"空间"在数学上开着,但物理上关着

真相属于哪种情况是本项目的**核心好奇对象**。每一种情况都对应不同的后续研究图景,但每一种答案本身都是可验证的、可发表的、有意义的科学结论。

---

## 2. 问题的演化历史

这个主问题是经过多次精细化浮现的,理解它的演化能帮助日后工作中避免已走过的弯路:

**原始形式(项目起点)**:找到超越 TF-QKD 的新 QKD 协议。

**第一次精细化**:认识到"超越 TF-QKD"有多种意义。排除"超越 PLOB"(物理不可能,需要量子中继或存储)。聚焦于"在无中继无存储约束下,标度比 $\sqrt{\eta}$ 好"。

**第二次精细化**:认识到 AI 搜索只能在已定义的协议空间内寻找最优,不能自动发现"重新定义空间"的新物理机制(BB84→MDI→TF-QKD 每次跃迁的本质)。AI 作为工具被重新定位:不是"产生洞察的主体",而是"辅助刻画问题结构的工具"。

**第三次精细化**:认识到"找新协议"(构造性陈述)和"刻画极限"(刻画性陈述)在信息论上等价。如果紧上界是 $\sqrt{\eta}$,无新协议可找;如果紧上界是 $\eta^\alpha$ 且 $\alpha < 1/2$,新协议的方向自然浮现。从"找"变为"刻画"不是目标降级,是问题的数学成熟化。

**当前形式**:主问题如 §1 所述。

---

## 3. 研究约束

以下约束定义问题的边界。违反这些约束的讨论超出本项目范围。

### 3.1 硬约束

| 编号 | 约束 | 形式化 |
|------|------|--------|
| H1 | 无量子中继 | $|\mathcal{P}| \in \{1, 2\}$,中间节点不包含纠缠生成或纠缠交换 |
| H2 | 无量子存储 | 源方制备态后不对本地量子系统做延迟操作 |
| H3 | 刻画式设备信任 | 源态已知;测量设备可部分不信任(Level 1-3,排除 Level 0 DI) |
| H4 | 有限维 | $\dim \mathcal{H}_{A_i'} < \infty$;允许 Fock 截断 |
| H5 | 可组合安全性 | 协议安全性必须可在 Portmann-Renner 可组合框架下陈述 |
| H6 | 离散变量 | 密钥信息编码在离散寄存器中 |

### 3.2 明确不在范围内

- 连续变量 QKD(CV-QKD)
- 设备无关 QKD(DI-QKD,基于 Bell 违反)
- Memory-assisted 或 quantum-repeater-based 协议
- 形式化证明工具(Coq/Lean/Isabelle)的使用
- 实验实现和硬件开发

---

## 4. 核心抽象:MS-EB 框架

### 4.1 框架定义

**MS-EB (Multi-Source Entanglement-Based) 框架**:将任何满足 §3.1 约束的 DV-QKD 协议表达为五元组

$$\Pi = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$$

- $\mathcal{P}$:源方集合(每方持 EB 纯态)
- $\mathcal{E}$:公共量子网络(CPTNI 映射,含可能的 untrusted relay)
- $\mathcal{A}$:宣告规则(需 GEAT non-signalling 兼容)
- $\mathcal{T}$:接受性测试
- $\mathcal{K}$:密钥映射(CPTNI)

完整技术定义见 `PHASE0_M1_TECHNICAL_SPEC.md` §2 及后续讨论。

### 4.2 框架的功能

MS-EB 在本项目中承担三个功能:

1. **统一表达**:BB84、MDI-QKD、TF-QKD、MP-QKD 及它们的参数变体能在同一语言下表述,便于系统比较
2. **工具接口**:协议对象自动派生出 WLC SDP 的输入(可计算紧密钥率下界)和 GEAT 的输入(可计算有限密钥率)
3. **问题空间的参数化**:主问题 §1 的"协议空间"在 MS-EB 下变成"符合 §3.1 约束的五元组构型空间" —— 这是可操作的数学对象

### 4.3 框架的已知限制

- 覆盖率约 85-90%(对 §3.1 约束内的主流 DV-QKD 协议)
- 不能表达的部分主要是"跨轮自适应改变协议结构"类协议
- 对"分布式相位参考"等特殊资源的表达是工程性的(通过 $\mathcal{E}$ 建模),不是原生支持

这些限制在当前范围内不修复。如果后续研究需要扩展,再处理。

---

## 5. 评估工具链

对任何 MS-EB 协议 $\Pi$,项目维护三层评估:

### 5.1 紧密钥率下界(WLC SDP)

基于 Winick-Lütkenhaus-Coles 2018 的半正定规划方法。对任何 $\Pi$ 计算

$$R_{\text{LB}}(\Pi, \eta, \text{noise params}) \leq R^\infty(\Pi)$$

这是对 Eve 所有相干攻击的凸优化结果,**不可通过协议构造绕过**。

Phase 0 建设。

### 5.2 有限密钥可组合率(GEAT)

基于 Metger-Fawzi-Sutter-Renner 2024 的广义熵积累定理。对任何 $\Pi$ 计算

$$\ell(\Pi, n, \varepsilon_{\text{sec}}, \varepsilon_{\text{corr}})$$

Phase 1 建设。

### 5.3 紧密钥率上界(协议族上界 SDP)

基于 Wilde-Tomamichel-Berta 2017 / Pirandola 2019 / Das-Khatri-Wilde 2020 的 relative entropy of entanglement 上界框架。对**协议族** $\mathcal{F}$(不是单个协议)计算

$$R_{\text{UB}}(\mathcal{F}, \eta, \text{topology}) \geq \sup_{\Pi \in \mathcal{F}} R^\infty(\Pi)$$

Phase 2 主要建设对象。这是刻画 gap 所需要的工具。

### 5.4 评估工具链的完整数据流

```
MS-EB 协议 Π ─────┬─── WLC SDP (Phase 0)  ──→ R_LB
                  │
                  ├─── GEAT (Phase 1)     ──→ ℓ(n, ε)
                  │
协议族 F ─────────┴─── Upper-bound SDP (Phase 2) ──→ R_UB

然后:gap(F, η) = R_UB(F, η) - sup_{Π∈F} R_LB(Π, η)
```

---

## 6. 子问题序列

主问题通过以下子问题分解。每个子问题是可独立推进的研究单元,且对前置子问题的完成状态有依赖。

### Sub-Q1(Phase 0):评估工具链的基础建设

**形式化陈述**:实现 WLC SDP 的协议无关版本,对 MS-EB 下的 BB84、MDI-QKD、TF-QKD(含 SNS 和 MP 变体)能给出与文献一致的密钥率曲线。

**验收**:对每个协议,数值密钥率与已发表解析/数值结果误差 < 1%(BB84/MDI)或 < 5%(TF/MP)。

**预计时长**:8-10 周(见 M1-M4)。

### Sub-Q2(Phase 0 末-Phase 1):现有协议族在 MS-EB 下的系统刻画

**形式化陈述**:对 §3.1 约束内的协议族 $\mathcal{F}$(BB84 族、MDI 族、TF 族),在 MS-EB 下给出结构化描述:

- $\mathcal{F}$ 内的协议如何被五元组参数化
- $\mathcal{F}$ 的对称群
- $\mathcal{F}$ 内密钥率的数值 Pareto 前沿

**验收**:产出对每个主要协议族的 "family sheet" —— 描述族的范围、已知最优协议、Pareto 前沿数据。

### Sub-Q3(Phase 1):PLOB 及其推广在 MS-EB 框架下的精读与重构

**形式化陈述**:完全理解 Pirandola 2017 PLOB 定理的证明。识别它在 "untrusted measurement relay" 拓扑下的适用性和不适用性。推导 Pirandola 2019 的网络推广和 Das-Khatri-Wilde 2020 的改进在 MS-EB 的等价陈述。

**验收**:产出一份 30-50 页的"接缝报告",精读这几篇论文的证明,识别关键假设,分析它们对"两方 + untrusted relay"拓扑的 bearing。

### Sub-Q4(Phase 2 上半):untrusted relay 拓扑上界的当前状态

**形式化陈述**:基于 Sub-Q3 的理解,给出当前文献对"两方 + untrusted relay"拓扑的最紧已知上界 $R_{\text{UB}}^{\text{current}}(\eta)$。确定这个上界的 scaling 形式(是 $\eta$?还是 $\sqrt{\eta}$?还是介于之间?)。

**验收**:对这个拓扑给出一个具体的、可计算的 $R_{\text{UB}}^{\text{current}}(\eta)$ 表达式,并与 TF-QKD 的 $\sqrt{\eta}$ 可达率做数值对比。

### Sub-Q5(Phase 2 下半 + Phase 3):Gap 刻画

**形式化陈述**:计算 $\text{gap}(\eta) = R_{\text{UB}}^{\text{current}}(\eta) - R_{\text{LB}}^{\text{TF-QKD}}(\eta)$ 的具体形状。判定 gap 是由于:

- (a) 当前上界证明技术的松弛(可通过更精细的证明收窄)
- (b) 当前 TF-QKD 族的不足(可通过新协议打开)
- (c) 以上两者的某种组合

**验收**:对 $\text{gap}(\eta)$ 的结构给出可论证的判断。如果判断是 (a),尝试证明更紧上界。如果是 (b),识别 TF-QKD 族外的候选协议结构。如果是 (c),对两个方向都给出分析。

### 子问题间的逻辑

```
Sub-Q1 ──── 建工具
   │
   ▼
Sub-Q2 ──── 用工具刻画已知
   │
   ▼
Sub-Q3 ──── 理解已知上界的推导
   │
   ▼
Sub-Q4 ──── 把上界放到我们的拓扑
   │
   ▼
Sub-Q5 ──── 刻画 gap,指向后续
```

任何子问题如果产生了意外结果(例如 Sub-Q2 发现某个协议的数值密钥率超过预期),子问题序列会对应调整,不严格按 Q1→Q5 线性推进。

---

## 7. Phase 0 详细路线

### 7.1 Milestone 分解

| Milestone | 主要内容 | 周数 | 对应子问题 |
|-----------|---------|------|-----------|
| M1 | WLC SDP 在 BB84 上的最小实现 | 2 | Sub-Q1 |
| M2 | 扩展到 MDI-QKD 和六态 | 1.5 | Sub-Q1, Sub-Q2 启动 |
| M3 | 数值诱骗态分析 | 2 | Sub-Q1, Sub-Q2 |
| M4 | TF-QKD 族数值验证 | 3 | Sub-Q1, Sub-Q2 |

**总 Phase 0:8-10 周(含缓冲)。**

> **⚠️ 工期口径对齐**:本节的 **8-10 周** 为研究规划视角下的理想工期;经 2026-04-18 两轮 codex 严肃审计后,实施层已保守调整为 **Phase 0 必需 12 周 + M4B(TF-QKD)可选 2–3 周 = 总预算 12–16 周**。具体工期以 [REFACTORING_PLAN.md §5](REFACTORING_PLAN.md) 为准;本 prospectus 的 8-10 周数字**仅作研究地图的节律参考**,不作为开工的硬约束。

> **⚠️ M4 结构口径对齐**:上表的 **M4 单里程碑(3 周,含 TF-QKD 与 MP 变体)** 为研究地图视角下的打包;经 codex §8-4 评审(失败耦合过高),实施层已拆分为:
> - **M4A(2 周)**:symmetry on BB84/6-state,不含 TF-QKD
> - **M4B(2–3 周,可延至 Phase 0.5)**:TF-QKD 族数值验证,独立验收
>
> 详见 [REFACTORING_PLAN.md §5](REFACTORING_PLAN.md)。

### 7.2 Phase 0 产出

- `qkdx/` 代码库:MS-EB 框架 + WLC SDP 的协议无关实现 + 三大协议族(BB84/MDI/TF)的完整支持
- 每个协议的 family sheet 初稿(Sub-Q2 部分完成)
- `PHASE0_M1_TECHNICAL_SPEC.md` — M1 实施指南(待落盘)

### 7.3 过渡到 Phase 1 的条件

研究地图口径下,M1-M4 完成即进入 Phase 1;实施开工口径以 [REFACTORING_PLAN.md §5](REFACTORING_PLAN.md) 为准(M1-M3 + M4A 必需,M4B 可延至 Phase 0.5)。

---

## 8. Phase 1+ 粗略规划

粗粒度即可,细节到时根据 Phase 0 结果再确定。

**Phase 1(约 3-4 个月)**:

- GEAT 有限密钥层实现
- Sub-Q2 的完整 family sheets
- Sub-Q3 启动(PLOB 精读)
- 接受性测试 $\mathcal{T}$ 的系统化处理

**Phase 2(约 6-12 个月)**:

- 上界 SDP 工具链(Layer 5.3)
- Sub-Q3 完成
- Sub-Q4 完成
- Sub-Q5 启动

**Phase 3(12+ 个月)**:

- Sub-Q5 完成
- 视结果决定后续方向:如果 gap 紧,工作收束;如果 gap 松,新协议结构探索

---

## 9. 诚信声明

本项目在方法论上承诺:

- 所有密钥率数字**基于 WLC SDP 或其严格扩展**,不使用自编公式
- 所有协议安全性声明**追溯到具体定理**(Shor-Preskill / Devetak-Winter / Portmann-Renner / Metger GEAT / Pirandola PLOB 及其扩展)
- 所有新发现(如有)**通过独立数值方法或人工重推的子情形验证**
- 所有结论在发表时**显式声明 limitations**

本项目起源于对 `RoyalTeng/AI4QKD` v1 仓库的审查。该仓库因评估层不严格导致"超越 BB84"的虚假结论。本项目在地基上排除这类错误 —— WLC SDP 的数学严格性使 AI 作弊性结果不可能被误认为发现。

AI 工具(Claude Anthropic Opus 4.7)在本项目规划阶段作为讨论伙伴使用。AI 的角色是"信息整理者 + 结构化讨论伙伴",**不是权威来源**。所有技术决策由人类研究者负责。对话历史在 `conversations/` 归档。

---

## 10. 参考文献(精简版)

本节只列执行当前方向必需的文献。详细清单见项目 wiki 或 Zotero 库。

**评估工具链核心**:

- Winick, Lütkenhaus, Coles 2018, Quantum 2:77 — WLC SDP 主文
- George, Lin, Lütkenhaus 2021, PRR 3:013274 — 数值方法的 finite-key 扩展
- Metger, Fawzi, Sutter, Renner 2024, Commun. Math. Phys. 405:261 — GEAT
- Kamin, Arqand, George, Lütkenhaus, Tan 2025, PRX Quantum 6:020342 — 实用 finite-key

**可组合安全性**:

- Portmann, Renner 2022, RMP 94:025008 — AC 框架综述
- Renner 2005 PhD thesis — smooth entropy 原著

**上界理论(Phase 1-2 阅读重点)**:

- Pirandola, Laurenza, Ottaviani, Banchi 2017, Nat. Commun. 8:15043 — PLOB 定理
- Pirandola 2019, Commun. Phys. 2:51 — 网络推广
- Wilde, Tomamichel, Berta 2017, IEEE TIT 63:1792 — PLOB 独立推导
- Das, Khatri, Wilde 2020, arXiv:2012.03262 — converse bound 最新版
- Takeoka, Guha, Wilde 2014, Nat. Commun. 5:5235 — PLOB 的前身

**协议族原文**:

- Lo, Curty, Qi 2012, PRL 108:130503 — MDI-QKD
- Lucamarini et al. 2018, Nature 557:400 — TF-QKD
- Ma, Zeng, Zhou 2018, PRX 8:031043 — PM-QKD
- Zeng, Zhou, Wu, Ma 2022, Nat. Commun. 13:3903 — MP-QKD

**背景综述(按需)**:

- Xu, Ma, Zhang, Lo, Pan 2020, RMP 92:025002 — 实用 QKD 综述
- Scarani et al. 2009, RMP 81:1301 — 经典 QKD 综述

---

## 文档管理

- **版本**:v3.0(2026-04-17)
- **前置**:v1.0(同日),已归档
- **关联文档**:
  - [REFACTORING_PLAN.md](REFACTORING_PLAN.md) — 函数级实施规范,工期/阈值以此为准
  - `PHASE0_M1_TECHNICAL_SPEC.md` — M1 实施细节,尚未落盘
  - `ROADMAP.md` — 周级进度(Phase 0 启动后生成)
  - `conversations/` — 原始讨论归档
  - `references/` — BibTeX 库
- **下次强制 review**:Phase 0 末(预计 2026-06-15 左右)
- **修订原则**:任何版本变更必须记录 (a) 修订日期 (b) 触发事件 (c) 主要变更点

---

## Changelog

- **v1.0**(2026-04-17 早些):项目管理叙事,T1/T2/T3 目标分层 + 概率估计 + 失败模式承诺。已归档。
- **v3.0**(2026-04-17):结构性重写为研究地图。主要变更:
  - 用"主问题 + Sub-Q1→Sub-Q5 子问题序列"替换 T1/T2/T3 目标分层
  - 去除概率估计、期待管理、过程性指标
  - 明确"找新协议"与"刻画极限"的信息论等价性
  - 把 AI 从"搜索主体"降为"讨论/计算辅助"
  - 保留 §7.1 两处口径对齐注脚(v1.0-notes 追加,指向 REFACTORING_PLAN.md §5)

---

*文档结束*
