**STRATEGIC_FIT**

Option B is the best process choice under the current autonomous-run constraint, but only as a staging decision, not as a standards change. The authoritative hard acceptance for `S2.5` is still decoy Fig.3 `< 5%` reproduction in [RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:301>), while the pre-existing literature memo already recommends a staged proxy because decoy Stage 3 is materially harder than qubit Fig.1 Stage 1/2 in [Kamin-2025.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/Kamin-2025.md:316>). For the project’s end goal, avoiding a long, fragile numerical detour is more important than forcing literal closure of this one benchmark in one unattended session.

**USER-INTENT_FIDELITY**

User decision `3b` on 2026-04-21 was literal: reproduce Fig.3 within `< 5%`, as recorded in [AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/AUTONOMOUS_RESEARCH_PLAN_2026-04-21.md:11>). The split is acceptable only because the user explicitly delegated process decisions that same day. It is not acceptable to claim that Phase A satisfies `3b` or closes `S2.5`; Phase A can only be a proxy milestone. If the ADR keeps “partial-closed” language, it overstates fidelity to user intent.

**AUTONOMOUS_RISK**

Option A is materially higher risk. The documented gap is not one missing tweak; it spans honest-model mismatch, missing dark counts, Bob no-detection handling / effective dimension mismatch, EC leakage modeling, and `γ` optimization method in [0001-kamin-fig3-tolerance-split.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/adr/0001-kamin-fig3-tolerance-split.md:20>) and [kamin_decoy_sdp.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/kamin_decoy_sdp.py:24>). That is a multi-axis rewrite, not a short debug loop. By contrast, qubit Fig.1 is already partially validated, with the main open issue explicitly separated from Fig.3 in [kamin_fig1_report.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/research/kamin_fig1_report.md:66>). I therefore treat Option A’s “3-5 weeks” as plausible and the earlier 2026-04-21 “3-5 days” placeholder as obsolete.

**PHASE-2_SYNERGY**

The synergy claim is real, but overstated. Real: decoy Fig.3 work does share machinery with later finite-key lower-bound benchmarking and with eventual lower-vs-upper-bound comparisons. Overstated: `Sub-Q3` in the plan is explicitly upper-bound work, and `Sub-Q4` formally consumes `Sub-Q2` lower bounds plus `Sub-Q3` upper bounds, per [RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:399>). So Fig.3 reproduction is useful calibration, not a formal prerequisite that only Option A unlocks.

**OPPORTUNITY_COST**

Choosing Option B costs immediate closure of the original `S2.5` hard acceptance, delays a rigorous decoy GEAT baseline, and may require wording re-ratification when the user returns. Choosing Option A would, if successful, give a cleaner Phase 1 endpoint and stronger early confidence for later comparison work. But on a probability-adjusted basis, A costs more: it can consume weeks, crowd out other signed work, and still miss `< 5%`. Option C is not viable because it directly conflicts with the user’s 2026-04-21 signoff.

**VERDICT**

PASS

**RECOMMENDATION**

Option B.

Adopt the split as the process decision, with one required correction: T2-Phase A must be labeled a proxy milestone only, and `S2.5` / user `3b` must remain open until Phase B completes.

**BINDING**

yes

This PASS is consistent with Agent 1’s PASS recommending Option B in [review-diff-1.json](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/workflow/adr-0001-proxy/review-diff-1.json>).