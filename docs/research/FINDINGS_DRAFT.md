# FINDINGS_DRAFT — 初稿,未经 Phase V 验证

> **⚠️ 本文件是 DRAFT,不是最终答案。必须经过 V1-V4 四轮验证后才允许 rename 为 `FINDINGS.md` 作为最终答案。本文件内容在验证过程中**随时可能被驳回或修订**。**

---

**日期**:2026-04-19(Phase R 完成日)
**作者**:Claude Opus 4.7 协作工作,基于 docs/research/01-06 推理链
**评审路线**:→ V1(逻辑自审) → V2(文献交叉) → V3(反例搜索) → V4(codex 独立)→ FINAL

---

## 0. TL;DR

**对 PROSPECTUS.md v3.1 §1 的主问题,基于当前文献的 [COROLLARY] 级分析,答案是情况 A。**

**Scaling 结论**:在 $\mathcal{T}_{\text{umr}}$(两方 + 至多一个 untrusted measurement relay + pure-loss bosonic)拓扑下,渐近 secret-key rate 上界

$$R^\infty \leq 1.4427\sqrt{\eta_{AB}} + O(\eta_{AB}), \qquad \text{对称 } \eta_A = \eta_B$$

TF-QKD 族达到 $R \sim 0.3 \sqrt{\eta_{AB}}$,scaling 同阶。**scaling 层面 $\sqrt{\eta}$ 紧,情况 A 成立**。

**Prefactor 开放**:上界 prefactor $1.4427$ 与最好已发表可达 $\sim 0.3$ 之间有 $\sim 1.14$ 的 gap,属情况 A 内的子问题,为 Phase 2-3 研究内容。

---

## 1. 主问题答案

### 1.1 正式陈述

> PROSPECTUS.md v3.1 §1 主问题:在无量子中继、无量子存储、使用离散变量载体的约束下,两方之间通过(至多一个)untrusted measurement relay 建立共享密钥的**信息论极限**是什么?

**答案**:

### 情况 A 成立(scaling 层面,[COROLLARY] 级确定性)

- 上界:$R^\infty(\mathcal{T}_{\text{umr}}; \eta_A, \eta_B) \leq -\log_2(1 - \min(\eta_A, \eta_B))$
- 对称拓扑渐近:$R^\infty \leq 1.4427\sqrt{\eta_{AB}} + O(\eta_{AB})$
- 下界(构造性):TF-QKD / PM-QKD / MP-QKD 达到 $R \sim c\sqrt{\eta_{AB}}$,$c \in [0.1, 0.4]$
- Scaling gap $= 0$

### 情况 B、C 被排除([COROLLARY] 级)

- 情况 B($\eta^\alpha$, $\alpha < 1/2$ 可达)与定理 4.1 矛盾
- 情况 C($\eta^\alpha$, $\alpha < 1/2$ 上界)同样矛盾

---

## 2. 支持证据链

### 2.1 [THM] 级外部定理(定理 4.1 的依赖)

- **PLOB 主定理**(Pirandola-Laurenza-Ottaviani-Banchi 2017,Nat. Commun. 8:15043,Thm. 5):$K^{\leftrightarrow}(\mathcal{N}_\eta) = -\log_2(1-\eta)$ for pure-loss bosonic。详见 [Log 02](02_plob_dissection.md) 命题 2.1。

- **Pirandola 2019 网络 min-cut bound**(Commun. Phys. 2:51,Thm. 2):LOCC-simulable 网络上的 $K^{\leftrightarrow}_{s,t} \leq \min_C \sum_{(i,j) \in C} E_R$。详见 [Log 03](03_network_extension.md) 命题 3.1。

- **LOCC-simulation of pure-loss**(Niset-Fiurášek-Cerf 2009 + PLOB17 Eq. 4):pure-loss 信道可由 LOCC + Choi state 模拟。详见 [Log 02](02_plob_dissection.md) B.3 Step 1。

- **TF-QKD 可达 $\sqrt{\eta}$**(Lucamarini et al. 2018,Nature 557:400,Eq. 2-3 + Fig. 2):构造性给出 $R \sim c\sqrt{\eta}$。详见 [Log 05](05_achievable_rates_tfqkd.md) 命题 5.2。

### 2.2 [COROLLARY] 级推论(本研究合成)

- **定理 4.1**(Log 04 核心结论):$R^\infty(\mathcal{T}_{\text{umr}}; \eta_A, \eta_B) \leq -\log_2(1 - \min(\eta_A, \eta_B))$. 由 §2.1 前三条外部定理组合而得。

- **对称情形 scaling**(Log 04 命题 4.2-4.3):对称下 $R^\infty \leq 1.4427 \sqrt{\eta_{AB}}$. 直接展开。

- **情况 B 排除**(Log 06 命题 6.2):由定理 4.1 的 scaling $O(\sqrt{\eta})$ 强制 $\alpha \geq 1/2$,与情况 B 要求 $\alpha < 1/2$ 矛盾。

- **情况 C 排除**(Log 06 命题 6.3):同样机制。

- **情况 A 成立**(Log 06 命题 6.4):scaling 上下界同阶。

### 2.3 [SYN] 级信息(须后续验证)

- Prefactor gap $\approx 1.14$(Log 06 命题 6.5)— 归因 γ(两端都松)为初步判断,细节待 Phase 2-3 的 Sub-Q4 归因分析。

- DKW20 / TGW14 替代 converse bound 在 $\mathcal{T}_{\text{umr}}$ 下不给更紧的 scaling,与定理 4.1 定性一致(Log 03 B.7-B.8)。

---

## 3. 已排除的风险

- **scaling 错误**:若某个 $\mathcal{T}_{\text{umr}}$ 协议达到 $R > c \sqrt{\eta}$(scaling 更好),会驳回定理 4.1。**目前文献中无此结果** —— TF/PM/MP 均为 $\sqrt{\eta}$。V3 做反例搜索再确认。

- **拓扑曲解**:$\mathcal{T}_{\text{umr}}$ 的定义是否精确匹配 PROSPECTUS §1?已在 [Log 01 §A](01_setup_and_literature_map.md#A-本日志的子问题) 显式对齐 PROSPECTUS §3.1 H1-H6。

- **"untrusted"正当形式**:Pirandola19 的 untrusted 定义是否等同于 PROSPECTUS §3.1 H3?Log 04 B.6 (ii) 识别为需要 V2 核查的关键点。

---

## 4. 剩余开放问题(Phase 2-3 工作)

情况 A 内部的开放子问题(Log 06 B.6):

### 4.1 A1 — 对称 prefactor 紧值 $c^\star$

当前区间 $[0.3, 1.4427]$。确定 $c^\star$ 需要:

- **上界方向**:$\mathcal{T}_{\text{umr}}$-specific converse(比 PLOB min-cut 紧)。可能 approach:利用 Charlie 必须 broadcast classical outcome 这一 constraint,构造更细的 entanglement measure,收窄 $1.4427$。—— **Sub-Q3 Phase 2 工作**。
- **下界方向**:Pareto 优化 TF-QKD / PM-QKD / MP-QKD 参数空间;探索新的 signal format。—— **Sub-Q2 Phase 0-1 工作**。

### 4.2 A2 — 不对称 $\eta_A \neq \eta_B$

上界已给(定理 4.1 用 $\min$);下界 prefactor 在不对称情形的表达未知(TF-QKD 原论文默认对称)。

### 4.3 A3 — 非 pure-loss 噪声修正

加入相位噪声、探测器效率、dark count 后,$E_R$ 的解析值不再是 $-\log_2(1-\eta)$。上下界 scaling 预期仍 $\sqrt{\eta}$,prefactor 下调。**Sub-Q3 Phase 2** 要做严格化。

### 4.4 A4 — finite-key 修正

Kamin 2025 对 decoy-state BB84 给 finite-key 分析;对 $\mathcal{T}_{\text{umr}}$ 协议(TF-QKD 等)的 GEAT-based finite-key 尚缺。**Sub-Q2/Sub-Q3 Phase 1** 工作。

### 4.5 A5 — non-IID 攻击

Metger 2024 GEAT 适用性在 $\mathcal{T}_{\text{umr}}$ 下应成立(MS-EB 框架天然兼容 NSP)。待 Phase 1 GEAT 实现验证。

---

## 5. 对 PHASE0_M1 的即时行动建议

**本研究不改变 PHASE0_M1** 的计划,但给出 **clarity-increasing notes**:

### 5.1 Sub-Q1 的验收重点

M1–M4 的任务是"框架能表达 + WLC SDP 能评估"——上述情况 A 结论表明:在 $\mathcal{T}_{\text{umr}}$ 下,**WLC SDP 可达 $\sqrt{\eta}$ scaling 的下界是正确的**,与文献一致;M4B 验收 "log-log 斜率 = 0.5 ± 0.05" 应该能通过。

### 5.2 Sub-Q3 的工作重心

由 §4.1 A1 分析,Sub-Q3 Phase 2 "上界精读" 的**重点不是重推 PLOB scaling**(已确定 $\sqrt{\eta}$),而是 **$\mathcal{T}_{\text{umr}}$-specific prefactor converse**。

### 5.3 Sub-Q4 归因诊断的简化

PROSPECTUS §6 Sub-Q4 (b) 的归因 A/B/C 可简化为:

- **α(上界松)**:Phase 2-3 具体工作(改进 converse)
- **β(下界松)**:Sub-Q2 Pareto 优化的一部分
- **γ(两端都松)**:初步判断,需要 A1 工作细化

### 5.4 文档引用的一致性建议

REFACTORING_PLAN §5 M4B 验收条件 "TF-QKD 的 R(η) log-log 斜率 = 0.5 ± 0.05" 与本研究主结论一致。M4B 的 qkdx/protocols/tfqkd.py 实现若能稳定产出此斜率,即验证本 FINDINGS 的 scaling 层。

---

## 6. 诚信红线

**本 FINDINGS_DRAFT 严格遵循 PROSPECTUS §9 + RESEARCH_PLAN §9 的诚信承诺**:

1. **定理追溯**:所有 [THM] 级引用(PLOB17 Thm. 5,Pirandola19 Thm. 2,Lucamarini18 Eq. 2-3)均可追溯到已发表论文与具体定理/方程号。V2 交叉核查负责验证。

2. **分级标注**:[THM] / [COROLLARY] / [SYN] / [CONJ] 四级分明;情况 A 结论依赖 [THM] + [COROLLARY] 级证据,不依赖 [CONJ]。

3. **不宣称新定理**:本 FINDINGS 的数学内容**完全是已发表结果的合成**,不包含新证明。"情况 A 成立"的陈述等价于"$\sqrt{\eta}$ 是紧 scaling",这在 TF-QKD 社区已是共识,我们只是**把共识写成 PROSPECTUS 主问题答案的严格形式**。

4. **限界声明**:prefactor 层面的精确值 $c^\star$ **未在本研究中确定**,只给出区间 $[0.3, 1.4427]$。任何更紧数值须在 Phase 2-3 实际推导。

5. **AI 协助范围**:本 FINDINGS_DRAFT 由 Claude Opus 4.7 基于训练语料中的 QKD 文献共识合成。所有引用须由人类研究者核对原文(V2 任务);未核对的定理号标 [?] 或在 V2 中补注。

---

## 7. 前置验证(进入 V1 前的自检)

### 7.1 逻辑链完整性

- [x] Log 01 立拓扑定义
- [x] Log 02 立 PLOB 点对点
- [x] Log 03 立 Pirandola19 网络推广
- [x] Log 04 整合得上界(定理 4.1)
- [x] Log 05 立 TF-QKD 下界
- [x] Log 06 立 gap 结构(scaling gap = 0,情况 A)

### 7.2 与 PROSPECTUS 定义的对齐

- [x] $\mathcal{T}_{\text{umr}}$ 的 H1-H6 严格映射 PROSPECTUS §3.1 的硬约束
- [x] 情况 A/B/C 的判定条件严格按 PROSPECTUS §1 定义

### 7.3 诚信标注

- [x] 所有定理标 [THM] + 论文/定理号
- [x] 所有推论标 [COROLLARY] + 依赖链
- [x] 所有合成标 [SYN] 且不进最终答案的核心
- [x] 所有猜测标 [CONJ] 且显式标为"待 V3 核查"

---

## 8. Phase V 启动条件

本 FINDINGS_DRAFT 现在满足进入 Phase V 的条件。下一步:

- **V1** 逻辑自审(必做)
- **V2** 文献交叉(必做)
- **V3** 反例搜索(必做)
- **V4** codex 独立评审(必做)

任何一轮发现 BLOCKER,回到 Phase R 修订。全部 PASS 后,rename 为 `FINDINGS.md`。

---

*FINDINGS_DRAFT 结束。进入 Phase V。*
