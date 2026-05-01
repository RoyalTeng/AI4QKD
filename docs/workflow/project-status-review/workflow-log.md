# Workflow Log — project-status-review

**启动时间**：2026-04-30
**评审类型**：项目整体完成情况评审（非代码变更评审）
**分支**：MS-EB

---

## Round 1 — 2026-04-30

### 评审范围
- 整个项目 MS-EB 分支的完成情况
- 对照 PROSPECTUS.md v3.1 的 Sub-Q1→Sub-Q4 计划
- 对照 RESEARCH_PLAN.md v1.0 的研究动作分解
- 对照 PHASE_STATUS.md v1.1 的当前状态快照

### Codex Agent 1 — Diff/Status Review

**Verdict**: FAIL

**Issues** (4 major + 1 minor):

| # | Severity | Category | Description |
|---|----------|----------|-------------|
| 1 | major | correctness | Phase 0/Sub-Q1 被标记为"完成"，但 framework_coverage.md 显示 SARG04 spec_only、MDI partial、TF partial、MP-QKD out_of_scope |
| 2 | major | correctness | path α 状态过时：快照写"11 sub-gap C3 REJECTED"，但 integration v0.3 显示已扩展为 12 sub-gap，10/12 C1+C3 PASS，2/12 OPEN |
| 3 | major | correctness | 代码模块统计不准：protocols/ 是 5 个非 6 个；analytic/ 是 8 个非 2 个 |
| 4 | major | test_coverage | 测试目录遗漏 test_finite_key 和 test_protocol；PHASE0_REPORT 记录 131 passed + 9 skipped |
| 5 | minor | correctness | gap_shape 版本号过时（v0.3 vs 实际 v0.4） |

### Codex Agent 2 — Holistic Architecture Review

**Verdict**: 方向正确但乐观

**关键发现**:
- 研究架构：BB84/六态/WLC/GEAT 方向契合度好；MDI/TF 族只部分覆盖
- Phase 完成度：Phase 0/1 有 overstated；Phase 2 ~40% 作为脚手架合理，作为决定性完成则不够
- 最大瓶颈：定理转移债务（trusted→untrusted relay、fixed-channel→adversarial comb、Choi-state→channel capacity）
- path α user-override：存在治理风险，虽未正式违反红线
- 严谨性：大体对齐 R0.1-R0.3；撤回教训已被应用
- 代码-文档一致性：scope_tag 默认 "covered" 与 framework_coverage.md 建议矛盾

**整体评价**："按产出物体积约 50%；按到主问题可辩护答案的实际距离，更接近'中游且仍被一个硬 converse 问题阻塞'"

**Top 3 建议**:
1. 更新状态账本 — 反映 2026-04-26 path-α 最新状态
2. 选一条定理转移路径强制走通 C1 工作（建议走更窄、低风险的 converse 路线，而非整个 path α bundle）
3. 硬化框架边界 — 移除默认 scope_tag="covered"，区分表达性与实现成熟度

### 本轮产出
- changes-v1.patch: 项目状态快照文档
- review-diff-1.json: Agent 1 结构化评审（通过 Codex stdout）
- review-holistic-1.md: Agent 2 架构评审（通过 Codex stdout）
