# C1(a) Point 6 Retest — Codex (gpt-5.4) — Khatri-Wilde Ch 20 §20.2

> Codex CLI sandbox 误报 "filesystem read-only" 但 `-o` 仍正确写入；disclaimer 已 strip。

**Date**: 2026-04-26  
**Reviewer**: Codex (independent)  
**PDF**: arXiv:2011.04672, PDF pp. 1178-1192 read (printed pp. 1165-1179)  
**Method**: pdftotext extract + textual verify

## Point 6 — Verdict
**UNCERTAIN**

§20.2 does textually establish the SKA ↔ bipartite-private-state-distillation purification equivalence:

> “There is a deep and powerful equivalence between a secret-key-agreement protocol as described above and a protocol that uses LOCC assistance to distill a bipartite private state.” (KW PDF p. 1184; printed p. 1171)

> “The main idea behind this equivalence is to apply the purification principle to a secret-key-agreement protocol and then examine the consequences.” (KW PDF p. 1184; printed p. 1171)

> “Thus, starting with a tripartite secret-key-agreement protocol, we can apply the purification principle, then trace over the systems of the eavesdropper, and the result is a bipartite private-state distillation protocol assisted by LOCC.” (KW PDF p. 1188; printed p. 1175)

> “Alternatively, this reasoning can go in the opposite direction.” (KW PDF p. 1188; printed p. 1175)

So point 6(i) is satisfied textually.

Point 6(ii) is not textually settled by §20.2 alone. KW’s formal setup is still an `n`-round SKA protocol over a single channel `N_{A→B}` plus LOPC/public-separable rounds, while Cui Eq. (1) is an untrusted-relay model in which Eve jointly acts on both Alice and Bob outbound systems and a message register. That mapping is plausible, but it is not supplied explicitly in §20.2. Therefore the overall point remains **UNCERTAIN**, not `PASS`.

## Cui Eve Model Coverage Check
KW clearly covers an Eve with purification/environment access and a public classical register:

> “we suppose that there is a quantum channel `N_{A→B}` connecting the legitimate sender Alice to the legitimate receiver Bob.” (KW PDF p. 1178; printed p. 1165)

> “we suppose that the quantum eavesdropper has access to the environment system `E`.” (KW PDF p. 1178; printed p. 1165)

> “we suppose that the eavesdropper has access to all of the classical data exchanged between the legitimate parties.” (KW PDF p. 1178; printed p. 1165)

> “`Y_i` is a system held by Eve, containing a coherent classical copy of the classical data exchanged in this round.” (KW PDF p. 1185; printed p. 1172)

This matches the Eve-ancilla plus classical-message part of Cui Eq. (1). But §20.2 does **not** explicitly show that Cui’s relay attack
`Û |n>_{A-out}|m>_{B-out}|E_0>_{Ea}|0>_M -> ...`
is already inside KW’s single-channel `N_{A→B}` template. Section 20.2.4 only generalizes to public separable channels, not to an arbitrary joint untrusted-relay unitary on both outbound quantum modes. So Cui coverage needs an extra embedding/reduction argument beyond KW §20.2.

## Aggregate Update for Point 6
The earlier `UNCERTAIN` caused by the missing KW PDF is narrowed but not upgraded to `PASS` or `FAIL`.

New status: KW Ch. 20 §20.2 now confirms the purification-based SKA ↔ private-state-distillation equivalence itself, but applicability to the Cui 2019 Eve model remains non-textual and still requires additional formal reasoning. This does **not** close any path α sub-gap and does **not** upgrade any `[SYN]`.