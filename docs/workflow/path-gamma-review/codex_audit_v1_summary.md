# Codex audit of path γ v0.2 — VERDICT 摘要

**日期**：2026-04-21
**评审对象**：[docs/proofs/umr_data_processing_gamma.md](../../proofs/umr_data_processing_gamma.md) v0.2
**原始输出**：[codex_review_v1.txt](codex_review_v1.txt) (4033 行，verdict 在末尾 line 5900-5942)
**Codex 版本**：v0.120.0, model gpt-5.4, reasoning effort xhigh

**VERDICT: UNSOUND**

---

## CRITICAL（3 项，invalidate [COROLLARY] claim）

1. **§2.1 在可组合安全下不够严谨**。§1.4 的 inequality 方向对，但需**先证明** trusted-relay executions 是 umr executions 在**同一 real/ideal game** 下的 literal subclass。"umr Eve can specialize to honest Charlie" 单句 **不** establish distinguisher 最终 state 跨 round 的相等。

2. **Charlie 角色的鸿沟**：
   - Pirandola 模型：Charlie 是 **honest internal node**，参与 adaptive network LOCC
   - umr 模型：Charlie 被**吸收进 adversarial interface**
   - 要 identify 两模型，需要 **embedding lemma** 证明 honest-Charlie 行为可作为 restricted umr attack 嵌入，**而不给 Eve extra side info via Charlie workspace/purification**

3. **§2.2 Step 2 不 automatic**。Pirandola 2019 applies to repeater-chain / network protocols with adaptive LOCC among **all** nodes. "任意 Π ∈ T_umr" 只有在**先证明一个 protocol-syntax lemma**（trusted Charlie 下 Π 是 valid chain/network LOCC protocol of Pirandola's type）后才 fall into scope. H1-H6 不 establish this.

**结论**：present proof 不是 [COROLLARY]-level rigorous.

---

## MAJOR（3 项，sign-off 前必须处理）

1. **§1.4 monotonicity** 公式 $R(\Pi; \mathcal{A}_2) \leq R(\Pi; \mathcal{A}_1)$ for $\mathcal{A}_1 \subseteq \mathcal{A}_2$ **正确**，但**只在** $R$ 定义于同一 ideal functionality + worst-case over nested adversary/distinguisher class 下成立。As stated it is a monotonicity **principle**, not a citable theorem without setup.

2. **$\mathcal{A}_\text{tr} \subsetneq \mathcal{A}_\text{umr}$ 合理**，但 draft **underspecifies umr adversary**. 写 Charlie 攻击为 $\mathcal{E}_C: C_\text{in} \to C_\text{out} \otimes C_\text{ann}$ **omits** composable model 中 adversarial device 通常保留的 Eve side register.

3. **Pirandola 引用 scope 不够精细**：
   - main text Eq. 9 是 **lossy-chain formula**
   - Eq. 11 是 **single-path network bound**
   - 若要 theorem language，supplement 中 **Thm 3 (chain)** 和 **Thm 6 (single-path network)** 是相关结果

---

## MINOR（3 项）

1. **WTB 2017 引用编号不准**（相对 repo PDF）：
   - 我草稿写 **Thm 26** 实际是 **Thm 12**（strong converse for teleportation-simulable channels）
   - 我草稿写 **Thm 47** 实际是 **Thm 19**（second-order bound）
   - **需修正 path γ v0.3 以及 upper_bound_report.md / upper_bound_msen.md / WTB-2017.md 中的编号**

2. **Khatri-Wilde 2024 引用**：arXiv:2011.04672v2 (2024) 是标准引用格式。对 secret-key agreement，相关条目是 **Prop 20.4, Cor 20.5**，而非 vague "Thm 20.x"

3. PLOB Eq. 19 引用正确 ✓

---

## 与 Claude audit 的对齐

两 reviewer 独立给出 UNSOUND verdict，从**不同角度**验证同一问题：

| 角度 | Claude audit | Codex |
|---|---|---|
| Verdict | UNSOUND-RETRACT | UNSOUND |
| 主错误性质 | 范畴错误 (category error, not set inclusion) | composable security 下不够严谨，需 embedding lemma |
| Charlie 角色 | 不同 Hilbert 空间 / 不同安全博弈 | honest internal node vs adversarial interface, 需 workspace/purification 安全等价性 lemma |
| Π 定义 | Portmann-Renner 协议 = honest parties tuple 不同 | Pirandola scope 不自动 cover, 需 protocol-syntax lemma |
| 引用精度 | 未细检 | WTB Thm 26→12, Thm 47→19 |
| 建议 | revert to [CONJ], 写 path γ 真版 or path α 三 lemma | 补 embedding lemma + protocol-syntax lemma 两 lemma |

**共识**：v0.2 simplified argument 绕过了 Log 07 § 3.1 / §4.3 明确要求的 rigor step。应 retract 到 [CONJ]，实施需 **明写**具体 lemma。

---

## Codex 输出位置说明

Codex 执行过程中做了大量 `exec` 和 `web_search` 调用，输出 4033 行里大部分是这些调用的结果 dump（Khatri-Wilde textbook、Pirandola PDF 等）。最终 Codex verdict 在**文件末尾 line 5900-5942**。我最初 head/tail 检查时未捕捉到这个位置的内容，错误声称 "Codex 未产生 focused verdict"。这是**我的 operational error**，不是 Codex 的问题。Codex 评审是**有效的**。

---

## 行动列表

1. ✅ v0.2 → v0.3 [CONJ] 已撤回（commit 6369e34）
2. ✅ claude_audit_v1.md + codex_audit_v1_summary.md（本文件）完整归档
3. ⏳ 修正 WTB 编号引用（Thm 26→12, Thm 47→19）于：
   - docs/proofs/umr_data_processing_gamma.md（v0.3 保留 v0.2 文本，但可加 footnote）
   - docs/findings/upper_bound_report.md
   - docs/proofs/upper_bound_msen.md
   - docs/literature/WTB-2017.md
4. ⏳ Khatri-Wilde 2024 引用精化（具体 Prop 20.4 / Cor 20.5）于相关位置
