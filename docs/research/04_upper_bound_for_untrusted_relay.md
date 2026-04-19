# Log 04:$\mathcal{T}_{\text{umr}}$ 上界的完整陈述

**日期**:2026-04-19
**子任务**:把 Log 02-03 的结果整合成 $\mathcal{T}_{\text{umr}}$ 拓扑上界的**单一完整陈述**,附带**可核查的假设清单**,可直接作为 PROSPECTUS Sub-Q3 验收产出的数学核心。

---

## A. 子问题

写出一条严格的定理,形式如 "在假设 H1-H_k 下,$\mathcal{T}_{\text{umr}}$ 任何协议满足 $R \leq f(\eta_A, \eta_B)$"。确定 $f$ 的精确形式与假设集合。

---

## B. 工作草稿

### B.1 定理陈述

**定理 4.1**(Upper Bound on $\mathcal{T}_{\text{umr}}$ Secret-Key Rate)

假设:

- **H1**(拓扑)系统包含 Alice、Bob 和**单一**中间节点 Charlie;Alice-Charlie 经由量子信道 $\mathcal{N}_A$(pure-loss bosonic,透过率 $\eta_A$),Charlie-Bob 经由 $\mathcal{N}_B$(pure-loss bosonic,透过率 $\eta_B$)。
- **H2**(Charlie 的能力)Charlie 可以做任何 local quantum operation(包括但不限于测量);Charlie 不拥有纠缠交换以外的中继功能(即不做 BDCZ 风格的 entanglement swapping with memory-based repeater)。
- **H3**(信任边界)Charlie **不可信**(与 Eve 等效);Alice 和 Bob 可信,Eve 可完全控制 $\mathcal{N}_A, \mathcal{N}_B$ 的环境。
- **H4**(协议自由度)Alice 和 Bob 可执行任意本地量子操作(含或不含量子存储,见 H5);两方间有无限带宽 authenticated classical channel。
- **H5**(无存储约束,PROSPECTUS §3.1 H2)Alice 和 Bob 的信号发送后不保留信号寄存器(per-round 信号制备)。
- **H6**(可组合安全)端到端密钥率 $R$ 由 Portmann-Renner 2022 可组合框架定义,IID collective attack + de Finetti 化简。

**结论**:

$$\boxed{R^\infty(\mathcal{T}_{\text{umr}}; \eta_A, \eta_B) \;\leq\; -\log_2\!\big(1 - \min(\eta_A, \eta_B)\big)}$$

特别地,对称情形 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$:

$$R^\infty(\mathcal{T}_{\text{umr}}^{\text{sym}}; \eta_{AB}) \;\leq\; -\log_2(1 - \sqrt{\eta_{AB}}) \;\approx\; 1.4427\sqrt{\eta_{AB}}\quad (\eta_{AB} \to 0)$$

**状态**(**v4/v5 修订**):**[SYN / CONJ]**(依赖 Log 02 Cmd 2.1 [THM] + Log 03 Cmd 3.1 [THM, Eq. (11)/(17)],但 untrusted-relay 继承 Log 03 Cmd 3.3-3.5 已降级为 [SYN / CONJ])

> **严重限界声明**:本定理的"上界可从 Pirandola 2019 min-cut 直接继承到 untrusted Charlie"的继承链**未升级到定理级**。Pirandola 2019 的严格 converse 针对 trusted / cooperative relay。对 untrusted relay 的上界继承依赖协议类族包含性("untrusted 协议 ⊆ trusted 协议,故 sup 单调 ≤"),这需要 Sub-Q3 Phase 2 严格化。

### B.2 证明整合(**v4/v5 修订**)

**Step 1**(**v5 补**):**包含关系**。$\mathcal{T}_{\text{umr}}$ 允许的协议集合 ⊆ Pirandola 2019 网络模型中 "Alice/Bob + 1 internal node with arbitrary LOCC-simulable operations" 允许的协议集合(因为后者允许 Charlie 做更强操作,untrusted Charlie 是更弱约束)。**此 Step 在文档层面的形式化尚缺,属 capacity monotonicity 的 [SYN 级继承]**。

**Step 2**:Log 03 Cmd 3.1(Pirandola19 **Eq. (11) single-path**,v4 修订后)给 min-cut $E_R$ upper bound(**single-path 是 max-over-cut**):

$$R^\infty \leq \min_C \max_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$$

**注(v4)**:原 Log 04 写的 `sum` 是 multi-path 版本(Eq. (17))。$\mathcal{T}_{\text{umr}}$ 是 linear single-path,cut 只含 1 条 edge,max 与 sum 数值相同,**但形式应统一为 Eq. (11)**。

**Step 3**:$\mathcal{T}_{\text{umr}}$ 的 cut 结构(Log 03 B.3)给 $\min_C \in \{C_1 = \{(A,C)\}, C_2 = \{(C,B)\}\}$,每个 cut 只含 1 条边,故

$$\min_C \max_{(i,j) \in C} E_R = \min(E_R(\Phi_{\mathcal{N}_A}), E_R(\Phi_{\mathcal{N}_B}))$$

**Step 4**:Log 02 Cmd 2.1 给 pure-loss 的 $E_R = -\log_2(1-\eta)$,故

$$\min(E_R) = -\log_2(1 - \min(\eta_A, \eta_B))$$

**Step 5**:H5(无存储)单调收缩自由度(Log 02 B.5 + Log 03 Cmd 3.6),不放松上界。

综合 Steps 1-5,得定理 4.1。**QED**(in 知识合成意义下)。

### B.3 证明中使用的所有外部定理清单

为方便 V2 文献交叉核查,列出依赖的外部定理:

1. **PLOB 主定理**:$E_R(\Phi_{\mathcal{N}_\eta}) = -\log_2(1-\eta)$ for pure-loss bosonic. 来源:PLOB17 Thm. 5.
2. **Pirandola 2019 network min-cut bound**:end-to-end $K^{\leftrightarrow}$ ≤ min-cut sum of $E_R$. 来源:Pirandola19 Thm. 2.
3. **LOCC-simulation of pure-loss**:$\mathcal{N}_\eta(\rho) = \mathcal{L}_{BK}(\rho \otimes \Phi_\eta)$. 来源:Niset-Fiurášek-Cerf 2009 / PLOB17 Eq. (4).
4. **Capacity 单调性 under 协议限制**:sup over smaller protocol set ≤ sup over larger set. 来源:capacity 定义 by Portmann-Renner 2022 + standard.

**所有四条都是 published theorems**,非猜测。V2 核查只需验定理号。

### B.4 定理 4.1 的"紧"性讨论(是否情况 A 还是情况 C)

定理 4.1 给出上界 $1.44\sqrt{\eta}$(对称,渐近)。**紧不紧**取决于是否存在 $\mathcal{T}_{\text{umr}}$ 协议达到这个 scaling(不一定是 prefactor)。

**Log 05 将证明 TF-QKD ∈ $\mathcal{T}_{\text{umr}}$ 且 $R_{\text{TF}} \sim c_{\text{TF}} \sqrt{\eta}$ for some $c_{\text{TF}} > 0$**。

若 $c_{\text{TF}} > 0$(非零常数,与 scaling 同级),则:

- Scaling $\sqrt{\eta}$ **achievable**(TF-QKD 构造性地达到这个 scaling)
- Scaling $\sqrt{\eta}$ **upper bound**(定理 4.1)

**两端 scaling 一致 ⇒ 情况 A 成立,scaling 层面**。**[待 Log 05 完成后锁定]**

### B.5 prefactor 层面的差距

- 定理 4.1 的 prefactor:$1.4427$
- TF-QKD 可达 prefactor $c_{\text{TF}}$:文献给的数值约在 $0.5 - 1.0$ 范围(视具体协议细节、诱饵态优化、探测器效率)

**prefactor gap $= 1.4427 - c_{\text{TF}} \sim O(1)$**,存在。这是情况 A 内的 "prefactor open" 部分,不是情况 B/C 的 evidence。

是否 prefactor gap 可以收窄?两个方向:

- **上界方向**:定理 4.1 用了 $E_R$,但对具体 network topology 可能有更紧的 $E_R$-free bound(如 TGW14 sub-additive,DKW20 improvements)
- **下界方向**:TF-QKD prefactor $c_{\text{TF}}$ 可能通过 optimization + 优化诱饵态 + 改进 post-processing 提高,但**不超过 $1.4427$**(因为定理 4.1 是硬上界)

两方向同时收敛到一个 $c^\star \in [c_{\text{TF}}, 1.4427]$ 的过程,就是 PROSPECTUS Sub-Q4 说的 "gap 刻画"。

### B.6 定理 4.1 的可疑之处(self-skepticism,为 V1 预备)

列出本定理可能**错**的地方,供 V1 逐条核查:

(i) **Pirandola19 Thm. 2 的精确范围**:它要求信道 LOCC-simulable。pure-loss bosonic 是,但 DV-QKD 的有限维近似是吗?—— 在足够大的 Fock 截断下 LOCC-simulation 成立(需要 V1 细看)。

(ii) **Charlie "untrusted" 的形式化**:Pirandola19 把 internal node 视作 Eve-controllable。在 $\mathcal{T}_{\text{umr}}$ 中,Charlie 公开经典宣告 —— 这经典宣告若被 Alice/Bob 正确使用,不算对 Alice/Bob 的安全性威胁,但若 Charlie 改宣告会 abort —— 这里需要核查 Pirandola19 对"untrusted"的精确定义(是否允许 untrusted node 广播经典信息)。这是 V2 的核心核查项。

(iii) **min-cut 的唯一性**:若 $\eta_A = \eta_B$ 恰好相等,min-cut 达于 $C_1$ 和 $C_2$ 两个;如果不对称,只取更小。定理陈述用 $\min$ 覆盖两种情形。

(iv) **H2 的 "无纠缠交换" 约束**:Pirandola19 默认允许内部节点做任何 LOCC-implementable 操作,纠缠交换是一种 LOCC(配合内部存储)。如果 Charlie **有量子存储**可以做纠缠交换,$\mathcal{T}_{\text{umr}}$ 就不是"无中继"了。H2 的表述要显式排除 memory-assisted relay。

**结论**:(i)(iii) 对定理陈述无威胁;(ii)(iv) 需要 V1/V2 详细核查。

---

## C. 本日志的已证命题(**v4/v5 修订后**)

**命题 4.1**(上界命题,v5 限界版)在 Log 04 §B.1 的 H1-H3 + H4 **放宽为 bosonic pure-loss** + H5 **放宽为 asymptotic collective attack** 下,

$$R^\infty(\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}; \eta_A, \eta_B) \leq -\log_2(1 - \min(\eta_A, \eta_B))$$

**[SYN / CONJ]**,依赖:
- Log 02 Cmd 2.1 [THM]:PLOB 点对点 pure-loss 的 $E_R$
- Log 03 Cmd 3.1 [THM, Eq. (11)]:Pirandola 2019 **single-path** min-cut(**v4 修订**,前 "sum + Thm. 2" 写法已更正)
- **untrusted-relay 继承** [SYN / CONJ]:capacity monotonicity 继承链未升级到定理级,是本命题降级的关键原因

> **明示**:本命题**不**覆盖 PROSPECTUS §3.1 原始 H4(finite-dim Fock)、H5(composable finite-key)、H6(DV)。仅在 §B.1 放宽后的 bosonic-asymptotic 子问题下有效。

**命题 4.2**(对称情形,**[SYN / CONJ]**)对称 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$ 时 $R^\infty \leq -\log_2(1 - \sqrt{\eta_{AB}}) \approx 1.44 \sqrt{\eta_{AB}}$. 继承命题 4.1 分级。

**命题 4.3**(scaling $O(\sqrt{\eta})$,**[SYN]**)在放宽版拓扑 + bosonic pure-loss channel 下,$\mathcal{T}_{\text{umr}}$ 上界的 scaling 最可能为 $O(\sqrt{\eta})$. 

**命题 4.4**(证明依赖的外部定理清单)命题 4.1 的证明**依赖** 3 条已发表定理 + 1 条未 lemma 化的 capacity monotonicity 直觉:

- [THM] PLOB 2017 pure-loss $E_R$
- [THM] Pirandola 2019 Eq. (11) single-path min-cut
- [THM] Niset-Fiurášek-Cerf 2009 LOCC-simulation
- **[SYN / CONJ]** untrusted-relay 协议类族 ⊆ trusted-relay 协议类族 → capacity 单调继承

**[元元命题]**:本日志的综合结论分级为 **[SYN / CONJ]**,**非 [COROLLARY]**(v1 误分级,v4/v5 降级)。

---

## D. 下一步依赖

Log 05:TF-QKD / MP-QKD 的可达速率,重点是

- TF-QKD prefactor $c_{\text{TF}}$ 的具体数值(理论 + 实验实现)
- 可达速率的 scaling 为 $\sqrt{\eta}$ 的证据

Log 05 完成后,Log 06 做 gap 结构分析,FINDINGS_DRAFT 出结论。

---

*Log 04 结束*
