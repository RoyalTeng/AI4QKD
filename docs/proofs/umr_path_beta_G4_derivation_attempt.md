# umr path β.G4 — Eve model transfer derivation attempt

**版本**: v0.1 **[CONJ-DRAFT]** — AI autonomous (2026-04-22 late, user 授权 draft + Codex iterate)
**对应 gap**: β.G4 (见 [umr_path_beta_derivation.md](umr_path_beta_derivation.md) §2.4 + [umr_path_beta_v0_4_detailed_draft.md](umr_path_beta_v0_4_detailed_draft.md) §5)
**目标**: 严格 derive inequality $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\mathcal{A}_\text{LOPC}}(\tilde{\mathcal{M}})$

---

## 0. 严谨性

- **[CONJ-DRAFT]** throughout
- 无 silent upgrade; 无 section title "(closes X)"; 无 combined chain claim
- Citations 5 级 taxonomy: [VERIFIED against PDF] / [MEMO-LEVEL QUOTE] / [SUMMARY] / [INFERENCE, unverified] / [RECALLED]
- 本 draft 是 "attempted direction"; 等 Codex review + iterate
- **不**升级任何分级; 即使 Codex PASS 仍 stay [CONJ-DRAFT] 直到 R0.2 C1+C2+C3

---

## 1. 背景设定

### 1.1 两个 adversary 模型

**Eve 的 umr 模型** $\mathcal{A}_\text{umr}$:
- Eve **purifies** $\mathcal{E}_1$ and $\mathcal{E}_2$ — 即 Eve 持有 each channel's environment register (isometric dilation)
- Eve **controls Charlie** — Charlie 的 BSM measurement choice + broadcast 都由 Eve 决定
- Eve sees: $\text{Env}(\mathcal{E}_1), \text{Env}(\mathcal{E}_2)$, Charlie's internal registers, broadcast history across rounds

**LOPC 模型** $\mathcal{A}_\text{LOPC}$ **on effective channel** $\tilde{\mathcal{M}}$:
- Eve purifies $\tilde{\mathcal{M}}$ itself (作为 single composite channel)
- Alice ↔ Bob 允许 LOPC (Local Operations + Public Communication)
- 没有"Charlie"概念 — Charlie has been absorbed into $\tilde{\mathcal{M}}$'s structure

### 1.2 要证的 inequality direction

希望证: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\mathcal{A}_\text{LOPC}}(\tilde{\mathcal{M}})$

**Interpretation**: umr Eve **更强** (持 Charlie 控制权) → Alice-Bob 更难 distill secret key → umr rate **更低**.

LOPC Eve **更弱** (Charlie 内嵌 $\tilde{\mathcal{M}}$ 不 adversarial) → Alice-Bob 更易 distill → LOPC rate **更高**.

因此 inequality direction: umr ≤ LOPC (作 upper bound of umr via LOPC).

---

## 2. Attempted direction — 尝试 construct simulation map

### 2.1 The challenge (Codex R1 曾 critique)

Previous attempt (β v0.4-R1) 声称: "LOPC Eve 可从 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2)$ simulate Charlie register"。Codex R1 correctly identified this as **unsupported premise** because:

- Charlie 的 BSM outcome statistics $p(c | \rho_{\hat{A}\hat{B}})$ depend on the **joint state** $\rho_{\hat{A}\hat{B}}$ held by Charlie
- $\rho_{\hat{A}\hat{B}}$ 是 $\mathcal{E}_1 \otimes \mathcal{E}_2$ 作用后的 **primary output**, 不仅是 environment register 的 function
- 即便 Eve 持 $\text{Env}(\mathcal{E}_1, \mathcal{E}_2)$ purifications, Charlie's output register is **still Eve's actual possession only if Charlie's BSM itself is captured**

### 2.2 Reframing — 不是 "simulate", 而是 "subsumption"

关键 insight (attempted, [CONJ-DRAFT]): 我们**不需要** LOPC Eve "simulate" umr Eve. 我们只需证明:

> **Claim β.G4.α**: 对任意 umr protocol $\Pi$ + umr Eve strategy, 存在一个 LOPC protocol $\Pi'$ + LOPC Eve strategy (on channel $\tilde{\mathcal{M}}$) 使得 (1) $\Pi'$ 的 secret key rate $\geq \Pi$ 的 rate, (2) $\Pi'$ 的 Eve strategy 是 legal LOPC-on-$\tilde{\mathcal{M}}$ strategy.

若 Claim β.G4.α 成立, 则 $\sup_\Pi R^{\mathcal{A}_\text{umr}}(\Pi) \leq \sup_{\Pi'} R^{\mathcal{A}_\text{LOPC}}(\Pi') = R^{\mathcal{A}_\text{LOPC}}(\tilde{\mathcal{M}})$.

### 2.3 Attempted proof of Claim β.G4.α [CONJ-DRAFT]

Construction:
- Given $\Pi$ on umr with Eve strategy $\mathcal{S}$
- LOPC protocol $\Pi'$: Alice-Bob **honestly** simulate umr's Charlie-side via **public classical communication** of simulated broadcast $c$
- Specifically:
  - Alice + Bob prepare their sources locally (same as umr)
  - Channel $\mathcal{E}_1, \mathcal{E}_2$ happen (same)
  - **Instead of Charlie doing BSM**: Alice and Bob do nothing to each other's modes; the effective channel $\tilde{\mathcal{M}}$ in LOPC includes $\mathcal{E}_1, \mathcal{E}_2$ + a "passthrough" that **delivers $\hat{A}, \hat{B}$ to some register held by Eve** (since LOPC Eve purifies $\tilde{\mathcal{M}}$)
  - LOPC Eve 被迫 hold $\hat{A}, \hat{B}$ + do BSM on them + broadcast $c$
  - **Ironically**: LOPC Eve's "optimal strategy" mirrors umr Eve's Charlie

### 2.4 Gap in 2.3 — this is still OPEN

上面 2.3 的 construction 实际上**错了**. LOPC Eve **不是 forced to do BSM + broadcast**:
- LOPC 定义是 Alice ↔ Bob LOCC + Eve passive on purification register
- LOPC Eve 不 "broadcast" classical info to Alice-Bob; 那是 Alice-Bob 之间的 classical side channel
- 所以 LOPC Eve 不 simulate umr Charlie's role; 两者 structurally 不同

### 2.5 Reframing attempt 2 — "LOPC 外加一个 side channel" (R2 correction, no claim)

Consider hypothetical extended protocol class: **LOPC + public classical side channel from Eve** (heuristic model). 这 essentially 把 umr 的 Charlie broadcast 看作 "Eve's classical announcement to Alice-Bob".

**R2 correction per Codex R1**: 本 draft **不声称** LOPC+gift 与 standard LOPC 或 umr 之间任何 rate inequality. 原 draft 曾 asserted $R^{\text{LOPC+gift}} \geq R^{\mathcal{A}_\text{umr}}(\Pi)$ 并 called LOPC+gift "strictly more permissive", 但**未**提供 formal quantifier-level definition of extended model 或 inf/sup order over Eve strategies. 该 assertion 撤回.

LOPC+gift **可能**作为 heuristic bridge useful, 但 **无 rate inequality 在本 draft 已 established**. 实际方向 (是否更松/更紧/agnostic) 需 user 或后续工作 formalize extended model 定义 + Eve strategy quantifier 后才能判定.

### 2.6 Gap summary (after this draft attempt)

- **§2.3 attempted direct simulation construction 失败** (per §2.4 argument, 仅针对 该 specific construction)
- **LOPC+gift 作 heuristic bridge**: 未 established rate inequality to either LOPC 或 umr
- 本 draft attempt **reaffirms β.G4 as open structural gap**; 本 draft 未 rule out 其他 simulation map, 只 invalidate §2.3 的 specific construction

---

## 3. Honest conclusion — β.G4 remains OPEN

本 draft 尝试 construct simulation map 失败. 结论:

- umr Eve model ↔ LOPC Eve model on effective channel 之间**没有简单的 inequality 关系** via direct simulation
- 可能的 path forward (未尝试):
  - **Path A**: 改变 effective channel 定义, 让 $\tilde{\mathcal{M}}$ 包含 Charlie broadcast 作 channel 的 classical output → LOPC 下 Alice-Bob 自然获得 broadcast. 但这时 $\tilde{\mathcal{M}}$ 不是标准 CPTP, 而是 CPTP + classical side channel
  - **Path B**: 放弃通过 LOPC framework 上界; 直接在 umr 框架里走 amortized-type argument (回到 β.G5 开门)
  - **Path C**: Portmann-Renner composable framework **explicitly** handle umr adversary class without reduction to LOPC [RECALLED — user must read Rev. Mod. Phys. 94:025008 for formal check]

### 3.1 Literature pointers (no AI application)

- **Portmann-Renner 2022 Rev. Mod. Phys. 94:025008** [RECALLED]: composable security for arbitrary adversary classes. 若该 framework 直接 handle umr Eve, 则可能避开 β.G4 bottleneck.
- **Khatri-Wilde 2020 Ch 20 Secret Key Agreement** [MEMO-LEVEL QUOTE via KhatriWilde-2020.md §3.1]: "n-shot secret-key-agreement protocol 通过 $\mathcal{N}$ 分发 ε-secure 密钥位" - 但明示该章**trusted relay** 假设 (per KhatriWilde-2020.md §4.2 "relay node 是可信 party"). Umr 违反 此假设 — 所以 Ch 20 **不 directly apply**.

### 3.2 Honest takeaway

β.G4 是**真正 structural**, 不能被 AI draft 的 simulation argument close. User 必须:
- Path C (Portmann-Renner 直读 PDF + 为 umr adversary 定制 proof), 或
- Path B (放弃 LOPC reduction, 走另外的 amortized framework with adversarial comb — 回到 β.G5 的同等难题), 或
- 声明 β 路线 **intrinsically blocked by Eve-model-transfer**, fallback γ 路线

---

## 4. Relation to prior drafts

- v0.4-R1 claim: "LOPC Eve simulates umr Eve via environments" — Codex R1 MAJOR → 撤回
- v0.4-R2+: 标 "OPEN structural" 无 simulation proof — Codex R2 PASS
- **本 draft (v0.1)**: 诚实 attempt simulation + 诚实 记录 failure + 诚实 列 Paths A/B/C. β.G4 仍 OPEN.

**本 draft value**: 明确记录为什么 simulation-based reduction 不 work, 为 user 将来 Path C / B / drop 决策提供 concrete rationale.

---

## 5. Gap status (after this attempt)

| Aspect | Status |
|---|---|
| β.G4 claim $R^\text{umr} \leq R^\text{LOPC}(\tilde{\mathcal{M}})$ | **still OPEN** |
| §2.3 direct simulation construction | **invalidated by §2.4 argument** (针对 that specific construction) |
| Other direct-simulation maps | **未排除** (本 draft 仅 invalidate §2.3 construction, 非 disprove all possible simulations) |
| Paths forward | **Path A / B / C enumerated** (no AI proof on any) |
| 升级可能性 | **只能通过 user research-level work on Path C** |

---

## 6. Changelog

- **v0.1** (2026-04-22 late, user 授权 draft+Codex iterate): Honest simulation attempt + failure documentation + Path A/B/C enumeration
