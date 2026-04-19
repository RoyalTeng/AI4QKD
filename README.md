# qkdx — Numerical QKD Rate Bounds under MS-EB Framework

**Status**: Phase 0 M1 开工中(2026-04-19 起)

在 MS-EB 五元组 $\Pi = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 框架下,对无中继无存储 DV-QKD 协议用半正定规划计算紧密钥率下界(WLC SDP),作为 PROSPECTUS 主问题研究的可信评估器。

## Documentation tree

- **Research map (WHY)**:[docs/PROSPECTUS.md](docs/PROSPECTUS.md) v3.1
- **Research plan (HOW-to-do-research)**:[docs/RESEARCH_PLAN.md](docs/RESEARCH_PLAN.md) v1.0
- **Implementation spec (HOW-to-build)**:[docs/REFACTORING_PLAN.md](docs/REFACTORING_PLAN.md) v3.1.4
- **M1 technical spec**:[docs/PHASE0_M1_TECHNICAL_SPEC.md](docs/PHASE0_M1_TECHNICAL_SPEC.md) v0.1
- **Migration guide (已执行)**:[docs/PHASE0_MIGRATION_GUIDE.md](docs/PHASE0_MIGRATION_GUIDE.md) v0.1
- **Research journal**:[docs/research/](docs/research/)(含 Log 01-07 + RETRACTION + FINDINGS v2 + Log 07 人类精读)

## Package layout

```
qkdx/
  core/       # Hilbert-space algebra (density operators, Kraus, POVM, entropy)
  protocol/   # MSEBProtocol data class (PROSPECTUS §4 + TECH_SPEC §2)
  protocols/  # BB84 / six-state / MDI / TF-QKD instances
  numerics/   # WLC SDP, facial reduction, decoy
  analytic/   # Shor-Preskill, six-state, GLLP closed-form baselines
  symmetry/   # Clifford / permutation twirling (M4A)
  utils/      # logging, validation, repro seed, precision constants
tests/        # 与 qkdx/ 结构对齐
notebooks/    # M1-M4 验收 Jupyter
```

## Legacy

v1 代码已归档至 [archive/legacy-v1/](archive/legacy-v1/)(2026-04-19 migrate, commit `607f618`)。废弃原因见归档 README。

## Environment

```bash
uv sync --frozen        # 依赖安装
export PYTHONHASHSEED=20260418
pytest tests/           # 运行测试
```

## 状态

Phase 0 M1 Week 1 — R1.1 WLC 2018 Level 4 精读(见 [docs/literature/](docs/literature/))。
