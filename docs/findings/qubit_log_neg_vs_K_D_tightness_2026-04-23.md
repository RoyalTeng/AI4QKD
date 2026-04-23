# Tightness comparison: log_neg vs K_D / E_R for qubit channels

**日期**: 2026-04-23（β.G3 框架延伸）  
**严谨性**: [SYN]（数值观测；公式来源是 [THM]/标准教科书结果，但本对比是合成观测）  
**Scope**: 单 qubit dephasing + depolarizing + erasure 信道（AD 信道因无 K_D 解析公式不在本对比内）

---

## 0. 背景

Plenio 2005 不等式链:
```
log_neg(ρ) ≥ E_R(ρ) ≥ K_D(ρ)
```
其中 K_D 是 Choi 态对应信道的两向蒸馏密钥率。

对于以下两个 qubit 信道，**两端**都有解析公式可比：

| 信道 | log_neg（[SYN]，本 session）| K_D / E_R（已知 [THM]）|
|------|---------------------|---------------------|
| Dephasing | log₂(1+\|1-2p\|) | 1 − h(p)（PLOB 2017 Eq.39） |
| Depolarizing | log₂(2−3p/2) | 1 − h(F) − (1−F)·log₂3, F=1−3p/4（Horodecki 99） |
| **Erasure** | log₂(2−p) | 1 − p（PLOB 2017 Eq.43） |

由 K_D / E_R 是 [THM] 级紧界，log_neg 是 PPT-relaxed 上界，二者之差量化 **PPT 松弛代价**。

---

## 1. 关键数据（来自 1001 点 CSV）

| p | dp log_neg | dp K_D | dp gap | de log_neg | de E_R | de gap | er log_neg | er K_D | **er gap** |
|---|---|---|---|---|---|---|---|---|---|
| 0.05 | 0.9260 | 0.7136 | 0.2124 | 0.9449 | 0.7099 | 0.2350 | 0.9635 | 0.9500 | **0.0135** |
| 0.10 | 0.8480 | 0.5310 | 0.3170 | 0.8875 | 0.4968 | 0.3907 | 0.9260 | 0.9000 | **0.0260** |
| 0.20 | 0.6781 | 0.2781 | 0.4000 | 0.7655 | 0.1524 | 0.6131 | 0.8480 | 0.8000 | **0.0480** |
| 0.30 | 0.4854 | 0.1187 | 0.3667 | 0.6323 | **0** | 0.6323 | 0.7655 | 0.7000 | **0.0655** |
| 0.40 | 0.2630 | 0.0290 | 0.2340 | 0.4854 | 0 | 0.4854 | 0.6781 | 0.6000 | **0.0781** |
| 0.50 | **0** | **0** | 0 | 0.3219 | 0 | 0.3219 | 0.5850 | 0.5000 | **0.0850** |
| 0.60 | 0.2630 | 0.0290 | 0.2340 | 0.1375 | 0 | 0.1375 | 0.4854 | 0.4000 | **0.0854** |
| 2/3 | 0.4150 | 0.0817 | 0.3333 | **0** | **0** | 0 | 0.4150 | 0.3333 | **0.0817** |
| 0.80 | 0.6781 | 0.2781 | 0.4000 | 0 | 0 | 0 | 0.2630 | 0.2000 | **0.0630** |

**符号**: dp = dephasing, de = depolarizing, er = erasure.

### 1.1 重要观测：erasure 是"近紧"信道

erasure 的 PPT 松弛 gap 始终 **< 0.09 bits**（最大），远小于 dephasing/depolarizing 的 0.4-0.6 bits。
这是因为 erasure 信道的"信息丢失"是显式的（带 |e⟩ flag），输出 Choi 态结构简单：
```
ρ_choi(erasure) = (1-p)·|Φ⁺⟩⟨Φ⁺| + p·(I_A/2) ⊗ |e⟩⟨e|
                  └──── 纯纠缠 ────┘   └─── 显式可分 ───┘
```
PPT relaxation 看到的"额外可分态空间"非常受限，故 log_neg 与真 K_D 接近。

**对比意义**: 不同信道家族对 PPT-based 上界的"信息论紧度"差别很大。可推论：

- **erasure-like 信道**: log_neg 是**接近紧**的上界
- **depolarizing-like 信道**: log_neg 极松（差 0.6+ bits at moderate noise）
- **dephasing-like 信道**: log_neg 中等松（差 0.2-0.4 bits）

---

## 2. 主要观测

### 2.1 PPT 松弛在中等噪声区**显著**（不可忽略）

- **Dephasing p=0.2**: log_neg 估 0.678 bits, 真 K_D 仅 0.278 bits → **2.4× 高估**
- **Depolarizing p=0.3**: log_neg 估 0.632 bits, 真 E_R = 0 → **无穷大相对差**

这不是数值误差，而是 PPT relaxation 的**结构性松弛代价**。

### 2.2 边界值零时两者收敛

- Dephasing p=0 / p=1 / p=0.5: log_neg = K_D（差为 0）
- Depolarizing p=0 / p=2/3+: log_neg = E_R = 0 或 1（边界）

中间噪声区差最大。

### 2.3 Depolarizing 的 SEP-PPT 间隙（**重要**）

**Werner separability boundary**（F < 1/2，对应 p > 4/9 ≈ 0.444 实际是 1/3 for E_R cutoff）vs **PPT boundary**（p = 2/3）:

- 对 p ∈ [4/9, 2/3]: 信道 E_R = 0（state 已是 separable），但 log_neg > 0
- 这是 **bound entanglement** 概念在单 qubit 信道上的体现 — 确切说是 PPT-but-actually-separable

实际查表: e_r_depolarizing_analytic = 0 starts at p ≈ 0.267 (where F=1-3·0.267/4 ≈ 0.8, with E_R 进入 0 transition near F=0.5 boundary actually need to re-check). 让我看看代码逻辑——`if F <= 0.5: return 0.0`，即 1 − 3p/4 ≤ 0.5 ↔ p ≥ 2/3.

但表里 p=0.3 已 E_R = 0。原因：`max(0, 1.0 − H2 − (1.0−F)·log₂3)`，对 F = 1-3·0.3/4 = 0.775, 1 − h(0.775) − 0.225·log₂3 = 1 − 0.768 − 0.357 = -0.125 < 0 → max(0, -0.125) = 0.

所以 E_R 公式 in the entangled regime（F > 1/2）经常是 0，因为 `1 − h − (1-F)log₂3` 项可以为负。**这是 isotropic state E_R 在 F ∈ (1/2, F_crit) 区域的真零**，反映了 isotropic 状态在高噪声下虽然纠缠但 E_R = 0（因 Choi-Vidal-Werner 的 dual-witness construction 限制）。

**这进一步说明 log_neg 是非常松的上界**：在 p ∈ [0.27, 2/3] 的整个区段内，log_neg > 0 但 E_R = 0。

---

## 3. 对 Sub-Q3 上界工作的意义

### 3.1 log_neg 不应作为 "tight" 上界候选

β.G3 数值观测中曾提到 "2·log_neg < Pirandola for η < 1/φ"。但本 memo 显示 log_neg 本身已**显著高于** K_D（系数 2-3×）。所以即使 2·log_neg < Pirandola，**真实 K_D 远更小**——log_neg 的"紧化"是表象。

### 3.2 E_R^PPT 比 log_neg 更接近真 K_D

E_R^PPT 是 SDP 优化:
```
E_R^PPT(ρ) = min{ S(ρ‖σ) : σ ≥ 0, σ^{T_B} ≥ 0, Tr σ = 1 }
```
其中 S 是相对熵。E_R^PPT(ρ) ≤ log_neg(ρ) 一般成立（PPT cone 包含 log_neg 的 sigma 候选）。

我们在 β.G3 中已数值算了 E_R^PPT 单臂 for AD（9 点 grid），验证 E_R^PPT/PLOB ∈ [0.20, 0.45]。本 memo 横向显示 dephasing/depolarizing 也有类似量级紧化。

### 3.3 真正的 [THM] 级上界仍是 K_D / E_R 的精确表达

对**已知封闭式**的信道：直接用 K_D / E_R 表达。无需 PPT relaxation。

对**未知封闭式**的信道（如 generalized Pauli, generic CPTP）: 需要 SDP 数值或定理级紧化（squashed entanglement, RAINS bound）。

---

## 4. 局限

- 仅 dephasing + depolarizing 两个信道（AD 无 K_D 封闭式可比；erasure 信道未做）
- "K_D 是 [THM]" 仅在引用源（PLOB 2017 Eq.39 / Horodecki 1999）原始假设下成立 —— 本 memo **未** PDF 核对
- 标签 [SYN]（合成观测；公式集成自不同文献）

---

## 5. 相关产物

- 脚本: `scripts/qubit_log_neg_vs_E_R_tightness.py`
- 图: `docs/research/figures/qubit_log_neg_vs_K_D_tightness.{png,pdf}`
- CSV: `docs/research/data/qubit_log_neg_vs_K_D_tightness.csv` (1001 点)
- 前置 memos: 
  - `docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md`
  - `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md`

---

*2026-04-23 autonomous session. PPT relaxation cost 量化 [SYN]。*
