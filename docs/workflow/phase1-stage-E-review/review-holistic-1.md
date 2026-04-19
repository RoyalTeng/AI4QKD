**Findings**

- High: Eq. 19 is misquoted at [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:184>). The paper’s Eq. (19) includes the EC leakage term `-log2(2/εEC)` in addition to `-2log2(2/εPA)`. As written, the memo slightly overstates the BB84 finite-key length.

- Medium: Theorem 4 is too compressed at [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:152>). The paper’s statement is not just the reliability inequality `α ≥ β - ζ`; it also includes conditions on the smoothing parameter and the limiting tightness claim `(A16)` as numerical imprecision goes to zero. So the memo captures the idea, but not the actual theorem statement.

- Medium: §3 is close to Level 3, but not quite reproducible yet. The missing bridge is the explicit construction of the finite-key feasible set `S_μ` / `S_μ^PM` from accepted statistics and source-replacement certainty constraints (paper Eq. 1, Eq. 12, and the unique-acceptance simplification before Eq. 19). Without that step, a researcher sees the endpoint SDP but not the exact asymptotic-to-finite-key transition.

- Medium: Scope discipline is mostly good, but a few phrases overreach: [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:18>), [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:24>), [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:233>), [GLL-2021.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GLL-2021.md:240>). “直接前置”, “共享 Renner 框架”, and “诱骗 phase-randomized” are stronger than the paper supports. GLL is a Renner/i.i.d. finite-key SDP method; GEAT/Kamin are related but distinct machinery. §5.3 is also more project speculation than paper bearing.

**Verdict**

Fidelity is mostly strong: Eq. 3, 4, 5, and the spirit of Eq. 14 are accurate; Eq. 19 needs correction. Template consistency is good: the memo has the expected summary, concept map, bearing, limitations, and next-level sections. The main upgrades needed are one formula fix, a more faithful Theorem 4 summary, and one short subsection explaining how WLC’s exact constraint set becomes GLL’s finite-key feasible set.