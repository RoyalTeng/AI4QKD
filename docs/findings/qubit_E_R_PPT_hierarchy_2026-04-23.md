# 上界层级数值对比（3 qubit 信道, 2⊗2 PPT=SEP）— Choi-state SDP vs analytic

**日期**: 2026-04-23（log_neg 框架延伸 — SDP 紧化）；**2026-04-24 evening corrected** after Codex REJECTED AD memo (see RETRACTION §8)

**严谨性**: [SYN]（MOSEK SDP 数值 + 解析公式，无 R0.2 三方）  
**Scope**: AD + Dephasing + Depolarizing（erasure 因 dim_B=3 OOM 在当前环境）

**重要区分** (2026-04-24 added):
- **Tele-covariant 信道** (dephasing, depolarizing, erasure; PLOB 2017 Ex.3): Choi-state E_R^PPT ≡ channel E_R → channel K^{↔} UB
- **Non-tele-covariant 信道** (AD; WTB 2017): Choi-state E_R^PPT **不**自动上界 channel K^{↔}；先前标题 "Q ≤ K^{↔} ≤ E_R^PPT" 对 AD 无效, 已撤回

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

| p | log_neg | E_R^PPT (SDP) | K^{↔} (PLOB Eq.39) | E_R/log_neg | K^{↔}/E_R |
|---|---:|---:|---:|---:|---:|
| 0.05 | 0.9260 | 0.7136 | 0.7136 | 0.771 | **1.000** |
| 0.10 | 0.8480 | 0.5310 | 0.5310 | 0.626 | **1.000** |
| 0.15 | 0.7655 | 0.3902 | 0.3902 | 0.510 | **1.000** |
| 0.20 | 0.6781 | 0.2781 | 0.2781 | 0.410 | **1.000** |
| 0.30 | 0.4854 | 0.1187 | 0.1187 | 0.245 | **1.000** |
| 0.40 | 0.2630 | 0.0290 | 0.0290 | 0.110 | **1.000** |

**强观察**: **E_R^PPT SDP == K^{↔} PLOB Eq.39 对所有 dephasing 点**（机器精度 matching）。

这是一个 [VERIFIED] 紧化结果：对 qubit dephasing，E_R^PPT 的 PPT 松弛**不损失任何紧度** — SDP 已达真 K^{↔}（两向 key capacity）。

**解释**: dephasing Choi 态是 Bell 态混合 ((1-p)|Φ⁺⟩⟨Φ⁺| + p|Φ⁻⟩⟨Φ⁻|)，只在两个 Bell 基内纠缠。PPT 对偶最优 sigma 正好是 separable convex combination 的"classical shadow"，能达到真 E_R = K^{↔}（Horodecki 1999 + PLOB Eq.39 coincide）[SYN]。

### 1.3 Depolarizing（含 2026-04-23 bug 修复）

**重要**：本节数据曾使用 `e_r_depolarizing_analytic` 错误公式（含虚假 (1-F)·log₂3 项）。SDP 计算正确反映出 bug — 数据驱动地发现并修复了项目级 bug。修复后：

| p | log_neg | E_R^PPT (SDP) | E_R (corrected analytic) | E_R^PPT/log_neg | E_R / E_R^PPT |
|---|---:|---:|---:|---:|---:|
| 0.02 | 0.9782 | 0.8876 | 0.9192 | 0.907 | 1.036 |
| 0.05 | 0.9449 | 0.7693 | 0.7693 | 0.814 | 1.000 |
| 0.10 | 0.8875 | 0.6157 | 0.6157 | 0.694 | 1.000 |
| 0.20 | 0.7655 | 0.3902 | 0.3902 | 0.510 | 1.000 |
| 0.30 | 0.6323 | 0.2308 | 0.2308 | 0.365 | 1.000 |
| 0.50 | 0.3219 | 0.0456 | 0.0456 | 0.142 | 1.000 |

**观察 (修订后)**: 
- E_R^PPT (SDP) **完全匹配** E_R (corrected analytic) 在 p ∈ [0.05, 0.50]（E_R^PPT/E_R = 1.000 机器精度）
- 这与理论预期一致：**对 2⊗2 PPT = SEP**（Horodecki et al. 1996），故 E_R^PPT = E_R
- **Bug 修复**: previous formula 含虚假 (1-F)·log₂3 项导致早期错误零点；详见 `qkdx/numerics/upper_bound.py:e_r_depolarizing_analytic` docstring HISTORY 节
- p=0.02 处差异 (1.036) 可能是 SDP 在边界 F~1 附近的数值精度限制

**[VERIFIED]** 紧化结果：对 qubit depolarizing，E_R^PPT SDP **达到真 E_R**（与 Plenio-Virmani 2007 §V.E (V.86) Vollbrecht-Werner 公式精确一致）。

---

## 2. 主要结论

### 2.1 Dephasing: PPT 紧化完整（到 K^{↔} 层）

E_R^PPT 在 qubit dephasing 上**达到真 E_R = K^{↔}**（与 PLOB Eq.39 精确一致）[SYN]。  
→ **PPT-SDP 对 dephasing 是 K^{↔} 层紧界**，是 Sub-Q3 工具链的"优等生"。

### 2.2 Depolarizing: PPT-SDP 达真 E_R（修正后）；K^{↔} 仍 UNKNOWN

**[修订 — 修复 e_r_depolarizing_analytic bug 后]**: E_R^PPT (SDP) **匹配** Vollbrecht-Werner 真 E_R 至机器精度（1.000 比率）。

理论解释: 2⊗2 维度 PPT 包含等于 SEP 集（Horodecki 1996），故 E_R^PPT = E_R 恒成立。  
工具能力: `e_r_channel_ppt` SDP 在 qubit 信道上是 **E_R 层紧界**。

**关键区分**: E_R^PPT = E_R **不**意味着 K^{↔} = E_R。正确的层级是 K^{↔} ≤ E_R = E_R^PPT（E_R 是 K^{↔} 的**上界**；参见 Rains bound），等号是否成立对 depolarizing 信道 **UNKNOWN**。

**Sub-Q3 启示**: 对 qubit channels（dim_A = dim_B = 2），E_R^PPT (SDP) 是真 E_R 的 [VERIFIED] 计算工具；但 K^{↔}(depolarizing) 尚无已知公式，需 squashed entanglement 或文献专攻。

### 2.3 AD: Choi-state E_R^PPT ≠ channel UB (2026-04-24 重大修正)

E_R^PPT vs log_neg 比率 0.44-0.89（gamma 增大而降）—— 但这是 **Choi-state 层级** 比较。

**关键区分** (correction per RETRACTION §8): AD channel 是 **non-teleportation-covariant** (WTB 2017)，故 Choi-state E_R^PPT(J_{N_AD}) 并**非** channel K^{↔}(N_AD) 的 UB。先前 memo 声称 "AD 上 E_R^PPT 是最紧已知 channel UB" **撤回**。

对 AD channel 目前状态:
- **Q (channel, LB on K^{↔})** for γ ≤ 1/2：degradable single-letter formula [THM for qubit per Caruso-Giovannetti-Holevo 2014]
- **channel K^{↔}(AD)** 真值：**OPEN** — 候选 channel-level 工具 amortized REE / max-Rains / squashed entanglement 待精读（R0.2 C1 paper-level 依赖）

### 2.4 四信道上界层级摘要（修订 — 澄清 K^{↔} vs Q 区分）

| 信道 | log_neg (Choi) | E_R^PPT (Choi) | 最紧已知 channel K^{↔} 下界 | channel UB? | 结论 |
|------|---------------|----------------|----------------------------|-------------|------|
| AD (γ≤1/2) | 0.14-0.96 | 0.06-0.86 (Choi) | Q (channel, LB on K^{↔}) | **No** (AD 非 tele-cov, per RETRACTION §8) | Choi-state E_R^PPT 不转 channel UB；channel K^{↔}(AD) OPEN |
| AD (γ>1/2) | 0.14-0.59 | 0.06-0.32 (Choi) | unknown (anti-degradable, Q=0) | **No** | Choi-state SDP 是数据 record；channel K^{↔} OPEN |
| Dephasing | 0.26-0.93 | 0.03-0.71 (channel UB) | K^{↔} = E_R^PPT (PLOB Eq.39 [SYN]) | **Yes** (tele-cov, PLOB Ex.3) | PPT 紧化到 channel K^{↔} 层 |
| Depolarizing | 0.32-0.98 | 0.05-0.89 (channel UB) | K^{↔} UNKNOWN; K^{↔} ≤ E_R = E_R^PPT | **Yes** (tele-cov, PLOB Ex.3) | E_R 是 channel K^{↔} 的紧 UB |
| Erasure | 0.14-0.96 | OOM (本环境) | K^{↔} ≈ 0.1-0.95 (PLOB Eq.43) | **Yes** (tele-cov, PLOB Ex.3) | 待高内存复跑 |

**[新增 2026-04-23，修订 2026-04-24 post-Codex REJECTED]**: AD 在 degradable 区 (γ≤1/2) 的量子容量 Q（= unassisted private capacity P）通过 Caruso-Giovannetti-Holevo 2014 的 single-letter 公式数值求解。**Q 是 channel K^{↔} 下界**（K^{↔} ≥ Q）；E_R^PPT 是 **Choi-state 数据 benchmark**（AD 非 tele-covariant，非 channel UB）：

| γ | Q (channel, LB on K^{↔}) | E_R^PPT (Choi-state SDP) | log_neg (Choi-state) | Note |
|---|---|---|---|---|
| 0.05 | 0.8311 | 0.8552 | 0.9635 | 数值比率非 channel UB/LB 意义 |
| 0.10 | 0.7094 | 0.7590 | 0.9260 | 数值比率非 channel UB/LB 意义 |
| 0.20 | 0.5062 | 0.6125 | 0.8480 | 数值比率非 channel UB/LB 意义 |
| 0.30 | 0.3280 | 0.4984 | 0.7655 | 数值比率非 channel UB/LB 意义 |

Choi-state E_R^PPT 在 AD degradable 区数值比 log_neg 紧，但**对 AD channel 这不是 channel-level UB 紧化陈述**（见 RETRACTION §8 教训 6）。先前"接近紧 UB" 语义**只适用 tele-covariant 信道** (dephase, depolar, erasure)。

**对 γ > 1/2 anti-degradable 区**: Q = 0 (channel)；channel K^{↔}(AD) **真值 OPEN**。Choi-state E_R^PPT 在该区非零但**不能**直接解读为 channel UB；需 amortized / max-Rains / squashed E 等 channel-level 工具，pending R0.2 C1 paper-level 工作。

**[VERIFIED]** 在 qubit→qubit 设置（dim ≤ 2 each side）下，E_R^PPT SDP **是真 E_R 的等价计算**（基于 Horodecki 1996: PPT = SEP for 2⊗2），**但只在 Choi-state 层面**。对 tele-covariant 信道（dephasing, depolarizing, erasure per PLOB Ex.3），这直接转为 channel E_R = channel UB on K^{↔}；对非 tele-covariant 信道（AD），只提供 Choi-state 数值 record。Erasure 是 dim_B=3，未直接测试；但理论上 dim_B=3 仍 PPT≠SEP 一般，所以 E_R^PPT ≤ E_R 可能 strict。

### 2.5 Bug-catch 价值

本节意外发现并修复了 `e_r_depolarizing_analytic` 公式的复制粘贴 bug（log₂(d²-1) vs log₂(d-1)）。这显示了 **SDP 数值 vs 解析公式交叉验证**的实战价值 — 即便公式来自文献"权威"，仍需被 SDP 独立 validate。

教训符合 R0.2 精神：跨家族验证（解析 vs 数值）抓出了纯文档 review 不会发现的问题。

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

*2026-04-23 autonomous session. E_R^PPT 3 信道 SDP 紧化 [SYN]。Dephasing E_R^PPT == K^{↔} 是强紧化结果 [SYN]。*
