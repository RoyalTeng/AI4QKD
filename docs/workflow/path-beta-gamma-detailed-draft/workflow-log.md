# Workflow log: path-beta-gamma-detailed-draft

**Feature**: β v0.4 + γ v0.6 detailed draft derivations for umr upper bound
**Authorization**: user "两个推导都做吧" (2026-04-22 autonomous)
**Max rounds**: 5 (dev-reviewer skill default)
**Outcome**: both PASS — β after R4, γ after R2

## Files reviewed

- `docs/proofs/umr_path_beta_v0_4_detailed_draft.md`
- `docs/proofs/umr_path_gamma_v0_6_detailed_draft.md`

## Round-by-round

### R1 (commit 5ed30ee)

Initial drafts with 5 Lemma proof sketches each.

- **β R1**: REJECTED (1 CRITICAL + 3 MAJORs)
  - CRITICAL: Khatri-Wilde Prop 19.2 misuse for adversarial comb → fixed channel
  - MAJOR: β.4 LOPC Eve simulation unsupported
  - MAJOR: section titles "(closes β.Gx)" silent upgrade
  - MAJOR: §9 misclassifies structural gaps as literature-check
- **γ R1**: REJECTED (1 CRITICAL + 4 MAJORs)
  - CRITICAL: v0.4 cross-task transfer reintroduced as "DPI chain"
  - MAJOR: γ.B.2 broken DPI chain
  - MAJOR: Prop 19.2 citation misdescribed
  - MAJOR: γ.B.2/γ.4 "[CLOSE]" silent upgrade
  - MAJOR: §9.1 γ.B.2 "half day textbook" overstated

→ Initially retracted (commit bed95ad) per "REJECTED → 停止" skill rule.
→ User instructed to continue per Codex suggestions → R2 rewrite.

### R2 (commit 4cbe141) — open-only rewrite

Completely rewritten per Codex R1 suggestions:
- β.4/β.5, γ.B.1/γ.B.3 proof sketches deleted; all structural gaps = OPEN
- Combined chain removed both docs
- Section titles de-upgraded
- §9 recast: separate PDF-verification from novel-proof-required
- Citations relabeled to literal content only

- **γ R2**: **PASS** (0 issues, ready to commit)
- **β R2**: FAIL (1 MAJOR only — citation fidelity at lines 57, 76-80, 146 labeled "literal" but actually paraphrases)

### R3 (commit f46b5aa) — β line-level citation fix

Relabeled β citations: [SUMMARY] / [MEMO-LEVEL QUOTE] / [INFERENCE, unverified] per actual fidelity.

- **β R3**: FAIL (2 MAJORs)
  - §0 policy line still claimed only [VERIFIED]/[RECALLED]
  - §10 summary same over-claim
- (Codex process initially stuck, killed zombies, relaunched — network flaky symptom)

### R4 (commit 750c27c) — β taxonomy alignment

§0 and §10 rewritten to enumerate 5-level citation taxonomy.

- **β R4**: **PASS** (1 minor style only — "四级" should be "五级")
- Fix committed as part of FINALIZE.

## Codex process stability notes

- R3 Codex exec hung for 47 minutes (sleeping 0% CPU) → killed
- Found zombie codex processes (1+ hour and 1+ day old) from prior runs
- Relaunched R3 → completed normally
- R4 relaunched cleanly after zombie cleanup, completed in ~1 minute
- Lesson: Codex CLI xhigh can hang on network; periodic zombie cleanup may be needed

## Outcome

Both drafts reached **open-only [CONJ-DRAFT]** state with:
- All structural gaps (β.G2/G4/G5, γ.B.G1/G3, γ.G3) explicitly OPEN
- No combined chain, no cross-task transfer, no cross-space transfer
- Citations taxonomy 5-level with caveats
- §9 user work plan separates textbook-check from novel-proof

**NOT upgraded**: R0.2 C1+C2+C3 pathway still required for any formal promotion.

## Retraction record

The initial R1 REJECTED retraction record at [docs/research/RETRACTION.md §7](../../research/RETRACTION.md) remains as historical lesson (5th cross-space trap incident). R2 rewrite is considered a response to Codex suggestions rather than a new independent draft; the retraction history is preserved.
