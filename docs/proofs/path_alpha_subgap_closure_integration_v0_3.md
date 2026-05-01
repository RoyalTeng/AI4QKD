# Path α Sub-Gap Closure — Integration Status Report v0.3

**版本**：v0.4
**日期**：2026-05-01（C2 user batch sign-off）
**前身**：
- [v0.3](path_alpha_subgap_closure_integration_v0_3.md)（2026-04-26 C3 batch round 2 post-fix）
- [v0.1 SUPERSEDED](path_alpha_subgap_closure_integration_v0_1.md)（C3 R1 holistic FAIL + diff REJECTED + Pirandola Eq. 11 citation 错揭露）
- [v0.2 SUPERSEDED](path_alpha_subgap_closure_integration_v0_2.md)（v0.2 是 R1 post-fix 即时版本，但 C3 R2 holistic 揭露未 propagate 到 later same-day state）

**类型**：**STATUS REPORT ONLY**（非 closure 文档；非 lemma proof；非升级请求）
**严谨性 banner**：本文件汇总 path α **12 sub-gap**（11 原 + L3.G2.E newly opened）的 C1(a) + C3 R2 round verdicts + post-split L3.G3 状态 + Pirandola Eq. 11 specialization chain caveat。**不**主张任何 sub-gap 已升级为 [COROLLARY]/[THM]；**不**主张 path α three-lemma combined chain 已 close；**不**得对外引用为定理级。

> **简写一览（首次出现给中文白话）**
> - **path α** = 12 sub-gap 路径策略，目标证 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 及其向 single-repeater bound 的 specialization
> - **C1 / C2 / C3** = 项目升级三闸门（独立验证 / 用户审签 / 第三方代码审查）
> - **C1(a)** = 跨家族 AI 直读 PDF（不同训练偏差源 AI 各自验证）
> - **L1.Gx / L2.Gx / L3.Gx** = path α 三 lemma（A / B / C）下的 sub-gap，编号源自 [umr_path_alpha_lemma_skeletons_v0_1.md](umr_path_alpha_lemma_skeletons_v0_1.md) §3-§5
> - **L3.G2.E** = 2026-04-26 newly opened sub-gap，从原 L3.G3 sub-residual 4 (channel-use accounting) split-out 而来
> - **post-split L3.G3** = L3.G3 经 L3.G2.E split out 后剩余 5 项 sub-residual
> - **[SYN] / [COROLLARY] / [THM] / [UNKNOWN]** = 严谨性四级标签
> - **Cui 2019** = Cui-Yin-Wang-Chen-Wang-Guo-Han 2019 *Phys Rev Applied* 11:034053 simplified TFQKD（path α anchor 协议）
> - **Pirandola Eq. 11** = Pirandola 2019 main paper 第 11 号公式 `C(N) ≤ min_C E_R(C)`，是 REE 切割上界，**不**直接给 single-repeater specific 形式
> - **REE** = Relative Entropy of Entanglement（相对熵纠缠度量）
> - **tele-covariance** = teleportation-covariance（信道在 teleportation 下保协变性，pure-loss bosonic 满足）

---

## §1 12 Sub-Gap 主状态矩阵（v0.3 修正）

| Sub-gap | Lemma | 主题 | C1(a) | C3 | C2 | 总状态 |
|---|---|---|---|---|---|
| **L1.G1** | A | Hilbert 空间 alignment | ✅ R2 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L1.G2** | A | embedding ι 构造 (HARDEST) | ✅ R1 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L1.G3** | A | Stinespring gauge invariance | ✅ R3 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L1.G4 v0.2** | A | trace-distance contraction（v0.1 [RETRACTED] → v0.2 redo）| ✅ R1 PASS（v0.2 redo verify）| ✅ R2 diff PASS（"R1 smuggling defect appears fixed"）| **C1+C2+C3 闭合 → [COROLLARY]** |
| **L2.G1 v0.3 final** | B | rate-direction sign | ✅ R2 PASS | ✅ R2 diff FAIL #5 → v0.3 patch → **R3 A 项 PASS** | **C1+C2+C3 闭合 → [COROLLARY]** |
| **L2.G2** | B | ε-composable decomposition | ✅ R3 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L2.G3** | B | Eve set across spaces | — | — | **OPEN per R0.1**（cross-space gap，user 显式声明范畴）|
| **L2.G4** | B | non-LOCC joint attack | ✅ R2 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L3.G1** | C | LOPC syntax cross-topology | ✅ R1 PASS | ✅ R2 diff PASS | C1+C2+C3 闭合 → [COROLLARY] |
| **L3.G2 v0.5 final** | C | key length cross-topology (under user Option B) | ✅ R3 PASS | ✅ R3 PASS | **C1+C2+C3 闭合 → [COROLLARY]** |
| **L3.G2.E v0.3 final** | C | channel-use counting alignment（NEWLY opened，split-out from former L3.G3 sub-residual 4）| ✅ R3 PASS | ✅ R2 diff PASS（"clean split-out"）| **C1+C2+C3 闭合 → [COROLLARY]** |
| **L3.G3 (post-split)** | C | Pirandola Eq. 11 specialization chain to specific η-form：5 项 sub-residual（citation / parameter-id / symmetry / protocol-model / edge-model）| — | — | **OPEN per R0.1**（5 项 user-level operational-link sub-residual）|

**v0.4 汇总**（post C2 user batch sign-off 2026-05-01）：

- **10/12 sub-gap C1 + C2 + C3 FULLY CLOSED → [COROLLARY]**：L1.G1, L1.G2, L1.G3, **L1.G4 v0.2**, **L2.G1 v0.3 final**, L2.G2, L2.G4, L3.G1, **L3.G2 v0.5 final**, **L3.G2.E v0.3 final**
- **2/12 OPEN per R0.1**：L2.G3（cross-space）+ post-split L3.G3（5 项 user-level sub-residual）
- **C2 用户审签 batch**：✅ **已完成**（2026-05-01 用户批量签批，签批记录见 [path_alpha_c2_signoff_2026-05-01.md](path_alpha_c2_signoff_2026-05-01.md)）
- **额外 caveat**：Pirandola Eq. 11 specialization chain（Eq. (8)/(9) lossy chain + tele-covariance + symmetric η split），**独立**于 12 sub-gap 之外的 conditional step

---

## §2 已 PASS 的 10 个 closure 文件清单（v0.4 C2 签批后确认）

| Sub-gap | 文件 | 关键 PDF 直读对象 | C3 R2 验证 |
|---|---|---|---|
| L1.G1 | [path_alpha_l1g1_closure_v0_1.md](path_alpha_l1g1_closure_v0_1.md) | Cui 2019 + Pirandola SI Note 1 + KW Ch 20 | diff PASS |
| L1.G2 | [path_alpha_l1g2_closure_v0_1.md](path_alpha_l1g2_closure_v0_1.md) | Cui Step 3 + Pirandola SI Note 1/2 + KW §20.1/§20.2 | diff PASS |
| L1.G3 | [path_alpha_l1g3_closure_v0_1.md](path_alpha_l1g3_closure_v0_1.md) | KW Chapter 4 §4.3 | diff PASS |
| **L1.G4 v0.2** | [path_alpha_l1g4_closure_v0_2.md](path_alpha_l1g4_closure_v0_2.md)（[v0.1 RETRACTED](path_alpha_l1g4_closure_v0_1.md)）| KW Ch 6 Theorem 6.3 + §4.4.2 + 数值 300 trials | **diff PASS** "R1 smuggling defect appears fixed" |
| L2.G2 | [path_alpha_l2g2_closure_v0_1.md](path_alpha_l2g2_closure_v0_1.md) | Portmann-Renner 2022 §III.B Theorem 2 + Lemma 3 | diff PASS |
| L2.G4 | [path_alpha_l2g4_closure_v0_1.md](path_alpha_l2g4_closure_v0_1.md) | Cui 2019 Eq. (1) + Section III page 3 | diff PASS |
| L3.G1 | [path_alpha_l3g1_closure_v0_1.md](path_alpha_l3g1_closure_v0_1.md) | KW Eq. (20.1.12) + Pirandola SI Note 1 + Cui Step 3 | diff PASS |
| **L3.G2 v0.5 final** | [path_alpha_l3g2_closure_v0_1.md](path_alpha_l3g2_closure_v0_1.md) | Portmann-Renner 2022 §III.B + Pirandola Methods near-Eq.-(35) + Cui Eq. (3)（user Option B）| **R3 PASS** |
| **L3.G2.E v0.3 final** | [path_alpha_l3g2e_closure_v0_1.md](path_alpha_l3g2e_closure_v0_1.md) | Cui Step 2.a + Step 3 + Pirandola SI Note 1/2 + Methods（per-edge-use 等同）| **diff PASS** "clean split-out" |

**已闭合（C3 R3 PASS + C2 签批完成）**：

| Sub-gap | 文件 | 原 C3 R2 issue | v0.3 patch | C2 |
|---|---|---|---|---|
| **L2.G1 v0.3** | [path_alpha_l2g1_closure_v0_1.md](path_alpha_l2g1_closure_v0_1.md) | §1.2 证明链 "Pirandola Eq. 11 [THM] ≤ -log_2(1-√η_AB)" 是 silent specialization upgrade | §1.2 chain 改两步：Eq. 11 → min_C E_R(C) → specialization → -log_2 形式；加 v0.3 corrected note + cross-link RETRACTION.md §9.3 | ✅ 2026-05-01 |

**[RETRACTED]**：

| Sub-gap | 文件 | REJECTED 依据 |
|---|---|---|
| L1.G4 v0.1 | [path_alpha_l1g4_closure_v0_1.md](path_alpha_l1g4_closure_v0_1.md) | C3 R1 diff REJECTED — §1.2 application 段 smuggled L1.G2 + L2.G3 closure（详 [RETRACTION.md §9.1](../research/RETRACTION.md#91-l1g4-v01-closure-撤回)）|

---

## §3 OPEN sub-gap — 结构性维持 [UNKNOWN]（v0.3 反映 post-split 状态）

### §3.1 L2.G3 — Eve set across spaces（与 v0.2 §3.1 一致）

trusted-relay Eve **仅** access $\mathcal{H}_E$，**不**触 $\mathcal{H}_C$ 这一 cross-space 假设。维持 **OPEN per R0.1**，需 user 显式声明。详 [v0.2 §3.1](path_alpha_subgap_closure_integration_v0_2.md#31-l2g3--eve-set-across-spaces与-v01-31-一致原文重述)（保留作 audit）。

### §3.2 post-split L3.G3 — 5 sub-residual（v0.3 修正：从 6 减至 5）

L3.G3 原 6 项 sub-residual 中第 4 项（"channel-use accounting"）已 split out 为 newly opened **L3.G2.E**（C1+C3 R2 PASS）。剩余 **post-split L3.G3 = 5 sub-residual**，全部 user-level OPEN：

1. **Citation gap**：Pirandola Eq. 11 (REE cut UB) → Eq. (8)/(9) lossy chain → `-log_2(1-√η_{AB})` specialization 链缺
2. **Parameter-identification gap**：是 `η_min` vs `η_AC·η_BC` vs symmetric？三个不可互换
3. **Symmetry / equidistance gap**：`√η_{AB}` 形式要求 equidistant split；否则 generic bound 是 `-log_2(1-min{η_AC, η_BC})`
4. ~~Channel-use accounting gap~~ → **已 split out 为 L3.G2.E**（v0.3 修正）
5. **Protocol-model gap**：honest Charlie 干涉 / detection 须 explicit written as Pirandola Note 1/2 permitted local op
6. **Edge-model gap**：A-C / B-C links 须 explicit declared 为 fixed memoryless pure-loss bosonic（确保 tele-covariance）

post-split L3.G3 编号沿用原序号（1/2/3/5/6），**不**重新编号；item 4 标 "已 split out 为 L3.G2.E" 作 audit。

**为什么 5 项全 OPEN per R0.1**：

- operational-link / 结构性 / parameter-form gap，per memory feedback `feedback_ai_draft_structural_gaps`，AI **不**得 draft closure
- 推进路径：(b) user 纸笔复核 / (c) 数值 SDP 工具 / (a) 跨家族 AI 直读 PDF（多步 specialization 直读，不是单步 statement verify）
- L3.G2.E 是从原 L3.G3 sub-residual 4 split 出来唯一**可 AI close** 的 abstract counting 部分；其余 5 项**不可** AI close

### §3.3 ~~Lemma C counting residual~~ → 已被 L3.G2.E 吸收（v0.2 → v0.3 修正）

v0.2 §3.3 把 "Lemma C counting/normalization residual" 列为独立 named residual。**v0.3 修正**：该 residual 已被 newly opened sub-gap **L3.G2.E** 吸收，**不**再独立列项。详 [path_alpha_l3g2e_closure_v0_1.md](path_alpha_l3g2e_closure_v0_1.md) §1.1 立项背景。

---

## §4 Path α three-lemma combined chain — 当前 conditional 状态（v0.3 修正）

按 [lemma_skeletons §6](umr_path_alpha_lemma_skeletons_v0_1.md) v0.3 corrected combined chain：

$$\underbrace{R_{Cui}(\Pi)}_{\text{TF-QKD 密钥率, Cui Eq. (3)}} \stackrel{\text{Lemma A+B+C [SYN, conditional]}}{\leq} \underbrace{R_{Pirandola}(\Pi_{tr})}_{\text{end-to-end 网络 secret-key capacity}} \stackrel{\text{Pirandola Eq. 11 (REE cut UB) [THM]}}{\leq} \underbrace{\min_C E_R(C)}_{\text{REE 最小切割流, Eq. 10/11}} \stackrel{\substack{\text{Eq. (8)/(9) specialization} \\ \text{+ tele-cov + sym η split [conditional]}}}{=} \underbrace{-\log_2(1-\sqrt{\eta_{AB}})}_{\text{single-repeater bound, N=1 equidistant}}$$

**当前 conditional status (post C2 user batch sign-off 2026-05-01)**：

- **10/12 sub-gap C1 + C2 + C3 FULLY CLOSED → [COROLLARY]**（详 §1）
- **2/12 OPEN per R0.1**：L2.G3（cross-space）+ post-split L3.G3（5 项 user-level sub-residual）
- **额外**：Pirandola Eq. 11 specialization chain（Eq. (8)/(9) + tele-covariance + sym η split），独立 conditional step
- **C2 用户审签 batch**：✅ 已完成（2026-05-01 user batch sign-off）
- **C2 用户审签 batch**：✅ 已完成（2026-05-01 user batch sign-off）
- **C3 R3**：✅ L2.G1 v0.3 + 4 propagation patches 已通过（lemma_skeletons §6 + path α v0.3 spec + integration）
- **Combined chain**：[SYN, conditional on **{L2.G3 + post-split L3.G3 (5 sub-residuals) + Pirandola Eq. 11 specialization chain}**]（10/12 sub-gap 已 C1+C2+C3 全闭合 → [COROLLARY]）

**对外引用资格**：

- **10 个 [COROLLARY] sub-gap**：可对外引用（限对应假设）
- **Combined chain**：仍 [SYN, conditional] — 不可对外引用
- Combined chain 升级仍需 L2.G3 + L3.G3 闭合

---

## §5 R0.1 / R0.2 红线复述（v0.3 与 v0.2 一致）

### §5.1 R0.1 — 不做计划外降级

- **10 个 COROLLARY closure**：每个 §1.3 strict scope 必须保持不动
- **L1.G4 v0.1 [RETRACTED]**：v0.2 已 C1+C2+C3 闭合 → [COROLLARY]
- **L2.G3 / post-split L3.G3 5 项**：**禁止** AI 自行 close

### §5.2 R0.2 — 三闸门并列必要（v0.2 措辞维持）

- **C1(a)** Codex 端直读 PDF 满足；Claude 端**间接**（通过 prior synthesis）
- **C2 用户签字**：✅ 已完成（2026-05-01 user batch sign-off，见 [path_alpha_c2_signoff_2026-05-01.md](path_alpha_c2_signoff_2026-05-01.md)）
- **C3 R3**：✅ 已完成（L2.G1 v0.3 + 4 propagation patches）
- **10/12 sub-gap [SYN] → [COROLLARY] 升级合法**

### §5.3 R0.3 — 严谨性分级

- 10 个 closure banner = `[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01) / C3 ✅`
- **L1.G4 v0.1 banner = [RETRACTED]**；v0.2 banner = `[COROLLARY]`
- combined chain 仍 [SYN, conditional]，**不可对外引用**

---

## §6 推荐下一步（按 R0.2 三闸门次序）

1. **L2.G1 v0.3 + 4 propagation patches C3 R3 重评**（AI 端可立即跑）
   - 验证 L2.G1 v0.3 的 Eq. 11 specialization caveat 已正确加入
   - 验证 lemma_skeletons §6 + path α v0.3 spec + integration v0.3 一致

2. **C2 用户审签 batch**（user 必须做，AI 不可代）
   - 9 个 PASS closure + L2.G1 v0.3（待 C3 R3 PASS 后）逐项审签
   - **L2.G3 显式 declaration** 在此阶段
   - 预估几小时

3. **post-split L3.G3 5 项 sub-residual 推进**（user-level，按 §3.2 选择策略）
   - 若推：每项需 user 直读 PDF / 纸笔 / 数值；几个月级
   - 若不推：path α 永远 [SYN, conditional on L3.G3]

4. **Pirandola Eq. 11 specialization chain 显式 verify**（C1(b) user 纸笔 / C1(c) 数值 SDP）
   - 与 post-split L3.G3 5 项**部分重叠**（item 1/2/3/5/6 都涉及 specialization）
   - user-level 工作

5. **Combined chain 升级评估**（仅在所有上述 close 后）
   - 整体升级 [COROLLARY] 候选

---

## §7 v0.3 vs v0.2 diff 概要

| Item | v0.2 | v0.3 |
|---|---|---|
| 总 sub-gap 数 | 11 + 1 named residual (Lemma C counting) | **12（11 原 + L3.G2.E newly opened）** |
| L1.G4 状态 | [RETRACTED] | **L1.G4 v0.1 [RETRACTED] + L1.G4 v0.2 redo C1+C3 R2 PASS** |
| L3.G2 状态 | C1 PASS / C3 R2 待 | **C1 + C3 R3 PASS** (v0.5 final) |
| L3.G2.E 状态 | （未提，作 named residual）| **新立项；C1+C3 R2 PASS** (v0.3 final) |
| L3.G3 状态 | 6 sub-residual OPEN | **post-split L3.G3 = 5 sub-residual OPEN** |
| Lemma C counting residual | 独立 named residual | **已被 L3.G2.E 吸收，不再独立列项** |
| L2.G1 状态 | C1 PASS | C1 PASS / **C3 R2 diff FAIL #5 → v0.3 patch → R3 待** |
| Pirandola Eq. 11 specialization caveat | 整合稿层级 | **已 propagate 到 lemma_skeletons §6 + path α v0.3 spec + L2.G1 v0.3 + integration v0.3**（4 处一致）|
| Combined chain | "11 sub-gaps + Lemma C counting + Eq. 11 specialization" | **"12 sub-gaps with post-split L3.G3 = 5 sub-residuals + Eq. 11 specialization"** |
| Total OPEN/conditional 总 conditional 数 | 11 + 2 named residuals = 13 | **12 sub-gaps（含 2 OPEN）+ Eq. 11 specialization**（cleaner inventory）|

---

## §8 Changelog

- **v0.1** (2026-04-26)：首版 status report。9/11 PASS + 2 OPEN per R0.1。**[SUPERSEDED 2026-04-26]** 因 C3 R1 holistic FAIL + diff REJECTED at L1.G4 + L3.G3 gap-id 揭露 Pirandola Eq. 11 citation 错。
- **v0.2** (2026-04-26 same-day)：v0.1 修补版本。8/11 PASS + L1.G4 [RETRACTED] + 2 OPEN + Lemma C counting residual + Eq. 11 specialization chain caveat。**[SUPERSEDED 2026-04-26 same-day]** 因 C3 R2 holistic 揭露 v0.2 与 same-day later state 不再 coherent（L3.G2.E 立项 + L1.G4 v0.2 redo + L3.G2 v0.5 final + post-split L3.G3 = 5 都未 propagate）。
- **v0.3** (2026-04-26 same-day)：本版。修正 v0.2 4 项 propagation 不足：(i) L1.G4 v0.2 redo 升入主矩阵；(ii) L3.G2 v0.5 final R3 PASS 升状态；(iii) L3.G2.E v0.3 final 进主矩阵作 12 个 sub-gap 第 12 项；(iv) post-split L3.G3 5 sub-residual 显式列；(v) "Lemma C counting residual" bucket 删除（被 L3.G2.E 吸收）；(vi) L2.G1 C3 R2 diff FAIL #5 → v0.3 patch 入状态 + 加 specialization caveat。Combined chain 仍 [SYN, conditional on multi-OPEN]，**不可对外引用**。下一步：L2.G1 v0.3 + 4 propagation patches C3 R3 verify + C2 用户审签。
