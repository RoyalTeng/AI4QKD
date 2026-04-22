# umr upper bound — path α (SCAFFOLDING-ONLY record; NOT a derivation)

**版本**：v0.2+R4 **[CONJ, scaffolding-only — NOT a derivation]** — AI autonomous (2026-04-22 Round 4 FIX cleanup)
**对应 Log 07**：§3.1 子节 "路径 α" + §4.3 "路径 α (monotonicity) 是正确路径,但需要写出来"
**Authoritative scaffolding**：[umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) v0.1

---

## 0. File purpose

本文件是 path α **scaffolding-only record**，**不** 声称包含 derivation。

- v0.1 (2026-04-22) 曾尝试 "attempted derivation" + 6-gap summary — **Codex R1 REJECTED**, **R2/R3/R4 共识**: identity-embedding 与 retracted v0.2 是同类 cross-space 陷阱
- **Authoritative 11-gap inventory**: 参阅 [umr_path_alpha_scaffolding.md §5](umr_path_alpha_scaffolding.md)
- 本文件**不** contain 独立的 derivation / 不独立 gap list；它只 record v0.1 回合的撤回 + 教训

**本文件内容**:
- §1: Target Theorem statement (reference only, 不 prove)
- §2: 撤回的 v0.1 derivation 的 quarantined appendix (cautionary record ONLY)
- §3: 本项目对 path α 当前立场 (scaffolding 指向)
- §4: 未来 derivation attempts 的 lessons

---

## 1. Target Theorem statement (reference only)

**Theorem α (unproved target)**: 对 $\Pi \in \mathcal{T}_\text{umr}$ 以 monotonicity reduction path (Khatri-Wilde §19-20 + PLOB 2017 继承):

$$R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B)) \quad \text{[UNPROVED TARGET]}$$

Scaling 推论（若证明成立）：$R \leq \sqrt{\eta_{AB}}/\ln 2 + O(\eta_{AB})$.

**当前状态**：**[UNKNOWN / UNPROVED]**。本 statement 的证明需要用户纸笔按 scaffolding 的 11 gaps 逐一 close。

---

## 2. Quarantined appendix — v0.1 (REJECTED 2026-04-22)

**⚠️ 以下 §2.1-§2.5 是 v0.1 的 "attempted derivation"，已被 Codex REJECTED 2026-04-22。仅作 cautionary record 保留。**

**⚠️ 读者请勿 interpret 以下内容为 proof。任何试图复用其 framework 都会再次落入 identity-embedding cross-space 陷阱。**

---

### 2.1 [RETRACTED] Step 1 — Protocol embedding $\iota$

**v0.1 尝试**: identity embedding of operations; 同 Hilbert 空间，不同 Eve 权限 attribution。

**RETRACTED reason** (Codex R1): 此 reframing 与 retracted v0.2 set-inclusion 属同类 cross-space 陷阱 (没有 formal Portmann-Renner embedding + security-transfer theorem)。

### 2.2 [RETRACTED] Step 2 — Monotonicity lemma (Khatri-Wilde Prop 19.2 / Cor 19.3)

**v0.1 尝试**: invoke Khatri-Wilde Prop 19.2 amortized entanglement framework apply to Alice-Bob-Charlie trusted-relay protocol; bound secret-key rate.

**RETRACTED reason**: Khatri-Wilde §19.2 是 point-to-point single channel; v0.1 把它 apply 到 stacked + Charlie-BSM 多方 scenario without proper extension derivation。

### 2.3 [RETRACTED] Step 3 — PLOB 2017 apply + channel-stack bound combine

**v0.1 尝试**: $E_R^\infty(\mathcal{E}_i) = -\log_2(1-\eta_i)$ + combine to $\min_i$.

**RETRACTED reason**: "$E^A_\text{stack} \leq \min_i E^A(\mathcal{E}_i)$" 论证 是 Pirandola 2019 min-cut 在 umr 下的继承问题 — 未 formalize。

### 2.4 [RETRACTED] Step 4 — Security reduction

**v0.1 尝试**: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq R_\varepsilon(\iota(\Pi))$ — umr Eve 更强 → 更低 rate → 上界继承。

**RETRACTED reason**: **关键** — 这是 v0.2 retraction 同类陷阱。direction + cross-space Eve inclusion 没有 Portmann-Renner 严格处理。

### 2.5 [RETRACTED] Step 5 — Combined chain

**v0.1 尝试**: $R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi) \leq -\log_2(1-\min(\eta_A, \eta_B))$ via Step 1-4 chain.

**RETRACTED reason**: entire chain is unsupported 因为 Step 1-4 全部 open 且 Step 4 是 retracted-class cross-space move。

**End of quarantined v0.1 appendix. ↑ 以上内容不作 proof 使用。**

---

## 3. Current authoritative position

path α 当前**没有** derivation at [CONJ] level。

**Authoritative gap inventory**: [umr_path_alpha_scaffolding.md §5 "综合 gap table"](umr_path_alpha_scaffolding.md) — **11 gaps, all [UNKNOWN]**。本文件 v0.2+R4 **不** introduce 独立的 gap list；scaffolding 是唯一 authoritative。

**Upgrade prerequisite**：用户 formal write L1 (Protocol embedding), L2 (Security reduction), L3 (Rate definition alignment) per Log 07 §4.3 + Portmann-Renner framework + Khatri-Wilde §19-20 — 预估 **10-15 人日** per scaffolding。任何 upgrade 仍需 R0.2 C1 ∧ C2 ∧ C3 invariant。

**严谨性**：**[CONJ / UNKNOWN]** for any α-related claim。**不** 升级 FINDINGS / Log 07 / 任何分级。

---

## 4. Lessons for future derivation attempts

**关键教训** (from v0.1 Codex R1 REJECTED):

> **任何声称 在 umr 与 trusted-relay 之间 做 "continuity" / "embedding" / "inclusion" / "monotonicity" / "reduction" 的 shortcut，无论措辞如何**（identity-embedding、super-receiver merge、adversarial containment 等），**都是 Portmann-Renner cross-space framework 的 un-closed gap**。

此类 shortcut 的 pattern (v1 FINDINGS / v0.2 γ / v0.1 α / v0.3 γ / v0.4-initial γ) 已多次被 Codex 捕获。**未来 derivation 必须** 先用用户纸笔 (C1(b)) 或等价 formal machinery 明写 cross-space protocol embedding + security-transfer lemma，**然后** 才能 invoke monotonicity。

**对应 scaffolding 中的 gap**：L1 (Protocol embedding) + L2 (Security reduction) 共同 handle 该 cross-space gap；**不能**将两者合并或绕过。

---

## 5. Changelog

- **v0.2+R4** (2026-04-22 Round 4 cleanup): 完全删除 derivation-style framing; §2 quarantined as REJECTED appendix; "6 gaps" + "derivation" 关键词全部去除；严格 scaffolding pointer
- **v0.2+R3** (2026-04-22 Round 3): 部分 cleanup — 保留了残余 "6 gaps explicit" 和 derivation sub-header (Codex R3 标记为 MAJOR)
- **v0.2+R2** (2026-04-22 Round 2): 最初 demotion 尝试，但保留 Step 1-5 作 cautionary
- **v0.1** (2026-04-22 autonomous, **REJECTED by Codex R1**): "attempted derivation" with 6-gap merged summary
