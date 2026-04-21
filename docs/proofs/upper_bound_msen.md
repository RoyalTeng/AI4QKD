# 上界在 MS-EB 框架下的重新陈述（U3.6）

**版本**：v0.1
**日期**：2026-04-21 autonomous session
**对应**：RESEARCH_PLAN §4.3 U3.6 研究动作
**严谨性分级**：所有命题**显式分级**为 [THM] / [COROLLARY] / [CONJ] / [UNKNOWN]（Log 07 标准 + FINDINGS v2 §1.2 严格继承）

---

## 0. 文档定位

本文档把 PLOB 2017 / Pirandola 2019 / WTB 2017 / TGW 2014 / Khatri-Wilde 2024 等文献给出的**上界定理**，在本项目 **MS-EB 框架**（PROSPECTUS §4）下统一重写为：

> 对任意满足 §3.1 硬约束 H1-H6 且具备 "两方 + 单 untrusted measurement relay + 纯损耗 bosonic 信道" 拓扑（简记 $\mathcal{T}_\text{umr}$）的协议 $\Pi \in \mathcal{F}_\text{MS-EB}$，$\Pi$ 的可达密钥率 $R(\Pi)$ 满足

$$R(\Pi) \leq f(\eta_A, \eta_B)$$

其中 $f$ 是具体的、可数值计算的函数。

**坦白**：本文档整合文献 SDP-可计算上界，但**严格归属（inheritance）到 umr 拓扑**尚未完整走完理论级证明。大部分命题分级为 **[CONJ]** 或 **[COROLLARY under assumption X]**，**不升级到 [THM]**。真正的 [THM] 级工作需要用户亲自完成（见 Log 07 §3 三条路径）。

---

## 1. 文献定理索引（原始拓扑 + 原始分级）

| 文献定理 | 原始陈述 | 原始拓扑 | 本项目继承状态 |
|---|---|---|---|
| PLOB 2017 Eq. 19 | $C_\text{loss}(\eta) = -\log_2(1-\eta)$ bosonic pure-loss | 两方直连（单信道） | [THM for original] → [CONJ for umr] |
| Pirandola 2019 Eq. 9 | $C_\text{loss,chain}(\eta, N) = -\log_2(1-\eta^{1/(N+1)})$ | N 内部 **trusted** repeater | [THM for trusted-relay] → [CONJ for umr] |
| WTB 2017 Thm 26 | $R \leq E_R(\mathcal{N})$ 对 tele-simulable | 两方直连 | [THM for original] → [CONJ for umr] |
| TGW 2014 Eq. 1 | $R \leq \log_2\frac{1+\eta}{1-\eta}$ pure-loss squashed-E | 两方直连 | [THM] → [COROLLARY under tele-sim inheritance] |
| Khatri-Wilde Thm 19.4 | $\log_2 M \leq \frac{n E_\text{sq}(\mathcal{N}) + g_2(\sqrt\varepsilon)}{1-\sqrt\varepsilon}$ | LOCC-assisted 两方 | [THM for LOCC] → [CONJ for umr] |
| Khatri-Wilde Thm 19.8 | $\log_2 M \leq n R_\max(\mathcal{N}) + \log_2\frac{1}{1-\varepsilon}$ | LOCC-assisted 两方 | [THM for LOCC] → [CONJ for umr] |

关键观察：**所有上述定理原始拓扑都是"两方 + trusted / LOCC-共有的 relay"**；**没有一个直接适用于 umr（Eve 控 Charlie）**。继承 lemma 是 Sub-Q3 理论工作的核心。

---

## 2. MS-EB 框架下的拓扑陈述

### 2.1 定义（Topology-typed protocol class）

**定义 2.1**（`T_umr` 拓扑类）
设 $\Pi = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 是 MS-EB 五元组。称 $\Pi$ 属于 $\mathcal{T}_\text{umr}$ 拓扑当且仅当：

- **T1**（两方 + 一中继）：$\mathcal{P} = \{A, B\}$（两个 source parties），$\mathcal{E}$ 在 A 和 B 之外包含唯一的 **measurement relay** Charlie
- **T2**（纯损耗信道）：Alice-Charlie 之间是 pure-loss bosonic $\mathcal{N}_A$（透射率 $\eta_A$），Charlie-Bob 之间 $\mathcal{N}_B$（透射率 $\eta_B$）
- **T3**（untrusted Charlie）：Charlie 的量子操作 $\mathcal{E}_\text{Charlie}$ 由 Eve 控制；Charlie 的测量结果通过 classical announcement $\mathcal{A}$ 分发
- **T4**（MS-EB 硬约束 H1-H6 满足）：$|\mathcal{P}| \in \{1, 2\}$ (H1), 无量子存储 (H2), 设备刻画信任 Level 1-3 (H3), Fock 截断 $N_\text{cut}$ (H4), Portmann-Renner 可组合安全 (H5), 离散变量载体 (H6)

**严谨性**：[SYN] —— 本定义把文献与项目术语对齐，不涉及定理陈述

### 2.2 拟重写定理陈述（template）

**Template 2.2**（待填的上界陈述模板）

对任意 $\Pi \in \mathcal{T}_\text{umr}$：

$$R_\varepsilon(\Pi, n) \leq f_\text{UB}(\eta_A, \eta_B, n, \varepsilon)$$

其中 $f_\text{UB}$ 是某个具体的闭合形式（如 $-\log_2(1-\sqrt{\eta_A \eta_B})$ 或 $n \cdot R_\max(\mathcal{N}_\text{eff})$）。

---

## 3. 候选上界陈述

### 3.1 候选 A：PLOB on single edge + data-processing（路径 γ）

**陈述 3.1**（Log 07 §3.3 路径 γ，形式化候选）

对 $\Pi \in \mathcal{T}_\text{umr}$，若以下 **Assumption DP** 成立：

> **Assumption DP**（data-processing on umr relay）：Eve 对 Charlie quantum register 的任意 local operation + classical announcement 不增加 Alice-Bob Hilbert space 上的 entanglement-assisted capacity。

则：

$$R(\Pi) \leq C_\text{PLOB}(\eta_A, \eta_B) := -\log_2(1 - \min(\eta_A, \eta_B))$$

**证明骨架**：
1. 忽略 Alice-Charlie-Bob 中某一段"最强"的链路（保留较弱一段）
2. 对保留一段应用 PLOB 2017 Eq. 19：$R \leq -\log_2(1 - \eta_\text{worst})$
3. Assumption DP 保证忽略另一段和 Charlie 的操作不增 capacity

**严谨性分级**：**[CONJ under Assumption DP]**
- Assumption DP 尚未形式化证明；这正是 Log 07 提到的"[UNKNOWN]"
- 若 Assumption DP 能升级为 [THM]（用户的纸笔工作），则本命题升级为 [COROLLARY]

**Sub-Q4 bearing**：若本陈述升级为 [THM]，则对 umr 拓扑，$f_\text{UB}(\eta) = -\log_2(1-\min(\eta_A, \eta_B))$，可以直接做 gap 定量分析。

### 3.2 候选 B：Pirandola 2019 chain-stretch 继承（路径 β）

**陈述 3.2**（Log 07 §3.2 路径 β，形式化候选）

若 Charlie 能做任意 LOCC 但**不能** entanglement swap with memory，则 Charlie-Bob segment 可视为 effective channel $\mathcal{N}_\text{eff} = \mathcal{N}_B \circ \text{(trace-out Charlie)}$，应用 Pirandola 2019 Eq. 9 at $N=1$：

$$R(\Pi) \leq C_\text{Pir,N=1}(\eta_A \eta_B) = -\log_2(1 - \sqrt{\eta_A \eta_B})$$

**严谨性分级**：**[CONJ]**
- Pirandola 2019 原始模型 Charlie 是 trusted；继承到 untrusted 需要 Charlie 的 LOCC 能力**保守化**
- Log 07 §3.2 认为这条路径"中风险"

### 3.3 候选 C：Khatri-Wilde max-Rains 的 umr 继承（路径 α）

**陈述 3.3**（待完全形式化）

若 Charlie 操作可被 subsume 在 Alice-Bob LOPC 之内（monotonicity reduction），则 Thm 19.8 给出：

$$\log_2 M \leq n \cdot R_\max(\mathcal{N}_\text{eff}) + \log_2\frac{1}{1-\varepsilon}$$

其中 $\mathcal{N}_\text{eff}$ 需要通过 Log 07 路径 α 的三条 lemma（协议嵌入 + 安全归约 + rate 定义对接）定义。

**严谨性分级**：**[UNKNOWN]** — 等待 Log 07 路径 α 的形式化

---

## 4. 数值化的上界候选（Layer 5.3 SDP）

对于任意"效应"信道 $\mathcal{N}_\text{eff}$（从某条候选路径得出），可用 `qkdx/numerics/upper_bound.py` 的工具数值给出上界：

### 4.1 E_R^PPT upper bound（已实施，U3.7）

$$R(\Pi) \leq E_R^\text{PPT}(\mathcal{N}_\text{eff}) = \inf_{\sigma \in \text{PPT}} D(\rho_{\mathcal{N}_\text{eff}} \| \sigma)$$

**严谨性分级**：
- 对 2⊗2 系统：[COROLLARY under candidate A/B/C + 2-qubit reduction]
- 对高维：**PPT 上界可能超过 SEP** → [COROLLARY for upper bound only]

### 4.2 max-Rains SDP upper bound（待实施）

Wang-Duan 2016b formulation：

$$R_\max(\mathcal{N}) = \log_2 \min \left\{\|T_{R'B} + T_{R'B}'\|_\infty : T_{R'B} \geq 0, T_{R'B} \geq \rho^{\mathcal{N}}_{RB}\right\}$$

配合 Khatri-Wilde Thm 19.8（strong converse）：

$$\log_2 M \leq n R_\max(\mathcal{N}_\text{eff}) + \log_2\frac{1}{1-\varepsilon}$$

**严谨性分级**：**[CONJ]** —— 同候选 A/B/C 的未完成状态

### 4.3 TGW squashed-E bound（解析）

PLOB pure-loss 的 TGW 上界 $\log_2\frac{1+\eta}{1-\eta}$ 总成立（因 E_sq 对 tele-simulable 单调），但**比 PLOB/Rains 松 2×**。作为 sanity check 保留。

---

## 5. 数值 gap 准备

有了 §4 的候选数值上界，可以配合 PHASE1_REPORT.md §2 的 Pareto 下界做 gap 定量：

$$\text{gap}(\eta_A, \eta_B) = f_\text{UB}(\eta_A, \eta_B) - R_\text{LB}^\text{TF-family}(\eta_A, \eta_B)$$

这是 G4.1（Sub-Q4 §5.1）的输入，**前置条件**是 §3 候选上界至少有一条升级到 [COROLLARY]。

**当前状态**：
- 三候选路径 α/β/γ 都在 [CONJ] 级
- G4.1 可以"带 [CONJ] 标签"地算 gap 形状，但数值结论严格不能升级到 [THM] 级结论

---

## 6. 验收对照（RESEARCH_PLAN §4.3）

| 验收项 | 要求 | 本文档状态 |
|---|---|---|
| $f(\eta)$ 是具体的可数值计算表达式 | 硬 | ✅ §3 给了三个候选 + §4 数值 API |
| 独立 sanity check | 硬 | ⏳ 数值上 E_R^PPT 与 PLOB analytical 已 cross-check (U3.7 tests); candidate-path 形式化待 Log 07 |
| **理论级 inheritance lemma** | 硬 | ❌ [CONJ] 级,**需要用户的纸笔工作** |

**承认**：本 U3.6 文档的理论 rigor 被"候选路径 α/β/γ 都还在 [CONJ] 级"限制。这是 Phase 2 剩余的**最硬单元**。

---

## 7. 下一步

1. **用户的理论工作**：Log 07 §3 路径 γ 的三条 data-processing lemma 形式化（推荐先做）
2. **我的数值工作**（已/将做）：
   - ✅ `qkdx/numerics/upper_bound.py` E_R^PPT SDP (U3.7, commit a7b1d9b)
   - ⏳ max-Rains SDP 扩展（U3.7 后续）
   - ⏳ G4.1 gap 数值图（带 [CONJ] 标签；候选 A/B/C 各画一条）
3. **U3.8 综合报告**：把 PLOB/Pir/WTB/TGW/Khatri-Wilde 5 份 memo + 本 U3.6 + Log 07 + 数值 U3.7 合成 30-50 页

---

## 8. 严谨性守则

本文档在**无例外**地遵循以下红线（FINDINGS v2 §1.2 + Log 07 §3.4）：

- **不把 [CONJ] 命题引用为 [THM]**
- **不越权把放宽版本的结论扩展到原始 H1-H6 版本**
- **承认 assumption DP / monotonicity reduction 尚未形式化**
- **Sub-Q4 归因不以本文候选上界为"最终 $f_\text{UB}$"的预判**（只作 gap 分析的 conditional 输入）

---

## Changelog

- **v0.1**（2026-04-21 autonomous session）：首版 MS-EB 上界重写，含三候选路径 α/β/γ 的形式化模板 + 数值 Layer 5.3 接入点
