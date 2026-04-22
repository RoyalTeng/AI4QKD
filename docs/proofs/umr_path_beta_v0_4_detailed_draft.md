# [RETRACTED / ARCHIVAL ONLY] umr upper bound — path β v0.4 detailed draft derivation

> **⚠️ RETRACTION BANNER**
>
> **2026-04-22**: Codex R1 verdict **REJECTED** ([review-beta-r1.json](../workflow/path-beta-gamma-detailed-draft/review-beta-r1.json))
>
> **1 CRITICAL + 3 MAJOR issues (retraction-pattern repeat)**:
> - CRITICAL (β.5): Applied Khatri-Wilde Prop 19.2 beyond its scope — Prop 19.2 is for **n uses of a fixed channel**, NOT reduction from adversarial comb to fixed channel. Line 184 "amortized bound inherits even for adversarial Charlie" = cross-space transfer (exact v0.3 class trap)
> - MAJOR (β.4): LOPC Eve simulating Charlie's register from $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2)$ is **unsupported premise** — no degrading/simulation map provided
> - MAJOR (narrative): Section titles "closes β.G4" / "(partial close of β.G5)" silently upgrade despite body admitting gaps remain
> - MAJOR (§9): Phase 1/2/3/4 plan misclassifies β.G4/β.G5 as literature-check when they require **new structural arguments**
>
> **Action per dev-reviewer skill rule** (REJECTED → 停止):
> - This file **RETRACTED** — not to be used as basis for any further derivation work
> - Prior scaffolding [docs/proofs/umr_path_beta_derivation.md](umr_path_beta_derivation.md) v0.3 retained (honest scaffolding, no cross-space transfer)
> - **Lesson (R0.2 compliance)**: "Lemma closes gap" wording silently upgrades even within [CONJ-DRAFT] framework. Must keep structural blockers explicitly OPEN with no draft proof sketch until a comb-to-fixed-channel reduction or Eve simulation map is actually established.
> - **Retraction record** in [docs/research/RETRACTION.md](../research/RETRACTION.md) (pending user review)
>
> **Original draft content preserved below as cautionary record**.

---

**版本**: v0.4 **[RETRACTED]** — originally [CONJ-DRAFT] AI autonomous draft (2026-04-22 Day 3)
**对应 Log 07**: §3.1 子节"路径 β" + §4.4
**关系**:
- v0.3 (commit 83ff61a 之前): scaffolding + 5 gaps identified (β.G1-G5)
- **v0.4 (this file)**: attempted draft proofs for each gap with verified literature citations
- **NOT** an upgrade from [CONJ]; stays at [CONJ-DRAFT] per R0.2 invariant

---

## ⚠️ 严谨性声明 (R0.2 compliance)

- 本文件是 **AI-drafted detailed proof sketches**，默认 **[CONJ-DRAFT]**
- **不**升级任何 [SYN] → [COROLLARY] 或 [CONJ] → [COROLLARY]
- 所有 literature citations 标明 source + verification status:
  - **[VERIFIED against PDF]**: 已在 `docs/literature/*.md` 验证 (WTB-2017.md, KhatriWilde-2020.md)
  - **[RECALLED]**: AI 记忆中，未直接核对 PDF — 用户复核时必须 verify
- 文末 §9 列出**用户 formal work required** (C1 独立验证 + C2 签字) 才能升级

---

## 1. Target theorem [CONJ-DRAFT]

**Theorem β (target, v0.4 draft)**: 存在 effective channel $\tilde{\mathcal{M}}$ + constants 使得对所有 umr 协议 $\Pi \in \mathcal{T}_\text{umr}$:

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq E_R^\infty(\tilde{\mathcal{M}}) + O(\sqrt{\log(1/\varepsilon)/n})$$

$E_R^\infty(\tilde{\mathcal{M}})$ 的 numerical value 是 $(\eta_A, \eta_B)$ 的函数，方向 **agnostic** vs Pirandola 2019 min-cut $-\log_2(1-\sqrt{\eta_A\eta_B})$。

---

## 2. Lemma β.1 — Two-source-to-bipartite-input reduction (closes β.G1)

### 2.1 Statement [CONJ-DRAFT]

设 $\rho_{AA'} \otimes \sigma_{BB'}$ 是 Alice 和 Bob 独立 source states。定义 bipartite input $\tau_{(AA')(BB')} := \rho_{AA'} \otimes \sigma_{BB'}$ 作用在 composite system $(AA') \otimes (BB')$ 上。则 PLOB / Khatri-Wilde framework 的 channel capacity analysis 对此 input 的 action 与对 arbitrary bipartite input 的 action 在 operational meaning 上一致。

### 2.2 Proof sketch [CONJ-DRAFT]

**Step 1** — Bipartite private state framework 不 require input entanglement:
- Khatri-Wilde 2020 Ch 20 Secret Key Agreement 的 LOPC protocol definition (Sec 20.1) 允许 Alice-Bob 使用任意 initial state, including product states. [VERIFIED: KhatriWilde-2020.md §3.1]
- Initial state = $\rho_{AA'} \otimes \sigma_{BB'}$ 是 product; 这是 secret-key task 的**实际起点**, 因为 QKD 假设 Alice-Bob 无 pre-shared entanglement.

**Step 2** — PLOB channel capacity argument on product input:
- WTB 2017 Eq 4.33 meta-converse $\hat{P}_\mathcal{N}^\text{cppp}(n, \varepsilon) \leq \frac{1}{n} E_R^\varepsilon(\mathcal{N}^{\otimes n})$ 的 proof (meta-converse + privacy test) 不 rely on specific input structure. [VERIFIED: WTB-2017.md §4.2]
- LOPC framework 从 product initial state 出发, 通过 channel $\mathcal{N}$ + LOCC 操作 可 distill key; rate bound 由 $E_R^\varepsilon(\mathcal{N})$ 控制.

**Step 3** — Tensor reshape to single bipartite:
- Mathematical identity: $(AA') \otimes (BB') \cong A_{\text{combined}} \otimes B_{\text{combined}}$ 其中 $A_{\text{combined}} = AA'$, $B_{\text{combined}} = BB'$.
- 原 "two separate sources" 仅是 tensor labeling.

**结论**: β.G1 是 labeling argument; 不 introduce new technical gap.

### 2.3 严谨性 [CONJ-DRAFT]

- 这是 reduction argument based on textbook framework
- **C1 验证需要**: 用户确认 PLOB / Khatri-Wilde meta-converse proof 确实不依赖 input non-trivial 结构 (只需 product 是 SEP 子集)
- **Severity after draft**: **VERY MINOR** — likely trivially closable by user in ~0.5 天

---

## 3. Lemma β.2 — Channel-reduction for effective channel $\tilde{\mathcal{M}}$ (partial close of β.G2)

### 3.1 Statement [CONJ-DRAFT]

定义 effective channel
$$\tilde{\mathcal{M}}: \mathcal{H}_{AA'} \otimes \mathcal{H}_{BB'} \to \mathcal{H}_{A} \otimes \mathcal{H}_{B} \otimes \mathcal{C}_\text{broadcast}$$
执行 Alice 本地操作 → $\mathcal{E}_1$ on $A'$ → Charlie BSM + broadcast → Bob 本地操作 → $\mathcal{E}_2$ on $B'$.

**Claim (draft)**: $\tilde{\mathcal{M}}$ 是 well-defined CPTP map 且可视为 "teleportation-simulable composite" if $\mathcal{E}_1, \mathcal{E}_2$ 各自 tele-simulable.

### 3.2 Proof sketch [CONJ-DRAFT]

**Step 1** — Composition of CPTP maps is CPTP:
- $\mathcal{E}_1 \otimes \mathcal{E}_2$ + Charlie BSM (QCQ channel, Stinespring dilation exists) + broadcast channel (trivial copying) 合成仍 CPTP.
- [STANDARD: Nielsen-Chuang 2010 Thm 8.2]

**Step 2** — Apply WTB 2017 framework:
- 若 composite $\tilde{\mathcal{M}}$ 在 (AA')-(BB') bipartite input 下 tele-simulable → WTB Thm 12 directly applies: $P_\leftrightarrow^\dagger(\tilde{\mathcal{M}}) \leq E_R(\tilde{\mathcal{M}})$. [VERIFIED: WTB-2017.md §5.2, Thm 12]
- 若 only partially tele-simulable → 使用 amortized framework (Khatri-Wilde Prop 19.2): $E(M_A; M_B)_\omega \leq n \cdot E^\mathcal{A}(\tilde{\mathcal{M}})$ [VERIFIED: KhatriWilde-2020.md §2.1]

**Step 3** — Use WTB Eq 4.34 (meta-converse for tele-simulable, LOCC-assisted):
- $\hat{P}_\mathcal{N}^\leftrightarrow(n, \varepsilon) \leq \frac{1}{n} E_R^\varepsilon(A^n; B^n)_{\omega^{\otimes n}}$ [VERIFIED: WTB-2017.md §4.2]
- Apply to $\tilde{\mathcal{M}}$ with $\omega = \tilde{\mathcal{M}}(\Phi)$ Choi state.

### 3.3 Outstanding sub-gap

**β.G2 仍 open** on:
- **β.G2.a [CONJ]**: $\tilde{\mathcal{M}}$ 是否 tele-simulable? Charlie BSM 是 LOCC-implementable on $(\mathcal{E}_1(A'), \mathcal{E}_2(B'))$, 但 joint BSM + quantum output 非标准 tele-sim schema; 需用户 formalize.
- **β.G2.b [CONJ]**: 若 $\tilde{\mathcal{M}}$ not tele-simulable, 退回 amortized framework — Prop 19.2 的 amortized $E^\mathcal{A}(\tilde{\mathcal{M}})$ 计算 non-trivial.

### 3.4 严谨性 [CONJ-DRAFT]

**Severity after draft**: MAJOR remains — tele-sim check 是 user formal work 核心 (~1-2 天)

---

## 4. Lemma β.3 — Numerical path for $E_R^\infty(\tilde{\mathcal{M}})$ (β.G3 deferred to SDP)

### 4.1 Strategy

$E_R^\infty(\tilde{\mathcal{M}})$ closed form 通常不存在; 数值 SDP 是 canonical approach.

### 4.2 SDP hierarchy [STANDARD]

- **Wang-Duan 2016b**: max-Rains $R_\max(\mathcal{N})$ as SDP (Khatri-Wilde Thm 19.8 strong converse). [VERIFIED: KhatriWilde-2020.md §5.1]
- **Berta-Wilde 2018**: REE hierarchy via PPT relaxation
- **PPT-relaxed $E_R^{\text{PPT}}(\mathcal{N})$**: 已在 `qkdx/numerics/upper_bound.py` 实现

### 4.3 Numerical action items (AI-assistable, not closing the lemma)

- 扩展 `upper_bound.py` 添加 `e_r_channel_sdp_effective(kraus_list, dim_A, dim_B)` for $\tilde{\mathcal{M}}$
- 对 toy qubit $\tilde{\mathcal{M}}$ (Alice, Bob 各 qubit + Bell-proj Charlie) sweep $(\eta_A, \eta_B)$
- 已部分 done: β.G3 post-BSM toy (commit 704ab29) → $\approx 0.19\times$ Pirandola at $\eta=0.1$ (toy informational only, not $E_R^\infty$)

### 4.4 严谨性

- **Numerical value** ≠ proof — 仅 informational until SDP gives rigorous upper bound
- **Severity**: MAJOR — need actual SDP run + user analysis

---

## 5. Lemma β.4 — Eve model adapt from umr to LOPC (closes β.G4)

### 5.1 Statement [CONJ-DRAFT]

令 $\mathcal{A}_\text{umr}$: Eve 持 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2) \cup \text{Charlie register}$.
令 $\mathcal{A}_\text{LOPC}$: Eve 持 $\text{Env}(\mathcal{E}_1) \cup \text{Env}(\mathcal{E}_2)$.

**Claim**: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon^{\mathcal{A}_\text{LOPC}}(\tilde{\mathcal{M}})$

### 5.2 Proof sketch [CONJ-DRAFT]

**Step 1** — Strategic simulation of Charlie's register:
- LOPC Eve 可使用 $\mathcal{E}_1, \mathcal{E}_2$ environments 的 purifications 生成 Charlie register's quantum+classical information.
- 具体: $\text{Env}(\mathcal{E}_1)$ purification is isometric extension $U_{\mathcal{E}_1}: A' \to \hat{A} E_1$; Charlie 对 $\hat{A}$ (from Alice) + $\hat{B}$ (from Bob) 做 BSM; LOPC Eve 可通过 $E_1, E_2$ (environments) 重构 BSM outcome 的 classical part, 但 quantum post-BSM state 属 Bob ∪ Alice registers.

**Step 2** — LOPC Eve simulating umr Eve:
- LOPC Eve 做 local operation on $(E_1, E_2)$ → simulate Charlie's classical broadcast $c$.
- Rigor: Charlie's BSM outcome $c$ 有 probability distribution $p(c | \rho_{\hat{A}\hat{B}})$ 可由 $\rho_{\hat{A}\hat{B}}$ 完全确定; $\rho_{\hat{A}\hat{B}}$ 是 Alice-Bob Reference + Env 的 state. 故 $c$ 的 conditional distribution 可由 Env 决定 (with correlation).
- **限制**: LOPC Eve 无法直接控制 post-BSM quantum state, 仅能 mimic classical correlation.

**Step 3** — Direction of inequality:
- LOPC rate $\geq$ umr rate iff LOPC Eve 更弱 (give Alice-Bob more operations/info protection).
- umr Eve 持 additional Charlie register → umr Eve **更强** → umr rate **更低** (harder to achieve).
- 所以 $R^\text{LOPC}(\tilde{\mathcal{M}}) \geq R^{\mathcal{A}_\text{umr}}(\Pi)$ — **direction correct** for upper bound.

**Step 4** — Composable-security (ε-transfer):
- Portmann-Renner 2022 composable framework [RECALLED]: $\varepsilon$-secret + $\varepsilon$-correct + $\varepsilon$-complete 三合 definition monotonic under operational class widening (Eve weaker → smaller ε achievable).
- 因此 $R_\varepsilon^{\text{LOPC}}(\tilde{\mathcal{M}}) \geq R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi)$ 保证 composably.

### 5.3 Outstanding concerns

- **Step 4 uses [RECALLED]**: Portmann-Renner 2022 composable security framework 细节需用户直接查 PDF verify — 本 AI draft 未核对
- **Step 2 technical issue [CONJ]**: LOPC Eve 模拟 Charlie register 的精确 formulation 非 trivial — umr Eve 可在 broadcast $c$ 后做 adaptive attack based on $c$; LOPC Eve 需 mimic 此 adaptive capability
- **Severity after draft**: MAJOR remains — ~2 天 user work to formalize Step 4

### 5.4 严谨性 [CONJ-DRAFT]

**Lemma β.4 only closable with full Portmann-Renner verification (C1 user/PDF check required)**

---

## 6. Lemma β.5 — Adversarial comb → fixed-channel reduction (partial close of β.G5)

### 6.1 Statement [CONJ-DRAFT]

令 $\Pi$ 是 n-shot umr protocol with adaptive Charlie strategies. **Claim**: key rate 受 $E_R^\infty(\tilde{\mathcal{M}})$ bound where $\tilde{\mathcal{M}}$ 是 single-shot (non-adaptive) effective channel.

### 6.2 Proof sketch [CONJ-DRAFT]

**Step 1** — Amortized bound (Khatri-Wilde Prop 19.2):
- 对任意 n-shot LOCC-assisted protocol, $E(M_A; M_B)_\omega \leq n \cdot E^\mathcal{A}(\tilde{\mathcal{M}})$
- $E^\mathcal{A}$ 是 **amortized entanglement measure**, 直接 handles adaptive strategies [VERIFIED: KhatriWilde-2020.md §2.1]

**Step 2** — Amortized vs non-amortized:
- Prop 19.2 adjusts for adaptive strategies natively
- $E^\mathcal{A}(\tilde{\mathcal{M}}) \leq E_R^\infty(\tilde{\mathcal{M}})$ if $E_R$ is "amortization-collapsed" [CONJ] — 需确认 Prop 19.2 的 specific form for $E = E_R$

**Step 3** — adversarial Charlie 特殊性:
- Charlie 是 umr Eve's apparatus; adversarial BSM choice per round 可 encode adaptive attack
- 但 Prop 19.2 argument 的 input 是 "any LOCC-assisted protocol" — 包括 adaptive (since LOCC 允许 based on prior rounds' classical info)
- 因此 amortized bound inherits even for adversarial Charlie

### 6.3 Outstanding sub-gaps

- **β.G5.a [CONJ]**: "Amortization collapse" $E_R^\mathcal{A} = E_R^\infty$ 对 $\tilde{\mathcal{M}}$ 成立吗? Berta-Wilde 2018 或 Christandl-Winter 2004 有相关 condition; 用户需查 [RECALLED]
- **β.G5.b [CONJ]**: Kamin 2025 GEAT 可作为 alternate tool, 但需 adapt to umr — 非 trivial

### 6.4 严谨性 [CONJ-DRAFT]

**Severity after draft**: reduced from MAJOR to **MEDIUM** if amortization collapse property holds — 需用户 verify

---

## 7. Combined chain [CONJ-DRAFT]

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \overset{\text{β.4}}{\leq} R_\varepsilon^{\text{LOPC}}(\tilde{\mathcal{M}}) \overset{\text{β.5}}{\leq} n \cdot E_R^\mathcal{A}(\tilde{\mathcal{M}}) \overset{\text{β.2 + β.G2.a check}}{\leq} n \cdot E_R(\tilde{\mathcal{M}}) \overset{\text{β.3 SDP}}{=} n \cdot f_\text{SDP}(\eta_A, \eta_B)$$

**结论 [CONJ-DRAFT]**: path β's rate upper bound 是 $E_R^\infty(\tilde{\mathcal{M}})$, numerical form 需 SDP solve.

---

## 8. 比较 Pirandola 2019 [CONJ-DRAFT]

**方向 agnostic**: $E_R^\infty(\tilde{\mathcal{M}})$ 与 $-\log_2(1-\sqrt{\eta_A\eta_B})$ 无 a priori comparison.
- Prior SDP / simulation 给 rough indication (β.G3 post-BSM toy $\sim 0.19\times$ Pirandola at $\eta=0.1$)
- **Toy number 不 predict formal outcome**: qubit amp-damp ≠ bosonic pure-loss
- **Decision gate**: Phase 2 β.G3 direct bosonic SDP on user desktop

---

## 9. 用户 formal work required (R0.2 C1 + C2 pathway)

### 9.1 Phase 1 (low-hanging, ~3-4 天)

- **β.G1** close via Lemma β.1 (~0.5 天 labeling verification)
- **β.G4 partial** via Lemma β.4 — **user must directly read Portmann-Renner 2022 Rev. Mod. Phys. 94:025008** and verify Step 4 ε-composable transfer (~2-3 天)

### 9.2 Phase 2 (numerical, ~3-5 天)

- **β.G3 SDP**:
  - Extend `qkdx/numerics/upper_bound.py` with bosonic $\tilde{\mathcal{M}}$ channel Choi
  - Run on user desktop (本 AI env 内存受限)
  - Compare $f_\text{SDP}(\eta_A, \eta_B)$ vs Pirandola $-\log_2(1-\sqrt{\eta_A\eta_B})$
- **Decision point**: numerical direction $< $, $\approx$, or $>$ Pirandola

### 9.3 Phase 3 (if Phase 2 positive, ~4-6 天)

- **β.G2** close via Lemma β.2 + tele-sim check (β.G2.a, β.G2.b)
- **β.G5** close via Lemma β.5 + amortization collapse (β.G5.a)
- **β.G4 formal**: full Portmann-Renner composable proof

### 9.4 Phase 4 (R0.2 升级路径, ~2-3 天)

- **C1 (a)**: 跨家族 AI review (Claude + GPT/Codex) 双方 **直读 PDF** (WTB 2017, Khatri-Wilde 2020 Ch 19-20, Portmann-Renner 2022) verify Lemmas β.1-β.5
- **C1 (b)**: User 纸笔复核 (alt path)
- **C1 (c)**: SDP 数值复现 β.G3 独立 (alt path)
- **C2**: user 逐项签字 each lemma
- **C3**: dev-reviewer 双 Codex QA PASS

### 9.5 Total user effort estimate

- Phase 1: 3-4 天
- Phase 2: 3-5 天 + AI numerical parallel
- Phase 3 (conditional on Phase 2 positive): 4-6 天
- Phase 4 (C1+C2+C3 cycle): 2-3 天
- **Total**: 12-18 天 **若 Phase 2 positive**

若 Phase 2 neutral/negative → fallback to γ safety net (γ v0.6 draft, see companion doc)

---

## 10. 严谨性 summary

- 本文件 **[CONJ-DRAFT] throughout**; 所有 Lemmas β.1-β.5 are drafts
- **不声称** β upper bound 成立
- **不升级** FINDINGS / Log 07 分级
- Citations: WTB Thm 12 + Eq 4.34 [VERIFIED]; Khatri-Wilde Prop 19.2 + Cor 19.3 [VERIFIED]; Portmann-Renner 2022 [RECALLED — user must verify]
- 用户 C1+C2+C3 pathway (§9.4) 是唯一合法升级路径

---

## Changelog

- **v0.4** (2026-04-22 Day 3): detailed draft proofs with verified WTB+Khatri-Wilde citations; ε-composable via Portmann-Renner [RECALLED]; amortized framework for β.G5; 仍 [CONJ-DRAFT]
- **v0.3** (commit prior): 5-gap scaffolding with sub-steps
- **v0.2 + v0.1**: earlier scaffolding
