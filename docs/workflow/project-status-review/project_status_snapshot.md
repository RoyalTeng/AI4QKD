# AI4QKD 项目完成情况快照 — 2026-04-30

**分支**: MS-EB (from main @ 903e982)
**评审请求**: 项目整体完成情况评审

---

## 1. 项目总体进度

| Phase | 状态 | 完成度估计 | 关键产出 |
|-------|------|-----------|---------|
| Phase 0 (Sub-Q1) | ✅ 完成 | ~95% | MS-EB 框架 + WLC SDP + 七族五元组 |
| Phase 1 (Sub-Q2) | ✅ 完成 | ~90% | 三族 Pareto 前沿 + GEAT 有限密钥 |
| Phase 2 (Sub-Q3) | 🟡 进行中 | ~40% | upper_bound_report v0.7 + path α 11 sub-gap |
| Phase 3 (Sub-Q4) | 🟡 初步 | ~15% | gap_shape v0.3 + gap_analysis 初稿 |

**整体估计**: 约 50-55% 完成（按 PROSPECTUS v3.1 Sub-Q1→Sub-Q4 全计划）

---

## 2. 代码库状态

### 2.1 核心模块 (qkdx/)

| 模块 | 文件数 | 状态 |
|------|--------|------|
| `qkdx/core/` | 4 | ✅ hilbert, operators, entropy, bell_povm |
| `qkdx/protocol/` | 1 | ✅ MSEBProtocol 基类 |
| `qkdx/protocols/` | 6 | ✅ BB84, six-state, efficient-BB84, MDI, PM-QKD |
| `qkdx/numerics/` | 8 | ✅ WLC SDP, decoy, facial, upper_bound, Kamin SDP |
| `qkdx/symmetry/` | 2 | ✅ groups, twirling |
| `qkdx/sweeps/` | 5 | ✅ BB84/MDI/TF family sweeps + pareto |
| `qkdx/finite_key/` | 2 | ✅ GLL-Renner, Kamin-GEAT |
| `qkdx/analytic/` | 2 | ✅ PM-QKD decoy, MDI decoy |
| `qkdx/utils/` | 2 | ✅ logging, solvers |

### 2.2 测试覆盖

- 测试目录: `tests/test_core/`, `tests/test_protocols/`, `tests/test_numerics/`, `tests/test_analytic/`, `tests/test_sweeps/`, `tests/test_symmetry/`, `tests/test_integration/`
- 共 79+ tests (Phase 1 末全绿)

---

## 3. 文档产出

### 3.1 核心规范文档
- PROSPECTUS.md v3.1 — 研究地图
- RESEARCH_PLAN.md v1.0 — 研究执行计划
- REFACTORING_PLAN.md v3.1.4 — 函数级实施规范
- PHASE_STATUS.md v1.1 — 当前进度快照
- CLAUDE.md v1.0 — AI 协作规范（含 R0.1-R0.3 红线）

### 3.2 Phase 报告
- PHASE0_REPORT.md — Phase 0 完成报告
- PHASE1_REPORT.md v1.1 — Phase 1 完成报告

### 3.3 Sub-Q3 产出
- upper_bound_report.md v0.7 — 上界接缝报告
- FINDINGS.md v2 — Interim Verdict (bosonic-asymptotic 放宽版)

### 3.4 Sub-Q4 产出
- gap_shape_g4_1.md v0.3 — Gap 形状分析
- gap_analysis_2026-04-24.md v0.1 — Gap 归因初稿

### 3.5 Path α 证明文档
- umr_path_alpha_three_lemma_v0_3.md — 三 lemma 框架 (USER-APPROVED PRIORITY)
- umr_path_alpha_three_lemma_v0_2.md — [REJECTED] v0.2
- path_alpha_l1g1~l3g2e_closure 共 12 份 sub-gap closure 文档
- path_alpha_subgap_closure_integration v0.1-v0.3 — 综合集成
- umr_path_alpha_paper_draft_skeleton_v0_1.md — 论文骨架
- umr_path_alpha_pdf_synthesis_v0_1.md — PDF 合成

### 3.6 其他证明路径
- umr_path_gamma_4_5_cheatsheet.md — path γ 速查表
- umr_path_delta_relaxed_trust_v0_1.md — [SUPERSEDED] path δ

---

## 4. 研究数据资产

### 4.1 数值扫描数据
- 7000+ 扫描点 (MDI + TF + BB84 F4 + Kamin Fig1)
- 30+ 图表 (PNG + PDF)

### 4.2 复现脚本
- reproduce_cui_2019_fig1.py
- path_alpha_v0_2_alignment.py
- path_alpha_l1g4_trace_distance_contraction.py

---

## 5. 当前 OPEN 项（阻塞性）

### 5.1 Sub-Q3 结构 gap（需要用户 paper-level work）

按优先级（遵循 2026-04-25 user directive，path α 优先）：

1. **path α 三 lemma framework** — L1.G1-G4 / L2.G1-G4 / L3.G1-G3 共 11 sub-gap
   - 状态: v0.3 USER-APPROVED PRIORITY, C3 REJECTED
   - 依赖: 用户直读 Pirandola 2019 §III-IV / Khatri-Wilde §19-20 / Lucamarini 2018

2. **β.G4 Eve model transfer** — Khatri-Wilde 2020 §19 Prop 19.2 umr 适用性
   - 状态: OPEN, fallback when path α fails

3. **β.G5 adversarial comb reduction** — WTB 2017 Thm 4 umr 继承
   - 状态: OPEN

4. **γ.B.G1 DPI target lemma** — Pirandola 2019 Eq. 9 拓扑适用性
   - 状态: OPEN

5. **γ.G3 ε-composable transfer** — Metger 2024 GEAT asymptotic→finite 桥接
   - 状态: OPEN

### 5.2 数值扩展
6. AD channel-level K^{↔} 上界工具选型 (anti-degradable γ>1/2)
7. Erasure E_R^PPT SDP (需高内存 16×16)
8. SARG04 严格实施 (Koashi 2005 announcement register)

### 5.3 Phase 1 残余
9. BB84 decoy+misalignment 带入族比较图
10. qubit Kamin 5-cell refactor
11. decoy Kamin WL22 beamsplitter honest model

---

## 6. 严谨性红线合规状态

### 6.1 R0.1 (不做计划外降级)
- ✅ 无已知违规
- 已记录降级先例: SARG04 v0.3 简化回滚 (PHASE1_LOG.md §2.1)

### 6.2 R0.2 (研究结论多方验证)
- ✅ 所有 [THM] 级结论已走 C1 ∧ C2 ∧ C3
- ⚠️ path α v0.3: user override C3 REJECTED, R0.2 三闸门未走完
- ⚠️ FINDINGS v2: 全部结论 [SYN]/[CONJ]/[UNKNOWN] 级，未升级

### 6.3 R0.3 (严谨性分级)
- ✅ 所有文档显式标注分级标签
- ⚠️ path α v0.3 的 11 sub-gap 仍全为 [UNKNOWN]

---

## 7. 撤回/失败记录 (先例)

1. **FINDINGS v1 retraction (2026-04-19)**: AI 自行 [SYN]→[COROLLARY] 升级
2. **path γ v0.2 retraction (2026-04-21)**: AI 绕过 Log 07 三 lemma 要求
3. **AD channel-level UB retraction (2026-04-24)**: Choi-state ≠ channel capacity
4. **path α v0.2 REJECTED (2026-04-25)**: spec-doc smuggling structural gap closure

---

## 8. 下一步建议

### 阻塞项（必须用户亲自做）
- path α 11 sub-gap 的 PDF 直读 + 形式化验证 (C1(b))
- 4 个结构 gap 的文献精读

### AI 可继续项（用户启动后）
- Path α sub-gap closure 文档的迭代完善
- 数值扩展 (AD K^{↔}, Erasure SDP, SARG04)
- Phase 1 残余修复
