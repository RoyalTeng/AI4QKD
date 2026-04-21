# Workflow log: werner-reduction (T1)

**Mode**: dev-reviewer on new research document (not code)
**Feature**: T1 ≡ RESEARCH_PLAN §2.2 R2.1 Level 4 upgrade — MDI ideal symmetric Werner form derivation
**Scope**: `docs/proofs/mdi_werner_reduction.md`
**Authorization**: 2026-04-21 user delegation under autonomous mode; C3 gate via dev-reviewer; stays at [CONJ] pending user C1 + C2

## Round commit trail

- v0.1 draft: 20d99d4 (Round 1 draft)
- v0.2 Round 2 FIX: fb483b4 (R1 REJECTED response)
- v0.3 Round 3 FIX: f50bfd8 (R2 REJECTED response; classical vs quantum rewrite)
- Round 4 downstream FIX: 9ede1fd (MDI-QKD.md §3.3.5 + kamin_sdp_mdi.py docstring)

## Round 1 (v0.1 @ 20d99d4)

**Agent 1 (xhigh, diff)**: REJECTED (1 CRITICAL + 4 MAJOR)
- CRITICAL: W2 outcome-dependent Bell-centered Werner missing
- MAJOR: A6 Table I misread; BDCZ Eq. numbers unverified; W4 delegation unjustified; W1/W3 [THM] labels overclaim

**Agent 2 (high, holistic)**: FAIL (2 MAJOR + 3 MINOR)
- Overlapping + C1(c) overclaim + "签字" language + test path typo + Lo-Curty-Qi §II vs Appendix A + missing concept map

## Round 2 (v0.2 @ fb483b4)

Rewrite closing R1 issues. Numerical verify Agent 1 CRITICAL (BSM outcome-dependent Bell-centered Werner confirmed via Python).

**Agent 1**: REJECTED (1 CRITICAL + 1 MAJOR)
- CRITICAL: W2.5 logic still wrong — confused classical bit-flip with quantum Pauli correction; (I⊗X)|Ψ⁻⟩ = -|Φ⁻⟩ not |Φ⁺⟩
- MAJOR: MDI-QKD.md §3.3.5 still missing basis-dependent rule

**Agent 2**: REJECTED (NEW_REGRESSION — W2.5 internal contradiction; kamin_sdp_mdi.py convention mismatch)

## Round 3 (v0.3 @ f50bfd8)

**Fundamentally different approach**: abandoned quantum Pauli correction picture; rewrote W2.5 as CLASSICAL raw-key bit XOR with basis-dependent Table I rule. Numerical verify via independent Python: Ψ⁻/Ψ⁺ + Table I flip → QBER = 2(1-F')/3 (matching Φ⁺-centered Werner).

**Agent 1 (xhigh, diff)**: FAIL (2 MAJOR + 1 suggestion)
- Core W2.5 CRITICAL substantively fixed; 3-round STOP rule NOT triggered
- MAJOR: MDI-QKD.md §3.3.5 still has old basis-independent flip rule
- MAJOR: kamin_sdp_mdi.py docstring still asserts superseded state-level Werner claim
- Suggestion: W2.5 prose claim wider than algebra (fine at [CONJ])

**Agent 2 (high, holistic)**: **PASS**
- CRITICAL_FIX_VALIDITY: original defect closed
- LABEL_DISCIPLINE: clean (R0.3 grades only)
- TABLE_I_ACCURACY: matches PDF
- THIRD-ROUND_JUDGMENT: fundamentally different, not recurring
- **READY_FOR_PENDING_USER_REVIEW: yes**
- Core conclusion: memo is honest [CONJ] with explicit gaps

## Round 4 (9ede1fd)

Mechanical downstream consistency fixes per Agent 1 R3 MAJOR:

1. `docs/literature/MDI-QKD.md` §3.3.5: rewritten basis-dependent flip rule (Z: Ψ⁻/Ψ⁺ both flip; X: Ψ⁻ flip, Ψ⁺ no flip); classical vs quantum distinction explicit
2. `qkdx/numerics/kamin_sdp_mdi.py` docstring (module + `kamin_mdi_h_per_sift`): rewritten to match v0.3 — outcome-dependent Bell-centered Werner, classical Table I flip, raw-key statistics equivalence, [CONJ] delegation pending G1 structural equivalence; corrected Lo-Curty-Qi §II → Appendix A reference

AST syntax check pass. Python import not verified in shell (cvxpy not installed in system Python).

## FINALIZE decision (autonomous 2026-04-22)

**T1 FINALIZED at [CONJ]** per 2026-04-21 user delegation:
- Agent 2 R3 explicit PASS + READY_FOR_PENDING_USER_REVIEW
- Agent 1 R3 acknowledged core CRITICAL closed, no STOP recommendation
- R4 downstream fixes committed; no further review round scheduled (diminishing returns; core already closed)

**Reason for stopping at R4 without new review cycle**:
- Core mathematical defect (W2 outcome-dependent Werner + W2.5 classical/quantum) is closed per both agents
- Remaining issues are **documentation consistency** (§3.3.5 wording + docstring wording), not research correctness
- Dev-reviewer skill allows max 5 rounds; 4 rounds used for one [CONJ]-level doc is sufficient; continued rounds show diminishing marginal value
- Document stays at **[CONJ]**; no rigor grade upgrade; user C1 + C2 still required for [COROLLARY]

**User review queue entry**:
- Primary: `docs/proofs/mdi_werner_reduction.md` v0.3+
- Secondary: `docs/literature/MDI-QKD.md` §3.2 + §3.3.5 (updated consistent)
- Impl docstring: `qkdx/numerics/kamin_sdp_mdi.py` (updated consistent)
- Deferred: W4 G1 structural SDP equivalence proof (substantial work; optional Level 4 upgrade)

**Not done (explicit for user)**:
- Independent PDF-level verification of Briegel 1998 / Dür 1999 Eq. numbers (requires human or C1(a))
- Independent algebraic re-derivation of W2 公式 (requires human or C1(c) Mathematica)
- SDP structural equivalence proof (Choi-level BB84 EB ↔ MDI post-Table-I effective)
- Non-ideal extension (non-symmetric / misalignment / decoy / finite-key)

**Decision authority**: autonomous per 2026-04-21 user delegation; document stays at [CONJ]; neither C1 nor C2 claimed satisfied.
