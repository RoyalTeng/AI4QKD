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

AI 起草的理论陈述默认 **[CONJ]** 级。升级到 **[COROLLARY] 或 [THM]** 的硬路径（单值规则）：

1. 至少 **两个独立评审** 各自**独立**返回 PASS / SOUND
2. 任一评审 UNSOUND / FAIL / REJECTED → **立即撤回**并留痕
3. **用户显式签字**是升级到 **[COROLLARY] 以及 [THM]** 的**必要**条件；对外引用 / 论文 / 展示同样要求

"独立"的含义**严格按 [RETRACTION.md §4.1 规则 3](../../docs/research/RETRACTION.md) 执行**：

- **不计入**：同一模型多次运行；同一家族模型互评；纯 AI 审计链（无论多深）
- **计入**任一：(a) **不同训练偏差源**的模型（例如 Claude + GPT/Codex 跨家族）且双方**直接读 PDF 原文**；(b) **人类**研究者纸笔复核；(c) **非 AI 工具**（SDP 数值 / 符号计算 / proof assistant）独立复现

**dev-reviewer skill 的地位**（硬红线）：自主 session 内 dev-reviewer 双 Codex 评审是**强制 QA triage**，用于捕获 bug / consistency / 引用精度问题 —— **但本身不单独满足 R2.2 的 independent-review 条件**（Claude + Codex 仍是跨家族 AI 审计链，未满足 (a) 的"直读 PDF"双边要求 + 未含 (b)/(c)）。dev-reviewer PASS 仍**必须**叠加用户签字（[COROLLARY]/[THM] 升级）或叠加 (b)/(c) 形式的独立验证。违反此边界的 session 视同 R2.1 计划外越权。

v1 FINDINGS retraction 因 "Claude 起草 + Claude 多审" 被误当多方验证；**不得**重蹈

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
3. **WTB 引用精度错 (2026-04-21 Codex 评审发现)**：AI 凭记忆写定理编号 → 全局修正（commit 2583ffc diff 内查证具体数字）

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
