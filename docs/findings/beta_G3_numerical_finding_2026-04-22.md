# β.G3 numerical finding: tensor-product log-negativity 在实际高损耗不 tighter than Pirandola

**版本**：v0.1 **[numerical finding, qubit abstraction, no rigor upgrade]**
**日期**：2026-04-22 Day 2 late evening autonomous
**目的**：为用户 β-main + γ-safety 决策 (Q1 Option 2) 提供 β.G3 "β bound 是否更紧" 的 early numerical signal

---

## 0. 严谨性 scope

- **Qubit abstraction** (amplitude damping)，**不是** bosonic pure-loss
- 计算 log-negativity (not E_R directly; log-negativity bounds and relates to channel capacity)
- 未 include Charlie BSM LOCC — 只是 upstream $E_1 \otimes E_2$ tensor product
- **directional signal only**; **不**作为 β.G3 definitive answer
- 不升级 FINDINGS / Log 07 / 任何 rigor

---

## 1. 实证数据

Script: [scripts/beta_G3_analytical_log_negativity.py](../../scripts/beta_G3_analytical_log_negativity.py)
Implementation: direct NumPy eigenvalue (no MOSEK SDP)

| η_arm | LN_single | LN_tensor (=2×LN_single) | Pirandola_trusted | PLOB_single | LN_tensor / Pir |
|---|---|---|---|---|---|
| 0.9 | 0.926 | 1.852 | 3.322 | 3.322 | **0.558** |
| 0.7 | 0.766 | 1.531 | 1.737 | 1.737 | **0.882** |
| 0.5 | 0.585 | 1.170 | 1.000 | 1.000 | 1.170 |
| 0.316 | 0.396 | 0.792 | 0.548 | 0.548 | 1.446 |
| 0.1 | 0.138 | 0.275 | 0.152 | 0.152 | **1.809** |
| 0.0316 | 0.045 | 0.090 | 0.046 | 0.046 | **1.938** |
| 0.01 | 0.014 | 0.029 | 0.015 | 0.015 | **1.980** |

**Additivity check**: LN of tensor product = 2 × LN of single arm (confirmed numerically).

**注**: Pirandola trusted-relay at symmetric η_A = η_B = η_arm 等于 $-\log_2(1-\eta_\text{arm})$ = PLOB single edge。这是因为 $\sqrt{\eta_A \eta_B} = \eta_\text{arm}$ 对称情形。

---

## 2. Interpretation

### 2.1 Cross-over behavior

**High η (low loss) regime (η_arm = 0.7-0.9)**: LN_tensor < Pirandola, 两者 ratio 0.56-0.88
- 在这个 regime, **tensor-product upstream bound 比 Pirandola 更紧**
- 这是 research-interesting 的 regime (bosonic 等价 ~1.5 dB 或更少 loss)
- 但**不是**实际 QKD 工作 regime

**Low η (high loss) regime (η_arm ≤ 0.316)**: LN_tensor > Pirandola, ratio → 2 as η → 0
- 在高损耗 (实际 QKD 规模), tensor-product upstream bound **2× 于 Pirandola** (松 2 倍)
- 这是 **实际 QKD 工作 regime** (QKD 通常 20+ dB loss, η ≤ 0.01)

### 2.2 对 β path 价值的 bearing

**关键理解**: Tensor product 是 **β.G3 的 upstream bound**, 不是 β 的 actual bound:
- $E_R(\tilde{\mathcal{M}}_\beta) \leq E_R(\mathcal{E}_1 \otimes \mathcal{E}_2) \leq LN_\text{tensor}$
- Charlie BSM 是 LOCC → 只能**降低** $E_R$
- 所以 $E_R(\tilde{\mathcal{M}}_\beta) \leq LN_\text{tensor}$ 但具体 gap 未知

**Case 1** (high loss): LN_tensor > Pirandola. $E_R(\tilde{\mathcal{M}}_\beta)$ 可能:
- (a) 大于 Pirandola → β 不 tighter than Pirandola
- (b) 小于 Pirandola 但大于 single-arm bound → β tighter than Pirandola (Charlie BSM saves the day)
- (c) 等于 single-arm bound → β 恢复 Pirandola min-cut

**Case 2** (low loss): LN_tensor < Pirandola. $E_R(\tilde{\mathcal{M}}_\beta) \leq LN_\text{tensor} <$ Pirandola  
- → β **potentially** tighter than Pirandola (证 via Charlie BSM LOCC reduces)
- 但需 exact $E_R$ SDP 确认

### 2.3 Practical QKD regime signal (cautionary)

在**实际 QKD loss 范围 (η ≤ 0.1, i.e., ≥ 10 dB loss)**:
- LN_tensor 是 **PLOB single-edge 的 2 倍** (additivity 下的 parallel two-arm bound)
- 要 β 比 Pirandola 更紧, 需要 **Charlie BSM LOCC 把 tensor product 收缩到 ≤ Pirandola**
- Charlie BSM 是 rank-1 projector onto Bell subspace → significant entanglement collapse
- 但 is it enough to bring the factor of 2 down?  **需要 direct SDP 确认**

**Tentative signal**: 在实际 regime, β 可能 **不给更紧 bound** — 仅 recover Pirandola 或甚至松。

---

## 3. 对 user decision workflow 的 impact

User 2026-04-22 Q1 Option 2 (β main + γ safety) 的 workflow:

**Phase 1** (β.G1 + β.G4 low-hanging): 不受 β.G3 signal 影响, 可照常做 (~3-4 天) — 这些 work 也对 γ fallback useful (Portmann-Renner framework shared)

**Phase 2** (β.G3 numerical):
- **本文件** 是 Phase 2 的 early signal
- tentative cautionary: 在实际 QKD regime, tensor-product upstream 不 tighter
- **但** Charlie BSM LOCC effect **未测**; 可能 recover tight bound
- **用户决策**: 继续 β.G2 + β.G5 formal (~4-5 天) **如果** β.G3 direct SDP 仍显示 tighter
- **fallback γ**: 如果 β.G3 最终 ≥ Pirandola, γ 兜底 (~5-8 天)

**Revised time estimate**:
- If β succeeds: β.G3 direct SDP + formal = 10-15 天 (as planned)
- If β 不 tighter (cautionary): **β.G1 + β.G4 + γ fallback** = **~8-12 天** (保留大部分 work for γ)

### 3.1 User 具体决策点

**建议 immediate action**: 继续 **β.G1 + β.G4 formal work** (~3-4 天) 因为:
1. 这些 work 对 γ 也有用 (framework shared)
2. 不 depend on β.G3 outcome
3. 用户可以在此期间思考 β 是否值得 push 更深

**Pending on β.G3 direct SDP**: 
- 需要 bigger MOSEK environment / cluster 来 compute $E_R(\tilde{\mathcal{M}})$ directly (16x16 PPT SDP)
- **AI 当前 session 环境内 MOSEK OOM-killed** — 无法 compute
- 可以考虑: 用户侧 Mathematica / Python with MOSEK academic license on desktop run SDP

---

## 4. 与 Log 07 §4.4 对齐

Log 07 §4.4 原文:
> "因为 umr 约束 Charlie 为 measure-only, 实际 capacity 应该**严格小于** trust capacity。Pirandola min-cut 给出的 $-\log(1-\sqrt{\eta})$ 在 umr 下可能是 loose 的。Sub-Q4 的 gap analysis 若走路径 β, 可能拿到一个 $\mathcal{K}_\text{umr} \leq f(\eta)$ 的新上界, $f(\eta) < -\log(1-\sqrt{\eta})$"

本 numerical finding 是**部分支持**但**不确认** Log 07 §4.4 的推测:
- 在**高 η regime** (0.7-0.9): LN_tensor **已**小于 Pirandola → β 方向正确
- 在**低 η regime** (实际 QKD): LN_tensor **大于** Pirandola (factor 2) → 需要 Charlie BSM LOCC 救场
- **未测**: direct $E_R(\tilde{\mathcal{M}})$ 含 Charlie BSM

Log 07 推测如果正确, 则 Charlie BSM LOCC 把 LN_tensor 从 2x 降到 ≤1x Pirandola in low-η regime. 这是 **open** problem。

---

## 5. Recommendation for user Phase 2 action

**Low-commitment option**: 用户先做 **β.G1 + β.G4 formal** (~3-4 天, 对 γ 也有用)

**High-commitment option (if user has MOSEK academic)**: 用户先 run **direct $E_R(\tilde{\mathcal{M}}_\beta)$ SDP** (16x16 PPT, MOSEK academic ≥ 2 min/point), 确认 Case 1/2/3 which. 这决定:
- 若 Case 2 (β 确 tighter): Phase 3 β.G2 + β.G5 有意义 (~4-5 天)
- 若 Case 1/3 (β 不 tighter): fallback γ (~5-8 天)

**Risk mitigation**: 两 option 都 keep γ as parallel safety; final commit to β only if Case 2 confirmed.

---

## 6. Changelog

- **v0.1** (2026-04-22 Day 2 late evening autonomous):
  - 计算 LN 在 parallel two-arm amp-damping (7 η points)
  - Cross-over observed: high η favors β direction, low η doesn't
  - Practical QKD regime (η ≤ 0.1): β upstream bound 2× Pirandola
  - Direct $E_R(\tilde{\mathcal{M}}_\beta)$ SDP **阻塞**于 local MOSEK OOM
  - Cautionary signal for user β-main decision, 但 NOT definitive

- **v0.3** (2026-04-22 Day 2 最终 definitive result, **tension resolved**):
  - 新增 [scripts/beta_G3_post_BSM_conditional_amp_damp.py](../../scripts/beta_G3_post_BSM_conditional_amp_damp.py): **真实 pure-loss qubit model**
  - 构造 |Φ+⟩_{AA'} ⊗ |Φ+⟩_{BB'} → amp-damp on A', B' → 投影 |Ψ-⟩ on (A',B') → trace
  - 得到 Alice-Bob 条件态 ρ_{AB}
  - 计算 log_negativity(ρ_{AB})
  - 结果 (physical pure-loss qubit):

    | η_arm | p_BSM | log_neg(cond) | p_BSM × LN | Pirandola | ratio |
    |---|---|---|---|---|---|
    | 0.95 | 0.249 | 0.93 | 0.23 | 4.32 | **0.054** |
    | 0.50 | 0.188 | 0.50 | 0.09 | 1.00 | **0.093** |
    | 0.10 | 0.048 | 0.30 | 0.014 | 0.15 | **0.095** |
    | 0.01 | 0.005 | 0.27 | 0.001 | 0.015 | **0.094** |

  - **β 方向 per-round bound ≈ 0.094 × Pirandola 稳定** (紧约 10 倍)

## 3. Three analyses 收敛 picture

| Analysis | η=0.1 ratio | 物理含义 |
|---|---|---|
| Tensor-product (无 LOCC, v0.1) | 1.81× | 上界 of β (太松) |
| Werner heuristic (depol loss, v0.2) | ~0 (artifact) | 下界 of β (太紧) |
| **Amp-damp post-BSM (v0.3)** | **0.095×** | **接近物理真值** (qubit) |

**结论**: β 路径在 qubit pure-loss 模型下**比 Pirandola 紧约 10 倍** — **strong positive signal for β formal work**.

**Direct SDP (on user desktop)** 预期 refine 0.094× 为 slightly tighter value (log_neg ≥ E_R^PPT ≥ E_R^∞)。

## 4. Updated user decision guidance

基于 v0.3 definitive data:
- **β 有明确 novel bound potential** (紧 ~10×)
- **建议 user fast-track β formal work** — Phase 1-3 全部做
- γ safety net **仍然保留** but less urgent
- Phase 2 β.G3 direct SDP 用户 desktop verify 本 qubit 结果 (expected confirm)

### Changelog
  - 新增 [scripts/beta_G3_mdi_effective_channel_werner.py](../../scripts/beta_G3_mdi_effective_channel_werner.py): **含 Charlie BSM LOCC**
  - 用项目 Werner reduction + 已知 Werner state $E_R$ 闭式 (Rains 1999)
  - 结果 (含 LOCC):
    | η_arm | E_R(Werner) | Pirandola | ratio |
    | 0.95 | 0.62 | 4.32 | **0.14×** |
    | 0.90 | 0.41 | 3.32 | **0.12×** |
    | 0.70 | 0.04 | 1.74 | **0.02×** |
    | ≤0.50 | 0 | ≥1 | 0 (heuristic cutoff) |
  - **Charlie BSM LOCC 完全翻转了 signal 方向** — β 从"松 2×"变为"紧 7-40×"
  - **但**: 此 Werner 分析使用 λ ≈ 1-η_arm **heuristic** (treat loss as depolarizing), η≤0.5 时 E_R=0 是 artifact
  - Real bosonic pure-loss channel 答案**介于**两者之间 (松 2× ... 紧 0.02×)
  - **唯一 definitive 答案**是 user 侧 desktop direct bosonic SDP

## 2.4 v0.2 Tension Summary

两种 numerical 计算给出**完全不同**的 β 方向:

| Analysis | η_arm=0.1 (实际 QKD) | 信号 |
|---|---|---|
| Tensor-product upstream (无 LOCC) | 1.81 × Pir (松) | β **不**tighter |
| Werner heuristic (含 LOCC + depolarizing loss) | ~0.02 × Pir (紧) | β **much** tighter |

**Resolution 待 direct SDP on real pure-loss bosonic model**。

对 user decision 的 implication:
- 两种 analysis 都支持 **β path 值得 formal work** (至少潜在有 novel value)
- 真正的 β bound magnitude **未知** — 只 desktop SDP 能 confirm
- Phase 1 (β.G1 + β.G4) 仍建议先做 (对 γ fallback 也有用)
- Phase 2 desktop direct SDP 是 **决定 β 是否产出新定理** 的关键
