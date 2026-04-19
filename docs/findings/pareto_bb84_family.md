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
| 族间比较图 | BB84 vs MDI vs TF | ✗ 待 MDI/TF 实施(Phase 1 后续) |

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

## 6. 下一步(S2.2 Week 4-8 续)

- [ ] 引入 scikit-optimize 做 2-D BO 对比 grid scan(可选,非硬验收)
- [ ] 加入 MDI family(需 `build_decoy_mdi_protocol` 或利用现有 `build_mdi_protocol` + 距离/损耗扫描)
- [ ] 加入 TF family(需 M4B 实施)— 完成后补族间比较图 $(\eta, R)$ 平面
- [ ] 引入 finite-key 约束后的真 Pareto 前沿(Phase 1 S2.4 GEAT)

## 7. 变更日志

- **v0.1** (2026-04-19):F1/F2/F4 初版 Pareto 扫描 + 基础设施验证。F3 SARG04 已从本文件移除,待 Koashi 2005 严格实施后重新纳入。
