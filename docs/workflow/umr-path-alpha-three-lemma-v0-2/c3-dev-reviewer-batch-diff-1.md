1. PASS — L1.G1
- A-F: A pass; B pass (`[SYN candidate]`, `C2/C3` still pending); C pass; D pass (no L1.G2/G3/G4 smuggling); E pass; F pass.

2. PASS — L1.G2
- A-F: A pass; B pass; C pass; D pass (`§3.5` keeps `L2.G3 / L3.G3` separate); E pass; F pass.

3. PASS — L1.G3
- A-F: A pass; B pass; C pass; D pass (path-α application is kept conditional on `L1.G1 / L1.G2 / L2.G3`); E pass (dimensional-ordering fix retained); F pass.

4. REJECTED — L1.G4
- [§-1](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:22>) says `"本文档仅 close L1.G4"` and other gaps remain pending, but [§1.2](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:47>) then asserts `"ρ^{Π_tr}_{ABE'} = Tr_C(ρ^{Π}_{ABCE})"` and `"if Π is ε-secure ... then Π_tr = ι(Π) is also ε-secure"`.
- [§1.3](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:59>) simultaneously says `"不主张 Π → Π_tr 嵌入 ι 的合法性"` and `"不主张 trusted-relay Eve 仅控 H_E"`; the derivation relies on exactly those assumptions. This is scope drift and adjacent-gap smuggling.
- A-F: A fail; B pass; C fail; D fail; E pass on the `Theorem 6.3 / Ch 6` correction; F pass.

5. PASS — L2.G1
- A-F: A pass; B pass; C pass; D pass (`P1/P2` stay explicit `[UNKNOWN]`; only the sign is closed); E pass; F pass.

6. PASS — L2.G2
- A-F: A pass; B pass; C pass; D pass (no concrete `Π / Π_tr` ε-bound claim); E pass on the main `Theorem 2` 2-additive correction; F pass.

7. PASS — L2.G4
- A-F: A pass; B pass; C pass; D pass (finite-key coherent security remains explicitly out of scope); E pass; F pass.

8. PASS — L3.G1
- A-F: A pass; B pass; C pass; D pass (stays at syntactic compatibility; no rate-equivalence claim); E pass; F pass.

9. FAIL — L3.G2
- [§2.3](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2_closure_v0_1.md:81>) correctly says the Pirandola support is the unnumbered condition `"紧邻 Eq. (35) 之前"`, but [§4](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2_closure_v0_1.md:118>) still asks Codex to verify `"Pirandola 2019 PDF Methods Eq. (8) — ε-close-to-private-state form"`.
- That means the cited round-2/round-3 correction is not fully retained in the live text.
- A-F: A pass; B pass; C pass; D pass; E fail; F pass.

Overall batch verdict: REJECTED.