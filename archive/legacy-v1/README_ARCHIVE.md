# Legacy v1 (2025-Q1, DEPRECATED)

本目录保留 AI4QKD v1 全部代码,仅作历史记录。**不要基于此开发**。

废弃原因(见项目根 `docs/REFACTORING_PLAN.md` §1.1 表格):

1. `simulator/quantum_simulator.py:29-67` 不读协议图,对任意协议返回固定数值
2. `ai_agent/enhanced_agent.py:108` 的适应度函数恒为常数 ≈ 0.2566
3. `formal_verification/`、`security_evaluator/` 是空目录
4. `devlog/story_update.md` 中 "78.6% 提升" 在代码里找不到来源
5. 声称 import torch / qiskit / z3,实际零导入

新版本见项目根 `qkdx/`(v2,按 `docs/PHASE0_M1_TECHNICAL_SPEC.md` 规范)。

本归档对应 commit:see `git log -- archive/legacy-v1/README_ARCHIVE.md`.

---

## 空目录附注(migrate 清理)

迁移时以下 5 个顶层目录为**空目录**(git 不可追踪),未通过 `git mv` 成功归档,
已在 migrate 后直接 `rmdir` 删除(等价于归档):

- `data/`(空,legacy 数据目录)
- `formal_verification/`(空,曾声称的形式化验证模块,实际未实现 — REFACTORING_PLAN §1 缺陷 #3 证据)
- `logs/`(空,legacy 运行日志目录)
- `security_evaluator/`(空,曾声称的安全评估器模块,实际未实现 — REFACTORING_PLAN §1 缺陷 #3 证据)
- `utils/`(空,legacy 工具目录)

删除理由:空目录在 git 中不可追踪,保留在新仓库会误导开发者以为有内容。
`formal_verification/` 和 `security_evaluator/` 的空目录性质本身是 AI4QKD v1
失败的证据,已在 `docs/REFACTORING_PLAN.md` §1 记录。
