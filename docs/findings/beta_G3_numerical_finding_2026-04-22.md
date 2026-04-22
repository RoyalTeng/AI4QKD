# β.G3 numerical exploration — toy qubit model [CONJ exploratory]

**版本**：v0.4 **[CONJ, exploratory numerical only]** (2026-04-22 R2 FIX 响应 Codex R1 REJECTED)
**日期**：2026-04-22 Day 2 late evening autonomous
**定位**：**toy-model 探索性 numerical signal**；**非** β.G3 definitive answer；不作为"β path 是否值得做" 决定依据

---

## 0. 严谨性 scope

### 0.1 本文件 IS

- **toy qubit single-rail exploration** (amp-damping channel as approximate pure-loss analog)
- 一种 **directional signal** 关于 E_R(β's effective channel) 可能的量级
- Numerical exercise at **[CONJ]** 级，**不**改变任何 path 的 formal 状态

### 0.2 本文件 IS NOT

- **NOT** a physical MDI model (see §0.3 scaling mismatch)
- **NOT** a proof that $E_R(\tilde{\mathcal{M}}_\beta) < $ Pirandola bound
- **NOT** a justification to "fast-track β" — 该决定**仍**依赖 formal β.G1-G5 gap closure + desktop bosonic SDP

### 0.3 Known model limitations (Codex R1 明示)

- **p_BSM scaling mismatch**: 本 toy 模型给 $p_{\Psi-}(\eta_\text{sym}) = \eta(2-\eta)/4$（低 η 线性）— 与 physical MDI linear-optic BSM 的 $p \sim \eta^2/2$（二次）**不符**。原因：amp-damp 把 "loss" 等同于 $|0\rangle$ 吸收，非 vacuum mode ejection
- **Single-rail vs dual-rail**: real MDI photons 是 dual-rail polarization encoded; 本 toy 是 single-rail qubit
- **No HOM dip model**: Hong-Ou-Mandel 干涉 visibility 未 model
- **No dark count / misalignment**
- **Qubit abstraction vs bosonic CV**: real 协议 bosonic; 结果 direction 可能 differ

### 0.4 对 β path formal 决策的 bearing

**本 numerical signal 本身 不足以** make the β-vs-Pirandola comparison definitive。真实 answer 依赖:
- β.G1-G5 formal gap closure (用户纸笔)
- β.G3 direct E_R^PPT SDP on **bosonic pure-loss** model (desktop)

本文件**只**给 directional plausibility,不 justifies fast-tracking β over γ safety net.

---

## 1. Three toy-model variants

本 numerical exploration 尝试了三种 qubit 近似 for β's effective channel $\tilde{\mathcal{M}}$：

| Variant | Model assumption | 含 LOCC? | Script | 结果 ratio to Pirandola at η=0.1 |
|---|---|---|---|---|
| A. Tensor-product upstream | $E_1 \otimes E_2$ (parallel amp-damp) | **No** (LOCC 未 apply) | [beta_G3_analytical_log_negativity.py](../../scripts/beta_G3_analytical_log_negativity.py) | **1.81** (松) |
| B. Werner heuristic | 把 loss 替换为 depolarizing, Werner reduction | Yes | [beta_G3_mdi_effective_channel_werner.py](../../scripts/beta_G3_mdi_effective_channel_werner.py) | **0** (artifact, η<0.5 E_R=0) |
| C. Post-BSM projection (toy) | amp-damp + project(A',B')→Bell + trace | Yes | [beta_G3_post_BSM_conditional_amp_damp.py](../../scripts/beta_G3_post_BSM_conditional_amp_damp.py) | **0.19** (all-Bell summed) |

**All three are toy qubit models with caveats** (see §0.3). None is definitive for physical MDI.

---

## 2. Canonical comparison convention (R2 FIX: pick one)

**Codex R1 正确指出**: `0.094×` (Ψ⁻ only) vs `0.19×` (all-Bell summed) 在 v0.1/v0.2/v0.3 不 consistent。R2 FIX 固定 **单一 canonical convention**:

**Canonical**: **Summed over all 4 Bell outcomes**（$\Phi^\pm, \Psi^\pm$）— 对应 **ideal 4-outcome Bell measurement** (not linear-optic 2-outcome)。

$$\text{β per-round bound}^\text{canonical} = \sum_c p_c \cdot \text{LN}(\rho_{AB|c})$$

其中 $c$ 遍历四个 Bell state。**这是本文件的 main comparison quantity**。

**Other conventions 作 sensitivity**（非 main claim）—— **R3 FIX** 以实测数值替换早期 handwave:
- **Ψ⁻ only**: 0.0949× Pir at η=0.1 (实测 commit c214fe3 log verify; used in v0.3 initial prose — R2 移除作 main claim)
- **Linear-optic BSM (Ψ± 接受)**: 0.1899× Pir at η=0.1 — **与 all-Bell summed 同值**，因为 Φ± outcome 在本 toy model 下给 **separable** conditional state (LN=0)，不贡献。**非** "2/4 × all-Bell" naive 假设
- Physical MDI (Ψ± + post-selection on HOM dip): 需要 separate modeling (本 toy 未含)

**R2 决定**：整个文件以 all-Bell-summed convention (0.19× plateau) 为 main reference;只在 §3 sensitivity subsection 提及 其他 convention 数值。

---

## 3. Canonical toy-model data (Variant C, all-Bell summed)

Data from [docs/research/data/beta_G3_post_BSM_sweep.csv](../research/data/beta_G3_post_BSM_sweep.csv), plot [docs/research/figures/beta_G3_post_BSM_vs_pirandola.png](../research/figures/beta_G3_post_BSM_vs_pirandola.png):

| η_arm | Σ_c p_c · LN_c (Variant C) | Pirandola reference | ratio |
|---|---|---|---|
| 0.001 | 2.7×10⁻⁴ | 1.4×10⁻³ | 0.188 |
| 0.01 | 2.7×10⁻³ | 1.5×10⁻² | 0.188 |
| 0.10 | 2.9×10⁻² | 1.5×10⁻¹ | 0.190 |
| 0.50 | 0.187 | 1.00 | 0.187 |
| 0.95 | 0.927 | 4.32 | 0.215 |

**观察**: ratio ≈ 0.19 plateau stable across η ∈ [0.001, 0.5].

**Caveat**: 这个 "per-round bound" 用 $p_c$ 来 average LN, 不等价于 $E_R$ of 完整 effective channel (那个需要 Choi-level SDP)。$E_R^\infty(\tilde{\mathcal{M}})$ 与 $\sum_c p_c \cdot \text{LN}(\rho|c)$ 不严格相等；差异取决于 channel structure 如何处理 classical outcome c.

### 3.1 Sensitivity: other conventions (non-canonical)

**R3 FIX: 用实测数值替换 R2 handwave**。at η=0.1:

**Per-outcome breakdown** (直接 compute from script verify):
- $p_{\Psi^-} = p_{\Psi^+} = 0.0475$, $\text{LN}(\rho|\Psi^\pm) = 0.3038$, contribution each = 0.0144
- $p_{\Phi^-} = p_{\Phi^+} = 0.4525$, $\text{LN}(\rho|\Phi^\pm) = 0$ (conditional state separable in toy model)

**Sensitivity conventions**:
- **Ψ⁻ single outcome** (early v0.3 claim): $p_{\Psi^-} \cdot \text{LN}_{\Psi^-} = 0.0144$, ratio **0.0949× Pir** at η=0.1 — 只取 1/4 outcome 丢 Ψ+ 对称贡献
- **Linear-optic BSM (Ψ± accepted)**: $\sum_{c \in \{\Psi^\pm\}} p_c \cdot \text{LN}_c = 0.0289$, ratio **0.1899× Pir** at η=0.1 — **与 all-Bell summed 实际同值**，因为 Φ± outcome 在本 toy model 下给 **separable** conditional state (LN=0)
- **All 4 Bell ideal** (canonical): same 0.0289, ratio **0.1899×** — 与 Ψ± 相等 (Φ± 不贡献)
- **E_R (rather than LN)**: E_R ≤ LN typically，所以 $\sum p_c \cdot E_R \leq $ 0.19× Pir — AI 未 compute E_R 直接 (需 SDP)

**关键修正** (R3 vs R2): 早前 §2 写 "Ψ±=0.13×" 和 §3.1 写 "2/4 × all-Bell = 0.10×" 两个数**都错**。正确实测: **Ψ± = all-Bell = 0.19×**, **Ψ- only = 0.0949×** (因为 Ψ+ 与 Ψ- 对称贡献，不是 1/4)。

**这些 sensitivity numbers 互相 consistent (after R3 re-computation)，但都是 toy qubit artifact，不应作 β path 的 definitive numerical verdict**。

---

## 4. Variant B (Werner heuristic) — explicit heuristic-only label

**v0.2 Werner 分析** (commit b2f4253):
- 把 pure loss 替换为 λ = 1-η depolarizing (**heuristic substitution**)
- 应用项目 Werner reduction [CONJ] 给 $W_{F'}$
- 算 $E_R(W_F) = 1 - H_2(F)$ for $F > 1/2$ (Rains 1999 标准)
- 结果:
  | η | E_R(W_F') | Pir | ratio |
  | 0.95 | 0.62 | 4.32 | 0.14 |
  | ≤0.50 | 0 | ≥1 | 0 (artifact) |

**Codex R1 correct critique**: Werner heuristic 把 loss 当 depolarizing 是 **不 physical** substitution; η ≤ 0.5 artifact (E_R=0) 非 genuine lower bound on β, 仅 **heuristic surrogate**。R2 标签修正: "Werner heuristic surrogate, **not** β lower bound".

---

## 5. Variant A (tensor-product upstream) — upper bound of β via LOCC monotonicity

Since Charlie BSM is LOCC, $E_R(\tilde{\mathcal{M}}_\beta) \leq E_R(\mathcal{E}_1 \otimes \mathcal{E}_2) \leq \text{LN}_{E_1 \otimes E_2}$.

So Variant A gives **valid upper bound on β's true bound**, but not tight (doesn't include Charlie BSM effect).

At η=0.1: LN_{E_1 ⊗ E_2} = 0.275 = 1.81 × Pirandola.

**结论**: 如果 $E_R(\tilde{\mathcal{M}}_\beta) \leq 0.275$ at η=0.1, β could potentially be tighter than Pirandola (0.152). 但 Variant A **only证明 β ≤ 2× Pirandola**, 不 prove β < Pirandola.

---

## 6. 综合 interpretation for user decision

Given **three toy qubit variants** (Variant A loose upper, Variant B heuristic surrogate with artifacts, Variant C toy post-BSM with wrong p_BSM scaling):

- **Variant C (0.19× plateau)** is the most detailed calculation 但 **p_BSM scaling incompatible** with physical MDI
- **Consistent direction**: LOCC reduces entanglement, Variant A → Variant C shows 1.81 → 0.19× reduction factor of ~10×
- **仍不 definitive**: 需 (a) physical p_BSM model + (b) direct SDP on bosonic CV

**β 是否 tighter than Pirandola** 的真实 answer **仍然 agnostic** per Log 07 §4.4:
- 方向上有 plausibility signal (Variant C at 0.19×)
- 但 model artifacts prevent 确 conclusion
- **必须 desktop bosonic SDP + β.G1-G5 formal** 才能 resolve

---

## 7. Updated user guidance (R2 FIX — agnostic)

**本文件 NOT 推荐 fast-track β**（R1 v0.3 过度 claim）:

- β 路径**仍 [CONJ] pending β.G1-G5 formal work** (~7-10 人日)
- **γ safety net 仍然 equally important** (numerical signal 不决定 formal 路径选择)
- Phase 1 β.G1 + β.G4 先做 (对 γ 也 useful) — unchanged
- Phase 2 desktop direct SDP + bosonic model 验证: **critical**, but the outcome **unknown**
- β.G3 numerical 本文件 仅提供 **plausibility** that β direction *could* give tighter bound; definitive proof 依赖 formal work

---

## Changelog

- **v0.4** (2026-04-22 R2 FIX per Codex REJECTED R1):
  - 主 convention 固定为 all-Bell-summed (0.19×); 移除 inconsistent "0.094×"作 main claim
  - Demote "definitive / real value / fast-track β" → "toy model [CONJ] exploratory"
  - Add §0.3 model limitations (p_BSM scaling, qubit vs bosonic)
  - Label Variant B as "heuristic surrogate" not "lower bound"
  - §6 interpretation 改 agnostic
  - §7 user guidance 改为 "β path remains [CONJ], numerical 不决定 fast-track"
  - Clean structure: 3 variants as subsections
- **v0.3** (2026-04-22 Day 2 evening, **over-claimed**): amp-damp post-BSM toy = "physical β bound ~0.094/0.19×"; **REJECTED by Codex R1**
- **v0.2** (2026-04-22 Day 2): Werner heuristic surrogate (labeled incorrectly as "lower bound"); **corrected in v0.4**
- **v0.1** (2026-04-22 Day 2 early): tensor-product upstream (valid upper bound of β)
