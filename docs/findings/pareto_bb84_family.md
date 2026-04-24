# BB84 Family Pareto Findings — Phase 1 S2.2 Week 4-8 起稿

**Version**: v0.1
**Date**: 2026-04-19
**Data source**: [bb84_family_sweep.json](bb84_family_sweep.json)
**Code**: [qkdx/sweeps/bb84_family_sweep.py](../../qkdx/sweeps/bb84_family_sweep.py)

---

## 1. Scope

**已纳入的变体**:
- F1 BB84(1-D sweep 在 QBER)
- F2 Six-state(1-D sweep 在 QBER)
- F4 Efficient BB84(2-D sweep 在 (QBER, p_Z))

**未纳入**:
- F3 SARG04:严格 Koashi 2005 口径待 announcement classical register 基础设施;v0.3 简化 Werner 模型(commit `a6e8192`)已回滚,**不纳入 Pareto 比较**以免误导。详见 [PHASE1_LOG.md §2.1](../PHASE1_LOG.md)。

## 2. 硬验收(RESEARCH_PLAN §3.2)

| 硬指标 | 要求 | 本轮状态 |
|--------|------|----------|
| 扫描点数 ≥ 1000 | per family | **F4 40×40 = 1600 点** ✓ |
| Pareto 上包络记录 | per family | ✓(F1/F2/F4 envelope 已记录 §4) |
| 族间比较图 | BB84 vs MDI vs TF | ✓ [family_comparison.png](../research/figures/family_comparison.png) (2026-04-24 含 Pirandola UB 候选线) |

## 3. Threshold QBER(key rate → 0 点,f_ec=1.0)

| Protocol | Threshold | 来源 |
|----------|-----------|------|
| F1 BB84 | **0.1100** | WLC SDP,grid step 0.0025 |
| F2 Six-state | **0.1275** | WLC SDP,同网格 |

**对照**:
- Shor-Preskill 解析:BB84 阈值 $1 - 2h(e) = 0 \to e \approx 11.0\%$ ✓
- Scarani 2009:Six-state 阈值 ≈ 12.62% — 本扫描 12.75% 差 1 个网格间距(0.0025),一致

## 4. F4 Efficient BB84 Upper Envelope(最大 R 对 QBER)

2-D 扫描下,每个 QBER 挑 $p_Z$ 使 R 最大(即 $p_Z \to 0.99$,$p_\text{sift} \to 0.9802$)。

| QBER | Max Rate | 对应 $p_Z$(网格 max) |
|------|----------|----------------------|
| 0.0000 | 0.9802 | 0.99 |
| 0.0256 | 0.6429 | 0.99 |
| 0.0513 | 0.4081 | 0.99 |
| 0.0769 | 0.2132 | 0.99 |
| 0.1000 | 0.0608 | 0.99 |

**Pareto 特征**:在对称信道假设下,F4 Pareto 前沿**退化为 $p_Z$ 单调上界**(越偏置越好);真 Pareto 前沿的非平凡结构需引入有限密钥统计约束(S2.4 GEAT 后才浮现)。本轮 infinite-key 扫描仅作为 S2.2 基础设施验证。

## 5. F4 vs F1 比率(同 QBER 下 Efficient BB84 相对 BB84 提升)

$p_Z \to 0.99$ 时 $p_\text{sift} = 0.99^2 + 0.01^2 = 0.9802$,F4 相对 F1 的密钥率比为 $0.9802/0.5 \approx 1.96$ — 接近 **BB84 的 2 倍**,符合 Lo-Chau-Ardehali 2005 预测。

## 5b. 上界对比 (2026-04-24 增补 [SYN])

把 BB84/six-state 的 R_LB 与等效 depolarizing 信道的真 E_R = E_R^PPT 对比 (信道 p_depol = 4·QBER/3)。

E_R 是真信道层 UB（Plenio-Virmani 2007 §V.E (V.86) for d=2: `E_R = 1 - h(F)`，2026-04-24 修复 `e_r_depolarizing_analytic` bug 后正确）。MOSEK SDP `e_r_channel_ppt` 数值匹配.

**[单位修正 2026-04-24]**: SP 率以 **bits/信号** (= bits/channel use)，BB84 p_sift=0.5，六态 p_sift=1/3。先前表格错误使用 per-sifted 值，已修正。

| QBER | E_R (UB, /signal) | F1 BB84 SP (LB, /signal) | F2 Six-state SP (LB, /signal) | E_R/SP_BB84 | E_R/SP_6st |
|------|-------------------|--------------------------|-------------------------------|-------------|------------|
| 1.0% | 0.919 | 0.419 | 0.288 | 2.19× | **3.19×** |
| 3.0% | 0.806 | 0.306 | 0.221 | 2.64× | 3.64× |
| 5.0% | 0.714 | 0.214 | 0.166 | 3.34× | 4.31× |
| 8.0% | 0.598 | 0.098 | 0.093 | 6.11× | **6.40×** |
| 10.0% | 0.531 | 0.031 | 0.051 | 17.1× | 10.5× |
| **11.0%** | 0.500 | ≈0 | 0.031 | ∞ | **16.3×** |
| **12.62%** | 0.453 | 0 | ≈0 | ∞ | **∞** |

**关键观察** [单位修正后]:
- **六态 E_R/SP 比率 ~3-6×** (per-signal)，优于 BB84，但**不是"接近 UB-LB 闭合"** — 先前 ≤1.8× 数据是 per-sifted 单位错误所致，已撤回。[CONJ]
- **BB84 离 UB 远** (在 11% 阈值 SP→0 而 E_R=0.5)，BB84 SP 公式 (1−2h(QBER)) 的 EC cost 非紧是观察结论。[SYN]
- 详细数据 / 图表见 [`docs/findings/log_neg_msEB_application_2026-04-23.md`](log_neg_msEB_application_2026-04-23.md) §4.4-4.5

## 6. 下一步(S2.2 Week 4-8 续)

- [ ] 引入 scikit-optimize 做 2-D BO 对比 grid scan(可选,非硬验收)
- [ ] 加入 MDI family(需 `build_decoy_mdi_protocol` 或利用现有 `build_mdi_protocol` + 距离/损耗扫描)
- [ ] 加入 TF family(需 M4B 实施)— 完成后补族间比较图 $(\eta, R)$ 平面
- [ ] 引入 finite-key 约束后的真 Pareto 前沿(Phase 1 S2.4 GEAT)

## 7. 变更日志

- **v0.3** (2026-04-24): §5b 单位修正 — per-sifted SP 值改为 per-signal（含 p_sift 因子）。正确比率 ~3-6×，先前 ≤1.8× "接近闭合"表述已撤回。
- **v0.2** (2026-04-24): §5b 上界对比追加（单位错误版，已由 v0.3 修正）。
- **v0.1** (2026-04-19):F1/F2/F4 初版 Pareto 扫描 + 基础设施验证。F3 SARG04 已从本文件移除,待 Koashi 2005 严格实施后重新纳入。
