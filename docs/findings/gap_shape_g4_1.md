# Gap 定量形状（G4.1 Sub-Q4 §5.1 初稿）

**版本**：v0.1 [CONJ 级]
**日期**：2026-04-21
**状态**：[CONJ] — 依赖 U3.6 三候选路径 α/β/γ 的形式化尚未完成
**数据**：[../research/data/gap_shape.csv](../research/data/gap_shape.csv)
**图**：[../research/figures/](../research/figures/)（`gap_shape.png` / `gap_shape.pdf`）

---

## 0. 重要免责

本 gap 分析的**所有 upper bound 候选都是 [CONJ] 级**（见 [docs/proofs/upper_bound_msen.md §3](../proofs/upper_bound_msen.md)）。本文档给出 gap 的**形状**（基于候选上界假设），**不**给出 gap 的 [THM] 级数值。

FINDINGS v2 §4.2 的红线被严格遵守：
> Sub-Q4 归因 α/β/γ 应在 Sub-Q3 完成之后基于定理级上界重新启动，不以本 interim 为预定位

本文档**只做 gap 形状**，**不做归因** A/B/C。

---

## 1. 参与 gap 计算的数据

### 1.1 下界（Sub-Q2 Pareto）

- 来源：[../research/data/tf_family_loss1d.csv](../research/data/tf_family_loss1d.csv)
- 协议：PM-QKD (Ma-Zeng-Zhou 2018) asymptotic rate
- 默认参数：η_det=0.145, p_d=8e-8, e_δ=0.015, M=16, f_EC=1.15

### 1.2 上界候选（[CONJ] 级）

| 候选 | 公式 | 严谨性分级 | 原始拓扑 |
|---|---|---|---|
| **A** PLOB 最弱 edge | $-\log_2(1 - \min(\eta_A, \eta_B))$ | [CONJ for umr under Assumption DP] | 单信道两方 |
| **B** Pirandola N=1 | $-\log_2(1 - \sqrt{\eta_\text{end2end}})$ | [CONJ for umr] | trusted-relay chain |
| **C** E_R^PPT amp-damp | numerical SDP on qubit amp-damp with $\gamma = 1-\eta_\text{arm}$ | [CONJ + qubit abstraction] | qubit-level |

**对称 umr 情形**（$\eta_A = \eta_B = \eta_\text{arm}$，$\eta_\text{end2end} = \eta_\text{arm}^2$）候选 A 与 B 公式一致。

---

## 2. 数值结果

### 2.1 上下界 vs loss

| loss (dB) | TF-PM-QKD LB | UB cand A/B | UB cand C (E_R^PPT) | PLOB direct (ref, non-umr) |
|---|---|---|---|---|
| 0 | 8.25e-4 | ∞ (η_arm=1; script uses 1e-30 floor → 99.66) | 1.000 | ∞ |
| 10 | 2.50e-4 | 0.5484 | 0.1934 | 0.1520 |
| 20 | 7.78e-5 | 0.1520 | 0.0616 | 0.0145 |
| 30 | 2.44e-5 | 0.04636 | 0.0202 | 0.00145 |
| 40 | 7.67e-6 | 0.01450 | 0.0065 | 1.44e-4 |
| 60 | 6.96e-7 | 0.00144 | 0.0007 | 1.44e-6 |
| 80 | 9.47e-9 | 1.44e-4 | 9.9e-5 | 1.44e-8 |

（values from [../research/data/gap_shape.csv](../research/data/gap_shape.csv); audit 2026-04-21 corrected 10 dB row previously misrecorded as 1.2073 → 0.5484）

### 2.2 Gap 比值（UB / LB）

| loss (dB) | candidate A/B / TF | candidate C / TF |
|---|---|---|
| 10 | ~2200× | ~770× |
| 20 | ~1950× | ~790× |
| 40 | ~1890× | ~850× |
| 60 | ~2080× | ~1000× |
| 80 | ~15200× | ~10500× |

**关键观察**：
1. **Gap ratio 相对稳定** in 20-60 dB 区间，~800-1000× （候选 C）、~1900-2100× （候选 A/B）
2. 候选 A/B（符号闭形）比候选 C（SDP 数值）**松 2-3×**
3. 低损耗区 (< 10 dB) gap 极大，但候选 A/B 在 0 dB 发散
4. 80 dB 区的 ratio 变大是因为 TF LB 急剧下降（接近 cutoff）

### 2.3 Gap 曲线 log-log 行为（**conditional sensitivity analysis only**）

**NOTE** — 本小节是 **如果** 某候选路径升级到 [THM] 时的 **sensitivity analysis**，**严格不**构成 Sub-Q4 归因结论。§0 disclaimer 保持有效。

在 log-log 下（loss_dB 是 x 轴）：
- TF LB 的 slope 约为 **-1/2**（对应 √η scaling）—— [SYN] 来自 Ma-Zeng-Zhou 2018 可达性
- UB cand A/B 的 slope 约为 **-1**（对应 η scaling）—— [CONJ], 依赖 Log 07 Assumption DP
- 两斜率差 → gap 形状在 log scale 下**线性发散**

**Conditional statement only（不 promote 到归因）**：若 Log 07 路径 γ 能把 candidate A/B 升级到 [THM]，则**gap shape 将与情况 B（可构造超越 √η 的协议）一致**。当前 [CONJ] 级，**不**据此做归因。

---

## 3. 与 FINDINGS v2 的对齐

FINDINGS v2 §1.1 [SYN] 判断："在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下，最可能的紧 scaling 为 $\sqrt{\eta_{AB}}$"。

本 G4.1 初稿给出的数值 gap：
- **支持 FINDINGS v2 的 [SYN]**：TF 族可达 √η，候选 A/B 上界为 η^{1/2}·(1+O(η^{1/2}))（对称情形），两者同阶
- **暴露 gap**：候选 A/B 给出的常数 $-\log_2(1-\sqrt{\eta}) \approx \sqrt{\eta}/\ln 2$ 约 1.44·√η，vs TF-PM-QKD 的 ~10⁻³·√η。**常数因子差 1000×**
- **可能的解读**：要么候选 A/B 的 1.44 常数过松（需更紧的上界），要么 TF-PM-QKD 的 10⁻³ 常数过紧（可构造更优协议）
- **这是 Sub-Q4 归因的原始数据**，**不是归因结论**

---

## 4. Limitations

1. **所有上界候选 [CONJ] 级**。在 Log 07 路径 γ 升级到 [THM] 之前，本分析只能说"gap 形状是这样的"，不能说"gap 真实值是这样"。
2. **单光子 qubit-abstraction 假设**（候选 C）：amp-damping channel 不是 bosonic pure-loss 的 qubit analog；qubit-level 上界可能系统性低估真 bosonic E_R。
3. **协议族仅 PM-QKD**：TF family 还有其他变体（SNS-TF, TF-QKD 原型, MP-QKD 等），未纳入。
4. **无限密钥情形**：目前 gap 是 asymptotic；有限密钥 gap 更大。

---

## 5. 下一步（G4.2 Sub-Q4 §5.2 触发条件）

触发条件：**U3.8 接缝报告** + **Log 07 路径 γ 形式化完成** + 至少一条候选升级到 [COROLLARY]。

届时可基于这份初稿做：
- 归因 A/B/C 判定
- "新协议搜索目标 = 填补 gap 中某位置"的定量指令

当前状态：前两个条件都**未满足**。归因工作**待命**。

---

## Changelog

- **v0.1**（2026-04-21 autonomous session）：首稿 [CONJ] 级 gap 形状分析，基于 PHASE1_REPORT.md 的 TF lower bound + U3.6 / U3.7 的三候选上界。
