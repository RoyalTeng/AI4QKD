# CLAUDE.md — AI4QKD 项目 AI 协作规范

**项目性质**：前沿研究（quantum information theory / QKD security proofs + numerical reproducibility）

**版本**：v1.0（2026-04-21）

---

## 0. 最高原则（不可违反）

> **研究性质的项目最要紧的就是严谨性；结论需要多方验证**

以下三条红线对所有自主 session、所有 AI 代理、所有文档产出均适用：

### R0.1 不做计划外降级

- **[FINDINGS.md + RESEARCH_PLAN + PHASE1_LOG] 已立的 scope 和分级标签不得静默降级**
- 遇到 "需要更多基础设施才能严格实施" 的场景 → 标 `spec_only`，写实施门槛，**不引入简化模型** **替代**
- 计划外降级即便加了 `scope_tag="partial"` 标签也不合法 —— 见 [docs/PHASE1_LOG.md §2.1](docs/PHASE1_LOG.md) SARG04 回滚先例
- 例外：经用户显式同意的降级必须在 `docs/PHASE1_LOG.md` 或等价日志中留时序记录

### R0.2 研究结论必须多方验证

- **AI 起草的理论陈述默认 [CONJ] 级**。**不得**基于单一 AI session 内的推理链自行升级到 [COROLLARY] 或 [THM]
- 升级到 **[COROLLARY] 或 [THM]** 的**硬**路径（单值规则，任何一级越权升级都非法）：
  1. 必须至少有 **两个独立评审** 各自**独立**返回 PASS / SOUND
  2. 任一评审返回 UNSOUND / FAIL / REJECTED → **必须撤回**并记录
  3. **用户显式签字**是升级到 **[COROLLARY] 以及 [THM]** 的**必要**条件，对外引用 / 论文 / 展示稿同样要求
- 评审的"独立"含义**严格按 [RETRACTION.md §4.1 规则 3](docs/research/RETRACTION.md) 执行**：
  - **不计入**"独立验证"的组合：同一模型多次运行、同一家族模型（例如 Claude 对 Claude）多 prompt 重评、AI 单层审计链
  - **计入**"独立验证"的组合须满足**任一**：
    - (a) **不同训练偏差源**的模型（例如 Claude + Codex/GPT 跨家族）**且** 双方均**直接读 PDF / 原文**而不是复述 AI 综述
    - (b) 包含**人类研究者**直接纸笔复核
    - (c) 使用**非 AI 工具**（数值 SDP / 符号计算 / 形式化 proof assistant）独立复现
  - v1 FINDINGS retraction 正是因为 "Claude 起草 + Claude 多次审" 被当作 "多方验证"；此陷阱**不得**重蹈

### R0.3 严谨性分级四级制（FINDINGS v2 §1.2 红线）

| 分级 | 含义 | 对外可引用？ |
|---|---|---|
| **[THM]** | 来源文献有定理级陈述 + 原始拓扑/假设与本项目对齐 + 已验证继承 lemma | 可引用 |
| **[COROLLARY]** | 从 [THM] 经机械推导得出 + 每步在文献可查 + 用户签字 | 可引用（限对应假设） |
| **[SYN]** | 文献综合判断 + 无反例 + 但未升级到定理级 | **内部讨论**可用；**论文/展示禁止**单独引用 |
| **[CONJ]** | 方向性假设 + 依赖未证 assumption | 内部 working hypothesis 可用；对外**禁止** |
| **[UNKNOWN]** | 开放问题 | 明确标记 |

AI 起草的合成陈述**默认** [SYN] 或更低。

---

## 1. 文档约定

### 1.1 严谨性标签必须显式

每条主张须以 **[THM] / [COROLLARY] / [SYN] / [CONJ] / [UNKNOWN]** 明示。禁止：
- 隐式分级（读者需自行判断）
- "显然 / obviously / straightforward" 等回避形式化的措辞
- 把 `pending sign-off` 当作 "实质已是 [COROLLARY]" 的 shortcut

### 1.2 撤回必须留痕

撤回或降级的文件：
- **不删除**原稿文本（保留作 cautionary record）
- 顶部加 **[RETRACTED / ARCHIVAL ONLY]** banner
- `§-1 撤回公告` 或等价章节说明撤回原因、评审引用
- 更新 Changelog 双向链接

先例：
- [docs/research/RETRACTION.md](docs/research/RETRACTION.md)：FINDINGS v1 retraction (2026-04-19)
- [docs/proofs/umr_data_processing_gamma.md](docs/proofs/umr_data_processing_gamma.md) §-1：path γ v0.2 retraction (2026-04-21)

### 1.3 引用精度

所有定理 / 公式编号必须**对 PDF 原文核对**。Level 3-4 精读 memo 引用的编号如果 AI 凭记忆写，**必须**在文件中标记 `[RECALLED]` 或 `[VERIFIED against PDF on date]`。

**先例索引**（详细数字见 [docs/research/RETRACTION.md](docs/research/RETRACTION.md) 与 [commit 2583ffc] 的 diff，不在本 live policy 文件内重复以免污染）。

---

## 2. 代码与测试约定

### 2.1 TDD 规范

- 测试先行：新功能**必须**先写测试（测试可预先 xfail）
- 测试必须打印真实数据值（不能只 assert pass/fail）
- 覆盖正常路径、异常路径、边界条件

### 2.2 数值复现性

每个 `docs/findings/` 数值结论必须带：
- 可执行脚本（`scripts/`）
- CSV 数据（`docs/research/data/`）
- 图（`docs/research/figures/` PNG + PDF）
- 对应 git commit SHA

### 2.3 不做未在 CLAUDE.md 明示的计划外降级

见 R0.1。

---

## 3. 评审约定

### 3.1 必须经评审的动作

- **升级分级标签**（[CONJ] → [COROLLARY]、[SYN] → [THM] 等）→ **双 reviewer + 用户** triple verification
- **对外论文 / 展示稿**（哪怕只是摘要）→ **用户审签**
- **重大理论文档**（upper_bound_report / proofs/*.md 等）→ **双 reviewer**

### 3.2 评审工作流

项目有 **dev-reviewer skill** 自动化双 Codex 评审。自主 session 内升级任何结论必须走此流程。

工作流位置：`docs/workflow/{feature}/`
- `changes-v{N}.patch`
- `review-diff-{N}.{json,md}`
- `review-holistic-{N}.md`
- `workflow-log.md`

### 3.3 评审 verdict 必须 ACT on

- **REJECTED / UNSOUND**：立即撤回，不 defend，不 patch 到上游
- **FAIL**：修复 major issues 后 Round 2 重评
- **PASS**：接受

**严禁**无视评审 verdict 强行保留结论。

---

## 4. 自主 session 约定

### 4.1 启动前

- 读 [docs/PROSPECTUS.md](docs/PROSPECTUS.md)（当前主问题 + 硬约束）
- 读 [docs/RESEARCH_PLAN.md](docs/RESEARCH_PLAN.md)（当前计划阶段）
- 读 [docs/research/FINDINGS.md](docs/research/FINDINGS.md) v2 + [RETRACTION.md](docs/research/RETRACTION.md)（当前结论状态 + 撤回先例）
- 读 [docs/research/07_pirandola_2019_technical_audit.md](docs/research/07_pirandola_2019_technical_audit.md)（用户亲自的 Log 07 技术审计，Sub-Q3 authoritative）

### 4.2 session 中

- 每个 commit 前检查：是否引入计划外降级？是否升级了标签？若是，必须走评审
- 定期记录到 `docs/AUTONOMOUS_SESSION_{DATE}_LOG.md`
- 失败 / 撤回 / 方法论教训都 **明确记录**，不掩盖

### 4.3 session 末

- 写 session conclusions 文档，严格按 R0.3 四级分级
- **不自动 commit** 理论级升级（[COROLLARY] 及以上）—— 等用户显式签字
- 提交 workflow 产物到 `docs/workflow/`

---

## 5. Python 项目风格（qkdx/）

### 5.1 模块结构

- `qkdx/` 核心代码
- `tests/` pytest 测试（镜像 `qkdx/` 目录）
- `scripts/` 顶层脚本（生成数据 / 图）
- `docs/` 文档（分 `literature/` `proofs/` `findings/` `research/` `workflow/`）

### 5.2 依赖

- numpy, cvxpy, mosek, matplotlib（数值）
- pytest（测试）
- 数值 SDP 必须声明 MOSEK 依赖（`~/mosek/mosek.lic`）

### 5.3 命名

- 文件：snake_case
- 类：PascalCase
- 函数：snake_case
- 常量：UPPER_SNAKE_CASE

---

## 6. 教训记录（持续更新）

### 6.1 已记录教训

1. **v1 overclaim retraction (2026-04-19)**：AI 自行把 [SYN] 升级为 [COROLLARY]，未经用户审签。**教训**：AI 合成不得升级分级；必须 triple verification。
2. **path γ v0.2 retraction (2026-04-21)**：AI "简化论证"绕过 Log 07 明确要求的三 lemma 明写。**教训**：简化不是严谨的捷径；若绕过了 identified gap 而不是 close 它们，就是 v1 陷阱的重复。
3. **WTB 引用精度错（2026-04-21 Codex 评审发现）**：AI 凭记忆或二手引用写定理编号。**教训**：引用必须对 PDF 核对，否则标 [RECALLED]。具体修正 diff 见 commit 2583ffc。
4. **Codex 大输出 missed verdict (初次 head/tail 错过末尾 verdict)**：**教训**：大输出必须 `grep "VERDICT"`，不是 head/tail。

---

## 7. Changelog

- **v1.0** (2026-04-21)：首版。用户明确要求（session 内）后确立。覆盖 R0.1-R0.3 三红线 + 文档 / 代码 / 评审 / session 约定。
