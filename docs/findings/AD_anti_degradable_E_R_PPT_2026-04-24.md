# AD anti-degradable (γ > 1/2): Choi-state E_R^PPT 的数值观察（不构成 channel-level UB）

**日期**: 2026-04-24（Day 4 末 autonomous session; 2026-04-24 evening revised after Codex REJECTED）
**严谨性**: [SYN-DATA]（Choi-state 数值观察 only; **不**构成 channel capacity K^{↔} 的 UB — 见 §-1）
**Scope**: qubit amplitude-damping 信道 γ ∈ [0, 1] 的 **Choi 态 E_R^PPT 数值**; 协议 / umr 拓扑 / channel capacity 陈述**不在本 memo 范围**

---

## -1. 撤回公告 / Correction Banner

**v1.0 (本 memo 首版) 曾声称**: "E_R^PPT(J_{N_AD}) 是 K^{↔}(N_AD) 的严格 UB"。

**Codex 独立评审 (2026-04-24) 判定**: **REJECTED — silent structural upgrade**。关键错误:

1. **K^{↔} ≤ D^{↔}_d 是 FALSE**：Horodecki et al. 2005 (PRL 94, 160502) 证明 private states 可有 key 但不蒸馏 ebit —— 所以此推理链不对。
2. **Choi-state E_R 是 channel E_R 的 LOWER bound**：PLOB 2017 明示 `E_R(N) = sup_ρ E_R[(I⊗N)(ρ)] ≥ E_R(J_N)`。从 Choi-state 上到 channel capacity 需要 **teleportation-covariance**（Pirandola 2017 Nat Comm 8:15043），而 **AD channel 不是 teleportation-covariant**（WTB 2017）。
3. **Horodecki 1996 2⊗2 PPT=SEP 只在 Choi 态层面**：只升级 `E_R^PPT(J_N) = E_R(J_N)` at Choi-state level；**不**继承到 channel 级反向。

**结果**: v1.0 声明的"K^{↔}(AD,γ=0.7) ≤ 0.183" 撤回。本 memo 降级为**纯 Choi-state 数值观察**，无 channel-level 陈述。

**教训**（符合 `feedback_ai_draft_structural_gaps.md` red-flag 警告）：AI autonomous 轻易把"Choi state 上的 E_R^PPT SDP 返回非零"误读为"channel K^{↔} 有 UB"——这是一个 channel-vs-state 跨层级混淆，属于 silent upgrade。

---

## 0. 动机（保留）

Day 4 新加 `quantum_capacity_amplitude_damping_degradable(γ)` 给出 γ ≤ 1/2 的 AD 信道 Q（Caruso-Giovannetti-Holevo 2014）。γ > 1/2 是 anti-degradable，Q = 0。

**合规目标**（修订）：量化 AD 信道的 **Choi 态** Rains bound 在 γ 扫描下的行为。不再声称这是 channel K^{↔} 的 UB。

---

## 1. 数值观察（仅 Choi-state 层级）

| γ | E_R^PPT(J_{N_AD}) (SDP, bits) | log_neg(J_{N_AD}) (analytic, bits) | Q(N_AD) (若 γ < 1/2) | log_neg/E_R^PPT (Choi) | Status |
|---|---|---|---|---|---|
| 0.05 | 0.8552 | 0.9635 | 0.8311 | 1.13 | degradable |
| 0.10 | 0.7590 | 0.9260 | 0.7094 | 1.22 | degradable |
| 0.20 | 0.6125 | 0.8481 | 0.5062 | 1.38 | degradable |
| 0.30 | 0.4984 | 0.7655 | 0.3280 | 1.54 | degradable |
| 0.50 | 0.3217 | 0.5850 | 0 (boundary) | 1.82 | border |
| 0.55 | 0.2844 | 0.5361 | Q = 0 | 1.89 | anti-degradable |
| 0.60 | 0.2491 | 0.4854 | Q = 0 | 1.95 | anti-degradable |
| 0.65 | 0.2154 | 0.4330 | Q = 0 | 2.01 | anti-degradable |
| 0.70 | 0.1830 | 0.3785 | Q = 0 | 2.07 | anti-degradable |
| 0.75 | 0.1517 | 0.3219 | Q = 0 | 2.12 | anti-degradable |
| 0.80 | 0.1213 | 0.2630 | Q = 0 | 2.17 | anti-degradable |
| 0.85 | 0.0913 | 0.2016 | Q = 0 | 2.21 | anti-degradable |
| 0.90 | 0.0616 | 0.1375 | Q = 0 | 2.23 | anti-degradable |
| 0.95 | 0.0315 | 0.0704 | Q = 0 | 2.24 | anti-degradable |

（Q 列通过 `quantum_capacity_amplitude_damping_degradable` 实时计算；E_R^PPT 来自 `qubit_E_R_PPT_SDP_all_4.csv` + `AD_antidegradable_E_R_PPT_fill.csv`；log_neg 解析 `analytic_log_neg_amplitude_damping`。）

### 观察（不含 channel-level claim）

- **E_R^PPT(J_{N_AD}) 作为 Choi 态函数**: 在整个 γ ∈ [0, 1] 区保持单调递减至 0 (γ=1)
- **log_neg / E_R^PPT 比率 (Choi 态层面)**: 从 1.13 (γ=0.05) 单调升到 **2.24 (γ=0.95)**（经验观察，无封闭推导 —— 不是 log₂(3) = 1.585 也不是其他已知常数；**留作 open question**）
- **Q = 0 区的 Choi-state E_R^PPT 非零**: 说明 Choi 态含 nonzero Rains 熵，但**不意味** channel 能在该区有 nonzero K^{↔}

---

## 2. Channel-level 意义（现在标 OPEN, v1.0 之 §2 撤回）

**OPEN 问题**：对 AD 信道 γ > 1/2，channel two-way key capacity K^{↔}(N_AD) 的 UB/LB 是什么？

**本 memo 的 Choi-state E_R^PPT 数据 NOT 直接适用**，因为：

- 一般 channel REE `E_R(N) = sup_ρ E_R[(I⊗N)(ρ)]`，与 Choi-state REE `E_R(J_N)` 满足 `E_R(N) ≥ E_R(J_N)`（PLOB 2017；Choi 态只是 sup 中一个特殊取法）
- 用 **Choi-state REE 作为 channel REE converse**（即 `E_R(N) = E_R(J_N)` 闭合）需要 channel **teleportation-covariance / teleportation-simulability**（PLOB 2017 Ex.3 + Pirandola 2017 Nat Comm 8:15043）
- AD channel **不是** teleportation-covariant（WTB 2017）→ 对 AD `E_R(J_N) ≤ E_R(N)`，本 memo 的数值是 channel REE 的 **下界**而非上界
- Choi-state 上的 Rains bound 给的是 Choi 态 distillation rate 信息，不直接等价于 channel capacity

**可能的正确路径**（均**未**在本 memo 完成）:
- **Amortized REE** / 递归 channel REE（Khatri-Wilde 2020 §16.2）
- **Squashed entanglement** channel version（Takeoka-Guha-Wilde 2014）
- **max-Rains** (Wang-Fang-Duan 2019) — channel 级 SDP
- **Direct converse** via simulability classes that DO include AD（若存在）

这些都需要 paper-level 精读（**R0.2 C1 依赖**, 不在 AI 自主范围内）。

---

## 3. 修订后的 Sub-Q3 / Sub-Q4 启示

### 3.1 对 Sub-Q3

- Choi-state E_R^PPT SDP 本身是 **state-level** 工具，不能作为 channel capacity 的直接 UB
- 对 **teleportation-covariant** 信道（dephasing, depolarizing, erasure），Choi-state REE 确实 = channel REE （PLOB 2017 Ex.3），故前期 report 中 dephasing/depolarizing/erasure 的 E_R^PPT 信道 UB 陈述**仍有效**
- AD 不在这个类 —— 需要专门 channel-level 工具

### 3.2 对 Sub-Q4 gap 归因

- 先前(`upper_bound_report §11.3`)标注 AD "E_R^PPT ∈ [Q, E_R^PPT]" 应解读为 **Choi-state 的**上下界，**不是** channel K^{↔} 的界
- AD 协议 Pareto vs UB 的 gap 归因在 channel-level 工具就绪前保留 OPEN

---

## 4. 数据产物

### 本轮新增
- `docs/research/data/AD_antidegradable_E_R_PPT_fill.csv` — 7 个新 Choi-state SDP 点 (γ=0.55…0.95)
- `scripts/AD_antidegradable_E_R_PPT_fill.py` — SDP 扫描脚本（docstring + print 均已 Choi-state-only, commit 254b471）
- `scripts/AD_anti_degradable_plot.py` — 可视化脚本（标题已改为 "Choi-state only, not channel-level UB for AD (non-tele-covariant)", commit 0b8cf40）
- `docs/research/figures/AD_anti_degradable_hierarchy.{png,pdf}` — 已基于修订后脚本 regenerate（commit 0b8cf40）

**CSV 物理数据未变**（`gamma`, `E_R_PPT_SDP`, `log_neg_analytic`, `Q_LB_on_K2way` 列保持不变；仅 `sdp_time_s` 运行时 metadata 因脚本重跑刷新 — 不影响科学内容）。语义解释降级至 Choi-state only 完成。

---

## 5. 严谨性边界（修订）

- **[SYN-DATA]**: Choi-state SDP 数值观察；不涉及 channel capacity 陈述
- **降级自 [SYN]**: v1.0 误声称 channel-level UB; 已撤回至纯 Choi-state 层级
- **不构成** [COROLLARY]: 无 channel-level 内容，连候选都不是
- **OPEN**: channel K^{↔}(AD, γ > 1/2) 的 UB/LB；需用户 paper-level work + C1/C2/C3

---

## 6. 提议的下一步（诚实化版）

**本轮已完成**:
- [x] 更新 plot 脚本移除 "Q ≤ K^{↔} ≤ E_R^PPT" 标题，改为 "Choi-state only" + tele-covariance disclaimer（commit 0b8cf40）
- [x] `upper_bound_report §11` AD 部分加 Choi-state vs channel-level 区分（v0.7, commit 0b8cf40）

**仍 OPEN**:
- [ ] 若需 channel-level AD UB，需调研 **amortized REE** / **max-Rains** / **squashed entanglement** 是否适用 —— **需用户 PDF 精读**（R0.2 C1 外部依赖）

---

## 7. Changelog

- **v1.2** (2026-04-25 follow-up review fix): §1 "channel REE converse" 表述精化（区分 `E_R(N)` 与 `E_R(J_N)` 关系：`E_R(N) ≥ E_R(J_N)` always；channel-level converse 闭合需 tele-cov）；§7 v1.1 entry 中"flagged for next revision"修正为"已完成"（plot 已 regenerate 在 commit 0b8cf40）。
- **v1.1** (2026-04-24 evening, post-Codex-REJECTED): **整体降级**。删除 channel-level K^{↔} UB 声明（§-1 撤回公告 + §2 重写）；log₂(3)/log₂(2) 数学错误去除；plot 标题已修订并 regenerate（commit 0b8cf40）。
- **v1.0** (2026-04-24): 首版 [SYN]，声称 E_R^PPT(J_N) 是 channel K^{↔} UB —— **撤回** per §-1。
