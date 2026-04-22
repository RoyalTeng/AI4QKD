# Main Question & Sub-Q Integration Status — 2026-04-22 (autonomous integration audit)

**类型**：Sub-Q aggregate audit + upgrade-path map
**作者**：AI Claude (autonomous session 2026-04-22)
**授权**：2026-04-21 user delegation under autonomous mode — process-level integration document, **NOT** rigor-grade upgrade
**严谨性分级**：**[SYN]** aggregate over existing [CONJ]/[SYN]/[THM] project artifacts；**不**引入任何新的 rigor 级别陈述
**预备**：[PROSPECTUS.md](../PROSPECTUS.md) + [RESEARCH_PLAN.md](../RESEARCH_PLAN.md) + [FINDINGS.md v2](../research/FINDINGS.md) + [CLAUDE.md](../../CLAUDE.md)

---

## 0. 目的

本文档**聚合**现有的 Sub-Q1 / Sub-Q2 / Sub-Q3 / Sub-Q4 + 主问题状态，给用户归来后一个单文件 snapshot。**不**做新推导；**不**升级任何分级。

---

## 1. 主问题状态（PROSPECTUS v3.1 §1）

> **主问题**：对 "两方 + 一个 untrusted measurement relay + 纯损耗" 拓扑 $\mathcal{T}_\text{umr}$，在 H1-H6 硬约束下，是否存在情况 A、B、C？

**严格 H1-H6 版本**：**[UNKNOWN]** — FINDINGS v2 §1.2 明示；H4/H5/H6 未覆盖

**放宽 bosonic-asym 版本**（H4/H5/H6 放宽）：
- Scaling = $\sqrt{\eta_{AB}}$：**[SYN]**（FINDINGS v2 §1.2）
- 情况 A 成立：**[SYN conditional on upper bound]**
- 情况 B/C 排除：**[CONJ]**（依赖 upper bound 严格继承）

**主问题明确结论**（autonomous 级，不升 [THM]）：

> 在 **放宽版** $\mathcal{T}_\text{umr}^\text{bosonic-asym}$（允许无穷维 Fock + asymptotic collective attack + coherent-state achievability）下，**scaling 最可能为** $\sqrt{\eta_{AB}}$（情况 A 方向）。**但** 严格 H1-H6 版本的主问题仍为 **[UNKNOWN]**。

---

## 2. Sub-Q1 状态（MS-EB 框架能否统一表达 DV-QKD 协议）

**结论**：**✅ CLOSED** (Phase 0 所有里程碑通过，详见 [PHASE0_REPORT.md](../PHASE0_REPORT.md))

| 验收项 | 状态 |
|---|---|
| M1 WLC SDP BB84 | ✅ |
| M2 六态 + MDI ideal GLLP | ✅ (Ma-Razavi Fig.3 延后到 Phase 1 per §1.2) |
| M3 诱骗态 + facial reduction | ✅ |
| M4A 对称性约化 | ✅ |
| Framework coverage (PROSPECTUS Sub-Q1 (d)) | ✅ (6 protocol families covered / partial / out_of_scope 标注) |

**主问题 bearing**：Sub-Q1 是工具层，不直接答主问题；已提供 BB84 / 六态 / MDI / decoy / TF (M4B partial) 的 MS-EB 编程平台。

---

## 3. Sub-Q2 状态（已知协议族的紧密钥率下界 Pareto 前沿）

**结论**：**基本闭合，两个 open 项**

| 验收项 | 状态 |
|---|---|
| S2.1 family sheets (BB84 / MDI / TF) | ✅ |
| S2.2 Pareto 前沿 (2831 TF + 2581 MDI pts) | ✅ |
| S2.3 器件不完美 | ✅ |
| S2.4 Metger 2024 GEAT Level 4 | ✅ ([GEAT-2024.md](../literature/GEAT-2024.md)) |
| S2.5 Kamin 2025 qubit Fig.1 | **partial** — 定位 cutoff ±6 dB (user 2a 签字) + positive-rate ±15%；T2-A 尝试 < 5% (proxy milestone only, ADR 0001 Accepted 2026-04-22) |
| S2.5 Kamin 2025 decoy Fig.3 | **OPEN** — 用户 3b 签字要求 < 5%；T2-B deferred 至 Phase 2 per ADR 0001 |

**硬结论（可 cite，不升级）**：

- **[THM]** TF-QKD 族 (Lucamarini 2018) 在放宽 bosonic-asymptotic 下可达 $\sqrt{\eta_{AB}}$ scaling
- **[THM]** MDI-QKD (Lo-Curty-Qi 2012) 安全性 via virtual-EB picture；asymptotic rate = Q_rect[1 - H(e_{X,1})] - Q_rect·f_EC·H(e_{Z,1})
- **[THM]** qubit BB84 QBER 阈值 ≈ 11.00% (Shor-Preskill)；六态 ≈ 12.62% (Lo 2001)
- **[CONJ]** MDI-QKD virtual-EB Werner reduction 在 `kamin_sdp_mdi.py` 的实现 (详见 [docs/proofs/mdi_werner_reduction.md](../proofs/mdi_werner_reduction.md) v0.3)

---

## 4. Sub-Q3 状态（已知上界工具在 MS-EB 框架下给出什么上界）

**结论**：**literature stack 完整；严格 umr 上界仍 [CONJ]；path γ v0.2 已 retract**

| 验收项 | 状态 |
|---|---|
| U3.1 TGW 2014 Level 3 | ✅ ([TGW-2014.md](../literature/TGW-2014.md)) |
| U3.2 PLOB 2017 Level 4 | ✅ ([PLOB-2017.md](../literature/PLOB-2017.md)) |
| U3.3 WTB 2017 Level 3 | ✅ ([WTB-2017.md](../literature/WTB-2017.md), Thm 12/19 修正) |
| U3.4 Pirandola 2019 Level 4 | ✅ ([Pirandola-2019.md](../literature/Pirandola-2019.md) + [Log 07 technical audit](../research/07_pirandola_2019_technical_audit.md) user 主笔) |
| U3.5 Khatri-Wilde 2020/2024 Level 3 (Ch 19-20) | ✅ ([KhatriWilde-2020.md](../literature/KhatriWilde-2020.md)) |
| U3.6 上界 MS-EB 重写 | partial ([upper_bound_msen.md](../proofs/upper_bound_msen.md) 196 行) |
| U3.7 Relative entropy SDP toy channels | ✅ ([upper_bound_report.md §4](upper_bound_report.md)) |
| U3.8 接缝报告 30-50 页 | partial ([upper_bound_report.md](upper_bound_report.md) 356 行) |
| Pirandola 2019 适用性 (untrusted relay) | **[CONJ]** — Log 07 path α / β / γ 三路径状态（2026-04-22 update）见下 |
| path α (monotonicity reduction) | **scaffolding-only** ([umr_path_alpha_scaffolding.md](../proofs/umr_path_alpha_scaffolding.md) 11 gaps); Codex 5-round: identity-embedding = v0.2 containment class, 不能作 derivation |
| path β (channel-reduction) | **[CONJ]** derivation attempt ([umr_path_beta_derivation.md](../proofs/umr_path_beta_derivation.md) v0.2+R3, 5 gaps); tightness vs Pirandola min-cut **agnostic** per Log 07 §4.4 |
| path γ v0.4+R3 (Log 07 §4.5 minimal baseline) | **[CONJ]** derivation attempt ([umr_path_gamma_v0_4_derivation.md](../proofs/umr_path_gamma_v0_4_derivation.md), 5 gaps); v0.2 (set-inclusion) + v0.3 (super-receiver) retracted 之后的 v0.4 是最干净版；Step B 降级 target DPI lemma 非 capacity transfer |

**硬结论**：

- **[COROLLARY of PLOB 2017]** 对点对点纯损 bosonic channel：$R \leq -\log_2(1-\eta)$；high-loss asymptote $\approx 1.44·\eta$
- **[COROLLARY of TGW 2014]** 对点对点纯损 bosonic channel：$R \leq \log_2\frac{1+\eta}{1-\eta}$；PLOB 紧 2×
- **[COROLLARY of Pirandola 2019 Eq.11 for trusted relay]** 单路径 trusted-relay：$R \leq -\log_2(1-\sqrt\eta)$；但**未** certify 到 umr (Log 07 Step C 失效)
- **[CONJ]** umr 上界 $R \leq 1.44·\sqrt{\eta_{AB}}$ — 依赖 untrusted-relay capacity monotonicity；**未**升级到 [COROLLARY]；v0.2 adversarial containment shortcut 已撤回

**Sub-Q3 明确结论**（autonomous 级）：

> umr 拓扑的 scaling upper bound **最可能为** $\sqrt{\eta_{AB}}$（per literature synthesis），**但** 严格 converse 继承仍为 **[CONJ]**。Log 07 path α (monotonicity + 三 lemma) / β (channel-reduction) / γ (single-edge PLOB + data-processing 真版) 三条路径任一的**用户形式化工作**可 close 技术层的 converse gap（此时用户纸笔可满足 R0.2 C1(b)）；**但** 由此技术闭合到 rigor 分级 [COROLLARY] 的升级**仍**单独需要 C2（用户明示签字）+ C3（dev-reviewer PASS），按 CLAUDE.md R0.2 的 C1 ∧ C2 ∧ C3 invariant **三条件并列必要**。

---

## 5. Sub-Q4 状态（Gap 刻画 + 归因 A/B/C）

**结论**：**gap shape 完成 [CONJ]；归因 G4.2 blocked on Sub-Q3 upper bound 升级**

| 验收项 | 状态 |
|---|---|
| G4.1 Gap 定量形状 | [CONJ] ([gap_shape_g4_1.md](gap_shape_g4_1.md)) |
| G4.2 Gap 归因 A/B/C | **blocked** — 触发条件 (Log 07 path γ 形式化 + 上界 [COROLLARY] 升级) 未满足 |

**硬结论**：

- **[CONJ for umr, scaling level]** 在对称 bosonic-asym 下，候选上界 scaling = $\sqrt{\eta}$（all 3 candidates [CONJ]）；下界 scaling = $\sqrt{\eta}$ ([THM] from TF-QKD family per FINDINGS v2)；**两端 scaling 同阶**
- **[CONJ, prefactor level]** 具体 prefactor 数值详见 [gap_shape_g4_1.md §2.1](gap_shape_g4_1.md)（PM-QKD numerical lower bound $\sim 10^{-3}\cdot\sqrt{\eta}$ + 候选 A/B 上界 $\sim 1.44\sqrt{\eta}$）；prefactor ratio **大约 3 orders of magnitude**（quantitative detail 见 gap_shape_g4_1.md，本 memo 不在此处算术化）
- **[UNKNOWN]** 归因是 α / β / γ — **明示 retracted 状态**：v1 FINDINGS + Log 07 + gap_shape_g4_1.md §3 均确认**归因判断 retracted**；任何 "γ 最可能" 之类的前预判**不应**在此 snapshot 中 revived

**Sub-Q4 明确结论**（autonomous 级）：

> gap 的**scaling 形状**刻画为 $\sqrt{\eta}$ vs $\sqrt{\eta}$ 同阶（[THM] 下界 + [CONJ] 上界）；**prefactor gap 大小** 详见 gap_shape_g4_1.md；**归因**（A/B/C）**仍为 [UNKNOWN]** — retracted claim 不在此文件 revived；启动 G4.2 需 Sub-Q3 upper bound 升级 (user C1 ∧ C2 ∧ C3)

---

## 6. 主问题答案清单（可 cite 格式）

### 6.1 Definitive (at [THM] / [COROLLARY] 级别，可对外 cite with caveats)

| # | 陈述 | 分级 | Scope |
|---|---|---|---|
| T1 | Point-to-point pure-loss bosonic channel 两方 $R \leq -\log_2(1-\eta)$ | [COROLLARY of PLOB 2017] | point-to-point bosonic/asymptotic theorem; **放宽 H4 / H5 / H6** (bosonic, infinite-dim Fock, asymptotic)；**不含** untrusted relay 层；**非** H1-H6 严格主问题答案 |
| T2 | TF-QKD (Lucamarini 2018) 在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下可达 $\sqrt{\eta_{AB}}$ | [THM] | 放宽 H4/H5/H6 |
| T3 | qubit BB84 阈值 11.00%, 六态 12.62% | [THM] | N/A for main Q |

### 6.2 [SYN] / [CONJ] (内部可用，对外禁止单独 cite)

| # | 陈述 | 分级 | Blocker to upgrade |
|---|---|---|---|
| S1 | umr scaling 最可能为 $\sqrt{\eta_{AB}}$ (放宽版) | [SYN] | 严格 converse 继承需 Log 07 path α/β/γ 形式化 + C1 ∧ C2 ∧ C3 |
| S2 | umr 上界 $\lesssim 1.44·\sqrt{\eta_{AB}}$ | [CONJ] | 同上 |
| S3 | 情况 A 成立 (放宽版) | [SYN] | 依赖 S2 |
| ~~S4~~ | ~~Gap 归因 γ (两端松) 最可能~~ — **已 retract** per v1 FINDINGS + gap_shape_g4_1.md §3 | N/A | 归因 A/B/C **明确 [UNKNOWN]**；G4.2 blocked 在 Sub-Q3 upper bound 升级 + C1 ∧ C2 ∧ C3 |

### 6.3 [UNKNOWN]

| # | 问题 | 升级路径 |
|---|---|---|
| U1 | 严格 H1-H6 版本主问题答案 | 需 H4 (Fock 截断) + H5 (Portmann-Renner composable finite-key) + H6 (严格 DV) 扩展工作 — 属 Phase 2-3 |
| U2 | Sub-Q4 归因 A/B/C 定量 | 需 Sub-Q3 upper bound 升至 [COROLLARY] (完整 C1 ∧ C2 ∧ C3 三条件) — user 纸笔可满足 C1(b) + C2，但仍需 C3 dev-reviewer PASS |
| U3 | TF-QKD 族外是否存在填 gap 的新协议 | Phase 3 Sub-Q4 归因 B 子任务 (如触发) |

---

## 7. R0.2 C1 + C2 + C3 Upgrade 路径（等用户归来）

**升级到 [COROLLARY] / [THM] 的硬 invariant**（[CLAUDE.md R0.2](../../CLAUDE.md) + [research-rigor.md R2.2](../../.claude/rules/research-rigor.md)）：**C1 ∧ C2 ∧ C3 三条件并列必要，任一缺失即非法**。

- **C1 (independent review)** 必要且独立：(a) 跨家族 AI + 直读 PDF；或 (b) 人类纸笔复核；或 (c) 非 AI 工具独立复现。同家族 AI 多运行或纯 AI 审计链**不**计入 C1。
- **C2 (用户显式签字)** 必要。用户的纸笔证明工作可同时满足 C1(b)，但仍需**另外**对升级分级做 C2 签字；C1(b) 不替代 C2。
- **C3 (dev-reviewer PASS)** 必要。dev-reviewer 即便 PASS 也**不**替代 C1；它是独立于 C1 / C2 的 QA 闸门。

| 升级目标 | 当前 C1 满足情况 | 当前 C2 满足情况 | 当前 C3 满足情况 | 优先级 |
|---|---|---|---|---|
| umr 上界 → [COROLLARY] | **未满足** — 需 (a)/(b)/(c) 任一 | **未满足** — 用户 C2 签字 pending | path γ v0.2 已 REJECTED；v0.3 未启动 | **最高** |
| Werner reduction → [COROLLARY] | **未满足** — 需 (a)/(b)/(c) 任一 | **未满足** — pending | R3 双 Codex: Agent 2 PASS, Agent 1 FAIL (downstream fixed @ 9ede1fd); partial C3 | **中** |
| Sub-Q4 G4.2 归因 | blocked on umr 上界 | 同上 | 同上 | blocked |

---

## 8. 本 snapshot 的限制

1. **仅 aggregation**，**不**引入新 rigor 陈述
2. 具体数字 (prefactor 值 / ratio) 源于 gap_shape_g4_1.md，本 snapshot **不**做算术合成
3. 不改 FINDINGS v2 / Log 07 / PHASE0_REPORT 任何分级
4. [SYN] 级聚合判断本身**不**可对外单独 cite；升级到 [COROLLARY] 需 **完整 C1 ∧ C2 ∧ C3**（三条件并列必要）
5. v0.2 修正 (2026-04-22 Round 2)：
   - 去除 v0.1 的 S4 "Gap 归因 γ 最可能" 误 revived claim（属 v1 retracted 模式，已 strike-through 标注）
   - 上升路径全部补 C3 必要性（v0.1 的 "user C1+C2" 措辞弱化）
   - T1 scope 补充 bosonic/infinite-dim 也放宽 H4/H5/H6 的事实
   - Prefactor 数字从 "1000×" 改为 "见 gap_shape_g4_1.md" 避免 algebraic mismatch

---

## 9. 下次 user session 的建议 agenda (按价值排序)

1. **最高价值**：审签 [umr 上界] path 选择（α / β / γ）+ 启动其中一条的严格形式化（需 ≥ 1 人日 用户工作）
2. **中价值**：审签 T1 Werner reduction v0.3 [CONJ] (20 min 用户阅读 + 2-3 天独立 C1 验证)
3. **中价值**：review ADR 0001 acceptance (T2 split 是否符合预期)
4. **低价值**：review session log + commit trail (20 min)

---

## 10. 命题 lookup table（for future citation）

| Prop ID | 陈述 | 分级 | 来源 |
|---|---|---|---|
| **P1** | 主问题答案（放宽版）= 情况 A | [SYN] | FINDINGS v2 §1.3 |
| **P2** | $R_\text{upper} \leq 1.44 \cdot \sqrt{\eta_{AB}}$ on umr (放宽版) | [CONJ] | FINDINGS v2 §1.1 |
| **P3** | $R_\text{lower} \geq c_\text{strict} \cdot \sqrt{\eta_{AB}}$ via TF-QKD family (with $c_\text{strict} \approx 0.2$ 严格 $\mathcal{T}_\text{umr}$; $c_\text{ext} \approx 0.3$ 扩展 $\mathcal{T}_\text{umr}^+$ 含 MP-QKD) | [THM] | Lucamarini 2018 via FINDINGS v2 §1.1 |
| **P4** | Gap scaling identical $\sqrt{\eta}$ 同阶；prefactor gap 量级见 gap_shape_g4_1.md (上界候选 1.44 vs PM-QKD numerical ~$10^{-3}$ prefactor) | [CONJ] on upper bound candidates | gap_shape_g4_1.md §2.1 |
| **P5** | Werner reduction of MDI (raw-key statistics) | [CONJ] | mdi_werner_reduction.md v0.3 |
| **P6** | Sub-Q1 closed | ✅ | PHASE0_REPORT.md |
| **P7** | qubit Kamin Fig.1 positive-rate ±15% | partial | kamin_fig1_report.md |
| **P8** | decoy Kamin Fig.3 < 5% | **OPEN** | ADR 0001 T2-B deferred |

---

*End of Main Question Interim Status snapshot — 2026-04-22 autonomous*

---

## 11. Day 2 late-evening status additions (2026-04-22)

### 11.0 User Q1 decision — β main + γ safety net (Option 2)

**User 2026-04-22**: "我选择 beta，第二个方案"

实施状态:
- [q1_decision_record_2026-04-22.md](q1_decision_record_2026-04-22.md) 正式记录
- [umr_path_beta_derivation.md](../proofs/umr_path_beta_derivation.md) v0.3 (§6-§8 deepened scaffolding)
- [umr_path_gamma_v0_4_derivation.md](../proofs/umr_path_gamma_v0_4_derivation.md) v0.5 (§6-§7 safety-net deepening)
- [umr_path_alpha_derivation.md](../proofs/umr_path_alpha_derivation.md): **dormant** (per user decision, α 不启动 formal 工作)

### 11.0.2 β.G3 toy-model numerical exploration (v0.4 — R2 FIX after Codex R1 REJECTED)

**诚实版本** (commit pending): v0.3 曾被 over-claim为 "definitive / β 真实值"; 经 Codex R1 review REJECTED (2 CRITICAL), 现 v0.4 降级:

**三种 toy qubit variants** (all **toy abstract**, not physical MDI):

| Variant | η=0.1 ratio | 标签 |
|---|---|---|
| A. Tensor-product upstream (no LOCC) | 1.81× | valid **upper bound** on β (β ≤ 2× Pir, 不紧) |
| B. Werner **heuristic surrogate** (depol substitution) | 0 (artifact) | **heuristic only**, NOT formal β lower bound |
| C. Post-BSM toy projection (all-Bell summed) | **0.19×** | toy qubit estimate; **p_BSM scaling 与物理 MDI 不符** |

**Canonical convention (R2 fix)**: all-Bell summed (Variant C), giving plateau ≈ 0.19× across η ∈ [0.001, 0.5].

**Honest interpretation**:
- Direction: Variant C→A reduction factor ~10× 是 plausibility signal that β-via-Charlie-BSM-LOCC **可能** tighter than Pirandola
- **BUT**: p_BSM scaling 不符 physical MDI linear-optic BSM; qubit 非 bosonic CV
- β-vs-Pirandola direction **仍 agnostic** per Log 07 §4.4
- **不足以** justify fast-tracking β over γ safety net

**User decision bearing**:
- β 路径**仍 [CONJ] pending β.G1-G5 formal work** (~7-10 人日)
- γ safety net equally important; decision between β/γ 不 由 toy numerical 决定
- Desktop bosonic SDP verification **critical** for real answer

详见 [beta_G3_numerical_finding_2026-04-22.md v0.4](beta_G3_numerical_finding_2026-04-22.md)

---

### 11.0.1 β.G3 numerical early signal (cross-over finding)

**[beta_G3_numerical_finding_2026-04-22.md](beta_G3_numerical_finding_2026-04-22.md)**: tensor-product log-negativity in qubit amp-damp model:

| η_arm | LN_tensor | Pirandola | ratio |
|---|---|---|---|
| 0.9 | 1.85 | 3.32 | **0.56** (upstream tighter) |
| 0.5 | 1.17 | 1.00 | 1.17 |
| 0.1 | 0.275 | 0.152 | **1.81** (upstream looser 2×) |
| 0.01 | 0.029 | 0.015 | **1.98** (实际 QKD) |

- **Practical regime (η ≤ 0.1, 实际 QKD)**: tensor-product upstream 2× Pirandola 松 — β 要 tighter 必需 Charlie BSM LOCC 救场
- **Low-loss regime (η ≥ 0.5)**: upstream 已经 tighter, β 自然更紧
- **Direct E_R(M̃_β) SDP** 在本地 MOSEK OOM — 留给用户 desktop 环境 verify

**Cautionary signal**: 在实际 QKD regime, β 可能**不**给 tighter bound via tensor-product route; 用户 Phase 2 β.G3 direct SDP 是决策节点。建议 user Phase 1 (β.G1 + β.G4) 先做 — 对 γ fallback 也 useful。



### 11.1 T2-A Frank-Wolfe stretch empirically invalidated

- commit dc021cf: [docs/findings/t2a_thm4_empirical_finding_2026-04-22.md](t2a_thm4_empirical_finding_2026-04-22.md)
- 实测 at (n=10^10, 10 dB): Hard rate 0.0870 vs Thm 4 rate 0.0854 vs Kamin visual ~0.06
- Thm 4 vs Hard improvement: **~1.8% only**
- 40-45% offset vs Kamin **not fixable** by τ-slack or FW outer loop
- 结论: my `kamin_choi_sdp_qubit_bb84(use_thm4=True)` 直接求解 Eq. 49 (不是 affine 下界), MOSEK 能 close optimum → **FW outer loop 不提供额外改进** (per Kamin §5.2.1 end)
- Offset 源 = plot-reading uncertainty ±20-30% + (γ, α) grid granularity + λ_EC 实现差异
- **T2-A stretch 工作已实证否定启动 value** — 保持 operational closure 状态

### 11.2 M4B TF-QKD 硬验收 (log-log slope 0.5 ± 0.05) 确认通过

- Per [docs/families/tfqkd_family.md:187, 234](../families/tfqkd_family.md)
- 实测 log-log slope = **0.519** (target 0.5 ± 0.05) ✓
- Follow-up gaps (documented, 非 blocker):
  - rel=0.05 绝对值验收未达 (需 k-photon error model)
  - F6 `partial → covered` 门槛未达 (需 Fock truncation + R_A phase register)
- **M4B 主要硬验收通过**; 可视为 Phase 0.5 effectively closed

### 11.3 Autonomous plateau reached (Day 2 close)

Remaining autonomous-achievable work:
- T2-A FW outer loop: **实证否定** (§11.1)
- M4B: **slope 验收通过** (§11.2)
- 三 paths: [CONJ]/scaffolding fully closed
- Sub-Q audit integration: v0.3 snapshot 当前

**进一步升级** 的 autonomous path 全部 blocked on user action:
- 选 path α/β/γ 中哪条做 formal (Q1)
- T2-B decoy Fig.3 trigger 时机 (Q2)
- Werner reduction C2 签字 + C1 验证 (Q4)

---

## Changelog

- **v0.4** (2026-04-22 Day 2 late evening autonomous plateau):
  - §11.1 T2-A stretch 实证否定记录
  - §11.2 M4B log-log slope 确认通过记录
  - §11.3 autonomous plateau statement + 升级 path blocked on user
- **v0.3** (2026-04-22 Day 2 evening，paths cycle 完成后补充)：
  - Sub-Q3 §4 表格新增 path α/β/γ 的具体状态行（scaffolding / [CONJ]-derivation / v0.4+R3）
  - 反映 Codex 5-round paths review 的最终状态
- **v0.2** (2026-04-22 Round 2 FIX, 响应 MQ audit REJECTED verdict):
  - **CRITICAL**: 去除 v0.1 表 S4 "Gap 归因 γ (两端松) 最可能" 的 revived retracted claim — v1 FINDINGS 模式重现被 reviewer 捕获
  - MAJOR: Upgrade path 全部显式写 C1 ∧ C2 ∧ C3 三条件；user 纸笔满足 C1(b) 不替代 C2 + C3
  - MAJOR: Prefactor 数字从 "~1000×" 改为 "见 gap_shape_g4_1.md" + c_strict/c_ext 澄清
  - MAJOR: T1 PLOB scope 补 bosonic/infinite-dim 也放宽 H4/H5/H6
- **v0.1** (2026-04-22 autonomous session，commit 49486eb): 首稿 [SYN] aggregate，后被 MQ audit REJECTED
