# 自主 session 日志 — 2026-04-21 起

**授权**：用户 2026-04-21 指令"按照规划继续研究、独立研究、直到用户回来"
**红线**：
1. 严格 TDD，每 commit 有测试
2. 关键 commit 走 dev-reviewer skill + 双 Codex 评审
3. 不做计划外降级（FINDINGS v2 / Phase1 log 3.8 红线）
4. AI 合成结论 [SYN]/[CONJ]/[UNKNOWN] 不升级到 [THM] / [COROLLARY]
5. Sub-Q4 归因不以 FINDINGS v2 为预判
6. 每个阶段都记录到本日志

**起点 commit**：`807b58e`（Phase A Stage 2 Kamin summary v2）

## 计划顺序

1. D.1 qubit Fig.1 Thm 4 τ-slack 迁移
2. D.4 Kamin MDI family 迁移
3. A.1 MDI + TF family Pareto 扫描
4. A.2 PHASE1_REPORT + DV-QKD 协议族地图
5. U3.5 Khatri-Wilde memo
6. U3.6 上界 MS-EB 重写
7. U3.7 Layer 5.3 SDP
8. U3.8 接缝报告
9. G4.1 Gap 定量形状
10. D.2 (opportunistic) WL22 beamsplitter

---

## 阶段记录（按顺序追加）

---

### D.1 qubit Fig.1 Thm 4 τ-slack (2026-04-21)

**结果**：9 tests pass，但 **未闭合** §4.1 残余 ±6 dB gap。

n=10^12 扫描：

| loss | Thm 4 rate | hard rate | Kamin ref |
|---|---|---|---|
| 0 dB | 0.888 | 0.893 | ~0.9 |
| 10 dB | 0.0887 | 0.0893 | ~0.09 |
| 20 dB | 0.00879 | 0.00836 | ~0.008 |
| 25 dB | 0.00275 | 0.00217 | ~0.002 |
| 30 dB | 0.00085 | 0.00025 | cutoff ~26 dB |

**发现**：Thm 4 τ-slack 与 hard 几乎相同。原因分析：
- qubit BB84 的 §4.1 cutoff 残余**不是** V² penalty 过松（Eq. 38 精确 V² 已与 Kamin 一致）
- 瓶颈是我的 SDP 观察集只有 2 cells (qber_Z, qber_X)，而 Kamin 用 5 cells (Z-correct, Z-error, X-correct, X-error, no-det)
- 加 τ slack 在 2-cell 观察上没新 DoF；需要扩展 SDP 到 5-cell 观察才能真正改善
- 这是一个 **结构性 refactor**，非 v2 级改动

**决定**：D.1 记录为"验证 Thm 4 实施 + 识别瓶颈"，进入 D.4。

**产出**：
- `qkdx/numerics/kamin_sdp.py` 新增：`_thm4_phi_coefficients_qubit`, `kamin_choi_sdp_qubit_bb84(..., use_thm4=True)`, `kamin_thm4_key_length_bb84`, `kamin_thm4_key_length_bb84_optimized`
- `tests/test_numerics/test_kamin_thm4_qubit.py` (9 tests, 全过)
