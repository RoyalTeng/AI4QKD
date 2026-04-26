# Paper Draft Skeleton — Path α Scaling Bound for Untrusted-Measurement-Relay TF-QKD (v0.1)

> **🟡 [SYN]/[DRAFT skeleton — Lemma proofs OPEN; not for external citation]**
>
> **All claims conditional on 11 sub-gaps closure** per [path α scaffolding v0.1](umr_path_alpha_scaffolding.md) §5.
>
> **Status**: structure proposal only. **No** proof. **No** numerical scaling tightness claim. **Per [autonomous plan §0](../AUTONOMOUS_PLAN_2026-04-25.md)** boundary.
>
> **Verification path**: any external citation requires R0.2 (C1 ∧ C2 ∧ C3) full process.

---

## Abstract (DRAFT)

**Working text** (highly conditional, [SYN]):

> "We establish a conditional secret-key-rate upper bound for twin-field quantum key distribution (TF-QKD) protocols with untrusted measurement relay (umr). Specifically, **assuming** the closure of certain technical structural sub-gaps (Lemma A protocol embedding, Lemma B security reduction, Lemma C rate alignment), we show that any TF-QKD protocol whose security has been established against fully adversarial relay (e.g., Cui-Yin-Wang-Chen-Wang-Guo-Han 2019) admits the upper bound $K_{umr} \leq -\log_2(1-\sqrt{\eta_{AB}})$, derived via reduction to Pirandola 2019 trusted-relay chain capacity. Numerical reproduction of the simplified TF-QKD protocol of Cui et al. is consistent with this scaling at the order of $\sim 30\times$ prefactor offset on a finite grid. We discuss the scope, limitations, and the verification work required to upgrade these results."

---

## §1 Introduction

### 1.1 Background

Quantum key distribution (QKD) [BB84, Ekert] aims at information-theoretic secure key sharing.
Among QKD families, twin-field QKD [Lucamarini 2018, Wang 2018, Ma 2018, Cui 2019] is significant because:
- It uses an untrusted measurement relay (Charlie potentially controlled by Eve)
- It achieves $\sqrt{\eta}$ scaling, surpassing the point-to-point Pirandola-Laurenza-Ottaviani-Banchi (PLOB) bound [Pirandola 2017]

For **point-to-point** quantum communication, the secret key capacity satisfies $K \leq -\log_2(1-\eta)$ [PLOB 2017]. For repeater chains and quantum networks, Pirandola 2019 [Pirandola-2019] generalizes to single-letter REE bounds.

A natural question arises: **what is the secret key capacity in the umr setting?**

### 1.2 Status of the question

Pirandola 2019 [Discussion p.7] **claims** (without independent formal proof in the paper) that the bounds also apply to networks with untrusted nodes. Lucamarini 2018, Wang 2018, Ma 2018, and Cui 2019 cite Pirandola's work primarily as a **scaling target**, **not** as a formal converse.

Direct path β/γ approaches that try to extend Pirandola's converse to untrusted relay encounter open structural gaps (Khatri-Wilde §19 LOPC framework reconciliation, amortized comb reduction, DPI in adversarial topology — see [Log 07](../research/07_pirandola_2019_technical_audit.md)).

### 1.3 This work

We propose **path α**: a three-lemma reduction that does **not** require extending Pirandola's untrusted-node treatment. Instead:

1. **Lemma A (Protocol Embedding)**: For any umr-secure TF-QKD protocol $\Pi$, define $\Pi_{tr}$ as the same protocol with Charlie's operations re-declared as protocol-specified (in the trusted-relay protocol class of Pirandola SI Note 1).
2. **Lemma B (Security Reduction)**: Security of $\Pi$ against umr Eve implies security of $\Pi_{tr}$ against trusted-relay Eve (weaker).
3. **Lemma C (Rate Alignment)**: $R_{umr}(\Pi) \leq R_{tr}(\Pi_{tr})$.

If all three lemmas hold (with their 11 sub-gaps closed per [scaffolding v0.1](umr_path_alpha_scaffolding.md)), the chain gives:

$$K_{umr}(\eta_A, \eta_B) \stackrel{Lemmas}{\leq} K_{trusted-chain}(\eta_A, \eta_B) \stackrel{Pirandola \, 2019 \, Eq.(11)}{\leq} -\log_2(1 - \sqrt{\eta_{AB}}).$$

**This work does not close the 11 sub-gaps**. We provide:
- The precise statement of each lemma (statement-only).
- The sub-gap inventory [scaffolding v0.1] retained verbatim.
- Numerical reframing showing consistency with Cui 2019 at finite grid (no scaling tightness asserted).
- A roadmap for verification.

### 1.4 Positioning relative to literature

We do not claim novelty in:
- The **target inequality** $-\log_2(1-\sqrt{\eta})$ — established by Pirandola 2019 in trusted-relay chain.
- The **anchor protocol** Cui 2019 — TF-QKD without phase postselection with full collective + asymptotic coherent attack security.
- The **point-to-point converse tools** — PLOB 2017, TGW 2014, KW Ch 19/20.

The novelty is in the **reduction architecture**: routing umr capacity through trusted-relay capacity via protocol embedding, **avoiding** the need to extend Pirandola's converse to untrusted nodes.

This architecture is **conditional** on the three lemmas, all of which remain OPEN.

---

## §2 Anchor Protocol: Cui-Yin-Wang-Chen-Wang-Guo-Han 2019

### 2.1 Protocol summary

(Refer to Cui 2019 §II for full description.)

### 2.2 Eve model (Cui 2019 Eq. (1))

$$\hat{U}|n\rangle_{A-out}|m\rangle_{B-out}|E_0\rangle_{Ea}|0\rangle_M = \sqrt{Y_{n,m}}|\gamma_{n,m}\rangle_E|1\rangle_M + \sqrt{1-Y_{n,m}}|other\rangle_E|0\rangle_M$$

This is "the most general collective attack" (Cui 2019 page 2). Coherent attack covered asymptotically via de Finetti / postselection (Cui 2019 page 3).

### 2.3 Why Cui 2019 (vs. Lucamarini / Wang / Ma)

- **Lucamarini 2018 original**: not strict (admitted by [18], reproved by Wang 2018 reverse attack). **Excluded**.
- **Wang 2018 SNS-TF**: full security proof with "possibly dishonest Charlie". Acceptable backup.
- **Ma 2018 PM-QKD**: full security proof with "untrusted relay held by Eve". Acceptable backup.
- **Cui 2019**: most explicit umr Eve formalization (Eq. (1)). Selected as primary anchor.

---

## §3 Reduction Architecture (Three-Lemma Scaffold)

(Refer to [Lemma skeletons v0.1](umr_path_alpha_lemma_skeletons_v0_1.md) for precise statement targets and sub-gap inventory.)

### 3.1 Lemma A — Protocol Embedding [DRAFT statement-stub]

**Statement target**: $\Pi_{tr} = \iota(\Pi)$ is a member of Pirandola 2019 SI Note 1 trusted-relay protocol class.

**Sub-gaps**: L1.G1 (Hilbert space alignment), L1.G2 (embedding construction), L1.G3 (Stinespring gauge), L1.G4 (output state metric).

### 3.2 Lemma B — Security Reduction [DRAFT statement-stub]

**Statement target**: $\Pi$ ε-secure under $\mathbb{E}_{Cui}$ ⇒ $\Pi_{tr}$ ε-secure under $\mathbb{E}_{tr} \subseteq \mathbb{E}_{Cui}$.

**Sub-gaps**: L2.G1 (sign direction), L2.G2 (composable ε three-component), L2.G3 (Eve set across spaces), L2.G4 (non-LOCC).

### 3.3 Lemma C — Rate Alignment [DRAFT statement-stub]

**Statement target**: $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ in shared rate convention.

**Sub-gaps**: L3.G1 (LOPC syntax), L3.G2 (key length cross-topology), L3.G3 (Pirandola Eq. 11 application).

### 3.4 Combined chain — CONDITIONAL

If all 11 sub-gaps closed:

$$K_{umr}(\Pi) \leq K_{trusted-chain}(\Pi_{tr}) \leq -\log_2(1-\sqrt{\eta_{AB}})$$

**Status**: [SYN, conditional]. No formal upgrade asserted.

---

## §4 Numerical Reframing

### 4.1 Cui 2019 Fig. 1 reproduction

(See [scripts/reproduce_cui_2019_fig1.py](../../scripts/reproduce_cui_2019_fig1.py) and [data/cui_2019_fig1_reproduction.csv](../research/data/cui_2019_fig1_reproduction.csv).)

Parameters: $p_d = 10^{-11}$, $\eta_d = 0.80$, $f = 1.1$, $e_d = 0$ (per Cui 2019 §IV).

| loss (dB) | Cui rate | path α scaling UB | UB / Cui ratio |
|---|---|---|---|
| 10 | 1.6e-2 | 5.5e-1 | ~34× |
| 20 | 4.8e-3 | 1.5e-1 | ~32× |
| 30 | 1.5e-3 | 4.6e-2 | ~31× |
| 40 | 4.6e-4 | 1.5e-2 | ~32× |
| 50 | 1.5e-4 | 4.6e-3 | ~31× |
| 60 | 4.6e-5 | 1.4e-3 | ~31× |

### 4.2 Observation (strict reframing)

In this finite grid 10-60 dB, the ratio (path α scaling UB) / (Cui rate) is **consistent with a constant prefactor near 30×**, which is consistent with both quantities having the same scaling order. We make **no claim** about scaling tightness in the asymptotic limit.

### 4.3 PLOB UB comparison

In the same grid, Cui rate exceeds PLOB UB ($-\log_2(1-\eta_{AB})$) starting at ~25 dB. This confirms the well-known TF-QKD-beats-PLOB property [Lucamarini 2018, Cui 2019] and motivates the relay-aware bound.

### 4.4 Strict scope

This numerical work is **reframing only**. It is **not** a verification of the conditional chain claim in §3.4. The chain claim depends on closure of 11 sub-gaps, which is open.

---

## §5 Open Sub-gaps and Verification Path

### 5.1 11 sub-gaps (full inventory in [scaffolding v0.1](umr_path_alpha_scaffolding.md) §5)

Lemma A: L1.G1 / L1.G2 / L1.G3 / L1.G4
Lemma B: L2.G1 / L2.G2 / L2.G3 / L2.G4
Lemma C: L3.G1 / L3.G2 / L3.G3

All currently [UNKNOWN].

### 5.2 8 user verification entry points (from [Lemma skeletons v0.1 §7](umr_path_alpha_lemma_skeletons_v0_1.md))

Each maps to specific PDF citations.

### 5.3 R0.2 three-gate upgrade

(C1) Independent validation: cross-family AI / human paper-level / non-AI tool
(C2) User signature
(C3) Dev-reviewer pass

---

## §6 Limitations and Discussion

### 6.1 Scope

- **Asymptotic only**: finite-key extension not in scope.
- **Bosonic loss channel**: per-segment $\eta_A, \eta_B$, end-to-end $\eta_{AB} = \eta_A \eta_B$.
- **Anchor protocol**: Cui 2019 (or Wang 2018 SNS / Ma 2018 PM as alternative).

### 6.2 Honest accounting of what is NOT proven

- 11 sub-gaps OPEN — chain not formally established.
- Numerical 30× ratio is **finite-grid observation**, not scaling tightness.
- Reduction architecture is conditional, not unconditional.

### 6.3 Comparison to alternative paths

- **path β (β.G4 / β.G5)**: targets full $K_{umr}$ direct converse. Stronger result if achieved, but with 4 hard sub-gaps.
- **path γ (γ.B.G1 / γ.G3)**: targets DPI single-edge decomposition. Subject to cross-task transfer trap.
- **path α (this work)**: scaling-level reduction via trusted-relay embedding. Weaker target but clearer route under user time constraint per [PHASE_STATUS §4.5](../PHASE_STATUS.md) directive.

### 6.4 No retraction of prior work

This paper does **not** modify or retract:
- [FINDINGS v2](../research/FINDINGS.md) interim verdict
- [PHASE_STATUS](../PHASE_STATUS.md)
- [RETRACTION.md](../research/RETRACTION.md) prior records

---

## §7 Conclusion (DRAFT, conditional)

**If** the three lemmas of path α are formally established (closing 11 sub-gaps per [scaffolding v0.1](umr_path_alpha_scaffolding.md)), **then** any umr-secure TF-QKD protocol of the Cui 2019 type satisfies the scaling-level bound $K_{umr} \leq -\log_2(1-\sqrt{\eta_{AB}})$. Pending such verification, this work provides the formalized scaffold and identifies precise verification entry points.

**Status**: [SYN, conditional, all 11 sub-gaps OPEN]
**Not for external citation** until R0.2 three-gate process complete.

---

## §8 Changelog

- **v0.1** (2026-04-26): paper draft skeleton initialized per [autonomous plan §1 Phase 3](../AUTONOMOUS_PLAN_2026-04-25.md). Strict [SYN]/[DRAFT] level. No proof. No numerical scaling tightness claim. All 11 sub-gaps OPEN.

---

*END OF v0.1 SKELETON.* No path α sub-gap closure asserted. R0.1/R0.2/R0.3 strictly maintained. Path α v0.3 [USER-APPROVED PRIORITY but NOT C3-passed] status unchanged.
