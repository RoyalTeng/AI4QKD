# FINDINGS — 最终结论

**文档状态**:经 Phase R(Log 01-06)+ Phase V(V1-V4)全部通过,作为本轮研究的最终答案。
**日期**:2026-04-19
**作者**:Claude Opus 4.7,literature-informed analysis

**⚠️ 诚信声明**:本 FINDINGS 是**对 PROSPECTUS v3.1 §1 主问题的 literature-informed 分析**,**不是新定理**。所有核心结论依赖已发表文献(PLOB17, Pirandola19, Lucamarini18 等)。最高确定性级别为**条件化 COROLLARY**,具体条件见 §1.2。

---

## 0. TL;DR

**PROSPECTUS.md v3.1 §1 主问题 — 关于 $\mathcal{T}_{\text{umr}}$(两方 + 至多一个 untrusted measurement relay + pure-loss bosonic + no quantum memory)渐近 secret-key rate 信息论极限 — 的答案是:**

### 情况 A(scaling 层面),条件化 COROLLARY 级

在 **asymptotic collective attack + pure-loss bosonic channel + 单 untrusted measurement relay + no quantum memory** 假设下,

$$R^\infty(\mathcal{T}_{\text{umr}}^{\text{sym}}; \eta_{AB}) \;\leq\; -\log_2(1-\sqrt{\eta_{AB}}) \;\approx\; 1.4427\,\sqrt{\eta_{AB}}\quad (\eta_{AB} \to 0)$$

且 TF-QKD / PM-QKD / MP-QKD 族**已构造性达到** $R \sim c\sqrt{\eta_{AB}}$,$c \in [0.1, 0.4]$。

**Scaling gap = 0** $\Rightarrow$ $\sqrt{\eta_{AB}}$ 是 scaling 级紧上界 $\Rightarrow$ **情况 A 成立**。

**情况 B、C 均被排除**(见 §1.3 两种解读下的论证)。

**Prefactor 开放**:$c^\star \in [0.3, 1.4427]$,精确值属 Phase 2-3 研究内容。

---

## 1. 主问题答案

### 1.1 正式陈述

令 $\mathcal{T}_{\text{umr}}$ 为 PROSPECTUS §3.1 硬约束 H1-H6 定义的拓扑类族(见 [Log 01 §A](01_setup_and_literature_map.md) 的精确定义)。在对称 pure-loss 假设下 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$,设 $R^\infty$ 为渐近 secret-key rate。

**定理**(条件化 COROLLARY,v4 审后):

$$R^\infty(\mathcal{T}_{\text{umr}}^{\text{sym}}; \eta_{AB}) \;\leq\; -\log_2(1 - \sqrt{\eta_{AB}})$$

且存在 $\mathcal{T}_{\text{umr}}$-class 协议(TF-QKD 族)使 $R \geq c \sqrt{\eta_{AB}}$ for $c > 0$。故**scaling gap = 0**,**情况 A 成立**。

### 1.2 "条件化 COROLLARY" 的含义(v4 精化)

**本结论的确定性分级为 "条件化 COROLLARY"**,比 FINDINGS_DRAFT 的 [COROLLARY] 下调半档,条件如下:

(C1) **定理号条件**:
- PLOB17 主结果号码 **最可能 Thm. 5**,codex V4 memory 独立支持(**[LIKELY]**)
- Pirandola19 min-cut 应引用 **Eq. (11)(single-path)** 或 **Eq. (17)(multi-path)**,不引具体 Thm 号(codex V4 建议)
- 具体定理号的最终核对是 PROSPECTUS §6 Sub-Q3 Phase 2 的工作(30-50 页精读报告)

(C2) **PROSPECTUS 约定条件**:
- PROSPECTUS §1 情况 B "$1/2 < \alpha < 1$" 字面与物理直觉("比 $\sqrt{\eta}$ 更好"通常对应 $\alpha < 1/2$)不一致
- 本 FINDINGS 在两种读法下均给出排除论证(见 §1.3)
- 若 PROSPECTUS 原作者确认 $\alpha$ 方向,确定性可提升至 [COROLLARY]

(C3) **技术范围条件**:
- Scaling gap = 0 在 **asymptotic + pure-loss + 单中继** 假设下成立
- finite-key 修正、非 IID 攻击、noisy channel 作为**外推风险**单列,不保 finite-key 下 scaling 仍 $\sqrt{\eta}$(虽然直觉期望如此)

### 1.3 情况 B、C 的排除(两种 α 读法均排除)

**读法 A(PROSPECTUS 字面 $\alpha \in (1/2, 1)$)**:

- 情况 B 要求 "$\eta^\alpha$ 上界可达,$\alpha > 1/2$",等价 rate $\lesssim \eta^\alpha < \sqrt{\eta}$
- 但 TF-QKD 已构造性达到 $R \geq c\sqrt{\eta}$(Lucamarini18 [VERIFIED in V2])
- 矛盾 $\Rightarrow$ 情况 B 不成立
- 情况 C "$\eta^\alpha$ 上界但不可达" 需 $\eta^\alpha$ 上界比 $\sqrt{\eta}$ **更紧**,即 $<\sqrt{\eta}$ — 但 TF-QKD 已达 $\sqrt{\eta}$,任何紧于 $\sqrt{\eta}$ 的上界与 TF-QKD 矛盾 $\Rightarrow$ 情况 C 不成立

**读法 B(物理直觉 $\alpha \in (0, 1/2)$,"比 $\sqrt{\eta}$ 更好 scaling")**:

- 情况 B 要求 "$\eta^\alpha$ 上界可达,$\alpha < 1/2$",等价 rate $\gtrsim \eta^\alpha > \sqrt{\eta}$
- 由定理 4.1(Log 04)上界 $1.44\sqrt{\eta}$,无协议能达到 $> \sqrt{\eta}$ $\Rightarrow$ 情况 B 不成立
- 情况 C 同理由上界排除

**结论**:**无论 PROSPECTUS 作者 $\alpha$ 的意图是哪种,情况 B 和 C 均被排除**,情况 A 唯一成立。

---

## 2. 支持证据链

### 2.1 [THM] 级外部定理(独立已核)

| 定理 | 引用 | 核查 |
|------|------|------|
| PLOB pure-loss $E_R = -\log_2(1-\eta)$ | Pirandola-Laurenza-Ottaviani-Banchi 2017, Nat. Commun. 8:15043, **Thm. 5(主结果)[LIKELY]** | V2 多源 [VERIFIED] 公式;定理号 codex [LIKELY]; 详见 [Log 02](02_plob_dissection.md) |
| Pirandola 2019 网络 min-cut | Pirandola 2019, Commun. Phys. 2:51, **Eq. (11) single-path** / **Eq. (17) multi-path** | V2 [VERIFIED]; codex V4 修订引用形式; 详见 [Log 03](03_network_extension.md) |
| Pure-loss LOCC-simulation | Niset-Fiurášek-Cerf 2009 / PLOB17 Eq. (4) | V2 [VERIFIED];teleportation stretching 技术标准 |
| TF-QKD $\sqrt{\eta}$ achievable | Lucamarini-Yuan-Dynes-Shields 2018, Nature 557:400 | V2 多源 [VERIFIED];多篇 follow-up 确认 |

### 2.2 [COROLLARY] 级(本研究合成)

| 结论 | 依赖 |
|------|------|
| **定理 4.1**:$R^\infty(\mathcal{T}_{\text{umr}}; \eta_A, \eta_B) \leq -\log_2(1 - \min(\eta_A, \eta_B))$ | §2.1 前三条 + Allowed($\mathcal{T}_{\text{umr}}$) ⊂ Allowed(Pirandola-network) 单调性 [V4 补] |
| 对称 scaling $\leq 1.44\sqrt{\eta_{AB}}$ | 定理 4.1 + 展开 |
| Scaling gap = 0 | 上界 $\sqrt{\eta}$ + 下界 $\sqrt{\eta}$ |
| 情况 A 成立 | Scaling gap = 0 的直接推论 |

### 2.3 [SYN] 级:文献共识术语

- **"single-repeater bound"** 是文献共识术语,等同于 $\sqrt{\eta}$ scaling,等同于定理 4.1 的对称上界(见 V2 §B.5)
- **多篇 2023-2025 "surpassing repeaterless bound" 论文均 stop at $\sqrt{\eta}$**(V3 §A.1),进一步加强情况 A
- **无文献中存在 $\mathcal{T}_{\text{umr}}$ 协议 beat $\sqrt{\eta}$ scaling**(V3 全面反例搜索)

---

## 3. 显式声明的限界

### 3.1 Prefactor 未锁定

- 本 FINDINGS **不**宣称 $c^\star$ 精确值,仅给出 $c^\star \in [0.3, 1.44]$
- 1.44 的上端 prefactor **对 DV-QKD 类内不紧**,因 PLOB achievability 依赖 CV + quantum memory(codex V4 finding 3)
- **DV-QKD 类内的紧 prefactor** 须由 Phase 2 Sub-Q3 具体 converse 细化

### 3.2 附加条件

- **asymptotic collective attack**:必要条件;finite-key 情形须 Sub-Q2/Sub-Q3 GEAT 分析
- **pure-loss bosonic channel**:必要条件;noisy channel 的 scaling 预期仍 $\sqrt{\eta}$ 但未严格证明(外推风险)
- **单 untrusted relay**:必要条件;多 relay 或 trusted relay 属于不同拓扑类

### 3.3 方法学限界

- 本 FINDINGS 是 **literature-informed analysis**,不是新的严格证明
- 所有 [COROLLARY] 均由已发表 [THM] 组合得出
- 具体定理编号在 C1 条件下仍有核对空间 — 这是 Sub-Q3 Phase 2 的工作

---

## 4. 剩余开放问题(Phase 2-3 研究)

情况 A 内部尚未解决的子问题,供 PROSPECTUS Sub-Q3 + Sub-Q4 的实际研究:

### A1 — 对称 prefactor 紧值 $c^\star$

目前只有区间 $[0.3, 1.44]$。缩窄方向:

- **上界改进**($\mathcal{T}_{\text{umr}}$-specific converse):利用 Charlie 必须 broadcast classical outcome 这一 constraint;可能 approach:DKW20 / TGW14 的 squashed entanglement 修订
- **下界改进**(Pareto 优化 TF/PM/MP):Sub-Q2 Phase 0-1 工作
- **DV-QKD 类内 converse**:由 PLOB achievability 对 DV 不紧(§3.1),可能有针对 DV 的更紧上界

### A2 — 不对称 $\eta_A \neq \eta_B$

上界已给(定理 4.1 用 $\min(\eta_A, \eta_B)$);下界 prefactor 在不对称情形的精确表达未研究。

### A3 — 非 pure-loss 噪声修正

加入相位噪声、探测器效率、dark count 后:

- $E_R$ 解析值不再是 $-\log_2(1-\eta)$
- scaling 预期仍 $\sqrt{\eta}$(direct argument:noise 不改变信道的 "最小 capacity cut" 结构)
- 严格证明是 Sub-Q3 Phase 2 工作

### A4 — finite-key 修正

Kamin 2025 对 decoy-state BB84 给 finite-key 分析;对 $\mathcal{T}_{\text{umr}}$ 协议(TF/PM/MP)的 GEAT-based finite-key:

- Metger-Fawzi-Sutter-Renner 2024 GEAT 适用性在 $\mathcal{T}_{\text{umr}}$ 下预期成立
- 具体数值在 $n \sim 10^{10}$ 级别是否仍 $\sqrt{\eta}$ scaling 未严格验证
- Sub-Q2 Phase 1 工作

### A5 — 非 IID 攻击的鲁棒性

GEAT 依赖 non-signalling Markov 条件;$\mathcal{T}_{\text{umr}}$ 下 Charlie 的 classical announcement 是否严格满足 non-signalling(每一轮 Charlie 的宣告不能依赖 Alice/Bob 在其他轮的选择)— 这在标准 QKD 假设下成立,但形式化证明属于 Sub-Q3 / Sub-Q4。

---

## 5. 对 PHASE0_M1 的即时行动建议

### 5.1 M1-M4 验收策略确认

本 FINDINGS 不改变 REFACTORING_PLAN §5 的 M1-M4 验收标准,但**加强数值基准**:

- M1(BB84 WLC SDP):Shor-Preskill scaling 是 $1 - 2h(e)$,不是 $\sqrt{\eta}$。BB84 是点对点,归 PLOB,与 $\mathcal{T}_{\text{umr}}$ 不同。**M1 测 $R(e)$ 曲线形状**。
- M2(MDI + 六态):MDI 归 $\mathcal{T}_{\text{umr}}$ 子集,**数值 scaling 应验证 $\eta^2$**(MDI 两光子 coincidence 要求,非 $\sqrt{\eta}$)
- M3(数值诱骗):仍点对点 BB84 类
- **M4B(TF-QKD):关键 $\mathcal{T}_{\text{umr}}$ 验证,log-log 斜率 = 0.5 ± 0.05 直接对应本 FINDINGS 情况 A**

### 5.2 Sub-Q3 的工作重心调整

由 §4.1 A1 分析,Sub-Q3 Phase 2 "上界精读"**不应重推 scaling**(已共识),而应聚焦:

- $\mathcal{T}_{\text{umr}}$-specific prefactor converse
- DV-QKD 类内的紧 prefactor 界(PLOB CV-based achievability 对 DV 不紧,有收窄空间)

### 5.3 Sub-Q4 归因诊断提前

基于本 FINDINGS,Sub-Q4 的 gap 归因诊断可**预先定位**到 γ(两端都松):

- α(上界松):$1.44$ prefactor 对 DV 类不紧,可收窄,证据:§3.1
- β(下界松):TF/PM/MP 未完全 Pareto 优化,收窄空间 1-2 倍

---

## 6. 诚信红线核对

按 PROSPECTUS §9 + RESEARCH_PLAN §9:

- [x] **密钥率数字基于 WLC SDP 或其严格扩展**:本 FINDINGS 未产出具体密钥率数字,仅 scaling 结论
- [x] **安全性声明追溯到定理**:情况 A 结论追溯到 PLOB17 Thm. 5(主结果)[LIKELY] + Pirandola19 Eq. (11) [VERIFIED] + Lucamarini18 [VERIFIED]
- [x] **新发现(如有)通过独立验证**:本 FINDINGS 不宣称新发现,仅合成已有定理;V4 codex 独立立场确认情况 A
- [x] **Limitations 显式声明**:§3(显式限界)+ §4(开放问题)+ §1.2(条件化 COROLLARY 含义)
- [x] **AI 协助范围**:Claude Opus 4.7 基于训练语料,V1-V4 独立审计(其中 V2/V4 使用 WebFetch + codex 外部工具)
- [x] **文献引用核对**:PLOB / Pirandola19 / TF-QKD 均通过 WebSearch + 多源交叉 [VERIFIED] 核心陈述;定理号[?] 待 Sub-Q3 精读

---

## 7. 终结语

本 FINDINGS 完成 PROSPECTUS v3.1 §1 主问题的 **literature-informed 回答**。结论:

> **情况 A 成立** — 在 asymptotic + pure-loss + 单 untrusted measurement relay 假设下,$\sqrt{\eta}$ 是 scaling 级紧上界。

确定性级别:**条件化 COROLLARY**,条件包括 PROSPECTUS α 约定澄清与定理号精确核对。

**不是**:新的数学定理、PROSPECTUS 替代品、Sub-Q3 Phase 2 精读报告替代品、定论。

**是**:从已发表文献到 PROSPECTUS 主问题框架的**严格桥接**,供 PHASE0_M1 实施者参考,供 PROSPECTUS Sub-Q3 / Sub-Q4 研究者作为起点,供外部审稿人作为方法学透明度的示例。

**下一步建议**(给人类研究者):

1. 按 REFACTORING_PLAN §5 启动 M1 实施(WLC SDP for BB84)
2. Phase 0.5 做 M4B 后,把数值验证("log-log 斜率 = 0.5")与本 FINDINGS §5.1 的 TF-QKD 条目对齐
3. Phase 2 Sub-Q3 的 30-50 页"上界接缝报告"作为本 FINDINGS 的 **严格证明升级**,核对 Thm 编号 + $\mathcal{T}_{\text{umr}}$-specific DV prefactor converse
4. 若 Sub-Q3 研究者确认 α 约定,本 FINDINGS 确定性可从"条件化 COROLLARY"提升至"[COROLLARY]"

---

## Changelog

- **v1.0**(2026-04-19):首次落盘,经 Phase R(Log 01-06)+ Phase V(V1-V4)全部通过。

---

*FINDINGS 结束*
