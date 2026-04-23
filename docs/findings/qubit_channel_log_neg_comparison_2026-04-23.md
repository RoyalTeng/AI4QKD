# Qubit 信道 log-negativity 解析公式对比

**日期**: 2026-04-23（β.G3 框架横向扩展）  
**严谨性**: [SYN] — 三个公式由 SymPy 符号验证 + 数值 SDP 双向核对  
**范围**: 三个单 qubit 信道的 Choi 态 log-negativity 封闭式  

---

## 0. 动机

β.G3 session 已为 **amplitude damping** 建立解析公式 log_neg(η) = log₂(1+η)（即 log₂(2-γ)）。本 memo 把同一方法扩展到 **dephasing** 和 **depolarizing** 两个典型 qubit 信道，为 Sub-Q3 上界工作提供横向数据。

所有三个公式均属**教科书级计算**，**不是**文献定理级结论；标签保持 [SYN]。

---

## 1. 公式总览

| 信道 | 参数 | Choi 的 PT 迹范数 | log_neg 公式 | 范围 | 零点 |
|------|------|-------------------|-----------|------|------|
| **Amplitude damping** (γ=damping prob) | γ ∈ [0, 1] | 2 − γ | `log₂(2 − γ)` | 永远非零 (γ < 1) | γ=1 |
| **Dephasing** (p=Z-flip prob) | p ∈ [0, 1] | 1 + \|1 − 2p\| | `log₂(1 + \|1 − 2p\|)` | 对称 p ↔ 1−p | p = 1/2 |
| **Depolarizing** (p=noise param) | p ∈ [0, 1] | max(2 − 3p/2, 1) | `max(0, log₂(2 − 3p/2))` | PPT for p ≥ 2/3 | p = 2/3 |

三个公式均在 `qkdx/numerics/upper_bound.py` 作为 `analytic_log_neg_*` 提供。

---

## 2. 推导概要

所有推导遵循同一模式（§2 of β.G3 memo）:

1. **Choi 态**: ρ = (I ⊗ E)(|Φ⁺⟩⟨Φ⁺|)（由 Kraus 运算子显式构造）
2. **偏转置 T_B**: 4×4 矩阵，块对角在 {|00⟩,|11⟩} 和 {|01⟩,|10⟩} 子空间
3. **特征值集**: 由两个 2×2 块分别求解
4. **迹范数**: ∑ \|λᵢ\|
5. **log-negativity**: E_N := log₂(迹范数)

### 2.1 Amplitude damping (AD)

已在 `beta_G3_golden_ratio_crossover_2026-04-23.md` §2 完整推导。  
以**透射率 η = 1 − γ** 参数化时，log_neg = log₂(1 + η)。

### 2.2 Dephasing

- Kraus: K₀ = √(1−p)·I, K₁ = √p·Z
- Choi = (1−p)|Φ⁺⟩⟨Φ⁺| + p|Φ⁻⟩⟨Φ⁻|（Bell 分解）
- PT 特征值: {1/2, 1/2, 1/2 − p, p − 1/2}
- 迹范数 = 1 + \|1 − 2p\|
- 对称性: p ↔ 1 − p（因为 Z 的 involution 性质）

### 2.3 Depolarizing

- Kraus: q₀·I, q₁·X, q₁·Y, q₁·Z 其中 q₀² = 1 − 3p/4, q₁² = p/4
- Choi = (1 − p)|Φ⁺⟩⟨Φ⁺| + (p/4)·I₄（Werner/isotropic 形式）
- Bell 保真度 F = 1 − 3p/4
- PT 特征值: (1/2 − p/4) × 3 (on symmetric subspace), (3p/4 − 1/2) × 1 (on antisymmetric)
- 迹范数 = 2 − 3p/2（对 p < 2/3），否则 1（PPT）
- PPT 阈值 p = 2/3 ↔ F = 1/2（Horodecki et al. 1996 PPT=SEP for 2⊗2）

---

## 3. 验证

### 3.1 SymPy 符号验证（C1(c) 候选）

脚本: [`scripts/sympy_log_neg_qubit_channels.py`](../../scripts/sympy_log_neg_qubit_channels.py)

验证的 6 项断言（三个信道，每个 Choi 态 + PT + 特征值 + 迹范数）全部 `True`。

### 3.2 数值 SDP 交叉验证

测试类 `TestAnalyticLogNegFormulas`（7 tests，均 pass，无 MOSEK 依赖）:

- `test_amplitude_damping_analytic_matches_numerical`: 7 点 γ ∈ {0, 0.1, ..., 1}
- `test_dephasing_analytic_matches_numerical`: 7 点 p ∈ {0, 0.1, ..., 1}
- `test_depolarizing_analytic_matches_numerical`: 8 点 p ∈ {0, 0.1, ..., 2/3, ..., 1}
- `test_boundary_values` / `test_full_noise_boundary` / `test_dephasing_symmetry`
- `test_invalid_parameter_raises`

所有解析 vs 数值偏差 < 1e-9（机器精度）。

---

## 4. 对 Sub-Q3 上界工作的意义

### 4.1 PLOB 对比（非 bosonic）

- PLOB 原公式 −log₂(1 − η) 严格专适用于 **bosonic pure-loss**
- Qubit 信道的类 PLOB 分析改用 **quantum capacity / private capacity**（各有封闭式）
- log_neg 提供**更宽松的**类 PPT 上界（永远 ≥ 1-LOCC rate）

### 4.2 Amplitude damping vs Dephasing vs Depolarizing 的对比

- **AD**: log_neg 永远 > 0（严格下界 log₂(1) = 0 仅在 γ=1 时取到）
- **Dephasing**: log_neg 在 p=1/2 降到零；p=1 又回升
- **Depolarizing**: log_neg 在 p=2/3 之后为零（PPT）

这说明 **信道家族对 PT-based 上界的"噪声容忍"差别巨大**：
- Depolarizing 最容易"失去"PT-based 绑定力
- AD 最难（能量不对称 Kraus 让 entanglement 保留）

### 4.3 对 umr 拓扑的启示

若 umr 内两臂都用 **depolarizing**（p 高），双臂 log-neg 和可能远低于 Pirandola/PLOB。但 β.G3 的 bottleneck 是 structural gap（β.G4, β.G5），**不是**具体信道的数值紧度。

本 memo 提供的公式**仅在 Sub-Q3 Phase 2 数值精读阶段**（比较 multiple achievable 下界族 vs upper bound candidate 族）有直接用途。

---

## 5. 限制

- 仅 qubit 信道；**不扩展到** bosonic pure-loss（§4.1）
- 仅 Choi 态 log-neg；**不**等同于信道 max-Rains / Rains bound / E_R^PPT
- **不**提供 additivity 保证（E_N 是 additive 的 — 这是一个已知 [THM]，Plenio 2005 证 — 但这里不依赖）
- [SYN] 标签，不升级到 [COROLLARY]（无外部 THM 锚点，同 β.G3 §2 结论）

---

## 6. 相关产物

- 代码: `qkdx/numerics/upper_bound.py:analytic_log_neg_{amplitude_damping,dephasing,depolarizing}`
- 测试: `tests/test_numerics/test_upper_bound.py::TestAnalyticLogNegFormulas`（7 tests，pass）
- SymPy 脚本: `scripts/sympy_log_neg_qubit_channels.py`
- 前置 memo: `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md`

---

*2026-04-23 autonomous session. 三公式 [SYN]。SymPy C1(c) + 数值 SDP 交叉已验证；无 C2/外部 THM。*
