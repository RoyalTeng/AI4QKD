# umr upper bound — path α derivation (monotonicity reduction via Khatri-Wilde §19-20)

**版本**：v0.1 **[CONJ]** — AI autonomous derivation (2026-04-22)
**对应 Log 07**：§3.1 子节 "路径 α" + §4.3 "路径 α (monotonicity) 是正确路径,但需要写出来"
**前置 scaffolding**：[umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) v0.1
**用途**：从 11-gap scaffolding 升级到 attempted derivation；所有仍未 close 的 gap 显式

---

## 0. 严谨性

- AI autonomous derivation → default **[CONJ]**
- 11 gaps from scaffolding + potentially new gaps from derivation attempt
- **不**升级 FINDINGS / Log 07
- 等 Codex review

---

## 1. Target Theorem [CONJ]

**Theorem α**: 对 $\Pi \in \mathcal{T}_\text{umr}$ 以 monotonicity reduction path (Khatri-Wilde §19-20 + PLOB 2017 继承):

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B))$$

Scaling 推论（对称 $\eta$）: $R \leq \sqrt{\eta_{AB}}/\ln 2 + O(\eta_{AB})$

---

## 2. Derivation chain (attempted)

### 2.1 Step 1 — Protocol embedding $\iota$ 构造

**Setup**:
- $\Pi$: umr protocol operating on $(A, A', B, B', E_1, E_2, E_\text{Charlie})$ where Alice holds $A$, sends $A'$ through $\mathcal{E}_1$ (env $E_1$); similarly for Bob; Charlie holds post-channel registers $(E_1', E_2')$ and does POVM + classical announcement $c$
- $\iota(\Pi)$: **same protocol operations** but in 一个 "trusted relay" model where Charlie is treated as cooperative honest party (not part of Eve)

**Construction**:
$\iota: \mathcal{H}_\Pi^\text{umr} \to \mathcal{H}_\Pi^\text{tr}$ is the **identity embedding of operations** — same Kraus operators, same announcements — but **attributes differ**:
- umr: Charlie register is part of $E_\text{adv}$ (Eve accessible)
- tr: Charlie register is honest (Alice-Bob-Charlie cooperation)

**Hilbert 空间**:
- $\mathcal{H}_\Pi^\text{umr}$: Alice + Bob + Charlie + environments
- $\mathcal{H}_\Pi^\text{tr}$: **Same** Hilbert 空间，不同 security attribution
- $\iota$ 是 **identity** on Hilbert 空间；只是 re-labeling of which registers Eve controls

**Gap α.G1 (from scaffolding)**: $\mathcal{A}_\text{umr}$ vs $\mathcal{A}_\text{tr}$ 的精确 set-level 定义。在上 identity-embedding $\iota$ 下，**物理 operations 相同** 但 Eve 权限不同。这不是 v0.2 的 set-inclusion shortcut —— 这是**关注 Eve 权限而非 Eve 集合** (different framing)。

**严谨性**：**[CONJ, G1 仍 open]**

### 2.2 Step 2 — Monotonicity lemma (Khatri-Wilde Prop 19.2 / Cor 19.3)

**Ref**: [Khatri-Wilde 2020/2024 §19.2](../literature/KhatriWilde-2020.md)

**Prop 19.2 statement** (为本推导 purpose 简述):

> 对 "n-shot LOCC-assisted quantum communication" protocol，输出的 entanglement 被 amortized entanglement 上界：
> $$\text{output entanglement} \leq n \cdot E^A(\mathcal{N})$$
> 其中 $E^A$ 是 amortized 版本；特别对 **tele-simulable channels**，$E^A(\mathcal{N}) = E(R; B')_\theta$ 对特定 input state $\theta$。

**Apply to $\iota(\Pi)$** (trusted-relay setting):
- $\iota(\Pi)$ 是 Alice + Bob + cooperative Charlie 的 protocol, LOCC-assisted
- $\iota(\Pi)$ 通过 channel stack $(\mathcal{E}_1, \mathcal{E}_2)$ with Charlie BSM
- 由 Khatri-Wilde Prop 19.2 + tele-simulability of $\mathcal{E}_1, \mathcal{E}_2$:
  $$R_\varepsilon(\iota(\Pi)) \leq E^A_\text{channel-stack}$$

**Gap α.G2**: 具体 channel stack 的 amortized entanglement $E^A$ 在 umr / trusted-relay 下的 formulation。Khatri-Wilde §19.2 是 point-to-point single channel; stacked + Charlie-BSM 需要 extension。

**Gap α.G3 (from scaffolding, modified)**: $\iota$ 是 identity 还是 embedding? 如果是 identity，$\iota(\Pi)$ 的 operations 与 $\Pi$ 相同，但 Khatri-Wilde Prop 19.2 的"LOCC-assisted" 在 trusted-relay 下 **包含** Charlie's operations（honest cooperative）； 在 umr 下**不包含** Charlie's operations 作为 LOCC step (Charlie 是 Eve)。 monotonicity 的 LOCC-assumption 在两情形**不等价**。

**严谨性**：**[CONJ, G2+G3]**

### 2.3 Step 3 — PLOB 2017 continuous apply

**Step 3**：对每个 single channel $\mathcal{E}_i$（$i=1,2$），PLOB 2017 Theorem 1 给:

$$E_R^\infty(\mathcal{E}_i) = -\log_2(1-\eta_i)$$

**Combine**: $R_\varepsilon(\iota(\Pi)) \leq \min_i E_R^\infty(\mathcal{E}_i) = -\log_2(1-\min(\eta_A, \eta_B))$

**Gap α.G4**: Step 2 给的是 $E^A_\text{channel-stack}$ bound，Step 3 给 per-channel $E_R^\infty$ bound. 两者的 chain 关系：$E^A_\text{stack} \leq \min_i E^A(\mathcal{E}_i)$? 对 multi-hop stacks, 这是 "min-cut" 型 bound (Pirandola 2019 Eq.11)。对 umr stacks with Charlie BSM, 不是 standard min-cut —— 需要 umr-specific bound 继承 argument.

**严谨性**：**[CONJ, G4]** — 是 Pirandola 2019 min-cut 在 umr 下的**类似继承** gap (with different framing)。

### 2.4 Step 4 — Security reduction (Gap L2 from scaffolding)

**Step 4**: 把 $R_\varepsilon(\iota(\Pi))$ 转成 $R_\varepsilon(\Pi)$ in $\mathcal{A}_\text{umr}$ model.

**Claim**: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon(\iota(\Pi))$

**Intuition**: umr Eve 更强 (持有 Charlie's register + environments) → umr rate 更低。

**Gap α.G5 (from scaffolding L2.G1)**: Direction correct? 需 careful check. v1 FINDINGS 曾 direction 错。

**Gap α.G6 (from scaffolding L2.G3)**: Eve 能力的 across-spaces 包含。v0.2 retraction 陷阱 (Claude audit + Codex 双 UNSOUND)。

**严谨性**：**[CONJ, G5+G6]** — 这是 **path γ v0.2 retraction** 同类 gap。

### 2.5 Step 5 — Final chain

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \overset{\text{G5,G6}}{\leq} R_\varepsilon(\iota(\Pi)) \overset{\text{G2,G3,G4}}{\leq} -\log_2(1-\min(\eta_A, \eta_B))$$

**严谨性**：**[CONJ, all 6 gaps open]**

---

## 3. Gap summary (upgrade from scaffolding)

| Gap (derivation) | From scaffolding | Severity | 状态 |
|---|---|---|---|
| α.G1 Embedding $\iota$ | L1.G1 + L1.G2 + L1.G3 + L1.G4 | MAJOR | open (reframed as "attribution-embedding" not set-inclusion) |
| α.G2 Khatri-Wilde Prop 19.2 apply to channel stack | L1 gap-related | MAJOR | open |
| α.G3 LOCC in umr vs trusted-relay | L1.G2 | MAJOR | open |
| α.G4 $E^A_\text{stack} \leq \min_i E^A(\mathcal{E}_i)$ for umr | L3.G3 | MAJOR | open |
| α.G5 Direction (umr ≤ tr rate) | L2.G1 | MINOR | standard direction check |
| α.G6 Eve spaces across topology | L2.G3 | **CRITICAL** | same as v0.2 retraction pattern |

**Total: 6 gaps** (合并/重组 scaffolding 的 11 gaps)。4 MAJOR + 1 CRITICAL + 1 MINOR。

**CRITICAL α.G6** specifically: avoid v0.2 "set-inclusion shortcut" temptation. **必须**用 explicit embedding $\iota$ (as attempted in Step 1) **plus** explicit Portmann-Renner ε-security transfer (as Step 4 gap).

---

## 4. Diff vs path γ v0.2

path α 在 Step 1 用 identity-embedding $\iota$ (rename Eve attribution) 而非 v0.2 的 set-inclusion。但最终 Step 4 (security reduction) 仍面临 **同类 Eve-across-spaces 问题**。 区别在于 α 有 explicit intermediate step (monotonicity + Khatri-Wilde)，γ v0.2 没有。

**是否 α safer than γ v0.2**：部分。 α 的 Step 2 + Step 3 确实 more explicit。 但 α.G6 仍是 same class of issue — 需要 Portmann-Renner 严格 handle。

---

## 5. 严谨性

- 本文件 **[CONJ]**; 6 gaps explicit (4 MAJOR + 1 CRITICAL + 1 MINOR)
- **不**升级 FINDINGS / Log 07
- 等 Codex review 特别 focus on α.G6 retraction pattern risk

## Changelog

- **v0.1** (2026-04-22 autonomous): upgrade scaffolding → attempted derivation; 6 gaps after merge/restructure
