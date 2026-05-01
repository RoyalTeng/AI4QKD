# Phase Status Snapshot — 2026-04-24 (last revised 2026-05-01)

**版本**：v1.2  
**日期**：2026-05-01（C2 user batch sign-off — path α 10 sub-gap 升级至 [COROLLARY]） / 2026-04-25（v1.1）  
**用途**：Phase 0/1/2/3 当前进度一览 + 用户决策队列

---

## 0. TL;DR

| Phase | 验收状态 | 主产出 |
|-------|---------|-------|
| **Phase 0** | ✅ 完成 | MS-EB 框架 + WLC SDP + 七族五元组 + M1-M4 数值 |
| **Phase 1** | ✅ 完成 (v1.1) | 三族 Pareto 2581+2831+1600 pts + Kamin GEAT + family_comparison 主图 |
| **Phase 2 (Sub-Q3)** | 🟡 部分完成 → 10/12 sub-gap [COROLLARY] | upper_bound_report v0.7 + path α 10 sub-gap C1+C2+C3 闭合 + 2 OPEN (L2.G3 + L3.G3) + β.G3 [SYN] |
| **Phase 3 (Sub-Q4)** | 🟡 初步（数据驱动 [CONJ]） | gap_shape v0.3 4 candidates + gap_analysis G4.2 v0.1 归因初稿 |

**AI 自主边界**：10/12 sub-gap 经 C1(a) + C2 (2026-05-01) + C3 升级至 [COROLLARY]。2/12 OPEN (L2.G3 + L3.G3) 仍等用户 paper-level work。Combined chain 仍 [SYN, conditional]。

---

## 1. Phase 0 — MS-EB 框架与基础设施

**状态**：✅ **完成**（[PHASE0_REPORT.md](PHASE0_REPORT.md)）

### 完成项

- ✅ `qkdx/` 代码库（协议/信道/numerics 三大模块）
- ✅ MS-EB 五元组 Π=(P,E,A,T,K) 形式化
- ✅ WLC SDP 求解器（Winick-Lütkenhaus-Coles 2018）
- ✅ 七族协议五元组文档（`docs/families/`）：BB84, six-state, Efficient BB84, MDI, PM-QKD, (F3 SARG04 spec_only), (F7 decoy BB84 via M3)
- ✅ M1-M4 数值验证（误差 < 1% BB84/MDI，< 5% TF/MP）
- ✅ [`framework_coverage.md`](research/framework_coverage.md)

### 已知 spec_only 项

- F3 SARG04: Koashi 2005 announcement register 需扩展 → Phase 1 末 (v0.3 简化实现已回滚, 先例 [PHASE1_LOG.md §2.1](PHASE1_LOG.md))
- RRDPS: block-level subspace counting security ≠ Devetak-Winter MS-EB → out_of_scope (Tamaki 2014 精读后 2026-04-23 确认)

---

## 2. Phase 1 — 协议族 Pareto + 有限密钥

**状态**：✅ **完成**（[PHASE1_REPORT.md v1.1](PHASE1_REPORT.md)）

### 2.1 Sub-Q2 三族 Pareto 硬验收

| 验收项 | 要求 | 实际 |
|---|---|---|
| 每族 ≥ 1000 pts | 硬 | BB84=1600, MDI=2581, TF=2831 ✓ |
| Pareto 上包络 | 硬 | 三族全部 ✓ |
| 族间比较图 | 硬 | [family_comparison.png](research/figures/family_comparison.png) ✓ (2026-04-24 v2 加 Pirandola UB cand) |
| Kamin 2025 < 5% 复现 | 硬 | qubit ±15% (gap 记录), decoy ±3x (WL22 beamsplitter 需扩展) |

### 2.2 有限密钥 GEAT 层

- ✅ Kamin 2025 Choi SDP + Thm 3/4 + Eq. 38/39 V² + Eq. 79 block-diag decoy SDP + Eq. 53 τ-slack
- ✅ 79 tests 全绿
- 残余 gap: qubit 5-cell refactor + decoy WL22 beamsplitter（[PHASE1_REPORT.md §7](PHASE1_REPORT.md)）

### 2.3 交叉点数据（首次定量）

- BB84 → TF: ~8 dB（TF 超越 MDI）
- MDI cutoff: ~56 dB
- TF cutoff: > 80 dB
- 全 loss 区间 PLOB UB > 3 族 rate

---

## 3. Phase 2 — Sub-Q3 上界工具链

**状态**：🟡 **部分完成**（AI 自主 ceiling = [CONJ]/[SYN]）

### 3.1 完成项

- ✅ **upper_bound_report.md v0.7**（1000+ 行，11 sections；v0.5 = Day 4 内嵌增补，v0.6 = R5 修正，v0.7 = 2026-04-25 followup-review 后修订）
  - §1-§10: Pirandola / TGW / WTB / Khatri-Wilde / log_neg / E_R^PPT SDP
  - §11 (Day 4, v0.6): 4 信道 tightness hierarchy + AD Q analytic (LB on K^{↔}) + Plenio 不等式 + BB84/six-state 紧化（已单位修正）
- ✅ **路径 β.G3 (log_neg 前传)**: `log_neg(E_AD(η)) = log₂(1+η)`, η_c=1/φ
  - C1(c) SymPy 符号验证 PASS
  - C2 用户签字 PASS
  - C3 dev-reviewer Codex R2 PASS
  - 标签：**[SYN]**（THM anchor search 无果，保持 [SYN]）
- ✅ **Day 4 数值补强**（commits b4efaae → 7e17e44）
  - `e_r_depolarizing_analytic` bug 修复（d²-1 vs d-1）
  - `quantum_capacity_amplitude_damping_degradable` (Q = LB on K^{↔}) for γ ≤ 1/2
  - 4 信道 Plenio 不等式 E_R ≤ log_neg 数值验证 800 pts (Choi-state level for AD; channel level for tele-covariant dephase/depolar/erasure per PLOB Ex.3; AD channel K^{↔} UB unresolved per RETRACTION §8)

### 3.2 OPEN 结构 gap（等用户 paper-level work）

| Gap ID | 内容 | 依赖文献 |
|--------|------|---------|
| **β.G4** | Eve model transfer: TF-QKD Pareto 在 umr 拓扑下是否低于 Pirandola UB | Khatri-Wilde 2020 §19 Prop 19.2 |
| **β.G5** | Adversarial comb reduction: amortization 在 untrusted relay 下继承 | WTB 2017 Thm 4 / Cor 5 |
| **γ.B.G1** | DPI target lemma: 受信道数据处理不等式的更紧上界 | 多文献直读 |
| **γ.G3** | ε-composable transfer: 可组合安全框架下 gap 变化 | Metger 2024 GEAT + Kamin 2025 asymptotic→finite 桥接 |

**撤回先例**（不得重蹈）:
- path γ v0.2 retraction (2026-04-21): AI "简化 adversarial containment" 绕过 Log 07 三 lemma 明写要求 → 两 reviewer 独立 UNSOUND

### 3.3 Sub-Q3 上界候选清单

| 候选 | 公式 | 适用 | 严谨性 |
|------|------|------|--------|
| PLOB direct | `-log₂(1-η)` | 直连信道 | [THM] |
| Pirandola N=1 | `-log₂(1-√η)` | umr Type B 对称 | [CONJ for umr] |
| TGW (squashed E) | `log₂((1+η)/(1-η))` | bosonic, pure loss | [THM for bosonic] |
| E_R^PPT SDP | 数值 | qubit abstraction | [THM for channel, SYN for umr via lemma] |
| log_neg analytic | log₂(2-γ) for AD | qubit abstraction | [THM] |
| AD Q (LB on K^{↔}) | max_p[h₂((1-γ)p)-h₂(γp)] | qubit AD degradable γ≤1/2; K^{↔} ≥ Q | [THM for qubit Q] |
| AD K^{↔} (anti-degradable) | OPEN | γ>1/2; Q=0 but K^{↔} OPEN | [UNKNOWN] |

---

## 4. Phase 3 — Sub-Q4 Gap 形状 + 归因

**状态**：🟡 **初步完成**（数据驱动 [CONJ] 级）

### 4.1 完成项

- ✅ **gap_shape_g4_1.md v0.4**（3 UB candidates A/B/C；AD Q 为参考量非 UB）
  - Candidate A/B/C 横跨 bosonic-asymptotic + qubit abstraction
  - Slope 分析: TF Pareto 与 Pirandola UB cand 同 √η
  - Prefactor gap: ~2000× at 40 dB
- ✅ **gap_analysis_2026-04-24.md v0.1 (G4.2 归因初稿)**
  - A (UB 松) / B (LB 松) / C (A+B) 三类诊断框架
  - BB84 SP: **B 显著**（SP→0 at 11% 阈值 vs E_R=0.5）
  - 六态 SP: **中等**（E_R/SP ~3-6× per-signal；先前 ≤1.8× 单位错误已修正 2026-04-24）
  - TF/MDI umr: UNKNOWN pending Sub-Q3 升 [THM]

### 4.2 OPEN 项（AI 自主 reach 不到）

- **A vs B prefactor 分解**：需 Sub-Q3 上界升 [THM] 后才可精确量化
- **decoy / squashed entanglement / Khatri-Wilde §19 / WTB bonds**: 用户 PDF 精读需求

### 4.3 FINDINGS v2 interim verdict 支持度

| Verdict | 数据支持 | 状态 |
|---------|---------|------|
| TF-QKD 族 √η 可达 | TF Pareto 60 dB rate ≈ 10⁻⁶ | [THM] 确立 (Phase 1 §2.2) |
| Bosonic-asymptotic 放宽下 √η 是紧 scaling | Pirandola UB cand 与 TF 同斜率 | [SYN] 实证支持 (Day 4) |
| 严格主问题 H1-H6 答案 | Sub-Q3 OPEN | [UNKNOWN] |

---

## 4.5 User directive 2026-04-25 — path α 三 lemma 优先策略 **[USER-APPROVED PRIORITY, §7.3 OVERRIDDEN by user 2026-04-25]**

> **🟡 [USER-APPROVED PRIORITY 2026-04-25 — direction-level approval, NOT C3-passed]**
>
> v0.3 dev-reviewer round 2 verdict REJECTED (diff) + FAIL (holistic) 触发了 §7.3 rollback condition。
>
> **user 2026-04-25 同 session 显式 override §7.3**（user 原话）："如果和红线违背，那就以我的 approve 为准 ... 我已经经过反复论证了，我的 approve 没问题"
>
> **override scope**：approve **path α direction** + v0.3 维持 active draft；**不**等价 C3 PASS；**不**等价 [SYN] → [COROLLARY] 升级；**不**得对外引用 lemma 表述为定理级。
>
> **R0.2 硬红线维持**：[COROLLARY] / [THM] 升级仍需 C1 ∧ C2 ∧ C3 完整流程。user override 仅适用于 cleanup-level + direction priority。
>
> **诚实风险记录**：user override Codex C3 verdict 的先例对应 v1 retraction（user 当时也 "反复论证过"）。后续若发现同型 trap → 按 v1 retraction 流程处理。
>
> ---

**用户决议**（autonomous session 内显式给出）：

> 反转 Log 07 的 γ-first 优先级。**path α 三 lemma 路径**（resource-enhancement / protocol-class inclusion，旧 [umr_path_alpha_scaffolding.md](proofs/umr_path_alpha_scaffolding.md) 的 11-gap 形式）作 Phase 2 优先策略，**优先于** path γ direct converse 与 path β 紧界 converse。
>
> **理由**（用户原话）："我手头时间紧迫，γ 估计需要更长精读周期，先看 α 能否在更短周期出 scaling-级结论。"

**directive scope**（重要边界）：

- ✅ approve **方向**与**优先级**：path α 三 lemma 是 Phase 2 优先 work direction
- ✅ approve **scaling 级目标**：仅追求 $K_{\text{umr}} \leq -\log_2(1-\sqrt{\eta_{AB}})$ scaling 级 looser UB；**不**追求 prefactor-紧 UB
- ❌ **不** approve [umr_path_alpha_three_lemma_v0_2.md](proofs/umr_path_alpha_three_lemma_v0_2.md) v0.2 [REJECTED] 文档的任何具体 lemma 表述、综合链或 [SYN] 数值断言
- ❌ **不** approve 任何 Lemma A/B/C 的 closure / draft proof / Justification sketch
- ❌ **不** approve 升级路径绕过 R0.2 (C1 ∧ C2 ∧ C3) 三闸门

**v0.2 retraction 维持**；后续 v0.3 重写产出按此 directive 进行。**任何 [SYN] → [COROLLARY] 升级**仍需 R0.2 (C1 ∧ C2 ∧ C3) 完整流程，user directive 仅 approve 方向不替代 C2 升级签字。

**回滚条件**：v0.3 dev-reviewer 再 REJECTED → directive 失效，回到 Log 07 的 γ-first 顺序。

### 4.5.1 C2 签批结果 (2026-05-01)

path α 10/12 sub-gap 经 C1(a) + C2 (user batch sign-off) + C3 完整流程，升级至 **[COROLLARY]**：
- ✅ **Lemma A 全部 4 个**：[COROLLARY]
- ✅ **Lemma B 3 个** (L2.G3 OPEN 除外)：[COROLLARY]
- ✅ **Lemma C 3 个** (L3.G3 OPEN 除外)：[COROLLARY]
- 🔓 **L2.G3 + L3.G3 (5 sub-residuals)**：仍 [UNKNOWN] OPEN
- Combined chain：仍 [SYN, conditional]
- 签批记录：[path_alpha_c2_signoff_2026-05-01.md](proofs/path_alpha_c2_signoff_2026-05-01.md)

---

## 5. 用户决策队列（AI 自主 reach 不到）

按优先级从高到低（**§4.5 directive 生效，user 2026-04-25 override §7.3** — path α 三 lemma framework 升至最高）：

### 5.1 Sub-Q3 结构 gap (R0.2 C1 非 AI 验证依赖)

**§4.5 user-directive 顺序**（2026-05-01 更新，C2 签批后）：

1. **path α 三 lemma framework** ([v0.3 → 10/12 [COROLLARY]](proofs/path_alpha_subgap_closure_integration_v0_3.md))：10 sub-gap C1+C2+C3 闭合 ✅；剩 L2.G3（cross-space Eve set 声明）+ post-split L3.G3（5 项 Pirandola Eq. 11 specialization）。**剩余 2 OPEN 仍需 user paper-level work**。
2. **β.G4 Eve model transfer** — Khatri-Wilde 2020 §19 Prop 19.2 umr 适用性（path α scaling-级失败时的 fallback；prefactor-紧 UB 仍依赖此）
3. **β.G5 adversarial comb reduction** — WTB 2017 Thm 4 umr 继承
4. **γ.B.G1 DPI target lemma** — Pirandola 2019 Eq. 9 拓扑适用性
5. **γ.G3 ε-composable transfer** — Metger 2024 GEAT asymptotic→finite 桥接

**回滚指针**（若 user 后续撤销 override）：original Log 07 γ-first 顺序 = β.G4 → β.G5 → γ.B.G1 → γ.G3

### 5.2 数值扩展（用户启动后 AI 可继续）

5. **AD channel-level K^{↔} 上界工具选型 + paper-level 验证**（anti-degradable γ>1/2 区 Q=0；channel K^{↔} OPEN per RETRACTION §8）：先做 (a) 候选工具家族选型（amortized REE / max-Rains / squashed entanglement / 其他 channel-level converse for non-tele-cov），再 (b) PDF-level 验证适用性条件，**最后**才考虑 (c) 数值实施。**步骤 (a)/(b) 是 R0.2 C1 外部依赖**，不在 AI 自主范围；步骤 (c) 在 (a)/(b) 完成后可恢复 AI 自主
6. **Erasure E_R^PPT SDP** — 需高内存环境（16×16 OOM）
7. **SARG04 严格实施** — Koashi 2005 announcement register 扩展

### 5.3 Phase 1 残余 (L1-L5)

8. BB84 decoy+misalignment 带入族比较图
9. qubit Kamin 5-cell refactor（cutoff 偏 6 dB 修正）
10. decoy Kamin WL22 beamsplitter honest model（~3x 系数 offset 闭合）

### 5.4 升级待签 (C2 用户签字)

**2026-05-01 更新**：path α 10 sub-gap C2 已完成。

剩余待签：
- β.G3 [SYN] 若找到 THM anchor (Wilde-Horodecki 2013 / Plenio-Virmani 2007 §V.C) 可升 [THM]
- upper_bound_report v0.7 §11 hierarchy table 可升 [COROLLARY]（仅 tele-covariant 信道行 — dephase/depolar/erasure；AD 行 channel-level UB 仍 OPEN per RETRACTION §8）
- gap_analysis G4.2 可升到 [THM] 级归因 verdict
- L2.G3 + L3.G3 闭合后 combined chain 可升 [COROLLARY]

---

## 6. AI 自主 pipeline 调用边界（R0.2 硬红线）

**C1 (independent validation) 必须满足 (a)/(b)/(c) 之一**：
- (a) 跨家族模型 **双方直读 PDF** (Claude + GPT/Codex 不含纯 AI 综述转述)
- (b) 人类研究者纸笔复核
- (c) 非 AI 工具（SDP / SymPy / proof assistant）独立复现

**C3 (dev-reviewer 双 Codex QA)** ≠ C1 —— dev-reviewer 是**强制 QA 闸门**但**不满足 C1**（Claude + Codex 是跨家族 AI 审计链，不含 PDF 直读或非 AI 验证）。

**合法升级路径**：C1 (a/b/c) ∧ C2 (用户签字) ∧ C3 (dev-reviewer PASS)。

**先例**（禁止重蹈）:
- v1 FINDINGS retraction (2026-04-19): AI 自行 [SYN] → [COROLLARY] 未 C2
- path γ v0.2 retraction (2026-04-21): AI 简化绕过 identified gap

---

## 7. 产出清单（Phase 0-3 累计）

### 7.1 文档

- **总报告**: [PHASE0_REPORT.md](PHASE0_REPORT.md), [PHASE1_REPORT.md](PHASE1_REPORT.md)
- **Sub-Q3**: [upper_bound_report.md v0.7](findings/upper_bound_report.md)
- **Sub-Q4**: [gap_shape_g4_1.md v0.3](findings/gap_shape_g4_1.md), [gap_analysis_2026-04-24.md v0.1](findings/gap_analysis_2026-04-24.md)
- **Pareto family sheets**: [pareto_bb84_family v0.2](findings/pareto_bb84_family.md), [pareto_mdi_family v0.2](findings/pareto_mdi_family.md), [pareto_tf_family v0.2](findings/pareto_tf_family.md)
- **证明**: [log_neg prefactor crossover (β.G3 analytic)](findings/log_neg_msEB_application_2026-04-23.md), [qubit E_R PPT hierarchy](findings/qubit_E_R_PPT_hierarchy_2026-04-23.md)

### 7.2 数值数据

- `docs/research/data/*.csv` — 7000+ 扫描点 (MDI + TF + BB84 F4 + Kamin Fig1)
- `docs/research/figures/*.{png,pdf}` — 30+ 图表

### 7.3 代码

- `qkdx/` 核心库 + 79 tests 全绿 (Phase 1 末)
- Day 4 新增 13 tests in `TestAnalyticLogNegFormulas`

### 7.4 Session logs

- [AUTONOMOUS_SESSION_2026-04-21_LOG.md](AUTONOMOUS_SESSION_2026-04-21_LOG.md)
- [AUTONOMOUS_SESSION_2026-04-22_LOG_v2.md](AUTONOMOUS_SESSION_2026-04-22_LOG_v2.md)
- [AUTONOMOUS_SESSION_2026-04-23_LOG.md](AUTONOMOUS_SESSION_2026-04-23_LOG.md)
- [AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md v0.2](AUTONOMOUS_SESSION_2026-04-23_EPILOGUE.md)
- [PHASE1_LOG.md](PHASE1_LOG.md)

---

## Changelog

- **v1.0** (2026-04-24): 首版。Phase 0-3 状态快照 + 用户决策队列 + R0.2 边界说明。
