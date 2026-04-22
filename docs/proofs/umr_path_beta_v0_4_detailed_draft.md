# umr upper bound — path β v0.4 detailed draft (R2 rewrite, open-only)

**版本**: v0.4-R2 **[CONJ-DRAFT, open-only]** — AI autonomous (2026-04-22 Day 3 late)

---

## ⚠️ R2 FIX notice — 响应 Codex R1 REJECTED

**R1 verdict** ([review-beta-r1.json](../workflow/path-beta-gamma-detailed-draft/review-beta-r1.json)): REJECTED (1 CRITICAL + 3 MAJORs)

**R1 问题清单**:
1. **CRITICAL (β.5)**: Khatri-Wilde Prop 19.2 (n uses of **fixed** channel) 误用于 adversarial comb → fixed channel reduction
2. **MAJOR (β.4)**: LOPC Eve 从 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2)$ 模拟 Charlie register — 无 simulation map proof
3. **MAJOR (narrative)**: Section titles "closes β.G4" silent upgrade despite body admitting gaps open
4. **MAJOR (§9)**: Phase 1-4 plan 把 β.G4/β.G5 structural gaps 当 literature check — 误导用户

**R2 FIX per Codex suggestions** (完全采纳):
- β.4 / β.5 **rewrite as "open comparison problem"** — 删除 proof sketch; 保留 gap statement + literature refs
- Section headers **rename to "attempted direction"** — 不再说 "closes X"
- §7 combined chain **removed** (was conditional on β.4 + β.5 closure)
- §9 plan **recast**: separate "PDF verification" from "novel proof required"; C1+C2+C3 仅 post-proof QA, 不 close structural gaps

**本 R2 rewrite 的 scope 限制**:
- 仅保留 (i) textbook-stable labeling (β.1) (ii) framework pointers with verified citations (β.2) (iii) numerical roadmap (β.3)
- β.4 + β.5 = structural blockers, open, **no AI proof sketch**
- **不**声称 combined chain 成立

---

## 0. 严谨性声明 (R0.2 compliance)

- AI autonomous draft → **[CONJ-DRAFT, open-only]**
- Citation fidelity taxonomy (五级, 均 明示 per citation):
  - **[VERIFIED against PDF]** — 已对 PDF 原文核对 (本项目内罕见; 须 explicit)
  - **[MEMO-LEVEL QUOTE]** — reproduced from `docs/literature/*.md` 本地 memo; memo 已对 PDF 做过 Level 3 精读, 但 memo 本身非 PDF 原文; 用户须对照 PDF verify
  - **[SUMMARY]** / **[SUMMARY, not direct quote]** — 本地 memo 或 AI 的 paraphrased summary, 非原文 quote; PDF verify required
  - **[INFERENCE, unverified]** — AI 的 reading / 推断, 无 PDF 直接支持; user must verify
  - **[RECALLED]** — AI 记忆, 未核对 memo 或 PDF; lowest confidence
- 所有 structural gaps 保持 OPEN; **不** AI draft proof sketch
- 用户 R0.2 C1+C2+C3 升级 pathway 仅适用 **post-proof review**

---

## 1. Target (open, no AI claim)

umr path β 的 formal target (Log 07 §4.4):

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq ? \cdot E_R^\infty(\tilde{\mathcal{M}}) + \text{(ε-corrections)}$$

其中 $\tilde{\mathcal{M}}$ 是某个 effective channel 的候选. **此 inequality 未 proven**; 本文件仅列 gaps 和 literature refs, **不** draft proof.

---

## 2. β.1 — Two-source-to-bipartite-input labeling (textbook-stable)

### 2.1 Statement

Alice 与 Bob 独立 source $\rho_{AA'} \otimes \sigma_{BB'}$ 可视为 composite system $(AA') \otimes (BB')$ 上 product state. LOPC / secret-key-agreement framework 允许 product initial state.

### 2.2 Literature support (paraphrased summary, not literal quote)

- Khatri-Wilde 2020 Ch 20 Secret Key Agreement framework [SUMMARY, not direct quote]: per `docs/literature/KhatriWilde-2020.md` §3.1 内部描述, 本地 memo 概括该章 LOPC-assisted secret-key agreement 允许 product initial state. **Caveat**: 此为 memo paraphrase; 用户须直接阅读 Khatri-Wilde PDF Sec 20.1 原文 verify product-state acceptance.

### 2.3 Status

**Textbook labeling**. 用户 verify: ~0.5 天 (read Khatri-Wilde Sec 20.1 directly).

---

## 3. β.2 — Effective channel $\tilde{\mathcal{M}}$ construction (framework pointer, open)

### 3.1 Target construction

希望 define effective channel $\tilde{\mathcal{M}}$ encoding umr per-round action (Alice source → $\mathcal{E}_1$ → Charlie BSM + broadcast → Bob → $\mathcal{E}_2$).

### 3.2 Open sub-gaps

- **β.2.a [OPEN]**: $\tilde{\mathcal{M}}$ 是 2-input broadcast channel with quantum+classical outputs; PLOB / WTB 原 framework 是 point-to-point. 是否 tele-simulable? **No AI sketch.**
- **β.2.b [OPEN]**: 若 $\tilde{\mathcal{M}}$ not tele-sim, 退到 Khatri-Wilde amortized framework (Prop 19.2) **仍需**把 adversarial umr reduced to "n uses of fixed $\tilde{\mathcal{M}}$" — 此 reduction 是 β.G5 structural blocker.

### 3.3 Relevant citations (mix of memo-level quotes + paraphrased summaries)

- **WTB 2017 Thm 12** (memo-level quote, reproduced from `docs/literature/WTB-2017.md` §5.2): "For teleportation-simulable channel $\mathcal{N}$: $P_\leftrightarrow^\dagger(\mathcal{N}) \leq E_R(\mathcal{N})$". **Caveat**: 此为本项目 memo 的 statement; 用户须对照 WTB 2017 PDF Thm 12 原文 verify.
- **Khatri-Wilde 2020 Prop 19.2** (memo-level quote per `docs/literature/KhatriWilde-2020.md` §2.1): "$E(M_A; M_B)_\omega \leq n \cdot E^\mathcal{A}(\mathcal{N})$" for any (n, M, ε) LOCC-assisted quantum communication protocol over channel $\mathcal{N}_{A\to B}$ with LOCC-monotone + separable-zero E. **Caveat**: 本地 memo 的 statement; 用户须对照 Khatri-Wilde 2020 Ch 19 PDF Prop 19.2 原文 verify (尤其 "LOCC-monotone + separable-zero" 条件 exact wording).
- **重要 scope note (my inference, not literal citation)**: Prop 19.2 的 n uses of channel 属于 **fixed $\mathcal{N}$** 的 repeated use; 对 "adversarial comb reduced to fixed channel" 的情形 Prop 19.2 **本身不直接 cover** — 这是 β.G5 structural gap. 此 scope 推断由 memo 对 statement 的 reading 得出, 用户须 PDF 确认.

### 3.4 Status

**Open structural gap** (β.G2 + β.G5 合并 view). User research-level proof required.

---

## 4. β.3 — Numerical roadmap for $E_R^\infty(\tilde{\mathcal{M}})$ (AI-assistable scaffolding)

### 4.1 Scaffolding actions

- 扩展 `qkdx/numerics/upper_bound.py` 添加 $E_R$ / max-Rains SDP over effective $\tilde{\mathcal{M}}$ Choi state
- Toy qubit scan $(\eta_A, \eta_B)$ grid (已部分 done — commit 704ab29 β.G3 post-BSM toy)
- Bosonic direct SDP 需 user desktop 环境 (本 AI env 内存受限)

### 4.2 Status

**Numerical diagnostic only** (scaffolding, not proof). Prior toy (0.19× Pirandola at η=0.1) is **informational**, not $E_R^\infty$.

---

## 5. β.4 — Eve model comparison (umr vs LOPC) — OPEN, attempted direction

### 5.1 Attempted direction (no proof)

希望 compare key rates under 两个 adversary classes:
- $\mathcal{A}_\text{umr}$: Eve 持 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2) \cup$ Charlie register
- $\mathcal{A}_\text{LOPC}$: Eve 持 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2)$ only

**期望 inequality direction**: $R^{\mathcal{A}_\text{umr}} \leq R^{\mathcal{A}_\text{LOPC}}$ (umr Eve 更强 → umr rate 更低).

### 5.2 Why this is open (Codex R1 critique internalized)

- **不能 simply claim** LOPC Eve 可从 $\text{Env}(\mathcal{E}_1, \mathcal{E}_2)$ 模拟 Charlie register
- Charlie's BSM outcome 统计 **不 generally** determined by environment systems alone
- 需要 explicit **degrading / simulation map** $\Sigma: \text{Env}(\mathcal{E}_1, \mathcal{E}_2) \to$ Charlie register; 此 map 是否存在取决于具体 $\mathcal{E}_1, \mathcal{E}_2$ family — 一般情况 **open**

### 5.3 User formal work required (novel proof)

- Construct (or disprove existence of) explicit $\Sigma$ map for bosonic pure-loss + Bell BSM case
- Alternative: Portmann-Renner 2022 composable framework 直接证明 $\varepsilon$-secret rate monotonicity [RECALLED — user must read Rev. Mod. Phys. 94:025008]
- **Not AI-draftable**

### 5.4 Status

**OPEN**, structural blocker. Severity: MAJOR (novel proof required).

---

## 6. β.5 — Adversarial comb → fixed channel reduction — OPEN, attempted direction

### 6.1 Attempted direction (no proof)

umr 每轮 Charlie 可 adapt strategy based on prior rounds' announcements → n-shot adversarial **process/comb**, not i.i.d. fixed channel. Target: reduce this comb to repeated uses of fixed $\tilde{\mathcal{M}}$.

### 6.2 Why this is open (Codex R1 critique internalized)

- Khatri-Wilde Prop 19.2 (n uses of **fixed** channel) **不 cover** this reduction
- 把 Prop 19.2 applied 到 adversarial Charlie = cross-space transfer (R0.2 red flag)
- **需要 separate theorem** 直接处理 adversarial combs / secret-key protocols

### 6.3 Candidate frameworks (literature pointers, no AI application)

- **Kamin 2025 GEAT**: entropy accumulation for comb structures; 但针对 i.i.d. Markov assumptions, 不直接 cover umr Charlie [RECALLED]
- **Pirandola 2017 teleportation stretching**: reduces comb to fixed channel for cooperative parties; 但 umr Charlie 是 adversarial, assumption 不满足 [RECALLED]
- **Khatri-Wilde 2020 Ch 20 amortized framework** [INFERENCE, unverified]: 本 AI 推断该章中 "adaptive" 语境是 Alice-Bob LOCC strategies, 与 umr Charlie 的 adversarial adaptation **可能**不同. **Caveat**: 此区分未对 Khatri-Wilde Ch 20 PDF 精确核对; 用户须直读该章原文 verify 是否可延伸到 adversarial relay case.

### 6.4 User formal work required (novel proof)

- 确定哪个 framework 可覆盖 adversarial Charlie; 若均不 cover, 需开发新的 reduction argument
- **Not AI-draftable**

### 6.5 Status

**OPEN**, structural blocker. Severity: MAJOR (novel proof required).

---

## 7. Gap summary (v0.4-R2)

| Gap | Severity | Closable by | AI-assistable? |
|---|---|---|---|
| β.1 | MINOR (labeling) | User ~0.5 天 textbook verify | YES (verified citation only) |
| β.2.a ($\tilde{\mathcal{M}}$ tele-sim) | OPEN structural | User novel proof | NO |
| β.2.b (amortized framework applicability) | OPEN structural | User novel proof | NO |
| β.3 (E_R SDP numerics) | SCAFFOLDING | AI numerical + user analysis | YES (diagnostic) |
| β.4 (Eve model transfer) | OPEN structural | User novel proof (Portmann-Renner or explicit Σ map) | NO |
| β.5 (adversarial comb → fixed) | OPEN structural | User novel proof (new framework or extension) | NO |

**Summary**: 1 MINOR (textbook) + 4 OPEN structural (blockers) + 1 scaffolding. **不** combined chain claimed; **不** proof sketch for β.4/β.5.

---

## 8. 与 Pirandola 2019 的比较

**方向 agnostic**. $E_R^\infty(\tilde{\mathcal{M}})$ 与 $-\log_2(1-\sqrt{\eta_A\eta_B})$ **未比较**; 任何比较声称需 β.3 numerical + β.2/β.4/β.5 close.

---

## 9. User formal work plan (§9 recast per Codex R1)

### 9.1 PDF verification only (literature-check, ~1 天)

- β.1 via Khatri-Wilde Sec 20.1 direct PDF read [~0.5 天]
- β.3 numerical setup pointer [~0.5 天 user framework choice]

### 9.2 Novel proof required (structural blockers, NOT literature-check)

- β.2.a + β.2.b: tele-simulability of $\tilde{\mathcal{M}}$ + amortized framework applicability — **novel structural proof**
- β.4: Eve model transfer — either explicit $\Sigma$ map construction, or Portmann-Renner composable proof (user reads PDF + crafts proof)
- β.5: adversarial comb → fixed channel reduction — likely requires **new framework** beyond Khatri-Wilde Ch 20 / Kamin 2025

**估时**: 每项 3-5 研究日 (novel proof work). **不含** AI draft.

### 9.3 AI numerical parallel (after structural gaps close)

- β.3 SDP 在 user desktop 运行
- 目的是 **informational diagnostic** on $E_R^\infty(\tilde{\mathcal{M}})$ vs Pirandola, 非 proof

### 9.4 Post-proof C1+C2+C3 QA (~2-3 天 after Phase 2 done)

- **C1**: 跨家族 AI independent review directly reading PDFs (WTB + Khatri-Wilde + Portmann-Renner); 或 C1(b) 人类纸笔; 或 C1(c) 数值
- **C2**: user 逐项签字 each lemma
- **C3**: dev-reviewer 双 Codex QA PASS
- **注意**: C1+C2+C3 是 **post-proof review** QA; 不能 close structural gaps — gaps 必须已 closed by §9.2 novel proof 才能 QA

---

## 10. 严谨性 summary

- **[CONJ-DRAFT, open-only]** — 所有 structural gaps 保持 OPEN
- **不**声称 combined chain inequality 成立
- **不**升级任何分级
- Citations 使用 §0 定义的 5 级 taxonomy: **[VERIFIED]** / **[MEMO-LEVEL QUOTE]** / **[SUMMARY]** / **[INFERENCE, unverified]** / **[RECALLED]**; 非 PDF-verified 项 caveats 明示
- AI autonomous **不** draft proof sketch for structural gaps (per feedback memory 2026-04-22)

---

## Changelog

- **v0.4-R2** (2026-04-22 late): Codex R1 REJECTED response — rewrite as open-only; delete β.4/β.5 proof sketches; rename headers; recast §9 separating literature-check vs novel proof; combined chain removed
- **v0.4-R1** (earlier): detailed draft with 5 Lemma proof sketches — REJECTED for cross-space transfer + Prop 19.2 misuse
- **v0.3 and earlier** (see umr_path_beta_derivation.md): original scaffolding
