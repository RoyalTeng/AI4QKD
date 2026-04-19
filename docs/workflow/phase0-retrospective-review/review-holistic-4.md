**Findings**

- Major: M2/Phase 0 closure is still over-claimed in the docs. [RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:165>) keeps M2 hard acceptance as “MDI vs Ma-Razavi 2012 Fig.3”, but [PHASE0_REPORT.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE0_REPORT.md:11>) says all milestones satisfy hard acceptance while the same report defers Fig.3 at [lines 41](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE0_REPORT.md:41>) and [182](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE0_REPORT.md:182>). That is the remaining scope-discipline break.
- Minor: `framework_coverage.md` still mixes current behavior and stale spec. It says current implementation keeps default `scope_tag="covered"` at [line 40](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/framework_coverage.md:40>), but later presents a no-default + `implementation_status` spec at [line 155](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/framework_coverage.md:155>); actual code matches the former, not the latter ([base.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/protocol/base.py:110>)).

**Verdict**

- Scope discipline across docs: `FAIL` due to the unresolved M2/Phase 0 acceptance mismatch; otherwise mostly aligned after `20f9029`, `b5b34c9`, `ec1f3cb`, `48333f8`.
- `out_of_scope` hard gate: `PASS`. `wlc_key_rate()` hard-blocks at [wlc.py:115](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/wlc.py:115>), and scope tests cover rejection.
- WLC regularization: `PASS`. MOSEK path now uses the correct convex combination `(1-ε)G(ρ)+ετ` at [wlc.py:180](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/wlc.py:180>).
- MDI virtual-EB formulation: `PASS WITH CAVEAT`. As an explicitly `partial`, ideal-symmetric shortcut it is coherent; not a full explicit Charlie-POVM/multi-source MS-EB realization. Direct run at `qber=0.05` gave `R=0.1068015214`, residual `~9e-15`.

`pytest` could not run in this sandbox because no writable temp dir was available; verdict is from code/doc inspection plus direct Python evaluation.