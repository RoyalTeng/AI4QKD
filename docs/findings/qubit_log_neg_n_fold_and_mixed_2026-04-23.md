# n-fold + 异信道复合 log-negativity 分析

**日期**: 2026-04-23（log_neg 框架延伸 B）  
**严谨性**: [SYN]（基于已验证单段公式的代入；异信道部分纯数值 PT）  
**Scope**: n-fold E^n（4 信道家族）+ 异信道 E_A ∘ E_B（3 代表对）

---

## 1. n-fold 复合（self-composition）

### 1.1 参数递归规则

**关键观测**：4 信道家族在 n-fold 复合下分两类:

| 类别 | 信道 | 递归 |
|------|------|------|
| **A 类（multiplicative "保留"）** | AD, Depolar, Erasure | `p_n = 1 − (1−p)^n` |
| **B 类（Z-parity）** | Dephasing | `p_n = (1 − (1−2p)^n) / 2` |

A 类对应"以概率 (1−p) 保留单段输入" → n 段后保留概率 (1−p)^n。  
B 类是 Z² = I 的离散 parity 累积（指数衰减到 1/2，不到 1）。

### 1.2 PPT 零点 vs 链长

各信道 log_neg = 0 的最小 n：

| 信道 | 零点条件 | 闭式 n_crit |
|------|---------|-----------|
| AD | γ_n = 1 → 永不（除 γ=1）| ∞ |
| Dephasing | p_n = 1/2 → 永不（除 p=1/2）| ∞ |
| Depolarizing | p_n ≥ 2/3 ↔ (1−p)^n ≤ 1/3 | `⌈log(1/3)/log(1−p)⌉` |
| Erasure | p_n = 1 → 永不（除 p=1）| ∞ |

**Depolarizing 是唯一在有限 n 进入 PPT** 的信道（数值表）：

| p | n_crit |
|---|--------|
| 0.05 | 22 |
| 0.10 | 11 |
| 0.20 | 5 |
| 0.30 | 4 |
| 0.50 | 2 |

意义：即便 depolarizing 单段噪声很弱（p=0.05），22 段后 PPT-relaxed 上界已"看不到"任何 entanglement。这是 **PPT 在长链下的早期失效**。

### 1.3 AD^n ≡ Erasure^n 的延伸

§3.1 of `qubit_log_neg_composition_2026-04-23.md` 已观察到 AD∘AD ≡ Erasure∘Erasure。

由 §1.1 表，**对所有 n**：AD 和 Erasure 共享递归 + 共享单段公式（log₂(2−p)）→ AD^n 和 Erasure^n 给出**完全相同** log_neg 函数。

数值验证（p=0.10）:
| n | AD^n | Erasure^n |
|---|------|-----------|
| 1 | 0.9260 | 0.9260 |
| 5 | 0.6695 | 0.6695 |
| 10 | 0.4315 | 0.4315 |
| 20 | 0.1655 | 0.1655 |

完全一致。这是 PPT-relaxed 视角下两类完全不同信道（AD = energy 衰减，erasure = 离散 flag）的"信息论同构"。

---

## 2. 异信道复合 E_A ∘ E_B

### 2.1 方法

无解析公式；数值方法：
1. `compose_kraus(K_A, K_B) = {K_A · K_B for K_A in family_A, K_B in family_B}`
2. 由复合 Kraus 集构造 Choi 态（`choi_state_from_kraus`）
3. PT + 特征值绝对值之和 = 迹范数 → log_neg

### 2.2 三对代表

固定**等噪声** diagonal（参数同步增长 t = γ = p）下：

| 复合 | t=0.10 | t=0.30 | t=0.50 |
|------|--------|--------|--------|
| AD ∘ Dephasing | 0.751 | 0.278 | 0.000 |
| AD ∘ Depolarizing | 0.792 | 0.429 | 0.176 |
| Dephasing ∘ Depolarizing | 0.668 | 0.171 | 0.000 |

### 2.3 观测

- **Dephasing 噪声更"破坏" log_neg**：AD ∘ Dephasing < AD ∘ Depolarizing 在所有 t（dephasing 直接攻击 Z-coherence，depolarizing 是各向同性）
- **Dephasing ∘ Depolarizing 在 t≥0.5 提前为零**：两个噪声叠加加速 PPT 失效
- **AD ∘ Depolarizing 在 t=0.5 仍 > 0**：log₂(2-0.5) ≈ 0.585 是 AD 单段贡献，与 depolarizing 进 PPT (p=0.5 < 2/3) 加合后仍非零

---

## 3. 局限

- 异信道复合 log_neg **无解析闭式**（数值 only）
- 复合**顺序敏感**：E_A ∘ E_B ≠ E_B ∘ E_A 一般成立（本 memo 用 E_A 后 E_B 先）
- erasure 复合需要 dim_B = 3 → 与 qubit-only 框架不兼容，未做
- [SYN]（数值数据 + 单段公式合成；无 R0.2 三方验证）

---

## 4. 相关产物

- 脚本: `scripts/qubit_log_neg_n_fold_composition.py`
- 脚本: `scripts/qubit_log_neg_mixed_composition.py`
- 图: `docs/research/figures/qubit_log_neg_n_fold.{png,pdf}`
- 图: `docs/research/figures/qubit_log_neg_mixed_composition.{png,pdf}`
- CSV: `docs/research/data/qubit_log_neg_n_fold.csv` (4 families × 5 p × 20 n = 400 rows)
- CSV: `docs/research/data/qubit_log_neg_mixed_composition.csv`
- 前置 memos: `qubit_log_neg_composition_2026-04-23.md`

---

*2026-04-23 autonomous session. n-fold + mixed composition log_neg 分析 [SYN]。*
