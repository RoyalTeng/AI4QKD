§A

Pirandola 2019 main-paper Eq. 11 is not the `-\log_2(1-\sqrt{\eta_{AB}})` formula. The exact Eq. 11 is
\[
C(\mathcal N)\le \min_C E_R(C),
\]
with Eq. 10 defining
\[
E_R(C):=\max_{(x,y)\in \tilde C} E_R(\sigma_{xy}).
\]
(main PDF p. 4)

Its claim is: the single-path/sequential end-to-end capacity of a quantum network is upper-bounded by the minimum REE flow across Alice-Bob cuts. The main paper sends the proof to Methods plus Supplementary Note 4; the explicit theorem is Theorem 6, which proves the same formula as supplementary Eq. (152) (Supp. PDF p. 27).

Proof stack:
- General weak-converse/private-state bound in Methods, Eqs. (35)-(41) (main PDF pp. 7-8).
- Network simulation and stretching (Methods pp. 8-9; Supp. Note 3, pp. 24-26).
- Network stretching with cuts, Lemma 5 / Eq. (149) (Supp. PDF p. 26).
- REE monotonicity under LOCC and subadditivity over tensor products (Supp. PDF p. 27).

The `-\log_2(1-\sqrt{\eta_{AB}})` form appears only after extra specialization:
- lossy chain formula Eq. (8), or equidistant fixed-total-loss formula Eq. (9) (main PDF p. 3);
- for `N=1`, Eq. (9) gives `-\log_2(1-\sqrt{\eta})`.

§B

Assumptions actually used for Eq. 11 / its derivation:

- Protocol class: adaptive chain/network protocols where all points perform adaptive local operations with unlimited two-way classical communication (Supp. Note 1, PDF p. 15; Supp. Note 2, PDF pp. 20-21).
- Trusted-relay-only? No. SI Note 1 gives a general adaptive chain protocol class; the paper’s discussion says the upper bounds are broader and also cover networks with untrusted nodes (main PDF p. 7). So “trusted relay” is not the sharp paper-side restriction.
- Memoryless channels: explicit at network level in Supp. Note 2 (“memoryless quantum channels”), PDF p. 20. Methods p. 7 says a chain can be treated as a single-route network.
- Adaptive LOs at each node: yes (Supp. PDF p. 15; p. 21).
- Two-way CC: yes (Supp. PDF p. 15; p. 21).
- Pure-loss bosonic / teleportation-covariant? Not required for Eq. 11 itself. Eq. 11 is stated for an arbitrary network with a resource-state simulation (Supp. PDF p. 27; Methods p. 8).
- Tele-covariance is only needed for the Choi-state specialization of the bound (main PDF p. 2; Supp. PDF pp. 26-27).
- Distillability is needed to turn the upper bound into the exact single-path capacity formulas used later (main PDF p. 4 Eq. 12-15; Supp. PDF pp. 29-30).
- Pure-loss bosonic edges fit that specialization: bosonic Gaussian channels are in the teleportation-covariant family (main PDF p. 2), and the lossy channel is a phase-insensitive Gaussian channel (main PDF p. 6), so this is a justified inference.
- Asymptotic regime: yes. Capacities are weak-converse asymptotic limits `n→∞, ε→0` (Supp. PDF p. 15 Eq. 91; p. 21 Eq. 125; Methods p. 8 Eq. 40-41).
- `ε`-close private-state criterion: yes (Supp. PDF p. 15; Methods p. 8).
- REE framework: yes. Methods are presented for a generic entanglement measure `E_M`, then specialized to REE; Eq. 11 itself is the REE version (Methods pp. 7-10; Supp. PDF p. 27).
- Bosonic technicality: for bosonic channels, simulations and REE are asymptotic, using approximating Choi/resource states and energy-constrained diamond convergence (main PDF p. 2; Methods pp. 8-9; Supp. PDF p. 27).

§C

Per [path_alpha_l1g2_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l1g2_closure_v0_1.md>) and [path_alpha_subgap_closure_integration_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_subgap_closure_integration_v0_1.md>) §3.2, `ι(Π)` is only a structural embedding into an honest A-C-B relay topology; Eq. 11 applicability was left open.

Compatibility check:

- Chain/network shape: yes. `ι(Π)` is a 3-point A-C-B topology, i.e. a single-route network / `N=1` chain, which matches Pirandola’s framework (Supp. PDF pp. 15, 20-21).
- Edge memorylessness: compatible if the A-C and B-C links are modeled as standard iid pure-loss bosonic channels. Pirandola’s theorem needs that at the network level (Supp. PDF p. 20).
- Edge teleportation-covariance: yes under the pure-loss bosonic reading, by the p. 2 + p. 6 inference above.
- Honest Charlie operation: compatible in principle. Pirandola’s repeater/node model gives Charlie a local register and local operations, so a joint interference/detection map on the two incoming modes can be represented as a local operation after both systems reach Charlie (Supp. PDF p. 15; p. 26).
- Per-trial accounting: this is the delicate point. A Cui trial uses one A→C transmission and one B→C transmission, plus Charlie’s announcement (Cui PDF p. 2). Pirandola’s chain/network use similarly consumes the route edges within one end-to-end use, but the paper describes that abstractly in LOCC-interleaved/sequential form (Supp. PDF p. 15; p. 24). So there is a plausible abstraction match, but it is not yet a fully written operational identification.
- Parameter form: even if `ι(Π)` fits the framework, Eq. 11 alone does not yield `-\log_2(1-\sqrt{\eta_{AB}})`. For a lossy single-route A-C-B network, the immediate quantity is the bottleneck edge transmissivity, i.e. `\min\{\eta_{AC},\eta_{BC}\}` (main PDF p. 3 Eq. 8; Supp. PDF p. 18 Eq. 108; network version pp. 29-30 Eq. 173-176). The `\sqrt{\eta_{AB}}` form needs the extra identification `\eta_{AB}=\eta_{AC}\eta_{BC}` plus symmetric/equidistant splitting.

§D

Remaining OPEN gaps for L3.G3:

- Citation-gap: Eq. 11 is only the REE cut bound. If path α wants the `-\log_2(1-\sqrt{\eta_{AB}})` formula, it still needs the missing specialization chain: Eq. 11 → distillable/pure-loss single-route formulas, or else it should cite the chain/lossy equations directly instead of Eq. 11.
- Parameter-identification gap: the proof must fix whether the relevant Pirandola parameter is `\eta_{\min}`, route transmissivity, or the product `\eta_{AB}=\eta_{AC}\eta_{BC}`. Those are not interchangeable.
- Symmetry/equidistance gap: the `\sqrt{\eta_{AB}}` expression requires a symmetric/equidistant split of total loss. Without that, the generic bound is `-\log_2(1-\min\{\eta_{AC},\eta_{BC}\})`.
- Channel-use accounting gap: an explicit argument is still needed that one Cui trial is one Pirandola chain use / single-path network use. This is about operational counting only, not about re-opening L3.G2’s key-length bridge.
- Protocol-model gap: the honest Charlie interference/detection step still needs to be written explicitly as a permitted local operation in Pirandola’s Note 1 / Note 2 abstract model, rather than only asserted informally.
- Edge-model gap: the path-α application still needs an explicit statement that the A-C and B-C links in `ι(Π)` are fixed memoryless pure-loss bosonic channels across trials. Once that is fixed, tele-covariance is fine; the missing part is the explicit instantiation.

§E

Scope checks:

- I did not use this round to close L2.G3; Eve-set-across-spaces remains separate.
- I did not use this round to reopen or smuggle L3.G2; the only rate-related issue kept here is channel-use accounting for Eq. 11 units.
- I am not claiming L3.G3 is closed.
- I am not recommending that AI close L3.G3.
- This is consistent with the integration report’s §3.2 instruction that L3.G3 remains open pending separate verification.

L3.G3 STATUS AFTER THIS ROUND: still OPEN. Gaps identified above must be addressed by separate verification, NOT by AI draft.