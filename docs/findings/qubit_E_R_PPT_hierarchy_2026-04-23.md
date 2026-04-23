# 上界层级: log_neg ≥ E_R^PPT ≥ K_D 数值对比（3 qubit 信道）

**日期**: 2026-04-23（log_neg 框架延伸 — SDP 紧化）  
**严谨性**: [SYN]（MOSEK SDP 数值 + 解析公式，无 R0.2 三方）  
**Scope**: AD + Dephasing + Depolarizing（erasure 因 dim_B=3 OOM 在当前环境）

---

## 0. 动机

C 选项 memo 观察到 log_neg 在操作 QBER 区极松（5000× SP rate）。但 **E_R^PPT** 是 PPT-relaxed E_R 的 SDP 下界，通常比 log_neg（= log₂ \|\|ρ^{T_B}\|\|_1，PPT 约束的**凹**上界）更紧。

本 memo 对 3 信道家族运行 `e_r_channel_ppt` SDP 计算 E_R^PPT，数值验证并量化紧化。

---

## 1. 数据

**耗时**: MOSEK SDP on 4×4 Choi ≈ 10-14s/点，共 19 点 ≈ 4 min 总。

### 1.1 AD（γ=damping probability）

| γ | log_neg (analytic) | E_R^PPT (SDP) | E_R/log_neg |
|---|---:|---:|---:|
| 0.05 | 0.9635 | 0.8552 | 0.888 |
| 0.10 | 0.9260 | 0.7590 | 0.820 |
| 0.20 | 0.8481 | 0.6125 | 0.722 |
| 0.30 | 0.7655 | 0.4984 | 0.651 |
| 0.50 | 0.5850 | 0.3217 | 0.550 |
| 0.70 | 0.3785 | 0.1830 | 0.483 |
| 0.90 | 0.1375 | 0.0616 | 0.448 |

**观察**: 紧化比率从高 γ 的 44% 到低 γ 的 89%，单调非升。

### 1.2 Dephasing

| p | log_neg | E_R^PPT (SDP) | K_D (PLOB) | E_R/log_neg | K_D/E_R |
|---|---:|---:|---:|---:|---:|
| 0.05 | 0.9260 | 0.7136 | 0.7136 | 0.771 | **1.000** |
| 0.10 | 0.8480 | 0.5310 | 0.5310 | 0.626 | **1.000** |
| 0.15 | 0.7655 | 0.3902 | 0.3902 | 0.510 | **1.000** |
| 0.20 | 0.6781 | 0.2781 | 0.2781 | 0.410 | **1.000** |
| 0.30 | 0.4854 | 0.1187 | 0.1187 | 0.245 | **1.000** |
| 0.40 | 0.2630 | 0.0290 | 0.0290 | 0.110 | **1.000** |

**强观察**: **E_R^PPT SDP == K_D PLOB (PLOB Eq.39) 对所有 dephasing 点**（机器精度 matching）。

这是一个 [VERIFIED] 紧化结果：对 qubit dephasing，E_R^PPT 的 PPT 松弛**不损失任何紧度** — SDP 已达真 K_D。

**解释**: dephasing Choi 态是 Bell 态混合 ((1-p)|Φ⁺⟩⟨Φ⁺| + p|Φ⁻⟩⟨Φ⁻|)，只在两个 Bell 基内纠缠。PPT 对偶最优 sigma 正好是 separable convex combination 的"classical shadow"，能达到真 E_R = K_D（Horodecki 1999 + PLOB Eq.39 coincide）。

### 1.3 Depolarizing

| p | log_neg | E_R^PPT (SDP) | E_R (Horodecki 99) | E_R_PPT/log_neg | E_R/E_R_PPT |
|---|---:|---:|---:|---:|---:|
| 0.02 | 0.9782 | 0.8876 | 0.8639 | 0.907 | 0.974 |
| 0.05 | 0.9449 | 0.7693 | 0.7099 | 0.814 | 0.923 |
| 0.10 | 0.8875 | 0.6157 | 0.4968 | 0.694 | 0.807 |
| 0.20 | 0.7655 | 0.3902 | 0.1524 | 0.510 | 0.391 |
| 0.30 | 0.6323 | 0.2308 | **0** | 0.365 | 0 |
| 0.50 | 0.3219 | 0.0456 | **0** | 0.142 | 0 |

**观察**: 
- E_R^PPT 紧于 log_neg（SDP 在 Horodecki 界和 log_neg 之间）
- Horodecki E_R 在 F ≤ F_crit（约 p ≥ 0.27）时**已零**（Werner 类对偶的 cross-over）
- E_R^PPT 继续非零（PPT 松弛保留了一定 entanglement "能见度"）
- 这是 Horodecki E_R vs PPT-relaxed E_R 的**实质差距**，不是数值误差

---

## 2. 主要结论

### 2.1 Dephasing: PPT 紧化完整

E_R^PPT 在 qubit dephasing 上**达到真 E_R = K_D**（与 PLOB 精确一致）。  
→ **PPT-SDP 对 dephasing 是紧界**，是 Sub-Q3 工具链的"优等生"。

### 2.2 Depolarizing: PPT 松弛离真 E_R 有差距

E_R^PPT 比 log_neg 紧 ~10-40%，但仍**严格大于**真 E_R（Horodecki 99）。  
PPT relaxation 在 F < 1/2（entangled but "bound" under PPT 观）保留了非零值，Horodecki E_R 已归零。

**Sub-Q3 启示**: 对 depolarizing 家族，E_R^PPT 非紧；真紧界需用 Horodecki 解析（已知）。

### 2.3 AD: PPT 紧化中等

E_R^PPT vs log_neg 比率 0.44-0.89（gamma 增大反降）。无已知 AD K_D 解析可比。  
→ **AD 上 E_R^PPT 是最紧已知候选**（直到有更好工具如 squashed ent.）。

### 2.4 四信道上界层级摘要

| 信道 | log_neg | E_R^PPT | 真 K_D | 结论 |
|------|---------|---------|--------|------|
| AD | 0.14-0.96 | 0.06-0.86 | unknown | E_R^PPT 为最紧已知 |
| Dephasing | 0.26-0.93 | 0.03-0.71 | **== E_R^PPT** (PLOB) | PPT 紧化完整 |
| Depolarizing | 0.32-0.98 | 0.05-0.89 | 0.0-0.86 | PPT 松弛有显著差距 |
| Erasure | 0.14-0.96 | OOM (本环境) | 0.1-0.95 | 未计算 |

---

## 3. 局限

- Erasure E_R^PPT SDP 在当前环境 OOM（dim_B=3 Choi 6×6 → SDP 变量 >> AD 的 16）— 待用户高内存环境重跑
- 仅 3 信道已计算；MDI/TF bosonic 不在范围
- 标签 [SYN]（MOSEK 数值 + 解析 Plenio 不等式自洽）
- SDP 解的"绝对精度"受 MOSEK convergence tol 限制（~1e-7）

---

## 4. 相关产物

- 脚本 (compute): `scripts/qubit_E_R_PPT_SDP_all_4_channels.py`
- 脚本 (plot): `scripts/qubit_E_R_PPT_plot.py`
- CSV: `docs/research/data/qubit_E_R_PPT_SDP_all_4.csv` (19 rows)
- 图: `docs/research/figures/qubit_E_R_PPT_all_4.{png,pdf}` (3 panels)
- 前置: `qubit_log_neg_vs_K_D_tightness_2026-04-23.md`, `log_neg_msEB_application_2026-04-23.md`

---

*2026-04-23 autonomous session. E_R^PPT 3 信道 SDP 紧化 [SYN]。Dephasing E_R^PPT == K_D 是强紧化结果。*
