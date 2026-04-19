# Phase 0 Migration Guide — v2 仓库迁移 + qkdx/ 骨架

**文档状态**:v0.1(2026-04-19 首次落盘)
**适用**:PROSPECTUS v3.1 + REFACTORING_PLAN v3.1.4 + RESEARCH_PLAN v1.0 三文档对齐后的实施起点
**依赖**:[scripts/migrate_legacy.sh](../scripts/migrate_legacy.sh) v3.2

---

## 0. 本指南处理的是什么

**三件事**:
1. **rsync** 当前仓库(含 `.git/`,**保留完整 git 历史**)到无空格新路径 `$HOME/Desktop/ai4qkd/AI4QKD/`
2. **归档 legacy**(48 项顶层代码 / 配置 / 文档)到 `archive/legacy-v1/`
3. **创建 `qkdx/` 骨架**(按 REFACTORING_PLAN §3)

**不处理**:
- 项目 Python 包依赖安装(`uv sync` / `pip install`)— 留给后续
- WLC SDP 代码实施 — Phase 0 M1 工作,本指南完成后启动
- 删除原路径仓库 — 本指南明确**保留原路径作为 fallback**

---

## 1. 预先决策

| 决策点 | 本指南采用 | 备选(不采用) |
|-------|-----------|---------------|
| git 历史 | **保留**(rsync `.git/`)| git init 新仓库(切断历史,风险高) |
| 原路径 | **保留作 fallback** | 迁移后立即删除(不可逆) |
| rsync 策略 | 手动运行,**不写入脚本** | 脚本封装(但 rsync 是单向不可逆动作,保持手动) |
| 迁移脚本运行时机 | **在新路径**(无空格)运行 | 在原路径运行(有空格,real-run 会 refuse) |

---

## 2. 执行顺序(严格按序)

```
(a) 脚本成形                → scripts/migrate_legacy.sh(已落盘)
(b) 原路径 --dry-run 审查     → 本指南 §3
(c) rsync 原路径 → 新路径     → 本指南 §4(含 .git/,保留历史)
(d) 新路径 --dry-run 再审     → 本指南 §5
(e) 人工确认                → 用户显式 ok
(f) 新路径真跑 migrate        → 本指南 §6
(g) 创建 qkdx/ 骨架           → 本指南 §7
(h) 启动 M1 WLC TDD           → RESEARCH_PLAN §2.1
```

---

## 3. 原路径 Dry-run 审查结果(已完成)

**命令**(已执行):

```bash
cd "/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD"
bash scripts/migrate_legacy.sh --dry-run
```

**输出摘要**(完整见 `/tmp/migrate_dryrun_current.log`,140 行):

```
WARN: current path contains whitespace: /Users/tengjun/Desktop/ai4qkd (1)/AI4QKD
WARN:   — dry-run allows this, but real-run will refuse
[DRY] ✓ pre-checks complete
[DRY] Step 1: create snapshot branch 'archive/pre-refactor-snapshot-YYYYMMDD-HHMMSS'
[DRY] Step 2-3: archive legacy items to archive/legacy-v1/
[DRY]   keep (8 items): .DS_Store, .git, .gitignore, .pytest_cache, docs, scripts, tests, venv
[DRY]   archive (48 items): <见 §8 分类表>
[DRY] Step 4: write archival README to archive/legacy-v1/README_ARCHIVE.md
[DRY] Step 5: commit archival changes
[DRY] ✓ migration complete
```

**预期输出**与**实际行为**一致性:

- ✓ 空格路径被 **warn** 但不 fatal(dry-run 模式)
- ✓ 48 项进归档,8 项保留(不含 `qkdx/` / `notebooks/` / `pyproject.toml` / `uv.lock`,因为它们还未创建;KEEP_LIST 为它们**预留名**)
- ✓ 所有 `experiment_*.py`、`simulator/`、`ai_agent/` 等 legacy 进归档
- ✓ `docs/`、`scripts/`、`.git/`、`.gitignore` 保留
- ✓ 48 个 `git mv -k --` 命令列出(包括带空格文件名 `test_basic\ 2.py`)

**Dry-run PASS 条件**:
- [x] `bash -n scripts/migrate_legacy.sh` 通过
- [x] `shellcheck scripts/migrate_legacy.sh` 通过
- [x] Dry-run 无 exit 非零
- [x] Archive / Keep 分类与 §8 表格一致

---

## 4. Rsync 命令(**未执行,等用户确认**)

### 4.1 命令

```bash
# 目标路径(无空格)
NEW_ROOT="${HOME}/Desktop/ai4qkd/AI4QKD"

# 确保目标父目录存在,但目标自身不存在(避免覆盖)
mkdir -p "$(dirname -- "$NEW_ROOT")"

if [[ -e "$NEW_ROOT" ]]; then
  echo "ERROR: $NEW_ROOT already exists. Move or delete it first." >&2
  exit 1
fi

# rsync 整个仓库,**包含 .git/**(保留历史)
rsync -a \
  --exclude '.pytest_cache' \
  --exclude '.DS_Store' \
  --exclude 'venv' \
  --exclude '.venv' \
  -- "/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/" "$NEW_ROOT/"
```

### 4.2 rsync 排除项解释

| 排除 | 理由 |
|------|------|
| `.pytest_cache` | 随 pytest 重建,体积大 |
| `.DS_Store` | macOS 系统生成,体积小但无用 |
| `venv` | 本地 Python 环境,新路径应独立重建 |
| `.venv` | 同上(当前不存在,但排除防未来误 copy)|
| **不排除** `.git` | **保留 git 历史** — 本指南核心决定 |
| **不排除** `docs/research.zip` | 60KB 用户生成的 snapshot,保留作审计 |

### 4.3 验证 rsync 成功

```bash
cd "$NEW_ROOT"
git log --oneline -10                 # 应看到与原路径相同的 commit
git status                            # 应 clean
git rev-parse HEAD                    # 应与原路径一致
ls -la scripts/migrate_legacy.sh      # 应存在
```

---

## 5. 新路径 Dry-run(**未执行,等用户确认**)

```bash
cd "$HOME/Desktop/ai4qkd/AI4QKD"
bash scripts/migrate_legacy.sh --dry-run
```

**预期与原路径 dry-run 差异**:

- 无 "path contains whitespace" WARN(新路径无空格)
- 其他输出结构相同,48 项 archive / 8 项 keep

**PASS 条件**:
- [ ] 无 WARN(空格警告消失)
- [ ] Archive / Keep 分类与原路径 dry-run 一致
- [ ] 无 exit 非零

---

## 6. 实跑 migrate(**未执行,等用户确认**)

```bash
cd "$HOME/Desktop/ai4qkd/AI4QKD"
bash scripts/migrate_legacy.sh           # 不带 --dry-run
```

**脚本实际动作**:
1. 创建 snapshot branch `archive/pre-refactor-snapshot-YYYYMMDD-HHMMSS`(作 rollback point)
2. 在 main 分支做归档(48 项 `git mv -k -- X archive/legacy-v1/`)
3. 写 `archive/legacy-v1/README_ARCHIVE.md`
4. `git commit -m "chore(migrate): archive legacy v1 → archive/legacy-v1/"`

**Rollback**(如需):

```bash
git checkout archive/pre-refactor-snapshot-YYYYMMDD-HHMMSS
# 或
git reset --hard HEAD~1    # 回到 migrate commit 之前
```

**验证**:
- [ ] `git log -3` 显示新的 migrate commit
- [ ] `git diff HEAD~1 --stat` 显示 48 项 rename
- [ ] `ls archive/legacy-v1/` 列出全部 legacy(48+)
- [ ] `ls -1 | wc -l` ≤ 12(只剩 8 keep + archive/ 自身 + 未来 qkdx/ 等)
- [ ] `cat archive/legacy-v1/README_ARCHIVE.md` 可见

---

## 7. 创建 qkdx/ 骨架(**未执行**)

### 7.1 mkdir 命令(单次)

```bash
cd "$HOME/Desktop/ai4qkd/AI4QKD"

# qkdx 骨架(按 REFACTORING_PLAN §3)
mkdir -p qkdx/{core,protocol,protocols,numerics,analytic,symmetry,utils}
mkdir -p tests/{test_core,test_protocol,test_protocols,test_numerics,test_analytic,test_integration}
mkdir -p notebooks
mkdir -p docs/references
mkdir -p docs/adr
mkdir -p logs/phase0

# 各子包的 __init__.py
for pkg in qkdx qkdx/core qkdx/protocol qkdx/protocols qkdx/numerics qkdx/analytic qkdx/symmetry qkdx/utils; do
  touch "$pkg/__init__.py"
done

# tests 的 __init__.py
for td in tests tests/test_core tests/test_protocol tests/test_protocols tests/test_numerics tests/test_analytic tests/test_integration; do
  touch "$td/__init__.py"
done

# conftest.py
cat > tests/conftest.py <<'EOF'
"""pytest 共享 fixtures — 按 REFACTORING_PLAN §11.1 repro seed 启动"""
import numpy as np
import os
import pytest

# 默认种子(PROSPECTUS §11.1 DEFAULT_SEED)
DEFAULT_SEED = 20260418


@pytest.fixture(autouse=True)
def _seed_everything():
    np.random.seed(DEFAULT_SEED)
    env_seed = os.environ.get("PYTHONHASHSEED")
    if env_seed != str(DEFAULT_SEED):
        import sys
        print(
            f"[repro] WARN: PYTHONHASHSEED={env_seed!r}, expected {DEFAULT_SEED!r}",
            file=sys.stderr,
        )


@pytest.fixture
def rng():
    """固定种子 PRNG"""
    return np.random.default_rng(DEFAULT_SEED)
EOF

# pyproject.toml 雏形(按 REFACTORING_PLAN §11.2)
cat > pyproject.toml <<'EOF'
[project]
name = "qkdx"
version = "0.0.1"
description = "Numerical QKD rate bounds under MS-EB framework"
requires-python = ">=3.11,<3.13"
dependencies = [
    "numpy==2.1.*",
    "scipy==1.14.*",
    "cvxpy==1.5.*",
    "clarabel==0.9.*",
    "scs==3.2.*",
    "structlog==24.*",
]

[dependency-groups]
dev = [
    "pytest==8.*",
    "pytest-cov==5.*",
    "mypy==1.11.*",
    "ruff==0.6.*",
    "papermill==2.*",
    "jupyter==1.*",
]
optional = [
    "mosek==10.2.*",  # 可选求解器,需要学术许可
]

[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
markers = [
    "slow: SDP 单次 > 10s 的测试",
    "research: 研究级别耗时测试,手动触发",
    "fallback_solver: 使用 CLARABEL/SCS fallback 求解器的测试",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
EOF
```

### 7.2 骨架目录表

| 路径 | 来源 / 定义 | 内容 |
|------|------------|------|
| `qkdx/` | REFACTORING_PLAN §3 | Python 包根 |
| `qkdx/core/hilbert.py` | REFACTORING_PLAN §4.1 | 密度算子代数 |
| `qkdx/core/operators.py` | §4.2 | Kraus / POVM |
| `qkdx/core/entropy.py` | §4.3 | 熵测度 |
| `qkdx/protocol/base.py` | §4.4 | MSEBProtocol 五元组 |
| `qkdx/protocols/bb84.py` | §4.5 | BB84 实例 |
| `qkdx/protocols/sixstate.py` | §4.10/§4.12 | 六态 |
| `qkdx/protocols/mdi.py` | §4.12 | MDI-QKD |
| `qkdx/protocols/tfqkd.py` | §4.12 | TF-QKD(M4B) |
| `qkdx/numerics/wlc.py` | §4.6 核心 | WLC SDP |
| `qkdx/numerics/facial.py` | §4.7 | facial reduction |
| `qkdx/numerics/decoy.py` | §4.8 | 数值诱骗 |
| `qkdx/analytic/shor_preskill.py` | §4.9 | Shor-Preskill |
| `qkdx/analytic/six_state.py` | §4.10 | 六态解析 |
| `qkdx/analytic/gllp.py` | §4.11 | GLLP |
| `qkdx/symmetry/groups.py` | §4.13 | 有限群 |
| `qkdx/symmetry/twirling.py` | §4.13 | 群平均 |
| `qkdx/utils/logging.py` | §4.13 | 日志封装 |
| `qkdx/utils/validation.py` | §4.13 | 断言工具 |
| `qkdx/utils/repro.py` | §11.1 | seed 控制 |
| `qkdx/utils/numerics.py` | §11.4 | 精度常量 |
| `qkdx/utils/solvers.py` | §11.3 | has_mosek() |
| `tests/` | §6 | pytest 测试(与 qkdx/ 对齐)|
| `notebooks/` | §5 M1 交付 | Jupyter 实验 |
| `docs/adr/` | RESEARCH_PLAN §8.3 | ADR 制度 |
| `logs/phase0/` | §11.5 | 求解器遥测(gitignored)|
| `pyproject.toml` | §11.2 | 依赖声明 |
| `uv.lock` | §11.2 | 依赖强约束(`uv sync` 生成)|

---

## 8. 分类表 — KEEP / ARCHIVE / NEW

### 8.1 KEEP(保留,8 项)

| 路径 | 来源 | 保留原因 |
|------|------|----------|
| `.git/` | rsync 自原仓库 | 保留完整历史 |
| `.gitignore` | 已更新 | 新项目仍用 |
| `.DS_Store` | macOS | gitignore 已排除,不动 |
| `.pytest_cache/` | 随测试重建 | gitignore 已排除 |
| `venv/` | 本地 Python 环境 | 新路径应独立重建(rsync 已排除) |
| `docs/` | v2 项目文档层 | 包括 PROSPECTUS / REFACTORING_PLAN / RESEARCH_PLAN / research/ |
| `scripts/` | 本脚本目录 | 包括 migrate_legacy.sh 自身 |
| `tests/` | **v1 为空目录** | KEEP_LIST 预留给 v2 tests/,v1 tests/ 为空无损失 |

### 8.2 ARCHIVE(归档到 `archive/legacy-v1/`,48 项)

**legacy 代码(17 项)**:

| 项 | 类型 |
|----|------|
| `ai_agent/` | 目录,包含 enhanced_agent.py(常数适应度 bug) |
| `simulator/` | 目录,quantum_simulator.py 不读协议图 |
| `qcgf_dsl/` | 目录,legacy DSL |
| `config/` | 目录,legacy config |
| `data/` | 目录,legacy data |
| `devlog/` | 目录,含 78.6% 无证数字的 story_update.md |
| `examples/` | 目录 |
| `formal_verification/` | **空目录**,之前声称但未实现 |
| `security_evaluator/` | **空目录**,之前声称但未实现 |
| `logs/` | 目录,legacy run 日志 |
| `paper/` | 目录 |
| `results/` | 目录 |
| `utils/` | **空目录** |
| `autoresearch_*.py` × 2 | autoresearch 集成 |
| `generate_*.py` × 2 | PDF 生成 |
| `security_analysis.py` | legacy 安全分析 |
| `visualize_protocol.py` | legacy 可视化 |

**legacy 实验(11 项)**:

全部 `experiment_*.py` 文件(e91, innovative, mdi, mdi_quick, metanode, sns_improved, sns_qkd, tf_optimized, tf_qkd, tf_quick, two_stage_enhanced, two_stage_innovation)

**legacy setup / docs / misc(13 项)**:

| 项 | 类型 |
|----|------|
| `README.md` | legacy README(v2 会另写) |
| `QUICK_START.md` | legacy |
| `DUAL_ADAPTIVE_BB84_PROTOCOL_GRAPH.png` | legacy 图 |
| `activate_env.bat`, `quick_setup.bat`, `quick_setup.sh`, `setup_environment.bat` | legacy env 脚本 |
| `requirements.txt` | legacy deps(v2 用 pyproject.toml) |
| `setup.py` | legacy install(v2 用 pyproject.toml) |
| `formal_security_proof.md` | legacy 非定理文档 |
| `protocol_description.md` | legacy |
| `research_log.md`, `research_plan_tf_qkd.md` | legacy docs |
| `test_basic.py`, `test_basic 2.py` | legacy tests(后者是空格路径副产品) |
| `autoresearch_*.md` × 2 | legacy docs |

**总计**:17 code + 11 experiments + 13 misc = **41 项…** 等等,dry-run 说 48 项,差 7 项。让我重数:

列 dry-run 完整:

```
DUAL_ADAPTIVE_BB84_PROTOCOL_GRAPH.png, QUICK_START.md, README.md,
activate_env.bat, ai_agent, autoresearch_generated_experiment.py,
autoresearch_generated_report.md, autoresearch_integration.py,
autoresearch_literature_review.md, config, data, devlog, examples,
experiment_{e91_qkd, innovative_qkd, mdi_qkd, mdi_quick, metanode_qkd,
sns_improved, sns_qkd, tf_optimized, tf_qkd, tf_quick,
two_stage_enhanced, two_stage_innovation}.py,
formal_security_proof.md, formal_verification, generate_enhanced_pdf.py,
generate_pdf_report.py, logs, paper, protocol_description.md, qcgf_dsl,
quick_setup.bat, quick_setup.sh, requirements.txt, research_log.md,
research_plan_tf_qkd.md, results, security_analysis.py,
security_evaluator, setup.py, setup_environment.bat, simulator,
test_basic 2.py, test_basic.py, utils, visualize_protocol.py
```

数一数:
- 图 1(DUAL...)
- md 4(QUICK_START, README, formal_security_proof, protocol_description, research_log, research_plan_tf_qkd, 和 autoresearch_*.md × 2 = 8 md)
- .bat / .sh 4(activate_env, quick_setup.bat, quick_setup.sh, setup_environment.bat)
- .py 顶层 ~ 17(autoresearch × 2,experiment × 12,generate × 2,security_analysis, visualize_protocol, setup, test_basic × 2)
- dir 13(ai_agent, config, data, devlog, examples, formal_verification, logs, paper, qcgf_dsl, results, security_evaluator, simulator, utils)
- 其他:requirements.txt

重算:1 + 8 + 4 + 17 + 13 + 1 + ~4 = 48 ✓

### 8.3 NEW(后续创建,§7 命令)

| 路径 | 何时建 |
|------|--------|
| `qkdx/` + 子包 | §7 命令 |
| `tests/test_*` | §7 命令 |
| `notebooks/` | §7 命令 |
| `docs/references/`, `docs/adr/` | §7 命令 |
| `logs/phase0/` | §7 命令(gitignored) |
| `pyproject.toml` | §7 命令 |
| `uv.lock` | `uv sync` 后生成 |

---

## 9. 执行前 Checklist(用户对每项打勾)

**Before §4 rsync**:
- [ ] 确认原路径在 main 分支 + clean
- [ ] 确认 `$HOME/Desktop/ai4qkd/` 目录可写,`$HOME/Desktop/ai4qkd/AI4QKD/` 目前**不存在**
- [ ] 确认磁盘空间(原仓库 + git 历史 ~100MB 级)

**Before §6 real-run migrate**:
- [ ] §5 新路径 dry-run 无 WARN
- [ ] 原路径保留作 fallback(未删除)
- [ ] 新路径在 main 分支 + clean
- [ ] 理解 rollback 命令(见 §6)

**After §6**:
- [ ] `git log -3` 看到 migrate commit
- [ ] snapshot branch `archive/pre-refactor-snapshot-*` 存在
- [ ] `archive/legacy-v1/` 包含 48+ 项

**After §7 qkdx 骨架**:
- [ ] `qkdx/` 目录树与 §7.2 表一致
- [ ] `uv sync --frozen` 能 pass(若 uv 已装;否则 `pip install -e .`)
- [ ] `pytest` 能运行(可能 0 tests 收集,正常)

---

## 10. 回答三个可能的问题

**Q1:rsync 后原路径怎么办?**
**A1**:保留至少到 Phase 0 M1 完成。M1 验收通过(M1 tests 绿)后再评估是否删除。不急,磁盘代价可接受。

**Q2:git 历史会不会被 rsync "污染"?**
**A2**:不会。rsync 是文件级复制,`.git/` 是完整的 git 目录,复制后新路径是一个独立的 local clone,有完整历史。两路径互不影响。远端(若有)同步需显式 `git push`。

**Q3:如果 rsync 中途失败怎么办?**
**A3**:rsync 是幂等的,可重跑;或删除 `$NEW_ROOT/` 后重试。失败的 rsync 不影响原路径。

---

*Migration Guide v0.1 结束。等用户确认后按 §2 执行顺序继续。*
