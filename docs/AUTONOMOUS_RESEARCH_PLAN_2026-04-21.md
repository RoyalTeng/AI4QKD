# 自主研究计划 — 2026-04-21 长时段 session（RESEARCH_PLAN v1.0 对齐版）

**计划日期**：2026-04-21（session end）
**预估时长**：不确定（用户长时间离开）
**权威上位文档**：[RESEARCH_PLAN.md v1.0](RESEARCH_PLAN.md) / [CLAUDE.md v1.0](../CLAUDE.md) / [PROSPECTUS.md v3.1](PROSPECTUS.md)

**定位**：本文档**不创建新动作编号**，仅把用户 2026-04-21 签字的 3 项决策（1b / 2a / 3b）映射到 RESEARCH_PLAN 既定动作序列，并在 RESEARCH_PLAN §1.2（验收）+ §7（deliverable 模板）+ §9（诚信红线）+ CLAUDE.md R0.1-R0.3（分级 + C1 ∧ C2 ∧ C3）三重约束下给出可自主推进的任务清单。

---

## 0. 用户本 session 已签字事项（2026-04-21 session end）

| 审阅项 | 决策 | 映射到 RESEARCH_PLAN 动作 |
|---|---|---|
| 1 (Werner form 形式化) | **(b) 启动 Lo-Curty-Qi 2012 §II 精读** | §2.2 **R2.1** Level 3 → Level 4 升级 |
| 2 (qubit Kamin ±6 dB) | **(a) 接受 Frank-Wolfe vs 单次 SDP 差异** | §3.3 **S2.5** Limitations 节正式记录 |
| 3 (Kamin Fig.3 3× offset) | **(b) 精确复现 < 5% tolerance** | §3.3 **S2.5** 硬验收"与 Kamin 2025 Fig.4/Table 1 误差 < 5%" 复审 |

---

## 1. 任务清单（RESEARCH_PLAN 动作编号）

### T1 ≡ R2.1 Level 3 → Level 4 升级（Lo-Curty-Qi 2012 Werner reduction）

**原 RESEARCH_PLAN §2.2 R2.1 验收**："能独立写出 MDI-QKD 的 MS-EB 五元组，特别是 $\mathcal{E}$ 含 Charlie 的 Bell 测量" — 已闭合（Level 3）

**用户 1b 触发的新验收**（Level 4，R2.1 延伸）：

> "能独立推导：ideal symmetric MDI（η_A = η_B, no misalignment, no decoy）下，BSM 成功后 conditional Alice-Bob state 化简到 Werner form，且 Werner QBER 与 qubit BB84 Z/X-basis QBER 有 explicit map。"

**阻碍**：Lo-Curty-Qi 2012 (arXiv:1109.1473, PRL 108 130503) **PDF 不在** `docs/literature/pdfs/`（已确认）。[ZOTERO_REFERENCES §4](research/ZOTERO_REFERENCES.md) 清单也未覆盖。

**可自主子步骤**：

| Step | 动作 | 验收（RESEARCH_PLAN §7.1 + §9）|
|---|---|---|
| T1.1 | `mcp__zotero__zotero_add_by_url` 加 arXiv:1109.1473（只加不读，按 2026-04-19 plan 模式） | Zotero item_key 回传，附 PDF |
| T1.2 | PDF §II + 附录精读，对照 [docs/literature/MDI-QKD.md §3.1-3.2](literature/MDI-QKD.md) 校验 | 精读笔记更新至 v0.2 Level 4；每定理引用带 Theorem N / Eq.(M) / 页码（RESEARCH_PLAN §9 红线） |
| T1.3 | 起草 `docs/proofs/mdi_werner_reduction.md` v0.1 **[CONJ]** | 按 §7.1 模板 + §9 定理追溯硬红线：Lemma W1-W4 每步引用 Lo-Curty-Qi Theorem/Eq 或明示 "本项目独立推导 [CONJ]" |
| T1.4 | dev-reviewer 双 Codex QA（C3 闸门） | 工作流位置 `docs/workflow/werner-reduction/`；FAIL 立即撤回 |
| T1.5 | **停留在 [CONJ]**，等用户 C1 (跨家族直读 PDF 或人类) + C2 (签字) | **不自主升级**（R0.2 invariant） |

**交付**：
- `docs/proofs/mdi_werner_reduction.md` v0.1 **[CONJ]**
- `docs/literature/MDI-QKD.md` v0.2（Level 4 升级）
- `docs/workflow/werner-reduction/` workflow 产物
- 若 T1.5 未能获用户签字 → **停留在 [CONJ]**，不入 FINDINGS

**时间估计**：2-4 天

**风险**：
- Lo-Curty-Qi 原文可能只给 verbal argument 无 explicit Werner form 计算 → 明示 "[CONJ] 本项目独立推导"，不越权说 "引用 Lo-Curty-Qi"
- Non-ideal scenario (asymmetric / misalignment / decoy)下 Werner form 可能 break → 明写 scope

---

### T2 ≡ S2.5 硬验收复审（Kamin Fig.3 < 5% finite-key 精度）

**[2026-04-22 update per ADR 0001 Accepted]**：T2 **split** to:
- **T2-A**：Kamin qubit BB84 **Fig.1** < 5%（proxy milestone，autonomous session 可执行，1-2 周估计）
- **T2-B**：Kamin decoy BB84 **Fig.3** < 5%（defer 至 Phase 2 Sub-Q3 comparison work）

**重要**：T2-A 不 close 原 S2.5 硬验收，也不 close 用户 3b 签字。二者 **继续 open**，直到 T2-B 完成。见 [docs/adr/0001-kamin-fig3-tolerance-split.md](adr/0001-kamin-fig3-tolerance-split.md)。

**RESEARCH_PLAN §3.3 S2.5 硬验收**（unchanged，继续 open）：

> "对 decoy-state BB84，有限密钥率（给定 n, ε_sec, ε_corr）与 Kamin 2025 Fig. 4 / Table 1 误差 < 5%"

**当前状态**（基于 session 内诊断）：
- Asymptotic R at γ=0.1：我 0.242 vs Kamin ~0.28 → **差 20%**（高于 5% 硬阈值）
- n=10^12 finite-key：我给值比 Kamin 小 **3×**
- 嫌疑来源：λ_EC 估计公式 / γ 优化算法 / EC overhead 常数

**可自主子步骤**：

| Step | 动作 | 验收 |
|---|---|---|
| T2.1 | 精读 [Kamin 2025 §§5-6](literature/pdfs/Kamin-2025-FiniteSizeAnalysisEntropyAccumulation.pdf) finite-key 推导 + Fig.3 reproduction | 识别 λ_EC 公式、γ 优化路径、EC overhead 常数三处 diff |
| T2.2 | 逐项对照我的 [qkdx/numerics/kamin_sdp_decoy.py](../qkdx/numerics/) 与论文 §§5-6 | diff 报告 `docs/workflow/kamin-fig3-repro/diff_report.md` |
| T2.3 | **TDD**：先写 `tests/test_numerics/test_kamin_fig3_within_5pct.py` (xfail)，再改代码 | 测试打印真实数据值（RESEARCH_PLAN §2.1 test 规范） |
| T2.4 | 逐项 fix；每次 fix 记录对 offset 的贡献（CSV） | `docs/findings/data/kamin_fig3_debug_trajectory.csv` |
| T2.5 | dev-reviewer 评审 numerics diff | 工作流位置 `docs/workflow/kamin-fig3-repro/` |
| T2.6 | **若 < 5%**：更新 [kamin_fig1_report.md](findings/kamin_fig1_report.md) + S2.5 硬验收 mark closed | 验收证据按 §7.3 模板（代码 commit SHA + seed + 复现命令） |
| T2.6' | **若仍 > 5%**：写 diagnostic report，明示剩余 offset 来源，**标 [CONJ]**，等用户决定是否升级 S2.5 接受阈值（需 ADR） | `docs/findings/kamin_fig3_gap_diagnostic.md` **[CONJ]** |

**交付**：
- 修订 `qkdx/numerics/kamin_sdp_decoy.py`（加法式修改，避免破坏现有 BB84 回归）
- 新增 tests
- 成功 → `docs/findings/kamin_fig3_reproduction.md` v0.1 **[CONJ]** 或达 5%后 **[SYN]**；失败 → `_gap_diagnostic.md` **[CONJ]**
- 若需放宽 5% → 启动 `docs/adr/0001-kamin-fig3-tolerance.md`

**时间估计**：3-5 天

**风险**：
- Kamin §§5-6 若只给 verbal description 无 explicit formula level → < 5% 无法达到；走 T2.6' 路径
- 修改 `kamin_sdp_decoy.py` 可能 regression 现有测试 → TDD 保护
- Finite-key 调优可能是长期工程，Week 2 unmatched

---

### T3 ≡ S2.5 Limitations 节记录（2a 决策归档）

**对应 RESEARCH_PLAN §3.3 S2.5**：qubit Kamin ±6 dB 残余用户已签字接受。

**可自主子步骤**：

| Step | 动作 | 验收 |
|---|---|---|
| T3.1 | 更新 [docs/findings/kamin_fig1_report.md](findings/kamin_fig1_report.md) §Limitations：明写 "2026-04-21 用户签字：接受 ±6 dB cutoff offset 为 Kamin 专有 Frank-Wolfe 全 DoF g 迭代 vs 本项目单次 SDP 的内在差异；不启动 Frank-Wolfe 实现" | time-stamped 条目，commit message 引用用户 sign-off |

**交付**：单 commit，约 10 分钟

**时间估计**：最短，可最先做

---

### T4 ≡ U3.1-U3.5 Phase 2 literature stack（opportunistic 推进）

**RESEARCH_PLAN §4.1-§4.2 既定**：Phase 2 上界精读 stack，用户 2026-04-19 已把 Pirandola 2019 / WTB 2017 / TGW 2014 / Khatri-Wilde 2020 加入 Zotero（commit 未记录，但 [ZOTERO_REFERENCES §4](research/ZOTERO_REFERENCES.md) 的 add-only plan 已执行）。

**状态**：
- WTB 2017: [docs/literature/WTB-2017.md](literature/WTB-2017.md) v0.1 Level 3 存在（Thm 12/19 已修正）
- Pirandola 2019: [docs/research/07_pirandola_2019_technical_audit.md](research/07_pirandola_2019_technical_audit.md) Level 3 audit 存在（用户主笔）
- TGW 2014: **无 memo**（PDF 在 `docs/literature/pdfs/TGW-2014-FundamentalRateLoss.pdf`）
- Khatri-Wilde 2020: [docs/literature/KhatriWilde-2020.md](literature/KhatriWilde-2020.md) 存在，完整度未查

**可自主子步骤**（每篇独立，需要时 parallel）：

| Step | 动作 | 产出 | 时间 |
|---|---|---|---|
| T4.1 | TGW 2014 Level 3 精读（§7.1 模板） | `docs/literature/TGW-2014.md` v0.1 **[DRAFT]** | 0.5-1 天 |
| T4.2 | Pirandola 2019 Level 4 升级（§4.1.2 U3.2 PLOB 类型 Level 4 要求） | `docs/literature/Pirandola-2019.md` v0.2 | 0.5-1 天 |
| T4.3 | WTB 2017 Level 3 → Level 4 升级 | `docs/literature/WTB-2017.md` v0.2 | 0.5-1 天 |
| T4.4 | Khatri-Wilde §19-20 (monotonicity) 子章节 Level 4 | 更新 `docs/literature/KhatriWilde-2020.md` | 0.5 天 |

**guardrail**：每份 memo 起草**不**改 FINDINGS v2 分级标签；所有引用 Theorem / Eq. / 页码精确，否则标 `[RECALLED]`（RESEARCH_PLAN §9 红线）

**交付**：4 份 literature memo 升级

**时间估计**：2-3 天（机会主义推进，不阻塞 T1 / T2）

---

### T5 ≡ U3.6 / path α / β / γ formal development【**dormant，不自主启动**】

**RESEARCH_PLAN §4.3 U3.6**：上界 MS-EB 重写，需 U3.1-U3.5 全部完成。

**状态**：path γ v0.2 已 retract；path α / β / γ 真版需**用户显式指示**启动。

**本 session 不做**：T5 等用户回来决定是否 trigger。

---

## 2. Autonomous session guardrails（硬红线）

### G1 — 分级守则（CLAUDE.md R0.1-R0.3）

- 所有新起草文档 default **[CONJ]** / **[DRAFT]**
- **不得**把任何现有 [CONJ] / [SYN] 升到 [COROLLARY] / [THM]
- **不得**在对外格式（摘要 / README / FINDINGS / PHASE0-3 report）中引用任何 [CONJ] 作为结论
- 任何"看起来像 COROLLARY" 的推导 → 写成 `[CONJ conditional on X+Y+...]`
- 升级路径**只有** R0.2 C1 ∧ C2 ∧ C3；AI **不得**自主启动

### G2 — dev-reviewer QA（R0.2 C3 必要）

- 任何 `docs/proofs/*.md` / `docs/findings/*.md` / `docs/literature/*.md` v0.1+ 起草**必须**走 dev-reviewer 工作流
- 工作流位置：`docs/workflow/{feature-name}/`
- Round 1 REJECTED 或连续 3 轮 FAIL 同一 issue → **立即撤回**并等用户
- dev-reviewer PASS **单独不满足** C1；仍需用户签字 + 独立 PDF 验证

### G3 — session logging

- 每 **非 trivial** commit 必须在 `docs/AUTONOMOUS_SESSION_2026-04-21_LOG_v2.md` 留行：`[YYYY-MM-DD HH:MM] [commit sha] [T编号] [rigor level] [scope tag]`
- 若发现自己即将做 "计划外降级" 或 "绕过 R0.2" → 立即 stop + 写 retraction + 等用户

### G4 — TDD（RESEARCH_PLAN §1.2 + CLAUDE.md §2.1）

- 所有 `qkdx/numerics/*.py` 修改前先写 test（xfail 可接受）
- 测试打印真实数据值
- 覆盖 normal + edge + error path
- 数值精度按 RESEARCH_PLAN §1.2 双轨：MOSEK `rel=0.01, abs=5e-4` / CLARABEL fallback `rel=0.02, abs=1e-3`

### G5 — commit 纪律

- 独立 commit per logical unit
- Commit message 明写 rigor grade + user-signoff status（或 "no user signoff yet"）
- **不**自动 commit 理论级升级
- **不**做 destructive git operations

### G6 — ADR 制度（RESEARCH_PLAN §8.3）

- 任何偏离 RESEARCH_PLAN 或 PROSPECTUS 的决策 → `docs/adr/NNNN-<slug>.md`
- 首个 ADR 编号 0001
- 如 T2.6' 需要放宽 S2.5 的 5% 阈值 → ADR 0001

### G7 — 文献精读诚信（RESEARCH_PLAN §9 红线）

- 每次引用 Theorem / Eq / 页码**必须**对 PDF 核对；凭记忆写的标 `[RECALLED]`
- WTB Thm 26→12, Thm 47→19 案例已先例，**不重蹈**
- 拓扑前提 / 信任假设 / 协议自由度四项核对（RESEARCH_PLAN §1.2b）**必做**

### G8 — 诱惑清单（当内心浮现任一下列想法时 → 立即停手）

- "简化论证绕过已识别 gap" → path γ v0.2 陷阱
- "文献未明示反对 = 文献支持" → v1 retraction 陷阱
- "dev-reviewer PASS + 我很有信心 = 可升级" → 越权 C1 ∧ C2 陷阱
- "用户会同意的，先做再说" → R0.2 authority chain 违反

---

## 3. 执行顺序建议（周度节律对齐 RESEARCH_PLAN §8.1）

**Day 0（即刻，最短）**：
- **T3** S2.5 Limitations 记录（10 min，单 commit）

**Week 1（Days 1-5）**：
- **T1.1** + **T1.2** Zotero add + Lo-Curty-Qi PDF 精读（Day 1-2）
- **T1.3** Werner reduction v0.1 起草（Day 3-4）
- **T1.4** dev-reviewer（Day 5）

**Week 2（Days 6-10）**：
- **T2.1** + **T2.2** Kamin §§5-6 精读 + diff 报告（Day 6-7）
- **T2.3** TDD test 起草（xfail）（Day 8）
- **T2.4** fix 循环（Day 9-10）

**Week 3（Days 11-15）**：
- **T2.5** + **T2.6** / **T2.6'** Kamin 验收（Day 11-12）
- **T4** opportunistic 推进，顺序 T4.1（TGW 无 memo 最优先）→ T4.2 → T4.3 → T4.4（Day 13-15）

**Checkpoint 每周五**：写 `conversations/weekly/2026-W17.md`（或当周编号）周报，含：完成项、阻塞、测试状态、文献进度（RESEARCH_PLAN §1.4）

**若超预估 2×**：停手 + 写 status update 到 session log；**不扩展任务**

---

## 4. 明确不会做的事（防止越权）

1. ❌ 不升级任何 [CONJ] 到 [COROLLARY]（即使 dev-reviewer PASS + 自觉 plausible）
2. ❌ 不起草任何 "对外 / 展示 / 汇报" 格式文档（摘要 / PPT / README 新章节 / PHASE?_REPORT 定稿更新）
3. ❌ 不擅自启动 T5（path α / β / γ 真版 formal development）
4. ❌ 不触 Phase 0 M1 rsync / 数据迁移
5. ❌ 不合并或重命名项目结构
6. ❌ 不 force push / 不 rebase 已 push commits
7. ❌ 不跳过 RESEARCH_PLAN §1.2b 的定理拓扑适用性核对（四项）
8. ❌ 不引入 AI 搜索协议（RESEARCH_PLAN §8.4 R4：只在 Sub-Q4 归因 B 时启动；目前不适用）

---

## 5. Fallback 与异常处理

| 情形 | 动作 |
|---|---|
| PDF 不可得（T1 Lo-Curty-Qi Zotero add 失败） | 改 arXiv 网页 abstract 精读 + scope 标 `[spec_only]`，T1 降级为 scope documentation |
| dev-reviewer 连续 3 轮 FAIL 同一 issue | 停手，写 deadlock report，等用户 |
| TDD 测试 regression | 回滚到 green，诊断，写 fix；> 1 天无法闭合 → 停手 |
| 发现 FINDINGS v2 / Log 07 / RESEARCH_PLAN 有错 | **不**擅自改；起草 `docs/pending_user_review/*.md` 放那等用户，commit 不 push |
| T2 < 5% 需要放宽阈值 | 走 ADR 0001 路径，**不**自主放宽 |
| 总时长远超 Week 3 | 不扩展新任务，收敛 + 写最终 session report + 等用户 |
| 不确定某步是否越权 | **默认保守**：按 [CONJ] 处理，写 note to user，等确认 |

---

## 6. 用户回来后审阅清单

| # | 审阅对象 | 期望 rigor grade | 期望行为 |
|---|---|---|---|
| 1 | `docs/proofs/mdi_werner_reduction.md` v0.1 | **[CONJ]** 或 **[DRAFT]** | 无 [COROLLARY] 越权；Lemma 引用带源 |
| 2 | `docs/literature/MDI-QKD.md` v0.2 | Level 4 标注 | 每定理引用精确 |
| 3 | `docs/findings/kamin_fig3_reproduction.md` / `_gap_diagnostic.md` | **[CONJ]** / **[SYN]** | 所有数字带 commit SHA + seed |
| 4 | `qkdx/numerics/kamin_sdp_decoy.py` diff | TDD tests 通过 | 无 BB84 baseline 回归 |
| 5 | `docs/workflow/werner-reduction/` + `kamin-fig3-repro/` | 完整 review trail | 所有 FAIL 已 ACT on |
| 6 | `docs/adr/0001-*.md`（若触发） | Proposed | 用户 Accept / Reject / Supersede |
| 7 | 本 plan 的 Changelog + session log | time-stamped | 任何偏离 plan 的决策有 ADR 或 note |

---

## 7. 与 RESEARCH_PLAN 的 traceability

| 本 plan T 编号 | RESEARCH_PLAN 动作 | Sub-Q | Phase |
|---|---|---|---|
| T1 (Werner reduction) | §2.2 R2.1（Level 4 升级） | Sub-Q1 | Phase 0 M2 延伸 |
| T2 (Kamin Fig.3) | §3.3 S2.5 硬验收复审 | Sub-Q2 | Phase 1 S2 |
| T3 (2a 记录) | §3.3 S2.5 Limitations | Sub-Q2 | Phase 1 S2 |
| T4 (literature stack) | §4.1-§4.2 U3.1-U3.5 | Sub-Q3 | Phase 2 |
| T5 (path α/β/γ) | §4.3 U3.6（**dormant**） | Sub-Q3 | Phase 2 Week 11-14 |

---

## 8. Changelog

- **v1.1**（2026-04-21 evening，对齐 RESEARCH_PLAN v1.0 后修订）：去除独立动作编号，全部映射到 RESEARCH_PLAN R/S/U/G；加 §7 traceability 表；明示 ADR 触发点 (T2.6')；T4 顺序调整（TGW 最优先）；G7 新增（文献精读诚信）；G8 新增（诱惑清单）
- **v1.0**（2026-04-21，初稿）：首稿，独立动作编号（已弃用）
