# ADR 0001 — Kamin Fig.3 < 5% tolerance task split

**Status**: **Accepted** (2026-04-22 via Codex proxy binding per 2026-04-21 user delegation)
**Proxy verdict**: Agent 1 (xhigh, [review-diff-1.json](../workflow/adr-0001-proxy/review-diff-1.json)) + Agent 2 (high, [review-holistic-1.md](../workflow/adr-0001-proxy/review-holistic-1.md)) both PASS Option B with consistent recommendation. Binding as process-level decision per [feedback memory 2026-04-21](../../.claude/projects/-Users-tengjun-Desktop-ai4qkd--1--AI4QKD/memory/feedback_autonomous_delegation_2026-04-21.md).
**Required correction (both agents concurred)**: T2-Phase A is a **proxy milestone only**; it does **not** close S2.5 hard acceptance or user 3b sign-off. Both **remain open** until T2-Phase B completes. See §Proxy corrections below.
**Decider**: User 2026-04-21 delegated process decisions to Codex proxy per [feedback memory](../../.claude/projects/-Users-tengjun-Desktop-ai4qkd--1--AI4QKD/memory/feedback_autonomous_delegation_2026-04-21.md)
**Binding mechanism**: Two-Codex PASS + verdict 一致 → binding as R0.2 C2 proxy (process / ADR level only; **not** rigor grade upgrade)
**Trigger**: [AUTONOMOUS_RESEARCH_PLAN T2](../AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md) — user review decision **3b** ("Kamin Fig.3 < 5% tolerance")

---

## Context

[RESEARCH_PLAN §3.3 S2.5](../RESEARCH_PLAN.md) hard acceptance criterion:

> "对 decoy-state BB84，有限密钥率（给定 n, ε_sec, ε_corr）与 Kamin 2025 Fig. 4 / Table 1 误差 < 5%"

Current diagnostic ([AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md §1.3.2](../AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md)):
- Asymptotic R at γ=0.1: my 0.242 vs Kamin ~0.28 → **20% offset** (> 5%)
- n=10^12 finite-key: my rate ≈ 1/3 of Kamin → **3× offset**

Root cause analysis (from [kamin_decoy_sdp.py:24-38 docstring](../../qkdx/numerics/kamin_decoy_sdp.py)):

1. **Honest channel model mismatch**: My impl uses per-photon loss + misalignment. Kamin Fig.3 uses [WL22 beamsplitter + misalignment model](https://arxiv.org/abs/2203.10669) with $\theta_\text{misalign} = \sin^{-1}(0.1)$
2. **No dark counts**: My impl explicitly ignores. Kamin Fig.3 uses non-zero background
3. **`eta_1_calib` calibration**: My impl dim_B=2 + external η_1 parameter. Kamin uses explicit no-det outcome in Bob POVM (dim_B≥3)
4. **λ_EC estimation**: My impl uses `f_EC = 1.16 · h(qber)`. Kamin may use smooth max-entropy tighter EC estimate
5. **γ optimization algorithm**: My impl uses grid search. Kamin uses Frank-Wolfe iterative optimization

Each of 1-5 contributes to the gap. Fully closing to < 5% requires addressing all five.

[Kamin-2025.md §9.3 ADR-B recommendation](../literature/Kamin-2025.md) (written 2026-04-20):

> 推荐：Phase 1 S2.5 采用 Stage 1 + Stage 2 缩减版作为硬验收 proxy；Stage 3 decoy 留到 Phase 2 Sub-Q3 与上界对比时合并实施

Stage 1/2 = qubit BB84 Fig.1; Stage 3 = decoy Fig.3 (the hard one).

---

## Decision options

### Option A — Full attack on Fig.3 now (reject ADR)

**Action**: Implement WL22 beamsplitter model + dark count + dim_B=3 + Frank-Wolfe γ opt + smooth max-entropy EC. Target Fig.3 < 5% tolerance directly.

**Effort estimate**: 3-5 weeks (per [Kamin-2025.md §9.2 Stage 3](../literature/Kamin-2025.md))

**Pros**:
- Directly satisfies user 3b sign-off literal wording
- Cleanly closes S2.5 hard acceptance criterion
- Provides rigorous decoy baseline for Sub-Q3 gap analysis

**Cons**:
- Very long autonomous run (3-5 weeks) without user feedback
- High risk of error accumulation in complex numerical implementation
- May conflict with other plan items (T1.x Round 3/4/5 if Werner review keeps FAILing)

### Option B — Split T2 (proposed)

**Action**:
- **T2-Phase A**: Kamin qubit Fig.1 < 5% tolerance (simpler implementation, current code close)
  - Scope: §6 qubit BB84 with loss + depolarizing noise (§6.3 benchmark); n ∈ {10^6, 10^8, 10^10, 10^12}; loss sweep 0-25 dB
  - Current state: cutoff 32 dB vs Kamin 26 dB at n=10^12 (±6 dB, user 2a signed off as accepted); **positive-rate region** within ±15% per `kamin_fig1_report.md`
  - **Achievable fix**: tighten λ, Frank-Wolfe γ optimization; target all (n, loss) points within 5%
  - Effort: 1-2 weeks
- **T2-Phase B**: Kamin decoy Fig.3 < 5% tolerance (deferred to Phase 2 Sub-Q3 work)
  - Scope: full WL22 beamsplitter + dark count + dim_B=3 + Frank-Wolfe
  - Effort: 3-5 weeks
  - Rationale: per Kamin-2025.md §9.3, decoy layer is intrinsically more complex; better combined with Phase 2 Sub-Q3 upper-bound comparison work

**Pros**:
- T2-Phase A achievable within one autonomous session; closes a piece of S2.5 硬验收
- T2-Phase B defer is well-documented; picks up naturally when Sub-Q3 wants numerical decoy baseline
- Reduces risk of long-running error-prone implementation without user review
- Aligns with RESEARCH_PLAN §5 Sub-Q4 (gap analysis) dependency — Sub-Q4 needs upper bound + lower bound, lower bound via decoy comes in Phase 2 anyway

**Cons**:
- Does not literally satisfy user 3b sign-off "Fig.3 < 5% tolerance" in current session
- May require re-review when user returns (to ratify split)

### Option C — Preserve status quo + explicit scope doc (reject both)

**Action**: Do not attempt < 5% reproduction. Document current offsets as known scope limitations (like user 2a for Fig.1 cutoff).

**Pros**: No further work; minimal risk

**Cons**:
- Directly contradicts user 3b sign-off which explicitly requested < 5%
- Leaves RESEARCH_PLAN §3.3 S2.5 硬验收 permanently open

---

## Proposed decision

**Option B (split)** — because:
1. Aligns with [Kamin-2025.md §9.3](../literature/Kamin-2025.md) pre-existing recommendation
2. Phase A is achievable within this autonomous session
3. Phase B defer is principled (synergy with Phase 2 Sub-Q3 work)
4. If user disagrees upon return, Phase B can be re-prioritized; no information lost
5. Option A risk profile (3-5 weeks alone without feedback) is worse for project
6. Option C contradicts user signed-off requirement

## Consequences if accepted (Option B)

- T2 in [AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md](../AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md) splits to T2-A and T2-B
- T2-A work estimate: 1-2 weeks
- T2-B deferred to Phase 2 Sub-Q3 work stream (trigger: Sub-Q3 requires tight decoy lower bound)
- S2.5 硬验收 partial-closed (qubit Fig.1 closed; decoy Fig.3 explicitly deferred)
- New literature memo update: `Kamin-2025.md §9.3` status 从 "recommendation" → "adopted via ADR 0001"

## Consequences if rejected (Option A or C)

- If Option A: commit to 3-5 week implementation
- If Option C: mark S2.5 as "partially closed with permanent scope" and proceed

## Binding process

Per 2026-04-21 user delegation:
1. Two-Codex (diff reviewer + holistic reviewer) independently assess this ADR
2. If both PASS + verdict 一致 (e.g., both recommend Option B or both reject) → binding process decision
3. If Codex verdict 不一致 → ADR stays Proposed, escalate to user upon return
4. ADR binding **only at process level**; does not constitute R0.2 C2 upgrade

## Review record

**2026-04-22 Codex proxy verdicts** (both PASS + Option B, BINDING):

- [Agent 1 diff review (xhigh)](../workflow/adr-0001-proxy/review-diff-1.json): `PASS` / Option B
  - "Option B should be accepted as the binding process decision. It is consistent with the pre-existing staged recommendation in Kamin-2025.md §9.3 … Deferring Phase B does not create a unique downstream Sub-Q4 blocker that Option A would remove."
  - MINOR: ADR overstates compliance by saying "partial-closed"; should be "proxy milestone"
- [Agent 2 holistic review (high)](../workflow/adr-0001-proxy/review-holistic-1.md): `PASS` / Option B / BINDING = yes
  - "Adopt the split as the process decision, with one required correction: T2-Phase A must be labeled a proxy milestone only, and S2.5 / user 3b must remain open until Phase B completes."

## Proxy corrections applied (2026-04-22)

1. ~~"T2-Phase A partial-closes S2.5"~~ → **T2-Phase A is a proxy milestone only; does NOT close S2.5 or user 3b**
2. ~~"Sub-Q4 gap attribution 需要 decoy finite-key baseline, Option A 独立 unlock"~~ → Phase B decoy Fig.3 useful calibration for later Sub-Q3 comparison work, **not** a uniquely Sub-Q4-blocking dependency (Sub-Q4 formally consumes Sub-Q2 lower bounds + Sub-Q3 upper bounds per RESEARCH_PLAN §5)
3. Phase A / B 工期估计 1-2 / 3-5 weeks 基于当前 `kamin_decoy_sdp.py` 实现审计结果（WL22 modeling + dark counts + explicit loss + Frank-Wolfe），取代 AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md 早期 "3-5 天" 的 placeholder 估计

## Downstream effect (post-acceptance)

- **S2.5 硬验收状态**：**OPEN** (unchanged); 用户 3b **OPEN**
- **T2-Phase A**：autonomous session 可执行；目标 qubit Fig.1 < 5%；**proxy milestone**
- **T2-Phase B**：defer 至 Phase 2 Sub-Q3 comparison work；trigger = user 指示 or Sub-Q3 需要精确 decoy baseline
- [AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md](../AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md) 需相应更新 T2 section

---

## Changelog

- **v1.1** (2026-04-22 autonomous session, **Accepted**): Codex proxy binding PASS; required corrections applied per Agent 2 recommendation
- **v1.0** (2026-04-22): Proposed
