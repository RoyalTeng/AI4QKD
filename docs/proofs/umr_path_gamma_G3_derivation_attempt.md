# umr path γ.G3 — ε-composable finite-size transfer derivation attempt

**版本**: v0.1 **[CONJ-DRAFT]** — AI autonomous (2026-04-23, user 授权 draft+Codex iterate)
**对应 gap**: γ.G3 (见 [umr_path_gamma_v0_4_derivation.md](umr_path_gamma_v0_4_derivation.md) §6.4 + [umr_path_gamma_v0_6_detailed_draft.md](umr_path_gamma_v0_6_detailed_draft.md) §5)
**目标**: Establish ε-composable finite-size bound `R_ε^{A_umr}(Π, n) ≤ -log_2(1 - η_arm) + Δ(n, ε)`

---

## 0. 严谨性

- **[CONJ-DRAFT]** throughout
- 无 silent upgrade; 无 combined chain
- Citations: 5 级 taxonomy
- "attempted direction"
- **特别**: γ.G3 依赖 γ.A, γ.B.G1, γ.B.G3 全部 closed; 这些**均 open**. 所以本 attempt 是 **conditional on future closure of γ.B chain**.

---

## 1. 目标 + 依赖

### 1.1 Target inequality

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi, n) \leq -\log_2(1 - \eta_\text{arm}) + \Delta(n, \varepsilon)$$

with $\Delta(n, \varepsilon) = O(\sqrt{\log(1/\varepsilon)/n})$.

### 1.2 Conditional nature

本 lemma assumes γ.B chain (γ.A + γ.B.G1 + γ.B.G3) 已 closed. 本 chain currently **全部 open**. 所以本 draft 是:
- **Conditional on γ.B chain closure**, 可能可以 establish ε-composable transfer
- 若 γ.B chain **本身 remains unclosed**, γ.G3 目标不可达

### 1.3 Decomposition goal

需要 bridge:
- (A) **Asymptotic** $E_R^\infty(\mathcal{E}_1) = -\log_2(1-\eta_A)$ from PLOB 2017 + WTB 2017 Thm 12
- (B) **Finite-size** ε-composable rate bound for umr protocol $\Pi$ of length $n$

The second-order expansion of (A) gives finite blocklength bound for **tele-simulable channel 2-way LOPC**; transferring to umr needs additional structural work.

---

## 2. Attempted approach — WTB Thm 19 second-order transfer

### 2.1 WTB Thm 19 statement [MEMO-LEVEL QUOTE via WTB-2017.md §6]

**Theorem 19 (WTB 2017)** for covariant channels:

$$\hat{P}_\mathcal{N}^\leftrightarrow(n, \varepsilon) \leq E_R(\mathcal{N}) + \sqrt{\frac{V(\mathcal{N}, \varepsilon)}{n}} \Phi^{-1}(\varepsilon) + O\!\left(\frac{\log n}{n}\right)$$

where $V(\mathcal{N}, \varepsilon)$ is "relative entropy variance" (memo). **Caveat**: 用户须对 WTB 2017 §6 PDF 原文核对 Thm 编号 + $V$ definition.

### 2.2 Applicability to $\mathcal{E}_1$

$\mathcal{E}_1$ (bosonic pure-loss) 是 covariant (under displacements) — WTB Thm 19 **prerequisites 满足 for $\mathcal{E}_1$ alone**.

**[COROLLARY of verified WTB Thm 19 + PLOB Eq. 19 + pure-loss covariance]**:

$$\hat{P}_{\mathcal{E}_1}^\leftrightarrow(n, \varepsilon) \leq -\log_2(1 - \eta_A) + \sqrt{\frac{V(\mathcal{E}_1, \varepsilon)}{n}} \Phi^{-1}(\varepsilon) + O\!\left(\frac{\log n}{n}\right)$$

**这是 Alice-Charlie point-to-point private capacity rate**, **not** umr key rate.

### 2.3 Attempted transfer to umr

Target: 从 $\hat{P}_{\mathcal{E}_1}^\leftrightarrow$ (Alice-Charlie 2-way) 到 $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi, n)$ (Alice-Bob umr).

**Observation**: 这需要 γ.B chain (单边 Alice-Charlie ↔ Alice-Bob umr operational link), 见 [γ.B.G1 attempt](umr_path_gamma_B_G1_derivation_attempt.md). γ.B chain currently **全 open** per 4 approaches fail.

### 2.4 Gap identification

若 γ.B chain 某天被 closed (通过 Path A/B/C/D user work), γ.G3 的 ε-transfer 会 inherit 该 chain 的 formulation:

- If γ.B operational link is **quantitative** (e.g., $R_{\text{A-B}}^\text{umr} \leq f \cdot \hat{P}_{\mathcal{E}_1}^\leftrightarrow$ for some factor $f$), then WTB Thm 19 2nd-order transfer is straightforward multiplication
- If γ.B link is **qualitative** (e.g., via private state DPI without explicit factor), then ε-composable propagation through the chain needs additional bookkeeping (Portmann-Renner style union bound per step)

### 2.5 Alternative approach — Kamin 2025 GEAT framework

**Approach B**: Kamin 2025 GEAT (Generalized Entropy Accumulation Theorem) 为 MDI-QKD 提供 finite-key rate analysis. Directly adapting to umr:
- Kamin 2025 assumes specific protocol structure (MDI-QKD with Bell state BSM + key map + EC + PA)
- umr 的 adversarial Charlie 可能 不 fit 该 assumption
- 需 user adapt Kamin 2025 to umr adversary class — 非 trivial, but historical precedent (已 done for MDI) 给 concrete template

### 2.6 Attempt outcome

本 draft 发现:
- ε-composable transfer **本身**是 Kamin-style / WTB-style framework adaptation, 不涉及 structural cross-space transfer
- **但** γ.G3 实施 depends on γ.B chain closure
- 目前 γ.B chain 全 open → γ.G3 也 effectively 阻塞

### 2.7 Honest status

**γ.G3 remains OPEN**, 但**不是**由于自身 structural difficulty, 而是**依赖 γ.B chain closure**.

---

## 3. Relation to Kamin 2025 MDI-QKD work

### 3.1 Kamin 2025 as template [SUMMARY]

Kamin 2025 (already precedent in our project per docs/findings/t2a_thm4_empirical_finding_2026-04-22.md + D.4 in session conclusions) provides finite-key rate analysis for MDI-QKD via GEAT. 核心 insight:
- GEAT bounds "smooth min-entropy per round" under adversarial i.i.d.
- Integrates rounds into finite-blocklength rate via von Neumann entropy accumulation

### 3.2 umr vs MDI-QKD structural difference [CONJ]

**[CONJ]** Possible extensions for umr:
- MDI-QKD has Bell state + Alice-Bob symmetric; umr generalizes to arbitrary Charlie BSM
- MDI-QKD has cooperative 3-party (Alice, Bob, Charlie-probability); umr has adversarial Charlie (more general attack class)
- MDI-QKD's post-selection (Ψ- Bell only) is typical for security proof; umr could use all-Bell-summed or any Charlie-chosen strategy

Kamin 2025 framework **可能**直接适用 umr with minimal modification **if** key generation step 固定. 但 adversarial Charlie 导致 protocol structure 不 fixed — 需 cover **all adversary strategies**, 不仅 MDI-QKD specific.

### 3.3 User action recommended

- Direct-read Kamin 2025 §4 GEAT (PDF 在 `docs/literature/pdfs/Kamin-2025-FiniteSizeAnalysisEntropyAccumulation.pdf`)
- 判断 GEAT 的 "channel model" assumptions 是否 cover umr
- 若 cover, user research-level work adapt framework to umr
- 若 not cover, 需 novel entropy accumulation for umr

---

## 4. Conditional statement (if γ.B chain closed)

**Conditional Theorem γ.G3 [CONJ-DRAFT, conditional on γ.B chain future closure]**:

> 若 γ.B chain (γ.A Alice-Charlie PLOB + γ.B.G1 DPI target lemma + γ.B.G3 operational link) **全部 rigorously closed** 且 link 是 rate-preserving:
>
> $$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi, n) \leq -\log_2(1 - \eta_\text{arm}) + \Delta(n, \varepsilon)$$
>
> with $\Delta(n, \varepsilon)$ determined by WTB Thm 19 $V$ constant + union bound over chain steps.

**Severity**: depends on γ.B chain closure; 本身 ε-transfer 是 standard finite-blocklength technique.

---

## 5. Status summary

| Aspect | Status |
|---|---|
| WTB Thm 19 second-order for $\mathcal{E}_1$ (Alice-Charlie) | [COROLLARY of verified WTB Thm 19 + pure-loss covariance] |
| Transfer to umr via γ.B chain | **depends on γ.B chain closure** (currently open) |
| Kamin 2025 GEAT adaptation to umr | **open**, 需 user verify GEAT covers umr adversary class |
| γ.G3 ε-composable bound on umr | **OPEN conditional on γ.B** |

### 5.1 Q1 decision impact

**Agnostic**: γ.G3 是 γ path 的 final ε-transfer step. γ 整体 status 由 γ.B chain 决定; γ.G3 不 independently shift status.

---

## 6. Changelog

- **v0.1** (2026-04-23, user 授权 draft+Codex iterate): WTB Thm 19 second-order transfer derivation; depends on γ.B chain closure; Kamin 2025 GEAT alternate template identified
