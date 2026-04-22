# umr upper bound — path β derivation (channel-reduction + PLOB/WTB on effective channel)

**版本**：v0.1 **[CONJ]** — AI autonomous derivation (2026-04-22)
**对应 Log 07**：§3.1 子节 "路径 β" + §4.4 ("direct umr converse via channel-reduction")
**用途**：提供 path β derivation attempt; 所有 gap 显式

---

## 0. 严谨性

- AI autonomous derivation → default **[CONJ]**
- gaps 显式 marked
- **不**升级 FINDINGS / Log 07 分级
- 等 Codex review

---

## 1. Target Theorem [CONJ]

**Theorem β (target)**: 定义 **effective channel** 

$$\tilde{\mathcal{M}}: \mathcal{H}_A \otimes \mathcal{H}_B \to \mathcal{H}_{A} \otimes \mathcal{H}_{B} \otimes \mathcal{C}_\text{broadcast}$$

其中 $\mathcal{C}_\text{broadcast}$ 是 Charlie's classical announcement register (含 BSM outcome)。$\tilde{\mathcal{M}}$ 的 action:
- Alice input $A$ 通过 $\mathcal{E}_1$ → Charlie's side
- Bob input $B$ 通过 $\mathcal{E}_2$ → Charlie's side
- Charlie 对 $(\mathcal{E}_1(A), \mathcal{E}_2(B))$ 做 BSM + announcement

**Claim**: 所有 $\Pi \in \mathcal{T}_\text{umr}$ 的 key rate 满足

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq E_R^\infty(\tilde{\mathcal{M}}) = \text{(some function of } \eta_A, \eta_B \text{)}$$

其中 $E_R^\infty(\tilde{\mathcal{M}})$ 是 effective channel 的 regularized relative entropy of entanglement。

**Scaling 预期** (Log 07 §4.4)：$E_R^\infty(\tilde{\mathcal{M}})$ 可能**严格小于** Pirandola 2019 min-cut bound $-\log_2(1-\sqrt{\eta_{AB}})$, because umr 约束 Charlie 为 measure-only (classical broadcast), 损耗 Eve 可提取的量子信息。

---

## 2. Derivation chain (attempted)

### 2.1 Step 1: Effective channel construction

**Claim**: 任何 umr 协议 $\Pi$ 的每轮 operation（after 合并 Alice-Bob source + channel + Charlie BSM + announcement）可 写成 **single CPTP map** $\tilde{\mathcal{M}}$。

**Construction**:
- Alice 准备 state $\rho_{AA'}^\text{source}$ on (key register, photon mode)
- Bob 准备 $\sigma_{BB'}^\text{source}$
- Alice's photon mode $A'$ 过 $\mathcal{E}_1$: $A' \to \hat{A}$ (to Charlie)
- Bob's $B'$ 过 $\mathcal{E}_2$: $B' \to \hat{B}$
- Charlie 对 $(\hat{A}, \hat{B})$ 做 POVM $\{M_k\}_k$ outcomes $k$
- Charlie broadcast $k$ as classical $c$

Full composite channel from $(\rho_{AA'} \otimes \sigma_{BB'})$ to $(A, B, c)$:

$$\tilde{\mathcal{M}}_\text{full}(\rho \otimes \sigma) = \sum_k \text{Tr}_{\hat{A}\hat{B}}\left[M_k \cdot (\mathcal{I}_{AB} \otimes \mathcal{E}_1 \otimes \mathcal{E}_2)(\rho \otimes \sigma)\right] \otimes |k\rangle\langle k|_c$$

后面 Alice-Bob 做 classical post-processing (sifting + announcement + key map) → final key state.

**Gap β.G1**: $\tilde{\mathcal{M}}$ 的 input 是 **two separate sources** $(\rho_{AA'}, \sigma_{BB'})$，而 PLOB 的 standard formulation 是 **single bipartite** input $\rho_{AA'}$。把 two-source 合并成 one needs 工作 — Alice 和 Bob source 独立 (no pre-shared entanglement by QKD assumption)。所以 input 是 **separable** 即 $\rho \otimes \sigma$。PLOB bound on separable inputs 依然 apply (any input)，但**具体 bound 数值**可能不是 teleportation-simulable 的 simplification。

**严谨性**：**[CONJ, G1]**

### 2.2 Step 2: PLOB on effective channel

**Claim**: Apply PLOB 2017 Theorem 1 to $\tilde{\mathcal{M}}$:

$$R_\varepsilon^{\text{LOPC}}(\tilde{\mathcal{M}}) \leq E_R^\infty(\tilde{\mathcal{M}})$$

其中 $E_R^\infty$ 是 channel 的 regularized REE。

**Gap β.G2**: PLOB 2017 的 $E_R$ 是 **strong-converse regularized REE**。对于 $\tilde{\mathcal{M}}$ 这种 **3-output (A, B, c)**, **2-input (Alice-Bob)** channel，PLOB 原 statement 需要重新适配。特别是：
- PLOB 2017 Theorem 1 的 channel $\mathcal{N}: A \to B$ 是 point-to-point single-sender single-receiver
- $\tilde{\mathcal{M}}$ 是 2-to-2 broadcast channel（+ classical output $c$）
- **直接 apply 不成立** — 需要 "channel-reduction" lemma

**严谨性**：**[CONJ, G2]** — MAJOR gap，因为 PLOB 直接 apply 的 formal justification 缺失。

### 2.3 Step 3: Computing $E_R^\infty(\tilde{\mathcal{M}})$

**Claim**: 具体数值 $E_R^\infty(\tilde{\mathcal{M}})$ 作为 $\eta_A, \eta_B$ 的函数。

**Approach**: 
- $E_R^\infty$ 是 SDP (Wang-Duan 2016b, Berta-Wilde 2018 有 SDP hierarchies)
- 对 umr-topology, 需 SDP over Choi states of $\tilde{\mathcal{M}}$
- 实际数值计算 non-trivial

**Gap β.G3**: 即使 $E_R^\infty$ 可 bound，具体 $f(\eta_A, \eta_B)$ 的 closed form 未知。Log 07 §4.4 推测 $f(\eta_A, \eta_B) < -\log_2(1-\sqrt{\eta_A\eta_B})$（因为 Charlie measure-only 约束 loosens Eve's extractable）。但"紧 constant" 需 SDP solve。

**严谨性**：**[CONJ, G3]** — 数值上需 SDP; analytic bound 未知。

### 2.4 Step 4: Connection to original umr protocol

**Claim**: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\text{LOPC}}(\tilde{\mathcal{M}})$

**Justification**: $\Pi$ 的 per-round operations 是 $\tilde{\mathcal{M}}_\text{full}$ 的 specialization (specific LOCC choices after seeing $c$); $\Pi$ 的 rate $\leq$ optimal LOPC rate over $\tilde{\mathcal{M}}$.

**Gap β.G4**: 虽然 "specialization ≤ optimal" 是 standard optimization argument, **Eve model** 的转换需注意:
- $\mathcal{A}_\text{umr}$: Eve 持有 channel environments $E_1, E_2$ + Charlie register
- LOPC 下 Eve 只持 channel environments
- LOPC 更强 (给 Alice-Bob 更多 operations)，但 Eve 更弱 (没有 Charlie register)
- 两者 trade-off 实际上 **复杂**：Eve 更弱 → rate 更高 → 上界不 tight
- 所以 $R^\text{LOPC}(\tilde{\mathcal{M}}) \geq R^{\mathcal{A}_\text{umr}}(\Pi)$ ← **direction 正确**（上界 inheritance）

**严谨性**：**[CONJ, G4]** — direction correct but needs rigorous transfer argument.

### 2.5 Step 5: Combine

Chain: $R^{\mathcal{A}_\text{umr}}(\Pi) \overset{\text{G4}}{\leq} R^\text{LOPC}(\tilde{\mathcal{M}}) \overset{\text{G2,PLOB}}{\leq} E_R^\infty(\tilde{\mathcal{M}}) \overset{\text{G3}}{=} f(\eta_A, \eta_B)$

若 $f(\eta_A, \eta_B) < -\log_2(1-\sqrt{\eta_A\eta_B})$ (as Log 07 §4.4 推测), path β 给**更紧**上界 than Pirandola 2019 min-cut。

**严谨性**：**[CONJ conditional on G1-G4 resolved + G3 SDP computed]**

---

## 3. Gap summary

| Gap | 描述 | Severity | 升级所需 |
|---|---|---|---|
| β.G1 | Two-source → single bipartite input 合并 | MINOR | labeling / tensor reshape argument |
| β.G2 | PLOB 2017 apply to 2-to-2 broadcast channel | MAJOR | channel-reduction lemma; 用户纸笔 2-3 天 |
| β.G3 | $E_R^\infty(\tilde{\mathcal{M}})$ closed form unknown | MAJOR | SDP solve; 可能 analytic closed form 不存在 |
| β.G4 | Eve model 跨 topology 转换 | MAJOR | 用户 Portmann-Renner adaptation; 1-2 天 |

**Total: 4 gaps, 3 MAJOR + 1 MINOR**。estimated **5-7 人日**。

---

## 4. Comparison with path α and path γ

| Aspect | α (monotonicity) | β (channel-reduction) | γ v0.3 (single-edge PLOB + data-processing) |
|---|---|---|---|
| Core tool | Khatri-Wilde §19-20 monotonicity | Channel-reduction + PLOB on composite | PLOB on single edge + data-processing inequality |
| Primary ref | Khatri-Wilde 2020/2024 | PLOB 2017 + WTB 2017 | PLOB 2017 + Nielsen-Chuang |
| Bound scaling | $\sqrt{\eta_{AB}}$ (same as Pirandola) | possibly **tighter** than $\sqrt{\eta_{AB}}$ | $\sqrt{\eta_{AB}}$ (same as PLOB single-edge) |
| Gaps count | 11 (all [UNKNOWN]) | 4 (3 MAJOR) | 5 (4 MAJOR) |
| Risk of v1/v0.2 pattern recurrence | LOW (explicit 11 gaps) | MEDIUM (Eve model transfer G4) | LOW (avoid set-inclusion by construction) |
| Potential tightness | same as Pirandola 2019 | **better**! possibly strict inequality | same as Pirandola 2019 single-edge |
| Recommendation | scaffolding only (not yet derivation) | **highest research value** (new bound) | **safest baseline** (Log 07 recommendation) |

---

## 5. 严谨性

- 本文件 **[CONJ]**
- 4 gaps explicit
- **不**升级 任何分级
- 等 Codex review

## Changelog

- **v0.1** (2026-04-22 autonomous)：channel-reduction approach, 4 gaps identified
