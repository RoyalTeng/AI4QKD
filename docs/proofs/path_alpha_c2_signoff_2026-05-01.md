# C2 用户签批记录 — Path α 10 Sub-Gap 批量签批

**签批日期**：2026-05-01
**签批人**：项目负责人（用户）
**签批方式**：批量签批（全部 10 个 sub-gap 一次性确认）

---

## 签批范围

按 [path_alpha_subgap_closure_integration_v0_3.md](../proofs/path_alpha_subgap_closure_integration_v0_3.md) §1 主状态矩阵，以下 10 个 sub-gap 已完成 C1(a)（跨家族 AI 直读 PDF）+ C3（第三方代码审查），现经 C2 用户签批后升级至 [COROLLARY]：

### Lemma A — 协议嵌入（4/4）

| Sub-gap | 主题 | Closure 文档 | C1(a) | C3 |
|---------|------|-------------|-------|-----|
| L1.G1 | Hilbert 空间 alignment | [path_alpha_l1g1_closure_v0_1.md](../proofs/path_alpha_l1g1_closure_v0_1.md) | R2 PASS | R2 PASS |
| L1.G2 | embedding ι 构造 | [path_alpha_l1g2_closure_v0_1.md](../proofs/path_alpha_l1g2_closure_v0_1.md) | R1 PASS | R2 PASS |
| L1.G3 | Stinespring gauge invariance | [path_alpha_l1g3_closure_v0_1.md](../proofs/path_alpha_l1g3_closure_v0_1.md) | R3 PASS | R2 PASS |
| L1.G4 v0.2 | trace-distance contraction（v0.1 撤回后重做）| [path_alpha_l1g4_closure_v0_2.md](../proofs/path_alpha_l1g4_closure_v0_2.md) | R1 PASS | R2 PASS |

### Lemma B — 安全归约（3/4，L2.G3 OPEN 除外）

| Sub-gap | 主题 | Closure 文档 | C1(a) | C3 |
|---------|------|-------------|-------|-----|
| L2.G1 v0.3 | rate-direction sign（Eq. 11 specialization caveat 已修正）| [path_alpha_l2g1_closure_v0_1.md](../proofs/path_alpha_l2g1_closure_v0_1.md) | R2 PASS | R3 PASS |
| L2.G2 | ε-composable decomposition | [path_alpha_l2g2_closure_v0_1.md](../proofs/path_alpha_l2g2_closure_v0_1.md) | R3 PASS | R2 PASS |
| L2.G4 | non-LOCC joint attack | [path_alpha_l2g4_closure_v0_1.md](../proofs/path_alpha_l2g4_closure_v0_1.md) | R2 PASS | R2 PASS |

### Lemma C — 密钥率对接（3/4，L3.G3 OPEN 除外）

| Sub-gap | 主题 | Closure 文档 | C1(a) | C3 |
|---------|------|-------------|-------|-----|
| L3.G1 | LOPC syntax cross-topology | [path_alpha_l3g1_closure_v0_1.md](../proofs/path_alpha_l3g1_closure_v0_1.md) | R1 PASS | R2 PASS |
| L3.G2 v0.5 | key length cross-topology（user Option B）| [path_alpha_l3g2_closure_v0_1.md](../proofs/path_alpha_l3g2_closure_v0_1.md) | R3 PASS | R3 PASS |
| L3.G2.E v0.3 | channel-use counting alignment | [path_alpha_l3g2e_closure_v0_1.md](../proofs/path_alpha_l3g2e_closure_v0_1.md) | R3 PASS | R2 PASS |

---

## 签批内容

用户确认以下各项：

1. **分级**：上述 10 个 sub-gap 各自从 [SYN] 升级为 [COROLLARY]（从 [THM] 文献经机械推导得出，每步在文献可查）
2. **Scope**：每个 sub-gap 的 §1.3 explicit scope 维持不动；closure 内容仅限于各自 claimed 的 lemma step
3. **适用假设**：各 sub-gap 的假设集（显式列于各 closure 文档 §1.2 或 §-1）被确认

---

## 未纳入签批的项（维持原状态）

| Sub-gap | 当前状态 | 原因 |
|---------|---------|------|
| L2.G3 | [UNKNOWN] OPEN | 需用户显式声明 trusted-relay Eve 仅控 H_E 的 cross-space 假设 |
| L3.G3 (post-split) | [UNKNOWN] OPEN | 5 项 user-level sub-residual，需用户直读 PDF / 纸笔推导 |

---

## Combined Chain 状态

签批后 combined chain 状态更新为：

**[SYN, conditional on {L2.G3 + post-split L3.G3 (5 sub-residuals) + Pirandola Eq. 11 specialization chain}]**

整体升级至 [COROLLARY] 仍需 L2.G3 + L3.G3 闭合。

---

## R0.2 合规确认

- ✅ C1(a)：10 个 sub-gap 均通过 Codex 跨家族直读 PDF 验证
- ✅ C2：本记录为用户显式签批
- ✅ C3：10 个 sub-gap 均通过 dev-reviewer 双 Codex QA
- ✅ C1 ∧ C2 ∧ C3 三者并列满足，升级至 [COROLLARY] 合法

---

*签批记录结束。本文件与 10 个 closure 文档的 banner 更新、integration report v0.4 更新同步提交。*
