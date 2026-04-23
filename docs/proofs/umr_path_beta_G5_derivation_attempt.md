# umr path β.G5 — adversarial comb → fixed channel reduction attempt

**版本**: v0.1 **[CONJ-DRAFT]** — AI autonomous (2026-04-23, user 授权 draft+Codex iterate)
**对应 gap**: β.G5 (见 [umr_path_beta_derivation.md](umr_path_beta_derivation.md) §2.5 + [umr_path_beta_v0_4_detailed_draft.md](umr_path_beta_v0_4_detailed_draft.md) §6)
**目标**: Establish reduction from n-shot adversarial umr comb → repeated use of fixed effective channel $\tilde{\mathcal{M}}$

---

## 0. 严谨性

- **[CONJ-DRAFT]** throughout
- 无 silent upgrade; 无 combined chain
- Citations: 5 级 taxonomy
- "attempted direction"
- **警惕**: β v0.4-R1 曾 misapply Khatri-Wilde Prop 19.2 to adversarial comb — 本 draft 严格避免

---

## 1. 问题陈述

### 1.1 Setup

umr n-shot protocol $\Pi$:
- 每轮 Alice, Bob 独立准备 source states
- $\mathcal{E}_1, \mathcal{E}_2$ 作用
- Charlie 对 $(\hat{A}_i, \hat{B}_i)$ 做 BSM $M_i$ (may be **adaptive** based on prior round outcomes $c_1, ..., c_{i-1}$)
- Broadcast $c_i$
- Alice-Bob 做 LOCC post-processing across all $n$ rounds

Charlie 的 **adaptive strategy**: $M_i = M_i(c_1, ..., c_{i-1})$ 是函数 of prior broadcast history.

### 1.2 Target inequality

希望 establish:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi, n) \leq R_\varepsilon^{\mathcal{A}_\text{umr, fixed}}(\Pi', n)$$

其中 $\Pi'$ 是 Alice-Bob 在 n 次**固定** $\tilde{\mathcal{M}}$ 上的 protocol (Charlie per-round BSM 相同, non-adaptive).

**理由**: 若成立, β.G3 numerical 仅需算 single-shot $E_R(\tilde{\mathcal{M}})$; amortized bound 给 $n \cdot E_R(\tilde{\mathcal{M}})$.

---

## 2. Attempted approaches

### 2.1 Approach A — Khatri-Wilde Prop 19.2 direct apply

**Attempt**: Apply Prop 19.2 to $\tilde{\mathcal{M}}$ as if it's "fixed channel used n times".

**Why this fails** (Codex R1 β v0.4-R1 已 identify):
- [MEMO-LEVEL QUOTE via KhatriWilde-2020.md §2.1]: Prop 19.2 条件是 "(n, M, ε) LOCC-assisted quantum communication protocol over channel $\mathcal{N}_{A\to B}$"
- **Scope**: protocol 是在 **fixed** $\mathcal{N}$ 上 n 次 use. umr 的 Charlie adaptive 意味着**每轮 channel 形式不同** (因为 Charlie BSM depends on prior $c$ history)
- 所以 $\tilde{\mathcal{M}}_i \neq \tilde{\mathcal{M}}$ 一般; the "n-shot protocol on fixed channel" assumption 不满足

**Conclusion**: Approach A **fails** — 直接 apply Prop 19.2 对 adversarial umr comb 是 scope 越界.

### 2.2 Approach B — Teleportation stretching [Pirandola 2017]

**Idea**: Pirandola 2017 (PLOB) 的 teleportation stretching 技术把 adaptive LOCC protocol 通过 resource state + teleportation simulation 转换为 non-adaptive form.

**Why this may not directly apply**:
- Teleportation stretching 假设 **cooperative 3-party**: sender + receiver + channel environment (Eve purification)
- umr 的 Charlie 是**独立 third party** 且 adversarial; 不是 "channel environment"
- Teleportation stretching 的 core lemma 假设 resource state $\omega_{AB}$ is **Choi of the channel**; 若 Charlie BSM 可变, resource state per round 不一 — teleportation stretching 不直接 apply

**Partial**: 若 Charlie BSM **fixed**, teleportation stretching gives standard result. 但那正是 we want to derive, 不是 assumption.

**Conclusion**: Approach B 面 circularity — teleportation stretching assumes the reduction already done.

### 2.3 Approach C — Kamin 2025 GEAT entropy accumulation

**Idea**: GEAT (Dupuis-Fawzi-Renner + Metger) bounds smooth min-entropy for n-shot adaptive quantum protocol via per-round conditional entropy.

**What GEAT handles [RECALLED]**:
- i.i.d. channel with adaptive LOCC — handled well (original EAT / GEAT design)
- Infrequent sampling tests + parameter estimation — handled
- **Adversarial third party with arbitrary per-round strategy** — 不 obviously covered

**Specific concern for umr**:
- GEAT 的 "channel" 是 fixed per round (可能 depends on classical info but 是 deterministic function)
- umr Charlie 是 **active adversary** — 每轮 choice of $M_i$ 是 Eve's decision, 不是 channel's deterministic output
- 可能需要把 Charlie 看作 Eve 的 extra register + GEAT apply 到 extended channel

**Conclusion**: Approach C **可能 viable** but requires **non-trivial adaptation**. User research-level work needed — check if Kamin 2025 / Metger 2024 GEAT 的 "channel" 可以 cover adversarial Charlie, or if extension lemma needed.

### 2.4 Approach D — Purify Charlie into Eve, view as adversarial channel with full Eve register

**Idea**: Purify Charlie's adaptive strategy into Eve's memory register. Then each round Alice-Bob see a "fixed-form" channel (Alice-Bob source → $\mathcal{E}_1, \mathcal{E}_2$ → Eve register → broadcast) where Eve pre-computes all strategies at round 1.

**Why this attempts to work**:
- All adaptive randomness absorbed into Eve's state at time 0
- Each round's channel 看 Alice-Bob 来说 is functionally one of $\tilde{\mathcal{M}}_{\sigma_\text{Eve}}(i)$ indexed by Eve's strategy encoding
- Alice-Bob的**rate 受 worst-case Eve strategy 约束** — 即 max over all encodings

**Issue**: 即便 purify Eve 可 collapse adaptivity 到 initial state, **Eve 仍可 choose strategy to minimize Alice-Bob rate**. "Worst-case" 不是 "fixed channel" in the amortized sense; amortized framework 要求 channel **每轮相同**.

**Partial progress**: 可能 reduce to "worst-case single-round $\tilde{\mathcal{M}}$ over Eve strategies" — $\sup_\Pi R \leq \sup_M E_R(\tilde{\mathcal{M}}_M)$ where $\tilde{\mathcal{M}}_M$ is Charlie BSM choice $M$. But this 不是 "fixed channel amortization".

**Conclusion**: Approach D 提供 **conservative bound** (worst-case single-round) without proper amortization. 不 give standard $n \cdot E_R$ form.

---

## 3. Summary — β.G5 honest status

All 4 approaches 遇到 unique obstacle:
- A: Prop 19.2 scope 不 cover adversarial comb
- B: Teleportation stretching circular / assume result
- C: GEAT may not cover adversarial Charlie (user PDF check needed)
- D: Worst-case collapse doesn't give standard amortization

**β.G5 remains OPEN**. 最有希望的 path: **Approach C (GEAT adaptation)** — 用户直读 Kamin 2025 / Metger 2024 PDF 看 framework 是否可扩展 umr adversary class.

### 3.1 Relation to α / γ paths

- **α path** 也需 amortization argument 把 monotonicity chain 累积 n 次 — 同样面 adversarial Charlie 问题
- **γ path** 是 single-edge + DPI approach; 不 依赖 channel reduction, 所以 γ path **不受 β.G5 阻塞**
- 意味着: **γ path 在 "adversarial comb reduction" 这点上比 β 优** (若 γ 的 γ.B chain 某天 closed)

### 3.2 Q1 decision impact — partial re-evaluation

原 Q1 Option 2 (β main + γ safety) rationale 包括 "β 可能给更紧 bound". 但 β.G4 + β.G5 两个 MAJOR structural blocker now both **concretely documented as unclosed**:
- β.G4: Eve model transfer — no simulation map found
- β.G5: adversarial comb reduction — Prop 19.2 scope 不 cover

**这 suggest** β path 形式化工作比 γ path **更 difficult** (γ 有 γ.B.G1 structural doubt, but γ.A PLOB single-edge 的 covariant case 是 standard). 

**Agnostic**: 不 shift Q1 decision; 仅 flag β formal path effort estimate **可能需 upward revise** (original β v0.3 §7 10-15 天 probably underestimate given β.G4 + β.G5 both structural).

---

## 4. Changelog

- **v0.1** (2026-04-23, user 授权 draft+Codex iterate): 4 approaches (Prop 19.2, Teleportation stretching, GEAT adaptation, Purify Eve worst-case) all fail with different obstacles. β.G5 remains OPEN. Kamin 2025 GEAT most promising path per Approach C.
