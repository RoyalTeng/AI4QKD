# C 选项: log_neg PPT 上界应用到 MS-EB 协议族

**日期**: 2026-04-23（log_neg 框架延伸 C）  
**严谨性**: [SYN]（基于已验证 log_neg 公式 + 标准 SP achievable rate）  
**Scope**: BB84 + six-state（基于 `qkdx/protocols/bb84.py:bb84_channel` 的 symmetric depolarizing 模型）

---

## 0. 动机

β.G3 框架建立了 4 信道家族 log_neg 闭式公式。本 memo 把这套工具应用到 MS-EB 协议族（Sub-Q1 中已建模），评估 **PPT-relaxed 上界紧度 vs 已知 achievable rate**。

---

## 1. 协议→信道映射

依 `qkdx/protocols/bb84.py:bb84_channel`：

**BB84 / six-state**: symmetric depolarizing 等效信道, 参数 **p_depol = 4·QBER/3**

理由（CML 2016 §3）: BB84 把 QBER 拆为 Z-basis bit-flip + X-basis phase-flip + Y combined，对称 depolarizing 在三 Pauli 上各 1/3 → 单方向 QBER = 3p_depol/4 · 1/3 = p_depol/4 + ... 经累计 = 3p_depol/4。反推 p_depol = 4·QBER/3。

**MDI**: 双臂 BB84 复合 + linear-optic Bell BSM；效果上 effective QBER ≈ 4·arm_p/3 − 8·arm_p²/9（qkdx/protocols/mdi.py:242）。本 memo 只做 single-link BB84/6-state，MDI 留作后续。

---

## 2. log_neg 公式

equivalent depolarizing 信道下：

```
log_neg(BB84/6-state, QBER) = max(0, log₂(2 − 3·(4·QBER/3)/2)) 
                           = max(0, log₂(2 − 2·QBER)) 
                           = max(0, 1 + log₂(1 − QBER))
```

零点：QBER = 1（完全噪声）。在 QBER ∈ [0, 1] 全程 > 0。

---

## 3. 数据：log_neg vs Shor-Preskill achievable

| QBER | p_depol | log_neg (UB) | SP_BB84 (LB) | SP_6state (LB) | ratio BB84 | ratio 6st |
|------|---------|--------------|--------------|----------------|-----------|-----------|
| 0.00% | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.000 | 1.000 |
| 1.00% | 0.0133 | 0.9855 | 0.8384 | 0.9034 | 1.18 | 1.09 |
| 3.00% | 0.0400 | 0.9561 | 0.6112 | 0.7581 | 1.56 | 1.26 |
| 5.00% | 0.0667 | 0.9260 | 0.4272 | 0.6344 | 2.17 | 1.46 |
| 8.00% | 0.1067 | 0.8797 | 0.1956 | 0.4710 | **4.50** | 1.87 |
| **11.0%** | 0.1467 | 0.8319 | ≈ 0 | 0.3257 | **5000+** | 2.55 |
| **12.62%** | 0.1683 | 0.8054 | 0 | 0.2531 | ∞ | **3.18** |
| 15.0% | 0.2000 | 0.7655 | 0 | 0.1524 | ∞ | 5.02 |

**符号**: UB = upper bound (log_neg, PPT-relaxed); LB = lower bound (achievable Shor-Preskill).

---

## 4. 主要观测

### 4.1 log_neg 在操作 QBER 区**严重过松**

- BB84 阈值 QBER ≈ 11%: SP rate → 0, **log_neg 仍 0.83 bits** (5000× looser)
- Six-state 阈值 ≈ 12.62%: SP_6state → 0.25, log_neg = 0.81 (3.2× looser)
- 即便 1% QBER（接近理想）: log_neg 已 1.18× 高于 SP_BB84

意义: **log_neg 不能作为 BB84/six-state 的紧上界**。PPT-relaxed 视角"看到"的还有 entanglement，但 SP achievable rate 已被 error correction cost (2·h(QBER)) 吃光。

### 4.2 上下界差距来源

log_neg 与 SP rate 的差距源于：
- log_neg 是 **PPT-relaxed E_R 上界**：忽略了 LOCC distillation cost
- SP rate 是**只用 Z-基**测量的 achievable rate，扣了 EC cost 和 PA cost
- "真" K_D 在两者之间：D₁ ≤ K_D ≤ E_R^PPT ≤ log_neg

### 4.3 协议家族区分能力丧失

BB84 vs six-state 在等效 depolarizing 模型下使用同一信道（仅 sift 协议不同）→ **log_neg 给出完全相同的 UB**。但 SP rates 不同（六态利用了 3 MUB 的 PA tightening）。

意义: **log_neg 上界对协议优化盲目**。要分辨 BB84/六态/etc 的真正排序，必须用 K_D 级紧界（Devetak-Winter / Pirandola / R_max SDP / 等）。

---

## 4.4 修订: 用真 E_R (corrected analytic) 紧化对比

**[2026-04-23 后续]**: 修复 `e_r_depolarizing_analytic` bug 后, 对 BB84/six-state 等效信道直接计算真 E_R = E_R^PPT (= 1 - h(F))。

| QBER | log_neg (松UB) | **E_R (corrected, 真UB)** | SP_BB84 | SP_6state | **E_R/SP_BB84** | **E_R/SP_6state** |
|------|---------------|--------------------------|---------|-----------|----------------|-------------------|
| 1.00% | 0.9855 | **0.9192** | 0.8384 | 0.9034 | 1.10 | **1.02** |
| 3.00% | 0.9561 | 0.8056 | 0.6112 | 0.7581 | 1.32 | **1.06** |
| 5.00% | 0.9260 | 0.7136 | 0.4272 | 0.6344 | 1.67 | **1.13** |
| 8.00% | 0.8797 | 0.5978 | 0.1956 | 0.4710 | 3.06 | **1.27** |
| 11.0% | 0.8319 | 0.5001 | ≈0 | 0.3257 | ∞ | **1.54** |
| 12.62% | 0.8054 | 0.4531 | 0 | 0.2531 | ∞ | **1.79** |

**关键修订观察**:

1. **E_R 是显著紧的 UB** vs log_neg: 在 11% QBER 处 E_R = 0.50 vs log_neg = 0.83 (40% 紧化)
2. **六态更幸运**: E_R / SP_6state ≤ 1.8× 在阈值附近, **量级合理**
3. **BB84 仍有大 gap**: BB84 SP rate 在 11% 阈值已 0, 而 E_R = 0.50 — 这表明 **BB84 的 EC cost (2·h(QBER)) 是非紧的**, 真 K_D 应在 [SP_BB84, E_R] 之间, 离两端都有距离
4. **六态接近紧界**: SP_six-state 与 E_R 比率 1-1.8×, 表明 **六态 SP 公式本身已接近紧 K_D**（用 X-Y-Z 三 MUB 信息）

### 4.5 Sub-Q3 工具评估更新

修复 bug 后, **E_R^PPT (= 真 E_R for 2⊗2)** 是 qubit MS-EB 协议族的**正确紧 UB 工具**:
- 对 BB84: log_neg → E_R 紧化 ~40%, 但 BB84 SP 离 E_R 仍远 (说明真 K_D 估计需要 protocol-specific 工作)
- 对 six-state: E_R 与 SP 接近 (1-2×), **几乎闭合 UB-LB gap**

---

## 5. 对 Sub-Q3 的启示

### 5.1 上界候选优先级

按本 memo + 前置 §3.2:
- **log_neg**：解析快、永远是 UB，但**操作 QBER 区无用**（5000× 松）
- **E_R^PPT (SDP)**：紧度 ~30-50% 比 log_neg（β.G3 单臂 grid）
- **R_max (max-Rains, SDP)**：理论上 E_R^PPT 的 dual，应同量级
- **K_D 直接公式**：仅对 dephasing/depolarizing/erasure 已知
- **squashed entanglement**: 紧但 SDP 开销高

**结论**: 对于实用 QKD QBER 范围（< 12%），需要 **Sub-Q3 Phase 2 PDF 精读** 找文献中的 protocol-specific 紧界。log_neg 工具适合做 sanity check，但**不是研究主轴**。

### 5.2 已闭合的 vs 仍 OPEN 的

- **闭合**: 解析 log_neg 公式（4 信道，C1(c) SymPy 验证）+ Plenio 不等式自洽
- **闭合**: log_neg vs K_D 紧度量化（dephasing, depolarizing, erasure）
- **OPEN**: BB84-effective channel 的 K_D 解析（depolarizing K_D 在中等 QBER 已接近 SP rate?）
- **OPEN**: MDI / TF-QKD 的 log_neg 应用（type B 拓扑，需考虑 BSM）
- **OPEN**: β.G4/β.G5/γ.B.G1/γ.G3 结构 gap（不变）

---

## 6. 局限

- 仅 BB84 + six-state（symmetric depolarizing 假设）
- 未做 MDI / TF / decoy（type B 拓扑或 multi-mode source 需额外建模）
- log_neg 不是协议-specific 的紧界
- [SYN]（合成观测；公式来自单段验证 + 标准 SP rate；未走 R0.2 三方）

---

## 7. 相关产物

- 脚本: `scripts/log_neg_vs_msEB_key_rate.py`
- 图: `docs/research/figures/log_neg_vs_msEB_rate.{png,pdf}`
- CSV: `docs/research/data/log_neg_vs_msEB_rate.csv` (401 QBER 点)
- 前置 memos:
  - `docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md`
  - `docs/findings/qubit_log_neg_vs_K_D_tightness_2026-04-23.md`

---

*2026-04-23 autonomous session. C 选项 log_neg + MS-EB 应用 [SYN]。*
