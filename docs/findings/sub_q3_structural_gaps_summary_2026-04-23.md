# Sub-Q3 structural gaps — AI autonomous attempts summary (2026-04-23)

**版本**: v0.1 [CONJ-DRAFT, research status aggregation]
**日期**: 2026-04-23 autonomous session
**目的**: 把 β.G4 + β.G5 + γ.B.G1 + γ.G3 四个 AI autonomous structural derivation attempts 的**失败 pattern** 结构化, 给用户**研究方向决策参考**

---

## 0. 严谨性

- 本 memo 仅 **aggregate** prior structural derivation attempts 的结论
- 无 structural gap claimed as closed
- 所有 chain inequalities 保持 [CONJ-DRAFT]
- 用于 user **research direction decision support**, 非 proof replacement

---

## 1. 4 次 structural derivation attempts 对照表

| Gap | Draft file | Codex verdict | Approaches tried | Key obstacle |
|---|---|---|---|---|
| **β.G4** (Eve model transfer) | [umr_path_beta_G4_derivation_attempt.md](../proofs/umr_path_beta_G4_derivation_attempt.md) | R1 FAIL → R2 **PASS** | §2.3 simulation, §2.5 LOPC+gift heuristic | Simulation map LOPC Eve ← umr Eve 需 forced broadcast; 无 general construction |
| **β.G5** (adversarial comb reduction) | [umr_path_beta_G5_derivation_attempt.md](../proofs/umr_path_beta_G5_derivation_attempt.md) | R1 review pending | A Prop 19.2, B Teleportation stretching, C GEAT, D Purify Eve | All four approaches 各自 fail; GEAT 最 promising 但需 user PDF check |
| **γ.B.G1** (DPI target lemma) | [umr_path_gamma_B_G1_derivation_attempt.md](../proofs/umr_path_gamma_B_G1_derivation_attempt.md) | R1 FAIL → R2 FAIL → R3 **PASS** | A Prop 19.2 circular, B Horodecki+CMI, C squashed, D broadcast classical side | Approach failures suggest (but not prove via CONJ1) single-edge decomposition 结构 不 work |
| **γ.G3** (ε-composable transfer) | [umr_path_gamma_G3_derivation_attempt.md](../proofs/umr_path_gamma_G3_derivation_attempt.md) | R1 review pending | WTB Thm 19 2nd-order, Kamin 2025 GEAT | **Conditional on γ.B closure**; 自身 不 structurally blocked |

**总观察**: 4 个 structural gaps 中, 3 个是 fundamental structural blocker (β.G4, β.G5, γ.B.G1); 1 个是 downstream dependent (γ.G3 依赖 γ.B closure).

---

## 2. Structural obstacle pattern 分析

### 2.1 共同 pattern — cross-space / cross-task transfer

所有 failed approaches 归结为同一 class of obstacle:

**Pattern**: 从 **A 空间/任务 的 inequality** 推到 **B 空间/任务 的 inequality**, 其中 A 和 B 有以下 structural 差异:
- Party sets (Alice-Charlie vs Alice-Bob vs Alice-Bob-Charlie-Eve)
- Task semantics (capacity vs secret key rate vs private state distance)
- Adversary models (LOPC vs umr vs trusted relay)

**Example β.G4**: umr Eve (含 Charlie + environments) → LOPC Eve (仅 environments). 需 construct simulation map — 4 approaches 的 candidate map 都 fail.

**Example γ.B.G1**: Alice-Charlie capacity $E_R(\mathcal{E}_1)$ → Alice-Bob umr key rate. 4 approaches 的 bridge 都 fail.

**Example β.G5**: Adaptive comb protocol → fixed channel repeated use. 4 approaches 的 amortization 都 fail.

### 2.2 Why AI draft fail repeatedly

**Fundamental reason [CONJ-DRAFT speculation]**: 
- AI 的 framework-matching heuristic (看哪个 amortized / teleportation / DPI / LOCC monotonicity framework **look like** it applies) **不 substitute for** structural reduction lemma
- AI 的 literature-pattern learning gives "usually these frameworks close such gaps" but 不**guarantee** specific instance 可 close
- cross-space transfer 本身是 research-level novelty; AI 无 established lemma fitting to **immediately** apply

### 2.3 Consequence: R0.2 C1+C2+C3 路径 the only sound path

**R0.2 C1 (independent validation not AI-only) 是 essential**:
- AI 无法 substitute for 人类/数值/另一 lemma framework 独立验证
- 5 次 cross-space trap 历史 (v1 FINDINGS → γ.v0.2 → γ.v0.3 → γ.v0.4 → β.v0.4+γ.v0.6) 体现 AI 系统性盲区 not fixed by more Codex iteration
- 用户 research-level work 是**唯一** sound path to [COROLLARY] 升级

### 2.4 What AI HAS done well (autonomous value)

Despite not closing structural gaps, AI attempts 产出:

1. **Concrete documentation of why each gap is hard** — "4 approaches tried, here's why each fails"; 比 scaffolding "gap open" 更 informative for user
2. **Literature pointers narrowed** — 从 "consult all Sub-Q3 literature" 缩到 "read Portmann-Renner §II composable framework for β.G4 Path C", "read Kamin 2025 §4 GEAT for β.G5 Approach C", "read Horodecki 2005 private state for γ.B.G1 Approach B"
3. **Speculative conjectures flagged** (γ.B.G1 CONJ1: 单边 PLOB 分解可能 structurally wrong) — 提供 user 考虑 reformulation 的起点
4. **Inter-path comparison** — γ path 在 "adversarial comb reduction" 这点比 β 优 (γ 不依赖 channel reduction)
5. **Numerical scaffolding infrastructure** (log-neg SDP, gap_shape analysis) — 持续 informational, not proof

---

## 3. Path forward — user research direction options

### 3.1 Option A: Push β path completely

- β.G1 (textbook labeling): 0.5 天 user
- β.G2 (tele-simulability + WTB Thm 12 apply): 2-3 天 user
- β.G3 (SDP numerical): AI 可做 (running), + 1-2 天 user analysis
- β.G4 (Eve model transfer): **MAJOR**, path C Portmann-Renner 需 PDF + 2-3 天 user novel proof
- β.G5 (adversarial comb): **MAJOR**, Approach C Kamin GEAT adaptation + 2-3 天 user
- **Total estimate**: 7-10 天 user + 2-3 AI days; possible failure modes if path C or Kamin don't extend

### 3.2 Option B: Push γ path (safety net)

- γ.A (single-edge PLOB): [COROLLARY] for bosonic covariant case — 0.5 天 user verify
- γ.B.G1 (DPI target lemma): **MAJOR**, 4 approaches fail, CONJ1 可能 structural — user 需 either new approach E 或 reformulation
- γ.B.G2 (BSM QCQ channel textbook): 0.5 天 user
- γ.B.G3 (Alice-Charlie ↔ Alice-Bob link): **MAJOR**, same obstacle as γ.B.G1
- γ.G3 (ε-composable): conditional on γ.B closure
- γ.G4 (classical announcement LOCC textbook): 0.5 天 user
- **Total estimate**: 5-8 天 user **if** γ.B chain 可以 close; **else** γ path blocked

### 3.3 Option C: Reformulate γ path per CONJ1 speculation

若 CONJ1 (单边 PLOB 分解 structurally wrong) 实际成立, consider reformulating γ:
- Re-target γ from $-\log_2(1-\eta_\text{arm})$ to **joint multi-edge bound** (e.g., Charlie broadcast capacity $\leq$ some function of $(\eta_A, \eta_B)$)
- 预期 scaling **可能 different** from original; user judge whether reformulated target worth pursuing
- Structural barrier: the reformulated target 本身是 new research question

### 3.4 Option D: Abandon formal upper bound pursuit, pivot to alternative Sub-Q3

若 β + γ 均 intractable:
- Focus on Sub-Q3 §4.5 seam report with current [CONJ] scaffolding
- Declare PROSPECTUS Sub-Q3 's "tight upper bound" question as open unresolved
- Pivot to Sub-Q4 gap attribution based on current upper bound candidates (without upgrade)
- Scientific value remains — "what we learned from trying 4 approaches" 本身是 contribution

---

## 4. Numerical state snapshot (Day 3)

- `gap_shape_analysis.py`: refresh complete, CSV + figures updated
- `beta_G3_E_R_effective_channel.py`: SDP running (1.5h+ on first grid point at 16×16 Choi)
- `max_rains_wang_duan_channel_sdp`: stub raised NotImplementedError (2 variants validation fail)
- Existing `log_negativity_channel_sdp` + `e_r_channel_ppt`: **functional** numerical upper bound tools
- toy β.G3 post-BSM: **0.19× Pirandola** at η=0.1 qubit

---

## 5. Recommendation (AI autonomous perspective)

**User 返回后可考虑**:

1. **先 PDF 上 Portmann-Renner 2022 + Kamin 2025** (已有 PDF) — 因为 β.G4 Path C 和 β.G5 Approach C 都 depends on 这些 framework 的 exact scope
2. **决定 γ CONJ1 严肃对待**: 是否尝试 Approach E (AI 未想到的) 或 reformulate γ target
3. **SDP 结果** (whenever β.G3 完成): analyze ratio vs Pirandola trusted-relay for numerical direction signal (非 proof)
4. **若 2-3 月 user time 仍不 close β/γ**: consider Option D — accept Sub-Q3 open-unresolved status

---

## 6. Commit trail Day 3 structural attempts

```
c586610 draft: β.G4 + γ.B.G1 structural derivation attempts
037d20a fix(β.G4 v0.2 + γ.B.G1 v0.2): R1 FAIL response
fb1c6dd docs(MQ v0.5 + β.G4 R2 PASS): Day 3 additions
f1d8c75 fix(γ.B.G1 v0.3): R2 FAIL Approach D fix
ede9c82 feat: max-Rains stub + P-R stub + Day 3 session log
1fc12c2 docs: γ.B.G1 R3 PASS + upper_bound_report v0.2 + gap_shape refresh
4ae4826 draft: γ.G3 ε-composable transfer v0.1
79d4f1e docs(session log): Update 1
7b32fe6 draft: β.G5 adversarial comb reduction v0.1
```

## Changelog

- **v0.1** (2026-04-23 Day 3 autonomous session): 4 structural gap AI attempts aggregated; path forward Options A-D articulated for user decision
