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
