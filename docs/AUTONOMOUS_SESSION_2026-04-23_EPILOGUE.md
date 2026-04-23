# 2026-04-23 Autonomous Session — Epilogue (β.G3 闭环 + log_neg 框架延伸)

**状态**: 等待用户审阅
**前置文档**: `docs/AUTONOMOUS_SESSION_2026-04-23_CONCLUSIONS.md` (v0.2, §7 β.G3 闭环)
**新增范围**: β.G3 三方验证完成后的横向 log_neg 框架延伸

---

## 1. 工作时序（commits）

### 1.1 β.G3 解析推导闭环（commits `33af74d` → `3035c9c`）

| commit | 内容 |
|--------|------|
| `33af74d` | SymPy C1(c) 验证记录（6 项断言全过） |
| `300945d` | C2 用户签字确认数学正确性，标签保持 [SYN] |
| `bcdd513` | session conclusions §7 闭环追加 |
| `3035c9c` | THM-anchor 文献搜索 — 无直接锚点 |

**结果**: β.G3 数学正确性三方独立验证完成。标签 [SYN]（永久），[COROLLARY] 升级路径暂闭（无外部 THM 锚点）。

### 1.2 log_neg 框架横向延伸（commits `439939c` → `245edc8`）

| commit | 内容 |
|--------|------|
| `439939c` | 3 qubit 信道 log_neg 解析公式（AD, dephasing, depolarizing）+ 7 tests |
| `514d949` | 3 信道对比图 + 1001 点 CSV |
| `c082ad3` | log_neg vs K_D / E_R 紧度量化（dephasing + depolarizing） |
| `e9c28b9` | AD 综合图：log_neg + E_R^PPT + Pirandola |
| `e1e73e4` | 加 erasure 信道为第 4 家族 + 4 信道紧度对比 |
| `bc7c0e8` | Plenio 不等式 log_neg ≥ K_D 数值 sanity test |
| `245edc8` | 复合 E∘E 退化 + AD∘AD ≡ Erasure∘Erasure 结构观测 |

---

## 2. 关键科学产出

### 2.1 β.G3 三方验证（"path 1 完成"）

- **数学**: log_neg(E_AD(η)) = log₂(1+η)、η_c = 1/φ（精确）
- **C1(c)**: SymPy 符号验证（`docs/workflow/beta-G3-analytic-proof-review/sympy-c1c-verification.md`）
- **C2**: 用户 2026-04-23 签字
- **C3**: dev-reviewer R2 PASS
- **标签**: [SYN]（永久；无外部 THM 锚点不能升 [COROLLARY]）

### 2.2 4 qubit 信道 log_neg 闭式公式（"框架延伸"）

| 信道 | log_neg | 零点 |
|------|---------|------|
| AD (γ=damping) | log₂(2 − γ) | γ=1 |
| Dephasing (p=Z-flip) | log₂(1 + \|1 − 2p\|) | p=1/2 |
| Depolarizing (p) | max(0, log₂(2 − 3p/2)) | p=2/3 |
| Erasure (p) | log₂(2 − p) | p=1 |

所有公式 SymPy 验证 + 数值 SDP 交叉验证（9 tests pass）。

### 2.3 紧度观测（PPT 松弛代价）

log_neg vs 真 K_D / E_R 的差距：

- **Erasure**: log_neg − K_D ∈ [0.01, 0.09] bits（**接近紧**）
- **Dephasing**: gap ∈ [0, 0.4] bits（中等松）
- **Depolarizing**: gap ∈ [0, 0.63] bits（极松，PPT > SEP boundary 在 p ∈ [4/9, 2/3]）

### 2.4 复合 E∘E 退化分析（**新结构观测**）

发现：**AD∘AD 与 Erasure∘Erasure 给出完全相同的 log_neg 函数** log₂(1 + (1−p)²)。

**意义**: 在 PPT-relaxed 上界视角下两类信道的两段复合不可区分；但实际 K_D 行为完全不同 — log_neg 失去区分能力。

### 2.5 Plenio 不等式数值确认

log_neg ≥ K_D / E_R 在 600 grid points × 3 信道全部满足（$10^{-12}$ 精度）。

---

## 3. 测试覆盖

`TestAnalyticLogNegFormulas` 共 **9 tests**，全部 pass，无 MOSEK 依赖：

1. AD 解析 vs 数值
2. Dephasing 解析 vs 数值
3. Depolarizing 解析 vs 数值
4. 边界值（identity极限）
5. 全噪声边界（PPT/erased）
6. Dephasing p ↔ 1-p 对称
7. 参数越界 raises ValueError
8. Plenio 不等式（200 × 3 channels）
9. Erasure 公式 vs 6×6 PT 数值

`TestLogNegAmplitudeDampingAnalytic` 7 tests（β.G3 原有），全过。

总：16 个 analytic-log_neg 测试，0.36s pure numpy。

---

## 4. 文档与产物清单

### 4.1 Findings memos

- `docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md` — 4 信道公式总览
- `docs/findings/qubit_log_neg_vs_K_D_tightness_2026-04-23.md` — 紧度对比
- `docs/findings/qubit_log_neg_composition_2026-04-23.md` — 复合 E∘E 分析

### 4.2 脚本（可重跑）

- `scripts/sympy_log_neg_qubit_channels.py` — SymPy 验证 AD/dp/de
- `scripts/sympy_log_neg_erasure.py` — SymPy 验证 erasure
- `scripts/qubit_log_neg_three_channels_compare.py` — 4 信道对比图
- `scripts/qubit_log_neg_vs_E_R_tightness.py` — 紧度对比图
- `scripts/AD_log_neg_vs_E_R_PPT_combined.py` — AD 综合图
- `scripts/qubit_log_neg_composition_E_circ_E.py` — 复合分析

### 4.3 数据 CSV

- `docs/research/data/qubit_log_neg_three_channels.csv` (1001 pts × 4 cols)
- `docs/research/data/qubit_log_neg_vs_K_D_tightness.csv` (1001 pts × 9 cols)
- `docs/research/data/qubit_log_neg_E_circ_E.csv` (1001 pts × 8 cols)

### 4.4 图

- `docs/research/figures/qubit_log_neg_three_channels.{png,pdf}` — 4 曲线对比
- `docs/research/figures/qubit_log_neg_vs_K_D_tightness.{png,pdf}` — 3 panel 紧度
- `docs/research/figures/AD_log_neg_vs_E_R_PPT.{png,pdf}` — AD 综合
- `docs/research/figures/qubit_log_neg_E_circ_E.{png,pdf}` — 4 panel 复合

### 4.5 代码增量

- `qkdx/numerics/upper_bound.py`: +4 函数（约 80 行）
- `tests/test_numerics/test_upper_bound.py`: +9 测试（约 130 行）

---

## 5. 局限与未做项

### 5.1 仍 OPEN（不在 AI 边界内）

- β.G4 / β.G5 / γ.B.G1 / γ.G3 — 4 个 umr 结构 gap，需用户研究级 PDF 精读
- AD 信道的 K_D 解析（无封闭式，本 session 未涉及）
- 异信道复合 E_A ∘ E_B（混合）
- 多于 2 段的复合（n-fold chain）

### 5.2 标签状态

所有新公式 [SYN]（教科书级计算 + SymPy 验证 + 数值复核 + Plenio 不等式自洽，但无 R0.2 三方验证流程）。
β.G3 是唯一过 C1(c)+C2+C3 三方验证的结论。

---

## 6. 用户决定点

下一步研究方向（您指令）：

| 选项 | 描述 | AI 边界内? |
|------|------|----------|
| A | 用户精读 Khatri-Wilde 寻找 [THM] 锚点 → β.G3 升 [COROLLARY] | ❌ 需用户 |
| B | 异信道 / n-fold 复合分析 | ✅ |
| C | 把这套 log_neg 工具应用到 MS-EB 协议族（BB84/MDI/etc）的紧度评估 | ✅ |
| D | 切换 RESEARCH_PLAN Phase 2 其他方向 | 部分需用户 |
| E | 暂停自主，等待您 review 本日所有 commits | — |

**默认建议**: E（review 后再决定方向）— 本回合产出已较丰富，需要 user oversight。

---

## 8. 后续延伸（v0.2 追加）

### 8.1 B + C 选项执行（commits `84b97e9`, `4af93e4`）

- **B (n-fold + 异信道)**: 4 信道 self-composition 递归，AD^n ≡ Erasure^n 全 n 等价（PPT 视角）
- **C (MS-EB 应用)**: BB84/six-state 等效 depolarizing(p=4·QBER/3); log_neg 在 11% 阈值处 5000× SP_BB84

### 8.2 E_R^PPT SDP 全面对比（commit `ac3947f`）

- 19 SDP 点 across 3 信道（erasure dim_B=3 OOM）
- **强观察**: dephasing E_R^PPT ≡ K_D (PLOB Eq.39) 机器精度匹配

### 8.3 重要 bug 发现 + 修复（commit `b4efaae`）

数据驱动地发现 `e_r_depolarizing_analytic` 公式错（用了 `(1-F)·log₂(d²-1)` 应是 `(1-F)·log₂(d-1)`）：
- 修复前误称"在 p ∈ [0.27, 2/3] 内 E_R = 0"
- 修复后 E_R = 1 - h(F) for d=2，与 SDP 完全匹配
- 添加 2 个 regression 测试; 11/11 pass
- 同时修订 `qubit_log_neg_vs_K_D_tightness_2026-04-23.md` (commit `5579e0f`)

### 8.4 BB84/six-state 真 E_R 紧化（commit `01935fa`）

修复 bug 后用真 E_R = 1-h(F) 评估:
- BB84 阈值 11% 处: log_neg 0.83 → E_R 0.50 (紧化 40%)
- **六态接近 UB-LB 闭合**: E_R / SP_six-state ≤ 1.8× 在阈值附近

### 8.5 AD K_D analytic（commit `73bd18f`）

新函数 `K_D_amplitude_damping_degradable(γ)` for γ ≤ 1/2 (Caruso-Giovannetti-Holevo 2014):
- E_R^PPT / K_D ∈ [1.03, 1.52]（接近紧 UB!）
- log_neg / K_D ∈ [1.16, 2.33]（中等松）
- γ > 1/2 anti-degradable: Q = 0, K_D 真正 OPEN

### 8.6 累计测试覆盖

- TestAnalyticLogNegFormulas: **13/13 tests pass**（含 SDP cross-validation, AD K_D, Plenio）
- TestLogNegAmplitudeDampingAnalytic: 7/7（β.G3 原有）
- 总：20 个 analytic-related tests

### 8.7 Sub-Q3 工具评估更新

| 信道 | 最紧已知 UB | 与 K_D gap |
|------|---|---|
| AD (γ ≤ 1/2) | E_R^PPT (SDP) | 1.03-1.52× K_D |
| AD (γ > 1/2) | E_R^PPT (SDP) | K_D unknown |
| Dephasing | E_R^PPT (= PLOB Eq.39) | 紧 |
| Depolarizing | E_R^PPT (= 1-h(F)) | 紧 |
| Erasure | log_neg (analytic) | gap < 0.09 bits |

---

## Changelog

- **v0.2** (2026-04-23 evening): §8 追加 — B/C 选项 + E_R^PPT SDP + bug 修复 + AD K_D + BB84 紧化
- **v0.1** (2026-04-23): 首稿，本回合自主 session 闭环 + log_neg 框架横向延伸总结。等待用户审阅。
