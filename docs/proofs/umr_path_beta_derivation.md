# umr upper bound — path β derivation (channel-reduction + PLOB/WTB on effective channel)

**版本**：v0.3 **[CONJ]** — AI autonomous scaffolding v0.3 (2026-04-22 Day 2 late evening, **user 决定选 β 作主攻** 后的深化 scaffolding)
**对应 Log 07**：§3.1 子节 "路径 β" + §4.4 ("direct umr converse via channel-reduction")
**用户决策引用**：[q1_decision_record_2026-04-22.md](../findings/q1_decision_record_2026-04-22.md) — β 主攻 + γ safety net

**v0.3 主要扩展**（相对 v0.2+R3）：
- 每个 β.G1-G5 gap 加 **sub-gaps + literature references + user action sub-steps**
- 新增 §6 **数值 roadmap**：E_R^∞(M_tilde) SDP 实施指导
- 新增 §7 **user formal work 推荐顺序** (按 gap 难度排序)
- 本文件仍 **[CONJ] / scaffolding-only**; **不**自我声称 derivation

---

## ⚠️ Round 2 FIX notice

[v0.1 Codex verdict (FAIL)](../workflow/paths-review/review-diff-1.json):
- MAJOR: "The derivation packages one honest-BSM round into a fixed CPTP map $\tilde{M}$, but the converse target is the full adaptive umr protocol class with adversarial Charlie. The current 4-gap list does not flag the missing reduction from that n-shot adversarial process/comb to repeated use of a fixed effective channel."
- MINOR: "Relative-tightness discussion stronger than Log 07 §4.4 supports; effective-channel REE could end up looser."

**Response (v0.2)**:
- 加入 **β.G5 adversarial-channel-reduction gap**
- 重写 §4 比较表为 agnostic ("could be tighter, comparable, or looser")
- 删除 "highest research value" overread

---

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

**Scaling 预期** (Log 07 §4.4 agnostic 表述, **v0.2 修正**)：$E_R^\infty(\tilde{\mathcal{M}})$ 的数值未知 — 可能 **小于** Pirandola 2019 min-cut bound (Log 07 §4.4 推测 direction)，**等于**，**或大于** (若 $\tilde{\mathcal{M}}$ 的 input dimensions / Eve workspace 反而放大 REE)。precise comparison 需要 SDP solve or analytic estimate。**v0.1 声称 "严格小于" 是 overread**, v0.2 修正 为 agnostic。

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

**Gap β.G3**: 即使 $E_R^\infty$ 可 bound，具体 $f(\eta_A, \eta_B)$ 的 closed form 未知。Log 07 §4.4 讨论 $f(\eta_A, \eta_B)$ 的数值未知；原文 agnostic：可能 smaller, comparable, or larger than Pirandola 2019 min-cut bound。v0.1 曾 overread "strictly smaller" — v0.2 修正。"紧 constant" 需 SDP solve 确定方向。

**严谨性**：**[CONJ, G3]** — 数值上需 SDP; analytic bound 未知; 方向未定。

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

$f(\eta_A, \eta_B)$ 的具体数值与 Pirandola 2019 min-cut bound $-\log_2(1-\sqrt{\eta_A\eta_B})$ 的**比较方向未定**：可能 smaller, comparable, or larger。需 SDP solve 或 analytic estimate 确定。path β 的 research 价值取决于该比较结果，**无法** a priori 声称 "更紧"。

**严谨性**：**[CONJ conditional on G1-G4 resolved + G3 SDP computed]**

---

## 3. Gap summary

| Gap | 描述 | Severity | 升级所需 |
|---|---|---|---|
| β.G1 | Two-source → single bipartite input 合并 | MINOR | labeling / tensor reshape argument |
| β.G2 | PLOB 2017 apply to 2-to-2 broadcast channel | MAJOR | channel-reduction lemma; 用户纸笔 2-3 天 |
| β.G3 | $E_R^\infty(\tilde{\mathcal{M}})$ closed form unknown | MAJOR | SDP solve; 可能 analytic closed form 不存在 |
| β.G4 | Eve model 跨 topology 转换 | MAJOR | 用户 Portmann-Renner adaptation; 1-2 天 |

**β.G5 (新增 v0.2, Codex R1 MAJOR)**: **Adversarial effective-channel reduction** —— 从 full adaptive adversarial Charlie umr class 到 "repeated use of a fixed CPTP map $\tilde{\mathcal{M}}$" 的 reduction。umr 是 **n-shot adversarial process/comb** (Eve/Charlie 可跨轮 adapt strategy based on all prior announcements)，不是 i.i.d. fixed channel。Kamin 2025 GEAT framework handle comb case via entropy accumulation; Pirandola 2017/2019 converse 用 teleportation stretching 把 comb 等效为 fixed channel — 但 **umr 的 Charlie 是 adversary，teleportation stretching 假设 honest cooperative structure**。此 reduction 未 established for umr。**MAJOR gap**; 可能需要 Portmann-Renner composable framework 或 Kamin GEAT 式处理。

**Total: 5 gaps, 4 MAJOR + 1 MINOR** (v0.2 加 β.G5)。estimated **7-10 人日** (revised upward after Codex R1)。

---

## 4. Comparison with path α and path γ

| Aspect | α (monotonicity) — scaffolding-only | β (channel-reduction) [this file] | γ v0.4+R3 (single-edge PLOB + DPI target lemma) |
|---|---|---|---|
| Core tool | Khatri-Wilde §19-20 monotonicity | Channel-reduction + PLOB on composite | PLOB on single edge (Step A) + DPI/LOCC-monotonicity target lemma (Step B) |
| Primary ref | Khatri-Wilde 2020/2024 | PLOB 2017 + WTB 2017 | PLOB 2017 + Nielsen-Chuang + Log 07 §4.5 |
| Bound scaling (targeted) | $\sqrt{\eta_{AB}}$ (same as Pirandola trusted-relay) | **unknown**: could be smaller, comparable, or larger vs Pirandola min-cut (per Log 07 §4.4 agnostic) | $\sqrt{\eta_{AB}}$ (conditional on target lemma) |
| Status (Codex R1-R4) | v0.2+R4: **scaffolding-only** record | v0.2+R3: 5 gaps at [CONJ] (β.G1-G5) | v0.4+R3: 5 gaps at [CONJ] (γ.B.G1-G3 + γ.G3 + γ.G4); Step E conditional |
| Risk of retraction pattern (historically observed) | HIGH — identity-embedding is same class as earlier retracted set-inclusion | MEDIUM — β.G5 adversarial-channel reduction open | MEDIUM — earlier cross-space traps avoided in current rewrite; Step B is target-only |
| Recommended next action | Await user纸笔 Portmann-Renner embedding + security-transfer (Lessons §4) | Close β.G5 (adversarial-channel reduction) + SDP numerical | Establish γ.B.G1-G3 DPI target lemma (user 形式化) |

---

## 5. 严谨性

- 本文件 **[CONJ] / scaffolding-only**
- **5 gaps explicit** (β.G1-G5)
- **不**升级 任何分级

---

## 6. v0.3 deepened sub-gaps + literature + user action sub-steps

### 6.1 β.G1 (MINOR) — Two-source → single bipartite input 合并

**Precise statement**: PLOB 2017 Thm 1 standard formulation 要求 **single bipartite input** $\rho_{AA'}$；umr 有 **two independent sources** $\rho_{AA'} \otimes \sigma_{BB'}$（Alice 与 Bob 的 source 独立, 因为 QKD 协议假设双方无 pre-shared entanglement）。

**Sub-steps to close**:
- **Step 6.1.1** (~0.5 天): 形式化 "two separate sources in LOPC context" = "single bipartite product-state input"（via tensor structure）
- **Step 6.1.2** (~0.5 天): 验证 PLOB 2017 Theorem 1 证明 step-by-step 不依赖 input 是 entangled，只依赖 tele-simulable channel 性质
- **Step 6.1.3**: 结论: β.G1 **实际上是 labeling**，可在 ~1 天内 close

**Literature reference**:
- PLOB 2017 §III.C (teleportation-simulable channels)
- Khatri-Wilde 2020 §15 (bipartite secret-key framework)

**Severity after sub-step analysis**: MINOR → ~1 人日

### 6.2 β.G2 (MAJOR) — PLOB 2017 apply to 2-to-2 broadcast channel

**Precise statement**: Standard PLOB 2017 Thm 1 是 **single-sender single-receiver point-to-point** channel $\mathcal{N}: A \to B$。$\tilde{\mathcal{M}}$ 是 **two-sender** (Alice, Bob) **three-output** (A, B, classical c) channel — formally 是 **multi-party broadcast channel with classical side channel**。

**Sub-steps to close**:
- **Step 6.2.1** (~1 天): 把 $\tilde{\mathcal{M}}$ 看作 Alice-to-(Bob, Charlie) 的 **broadcast channel**，其中 Bob input 作 **separate non-malleable side channel** (Bob's $B$ to $B$ identity). 这减少到 $\mathcal{E}_1: A \to (\hat{A}, c)$ effective，Bob 的 role 是 LOPC 下一方。
- **Step 6.2.2** (~1 天): 引用 **Wilde-Tomamichel-Berta 2017 §V.B** (broadcast channel strong converse) — WTB 扩展 PLOB 到 broadcast。
- **Step 6.2.3** (~1 天): 适用 **Khatri-Wilde 2020 Ch 20 secret key agreement** — bipartite private state framework 对 multi-output channel。

**Key decision point**: 使用 **WTB 2017** (broadcast converse) **或** **Khatri-Wilde 2020 Ch 20** (bipartite private state)。两条 framework 都可以但 details 不同。建议先试 WTB 2017 因为 single-letter 更强 (PLOB-style)。

**Literature reference stack**:
- WTB 2017, "Converse bounds for private communication over quantum channels", IEEE TIT 63(3):1792, arXiv:1602.08898 (Thm 12 已 VERIFIED against PDF in WTB-2017.md)
- Khatri-Wilde 2020, Ch 20 "Secret Key Agreement"
- Berta-Wilde 2018, "Weak converse for classical communication via entanglement", IEEE TIT 64(10):7220 (扩展 WTB framework)

**Severity**: MAJOR, estimated **2-3 人日**

### 6.3 β.G3 (MAJOR) — $E_R^\infty(\tilde{\mathcal{M}})$ 数值/闭式

**Precise statement**: 若 β.G1 + β.G2 close, target bound becomes $R \leq E_R^\infty(\tilde{\mathcal{M}})$。但 $E_R^\infty(\tilde{\mathcal{M}})$ 的 **具体数值** 作为 $(\eta_A, \eta_B)$ 函数 **未知**。

**Numerical roadmap** (AI autonomous 可做部分):
- **Step 6.3.1** (AI autonomous, ~0.5 天): 扩展 `qkdx/numerics/upper_bound.py` 增加 `e_r_channel_sdp(kraus_list, dim_A, dim_B)` 计算 single-letter $E_R(\rho_{\mathcal{M}})$ via Wang-Duan 2016b SDP hierarchy
- **Step 6.3.2** (AI autonomous, ~1 天): 对 toy $\tilde{\mathcal{M}}$ (qubit 版 Alice + qubit Bob + Bell-projection Charlie + binary classical outcome) 计算 $E_R^\infty$ 上界 via log-negativity
- **Step 6.3.3** (AI autonomous, ~1 天): 扫描 $(\eta_A, \eta_B)$ grid, 得到 $E_R$ vs Pirandola min-cut 对比图表
- **Step 6.3.4** (用户 ~1-2 天): 分析数值结果 — 是否显示 $E_R^\infty(\tilde{\mathcal{M}}) < -\log_2(1-\sqrt{\eta_A\eta_B})$? 若是, path β 潜在 novel bound.

**Literature reference**:
- Wang-Duan 2016b, "Semidefinite programming strong converse bounds for quantum channel capacity", IEEE TIT 62:2001, arXiv:1509.07127
- Berta-Wilde 2018 (above)
- Christandl-Winter 2004 (squashed entanglement definition; 与 $E_R$ 互补)

**Severity**: MAJOR, **用户工作 1-2 天** + **AI numerical 2-3 天**

### 6.4 β.G4 (MAJOR) — Eve model 跨 topology 转换

**Precise statement**: $\mathcal{A}_\text{umr}$ (Eve 控 $E_1, E_2$ + Charlie reg) vs LOPC Eve (只控 $E_1, E_2$)。目标证明 $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^\text{LOPC}(\tilde{\mathcal{M}})$.

**Sub-steps**:
- **Step 6.4.1** (~1 天): 观察 **umr = LOPC + Eve 额外 Charlie 控制 power**; 等价地, umr 是 LOPC 的特殊 strategy family (under umr Eve model).
- **Step 6.4.2** (~1 天): LOPC Eve 可 **模拟** umr Eve (用 $\mathcal{E}_1, \mathcal{E}_2$ environments 的 purifications 代替 Charlie register). 因此 "LOPC rate" ≥ "umr rate".
- **Step 6.4.3** (~1 天): 严格 Portmann-Renner composable framework formulate: $R_\varepsilon^{\mathcal{A}_\text{umr}}$ 定义下 $\varepsilon$ 是 secret + correct + complete 三合; transfer to LOPC $\varepsilon$ 保 monotonicity.

**Literature reference**:
- Portmann-Renner 2022, "Security in quantum cryptography", Rev. Mod. Phys. 94:025008
- Khatri-Wilde 2020 §15.1 (bipartite private states)

**Severity**: MAJOR, **2-3 人日**

### 6.5 β.G5 (MAJOR, Codex R1 新增) — Adversarial effective-channel reduction

**Precise statement**: umr 是 **n-shot adversarial process/comb**（Eve/Charlie 可跨轮 adapt strategy based on all prior announcements），不是 i.i.d. fixed channel。把 umr 等效为 "repeated use of fixed $\tilde{\mathcal{M}}$" 需要 reduction argument.

**Sub-steps**:
- **Step 6.5.1** (~1 天): 利用 **Kamin 2025 GEAT framework** 的 entropy accumulation technique, 每轮 effective $\tilde{\mathcal{M}}_i$ (allowing adaptive) bounded by single-round $E_R(\tilde{\mathcal{M}})$
- **Step 6.5.2** (~1 天): 替代: 使用 **Pirandola-style teleportation stretching** — 但 teleportation stretching 假设 cooperative structure; 需 check 在 umr 下 valid 吗?
- **Step 6.5.3** (~1 天): 最可能 framework: **Khatri-Wilde 2020 Ch 20 "secret key agreement over quantum channels"** — 含 amortized-Rains bound 处理 adaptive strategies.

**Literature reference**:
- Kamin 2025 §4 GEAT adaptation
- Khatri-Wilde 2020 Prop 20.6 (LOCC-assisted amortized bound)

**Severity**: **MAJOR**, **2-3 人日**

### 6.6 Summary of user work estimate

| Sub-gap | AI-assistable? | 用户人日 |
|---|---|---|
| β.G1 | partial (labeling argument) | 1 |
| β.G2 | partial (literature pointer) | 2-3 |
| β.G3 | **YES** (SDP numerical) | 1-2 (user analysis of AI-computed data) |
| β.G4 | partial (framework adaptation) | 2-3 |
| β.G5 | partial (framework choice) | 2-3 |
| **Total** | | **8-12 人日** |

(Matches early estimate ~7-10 人日; updated to 8-12 given β.G5 added)

---

## 7. User formal work 推荐顺序

**Phase 1** (low-hanging fruit): β.G1 + β.G4 sub-steps 6.4.1-6.4.3 (**~3-4 天**)
- β.G1 基本是 labeling
- β.G4 用 Portmann-Renner

**Phase 2** (core novelty question): β.G3 (**AI numerical ~2-3 天 + 用户 analysis ~1-2 天**)
- **关键 decision**: E_R^∞(M_tilde) 数值结果
- 若 **严格小于** Pirandola → continue to β.G2 + β.G5 for formal write-up
- 若 **≥** Pirandola → β 与 γ 等价, fallback to γ safety net

**Phase 3** (if Phase 2 positive): β.G2 + β.G5 formal write-up (**~4-5 天**)

**Phase 4**: dev-reviewer + C2 签字 (**~1-2 天**)

**Total**: **10-15 天** per decision flow

---

## 8. γ safety net sync (parallel)

若用户 Phase 2 (β.G3 numerical) 显示 $E_R^\infty(\tilde{\mathcal{M}}) \geq$ Pirandola (即 β 不紧于 Pirandola)，则 **fallback** to γ v0.4+R3 safety net. 详见 [umr_path_gamma_v0_4_derivation.md](umr_path_gamma_v0_4_derivation.md) + `docs/findings/q1_decision_record_2026-04-22.md`。

---

## Changelog

- **v0.3** (2026-04-22 Day 2 late evening, **user decided β 主攻**): deepen 5 gaps with sub-steps + literature + numerical roadmap; add §6-§8 for user formal work guidance
- **v0.2** (2026-04-22 Round 2 FIX): +β.G5 adversarial reduction; tightness agnostic
- **v0.1** (2026-04-22 autonomous)：channel-reduction approach, 4 gaps identified
