# umr upper bound — path γ v0.4 derivation (Log 07 §4.5 strict, NO super-receiver merge)

**版本**：v0.4 **[CONJ]** — AI autonomous (2026-04-22 Round 2 FIX 响应 Codex FAIL verdict on v0.3)
**对应 Log 07**：§4.5 "scaling exponent 的上界 (最弱的可靠判断)" **strict reading**
**NOT v0.2 / v0.3**：
- v0.2: adversarial containment (set-inclusion) — retracted 2026-04-21
- v0.3: super-receiver Bob-Charlie-Eve merge — Codex R1 FAIL 2026-04-22 (仍是 cross-space 陷阱)
- **v0.4**：**no merging Bob with Eve**; strict "single-edge PLOB on $\mathcal{E}_1$ alone" + separately stated DPI/LOCC-monotonicity lemma

---

## ⚠️ Round 2 FIX notice (v0.3 → v0.4)

[v0.3 Codex verdict (FAIL)](../workflow/paths-review/review-diff-1.json):

> "Path γ v0.3 does avoid the literal v0.2 set-inclusion shortcut, but Step 1/2 replace it with a different unsound move: **Bob, Charlie, and Eve are merged into a single remote register** and then PLOB is treated as 'label agnostic'. That is not just relabeling, because **the honest receiver in the secret-key task has been fused with the adversary** whose knowledge must be excluded."

> "Delete the super-receiver PLOB route and rewrite γ strictly as the Log 07 §4.5 program: single-edge PLOB on $\mathcal{E}_1/\mathcal{E}_2$ plus a separately stated DPI/LOCC-monotonicity lemma that transfers an Alice→Charlie correlation bound to the Alice-Bob key-rate setting."

**Response (v0.4, this file)**: **accepted**。完全删除 v0.3 的 "super-receiver merge"; 重新 derivation 按 Codex 指示 strict separation of PLOB step and DPI step。

---

## 0. 严谨性

- AI autonomous derivation → **[CONJ]**
- Gaps 显式
- **不**升级 FINDINGS / Log 07
- 等 Codex R2 review

---

## 1. Target Theorem [CONJ]

**Theorem γ (v0.4 target)**: 对 $\Pi \in \mathcal{T}_\text{umr}$:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B))$$

Scaling 推论（对称 $\eta$）: $R \leq \sqrt{\eta_{AB}}/\ln 2 + O(\eta_{AB})$。

---

## 2. Strict derivation (v0.4, 按 Codex 指示)

### 2.1 Step A — PLOB applied to Alice-Charlie channel (NO merging)

**Setup**: $\mathcal{E}_1: A' \to \hat{A}_1$ 是 Alice's photon mode 到 Charlie's receiver register。 $\mathcal{E}_1$ 是 standard bosonic pure-loss channel with transmittance $\eta_A$。

**PLOB 2017 Theorem 1 applied to $\mathcal{E}_1$**: 对任何 point-to-point LOPC protocol on $\mathcal{E}_1$ (Alice 作为 sender, **Charlie** 作为 receiver) between Alice 和 Charlie:

$$K_\text{A-C}^{\text{LOPC}}(\mathcal{E}_1) \leq E_R^\infty(\mathcal{E}_1) = -\log_2(1-\eta_A)$$

其中 $K_\text{A-C}^{\text{LOPC}}$ 是 "Alice-Charlie secret-key capacity" (point-to-point, 两方 LOPC)。

**Severity**：**[COROLLARY of PLOB 2017 Thm 1]**; **Charlie** 作为 point-to-point receiver 是 standard PLOB formulation; Bob 完全不在此 step。

**NOT merged**: 与 v0.3 不同, Bob **不是** "super-receiver" 的一部分 in Step A; 我们只讨论 **Alice-Charlie** point-to-point capacity。

### 2.2 Step B — DPI / LOCC-monotonicity lemma (separately stated, Log 07 §4.5 核心)

**Target claim**: Alice-Bob secret-key rate $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi)$ 不超过 Alice-Charlie secret-key rate $K_\text{A-C}^\text{LOPC}(\mathcal{E}_1)$。

**Intuition** (Log 07 §4.5): Alice 送出的信息**最多**被 Charlie 接收；Eve 对 Charlie mode 做任何 downstream operation (包括联合 Bob mode 做 BSM + broadcast classical $c$) 只是 Alice-Charlie 可见信息的 **classical downstream processing**。经典下游 operations **不增加** 可提取的 Alice-Bob secret key。

**Formal lemma (γ.DPI)** [target statement]:
Let $K_\text{A-B}(\Pi)$ be the secret-key capacity of the full Alice-Bob-Charlie umr protocol $\Pi$ (with Charlie adversarial). Let $K_\text{A-C}^\text{LOPC}(\mathcal{E}_1)$ be the point-to-point Alice-Charlie LOPC secret-key capacity (Alice sender, Charlie receiver). Then:

$$K_\text{A-B}(\Pi) \leq K_\text{A-C}^\text{LOPC}(\mathcal{E}_1)$$

**Justification intuition**: Alice-Bob 的 shared key must be computable from (Alice's register, Bob's classical announcements + Charlie's public broadcast). Charlie's broadcast is classical side-info derived from post-$\mathcal{E}_1$ Alice-mode + post-$\mathcal{E}_2$ Bob-mode. Assume Eve controls Charlie — then classical broadcast 是 Eve-accessible classical channel. Eve 对 Alice-mode (after $\mathcal{E}_1$) 拥有 full access (via Charlie)。所以 Alice-Bob secret key 最多是 **Alice-Charlie** (point-to-point) secret key 的 downstream — 因为 Bob 的 info 来自 Alice-Charlie 的 public classical channel + Bob's own local data。

**Gap γ.DPI.G1** (**关键 gap**): 此 claim 的 **严格数学** formulation 需 explicit use 于:
- Portmann-Renner composable security framework
- LOCC monotonicity of secret-key capacity (Horodecki 2009 or similar)
- 具体 operator-algebra argument 把 "Bob 的 info 是 Alice-Charlie public broadcast 的 downstream" 变成 $K_\text{A-B}(\Pi) \leq K_\text{A-C}^\text{LOPC}$

**Gap γ.DPI.G2**: Bob 对 Alice-Charlie LOPC 来说是 **"额外合法方"** — 他不是 receiver (Charlie 是), 也不是 Eve (按本 path γ v0.4 的 careful setup); 他是 **Alice-Bob key 的 co-holder**, 只能通过 Charlie 的 public broadcast 学到 Alice 的 info。严格说 Bob 在 Alice-Charlie-only point-to-point LOPC model 下**不存在**。需要 explicit framework 处理 "co-key-holder Bob" 不是简单的 side-info — 这是 subtle。

**严谨性**：**[CONJ, γ.DPI.G1 + γ.DPI.G2 open]**

### 2.3 Step C — Symmetric Bob-Charlie argument

By symmetry, 重复 Step A + Step B with Bob's channel $\mathcal{E}_2$:

$$K_\text{A-B}(\Pi) \leq K_\text{B-C}^\text{LOPC}(\mathcal{E}_2) = -\log_2(1-\eta_B)$$

**Combine**:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq \min\{-\log_2(1-\eta_A), -\log_2(1-\eta_B)\} = -\log_2(1-\min(\eta_A, \eta_B))$$

**严谨性**：**[CONJ conditional on γ.DPI.G1 + γ.DPI.G2 resolved]**

### 2.4 Step D — ε-composable security ε transfer

**Gap γ.G3** (from v0.3): PLOB 2017 gives asymptotic capacity; ε-composable framework gives finite ε rate. 需 Devetak-Winter or Portmann-Renner-style ε transfer。**未 handled** at this scaffolding level。

**严谨性**：**[CONJ, γ.G3]**

### 2.5 Step E — Combine scaling

$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\eta_\text{arm})$, $\eta_\text{arm} = \min(\eta_A, \eta_B)$

High-loss: $\approx \eta_\text{arm}/\ln 2 = \sqrt{\eta_{AB}}/\ln 2$ (for symmetric)

---

## 3. Gap summary (v0.4)

| Gap | 描述 | Severity | 升级所需 |
|---|---|---|---|
| γ.DPI.G1 | LOCC-monotonicity argument: $K_\text{A-B}(\Pi) \leq K_\text{A-C}^\text{LOPC}$ strict proof | **MAJOR** | Portmann-Renner + Horodecki 框架; 用户纸笔 2-3 天 |
| γ.DPI.G2 | Bob 在 Alice-Charlie point-to-point framework 下的 role | **MAJOR** | Operator-algebra framework; 用户纸笔 1-2 天 |
| γ.G3 | ε-composable transfer (PLOB asymptotic → ε-bounded) | MAJOR | Devetak-Winter or Portmann-Renner; 1-2 天 |
| γ.G4 | Classical announcement $c$ LOCC processing (standard but needs writeup) | MINOR | Standard LOCC argument |

**Total: 4 gaps (3 MAJOR + 1 MINOR)**

**Key diff 对 v0.3**：
- v0.3 Step 1 (super-receiver merge) **DELETED**
- v0.3 Step 2 (super-LOPC PLOB apply) **DELETED**
- v0.4 Step A (point-to-point PLOB on $\mathcal{E}_1$，Charlie 是 receiver) **NEW**
- v0.4 Step B (separately stated DPI/LOCC-monotonicity lemma) **NEW**
- Bob 和 Eve **NOT merged** at any step

---

## 4. 与 Log 07 §4.5 对齐度

Log 07 §4.5 原文：
> "单 channel PLOB on $\mathcal{E}_1$ alone ⇒ $\mathcal{K}_\text{umr} \leq -\log(1-\sqrt{\eta})$（**这一步只需 Alice-单独看 $\mathcal{E}_1$**, 不用网络 min-cut）"

> "等一下 — 第二步实际不需要 Pirandola 2019，只需 PLOB 2017 应用在 Alice-Charlie 这一条 channel 上, 然后注意 'Alice 送出去的信息最多被 Charlie 接收', Eve 把 Charlie 做的事当做 additional attack, **不能增加 Alice-Bob 的 correlation**"

v0.4 **严格实施** Log 07 §4.5:
- Step A = "单 channel PLOB on $\mathcal{E}_1$ alone" ✓
- Step B = "Eve 对 Charlie 的 downstream operation 不增加 Alice-Bob correlation" (明写 DPI lemma) ✓
- **No** super-receiver merge (v0.3 错误)
- **No** set-inclusion (v0.2 错误)

---

## 5. 严谨性

- **[CONJ]** overall
- 4 gaps explicit
- **不**升级任何分级
- **v0.2 + v0.3 两种 cross-space 陷阱 都 avoid**

---

## 6. Changelog

- **v0.4** (2026-04-22 Round 2 FIX): 响应 Codex R1 FAIL — 删除 v0.3 super-receiver merge; 严格按 Log 07 §4.5 写 point-to-point PLOB + separately stated DPI lemma
- **v0.3** (2026-04-22): v0.3 super-receiver merge approach — **Codex R1 FAIL**: Bob merged with Eve fuses honest receiver with adversary; 删除
- **v0.2** (2026-04-21): adversarial containment set-inclusion — **retracted** 2026-04-21 per Claude audit + Codex audit
- **v0.1** (2026-04-21): initial three-lemma attempt, 保守 [DRAFT]
