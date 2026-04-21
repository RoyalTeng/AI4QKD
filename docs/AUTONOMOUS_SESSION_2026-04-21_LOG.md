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

---

### A.1 MDI family Pareto (commit ccd0090)

基于 `qkdx/analytic/mdi_decoy.py` (Ma-Razavi 2012)，新增 `qkdx/sweeps/mdi_family_sweep.py`：
- 1D + 2D Pareto 扫描（loss × e_d, loss × p_d）
- **2581 点**，满足 S2.2 硬验收 ≥ 1000
- 6 tests 全过

数值结果（Ma-Razavi Table I defaults）：
| loss (dB) | rate | 备注 |
|---|---|---|
| 0 | 1.90e-3 | max |
| 20 | 3.85e-4 | |
| 40 | 9.21e-6 | |
| 56 | cutoff | ≈ Ma-Razavi Fig. 4 |

图：[figures/mdi_family_*.{png,pdf}](research/figures/) (3 张)

---

### A.1 TF/PM-QKD family Pareto (commit 9e3df89)

基于 `qkdx/analytic/pm_qkd_decoy.py` (Ma-Zeng-Zhou 2018)，新增 `qkdx/sweeps/tf_family_sweep.py`：
- 1D + 3×2D Pareto 扫描（loss × e_delta, loss × p_d, loss × M）
- **2831 点**，满足硬验收
- 6 tests 全过

数值结果：
| loss (dB) | rate (bits/signal) | √η | PLOB |
|---|---|---|---|
| 0 | 8.25e-4 | 1.0 | ∞ |
| 40 | 1.63e-5 | 0.01 | 1.44e-4 |
| 80 | 1.51e-7 | 3.16e-4 | 1.44e-8 |

**验证 √η scaling**（PM-QKD rate ≈ 10⁻³·√η）与 FINDINGS v2 §1.1 [SYN] 一致。

图：[figures/tf_family_*.{png,pdf}](research/figures/) (4 张, 含 √η + PLOB 参考线)

---

### A.2 PHASE1_REPORT + 族地图 (commit ffa3c3d)

综合报告 [docs/PHASE1_REPORT.md](PHASE1_REPORT.md) v1.0：
- 三族 Pareto 集成（BB84 = 1600, MDI = 2581, TF = 2831 = **7000+ 点 total**）
- Kamin GEAT 工具链 79 tests summary
- DV-QKD 族地图主图 [figures/family_comparison.{png,pdf}](research/figures/)

**族交叉点分析**：
- BB84 dominates 0-8 dB
- TF 在 **8 dB 处超越 MDI** (3.16e-4 vs 2.97e-4)
- TF dominates > 30 dB (√η 优势)

---

### U3.7 Layer 5.3 SDP (E_R^PPT) (commit a7b1d9b)

新模块 [qkdx/numerics/upper_bound.py](../qkdx/numerics/upper_bound.py)：
- `partial_transpose_B` + CVXPY 版本
- `e_r_ppt(rho, d_A, d_B)` — Vidal-Werner 2002 SDP
- `e_r_channel_ppt(kraus, d_A)` — 信道 E_R^PPT via Choi
- 标准 qubit 信道 Kraus: identity, depolarizing, dephasing, amp damping
- `dv_gap_from_achievable` helper

**验证**：11 tests pass, 2 min MOSEK
- E_R^PPT(identity qubit) = 1.0 ✓
- E_R^PPT(fully depol) ≈ 0 ✓
- 对 Vollbrecht-Werner 2001 isotropic state 形式一致
- Amp damping @ γ=0.5: E_R^PPT = 0.32

产出：[scripts/sweep_upper_bound_toy.py](../scripts/sweep_upper_bound_toy.py) +
[figures/upper_bound_toy_channels.{png,pdf}](research/figures/) +
[data/er_ppt_*_sweep.csv](research/data/).

---

### U3.5 Khatri-Wilde 2020 Level 3 memo (commit 804da71)

[docs/literature/KhatriWilde-2020.md](literature/KhatriWilde-2020.md) — arXiv:2011.04672v2 1200+ 页教科书精读：
- Ch 19 LOCC-Assisted Quantum Comm: **Proposition 19.2** amortized entanglement 统一框架
- Ch 19 **Thm 19.4** squashed entanglement weak converse
- Ch 19 **Thm 19.8** max-Rains STRONG converse (SDP-computable)
- Ch 20 Secret Key Agreement
- 三候选 umr 修复路径 α/β/γ 对接 Log 07

---

### U3.6 上界 MS-EB 重写 + max-Rains SDP (commit 26b11ae)

[docs/proofs/upper_bound_msen.md](proofs/upper_bound_msen.md) v0.1：
- $\mathcal{T}_\text{umr}$ 拓扑类的 MS-EB 定义
- 三候选上界陈述（所有 **[CONJ]** 级）：
  - A: PLOB worst-edge
  - B: Pirandola N=1 chain
  - C: Khatri-Wilde max-Rains

`qkdx/numerics/upper_bound.py` 扩展：
- `r_max_channel_sdp` — Wang-Duan 2016b max-Rains SDP
- Identity qubit → R_max = 1 ✓
- 新增 4 tests（总 15 pass）

---

### G4.1 Gap 定量形状 [CONJ] (commit 2238581)

[docs/findings/gap_shape_g4_1.md](findings/gap_shape_g4_1.md) v0.1：
- 比较 Sub-Q2 TF 下界 vs Sub-Q3 三候选上界
- Gap ratio 表（[CONJ] 级）：
  - 20 dB: ~1950× (cand A/B), ~790× (cand C)
  - 60 dB: ~2080× (cand A/B), ~1000× (cand C)
- Log-log 斜率：TF 1/2, UB cand A/B 是 1 → 线性发散

**红线遵守**：FINDINGS v2 §4.2 禁止以 [CONJ] 级 gap 做归因。本 G4.1 仅作 shape，**不归因**。

---

### U3.8 upper_bound_report.md v0.1 (commit 55ba0ae)

[docs/findings/upper_bound_report.md](findings/upper_bound_report.md) — **~25 页等价** Sub-Q3 接缝报告：
- §1 引言 + PROSPECTUS Sub-Q3 回顾
- §2 五篇文献定理精要浓缩
- §3 MS-EB 重写（从 U3.6）
- §4 Layer 5.3 SDP 实施
- §5 数值验证 + gap 分析
- §6 Limitations
- §7 Sub-Q4 handoff
- §8 完整文件/commit 索引
- §9 严谨性守则声明

**验收对齐 RESEARCH_PLAN §4.5 所有 3 条硬验收**（定理可追溯、可复现实验索引、R_UB 表达式）。完整 30-50 页版本等候用户 Log 07 路径 γ 形式化后扩展。

---

### Codex 评审尝试 (未完成)

用户指令"让 codex 评审"，本 session 尝试对 Sub-Q3 stack 跑 Codex dev-reviewer。两次调用（17:26 + 17:46）均**无输出**（Codex 进程启动后卡住 > 15-20 min 无 stdout）。与 Phase A 总结文档记录的"Codex review flakiness" 现象一致。

**尝试记录**：
- `codex exec --sandbox read-only --skip-git-repo-check -C $PWD "$(cat prompt.txt)"` 简单形式
- 最小 prompt（600 字符以内），要求 600 words 结构化输出
- 背景进程长时间运行无输出，kill -9 终止

**替代措施**：
1. 本 session 所有关键 commit 都走了 TDD (测试先行)，每 commit 带 tests pass
2. SDP 数值结果对解析极限做 sanity check（E_R^PPT(id)=1, R_max(id)=1, Vidal-Werner isotropic formula 一致）
3. 所有文档严格 [THM/COROLLARY/CONJ/UNKNOWN] 分级，不越权升级
4. 交付物可独立 audit（CSV + PNG + PDF + commit SHA 全 traceable）

**待做**：用户回来后如有机会，可手动在不同 host 跑 codex 评审，或请 Codex-GPT Plus / Claude-3 做独立 review。

---

### Claude-native 审计代理 (commits a8edc77 + 4066a10)

Codex 环境卡住无响应，**替代方案**：spawn Claude-native `general-purpose` Agent 作 physics-aware 审计代理，任务：
- 读六份文件（qkdx/numerics/upper_bound.py + tests + U3.6/G4.1/U3.8 + Khatri-Wilde memo）
- 核对 FINDINGS v2 §1.2 四级分级守则
- 检查 SDP 公式正确性、umr 继承 overclaim、数值-文档一致性

**审计结果**：**PASS** with 4 MAJOR + 5 MINOR 修正建议。

**4 MAJOR 修正（commit a8edc77 全部 address）**：

1. **`e_r_depolarizing_analytic` Werner fidelity 公式错**：
   - 旧：F = 1 - p/2（不正确）
   - 新：F = 1 - 3p/4（正确；来自 ⟨Φ⁺|(I⊗N_p)|Φ⁺⟩⟨Φ⁺||Φ⁺⟩）
   - 影响：函数只作解析参考，未被任何测试调用，无下游 propagation
2. **`r_max_channel_sdp` 实际是 log-negativity，不是严格 Wang-Duan 2016b max-Rains**：
   - 审计正确识别：我的 SDP `min Tr[V] s.t. V ≥ ±ρ^{T_B}` 给 log-negativity
   - WD 2016b 严格 max-Rains 是两算子 form `min ||Tr_B[V+W]||_∞`
   - 重命名函数 `log_negativity_channel_sdp` + 保留 `r_max_channel_sdp` 为 alias
   - docstring 显式声明是 log-negativity（仍是 Thm 19.8 strong-converse 有效上界，只是 loose）
3. **`gap_shape_g4_1.md` 10 dB 行数值错**（1.2073 → 0.5484）+ TF LB 数值错（3.80e-4 → 2.50e-4 per CSV）：
   - 同样修 `pareto_tf_family.md`
   - 重新计算 gap ratios (10 dB: 2200× 而非 3200×)
4. **`gap_shape_g4_1.md` §2.3 表述越界**：
   - 旧："反证情况 A" 有潜在 [CONJ]→[THM] 越级嫌疑
   - 新：显式 "conditional sensitivity analysis only" + "不 promote 到归因"
   - 保持 §0 disclaimer 严格

**验证**：15 tests still pass 修正后。

---

## 总结 — 本 session 工作量（2026-04-21, ~8 小时）

**Commits 数**：9 个重大 commit
- `c49b2bf` D.1 qubit Thm 4 diagnostic
- `ccd0090` A.1 MDI Pareto
- `9e3df89` A.1 TF Pareto
- `ffa3c3d` A.2 PHASE1_REPORT
- `a7b1d9b` U3.7 Layer 5.3 SDP
- `804da71` U3.5 Khatri-Wilde memo
- `26b11ae` U3.6 MS-EB + max-Rains SDP
- `2238581` G4.1 Gap [CONJ]
- `55ba0ae` U3.8 upper_bound_report v0.1

**测试总数**：新增 30+ tests，累计 Kamin + sweeps + upper_bound 超过 100 tests
**数据文件数**：新增 8 个 CSV
**图件数**：新增 12 张 PNG + 12 张 PDF（publication-ready）
**文档页数**：新增 docs 超过 1000 行（含 U3.5, U3.6, U3.8 三大长文）

**验收对齐**：
- ✅ PROSPECTUS Sub-Q2 全部子验收（three family sheets + Pareto + 族比较图）
- ✅ PROSPECTUS Sub-Q3 (a-e) 中 (a)(b)(c) via 精读 memo, (d)(e) via U3.6+U3.7
- ✅ RESEARCH_PLAN §3.4 PHASE1_REPORT
- ✅ RESEARCH_PLAN §4.5 U3.8 v0.1（≥25 页等价，30-50 页完整版依赖用户理论工作）
- ✅ 诚实披露 gap 和 [CONJ] 级限制

**严谨性红线遵守**：
- [THM/COROLLARY/CONJ/UNKNOWN] 四级分级全文遵守
- FINDINGS v2 §1.2 不升级红线遵守
- Sub-Q4 归因不预判（仅作 gap shape [CONJ] 级分析）
- 所有 UB 候选 [CONJ] 明标

**剩余 open**（按优先级）：
- 用户 Log 07 路径 γ 的 Assumption DP 形式化（纸笔工作）
- D.4 Kamin MDI finite-key 迁移（多小时，未启动）
- D.2 WL22 beamsplitter（decoy Fig.3 ~3x offset, 多小时）
- Codex 评审（本地环境卡住，换 host/session 再试）
- 任何候选升级到 [COROLLARY] 后：G4.2 归因 + Sub-Q4 后续工作
