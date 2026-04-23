# Composed channels E∘E: log-negativity 退化分析

**日期**: 2026-04-23（log_neg 框架延伸）  
**严谨性**: [SYN]（解析公式由信道复合规则 + 已验证 log_neg 公式得出；纯组合）  
**Scope**: 4 个 qubit 信道家族的序列复合 E∘E 的 log_neg

---

## 0. 动机

umr 拓扑中，单 transmission 经过两段信道（Alice→Charlie→Bob）。当两段都是同一类型信道时，整个传输路径相当于**复合信道** E ∘ E。这与 β.G3 之前研究的 **tensor product** E₁ ⊗ E₂（双臂并行 BSM 设置）**不是同一个**。

本 memo 给出复合（**非** tensor）情况下每个信道家族的 log_neg 解析退化。

---

## 1. 复合规则（标准）

各信道家族在复合下保持族内（self-conjugate semigroup）:

| 家族 | 单段参数 | 复合等效参数 |
|------|----------|------------|
| AD | γ | γ_eff = 1 − (1−γ)² = 2γ − γ² |
| Dephasing | p | p_eff = 2p(1−p) |
| Depolarizing | p | p_eff = 1 − (1−p)² = 2p − p² |
| Erasure | p | p_eff = 1 − (1−p)² = 2p − p² |

复合的 log_neg = 解析公式应用于 effective param。

---

## 2. 解析复合公式

| 家族 | log_neg(E∘E, p) | 闭式 |
|------|-----------------|------|
| AD | log₂(2 − γ_eff) = log₂(2 − 2γ + γ²) | **log₂(1 + (1−γ)²)** |
| Dephasing | log₂(1 + \|1−2p_eff\|) = log₂(1 + (1−2p)²) | log₂(1 + (1−2p)²) for p≤1/2 |
| Depolarizing | max(0, log₂(2 − 3p_eff/2)) | max(0, log₂((3p² − 6p + 4)/2)) |
| Erasure | log₂(2 − p_eff) = log₂(2 − 2p + p²) | **log₂(1 + (1−p)²)** |

---

## 3. 关键结构观测

### 3.1 AD∘AD ≡ Erasure∘Erasure（**新发现**）

由表中可见：**AD 和 erasure 在复合下给出完全相同的 log_neg 函数** log₂(1 + (1−p)²)。

**原因**：两个信道有相同的复合参数规则（p_eff = 2p − p²），且单段 log_neg 公式都是 log₂(2 − param)。所以复合后函数形式恒等。

**意义**：在 PPT-relaxed 上界视角下，**AD 和 erasure 信道的两段复合是不可区分的**。但这两个信道的 K_D 行为完全不同（erasure K_D = (1−p)², AD K_D 复杂），所以两种信道仅在 PPT 投影下"等价"。

**警示**：如果用 log_neg 作 Sub-Q3 上界，AD 和 erasure 给同样的紧度，但实际可达 K_D 差距很大 — log_neg 失去了区分这两类信道的能力。

### 3.2 Depolarizing 复合的 PPT 边界提前到达

- 单段 depolarizing PPT 阈值：p = 2/3 ≈ 0.6667
- 复合 depolarizing(p)∘depolarizing(p) PPT 阈值：p = 1 − 1/√3 ≈ 0.4226

复合让 PPT-投影的"信息消亡"提前发生 — 中等噪声单 arm 仍可有 log_neg > 0，但两段复合后已 PPT。

### 3.3 Dephasing 的特殊对称性

p_eff = 2p(1−p) 对所有 p ∈ [0,1] 都满足 p_eff ∈ [0, 1/2]，且 p_eff = 1/2 当且仅当 p = 1/2。

所以 dephasing(p) ∘ dephasing(p) 的 log_neg 在 p = 1/2 取唯一零点；其他 p 均 > 0。

公式：log_neg(DP∘DP, p) = log₂(1 + (1−2p)²)，一个对称单峰函数（max at p=0 and p=1, min at p=1/2）。

---

## 4. 数值表（部分）

| p | AD | AD∘AD | DP | DP∘DP | DE | DE∘DE | ER | ER∘ER |
|---|-----|-------|-----|-------|-----|-------|-----|-------|
| 0.05 | 0.964 | 0.928 | 0.926 | 0.856 | 0.945 | 0.890 | 0.964 | 0.928 |
| 0.10 | 0.926 | 0.856 | 0.848 | 0.714 | 0.888 | 0.778 | 0.926 | 0.856 |
| 0.20 | 0.848 | 0.714 | 0.678 | 0.444 | 0.766 | 0.546 | 0.848 | 0.714 |
| 0.30 | 0.766 | 0.575 | 0.485 | 0.214 | 0.632 | 0.305 | 0.766 | 0.575 |
| 1/φ | 0.467 | 0.197 | 0.306 | 0.078 | 0.102 | **0** | 0.467 | 0.197 |
| 0.50 | 0.585 | 0.322 | **0** | **0** | 0.322 | 0 | 0.585 | 0.322 |

**注意**: AD 和 ER 列**完全相同**（验证 §3.1）。

---

## 5. 局限

- 仅 self-composition E∘E（同信道两段）；异信道复合 E_A ∘ E_B 未做
- log_neg 是 PPT-relaxed 上界，**不是** K_D；§3.1 的"等价"仅在 log_neg 下成立
- 标签 [SYN]（公式合成、解析推导，未走 R0.2 三方独立验证）
- **不**触及 umr 中 BSM 引起的额外结构变化（β.G4/G5/G3 仍 OPEN）

---

## 6. 相关产物

- 脚本: `scripts/qubit_log_neg_composition_E_circ_E.py`
- 图: `docs/research/figures/qubit_log_neg_E_circ_E.{png,pdf}`
- CSV: `docs/research/data/qubit_log_neg_E_circ_E.csv`
- 前置 memos: 
  - `docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md`
  - `docs/findings/qubit_log_neg_vs_K_D_tightness_2026-04-23.md`
  - `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md`

---

*2026-04-23 autonomous session. 复合信道 log_neg [SYN]。AD∘AD ≡ ER∘ER 是新结构观测。*
