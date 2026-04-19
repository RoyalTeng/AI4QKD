# Research Prospectus v3.1

## 无中继离散变量 QKD 的根本极限:统一框架、严格评估与 Gap 刻画

**版本**:v3.1
**日期**:2026-04-17
**作者**:[用户] + Claude (Opus 4.7) 协作规划
**前置版本**:v3.0(2026-04-17 早些时候)→ v1.0(同日更早)

> **与 [REFACTORING_PLAN.md](REFACTORING_PLAN.md) 的关系**:
> 本文档(v3.1)是**研究地图**(WHY — 主问题、约束、Sub-Q1→Sub-Q4 子问题序列);
> REFACTORING_PLAN.md(v3.1.4)是**函数级实施规范**(HOW — 每个模块的 API、测试、里程碑硬验收、运营控制)。
> 当工期/里程碑结构数字不一致时,**以 REFACTORING_PLAN.md §5 为准**
> (该文档经 2026-04-18 codex 六轮审计硬化)。

---

## 修订说明

本文档是对 v1.0 的**结构性重写**,不是增量更新。两者的关键区别:

- **v1.0 的定位**:项目管理文档 —— 包含 T1/T2/T3 目标分层、概率评估、期待管理、失败模式承诺、过程性指标等。假设研究者需要显式的目标阶梯和心理预期管理。
- **v3.0 的定位**:研究地图 —— 只包含问题陈述、方法、可验证的子问题序列。假设研究者由学术好奇心驱动,不需要外部期待管理。

**为什么修订**:v1.0 假设的驱动力(部分功利、需要阶段性激励)与研究者真实驱动力(纯粹学术好奇心,想要知道真相)不符。v1.0 的很多结构对好奇心驱动的研究无用甚至有害 —— 例如"T3 概率 < 5%"这类估计反复出现会制造不必要的噪音。

v1.0 历史归档,不再作为 active 文档。

**v3.0 → v3.1 的修改**:子问题列表从 5 个合并回 4 个(与 §1 主问题的原始 4 问对齐),但每个子问题的描述做了充分展开,保留了 v3.0 中 5 个 Sub-Q 的全部执行精度。结构更清晰,执行粒度不损失。

---

## 1. 主问题

**核心问题**:在无量子中继、无量子存储、使用离散变量载体的约束下,两方之间通过(至多一个)untrusted measurement relay 建立共享密钥的**信息论极限**是什么?

这个问题的答案有三种结构性可能:

- **情况 A**:$\sqrt{\eta}$ 标度是紧上界。TF-QKD 族达到了根本极限,无中继无存储 DV-QKD 的故事已经讲完
- **情况 B**:存在 $\eta^\alpha$($1/2 < \alpha < 1$)的上界,且这个上界可达。TF-QKD 之后还有空间,某种新协议结构能利用这个空间
- **情况 C**:存在 $\eta^\alpha$ 的上界但不可达。标度"空间"在数学上开着,但物理上关着

**真相属于哪种情况**是本项目的核心好奇对象。每一种情况都对应不同的后续研究图景,但每一种答案本身都是可验证的、可发表的、有意义的科学结论。

---

## 2. 问题的演化历史

这个主问题是经过多次精细化浮现的,理解它的演化能帮助日后工作中避免已走过的弯路:

**原始形式(项目起点)**:找到超越 TF-QKD 的新 QKD 协议。

**第一次精细化**:认识到"超越 TF-QKD"有多种意义。排除"超越 PLOB"(物理不可能,需要量子中继或存储)。聚焦于"在无中继无存储约束下,标度比 $\sqrt{\eta}$ 好"。

**第二次精细化**:认识到 AI 搜索只能在已定义的协议空间内寻找最优,不能自动发现"重新定义空间"的新物理机制(BB84→MDI→TF-QKD 每次跃迁的本质)。AI 作为工具被重新定位:**不是"产生洞察的主体",而是"辅助刻画问题结构的工具"**。

**第三次精细化**:认识到"找新协议"(构造性陈述)和"刻画极限"(刻画性陈述)在信息论上等价。如果紧上界是 $\sqrt{\eta}$,无新协议可找;如果紧上界是 $\eta^\alpha$ 且 $\alpha < 1/2$,新协议的方向自然浮现。**从"找"变为"刻画"不是目标降级,是问题的数学成熟化**。

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

**Phase 0 建设**。

### 5.2 有限密钥可组合率(GEAT)

基于 Metger-Fawzi-Sutter-Renner 2024 的广义熵积累定理。对任何 $\Pi$ 计算

$$\ell(\Pi, n, \varepsilon_{\text{sec}}, \varepsilon_{\text{corr}})$$

**Phase 1 建设**。

### 5.3 紧密钥率上界(协议族上界 SDP)

基于 Wilde-Tomamichel-Berta 2017 / Pirandola 2019 / Das-Khatri-Wilde 2020 的 relative entropy of entanglement 上界框架。对**协议族** $\mathcal{F}$(不是单个协议)计算

$$R_{\text{UB}}(\mathcal{F}, \eta, \text{topology}) \geq \sup_{\Pi \in \mathcal{F}} R^\infty(\Pi)$$

**Phase 2 主要建设对象**。这是刻画 gap 所需要的工具。

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

主问题通过以下四个子问题分解。每个子问题是可独立推进的研究单元,且对前置子问题的完成状态有依赖。

### Sub-Q1:MS-EB 框架能否统一表达无中继 DV-QKD 协议?(Phase 0 M1-M4)

**问题陈述**:MS-EB 五元组 $(\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 作为一个协议表达语言,是否能干净地涵盖 §3.1 约束内的全部主流 DV-QKD 协议?这个涵盖不仅是"语言层面能写",更重要的是能**自动派生**到评估工具所需的数学对象上。

具体需要回答:

**(a) 表达完备性**:BB84 及其变体(六态、SARG04、Efficient BB84)、MDI-QKD 及其变体、TF-QKD 及其变体(SNS-TF、PM-QKD、MP-QKD) —— 这七个主要协议族的各代表性协议,是否都能作为 MS-EB 五元组被严格书写?书写过程中是否暴露框架的裂缝?

**(b) 工具接口畅通**:给定一个 MS-EB 协议对象,能否自动派生出 WLC SDP 所需的联合态 $\rho_{AB}$、约束算符集 $\{\Gamma_k\}$、key map 的 Kraus 算符?派生过程无需针对每个协议手写代码。

**(c) 框架的对称性原生支持**:MS-EB 是否能原生携带协议的对称群信息?对称性降维是否能作为一等公民在 SDP 构造中自动生效?

**(d) 未覆盖区域的显式标记**:对框架覆盖不到的协议类型(如自适应改变 $\mathcal{E}$ 的协议),是否能在 MS-EB 元数据中显式标注 "out of scope",避免 AI 搜索或人工工作浪费在框架表达不了的结构上?

**验收产出**:

- 可运行的 Python 代码库 `qkdx/`,实现 MS-EB 框架和 WLC SDP 求解器
- 对七个主要协议族的五元组书写(code + 配套文档)
- M1-M4 的数值结果与文献对比(误差 < 1% 对 BB84/MDI,< 5% 对 TF/MP)
- 一份 `framework_coverage.md`,列出已覆盖协议 + 已知裂缝

**预计时长**:6-10 周(Phase 0 M1-M4)。

---

### Sub-Q2:在 MS-EB 框架下,已知协议族的紧密钥率下界是什么?(Phase 0-1)

**问题陈述**:Sub-Q1 建立了能表达和评估的工具。Sub-Q2 使用这个工具,对每个已知协议族做**系统的紧密钥率下界刻画** —— 不仅计算单个协议的密钥率,而是在协议族参数空间中找到 Pareto 最优,以及了解"这个协议族能达到多好"。

具体需要回答:

**(a) 协议族的参数化**:对每个协议族 $\mathcal{F}$(BB84 族、MDI 族、TF 族),在 MS-EB 下如何系统地参数化族内所有合法变体?参数包括:信号态选择、基矢概率、诱骗态强度、宣告规则细节、接受性测试阈值等。

**(b) 族内 Pareto 前沿**:对每个协议族,在 $(\eta, R)$ 平面上绘制**整个族能达到的 Pareto 前沿** —— 不是某个固定参数下的单曲线,而是参数自由选择下的上包络。这需要系统的数值优化(Bayesian optimization 或 CMA-ES 层级的搜索,不是完整 AI 搜索)。

**(c) 族间比较**:在相同 $\eta$ 下,BB84 族、MDI 族、TF 族的 Pareto 前沿如何排布?交叉点在哪里?TF 族的 $\sqrt{\eta}$ 可达率在 $\eta$ 多小的时候真正显著超越 BB84?

**(d) 有限密钥下的族刻画**:Phase 1 引入 GEAT 后,上述 Pareto 前沿在有限密钥场景(给定 $n, \varepsilon_{\text{sec}}$)下如何变化?哪些协议在渐近下最优但在有限密钥下退步?

**(e) 现实器件参数下的族刻画**:引入器件不完美参数(探测效率 $\eta_d$、dark count、基选偏置等)后,族的 Pareto 前沿变化如何?

**验收产出**:

- 每个协议族的 `family_sheet.md`,包含参数空间描述、Pareto 前沿数据、族间比较图
- 有限密钥修正下 Kamin 2025 的结果独立复现(误差 < 5%)
- 整合的 "DV-QKD 协议族地图" —— 一张图看清各族的定位和边界

**预计时长**:2-4 个月(跨 Phase 0 末到 Phase 1)。

---

### Sub-Q3:已知的上界工具在 MS-EB 框架下给出什么上界?(Phase 1-2)

**问题陈述**:主问题的答案取决于**上界** —— 如果紧上界是 $\sqrt{\eta}$,那 TF-QKD 已经最优;如果紧上界更大,gap 中有空间。这个子问题要把文献中已有的上界工具(PLOB 及其推广)**精读到骨头里**,然后**把它们应用到我们的拓扑**(两方 + untrusted relay + 纯损耗信道)。

这件事不是"套公式" —— PLOB 原始定理的陈述是单信道两方,不直接管我们的拓扑。需要做真正的工作来判断上界到底说了什么。

具体需要回答:

**(a) PLOB 精读**:完全理解 Pirandola-Laurenza-Ottaviani-Banchi 2017 的证明结构。识别每一个关键假设:信道是纯损耗玻色、两方之间的单一信道拓扑、relative entropy of entanglement 的可加性、teleportation simulation 的适用范围。每个假设对应证明的哪一步?每个假设在 "untrusted relay" 拓扑下是否仍然成立?

**(b) 网络拓扑推广**:Pirandola 2019 的 "End-to-end capacities of a quantum communication network" 把 PLOB 从单信道推广到一般网络。对 "两方 + 单中间测量站" 这个特定拓扑,该论文给出的是什么上界?证明技术是什么?

**(c) 替代证明路线**:Wilde-Tomamichel-Berta 2017 给了 PLOB 的独立推导(通过 squashed entanglement 或 other converse 技术)。这套推导对我们的拓扑能给出什么?Das-Khatri-Wilde 2020 的最新改进呢?

**(d) 上界的 MS-EB 表述**:把上述文献中的上界,重新陈述为"在 MS-EB 框架下,任何满足 §3.1 约束且具备特定拓扑特征的协议 $\Pi$ 必满足 $R(\Pi) \leq f(\eta)$"的形式。这个重新陈述是后续 Sub-Q4 的基础。

**(e) 上界 SDP 的实现**:对于协议族 $\mathcal{F}$,基于 relative entropy of entanglement 的凸优化能否给出可计算的数值上界?这是评估工具链的第三层(见 §5.3)。

**验收产出**:

- 一份 30-50 页的"上界接缝报告" `upper_bound_report.md`,精读四篇关键论文,逐条识别关键假设及其对我们拓扑的 bearing
- 上界 SDP 的初步实现(至少对简单信道)
- 对 "两方 + untrusted relay + 纯损耗信道" 拓扑,给出一个具体的、可数值计算的当前已知最紧上界 $R_{\text{UB}}^{\text{current}}(\eta)$

**预计时长**:3-5 个月(跨 Phase 1 末到 Phase 2 中)。

---

### Sub-Q4:上下界之间的 gap 是怎么结构化的?Gap 里能否构造新协议,或上界能否收紧?(Phase 2-3)

**问题陈述**:Sub-Q2 给出已知协议族的下界(Pareto 前沿),Sub-Q3 给出已知上界。两者之间的 gap 就是主问题真正的研究对象。这个子问题做 **gap 的结构分析** —— 不是简单的"gap 有多大",而是"gap 为什么这么大,gap 里能发生什么"。

具体需要回答:

**(a) Gap 的定量形状**:$\text{gap}(\eta) = R_{\text{UB}}^{\text{current}}(\eta) - R_{\text{LB}}^{\text{TF-QKD}}(\eta)$ 在 $\eta$ 的各区间是什么形状?渐近行为是什么?是不是在某个 $\eta$ 区间 gap 特别大?

**(b) Gap 的归因**:gap 的存在可以归因于三种原因之一或组合:

- **原因 A(上界松)**:当前证明技术保守,真正的紧上界可能更低。若如此,研究方向是**改进证明**(更精细的 relative entropy 分析、更好的 channel simulation、利用 untrusted relay 结构的新技术)。
- **原因 B(下界松)**:已知协议族不够好,存在 TF-QKD 族之外的协议能在 gap 中达到更高密钥率。若如此,研究方向是**构造新协议**(在 MS-EB 框架下的协议结构搜索)。
- **原因 C(上下都松)**:两边都有改进空间。gap 是两种松弛的叠加。

判定 gap 的真实归因需要对 (a) 的定量分析做结构化诊断。

**(c) 如果是原因 A**:尝试证明更紧上界。利用 Sub-Q3 精读中发现的证明"可收紧处" —— 比如 untrusted relay 的特殊性质是否能被上界证明利用?这是一个**数学工作**,不依赖物理洞察。

**(d) 如果是原因 B**:在 MS-EB 框架下系统地探索 TF-QKD 族外的协议结构。这里是 AI 搜索可以发挥作用的地方 —— **搜索目标由 gap 的位置指定**,不是盲目搜索。AI 在已定义的 MS-EB 空间中寻找"能占据 gap 的协议结构"。

**(e) 如果是原因 C**:两条线并行推进,看哪一边先能把 gap 压小。

**(f) 极限情形**:如果最终 $R_{\text{UB}}^{\text{refined}} = R_{\text{LB}}^{\text{best}} = c^* \sqrt{\eta}$ 对某个 $c^*$,那么**主问题答案是情况 A**($\sqrt{\eta}$ 是紧上界,TF-QKD 最优)。这是完全合法的结论,本身是重要结果。

**验收产出**:

- Gap 的结构化诊断报告 `gap_analysis.md`,给出对原因 A/B/C 的判断
- 根据判断结果:
  - 若 A:更紧上界的证明(哪怕只是收紧了一个前因子,也是成果)
  - 若 B:一个或多个可达 gap 中某点的新协议结构候选(在 MS-EB 中被严格表达、在 WLC SDP 下被严格评估)
  - 若 C:两个方向的阶段性产出
- 主问题的初步答案(情况 A / B / C 之一)

**预计时长**:6-12 个月(Phase 2 下半 + Phase 3),视 gap 归因决定具体工作量。

---

### 子问题间的逻辑关系

```
Sub-Q1 ──────── 建框架 + 工具
   │
   ▼
Sub-Q2 ──────── 用工具刻画已知协议族的下界
   │
   ▼
Sub-Q3 ──────── 理解已知上界工具 + 应用到我们的拓扑
   │
   ▼
Sub-Q4 ──────── 刻画 gap,诊断归因,做结论性工作
```

任何子问题如果产生了意外结果(例如 Sub-Q2 发现某个协议族的数值密钥率突破已知解析结果,或 Sub-Q3 发现某个上界证明在我们的拓扑下直接退化),子问题序列会相应调整,不严格按线性推进。

**Sub-Q1 和 Sub-Q2 覆盖 Phase 0 到 Phase 1,Sub-Q3 覆盖 Phase 1 末到 Phase 2 中,Sub-Q4 覆盖 Phase 2 下半到 Phase 3**。项目总时长预计 2-3 年,取决于 Sub-Q4 的归因和后续工作量。

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

### Phase 1(约 3-4 个月)

- GEAT 有限密钥层实现
- Sub-Q2 的完整 family sheets
- Sub-Q3 启动(PLOB 精读)
- 接受性测试 $\mathcal{T}$ 的系统化处理

### Phase 2(约 6-12 个月)

- 上界 SDP 工具链(Layer 5.3)
- Sub-Q3 完成
- Sub-Q4 启动

### Phase 3(12+ 个月)

- Sub-Q4 完成
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

- Winick, Lütkenhaus, Coles 2018, *Quantum* 2:77 — WLC SDP 主文
- George, Lin, Lütkenhaus 2021, *PRR* 3:013274 — 数值方法的 finite-key 扩展
- Metger, Fawzi, Sutter, Renner 2024, *Commun. Math. Phys.* 405:261 — GEAT
- Kamin, Arqand, George, Lütkenhaus, Tan 2025, *PRX Quantum* 6:020342 — 实用 finite-key

**可组合安全性**:

- Portmann, Renner 2022, *RMP* 94:025008 — AC 框架综述
- Renner 2005 PhD thesis — smooth entropy 原著

**上界理论**(Phase 1-2 阅读重点):

- Pirandola, Laurenza, Ottaviani, Banchi 2017, *Nat. Commun.* 8:15043 — PLOB 定理
- Pirandola 2019, *Commun. Phys.* 2:51 — 网络推广
- Wilde, Tomamichel, Berta 2017, *IEEE TIT* 63:1792 — PLOB 独立推导
- Khatri, Wilde 2020, arXiv:2011.04672 — *Principles of Quantum Communication Theory: A Modern Approach*(综合 converse bounds 的现代教科书;替代此前误引 "DKW 2020 arXiv:2012.03262",该 ID 实为不相关的热力学论文)
- Takeoka, Guha, Wilde 2014, *Nat. Commun.* 5:5235 — PLOB 的前身

**协议族原文**:

- Lo, Curty, Qi 2012, *PRL* 108:130503 — MDI-QKD
- Lucamarini et al. 2018, *Nature* 557:400 — TF-QKD
- Ma, Zeng, Zhou 2018, *PRX* 8:031043 — PM-QKD
- Zeng, Zhou, Wu, Ma 2022, *Nat. Commun.* 13:3903 — MP-QKD

**背景综述**(按需):

- Xu, Ma, Zhang, Lo, Pan 2020, *RMP* 92:025002 — 实用 QKD 综述
- Scarani et al. 2009, *RMP* 81:1301 — 经典 QKD 综述

---

## 文档管理

- **版本**:v3.1(2026-04-17)
- **前置**:v3.0(同日,仅 §6 结构差异)→ v1.0(同日,结构性重写)
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
- **v3.1**(2026-04-17):子问题序列从 5 个合并为 4 个。主要变更:
  - Sub-Q1 / Sub-Q2 保持结构,展开 (a)-(d) 子点 + "验收产出"小节
  - v3.0 Sub-Q3(PLOB 精读)与 v3.0 Sub-Q4(应用于拓扑)合并为 **v3.1 Sub-Q3**,展开 (a)-(e) 子点
  - v3.0 Sub-Q5(gap 刻画)成为 **v3.1 Sub-Q4**,展开 (a)-(f) 子点并明确归因 A/B/C + 极限情形
  - §8 Phase 2/Phase 3 的 "Sub-Q5 启动/完成" 统一改为 "Sub-Q4 启动/完成"(修复 v3.1 草稿残留)
  - 子问题逻辑图从 5 节点改为 4 节点
  - 头部/尾部版本号与关联文档小幅更新

---

*文档结束*
