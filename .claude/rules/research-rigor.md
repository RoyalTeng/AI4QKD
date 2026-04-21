# Research Rigor Rules (项目级)

**项目性质**：quantum information theory / QKD security proofs / numerical reproducibility 前沿研究

**规则来源**：用户 2026-04-21 session 内明确声明

**适用范围**：所有 AI 自主 session、所有 AI 代理、所有文档产出

---

## R1. 最高原则

> **研究性质的项目最要紧的就是严谨性；结论需要多方验证**

---

## R2. 三条红线（不可违反）

### R2.1 不做计划外降级

- [FINDINGS.md + RESEARCH_PLAN + PHASE1_LOG] 已立 scope 和分级标签**不得静默降级**
- 需要简化 → 标 `spec_only` + 写实施门槛；**不引入简化模型替代**
- 即使 `scope_tag="partial"` 也不合法 —— 见 SARG04 回滚先例 (docs/PHASE1_LOG.md §2.1)
- 例外：用户显式同意 → 必须时序记录

### R2.2 研究结论必须多方验证

AI 起草的理论陈述默认 **[CONJ]** 级。升级路径：

1. 至少 **两个独立评审**（两个不同 AI 代理 + 用户审签，或等价组合）
2. 两评审**各自独立**返回 PASS / SOUND
3. 任一评审 UNSOUND / FAIL / REJECTED → **立即撤回**并留痕
4. 用户审签是升级到 [THM] 或对外引用的**必要**条件

"独立"的含义：不同模型 / 不同 agent 身份 / 不同 prompt 角度 —— 不是同一 AI 两次运行

### R2.3 四级严谨性分级（FINDINGS v2 §1.2）

| 分级 | 可引用？ |
|---|---|
| **[THM]** 文献定理 + 原始拓扑对齐 + 继承 lemma 验证 | 可 |
| **[COROLLARY]** 从 [THM] 机械推导 + 文献每步可查 + 用户签字 | 可（限对应假设） |
| **[SYN]** 文献综合 + 无反例 + 未升级定理 | 内部可用；对外禁止 |
| **[CONJ]** 方向性假设 + 依赖未证 assumption | 内部 working；对外禁止 |
| **[UNKNOWN]** 开放问题 | 明确标 |

AI 合成**默认** [SYN] 或更低。**禁止**自行升级。

---

## R3. 先例（不可重蹈）

1. **FINDINGS v1 retraction (2026-04-19)**：AI 自行把 [SYN] 升 [COROLLARY]，未审签 → 撤回
2. **path γ v0.2 retraction (2026-04-21)**：AI 用"简化 adversarial containment"绕过 Log 07 明确要求的三 lemma → 两 reviewer 独立 UNSOUND → 撤回
3. **WTB Thm 26/47 引用错**：AI 凭记忆写编号，实际 PDF 是 Thm 12/19 → 全局修正（commit 2583ffc）

---

## R4. 违规后果

- 任何违反 R2.1-R2.3 的 commit → 必须在下一 commit 前**回滚或降级**
- 违规累计被记入 docs/research/RETRACTION.md 作案例
- 自主 session 自我检测到违规 → 立即停手，写 retraction 说明，交用户

---

## R5. CLAUDE.md 衍生

详细规则展开见项目根 [CLAUDE.md](../../CLAUDE.md)。本文件是压缩版 quick-reference，与 CLAUDE.md 内容保持一致。

**内容冲突时以 CLAUDE.md 为准**。

---

*END OF R1-R5 rules. 2026-04-21 v1.0*
