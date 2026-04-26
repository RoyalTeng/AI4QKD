# Autonomous Research Plan — 2026-04-25 (user 离开期间)

**计划制定**：2026-04-25 session
**目标**：在 user 离开期间推进 path α [USER-APPROVED PRIORITY] 工作，**严格 [SYN]/[CONJ] 级**，**不**升级、**不**闭合 structural gap、**不**修改 formal records。
**user 返回时**：本文件 §"已完成进度"会持续更新；user 直接读本文件即可同步状态。

---

## §0 边界（**硬红线，autonomous 不可越**）

按 memory `feedback_autonomous_delegation_2026-04-21.md` + R0.1/R0.2 + 第 5/6 次 trap 教训：

### 0.1 **绝对不做**

- ❌ 任何 lemma proof / Justification sketch / closure attempt
- ❌ 任何 [SYN] → [COROLLARY] / [THM] 升级
- ❌ 修改 [FINDINGS.md](research/FINDINGS.md) / [PHASE_STATUS.md](PHASE_STATUS.md) / [RETRACTION.md](research/RETRACTION.md) 等 formal records 的结论级内容
- ❌ 提交 dev-reviewer round 3（**user 必须显式 approve 才能提交** —— 前两轮 REJECTED 的教训）
- ❌ 把 path α v0.3 的"USER-APPROVED PRIORITY but NOT C3-passed" banner 删掉或改弱

### 0.2 **可以做**

- ✅ 读 repo 内**未读** PDF + 写直读笔记
- ✅ 数值扩展（reproduce 现有 paper figures + 对比 path α scaling UB）
- ✅ 完善 [Lemma skeletons v0.1](proofs/umr_path_alpha_lemma_skeletons_v0_1.md) 的 statement-only 部分
- ✅ Cross-validate path α 引用准确性（PDF 直读核对页码 / 公式编号）
- ✅ 起草 paper draft skeleton（**严格 [SYN]/[CONJ]**，conditional 句式）
- ✅ 在 [PDF synthesis v0.1](proofs/umr_path_alpha_pdf_synthesis_v0_1.md) 增补 update sections

### 0.3 **遇到这些情况立刻 STOP，留 readback**

- 发现 path α 与 v0.2 round 1 / v0.3 round 2 同型 trap → STOP + log
- 发现新研究级 finding 需要 user judgment → STOP + log
- 任何 sub-gap 看起来 closeable → STOP + log（不闭合，留 user）
- 任何引用错误（页码 / 公式） → STOP + log
- Codex 评审 / web search 触发任何 R0.2 红线 → STOP + log

---

## §1 4 阶段计划

### Phase 1：Cross-validate path α 框架（PDF 直读，~2 sessions）

**未读 PDF in repo**（path α 相关）：
- [ ] **Lo-Curty-Qi 2012 MDI-QKD** — 5 页 — Cui 2019 引 MDI 安全模型 [6,7] 的源头之一；core MDI Eve assumption
- [ ] **TGW 2014** — squashed-entanglement upper bound — alternative converse path（cross-check 用）
- [ ] **WTB 2017** — converse bounds for private comm — Pirandola converse 工具源
- [ ] **PLOB 2017** — point-to-point bound — path α target inequality 的 building block
- [ ] **KW Ch 21+** (if exists) — 探索 KW 教科书是否有网络章节（之前只读 Ch 19/20）

**输出**（per PDF）：
- 在 [PDF synthesis v0.1](proofs/umr_path_alpha_pdf_synthesis_v0_1.md) 加 update section
- 标记每篇与 path α 11 sub-gap 的 cross-reference

**STOP 触发**：发现 path α 引用错误 / 同型 trap / 新结论。

---

### Phase 2：数值扩展（autonomous-acceptable，~1-2 sessions）

**任务清单**：
- [ ] 复现 Cui 2019 Fig. 1（infinite decoy）—— 写 `scripts/reproduce_cui_2019_fig1.py`
- [ ] 复现 Cui 2019 Fig. 2（finite decoy）—— 写 `scripts/reproduce_cui_2019_fig2.py`
- [ ] 在同一坐标轴叠加：Cui 2019 protocol rate vs path α scaling UB ($-\log_2(1-\sqrt{\eta})$) vs PLOB UB ($-\log_2(1-\eta)$)
- [ ] 输出 `docs/research/figures/path_alpha_cui_2019_comparison.png` + CSV
- [ ] 在 [Lemma skeletons v0.1](proofs/umr_path_alpha_lemma_skeletons_v0_1.md) 添加"数值佐证"小节（**严格 reframing only，不 confirm scaling tight**，per round 1 trap fix）

**严谨性约束**：
- 数值脚本 docstring 必须含 "no Lemma closure asserted, sub-gaps OPEN"
- 任何"keys per signal"数据**仅作 reframing**，不主张 path α scaling 紧
- 措辞用 "is consistent with this finite grid"（不用 "confirm" / "数值 confirm"）

**STOP 触发**：数值结果偏离 Cui 2019 published 太远 → STOP 排查。

---

### Phase 3：完善 Lemma skeletons + paper draft skeleton（~2 sessions）

**任务清单**：
- [ ] 把 Phase 1 cross-validation 发现 fold 进 [Lemma skeletons v0.1](proofs/umr_path_alpha_lemma_skeletons_v0_1.md)
- [ ] 补充 §7 user 核对点 5（Curras 2018 待补 PDF 时再做）
- [ ] 起草 `docs/proofs/umr_path_alpha_paper_draft_skeleton_v0_1.md`：
  - Strict [SYN]/[CONJ] 级，conditional 句式
  - Section structure：Intro / Anchor protocol (Cui 2019) / Path α reduction (Lemma A/B/C statement only) / Conditional bound / Numerical reframing / Open gaps
  - **不**写任何 lemma proof

**严谨性约束**：
- Paper draft skeleton 顶部 banner: "[SYN]/[DRAFT] — Lemma proofs OPEN; not for external citation; ALL claims conditional on 11 sub-gaps closure per [scaffolding v0.1]"
- 所有 main claim 用条件句式
- 引用与 Phase 1 PDF 直读核对一致

**STOP 触发**：
- 发现需要 lemma proof 才能讲清楚的 section → STOP，留作 user paper-level work
- 发现 [SYN] → [COROLLARY] 的 implicit slip → STOP 重写

---

### Phase 4：进度 log + user readback（每个 phase 末尾）

**输出**：本文件 §"已完成进度"持续 append。

**user 返回时优先读取**（按顺序）：
1. 本文件 §"已完成进度"
2. [PDF synthesis v0.1](proofs/umr_path_alpha_pdf_synthesis_v0_1.md)（最新 updates）
3. [Lemma skeletons v0.1](proofs/umr_path_alpha_lemma_skeletons_v0_1.md)（如有更新）
4. 数值产出（如有）
5. paper draft skeleton（如有）

---

## §2 已完成进度（autonomous 推进时持续更新）

### 2026-04-25 session（计划制定时）已完成

- ✅ Pirandola 2019 全 36 页直读
- ✅ KW Ch 19 + Ch 20 §20.1-§20.2 直读
- ✅ Lucamarini 2018 全 7 页直读
- ✅ Wang 2018 SNS 全 13 页直读
- ✅ Ma 2018 PM-QKD 前 8 页直读
- ✅ Cui 2019 全 9 页直读
- ✅ [PDF synthesis v0.1](proofs/umr_path_alpha_pdf_synthesis_v0_1.md) 含 v0.1 update 1/2/3
- ✅ [Lemma skeletons v0.1](proofs/umr_path_alpha_lemma_skeletons_v0_1.md) 创建
- ✅ Path α anchor protocol 选定：Cui 2019（Wang 2018 SNS 备选）

### Phase 1 进度

- ✅ Lo-Curty-Qi 2012 MDI-QKD 直读（7 页）—— 2026-04-25
- ✅ PLOB 2017 主文直读（12 页）—— 2026-04-25
- ✅ TGW 2014 直读（13 页）—— 2026-04-25
- ⏭️ WTB 2017 **skip per user**（53 页太长，path α 不 critical）—— 2026-04-26
- ✅ KW Ch 21+ 探索 — **KW 2020 止于 Ch 20**，无网络章节 —— 2026-04-26

**Phase 1 完成**。详情见 [PDF synthesis v0.1 update 4-7](proofs/umr_path_alpha_pdf_synthesis_v0_1.md)。Path α 状态不变（11 gap OPEN），Cui 2019 anchor 维持。**未发现同型 trap，未发现撤回证据**。

### Phase 2 进度

- ✅ Cui 2019 Fig. 1 复现脚本 [scripts/reproduce_cui_2019_fig1.py](../scripts/reproduce_cui_2019_fig1.py)（infinite decoy 版） —— 2026-04-26
  - 输出：[data/cui_2019_fig1_reproduction.csv](research/data/cui_2019_fig1_reproduction.csv)
  - 图：[figures/cui_2019_fig1_reproduction.png](research/figures/cui_2019_fig1_reproduction.png)
  - **数值表观**（仅 reframing，不主张 path α scaling 紧）：
    - 0-30 dB Cui rate scales like √η
    - 30 dB+ Cui rate **超越 PLOB UB**（TF-QKD 设计目标）
    - Path α scaling UB 始终在 Cui rate 上方约 **30× prefactor**
- [ ] Cui 2019 Fig. 2 复现脚本（finite decoy 版）—— 暂缓，infinite decoy 已足够 reframing
- ✅ path α scaling UB 叠加对比图 —— 已含在 Fig. 1 复现中

### Phase 3 进度

- [ ] Lemma skeletons v0.2（fold Phase 1 findings）—— 暂缓，v0.1 已含 Phase 1 主要 findings 的 8 个 user 直读核对点；v0.2 fold 等 user review v0.1 后再做
- ✅ Paper draft skeleton v0.1 [umr_path_alpha_paper_draft_skeleton_v0_1.md](proofs/umr_path_alpha_paper_draft_skeleton_v0_1.md) —— 2026-04-26
  - 严格 [SYN]/[DRAFT] level，conditional 句式
  - 数值表格（Phase 2 reproduction 结果）含在 §4
  - 11 sub-gaps 维持 OPEN
  - **不可作对外引用** until R0.2 三闸门完成

### Phase 4 readback 摘要 (2026-04-26 autonomous 完成)

**Phase 1-3 总结**（user 离开期间 ~3 hours wallclock 工作）：

**Phase 1（PDF cross-validation）**：
- ✅ 已读 9 篇 PDF 共约 110 页（Pirandola 2019, KW Ch 19/20, Lucamarini 2018, Wang 2018, Ma 2018, Cui 2019, LCQ 2012, PLOB 2017, TGW 2014）
- ⏭️ Skip WTB 2017（per user 决定）
- ✅ 确认 KW 教科书止于 Ch 20，无网络章节
- **结论**：path α anchor (Cui 2019) + target inequality (Pirandola 2019 N=1 chain) + 数学语言 (Pirandola SI Note 1 + KW Ch 20 + Cui Eq.1) 框架完整
- **无同型 trap，无撤回证据**

**Phase 2（数值复现）**：
- ✅ Cui 2019 Fig. 1 (infinite decoy) 复现完成
- 数值表观与 Cui 论文一致（Cui rate 在 30 dB+ 超越 PLOB；与 path α scaling UB 比 ratio ~30× constant prefactor）
- **此为 finite-grid reframing**，**不**主张 path α scaling 紧

**Phase 3（paper draft skeleton）**：
- ✅ Paper draft skeleton v0.1 完成
- 9 sections，约 250 lines，全部 [SYN]/[DRAFT] level
- 核心结构：Intro / Anchor (Cui 2019) / Reduction architecture (Lemma A/B/C statement only) / Numerical reframing / Open sub-gaps / Verification path / Limitations / Conclusion
- **未做任何 lemma proof**，**未** close 任何 sub-gap

**整体严谨性账目**：
- ✅ All 11 sub-gaps **维持 [UNKNOWN]**
- ✅ 无 [SYN] → [COROLLARY] / [THM] 升级
- ✅ formal records (FINDINGS / PHASE_STATUS / RETRACTION) **未修改**
- ✅ Path α v0.3 [USER-APPROVED PRIORITY but NOT C3-passed] banner **未删**
- ✅ 未提交 dev-reviewer round 3
- ✅ 未触发任何 §3 STOP condition

**user 返回时建议的最优 action**（按本计划 §5 优先级，已不变）：
1. 读本文件 §2 已完成进度（5 分钟）
2. 决定 path α 下一步：
   - **(A) 启动 paper-level work**：按 [Lemma skeletons v0.1 §7 8 个核对点](proofs/umr_path_alpha_lemma_skeletons_v0_1.md) 直读 PDF，3-4 天 user 时间
   - **(B) approve dev-reviewer round 3**：基于 v0.3 已 cleanup + paper draft skeleton v0.1 + Lemma skeletons v0.1 一并提交
   - **(C) pivot 到其他方向**（β.G4 / γ / etc.）
   - **(D) 暂停 path α**

**autonomous 留下的所有产物清单**（user 返回时按需 review）：
- [docs/proofs/umr_path_alpha_pdf_synthesis_v0_1.md](proofs/umr_path_alpha_pdf_synthesis_v0_1.md) — PDF 直读笔记 + cross-validation（含 v0.1 update 1-7）
- [docs/proofs/umr_path_alpha_lemma_skeletons_v0_1.md](proofs/umr_path_alpha_lemma_skeletons_v0_1.md) — 三 lemma statement-only 形式化骨架
- [docs/proofs/umr_path_alpha_paper_draft_skeleton_v0_1.md](proofs/umr_path_alpha_paper_draft_skeleton_v0_1.md) — paper draft 结构提案
- [scripts/reproduce_cui_2019_fig1.py](../scripts/reproduce_cui_2019_fig1.py) + 输出（CSV + PNG + PDF）— 数值 reframing
- 本文件（autonomous plan 进度更新）

---

## §3 出现以下情况 autonomous **必须 STOP** 等 user

| 触发条件 | Action |
|---|---|
| Path α 与已撤回 v1/γ.v0.2/γ.v0.6/AD-channel/v0.2 同型 trap | STOP + log + flag for retraction discussion |
| 发现新 sub-gap 不在 11 个 inventory 中 | STOP + log + 不擅自加 |
| 发现 path α 应被撤回的硬证据 | STOP + log + 不主动撤但等 user 判定 |
| 数值结果显著偏离 published values | STOP + log + 不调参强行匹配 |
| Codex 评审需要 / 触发 R0.2 红线 | STOP + log |
| 任何 lemma 看起来 closeable | STOP + log + 不闭合 |

---

## §4 Estimated total work

按 4 phases：
- Phase 1: ~2 sessions（5-6 PDFs 直读）
- Phase 2: ~1-2 sessions（数值脚本 + figure）
- Phase 3: ~2 sessions（lemma skeletons + paper draft）
- Phase 4: 持续 log

**总：~5-7 sessions** wallclock，**严格 [SYN]/[CONJ] 级输出**。

任何超出 §0.2 边界的工作或触发 §3 STOP 条件，留 user readback 等回归。

---

## §5 user 返回后建议的最优 action

按本计划执行结果，user 返回后建议（按优先级）：

1. **读本文件 §2 已完成进度**（5 分钟）
2. **决定 path α 下一步**：
   - (A) 启动 paper-level work（按 [Lemma skeletons §7 8 个核对点](proofs/umr_path_alpha_lemma_skeletons_v0_1.md#§7) 直读）
   - (B) approve dev-reviewer round 3（基于 Phase 3 polished 版本）
   - (C) pivot 到其他方向（β.G4 / γ / etc.）
   - (D) 暂停 path α
3. **如果选 (A)**：用 §7 核对点开始读 PDF；预计 3-4 天 user 时间
4. **如果选 (B)**：autonomous 提交 dev-reviewer round 3；如果再 REJECTED → §7.3 rollback 触发（per v0.3 §7.3 operationalized triggers）

---

## §6 Changelog

- **v0.1** (2026-04-25)：首版自主研究计划。autonomous 边界严格按 R0.1/R0.2 + 第 5/6 次 trap memory + §7.3 operationalized rollback triggers。

---

*END OF PLAN.* 11 sub-gaps OPEN. R0.1/R0.2/R0.3 严格维持. Autonomous pipeline cap [SYN]/[CONJ]. user-directive 2026-04-25 priority 维持. 任何升级仍需 R0.2 三闸门.
