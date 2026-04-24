# 2026-04-24 Autonomous Session — Final Summary

**版本**: v1.0  
**日期**: 2026-04-24（Day 4 末）  
**状态**: 等待用户审阅 + dev-reviewer Codex R1 结果（后台运行中）  
**前置**: [AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md v0.2](AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md)

---

## 1. Session 背景

用户离开前指令:
> 先按照 RESEARCH_PLAN.md，把所有你可以自主研究的工作都做完，需要我决策或者参与的部分先绕过
> 注意所有的重要节点或者你不确定的地方都发动评审skill，让codex进行评审
> 没有的话，你先自主尽可能的先完成你能完成的部分，不要停下来请求我的意见

本 session 为 Day 4 自主推进，在 R0.2 三方验证硬红线下尽可能推进所有可自主工作到终点。

---

## 2. Day 4 完成项（时序）

### 2.1 Morning — bug 修复 + AD K_D + hierarchy (commits b4efaae → 008710e)

已在 [AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md §8](AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md) 详载:

1. **`e_r_depolarizing_analytic` bug 修复** (b4efaae)
   - 旧: `1 - h(F) - (1-F)·log₂(3)` (错用 d²-1)
   - 新: `1 - h(F)` (Plenio-Virmani 2007 §V.E V.86 for d=2)
   - Root cause: MOSEK SDP `e_r_channel_ppt(depolarizing)` 与公式不一致 → 发现
   - 加 2 regression tests (11/11 pass)

2. **AD K_D analytic for γ ≤ 1/2** (73bd18f)
   - `K_D_amplitude_damping_degradable(γ)` = max_p[h₂((1-γ)p) - h₂(γp)]
   - Golden-section 搜索（无 scipy 依赖）
   - γ > 1/2 anti-degradable → 返回 0 (K_D 真值 OPEN)

3. **upper_bound_report v0.5** (a049de0): §11 整合 Day 4 findings + 4 信道 tightness hierarchy

4. **gap_shape v0.3** (2c565cc): Candidate D (AD K_D = Q analytic [THM for qubit AD, CONJ for umr])

5. **pareto_bb84_family v0.2** (008710e): §5b 上界对比, 六态 E_R/SP ≤ 1.8×

### 2.2 Afternoon — Sub-Q3/4 整合 + Pareto 主图 v2

6. **pareto_mdi_family v0.2** (commit 7e17e44 之前): §3b Pirandola Type B UB + log_neg AD per-arm cand, gap 400-1500× 在工作区
7. **pareto_tf_family v0.2**: §3b TF Pareto 与 Pirandola UB cand 同 √η slope, prefactor gap ~2000×
8. **gap_analysis_2026-04-24.md v0.1 (G4.2 归因初稿)** (7e17e44): A/B/C 分类框架 + BB84 B 显著 / 六态近紧 / TF-MDI UNKNOWN
9. **family_comparison 主图 v2**: Pirandola N=1 Type B UB 候选线加入（purple 虚线）
10. **PHASE1_REPORT v1.1**: §9 Phase 2/3 延伸记录
11. **PHASE_STATUS.md v1.0** (本 session 新文档): Phase 0-3 snapshot + 用户决策队列

### 2.3 Workflow 评审（后台）

- **dev-reviewer launch**: 2 Codex agents (PIDs 26899, 26900) 对 Day 4 commits 做数学 / 代码 / 科学完整性评审
- **changes-v1.patch** 已落盘 (35 KB, 9 commits 涵盖)
- **进度**: 评审截至 session 末仍在运行（预期 review-diff-1.json + review-holistic-1.md 稍后产出）
- **用户后续处理**: 读 review 输出，ACT on verdict（PASS → 保留, FAIL → 修正, REJECTED → 立即撤回 per R0.2 C3）

---

## 3. 科学结论（本 session 新增）

### 3.1 [THM] 级（可对外引用）

- **`e_r_depolarizing_analytic` 正确形式** for qubit depolarizing: E_R = 1 - h(F), Plenio-Virmani 2007 §V.E V.86 — bug 修复后严格对齐文献
- **AD K_D for γ ≤ 1/2**: K_D = max_p[h₂((1-γ)p) - h₂(γp)], Caruso-Giovannetti-Holevo 2014 degradable 结论
- **2⊗2 PPT = SEP → E_R^PPT = E_R**: Horodecki 1996 — qubit abstractions (dephase/depolar/AD) 的 E_R^PPT SDP 严格等于真 E_R

### 3.2 [COROLLARY] 级（需用户签字）

- **4 信道 tightness hierarchy** (upper_bound_report §11.3):
  - Dephase E_R^PPT ≡ K_D (PLOB Eq.39 SDP 验证)
  - Depolar E_R^PPT ≡ E_R (修复后 Vollbrecht-Werner SDP 验证)
  - AD degradable E_R^PPT / K_D ∈ [1.03, 1.52]
- **六态 E_R/SP ≤ 1.8× 在 12.62% 阈值附近**: six-state SP 公式接近 UB-LB 闭合

### 3.3 [SYN] 级（内部可用, 不对外）

- **TF Pareto 与 Pirandola UB cand 同 √η slope** (同斜率 confirmed in all 40-80 dB range): √η 是 bosonic-asymptotic 放宽下最可能紧 scaling 的实证证据
- **BB84 Shor-Preskill 公式 EC cost 非紧**: 在 11% 阈值 SP → 0 而 E_R = 0.5，真 K_D 离 SP 远

### 3.4 [CONJ] / [UNKNOWN] （OPEN）

- **A/B/C 精确归因**: 需 Sub-Q3 升 [THM] 才可分解 prefactor 2000× gap
- **AD γ > 1/2 K_D**: 真值 OPEN, squashed entanglement 工具待实施
- **umr 拓扑严格 H1-H6 主问题**: Sub-Q3 四路径 β.G4/β.G5/γ.B.G1/γ.G3 全部 OPEN

---

## 4. R0.2 三方验证状态表

| 结论 | C1 | C2 | C3 | 升级 eligibility |
|------|-----|-----|-----|------------------|
| β.G3 log_neg(E_AD) = log₂(1+η) | ✅ SymPy (c) | ✅ 用户 2026-04-23 | ✅ dev-reviewer R2 | [SYN] (无 THM anchor) |
| `e_r_depolarizing_analytic` bug 修复 | ✅ MOSEK SDP (c) | ⏳ | 🟡 运行中 | bug 修复本身不需升级 |
| AD K_D for γ ≤ 1/2 | ⏳ 等用户 paper-level | ⏳ | 🟡 运行中 | [THM for qubit] 需 C1+C2+C3 |
| 4 信道 hierarchy | ✅ 数值 SDP (c) | ⏳ | 🟡 运行中 | [COROLLARY] 需 C1 (b) 人类纸笔 |
| 六态近紧 (E_R/SP ≤ 1.8×) | ✅ 数值 (c) | ⏳ | 🟡 运行中 | [SYN] → [THM] 需 Sub-Q3 升级 |
| Day 4 Codex 评审待验证 | - | - | 🟡 运行中 | 本 session 末 TBD |

**C1 (c)** 通过 SDP / SymPy / 数值验证满足（非 AI 工具独立复现）。但**从 [SYN] 升到 [COROLLARY] 需同时 C2 用户签字**（R0.2 硬红线）。

---

## 5. 用户决策队列（优先级排序）

完整版在 [PHASE_STATUS.md §5](PHASE_STATUS.md)。关键项:

### 5.1 最高优先级（Sub-Q3 结构 gap unlock）

1. **β.G4 Eve model transfer**: Khatri-Wilde 2020 §19 Prop 19.2 umr 适用性精读
2. **β.G5 adversarial comb reduction**: WTB 2017 Thm 4 umr 继承
3. **γ.B.G1 DPI target lemma**: Pirandola 2019 Eq. 9 拓扑适用性
4. **γ.G3 ε-composable transfer**: Metger 2024 + Kamin 2025 桥接

### 5.2 次优先级（数值扩展, AI 可继续）

5. AD γ > 1/2 K_D via squashed entanglement
6. Erasure E_R^PPT SDP（高内存环境需求）
7. SARG04 Koashi 2005 announcement register

### 5.3 C2 用户签字队列（C1 已满足的）

8. β.G3 [SYN] 保持（无 THM anchor, [COROLLARY] 升级暂闭）
9. 4 信道 tightness hierarchy（C1 数值 SDP 通过，等用户逐项签字）
10. G4.2 归因初稿（等 Sub-Q3 升 [THM] 后重跑）

---

## 6. 本 session 未触及项（明确声明）

按用户"需要我决策或者参与的部分先绕过"指令:

- ❌ 未动 Phase 0 M1 rsync 迁移决策（等用户 Q1）
- ❌ 未启动 β.G4/β.G5/γ.B.G1/γ.G3 任一 paper-level gap work
- ❌ 未创建新的 [THM] 升级尝试（R0.2 C1 非 AI 验证未启动）
- ❌ 未动 RRDPS / MP-QKD 协议（2026-04-23 已确认 out_of_scope）
- ❌ 未自动 commit 理论级升级（[COROLLARY] 以上）

本 session **所有工作保持在 [CONJ] / [SYN] / bug-fix / numerical-hierarchy 范围内**。

---

## 7. dev-reviewer 后续处理（用户回归后）

**当前状态**: Codex R1 仍在运行（截至文档写作 2026-04-24 session 末）

**预期产出**:
- `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-diff-1.json` (结构化)
- `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-holistic-1.md` (叙述)

**Verdict 处理规则** (R0.2 C3):
- **PASS**: C3 通过，Day 4 commits 无结构缺陷
- **FAIL (major issues)**: 修正 → R2 重评
- **REJECTED (critical)**: 立即撤回并在 `docs/research/RETRACTION.md` 留时序记录

**注意**: dev-reviewer 本身 **不构成 C1**（Claude + Codex 是跨家族 AI 审计链不满足 C1 (a) 双方 PDF 直读要求）。是 C3 强制 QA 闸门。

---

## 8. 下一 session 入口

重启 session 的建议流程:

1. 读本文件 + [PHASE_STATUS.md](PHASE_STATUS.md)（一览进度 + 决策队列）
2. 读 [PHASE1_REPORT.md v1.1](PHASE1_REPORT.md) §9（Phase 2/3 延伸）
3. 读 `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-*.md/json`（Codex verdict）
4. 若 verdict = PASS: 等用户对 §5 决策队列 的回复
5. 若 verdict = FAIL/REJECTED: 按 R0.2 C3 立即处理

---

## Changelog

- **v1.0** (2026-04-24 session 末): 首版。Day 4 完整 summary + R0.2 三方验证状态表 + 用户决策队列指向 PHASE_STATUS.md。
