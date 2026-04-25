# 2026-04-24 Autonomous Session — Final Summary

**版本**: v1.2  
**日期**: 2026-04-24（Day 4 末; 2026-04-25 evening followup-review fix）  
**状态**: dev-reviewer R5 (Day 4) PASS + R7 (AD anti-degradable retraction) PASS + post-R7 followup review FAIL→fix；等待用户审阅  
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

### 2.1 Morning — bug 修复 + AD Q (原标 K_D, 已 rename 2026-04-24 per retraction §8) + hierarchy (commits b4efaae → 008710e)

已在 [AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md §8](AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md) 详载:

1. **`e_r_depolarizing_analytic` bug 修复** (b4efaae)
   - 旧: `1 - h(F) - (1-F)·log₂(3)` (错用 d²-1)
   - 新: `1 - h(F)` (Plenio-Virmani 2007 §V.E V.86 for d=2)
   - Root cause: MOSEK SDP `e_r_channel_ppt(depolarizing)` 与公式不一致 → 发现
   - 加 2 regression tests (11/11 pass)

2. **AD Q analytic for γ ≤ 1/2** (73bd18f; 2026-04-24 evening: 原 K_D 重命名为 Q per retraction §8)
   - `quantum_capacity_amplitude_damping_degradable(γ)` = max_p[h₂((1-γ)p) - h₂(γp)]
   - Golden-section 搜索（无 scipy 依赖）
   - 返回 **Q = channel quantum capacity (LB on K^{↔}, 非 K_D 真值)**
   - γ > 1/2 anti-degradable → 返回 0 (Q=0; channel K^{↔}(AD) 真值 OPEN)

3. **upper_bound_report v0.5** (a049de0): §11 整合 Day 4 findings + 4 信道 tightness hierarchy

4. **gap_shape v0.3** (2c565cc): Candidate D (AD Q analytic, channel LB on K^{↔} [THM for qubit]; 后 v0.4 改为"参考量非 UB 候选" per RETRACTION §8)

5. **pareto_bb84_family v0.2** (008710e): §5b 上界对比, 六态 E_R/SP ≤ 1.8× **[已撤回 2026-04-24: per-sifted unit 错, per-signal ~3-6×]**

### 2.2 Afternoon — Sub-Q3/4 整合 + Pareto 主图 v2

6. **pareto_mdi_family v0.2** (commit 7e17e44 之前): §3b Pirandola Type B UB + log_neg AD per-arm cand, gap 400-1500× 在工作区
7. **pareto_tf_family v0.2**: §3b TF Pareto 与 Pirandola UB cand 同 √η slope, prefactor gap ~2000×
8. **gap_analysis_2026-04-24.md v0.1 (G4.2 归因初稿)** (7e17e44): A/B/C 分类框架 + BB84 B 显著 / 六态中等（per-signal E_R/SP ~3-6×; 先前"六态近紧 ≤1.8×" 已撤回 per e054a1e 单位修正）/ TF-MDI UNKNOWN
9. **family_comparison 主图 v2**: Pirandola N=1 Type B UB 候选线加入（purple 虚线）
10. **PHASE1_REPORT v1.1**: §9 Phase 2/3 延伸记录
11. **PHASE_STATUS.md v1.0** (本 session 新文档): Phase 0-3 snapshot + 用户决策队列

### 2.3 Workflow 评审闭环（5 轮 Codex 评审）

dev-reviewer 共运行 5 轮，产出如下:

| 轮次 | Verdict | 主要问题 |
|------|---------|---------|
| R1 | FAIL (UNSOUND) | (1) AD K_D/Q 概念错误; (2) per-sifted SP units; (3) depolarizing hierarchy 反向 |
| R2 | FAIL | K^{↔} ≥ E_R 方向仍错（修复引入新反向写法） |
| R3 | FAIL | §heading + PHASE_STATUS/PHASE1_REPORT 术语仍 stale |
| R4 | FAIL | dephasing 表 K_D 残留 + PHASE 文档仍有 K_D |
| **R5** | **PASS** | 无剩余 major 问题；残 `K_D` 3 处 + `近紧` grep 为 minor suggestion |

**最终 commit e054a1e**: 28 文件更改，修正 3 个 UNSOUND major issues:

1. **AD Q vs K_D**: `K_D_amplitude_damping_degradable` → `quantum_capacity_amplitude_damping_degradable`；全局文档/脚本/测试从 K_D → Q (LB on K^{↔})
2. **Per-signal SP units**: BB84/six-state SP rate 修正为 per-signal（p_sift=0.5/1/3 已含）；真实比率 ~2-6×（非 1.8×）
3. **Hierarchy 方向**: K^{↔} ≤ E_R^PPT = E_R（Rains bound UB）；depolarizing K^{↔} 真值 UNKNOWN

**产物**: `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-diff-{1-5}.json` + `review-holistic-{1-3}.md`

---

## 3. 科学结论（本 session 新增）

### 3.1 文献 [THM] 之 *实现 / 验证*（**项目内尚未升 [THM]，需 C2 用户签字**）

以下三项的**外部文献结论**是 [THM]，本 session 完成的是数值实现 + 与文献公式一致性验证 (R0.2 C1 数值条件 + C3 dev-reviewer 满足；**C2 用户签字 pending** — 不符合 R0.2 完整三条件，故对**项目内引用层面**仍 [SYN]，不可对外引用为本项目独立 [THM]):

- **`e_r_depolarizing_analytic` 正确形式** for qubit depolarizing: E_R = 1 - h(F), Plenio-Virmani 2007 §V.E V.86 — **文献 [THM]**；本 session bug 修复后与文献严格对齐
- **AD Q (channel, LB on K^{↔}) for γ ≤ 1/2**: Q = max_p[h₂((1-γ)p) - h₂(γp)], Caruso-Giovannetti-Holevo 2014 degradable single-letter — **文献 [THM]**；Q is LB on channel K^{↔}, **不是** K^{↔} 本身
- **2⊗2 PPT = SEP → E_R^PPT = E_R**: Horodecki 1996 — **文献 [THM]**；本 session 在 qubit abstractions (dephase/depolar/AD) 的 Choi 态 E_R^PPT SDP 与 E_R 数值匹配验证

**升级 eligibility 状态** (R0.2 三条件)：项目内升 [THM] 需 C1 (b) 人类纸笔复核 **或** C1 (a) 跨家族 PDF 直读 — 当前 C1 是 (c) 数值复现，本身合规但**与 C2 用户签字一并缺失** → 三条件未齐 → 本表条目暂留 [SYN] 而非 [THM]。

### 3.2 [SYN] 级（内部可用，原 [COROLLARY] 候选因 R5 修正而下调）

- **4 信道 tightness hierarchy** (upper_bound_report §11.3, v0.7 post-2026-04-24-evening):
  - Dephase (tele-cov): E_R^PPT ≡ K^{↔} channel (PLOB Eq.39 SDP 验证)
  - Depolar (tele-cov): E_R^PPT = E_R channel (修复后 Vollbrecht-Werner SDP 验证); channel K^{↔} ≤ E_R，真值 UNKNOWN
  - AD **non-tele-cov**: Q (channel, LB on K^{↔}) for γ ≤ 1/2 analytic; Choi-state E_R^PPT **not** channel UB per WTB 2017 → channel K^{↔}(AD) OPEN (see RETRACTION §8)
- **六态 E_R/SP_6st 比率 ~3-6× (per-signal)**: per-sifted 单位错误已修正，先前 ≤1.8× 结论撤回

### 3.3 [SYN] 级（内部可用, 不对外）

- **TF Pareto 与 Pirandola UB cand 同 √η slope** (同斜率 confirmed in all 40-80 dB range): √η 是 bosonic-asymptotic 放宽下最可能紧 scaling 的实证证据
- **BB84 Shor-Preskill 公式 EC cost 非紧**: 在 11% 阈值 SP → 0 而 E_R = 0.5，真 K^{↔} 离 SP 远（depolarizing tele-covariant → E_R = channel UB 合法）

### 3.4 [CONJ] / [UNKNOWN] （OPEN）

- **A/B/C 精确归因**: 需 Sub-Q3 升 [THM] 才可分解 prefactor 2000× gap
- **AD γ > 1/2 K^{↔}** (channel): 真值 OPEN；squashed entanglement / max-Rains / amortized REE 等 channel-level 工具待 R0.2 C1 paper-level work
- **umr 拓扑严格 H1-H6 主问题**: Sub-Q3 四路径 β.G4/β.G5/γ.B.G1/γ.G3 全部 OPEN

---

## 4. R0.2 三方验证状态表

| 结论 | C1 | C2 | C3 | 升级 eligibility |
|------|-----|-----|-----|------------------|
| β.G3 log_neg(E_AD) = log₂(1+η) | ✅ SymPy (c) | ✅ 用户 2026-04-23 | ✅ dev-reviewer R2 | [SYN] (无 THM anchor) |
| `e_r_depolarizing_analytic` bug 修复 | ✅ MOSEK SDP (c) | ⏳ | ✅ R5 PASS | bug 修复本身不需升级；E_R = 1-h(F) 正确 |
| AD Q for γ ≤ 1/2 (原 K_D) | ⏳ 等用户 paper-level | ⏳ | ✅ R5 PASS | [THM for qubit] 需 C1+C2+C3；Q = LB on K^{↔} |
| 4 信道 hierarchy | ✅ 数值 SDP (c) | ⏳ | ✅ R5 PASS | [SYN]；K^{↔}(depol) UNKNOWN；C2 用户签字待 |
| 六态 E_R/SP 比率 ~3-6× (per-signal) | ✅ 数值 (c) | ⏳ | ✅ R5 PASS | [SYN]（先前 ≤1.8× 因 units 错误已撤回） |
| Day 4 Codex 评审 | - | - | ✅ R5 PASS | C3 已通过 |

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

5. AD γ > 1/2 channel K^{↔} via squashed entanglement (或 max-Rains / amortized REE)
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

## 7. dev-reviewer 最终结果（已完成）

**最终状态**: **Round 5 PASS** — C3 闸门通过

**5 轮历程**:
- R1 → FAIL (UNSOUND): 3 major issues 发现（AD K_D/Q 混淆、unit 错误、hierarchy 方向错）
- R2 → FAIL: hierarchy 方向修复引入新反向写法
- R3 → FAIL: summary 文档术语 stale
- R4 → FAIL: dephasing 表 + PHASE 文档 K_D 残留
- R5 → **PASS**: 所有 major issues 已清除；残留 minor（3 个 K_D 散落 prose + `近紧` grep）

**产出清单**:
- `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/changes-v{1-5}.patch`
- `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-diff-{1-5}.json`
- `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-holistic-{1-3}.md`

**边界确认**: dev-reviewer (Claude + Codex 跨家族) = C3；不是 C1（C1 需双方 PDF 直读或人类纸笔或非 AI 工具）。R0.2 三条件仍需 C1 (C3 之外) + C2 用户签字同时满足才可升级 [COROLLARY]/[THM]。

---

## 8. 下一 session 入口

重启 session 的建议流程:

1. 读本文件 + [PHASE_STATUS.md](PHASE_STATUS.md)（一览进度 + 决策队列）
2. 读 [PHASE1_REPORT.md v1.1](PHASE1_REPORT.md) §9（Phase 2/3 延伸）
3. 读 `docs/workflow/day4-bug-fix-AD-KD-hierarchy-review/review-*.md/json`（Codex verdict）
4. 若 verdict = PASS: 等用户对 §5 决策队列 的回复
5. 若 verdict = FAIL/REJECTED: 按 R0.2 C3 立即处理

---

---

## 9. Evening followup — Codex R1-R7 retraction (AD channel-UB overclaim)

本 session 末续：尝试写 AD anti-degradable E_R^PPT memo，Codex R1 **REJECTED**（critical: Choi-state E_R^PPT 被误作 channel K^{↔} UB，但 AD 非 tele-covariant per WTB 2017 + PLOB 2017 Ex.3）。

7 轮 iteration (commits 0b8cf40 → 81d7c0d):

| Round | Verdict | 主要 residual |
|-------|---------|--------------|
| R1 | REJECTED | Fundamental channel-vs-state 混淆 |
| R2 | REJECTED | fill script print banner + stale TODO |
| R3 | REJECTED | AD_full_hierarchy docstring + PHASE1_REPORT + gap_analysis |
| R4 | REJECTED | AD_full_hierarchy runtime banner 依旧印 channel hierarchy |
| R5 | REJECTED | EPILOGUE §8 + FINAL §2.1 session log 残 K_D prose |
| R6 | FAIL | 3 minor prose residuals |
| **R7** | **PASS** | 无剩余 live overclaim outside retraction banners |

**产物**:
- RETRACTION §8: 第 6 次 silent-upgrade trap 记录（channel-vs-state，与 §7 cross-space trap 同家族）
- memory/feedback_channel_vs_state_trap.md: 固化教训 + red-flag checklist
- upper_bound_report.md v0.7: AD rows 标 "Choi only"，tele-cov 信道保持 channel-level
- AD CSV 数据保留（Choi-state 数值无错），语义解释降级完成

**教训**: Codex 独立评审在本 session 续 catch 到了 AI 本轮引入的 fundamental 错误。 R0.2 C3 闸门工作如预期 —— 但也暴露了 "一个 silent upgrade 会自动扩散到所有 summary/script/log" 的 repo-wide 污染问题，下次写 capacity 陈述前必须 **pre-flight check tele-cov 前提**。

---

## Changelog

- **v1.2** (2026-04-24 evening 续): §9 加入 — AD anti-degradable 尝试 + Codex R1-R7 retraction cycle + RETRACTION §8 + 第 6 次 silent-upgrade trap 固化。
- **v1.1** (2026-04-24 session 末续): 更新 dev-reviewer 结果（5 轮 → R5 PASS）；修正科学结论分级（六态 ≤1.8× 撤回 → per-signal ~3-6×；K_D → Q LB on K^{↔}）；R0.2 状态表同步。
- **v1.0** (2026-04-24 session 末): 首版。Day 4 完整 summary + R0.2 三方验证状态表 + 用户决策队列指向 PHASE_STATUS.md。
