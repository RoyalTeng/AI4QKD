No blocking findings. I would mark Round 3 as PASS on all five dimensions.

1. `METHODOLOGY`: PASS. `docs/findings/s2.3_device_imperfections.md` now states the comparison correctly as per-profile `μ`-optimized with `ν = 0.2·μ`, and `tests/test_sweeps/test_decoy_bb84_sweep.py` anchors that exact scope with `nu_ratio=0.2`.
2. `FINDING STRENGTH`: PASS. The mechanism split is coherent and matches the archived numbers: `η_d=0.5` alone gives about `50.7%` degradation at 25 km, while adding `e_d=0.033` moves it to about `84.24%`; dark count remains negligible through 100 km.
3. `LIMITATIONS`: PASS. `docs/findings/s2.3_device_imperfections.md` §5 now includes limitation `#9 Basis bias 未建模`, explicitly calling out the missing plan input and its current non-implementation status.
4. `PLAN ALIGNMENT`: PASS. The JSON archive contains the full sweep: `docs/findings/s2.3_device_imperfections_r2.json` stores `n_points = 1221`, and `full_1000pt_sweep_TYPICAL_S23.full_records` has length `1221`. Note: `full_records` is nested, not top-level.
5. `SCOPE DISCIPLINE`: PASS. `docs/PHASE1_LOG.md` §3.5.2 is now framed as removal of overreaching scope-rewrite language, not as a live recommendation to rewrite the plan. The remaining mention in §3.5.1 reads as historical record, not current prescription.

Summary: Round 2’s two blockers are closed. The delivery now reads methodologically correct, evidentially stronger, limitation-complete, plan-aligned, and scope-disciplined.