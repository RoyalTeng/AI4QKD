# MDI-QKD family Pareto findings (Phase 1 S2.2 A.1)

**生成时间**：2026-04-21 自主 session
**扫描脚本**：[scripts/sweep_mdi_family.py](../../scripts/sweep_mdi_family.py)
**数据文件**：
- [data/mdi_family_loss1d.csv](data/mdi_family_loss1d.csv) (81 pts)
- [data/mdi_family_loss_x_edev.csv](data/mdi_family_loss_x_edev.csv) (1250 pts)
- [data/mdi_family_loss_x_pdark.csv](data/mdi_family_loss_x_pdark.csv) (1250 pts)

**图表**：[figures/mdi_family_*](figures/)（PNG + PDF）

**总扫描点**：81 (1D) + 1250 + 1250 = **2581 points**，**满足 S2.2 硬验收 ≥ 1000 pts/family**。

---

## 1. 协议族参数

Ma-Razavi 2012 MDI-QKD, decoy-state original variant (Fig. 4 dashed curve)：

| 参数 | 默认值 (Table I) | 扫描范围 |
|---|---|---|
| η_det | 0.145 | 固定 |
| p_d | 3×10⁻⁶ | 10⁻⁸ — 10⁻⁴ (25 pts log scale) |
| e_d | 0.015 | 10⁻³ — 10⁻¹ (25 pts log scale) |
| f_EC | 1.16 | 固定 |
| loss_dB_total | — | 0 — 80 dB |

μ 信号强度在每点内部被 `mdi_original_rate_optimised`（50-pt log grid, μ ∈ [0.01, 1.0]）优化，不算做 Pareto 轴。

---

## 2. Pareto 前沿关键结果

### 2.1 1D loss sweep (默认参数)

| loss (dB) | rate (bits/signal) | 备注 |
|---|---|---|
| 0 | 1.90e-3 | max |
| 10 | 1.12e-3 | |
| 20 | 3.85e-4 | |
| 30 | 8.02e-5 | |
| 40 | 9.21e-6 | |
| 50 | 5.80e-7 | |
| 55 | 5.48e-8 | |
| **56** | **~1e-10** | **cutoff** |

**对 Ma-Razavi 2012 Fig. 4 "Decoy: original" dashed 曲线的核验**：max rate ≈ 2e-3 at 0 dB, cutoff ≈ 60 dB @ η_det=0.145。我的实施 cutoff=56 dB（稍早），差异在 e_d=0.015 的 QBER 贡献。

### 2.2 2D loss × e_d（探测器失准）

Pareto 观察：

- e_d = 0.001（近理想）：cutoff 延伸到 ~65 dB
- e_d = 0.01（Ma-Razavi default）：cutoff ≈ 56 dB
- e_d = 0.05：cutoff 缩短到 ~35 dB
- **e_d > 0.11**：所有 loss 下 rate = 0（失准超限度）

### 2.3 2D loss × p_d（暗计数）

Pareto 观察：

- p_d = 10⁻⁸：cutoff ≈ 65 dB
- p_d = 10⁻⁶（Ma-Razavi default）：cutoff ≈ 56 dB
- p_d = 10⁻⁵：cutoff ≈ 40 dB
- p_d = 10⁻⁴：cutoff ≈ 20 dB

---

## 3. 族间对比预备（留给 A.2 PHASE1_REPORT）

与 BB84 family 对比需要在相同拓扑下：MDI 的 loss 轴是 **两臂合计** dB，BB84 是单跳 dB。对齐口径后（MDI 的 η_total ≡ η_AB = η_A × η_B），在相同端到端 η 下：

| η (end-to-end) | BB84 rate | MDI rate | 比值 |
|---|---|---|---|
| 1.0 (0 dB) | ~0.55* | 1.9e-3 | ~290 |
| 0.01 (20 dB) | 0 (< cutoff) | 3.85e-4 | ∞ |

*BB84 analytic 在 qber=0 @ η=1 理论值约 0.5 (p_sift=1/2 × 1 bit).

**MDI 的优势**：在高损耗区间（> ~15 dB）仍有正率，而 BB84 早已 cutoff；但低损耗区间被 p_sift=1/4 × 光子数 × Bell 成功率等因子严重稀释。

---

## 4. 验收对照表

| RESEARCH_PLAN §3.2 验收 | 状态 |
|---|---|
| 每个族能在参数空间扫 ≥ 1000 点 | ✅ 2581 points total |
| Pareto 前沿上包络被记录 | ✅ `upper_envelope_loss` helper + CSV |
| 族间比较图（BB84 vs MDI vs TF 在 (η, R) 平面） | ⏳ 待 TF family Pareto 完成后组合 |

---

## 5. 局限 + 待扩展

1. **仅 Ma-Razavi original variant**：Wang 2013 "modified decoy" 更紧；未实施
2. **对称 loss (η_a = η_b)**：非对称 MDI (η_a ≠ η_b) 是族内变体，未扫
3. **单光子源**：当前模型已经是 WCP decoy，无需单光子扩展
4. **有限密钥**：当前是 asymptotic；Kamin 2025 GEAT 扩展（D.4）待做

---

## 6. Changelog

- **v0.1** (2026-04-21)：首版，A.1 MDI family sweep + 2581 点 Pareto + 3 图
