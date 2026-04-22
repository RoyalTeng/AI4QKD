# Workflow log: beta-G3-numerical-review

**Feature**: β.G3 numerical exploration (toy qubit model, post-BSM conditional E_R)
**Authorization**: User 2026-04-22 Q1 Option 2 (β main + γ safety) + "发动评审，让codex评审一下"
**Max rounds**: 5 (dev-reviewer skill default)
**Outcome**: PASS after Round 3

## Commit trail

- Pre-review state: 0eb0de5 (β.G3 plot + dense sweep + Werner + tensor + post-BSM all committed)
- R1 review: commit 0eb0de5 baseline
- R2 FIX: c214fe3
- R2 review: commit c214fe3 baseline
- R3 FIX: 975bec3
- R3 review: commit 975bec3 baseline (PASS)

## Round log

### Round 1 (commit 0eb0de5)

**Codex verdict**: REJECTED
- CRITICAL-1: 0.094× (Ψ- only) vs 0.19× (summed) inconsistent across docs
- CRITICAL-2: Silent rigor upgrade (directional → definitive → fast-track β)
- MAJOR-1: "physical" mislabel; p_BSM scaling 不符 physical MDI
- MAJOR-2: Doc 结构混乱 + Werner "lower bound" mislabel

### Round 2 FIX (commit c214fe3)

Comprehensive rewrite:
- Canonical convention fixed: all-Bell summed (0.19×)
- Demote all "definitive/fast-track" to [CONJ] exploratory
- Explicit qubit toy vs physical MDI caveats
- Werner relabeled "heuristic surrogate"
- Doc structure cleaned

### Round 2 review

**Codex verdict**: FAIL (1 MAJOR)
- §2 "Ψ±=0.13×" vs §3.1 "2/4×all-Bell=0.10×" 自相矛盾 (都是 handwave numbers)

### Round 3 FIX (commit 975bec3)

Reconcile with 实测 numbers:
- Direct compute per-outcome contributions at η=0.1
- Ψ- only = 0.0949×
- Ψ± linear-optic = 0.1899× (因为 Φ± contribute 0 in toy)
- All-Bell = 0.1899× (same as Ψ± in this toy)
- Updated §2 table + §3.1 prose with verified values + explanation

### Round 3 review

**Codex verdict**: **PASS** (0 issues)
- Verified at HEAD 975bec3
- §2 Ψ±=0.1899× consistent with §3.1 per-outcome breakdown
- Toy model explanation clear (Φ± separable → not contributing)
- Round 2 issue closed, no regression

"Ready to commit - None" recommendation.

## FINALIZE

**Outcome**: β.G3 numerical work cycle closed at [CONJ] toy exploratory level.
- 0 rigor upgrades
- Three toy variants (A tensor / B Werner heuristic / C post-BSM) documented with explicit caveats
- Canonical convention (all-Bell summed 0.19×) fixed and consistent across docs
- β-vs-Pir direction remains agnostic per Log 07 §4.4
- β path decision (formal work) not driven by toy numerical signal

**User guidance preserved**:
- β Phase 1 (β.G1 + β.G4) first, useful for γ fallback too
- β.G3 direct bosonic SDP on desktop = critical decision point
- γ safety net equally preserved

---

## γ toy numerical companion review (parallel to β.G3)

**Feature**: γ path toy Choi-state diagnostic (single amp-damp log-negativity)
**Authorization**: user "推进吧" autonomous
**Max rounds**: 5
**Outcome**: PASS after Round 2

### Round 1 (commit 83ff61a)

**Codex verdict**: FAIL (3 MAJORs)
- MAJOR-1: MQ §11.0.3 line 266 "若 β 正确 formal 成立，会给约 5× tighter than γ" → directional formal claim
- MAJOR-2: γ script docstring "rigorous derivation via data-processing monotonicity" → silent rigor upgrade (DPI 仍 [CONJ])
- MAJOR-3: γ script interpretation "γ bound ≤ LN(E_1)" → overstates without channel-to-state reduction lemma

### Round 2 FIX (commit 476e912)

- γ script docstring: relabel "toy Choi-state diagnostic ONLY, 非 γ path derivation"; explicit DPI [CONJ] caveat
- γ script interpretation block: "LN_Choi is NOT the γ bound"; "does NOT predict formal β-vs-γ ordering"
- MQ §11.0.3: replace "若 β formal 成立" with "严格 local 解读：两个 surrogate 数值相差 ~4.7×... 不 predict formal β-vs-γ 序列"
- Add "Q1 决策不受 toy 数值影响" 明示

### Round 2 review

**Codex verdict**: **PASS** (0 issues)
- All 3 R1 MAJORs closed
- No regression; math consistency verified (LN = log2(1+η_arm) matches reported toy values)
- §11.0.2 agnostic β.G3 stance consistent with reworded §11.0.3

"Ready to commit - None" recommendation.

### FINALIZE (γ toy)

**Outcome**: γ toy numerical cycle closed at [CONJ] informational level.
- 0 rigor upgrades
- Toy Choi-state LN 数据 保留 (log2(1+η_arm) baseline)
- β/γ toy 对比 descriptive only, 不 drive formal decision
- Q1 决策 (β main + γ safety net) 不受 toy numerics 影响
