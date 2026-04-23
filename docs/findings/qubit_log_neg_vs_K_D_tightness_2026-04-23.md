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
| 0.20 | 0.6781 | 0.2781 | 0.4000 | 0.7655 | 0.3902 | 0.3754 | 0.8480 | 0.8000 | **0.0480** |
| 0.30 | 0.4854 | 0.1187 | 0.3667 | 0.6323 | 0.2308 | 0.4015 | 0.7655 | 0.7000 | **0.0655** |
| 0.40 | 0.2630 | 0.0290 | 0.2340 | 0.4854 | 0.1187 | 0.3667 | 0.6781 | 0.6000 | **0.0781** |
| 0.50 | **0** | **0** | 0 | 0.3219 | 0.0456 | 0.2764 | 0.5850 | 0.5000 | **0.0850** |
| 0.60 | 0.2630 | 0.0290 | 0.2340 | 0.1375 | 0.0072 | 0.1303 | 0.4854 | 0.4000 | **0.0854** |
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

**对比意义** (修订后): 不同信道家族对 PPT-based 上界的"信息论紧度"差别很大。可推论：

- **erasure-like 信道**: log_neg 是**接近紧**的上界（gap < 0.09 bits）
- **depolarizing-like 信道**: log_neg 中等松（gap 0.2-0.4 bits）
- **dephasing-like 信道**: log_neg 中等松（gap 0.2-0.4 bits）

修复 e_r_depolarizing_analytic bug 后, depolarizing 紧度量级与 dephasing 类似（不再"极松"）。

---

## 2. 主要观测

### 2.1 PPT 松弛在中等噪声区**显著**（不可忽略）

**[修订 2026-04-23 — 修复 e_r_depolarizing_analytic bug 后]**:

- **Dephasing p=0.2**: log_neg 估 0.678 bits, 真 K_D 仅 0.278 bits → **2.4× 高估**
- **Depolarizing p=0.3**: log_neg 估 0.632 bits, 真 E_R = **0.231** bits → **2.7× 高估**（不再是"无穷大"）

这不是数值误差，而是 PPT relaxation 的**结构性松弛代价**。修复后 depolarizing E_R 严格 > 0 在 p ∈ [0, 2/3]，紧度比率类似 dephasing。

### 2.2 边界值零时两者收敛

- Dephasing p=0 / p=1 / p=0.5: log_neg = K_D（差为 0）
- Depolarizing p=0 / p=2/3+: log_neg = E_R = 0 或 1（边界）

中间噪声区差最大。

### 2.3 Depolarizing 的 PPT/SEP 边界（修订 2026-04-23）

**[修订]**: 之前章节基于 buggy `e_r_depolarizing_analytic` 公式（含虚假 (1-F)·log₂3 项）。修复后:

**正确 Werner 边界** = 唯一 separability/PPT boundary at **p = 2/3**（F = 1/2）。这与 Horodecki et al. 1996（PPT = SEP for 2⊗2）一致：单一 boundary，无中间 "PPT-but-separable" 段。

**修订后表（depolarizing）**:

| p | log_neg | E_R (corrected) | gap |
|---|---------|------------------|-----|
| 0.05 | 0.945 | **0.769** | 0.176 |
| 0.10 | 0.888 | **0.616** | 0.272 |
| 0.20 | 0.766 | **0.390** | 0.376 |
| 0.30 | 0.632 | **0.231** | 0.401 |
| 0.40 | 0.485 | **0.119** | 0.367 |
| 0.50 | 0.322 | **0.046** | 0.276 |
| 0.60 | 0.138 | **0.007** | 0.131 |
| 2/3 | 0.000 | 0.000 | 0.000 |

**真观察**（修订）:
- log_neg 比 E_R 大 **0.13-0.40 bits**（中等噪声区）
- 但 E_R 在 p ∈ [0, 2/3] **始终 > 0**（无之前误报的零段）
- log_neg/E_R 比率在 p=0.5 最大约 7×（仍是松界但不是无穷比）

**Bug-catch 影响**: 之前误称"在 p ∈ [0.27, 2/3] log_neg > 0 但 E_R = 0" — 实际 E_R 在该段也 > 0。详见 `qubit_E_R_PPT_hierarchy_2026-04-23.md` §2.5。

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
