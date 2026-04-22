# umr path γ.B.G1 — DPI target lemma derivation attempt

**版本**: v0.1 **[CONJ-DRAFT]** — AI autonomous (2026-04-23, user 授权 draft + Codex iterate)
**对应 gap**: γ.B.G1 (见 [umr_path_gamma_v0_4_derivation.md](umr_path_gamma_v0_4_derivation.md) §6.1 + [umr_path_gamma_v0_6_detailed_draft.md](umr_path_gamma_v0_6_detailed_draft.md) §3)
**目标**: 形式化 "Eve 对 Charlie's received-mode 的 downstream operations 不 increase Alice-Bob secret key correlation beyond $E_R(\mathcal{E}_1)$ bound" 的 DPI / LOCC-monotonicity lemma

---

## 0. 严谨性

- **[CONJ-DRAFT]** throughout
- 无 silent upgrade; 无 section title "(closes X)"; 无 combined chain
- Citations 5 级 taxonomy per β v0.4-R4 convention
- "attempted direction"; 等 Codex review + iterate
- **特别警惕**: γ v0.6-R1 曾以 "DPI chain" 语言重新包装 cross-task transfer — 本 draft **严格**避免

---

## 1. 问题陈述

### 1.1 Setup (umr 单边)

- $\mathcal{E}_1: A' \to \hat{A}$ (bosonic pure-loss, transmittance $\eta_A$)
- Alice 保留 reference register $A$ (entangled with $A'$ in source state)
- Alice 's mode $\hat{A}$ **到达 Charlie 后**, Charlie 做 joint BSM with Bob's $\hat{B}$ (from $\mathcal{E}_2(B')$), broadcast outcome $c$
- Eve 持有 $\text{Env}(\mathcal{E}_1)$ purification + Charlie controlled
- Final Alice-Bob state $\rho_{AB}^\text{final}$ depends on: source + $\mathcal{E}_1, \mathcal{E}_2$ + Charlie's BSM + broadcast + post-processing

### 1.2 γ.B.G1 target lemma (attempted statement)

**Target lemma γ.B.G1 (v0.1 [CONJ-DRAFT])**:

> 定义 $\mathcal{T}_\text{post-E1}: \hat{A} \otimes \hat{B} \otimes (\text{Alice-Bob registers}) \to (\text{Alice-Bob final registers})$ 为 "post-$\mathcal{E}_1$ Eve-controlled downstream operation" — 包括 Charlie BSM + broadcast + Bob-side operations + Alice-Bob post-processing (except Alice-Bob's LOCC based on $c$).
>
> 则 Alice-Bob bipartite private-state distance under $\mathcal{T}_\text{post-E1}$ 不 increase beyond Alice-Charlie primary-output correlation bound.

**Technical form (attempted)**:
$$\|\rho_{AB}^\text{final}(\mathcal{T}_\text{post-E1}) - \gamma_{AB}^K\|_1 \geq \|\rho_{A\hat{A}}^\text{primary} - \gamma_{A\hat{A}}^{K'}\|_1$$

for **some** corresponding $K'$ bound by Alice-Charlie channel capacity.

### 1.3 为什么这个陈述 vulnerable

**警报**: 上面 "Alice-Bob bipartite private state distance" vs "Alice-Charlie primary-output correlation" 就是 Codex 多次 flag 的 **cross-task transfer 陷阱** — 两边属于不同的 party sets 和 security models.

本 draft 的目的: **诚实** explore 这个 transfer 是否 rigorously 可证, 或识别它为 structurally unclosable.

---

## 2. Attempted approaches

### 2.1 Approach A — Khatri-Wilde Prop 19.2 amortized entanglement

**Strategy**: 直接 apply Khatri-Wilde Prop 19.2 to channel $\mathcal{E}_1$:

[MEMO-LEVEL QUOTE via KhatriWilde-2020.md §2.1]: "$E(M_A; M_B)_\omega \leq n \cdot E^\mathcal{A}(\mathcal{N})$ for any (n, M, ε) LOCC-assisted quantum communication protocol over channel $\mathcal{N}_{A\to B}$ with LOCC-monotone + separable-zero $E$".

**Issue (identified by Codex R1, 2026-04-22)**:
- Prop 19.2 的 scope 是 channel $\mathcal{N}_{A \to B}$ 用在 **two-party LOCC-assisted** protocol
- umr 是 **three-party** (Alice, Bob, Charlie) with Charlie adversarial
- Direct apply Prop 19.2 to $\mathcal{E}_1$ (Alice-Charlie channel) gives Alice-Charlie capacity bound, **not** Alice-Bob umr key rate
- Bridging to Alice-Bob 需要额外 reduction (这就是 γ.B.G1 本身)

**Conclusion**: Approach A **失败** — circular. Prop 19.2 本身是目标 lemma 的一个组件, 不能用它证它自己.

### 2.2 Approach B — Horodecki 2005 private state + BSM as LOCC-on-shared-state

**Strategy**: 尝试把 umr 看作 Alice-Bob **共享一个 bipartite state** $\rho_{\hat{A}\hat{B}}$ (after $\mathcal{E}_1 \otimes \mathcal{E}_2$ 作用), Charlie's BSM 是 "joint measurement on the shared state".

**问题**:
- **不是** Alice-Bob 共享状态 — $\hat{A}, \hat{B}$ 分别在 Charlie 手里 (Charlie 收到的 two modes). Alice 持 reference $A$; Bob 持 reference $B$. 所以实际是 **four-party state** $\rho_{A B \hat{A} \hat{B}}$
- Charlie 作为独立 party, BSM 是 Charlie 的 local operation on $(\hat{A}, \hat{B})$, 不是 Alice-Bob 的 LOCC
- Charlie 把 $c$ broadcast 给 Alice-Bob → 等效于 "Alice-Bob 获得 classical info from Charlie's measurement on their shared-but-not-directly-held state"

**形式化尝试**: 相关候选 quantity 是 $I(A : B | c)_\rho$ (conditional mutual information of Alice-Bob given Charlie's broadcast) 或其他 secret-key-relevant 量, but precise form 未定.

**Issue 1 (R2 correction per Codex R1)**: $I(A : B | c) \leq I(A : B)$ (conditioning 不增加 joint info) **是错的** — conditional mutual information 与 unconditional mutual information 之间**无 general monotonicity**, 方向可正可负取决于 state structure. 本 draft 原先的 "conditioning 不增加" 声明**撤回**.

**Issue 2**: 即使有某个 DPI chain 给 mutual information bound, **bridge to $E_R(\mathcal{E}_1)$ still fails** because $I \not\leq E_R$ generally (Codex R1 §3 已指出). 所以 Approach B 即使 technical mutual-info chain 可走通, 仍不 close γ.B.G1.

**Conclusion**: Approach B **未 close** γ.B.G1. 两个 blocker:
- 需要 well-defined candidate DPI chain (未找到 rigorous one)
- 即使找到, 到 $E_R$ 的 bridge 仍 open ($I \not\leq E_R$ generally)

### 2.3 Approach C — squashed entanglement framework [SUMMARY, unverified]

**Idea**: Squashed entanglement $E_\text{sq}$ is LOCC-monotone + subadditive + separable-zero, with operational meaning (Christandl-Winter 2004). Khatri-Wilde Thm 19.4 / 20.3 gives $\log_2 K \leq \frac{1}{1-\sqrt{\varepsilon}}[n \cdot E_\text{sq}(\mathcal{N}) + g_2(\sqrt{\varepsilon})]$ as **weak converse** for secret key agreement.

**问题**:
- $E_\text{sq}(\mathcal{N}_{A \to B})$ 是 channel squashed entanglement — 对 $\mathcal{E}_1$ 可计算, 但对 $\tilde{\mathcal{M}}$ 整体需重新定义
- $E_\text{sq}$ 本身不 SDP-计算 — 需 squashing choice (Li-Winter 2014 pass-through bounds)
- 同样问题: $\mathcal{E}_1$ 单边的 $E_\text{sq}$ 和 umr 整体 key rate 之间仍需 **cross-task bridge**

**Conclusion**: Approach C 面同一 cross-task 障碍. $E_\text{sq}$ framework 提供 upper bound on Alice-Charlie capacity, 但不**直接** bound Alice-Bob umr key rate.

### 2.4 Approach D — 把 umr 看作 broadcast channel with classical side output

**Idea**: Define $\tilde{\mathcal{M}}_\text{one-edge}: A' \to (\hat{A}, c)$ where $\hat{A}$ 是 post-$\mathcal{E}_1$ mode (goes to Eve-controlled Charlie), $c$ 是 "Charlie's broadcast on Alice's mode" (classical公共信息).

**Issue**:
- $\tilde{\mathcal{M}}_\text{one-edge}$ 的 output $(\hat{A}, c)$: $\hat{A}$ **不 delivered to Bob** (stays in Charlie); $c$ is公共 classical info
- 所以 $\tilde{\mathcal{M}}_\text{one-edge}$ 不是一个 "Alice → Bob" 的 effective channel — 它是 "Alice → (Eve, public)" channel
- PLOB / WTB 的 capacity 定义 is for Alice-sender Bob-receiver; 这里 Bob **没直接 receive** 任何东西 from $\mathcal{E}_1$ edge

**Partial insight**: Alice-Bob 的 key material 实际来自 "Alice 发送 mode → Charlie → Charlie broadcast $c$ → Alice-Bob combine with their own operations + $c$ to distill key". 所以 Alice-Bob 的 "effective channel" 在 $\mathcal{E}_1$ edge 上**仅 contribute through Charlie's side**.

**Conclusion**: Approach D 揭示 $\mathcal{E}_1$ **不 directly** bound Alice-Bob key rate. Alice-Bob key 来自 **Charlie's broadcast + Alice-Bob local operations**, 其中 Charlie's broadcast 的 information content 受 $\mathcal{E}_1$ 和 $\mathcal{E}_2$ 的 **joint** capacity 约束, 不是单边.

---

## 3. Key structural insight (attempted)

从 Approach A/B/C/D 失败 + 部分 insights 总结:

**Conjecture γ.B.G1.CONJ1 [CONJ-DRAFT, speculation only]** (R2 correction per Codex R1):

> 4 个 approaches 的 failure **可能 suggest** (但**未 prove**): γ path 的 single-edge PLOB 分解 intuition 可能**不是**正确 formulation — umr key rate 或许 essentially 是某种 joint multi-edge quantity (例如 Charlie broadcast information content 或类似), 不 decomposable 成 single-edge $E_R(\mathcal{E}_1)$ bound.

**注意**: 这是 **speculation**, 非 established. 4 approaches 失败只证明当前 single-edge-transfer program **目前 unclosed**, **不 establish** 正确 formulation 必然 NOT single-edge. 可能存在 approach E/F/... 我未想到.

**Possible alternative formulations (candidates, unverified)**:
- Joint bound on Charlie's classical broadcast information content (受 joint $(\mathcal{E}_1, \mathcal{E}_2)$ constraint)
- Multi-edge amortized framework (与 β.G5 同类)
- Different entropy measure avoiding $I \not\leq E_R$ obstacle

**Consequence (tentative, [CONJ-DRAFT])**: γ path 原 intuition "单边 PLOB + DPI transfer" **可能 need reformulation**; 但本 draft 不 prove it 必须 reformulation, 只 identify 现 approaches 全 fail.

### 3.1 Candidate reformulation

也许 γ path 应该 re-target: **bound Charlie's broadcast classical capacity**, which is in turn bounded by $(\mathcal{E}_1, \mathcal{E}_2)$ joint classical capacity (Holevo-type bound). 但这是 different target from γ's original $-\log_2(1-\eta_\text{arm})$ scaling.

---

## 4. Honest conclusion — γ.B.G1 remains OPEN (with structural doubts)

本 draft 尝试 4 个 approaches (Prop 19.2 amortized, Horodecki private state, squashed entanglement, broadcast-channel-with-classical-side). **4 个 approaches 均 fail** — 遇到不同障碍 (circular, $I \not\leq E_R$, cross-task obstacle, receiver-side asymmetry).

**Speculation (R2 correction, CONJ1 only)**: γ path 单边 PLOB 分解 intuition 或许 **structurally 不 work**, 但本 draft **不 prove** 这一点; 只 prove 现 4 approaches 全 fail. 可能存在 approach E/F/... AI 未想到.

### 4.1 Paths forward (for user decision, agnostic)

- **Path A** (Continue γ original target): user research-level 尝试 additional approach E/F beyond AI's 4. 可能 close γ.B.G1 on original $-\log_2(1-\eta_\text{arm})$ target.
- **Path B** (Reformulate γ): 改换 target quantity (e.g., Charlie broadcast capacity, multi-edge joint bound). Scaling 可能 different, 需 user 决定 reformulated target 是否仍值得.
- **Path C** (Drop γ): 放弃 γ safety net, 纯 β-centric Sub-Q3. 若 β 也 fail 则整体 Sub-Q3 upper bound regresses.
- **Path D** (Fallback to other literature bound): 寻找 已 established 的 umr-specific upper bound 文献 (若存在). 本 draft 未做 exhaustive 搜索.

**Agnostic note**: 本 draft **不 claim** γ path fallback to Pirandola trusted-relay bound — trusted-relay 假设 umr 不满足 (RETRACTION.md §1.1 已讨论), 所以 trusted-relay bound 对 umr **不直接 apply**. γ weakening 的 concrete form 未 established.

### 4.2 Literature pointers (no AI application)

- **Khatri-Wilde 2020 Ch 20** [MEMO caveat]: 明示 trusted relay 假设, umr 违反 — per memo §4.2
- **Horodecki 2005 PRL 94:160502** [RECALLED]: Bipartite private state framework, 主要 two-party; three-party umr 需 extension
- **Christandl-Winter 2004** [RECALLED]: Squashed entanglement definition

---

## 5. Gap status (after this attempt)

| Aspect | Status |
|---|---|
| γ.B.G1 claim (single-edge Alice-Charlie bound transfers to Alice-Bob) | **still OPEN** |
| Approaches A/B/C/D tried | **all fail**, various obstacles (circular / $I \not\leq E_R$ / cross-task / receiver asymmetry) |
| CONJ1 (single-edge decomposition may be wrong) | **speculation [CONJ-DRAFT]**, not established by 4 failures |
| 升级可能性 | **only via user research-level work on Path A/B/C/D** |

### 5.1 Implication for Q1 decision (β main + γ safety) — agnostic

本 draft 发现 γ safety net **可能**比 previously assumed weaker, 但 **agnostic about specific form**:
- **β main 继续有效** (β path 独立 of γ, 不受 γ.B.G1 的 4 approach failures 影响)
- **γ safety 状态**: currently **open** — 本 draft 不 prove γ 必然 fail, 也不 establish 具体 fallback bound

**不声明** fallback 到 Pirandola trusted-relay bound — 后者 assumes trusted relay, umr violation (per RETRACTION.md §1.1). 若 γ 真的 reformulate, specific fallback target 需 user research-level analysis 决定.

**Agnostic takeaway for Q1**: Q1 决策 (β main + γ safety) 的 rationale 基于 β / γ 的 research direction 可行性 analysis, 本 draft failure 不 shift decision, 但 adds caveat that γ path may need additional work or reformulation.

---

## 6. Changelog

- **v0.1** (2026-04-23, user 授权 draft+Codex iterate): 4 approaches tried, all fail on cross-task transfer. γ.B.G1 remains OPEN. 更深的 insight: 单边 PLOB transfer intuition 可能 structurally 错; γ path 可能需 reformulation.
