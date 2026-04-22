# umr upper bound — path γ 真版 derivation (v0.3, NOT v0.2 adversarial containment)

**版本**：v0.3 **[CONJ]** — AI autonomous derivation (2026-04-22)
**对应 Log 07**：§4.5 (scaling exponent 上界 — "最弱但最可靠的" 路径)
**NOT v0.2**：**完全不同**于 2026-04-21 retracted adversarial containment approach
**用途**：为 Log 07 path γ 真版提供 derivation attempt；所有 gap 显式

---

## 0. 严谨性声明

- AI autonomous derivation → default **[CONJ]**
- **11 gap 显式 marked** in the derivation chain
- 若任一 gap 未由用户纸笔 close（C1(b)）→ 保持 [CONJ]
- 必须避免 v0.2 "adversarial containment set-inclusion" 陷阱（见 [umr_data_processing_gamma.md §-1](umr_data_processing_gamma.md) retraction notice）

**关键 diff 对 v0.2**：
- v0.2: 声称 $\mathcal{A}_\text{tr} \subseteq \mathcal{A}_\text{umr}$ set-inclusion shortcut — **rejected** (两 Eve 集合不在同 Hilbert 空间)
- v0.3 (本文件): **不** invoke set-inclusion；完全走 **single-edge PLOB + explicit data-processing lemma** (Log 07 §4.5 approach)

---

## 1. 目标 Theorem 陈述 [CONJ]

**Theorem γ (v0.3 target)**: 对所有 $\Pi \in \mathcal{T}_\text{umr}$（标准 umr protocol: Alice + Bob + untrusted Charlie measurement relay），composable $\varepsilon$-secret key rate 满足:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1 - \eta_\text{arm}) \quad \text{where } \eta_\text{arm} = \min(\eta_A, \eta_B)$$

其中：
- $\eta_A$：Alice → Charlie 透过率
- $\eta_B$：Bob → Charlie 透过率
- $\mathcal{A}_\text{umr}$：umr Eve class (Charlie 被 Eve 完全控制)

**Scaling 推论**：对称 $\eta_A = \eta_B = \eta_\text{arm}$，high-loss limit $R \leq \frac{\eta_\text{arm}}{\ln 2} + O(\eta_\text{arm}^2)$，而 $\eta_\text{AB} = \eta_\text{arm}^2$，故 $R \leq \frac{\sqrt{\eta_{AB}}}{\ln 2} + O(\eta_{AB})$ at $\eta_\text{AB} \ll 1$。

这给 **Log 05 TF-QKD achievable $\sqrt{\eta_{AB}}$ scaling** 同阶的 converse 上界。

---

## 2. Derivation chain (attempted proof)

### 2.1 Step 1: Alice-perspective reduction

**Claim**：考虑 Alice 的 single channel $\mathcal{E}_1: A' \to \hat{B}_1$（Alice's photon mode → Charlie-side post-channel mode）。 **任何** umr 协议 $\Pi \in \mathcal{T}_\text{umr}$ 对 Alice-Bob 之间可提取的 secret key 在 $\mathcal{A}_\text{umr}$ 模型下**最多** equals Alice-single-channel 下能提取到的 "某个 remote secret key"，**by Alice-perspective 看** Bob 是 Eve + Charlie + 整个 post-Charlie system 的一部分。

**Claim formulation**: Define "Alice-perspective 视角下 Alice 与 Bob 的 shared key" 为：
- Alice 手持 Alice register $A$
- "Bob side + everything else" 合并成 single super-register $\tilde{B} = (B, \text{Charlie's register}, \text{Eve's total ancilla})$
- Alice-$\tilde{B}$ LOPC 下的 secret-key capacity

**Sub-claim**：$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\text{Alice-vs-}\tilde{B}\text{-LOPC}}(\mathcal{E}_1)$

**Gap γ.G1**: "Bob, Charlie, Eve 合成 $\tilde{B}$" 在 umr Eve 模型下，Bob 确实是合法方 (not Eve)，但他的 register 通过 Charlie 的 classical announcement 接收信息。把 Bob merge 到 $\tilde{B}$ 做 LOPC 是否 valid？形式上 **Alice-$\tilde{B}$ LOPC $\supseteq$ umr 协议 $\Pi$ 允许的 Alice-Bob LOPC** — 因为 LOPC 允许的操作 family 更大 (合并 Bob 给超 LOPC 更多余地)。所以 $R_\varepsilon^{\text{super-LOPC}} \geq R_\varepsilon^{\Pi}$ ✓ **direction correct**。但 formal justification 需要 composable security machinery (Portmann-Renner 2022)。**未 formalize**。

**严谨性**：**[CONJ, Gap γ.G1 未 close]**

### 2.2 Step 2: PLOB 2017 apply to single channel

**Claim**：对任何 point-to-point bosonic channel $\mathcal{E}$ with transmittance $\eta$，Pirandola-Laurenza-Ottaviani-Banchi 2017 给：

$$R_\varepsilon^{\text{LOPC}}(\mathcal{E}) \leq E_R^\infty(\mathcal{E}) = -\log_2(1-\eta)$$

其中 $E_R^\infty$ 是 regularized relative entropy of entanglement of the channel。

**依据**: PLOB 2017 Theorem 1 + 应用于 pure-loss bosonic channel (PDF §III)。**[THM]** — 原文明确声明。

**Apply to $\mathcal{E}_1$**: transmittance $\eta_A$，给 $R_\varepsilon^{\text{Alice-LOPC-on-}\mathcal{E}_1} \leq -\log_2(1-\eta_A)$。

**严谨性**：**[COROLLARY of PLOB 2017 Theorem 1]** — 单信道情形 PLOB 显式 apply。

**Gap γ.G2**: Step 2 的"Alice-LOPC" 是 Alice 与 remote Bob-Charlie-Eve 合成方的 LOPC；PLOB 2017 原 statement 是 point-to-point Alice-Bob LOPC。两者在**形式上**相同 (远端只是 label) — PLOB 不 care Alice 对面是谁，只 care channel 属性 + LOPC structure。**此 gap 实际可 close**，是 labeling 问题，not substantive。

### 2.3 Step 3: Combine Step 1 + Step 2

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \overset{\text{G1}}{\leq} R_\varepsilon^{\text{super-LOPC}}(\mathcal{E}_1) \overset{\text{G2+PLOB}}{\leq} -\log_2(1-\eta_A)$$

**对称假设**: By symmetric argument on Bob's single-channel $\mathcal{E}_2$:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\eta_B)$$

**Combine**:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq \min\{-\log_2(1-\eta_A), -\log_2(1-\eta_B)\} = -\log_2(1-\min(\eta_A, \eta_B))$$

**严谨性**：**[CONJ conditional on G1 + G2 resolved]**

### 2.4 Step 4: Data-processing lemma (Log 07 §4.5 明写要求)

**Claim (Log 07 §4.5)**：Eve 对 Alice→Charlie mode 做任意后续操作（including 联合 Bob-mode 做 BSM）**不会增加** Alice-Bob mutual information 的上界。

**Formal statement**:

> Data-Processing Lemma (γ.DP): 对 quantum channel $\mathcal{N}: A \to B$ 及任何 completely positive map $\Lambda: B \to B'$，如果 $\rho_{AB}$ 是 input-output state (via $\mathcal{N}$)，则
> $$I(A : \Lambda(B))_\rho \leq I(A : B)_\rho$$
> (mutual information 在 downstream channel 下非增)

**Standard ref**: Nielsen-Chuang 2010 Thm 12.11 ("Quantum data processing inequality")。 **[THM]** 标准 QI textbook fact。

**Apply**: $\mathcal{E}_1: A' \to \hat{B}_1$ 给 output mode 进到 Charlie 设备；Charlie (controlled by Eve) 对 $\hat{B}_1$ 做任何 operation $\Lambda$ → output $\hat{B}_1'$。 Eve 把 $\Lambda(\hat{B}_1)$ 与 Bob 的 mode 联合做 BSM → classical announcement $c$。

**Consequence**: 由 data-processing, $I(A : c)_\text{Alice-observe} \leq I(A : \hat{B}_1)_{\text{post-}\mathcal{E}_1} \leq -\log_2(1-\eta_A)$ (PLOB bound on mutual info)。

**Gap γ.G3**: 从 mutual information bound 到 $\varepsilon$-composable secret-key bound，需要 Devetak-Winter formula or equivalent. **未 explicitly handle** the ε parameter transfer. Needs Portmann-Renner 2022 framework.

**Gap γ.G4**: Charlie operation $\Lambda$ 可能 **entangle** $\hat{B}_1$ 与 Bob 的 mode (via BSM)；BSM 结果 $c$ 作为 classical side information 给 Alice-Bob；Alice 看 $c$ 后能 refine 对 Bob mode 的 inference。但**这个 refinement** 不增加 Alice-Bob mutual info (由 classical announcement 是 LOCC, LOCC non-increasing entanglement & secret-key) — 但**需要严格 proof** 不是直觉。

**Gap γ.G5**: "Data-processing 给 single-channel PLOB inherit 到 umr" 的数学形式：
- umr 的 effective Alice-Bob mutual info $\leq$ Alice-Charlie mutual info after $\mathcal{E}_1$ (by data-processing)
- Alice-Charlie mutual info $\leq$ PLOB bound $-\log_2(1-\eta_A)$
- **Claim**: Alice-Bob secret-key rate $\leq$ Alice-Charlie mutual-info bound 在 $\eta_A$
- 这个 claim **等效于 $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq E_R^\infty(\mathcal{E}_1)$**
- 但 $E_R^\infty$ 不等于 mutual info bound — PLOB 用 relative entropy of entanglement，not mutual info
- **Gap**: 连接两者需要 $E_R^\infty \geq I(A:B) - \log_2|A|$ 类型 chain rule — 但这个 chain 不 tight

**严谨性**：**[CONJ conditional on G3 + G4 + G5]**

### 2.5 Step 5: Summary scaling

$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\eta_\text{arm})$

For $\eta_\text{arm} \ll 1$: $-\log_2(1-\eta_\text{arm}) \approx \eta_\text{arm}/\ln 2$.

With $\eta_\text{AB} = \eta_\text{arm}^2$ (对称两臂独立):

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \lesssim \frac{\sqrt{\eta_\text{AB}}}{\ln 2} + O(\eta_\text{AB}) \quad \text{(scaling)}$$

**[CONJ, scaling level]** — 匹配 Log 07 §4.5 预期。

---

## 3. Gap summary table

| Gap ID | Gap 描述 | Severity | 升级所需 |
|---|---|---|---|
| γ.G1 | Super-LOPC inclusion formal | MAJOR | Portmann-Renner composable security framework; 用户纸笔 ~1-2 天 |
| γ.G2 | PLOB single-channel label agnosticism | MINOR | labeling argument; 可能可简单 close |
| γ.G3 | ε-composable bound transfer from mutual-info bound | MAJOR | Devetak-Winter or Portmann-Renner framework; 用户纸笔 ~1-2 天 |
| γ.G4 | Classical announcement $c$ non-increasing mutual info | MAJOR | Formal LOCC monotonicity argument; 标准但需书写 ~1 天 |
| γ.G5 | $E_R^\infty$ vs mutual info bridge | MAJOR | Tighter analysis or alternative chain |

**总计 5 gaps, 4 MAJOR**。estimated **3-5 人日** 纸笔工作 if pursued。

---

## 4. Diff 对 v0.2 retracted

| Aspect | v0.2 (REJECTED) | v0.3 (this file) |
|---|---|---|
| 核心论证 | $\mathcal{A}_\text{tr} \subseteq \mathcal{A}_\text{umr}$ set-inclusion | Single-channel PLOB + data-processing |
| 陷阱 | 两 Eve 集合不在同 Hilbert 空间 | 不 invoke set-inclusion, 只用 channel-level PLOB |
| Reviewer 判定 | UNSOUND (Claude + Codex both) | **TBD via Codex review** |
| Log 07 原意 match | **No** (§4.3 三 lemma 跳过) | **Yes** (§4.5 "最弱但最可靠") |

---

## 5. 严谨性

- 本文件 **[CONJ]** overall
- 5 gaps explicit
- **不**升级任何 [CONJ] → [COROLLARY]
- **不**改 FINDINGS / Log 07
- **不**对外 cite
- 等 Codex review 确认**不**含 v0.2-style 陷阱

---

## 6. Codex review 点

关键问题 (for Codex review):
1. 是否 avoid v0.2 set-inclusion 陷阱？
2. γ.G1 的 super-LOPC 论证 是否 correct direction？
3. γ.G4 / γ.G5 的 data-processing chain 是否 actually tight 对 scaling level?
4. 整体 chain $\text{Step 1} \to \text{Step 5}$ 在 [CONJ] 级别是否 coherent?
5. 若所有 5 gaps resolve, 是否 proof 成立? Or 仍有 hidden gap?

---

## Changelog

- **v0.3** (2026-04-22 autonomous, NOT v0.2 adversarial containment): Log 07 §4.5 path γ 真版 derivation attempt with 5 explicit gaps
