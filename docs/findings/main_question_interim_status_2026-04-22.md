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
| Pirandola 2019 适用性 (untrusted relay) | **[CONJ]** — Log 07 path α / β / γ 三路径都未形式化；v1 FINDINGS + v0.2 path γ 都已 retract |

**硬结论**：

- **[COROLLARY of PLOB 2017]** 对点对点纯损 bosonic channel：$R \leq -\log_2(1-\eta)$；high-loss asymptote $\approx 1.44·\eta$
- **[COROLLARY of TGW 2014]** 对点对点纯损 bosonic channel：$R \leq \log_2\frac{1+\eta}{1-\eta}$；PLOB 紧 2×
- **[COROLLARY of Pirandola 2019 Eq.11 for trusted relay]** 单路径 trusted-relay：$R \leq -\log_2(1-\sqrt\eta)$；但**未** certify 到 umr (Log 07 Step C 失效)
- **[CONJ]** umr 上界 $R \leq 1.44·\sqrt{\eta_{AB}}$ — 依赖 untrusted-relay capacity monotonicity；**未**升级到 [COROLLARY]；v0.2 adversarial containment shortcut 已撤回

**Sub-Q3 明确结论**（autonomous 级）：

> umr 拓扑的 scaling upper bound **最可能为** $\sqrt{\eta_{AB}}$（per literature synthesis），**但** 严格 converse 继承仍为 **[CONJ]**。Log 07 path α (monotonicity + 三 lemma) / β (channel-reduction) / γ (single-edge PLOB + data-processing 真版) 三条路径任一由**用户** 形式化可升级。

---

## 5. Sub-Q4 状态（Gap 刻画 + 归因 A/B/C）

**结论**：**gap shape 完成 [CONJ]；归因 G4.2 blocked on Sub-Q3 upper bound 升级**

| 验收项 | 状态 |
|---|---|
| G4.1 Gap 定量形状 | [CONJ] ([gap_shape_g4_1.md](gap_shape_g4_1.md)) |
| G4.2 Gap 归因 A/B/C | **blocked** — 触发条件 (Log 07 path γ 形式化 + 上界 [COROLLARY] 升级) 未满足 |

**硬结论**：

- **[CONJ for umr]** 在对称 bosonic-asym 下 gap = $1.1 \cdot \sqrt{\eta}$（3 candidate upper bound 去掉 1.44 vs TF 下界 0.3）；常数因子 ~1000× (但都属 [CONJ] 上界候选)
- **[UNKNOWN]** 归因是 α (上界松) / β (下界松) / γ (两端松)

**Sub-Q4 明确结论**（autonomous 级）：

> gap 的**形状**已刻画（log-log plot slope -1 vs -1/2）；**归因**待 Sub-Q3 upper bound 升级后启动；**当前**只能说 "在放宽假设下 gap ≈ 1.1·√η，具体归因待 user+C1+C2 升级 upper bound"。

---

## 6. 主问题答案清单（可 cite 格式）

### 6.1 Definitive (at [THM] / [COROLLARY] 级别，可对外 cite with caveats)

| # | 陈述 | 分级 | Scope |
|---|---|---|---|
| T1 | Point-to-point pure-loss bosonic channel 两方 $R \leq -\log_2(1-\eta)$ | [COROLLARY of PLOB 2017] | 原始 H1-H6 不含 untrusted relay |
| T2 | TF-QKD (Lucamarini 2018) 在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下可达 $\sqrt{\eta_{AB}}$ | [THM] | 放宽 H4/H5/H6 |
| T3 | qubit BB84 阈值 11.00%, 六态 12.62% | [THM] | N/A for main Q |

### 6.2 [SYN] / [CONJ] (内部可用，对外禁止单独 cite)

| # | 陈述 | 分级 | Blocker to upgrade |
|---|---|---|---|
| S1 | umr scaling 最可能为 $\sqrt{\eta_{AB}}$ (放宽版) | [SYN] | 严格 converse 继承需 Log 07 path α/β/γ 形式化 |
| S2 | umr 上界 $\lesssim 1.44·\sqrt{\eta_{AB}}$ | [CONJ] | 同上 |
| S3 | 情况 A 成立 (放宽版) | [SYN] | 依赖 S2 |
| S4 | Gap 归因 γ (两端松) 最可能 | [CONJ] | G4.2 blocked |

### 6.3 [UNKNOWN]

| # | 问题 | 升级路径 |
|---|---|---|
| U1 | 严格 H1-H6 版本主问题答案 | 需 H4 (Fock 截断) + H5 (Portmann-Renner composable finite-key) + H6 (严格 DV) 扩展工作 — 属 Phase 2-3 |
| U2 | Sub-Q4 归因 A/B/C 定量 | 需 Sub-Q3 upper bound 升至 [COROLLARY]，需 user C1 + C2 |
| U3 | TF-QKD 族外是否存在填 gap 的新协议 | Phase 3 Sub-Q4 归因 B 子任务 (如触发) |

---

## 7. R0.2 C1 + C2 + C3 Upgrade 路径（等用户归来）

**升级到 [COROLLARY]/[THM] 的硬 invariant**（[CLAUDE.md R0.2](../../CLAUDE.md) + [research-rigor.md R2.2](../../.claude/rules/research-rigor.md)）：

| 升级目标 | C1 (独立验证) | C2 (用户签字) | C3 (dev-reviewer) | 优先级 |
|---|---|---|---|---|
| umr 上界 → [COROLLARY] | (a) 跨家族 AI + 读 Pirandola 2019 PDF; OR (b) 人类纸笔 path α/β/γ 明写; OR (c) 非 AI 工具 (Mathematica symbolic) | 必须 | path γ v0.2 已 REJECTED；path γ v0.3 工作 stall | **最高** (解锁 Sub-Q4 G4.2) |
| Werner reduction → [COROLLARY] | (a) 跨家族 AI + 读 Lo-Curty-Qi + BDCZ 1998 PDF; OR (b) 人类纸笔; OR (c) Mathematica | 必须 | R3 Agent 2 PASS ✓, Agent 1 FAIL (downstream only) | **中** (内部工具链论证) |
| Sub-Q4 G4.2 归因 | 依赖 umr 上界升级 | 必须 | blocked | blocked |

---

## 8. 本 snapshot 的限制

1. **仅 aggregation**，**不**引入新 rigor 陈述
2. 数字 (e.g., "差 1000×") 是 [CONJ] 级来源于 gap_shape_g4_1.md
3. 不改 FINDINGS v2 / Log 07 / PHASE0_REPORT 任何分级
4. [SYN] 级聚合判断本身**不**可对外单独 cite；需 user sign-off 转 [COROLLARY]

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
| **P3** | $R_\text{lower} \geq 0.3 \cdot \sqrt{\eta_{AB}}$ via TF-QKD | [THM] | Lucamarini 2018 via FINDINGS v2 |
| **P4** | Gap scaling = √η; 常数差 ~1000× | [CONJ] | gap_shape_g4_1.md |
| **P5** | Werner reduction of MDI (raw-key statistics) | [CONJ] | mdi_werner_reduction.md v0.3 |
| **P6** | Sub-Q1 closed | ✅ | PHASE0_REPORT.md |
| **P7** | qubit Kamin Fig.1 positive-rate ±15% | partial | kamin_fig1_report.md |
| **P8** | decoy Kamin Fig.3 < 5% | **OPEN** | ADR 0001 T2-B deferred |

---

*End of Main Question Interim Status snapshot — 2026-04-22 autonomous*
