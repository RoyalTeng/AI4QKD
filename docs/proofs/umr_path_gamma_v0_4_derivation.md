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

### 2.2 Step B — DPI / LOCC-monotonicity **target lemma** (NOT cross-task capacity transfer)

**⚠️ v0.4 scope restriction (Codex R2 指示)**: v0.3/v0.4-initial 曾 propose $K_\text{A-B}(\Pi) \leq K_\text{A-C}^\text{LOPC}(\mathcal{E}_1)$ 作为 Step B claim — 这是**未 justified 的 cross-task capacity transfer** (different party sets + different security models)。

**Codex R2 verdict (FAIL)**:
> "Log 07 §4.5 only motivates a data-processing/correlation monotonicity step, but v0.4 upgrades that into the stronger cross-task claim $K_\text{A-B}(\Pi) \leq K_\text{A-C}^\text{LOPC}(E_1)$ between different party sets and security models. ... the proof still lacks a justified transfer from an Alice-Charlie capacity bound to the Alice-Bob umr key-rate setting."

**Response**: v0.4 (current) **downgrades** Step B 为**target DPI lemma** (不直接声称 cross-task capacity 转移):

**Step B Target (γ.DPI target)**:
> 存在一个 DPI/LOCC-monotonicity lemma 证明：**Eve 对 Charlie 收到的 Alice mode 所做的任何 downstream operations（含 joint quantum BSM with Bob's mode + classical broadcast）不能增加** Alice-Bob 在 $\mathcal{A}_\text{umr}$ 下可提取的 secret key rate **beyond** 对 Alice's output mode (post-$\mathcal{E}_1$) 所 bound 的 PLOB 限制。

**即**：lemma 只声称 "downstream operations non-increasing Alice-Bob secret key correlation"; **不**声称 $K_\text{A-B} \leq K_\text{A-C}$ 跨 task capacity 转移。

**Gap γ.B.G1** (**关键 gap**): 此 lemma 的 **严格 formulation** 需包含:
- 明确定义 "Alice-Bob secret key correlation" 的 operator-algebra formulation
- LOCC-monotonicity of 该 correlation under Eve's downstream operations (包括 Charlie's joint BSM + classical broadcast)
- 连接到 $E_R^\infty(\mathcal{E}_1) = -\log_2(1-\eta_A)$ 的 PLOB bound 的方式
- **不** 直接声称 cross-task capacity inequality

**Gap γ.B.G2**: Charlie 对 Alice mode 和 Bob mode 的 **joint BSM** 是 **quantum operation** (not classical downstream) — v0.3/v0.4-initial 错误地 classify as "classical". **正确描述**: BSM 是 joint quantum 操作，输出既有 quantum post-measurement state 又有 classical outcome $c$。lemma 必须 handle 这个 joint quantum+classical structure。

**Gap γ.B.G3** (subsume former DPI.G2): Bob 在 secret-key 任务中的角色在 Step A (Alice-Charlie point-to-point PLOB) 完全缺席 — 所以 Step A 的 PLOB bound $-\log_2(1-\eta_A)$ 是 Alice-Charlie bit capacity 的 bound，不是 Alice-Bob 的。**Step B lemma 必须建立两者之间的 operational 联系**，而不是简单 monotonicity。

**严谨性**：**[CONJ, γ.B.G1 + γ.B.G2 + γ.B.G3 all open]** — Step B 是 **target lemma 陈述**，不是 proof。

### 2.3 Step C — 预期 scaling conclusion (conditional on Step B target lemma)

**若** Step B target lemma 被 user formally established，**则**：
- Alice's mode-level PLOB bound $-\log_2(1-\eta_A)$ (Step A) 可 transfer 到 Alice-Bob secret-key rate bound
- Symmetric argument with $\mathcal{E}_2$ gives bound $-\log_2(1-\eta_B)$
- Combine: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\min(\eta_A, \eta_B))$

**严谨性**：**[CONJ conditional on Step B target lemma]** — 目前 Step B 只是 target statement，未 proof，所以 Step C 的 conclusion 也是 conditional。

### 2.4 Step D — ε-composable security ε transfer

**Gap γ.G3** (from v0.3): PLOB 2017 gives asymptotic capacity; ε-composable framework gives finite ε rate. 需 Devetak-Winter or Portmann-Renner-style ε transfer。**未 handled** at this scaffolding level。

**严谨性**：**[CONJ, γ.G3]**

### 2.5 Step E — Combine scaling **[conditional on γ.B.G1-G3 + γ.G3]**

**Conditional** on Step B target lemma 的 formal establishment + Step D ε-transfer:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\eta_\text{arm}), \quad \eta_\text{arm} = \min(\eta_A, \eta_B) \qquad \text{[CONJ]}$$

High-loss: $\approx \eta_\text{arm}/\ln 2 = \sqrt{\eta_{AB}}/\ln 2$ (for symmetric)

**注**: 本 Step E 的 inequality **依赖** Step B + Step D 的所有 gaps 被 close。任一 gap unresolved → Step E 不成立。本文件**不**独立声称此 inequality。

---

## 3. Gap summary (v0.4)

| Gap | 描述 | Severity | 升级所需 |
|---|---|---|---|
| γ.B.G1 (v0.4 R3) | Step B DPI target lemma: "downstream operations non-increasing Alice-Bob secret key correlation" + 连接 PLOB bound — 正式 lemma 陈述 + proof | **MAJOR** | Portmann-Renner composable framework; 操作定义 "Alice-Bob secret key correlation"; 2-3 天 |
| γ.B.G2 (v0.4 R3) | Charlie joint BSM 是 quantum+classical operation (non classical-only); lemma 必须 handle 这个 structure | **MAJOR** | quantum-channel framework; 1-2 天 |
| γ.B.G3 (v0.4 R3) | Alice-Charlie PLOB bound 与 Alice-Bob secret key 之间的 operational 联系 (不是 capacity transfer) | **MAJOR** | LOCC monotonicity + reduction argument; 2-3 天 |
| γ.G3 | ε-composable transfer (PLOB asymptotic → ε-bounded) | MAJOR | Devetak-Winter or Portmann-Renner; 1-2 天 |
| γ.G4 | Classical announcement $c$ LOCC processing (standard but needs writeup) | MINOR | Standard LOCC argument |

**Total: 5 gaps (4 MAJOR + 1 MINOR)**. v0.4 R3 改正: 前 γ.DPI.G1/G2 (涉及 cross-task capacity) 替换为 γ.B.G1-G3 (**仅 target DPI lemma**, 不声称 capacity transfer)

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

- **[CONJ]** overall / **scaffolding-only**
- **5 gaps explicit** (v0.4 R3 修正)
- **不**升级任何分级
- **v0.2 + v0.3 两种 cross-space 陷阱 都 avoid**; v0.4 R3 加上**未 claim cross-task capacity transfer**

---

## 6. v0.5 deepened sub-gaps (2026-04-22 Day 2, **user 选 γ safety net**)

γ path 作为 β 主攻的 fallback safety net; 若 β.G3 numerical 显示 β 不紧于 Pirandola, 则 γ 承担 baseline [COROLLARY] 升级。

### 6.1 γ.B.G1 (MAJOR) — Step B target DPI lemma formal formulation

**Precise statement**: Formally state: "Eve 对 Charlie 收到的 Alice mode 所做的任意 downstream operations（含 joint BSM with Bob mode + classical broadcast）**不能增加** Alice-Bob secret key correlation 超过对 Alice's output mode 的 PLOB bound。"

**Sub-steps**:
- **Step 6.1.1** (~1 天): Operator-algebra formulation: define "Alice-Bob secret key correlation" as **bipartite private state distance** (Horodecki 2005, PRL 94:160502). 
- **Step 6.1.2** (~1 天): LOCC monotonicity of private state distance: 标准定理 (Horodecki 2005, Thm 2)。关键 check: umr 下 Charlie classical broadcast $c$ 是 **公共 classical** 信道，对 Alice-Bob LOCC structure 是 **side info**, 保 monotonicity.
- **Step 6.1.3** (~1 天): 连接: Alice-Charlie PLOB bound $E_R^\infty(\mathcal{E}_1)$ bound Eve 可提取信息; 通过 monotonicity, Alice-Bob 的 secret key correlation 受同 bound。

**Literature reference**:
- Horodecki 2005, "Secure key from bound entanglement", PRL 94:160502
- Khatri-Wilde 2020 §15 bipartite private state framework
- PLOB 2017 Theorem 1

**Severity**: MAJOR, **~2-3 人日**

### 6.2 γ.B.G2 (MAJOR) — Charlie joint BSM 是 quantum+classical operation

**Precise statement**: Charlie 对 (Alice mode, Bob mode) 做 BSM 是 **joint quantum operation** (not classical). 输出: quantum post-state on (A, B) + classical outcome $c$. DPI lemma 必须 handle 此 structure.

**Sub-steps**:
- **Step 6.2.1** (~0.5 天): 形式化 BSM 为 quantum-to-classical-quantum (QCQ) channel: $\mathcal{B}: \hat{A} \otimes \hat{B} \to \mathcal{A}_\text{post} \otimes \mathcal{B}_\text{post} \otimes \mathcal{C}_\text{classical}$
- **Step 6.2.2** (~1 天): BSM 可被 "dilated" 到 purely quantum operation via Stinespring (classical $c$ 等同 quantum register with orthogonal basis). 应用 quantum DPI.
- **Step 6.2.3** (~0.5 天): quantum DPI 给: $I(A : \mathcal{B}(\hat{A}, \hat{B}))_\rho \leq I(A : \hat{A})_\rho = I(A : \mathcal{E}_1(A))_\rho \leq$ PLOB bound。

**Literature reference**:
- Nielsen-Chuang 2010 Thm 12.11 (quantum data processing inequality)
- Wilde 2017 QIT textbook §11.9 (QCQ channels + DPI)

**Severity**: MAJOR, **~1-2 人日**

### 6.3 γ.B.G3 (MAJOR) — Alice-Charlie PLOB bound ↔ Alice-Bob key rate operational link

**Precise statement**: PLOB 给 **two-way private capacity** on single channel Alice↔Charlie. Need connect to **Alice-Bob secret key rate** in umr (different party set).

**Sub-steps**:
- **Step 6.3.1** (~1 天): 关键观察: umr 的 key generation 是 Alice-Bob (not Alice-Charlie). Bob 的 info 来自 Charlie broadcast (classical) + Bob own measurements on $\hat{B}$ (post-$\mathcal{E}_2$).
- **Step 6.3.2** (~1 天): 分两路:
  - (i) 对称: repeat argument with $\mathcal{E}_2$ replaced — 给 $-\log_2(1-\eta_B)$ bound.
  - (ii) Combine: min over two channels.
- **Step 6.3.3** (~1 天): Rigorous via bipartite private state framework: Alice-Bob secret key $\leq$ min of each point-to-point bound.

**Literature reference**:
- Log 07 §4.5 (用户原文 intuition)
- Khatri-Wilde 2020 Prop 15.2

**Severity**: MAJOR, **~2-3 人日**

### 6.4 γ.G3 (MAJOR) — ε-composable transfer

**Precise statement**: PLOB 2017 asymptotic capacity → $\varepsilon$-composable finite rate

**Sub-steps**:
- Apply Devetak-Winter finite-size framework, or Portmann-Renner composable wrap.

**Severity**: MAJOR, **~1-2 人日** (可能借用 Kamin GEAT 2025 结果)

### 6.5 γ.G4 (MINOR) — Classical announcement LOCC processing

**Sub-steps**:
- Standard LOCC monotonicity argument; Horodecki 2009 §V.

**Severity**: MINOR, **~0.5 天** (textbook)

### 6.6 Summary γ user workload

| Sub-gap | AI-assistable? | 用户人日 |
|---|---|---|
| γ.B.G1 | partial (literature pointer) | 2-3 |
| γ.B.G2 | partial (framework pointer) | 1-2 |
| γ.B.G3 | partial | 2-3 |
| γ.G3 | substantial (Kamin 2025 可直接 use) | 1-2 |
| γ.G4 | textbook (AI 可起草 draft) | 0.5 |
| **Total** | | **6.5-10.5 人日** |

**Matches early estimate 5-7 人日 if user reuses Kamin + textbook results liberally**。γ 工期比 β 短 **if** β.G3 numerical 发现 β ≥ Pirandola (这时 γ 兜底 + user 节省 β.G2+G5 工时)。

---

## 7. γ as safety net — decision point

γ 触发条件 (user workflow):
1. β Phase 1 (β.G1 + β.G4) close → proceed
2. β Phase 2 (β.G3 numerical): **AI computes E_R^∞(M_tilde) sweep**
3. 若 result < Pirandola min-cut → β promising, continue β.G2 + β.G5
4. 若 result ≥ Pirandola → **fallback γ**:
   - β.G1 + β.G4 work **部分 reusable** for γ (Portmann-Renner framework identical)
   - γ.B.G1 + γ.B.G2 + γ.B.G3 **新工作** ~5-8 人日
   - 总工期: β Phase 1 (~3-4 天) + γ fallback (~5-8 天) = **~8-12 天 total** (vs β 完整 10-15 天)

---

---

## 6. Changelog

- **v0.4 R3 FIX** (2026-04-22 Round 3): 响应 Codex R2 FAIL — Step B 从 cross-task $K_\text{A-B} \leq K_\text{A-C}^\text{LOPC}$ capacity transfer **downgrade** 到 DPI target lemma; Charlie BSM 明确为 quantum+classical joint operation (不是 classical-only); gaps 由 2 → 3 (γ.B.G1-G3)
- **v0.4 R2** (2026-04-22 Round 2 FIX): 响应 Codex R1 FAIL — 删除 v0.3 super-receiver merge; 严格按 Log 07 §4.5 写 point-to-point PLOB + separately stated DPI lemma
- **v0.3** (2026-04-22): v0.3 super-receiver merge approach — **Codex R1 FAIL**: Bob merged with Eve fuses honest receiver with adversary; 删除
- **v0.2** (2026-04-21): adversarial containment set-inclusion — **retracted** 2026-04-21 per Claude audit + Codex audit
- **v0.1** (2026-04-21): initial three-lemma attempt, 保守 [DRAFT]
