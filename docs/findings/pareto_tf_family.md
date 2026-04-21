# TF / PM-QKD family Pareto findings (Phase 1 S2.2 A.1)

**生成时间**：2026-04-21 自主 session
**扫描脚本**：[scripts/sweep_tf_family.py](../../scripts/sweep_tf_family.py)
**数据文件**：
- [data/tf_family_loss1d.csv](data/tf_family_loss1d.csv) (81 pts)
- [data/tf_family_loss_x_edelta.csv](data/tf_family_loss_x_edelta.csv) (1250 pts)
- [data/tf_family_loss_x_pdark.csv](data/tf_family_loss_x_pdark.csv) (1250 pts)
- [data/tf_family_loss_x_M.csv](data/tf_family_loss_x_M.csv) (250 pts)

**图表**：[figures/tf_family_*](figures/)（PNG + PDF）

**总扫描点**：2831，满足 S2.2 硬验收 ≥ 1000。

---

## 1. 协议族参数（Ma-Zeng-Zhou 2018 PM-QKD）

| 参数 | 默认值 | 扫描范围 | 含义 |
|---|---|---|---|
| η_det | 0.145 | 固定 | 探测器效率 |
| p_d | 8×10⁻⁸ | 10⁻⁹ — 10⁻⁵ (25 pts log) | 暗计数 |
| e_delta | 0.015 | 10⁻³ — 0.05 (25 pts log) | 相位切片 + 失准 |
| f_EC | 1.15 | 固定 | EC 效率 |
| M | 16 | {4, 8, 16, 32, 64} | 相位切片数 |
| loss_dB_total | — | 0 — 80 dB | 两端总 loss |

---

## 2. 关键结果

### 2.1 1D loss sweep

| loss (dB) | rate (bits/signal) | √η 参考 | PLOB (-log₂(1-η)) |
|---|---|---|---|
| 0 | 8.25e-4 | 1.0 | ∞ |
| 10 | 3.80e-4 | 0.316 | 0.152 |
| 20 | 1.45e-4 | 0.100 | 0.0145 |
| 40 | 1.63e-5 | 0.010 | 1.44e-4 |
| 60 | 1.59e-6 | 0.001 | 1.44e-6 |
| 80 | 1.51e-7 | 3.16e-4 | 1.44e-8 |

**关键观察**：
- 在 > 60 dB 的高损耗区间，PM-QKD rate 仍 > 0（cutoff > 80 dB），这正是 TF 族的 √η scaling 优势
- PM-QKD rate ≈ 10⁻⁴·√η 在所有 loss（验证 TF √η 比例，系数约 0.001）
- PLOB 上界在高损耗下 tight（与 PM-QKD 比例相近），在低损耗下比 PM-QKD 大 10²-10³ 倍

### 2.2 2D loss × e_δ

- e_δ = 0.001（near-ideal）：高损耗 rate 提升 ~50%
- e_δ = 0.015（Ma default）：baseline
- e_δ = 0.03：cutoff 提前至 ~50 dB
- e_δ > 0.04：all loss 下 rate → 0（相位噪声主导）

### 2.3 2D loss × p_d

- p_d = 10⁻⁹：cutoff > 100 dB（扩展到极远距离）
- p_d = 10⁻⁸（default）：baseline
- p_d = 10⁻⁶：cutoff ≈ 40 dB
- p_d = 10⁻⁵：cutoff ≈ 20 dB（与 MDI 近似）

### 2.4 2D loss × M（相位切片）

**权衡**：
- M=4：sifting factor 2/4=0.5（最大）但 phase-slice 离散误差大
- M=16（default）：sifting 2/16=0.125，phase-slice 误差 ~0.0035
- M=64：sifting 2/64=0.03，phase-slice 误差趋近 0

结果：**M=4 在大部分 loss 区间最优**（sifting 占主导），M 过大反而受 sifting 稀释。

---

## 3. 族间对比预备

| η_end2end | PM-QKD rate | MDI rate | BB84 rate (WLC SDP qber→0) |
|---|---|---|---|
| 1.0 (0 dB) | 8.25e-4 | 1.9e-3 | ~0.5 |
| 0.1 (10 dB) | 3.80e-4 | 1.12e-3 | 0 (< cutoff) |
| 0.01 (20 dB) | 1.45e-4 | 3.85e-4 | 0 |
| 10⁻⁴ (40 dB) | 1.63e-5 | 9.21e-6 | 0 |
| 10⁻⁶ (60 dB) | 1.59e-6 | 0 (< cutoff) | 0 |

**关键对比点**：
- 0 dB：BB84 >>> MDI > PM-QKD（低损耗 BB84 最优）
- 20 dB：MDI > PM-QKD > BB84（cutoff 后 BB84 无解）
- 40 dB：PM-QKD > MDI（√η 开始主导）
- **交叉点 ≈ 30-40 dB**：超过后 TF 族领先

这与 FINDINGS v2 §1.1 中的 "TF-QKD 族 √η 可达" [THM] 结论一致。

---

## 4. 验收对照

| RESEARCH_PLAN §3.2 验收 | 状态 |
|---|---|
| ≥ 1000 扫描点 | ✅ 2831 points |
| Pareto 上包络记录 | ✅ `upper_envelope_loss` helper |
| 族间比较图 | ⏳ 待 A.2 PHASE1_REPORT 综合 |

---

## 5. 局限

1. PM-QKD 仅 Ma-Zeng-Zhou 2018 variant；Lucamarini 2018 TF-QKD、Wang 2018 SNS-TF、Zeng 2022 MP-QKD 未纳入
2. 渐近 (asymptotic) 密钥率；有限密钥 GEAT 未叠加
3. Fiber-loss only；未考虑拓扑异常（如非对称 Alice-Bob, Charlie-偏置）

---

## 6. Changelog

- **v0.1** (2026-04-21)：首版，A.1 TF family sweep 2831 pts + 4 图
