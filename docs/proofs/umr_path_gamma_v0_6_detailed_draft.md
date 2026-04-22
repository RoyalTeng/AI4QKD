# umr upper bound — path γ v0.6 detailed draft (R2 rewrite, open-only)

**版本**: v0.6-R2 **[CONJ-DRAFT, open-only]** — AI autonomous (2026-04-22 Day 3 late)

---

## ⚠️ R2 FIX notice — 响应 Codex R1 REJECTED

**R1 verdict** ([review-gamma-r1.json](../workflow/path-beta-gamma-detailed-draft/review-gamma-r1.json)): REJECTED (1 CRITICAL + 4 MAJORs)

**R1 问题清单**:
1. **CRITICAL (γ.B.1/γ.B.3/combined chain)**: 以 "DPI chain" 语言重新包装 v0.4 已 ruled out 的 cross-task transfer $R \leq \log K_\text{A-B} \leq E_R^\varepsilon(\mathcal{E}_1)$
2. **MAJOR (γ.B.2)**: Invalid DPI chain $I(A:\mathcal{B}(\hat{A},\hat{B})) \leq I(A:\hat{A},\hat{B}) \leq I(A:\hat{A})$ 缺 Markov + $I \leq E_R$ 一般不成立
3. **MAJOR (citations)**: Khatri-Wilde Prop 19.2 misdescribed as "any LOCC-compatible entanglement measure is monotone under LOCC" — 实际是 n-shot amortized converse specific form
4. **MAJOR (upgrade)**: γ.B.2/γ.4 labels "[CONJ-DRAFT → CLOSE]" / "[CLOSE]" silent upgrade despite "CONJ-DRAFT throughout"
5. **MAJOR (§9.1)**: γ.B.2 分类为 "half day textbook close" 过乐观; proof sketch 本身 broken

**R2 FIX per Codex suggestions** (完全采纳):
- γ.B.1, γ.B.3, combined chain: **删除 cross-task transfer**; operational reduction 保持 OPEN target
- γ.B.2: **rewrite around valid monotone, or leave open**; 删除 broken DPI chain + `I ≤ E_R` step
- Citations: Khatri-Wilde Prop 19.2 / Cor 19.3 仅在 actual amortized-entanglement form 引用 (literal content)
- Labels: γ.B.2 / γ.4 改回 **[CONJ-DRAFT, textbook-closable]** 或 **[OPEN, low-risk]**; 无 CLOSE label
- §9.1: workload split 修正 — 仅 genuinely textbook-stable 进 Phase 1

**本 R2 rewrite scope**:
- 保留 (i) γ.A single-edge PLOB [COROLLARY of verified WTB + PLOB]
- 保留 (ii) γ.4 classical announcement LOCC as textbook-closable note
- γ.B.1 / γ.B.2 / γ.B.3 / γ.3 **全改 OPEN structural**, 无 AI proof sketch
- combined chain 删除

---

## 0. 严谨性声明 (R0.2 compliance)

- AI autonomous draft → **[CONJ-DRAFT, open-only]**
- Citations: **[VERIFIED against PDF]** 或 **[RECALLED]** 明示; paraphrase 避免 — 使用 literal content
- Structural gaps 保持 OPEN; **不** AI draft proof sketch
- 用户 R0.2 C1+C2+C3 升级 pathway 仅 **post-proof review**

---

## 1. Target (open, no AI claim)

γ path formal target (Log 07 §4.5 strict reading):

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1 - \eta_\text{arm}) + \text{(ε-corrections)}$$

其中 $\eta_\text{arm} = \min(\eta_A, \eta_B)$.

**此 inequality 未 proven**; 本文件仅列 gaps + literature refs, **不** draft proof.

---

## 2. γ.A — Single-edge PLOB on $\mathcal{E}_1$ (textbook-stable, Alice-Charlie only)

### 2.1 Statement [COROLLARY of PLOB 2017 + WTB 2017]

$\mathcal{E}_1: A' \to \hat{A}$ bosonic pure-loss with transmittance $\eta_A$. 对 **Alice-Charlie point-to-point** LOPC-assisted secret key agreement:

$$K_{A\text{-}C}^\leftrightarrow(\mathcal{E}_1) \leq E_R^\infty(\mathcal{E}_1) = -\log_2(1 - \eta_A)$$

### 2.2 Verified citations (literal content)

- WTB 2017 Thm 12: "For teleportation-simulable channel $\mathcal{N}$: $P_\leftrightarrow^\dagger(\mathcal{N}) \leq E_R(\mathcal{N})$" [VERIFIED via WTB-2017.md §5.2]
- PLOB 2017 specialization: bosonic pure-loss $\mathcal{E}_\eta$ satisfies $E_R(\mathcal{E}_\eta) = -\log_2(1-\eta)$ [RECALLED — PLOB 2017 Eq 19]

### 2.3 Status

**[COROLLARY of verified]**. 此 bound 是 **Alice-Charlie** point-to-point capacity, **NOT** umr Alice-Bob key rate.

**Connection to umr Alice-Bob key rate**: **OPEN structural** (see γ.B below).

---

## 3. γ.B.1 / γ.B.3 — Operational link Alice-Charlie ↔ Alice-Bob (OPEN structural)

### 3.1 Target (未 proven)

希望 establish: Alice-Charlie bound $E_R(\mathcal{E}_1)$ 以某种 operational way bound Alice-Bob umr key rate.

### 3.2 Why this is open (Codex R1 critique internalized)

- **不能** simply claim $R_\text{A-B} \leq K_\text{A-C}^\text{LOPC}$ (这是 cross-task capacity transfer, v0.4 已 ruled out)
- **不能** disguise as "DPI chain" 或 "Eve operations non-increasing Alice-Bob correlation" — 这些仍是 cross-task transfer 的重新包装
- operational link 必须在**单一 consistent task/state model** 内证明, 不能 bridge different party sets 无 explicit reduction
- 这是 **Log 07 §4.5 明确 identified** 的 critical gap, 不能由 AI draft sketch close

### 3.3 Candidate frameworks (literature pointers, no AI application)

- **Horodecki 2005 bipartite private state** (PRL 94:160502): private state framework for key distillation [RECALLED]
- **Khatri-Wilde 2020 Ch 20 Secret Key Agreement**: framework for LOPC-assisted secret key via channel [VERIFIED via KhatriWilde-2020.md §3, literal content: "n-shot secret-key-agreement via $\mathcal{N}$ distributes $\log_2 K$ ε-secure key bits"]
- **Khatri-Wilde Cor 19.3**: "If $E_S$ is subadditive + separable-zero, and $\mathcal{N}$ is teleportation-simulable with resource state $\theta_{RB'}$, then $E_S(M_A;M_B)_\omega \leq n \cdot E_S(R;B')_\theta$" [VERIFIED via KhatriWilde-2020.md §2.2]
  - **Scope**: Prop 19.2 / Cor 19.3 是 bipartite Alice-Bob key agreement via **single fixed channel** $\mathcal{N}: A \to B$
  - **不 directly**: umr is three-party (Alice, Bob, Charlie); single-edge $\mathcal{E}_1$ is Alice-to-Charlie; Bob 的 contribution via $\mathcal{E}_2$ 与 Charlie broadcast 不 trivially subsumed

### 3.4 User formal work required (novel proof)

- Establish operational reduction: umr Alice-Bob secret key task → some well-defined bipartite task bounded by $E_R(\mathcal{E}_1)$ + $E_R(\mathcal{E}_2)$
- Alternative: show Alice-Bob key rate bounded by min of two single-edge bounds via **new reduction** (not via trivial monotonicity)
- **Not AI-draftable per R0.2 discipline** — see feedback memory 2026-04-22

### 3.5 Status

**OPEN structural blocker**. Severity: MAJOR (novel proof required).

---

## 4. γ.B.2 — Charlie BSM as quantum operation (OPEN, textbook-closable注释)

### 4.1 Status (R2 correction)

**R2 note**: 此 lemma previously contained broken DPI chain. Removed.

### 4.2 Textbook-stable facts only

- Charlie joint BSM on $(\hat{A}, \hat{B})$ is **CPTP map** with quantum output registers + classical outcome register. Standard Stinespring dilation exists. [RECALLED — Nielsen-Chuang 2010 §8, Wilde 2017 §11]
- 此事实不 足以 establish Alice-Bob correlation bound from Alice-Charlie bound — 需 γ.B.1/γ.B.3 operational reduction.

### 4.3 Status

**[OPEN, low-risk sub-note]**. Severity: 无 proof sketch attempted; 仅 framework level statement.

---

## 5. γ.3 — ε-composable finite-size transfer (OPEN structural, literature pointer)

### 5.1 Target (未 proven)

From asymptotic $E_R$ bound to ε-composable finite-$n$ rate bound.

### 5.2 Literature pointers

- **WTB 2017 Thm 19**: second-order expansion for covariant channels — $\hat{P}^\leftrightarrow(n,\varepsilon) \leq E_R(\mathcal{N}) + \sqrt{V/n}\Phi^{-1}(\varepsilon) + O(\log n/n)$ [VERIFIED via WTB-2017.md §6]
- **Kamin 2025 GEAT**: finite-key analysis framework for specific protocols [RECALLED; already integrated for MDI-QKD in `docs/findings/`]
- **Portmann-Renner 2022**: composable security framework [RECALLED — user must read Rev. Mod. Phys. 94:025008 for integration]

### 5.3 Why this is open

- WTB Thm 19 is for **single-channel Alice-Bob point-to-point**; umr has 3-party + adversarial Charlie + Eve model different from WTB
- ε-transfer 必须 handle composable security across umr 结构, 不是 simple 2nd-order plug-in

### 5.4 User formal work required

- Determine if Kamin GEAT covers umr Eve model (it was adapted for MDI-QKD, not umr directly)
- Or adapt Portmann-Renner framework to umr
- **Not AI-draftable**

### 5.5 Status

**OPEN structural**. Severity: MAJOR.

---

## 6. γ.4 — Classical announcement LOCC processing ([OPEN, low-risk])

### 6.1 Target (still formal statement needed)

Charlie's classical broadcast $c$ is public; Alice-Bob can condition LOCC on $c$ without increasing Alice-Bob quantum correlation.

### 6.2 Verified content

Khatri-Wilde Prop 19.2 (literal content): "$E(M_A; M_B)_\omega \leq n \cdot E^\mathcal{A}(\mathcal{N})$ for any LOCC-monotone separable-zero entanglement measure $E$, with $n$ uses of fixed channel $\mathcal{N}$" [VERIFIED via KhatriWilde-2020.md §2.1]

**Note**: This is specifically **n-shot amortized converse**, NOT a blanket "any LOCC-compatible measure is monotone" claim.

### 6.3 Status (no upgrade)

**[OPEN, low-risk]**. 虽然 textbook-level argument 可 formalize, 但 **not yet closed** — 用户 formal write-up required (~0.5-1 天 directly referencing Horodecki 2009 review §V or Khatri-Wilde Prop 19.2).

---

## 7. Gap summary (v0.6-R2)

| Gap | Severity | Closable by | AI-assistable? |
|---|---|---|---|
| γ.A (single-edge PLOB) | [COROLLARY of verified] | Already stands (Alice-Charlie only) | Verified citation only |
| γ.B.1 (operational link statement) | OPEN structural | User novel proof | NO |
| γ.B.2 (BSM as CPTP framework note) | [OPEN, low-risk] | User textbook write-up | partial (framework pointer) |
| γ.B.3 (Alice-Charlie ↔ Alice-Bob reduction) | OPEN structural | User novel proof | NO |
| γ.3 (ε-composable transfer to umr) | OPEN structural | User (Kamin/Portmann-Renner adaptation) | partial (framework pointer) |
| γ.4 (classical announcement LOCC) | [OPEN, low-risk] | User textbook write-up ~0.5 天 | partial (framework pointer) |

**Summary**: 1 [COROLLARY] (Alice-Charlie only) + 3 OPEN structural (blockers) + 2 [OPEN, low-risk] textbook. **不** combined chain claimed.

---

## 8. **不** claim combined chain

v0.6-R1 曾 combined chain: $R \leq \log K_\text{A-B} \leq E_R^\varepsilon(\mathcal{E}_1) \leq ...$ — **REJECTED** as cross-task transfer.

**R2 rewrite**: combined chain **removed**. 单边 PLOB ($\mathcal{E}_1$) 的 Alice-Charlie bound 与 Alice-Bob umr 之间**无 established link**.

---

## 9. User formal work plan (§9 recast per Codex R1)

### 9.1 Genuinely textbook-stable (Phase 1, ~1-2 天)

- γ.A verify: Alice-Charlie PLOB via WTB Thm 12 direct PDF read
- γ.4 write-up: classical announcement LOCC via Horodecki 2009 review §V 或 Khatri-Wilde Prop 19.2 direct PDF read

### 9.2 Novel proof required (structural blockers, Phase 2, **NOT literature-check**)

- γ.B.1 + γ.B.3: operational reduction umr Alice-Bob ↔ single-edge bounds — **novel structural proof**
- γ.3: ε-composable transfer to umr — adapt Kamin 2025 GEAT 或 Portmann-Renner framework; 可能需要 new technical work

**估时**: 每项 3-5 研究日 (novel proof). **不含** AI draft.

### 9.3 Post-proof C1+C2+C3 QA (~2-3 天 after Phase 2)

- **C1**: 跨家族 AI independent review direct-PDF; 或 C1(b) 人类纸笔; 或 C1(c) 数值
- **C2**: user 逐项签字
- **C3**: dev-reviewer 双 Codex QA PASS
- **注意**: C1+C2+C3 是 **post-proof review**; 不 close structural gaps — gaps 必须先由 §9.2 novel proof closed

---

## 10. 严谨性 summary

- **[CONJ-DRAFT, open-only]** — structural gaps OPEN, 无 AI proof sketch
- **不**声称 combined chain; **不**跨 task capacity transfer
- **不**升级任何分级
- Citations 严格 [VERIFIED] / [RECALLED]; paraphrase 最小化, literal content 优先
- AI autonomous **不** draft proof sketch for structural gaps (per feedback memory 2026-04-22)

---

## 11. 与 path β 关系

γ 作 β 的 safety net per Q1 Option 2. β / γ **均为** structural gaps OPEN 的 scaffolding level; **非** formal proven 状态. 用户 research-level work 同时 needed for both.

---

## Changelog

- **v0.6-R2** (2026-04-22 late): Codex R1 REJECTED response — delete cross-task transfer from γ.B.1/B.3/combined chain; rewrite γ.B.2 as framework note (no broken DPI chain); demote CLOSE labels to [OPEN]; recast §9 separating textbook from novel proof; removed combined chain
- **v0.6-R1** (earlier): detailed draft with 5 Lemma proof sketches — REJECTED for cross-task transfer in DPI chain disguise
- **v0.4/v0.5 and earlier** (see umr_path_gamma_v0_4_derivation.md): original strict Log 07 §4.5 scaffolding
