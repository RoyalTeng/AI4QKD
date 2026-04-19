#!/usr/bin/env bash
# scripts/migrate_legacy.sh — 归档 AI4QKD v1 legacy 到 archive/legacy-v1/
# v3.2(2026-04-19 用户第三轮审查后)
#
# 设计约束:
#   1. **保留现有 git 历史**(不 git init 新仓库)
#   2. rsync 到无空格路径作为独立步骤,本脚本不处理 rsync
#   3. 本脚本只做:insurance snapshot branch → archive → commit
#   4. --dry-run 模式:不改任何文件,只打印将执行的动作
#   5. 人工确认后再真跑,不自动执行破坏性动作
#
# 执行顺序(见 docs/PHASE0_MIGRATION_GUIDE.md):
#   (a) 脚本成形(本文件)
#   (b) 在原路径 --dry-run 审查输出
#   (c) rsync(手动命令)到 $HOME/Desktop/ai4qkd/AI4QKD/
#   (d) 在新路径 --dry-run 再审一次
#   (e) 人工确认
#   (f) 新路径真跑 bash scripts/migrate_legacy.sh
#   (g) 创建 qkdx/ 骨架(独立步骤,不在本脚本)

set -Eeuo pipefail

# --------------------------------------------------------------------------
# 强制 bash(zsh 下 shopt / dotglob 行为不同)
# --------------------------------------------------------------------------
[[ -n "${BASH_VERSION:-}" ]] || {
  echo "ERROR: this script requires bash. Current shell appears not to be bash." >&2
  exit 1
}

shopt -s dotglob nullglob

# --------------------------------------------------------------------------
# Args
# --------------------------------------------------------------------------
DRY_RUN=0
case "${1:-}" in
  --dry-run) DRY_RUN=1 ;;
  "") DRY_RUN=0 ;;
  *)
    echo "usage: $0 [--dry-run]" >&2
    exit 2
    ;;
esac

# --------------------------------------------------------------------------
# Pretty print helpers
# --------------------------------------------------------------------------
tag() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY] %s\n' "$*"
  else
    printf '[EXEC] %s\n' "$*"
  fi
}

warn() { printf 'WARN: %s\n' "$*" >&2; }
fatal() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

run() {
  # 执行命令,dry-run 只打印
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY] cmd: '
    printf '%q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

# --------------------------------------------------------------------------
# Pre-check #1: git worktree
# --------------------------------------------------------------------------
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  fatal "not inside a git worktree. Run this script inside the AI4QKD repo."
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
if [[ "$PWD" != "$REPO_ROOT" ]]; then
  fatal "current dir is not repo root. cd to $REPO_ROOT first."
fi

# --------------------------------------------------------------------------
# Pre-check #2: 路径不含空格(dry-run 允许,real-run 拒绝)
# --------------------------------------------------------------------------
if [[ "$PWD" =~ [[:space:]] ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    warn "current path contains whitespace: $PWD"
    warn "  — dry-run allows this, but real-run will refuse"
    warn "  — rsync to a space-free path first (see docs/PHASE0_MIGRATION_GUIDE.md)"
  else
    fatal "current path contains whitespace: $PWD
       rsync to a space-free path before running (see docs/PHASE0_MIGRATION_GUIDE.md)"
  fi
fi

# --------------------------------------------------------------------------
# Pre-check #3: 工作树 / 暂存区干净
# --------------------------------------------------------------------------
DIRTY=0
if ! git diff --quiet; then
  warn "unstaged changes present"
  DIRTY=1
fi
if ! git diff --cached --quiet; then
  warn "staged (uncommitted) changes present"
  DIRTY=1
fi
if [[ "$DIRTY" == "1" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    warn "  — dry-run continues; real-run will refuse"
  else
    fatal "working tree or index is dirty. Commit or stash before running real migration."
  fi
fi

# --------------------------------------------------------------------------
# Pre-check #4: 当前分支必须是 main(real-run 要求)
# --------------------------------------------------------------------------
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    warn "current branch is '$CURRENT_BRANCH', not 'main'"
    warn "  — dry-run continues; real-run will checkout main first"
  else
    fatal "current branch is '$CURRENT_BRANCH', expected 'main'. Switch before migrating."
  fi
fi

tag "✓ pre-checks complete"
tag "  PWD            = $PWD"
tag "  CURRENT_BRANCH = $CURRENT_BRANCH"
tag "  DRY_RUN        = $DRY_RUN"
tag ""

# --------------------------------------------------------------------------
# Step 1: 创建 insurance snapshot branch
# --------------------------------------------------------------------------
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
SNAPSHOT_BRANCH="archive/pre-refactor-snapshot-${TIMESTAMP}"

tag "Step 1: create snapshot branch '${SNAPSHOT_BRANCH}' (保留 git 历史,不 git init)"
run git branch "$SNAPSHOT_BRANCH"
tag ""

# --------------------------------------------------------------------------
# Step 2: 归档清单 — KEEP / ARCHIVE 分类
# --------------------------------------------------------------------------
# 顶层项目保留清单(保留,不归档):
KEEP_LIST=(
  # Git / 系统
  ".git"
  ".gitignore"
  ".claude"
  ".DS_Store"                  # 不归档,但也不动(gitignore 已排除)
  # 缓存 / 环境(gitignore 已排除)
  ".pytest_cache"
  ".mypy_cache"
  ".ruff_cache"
  ".venv"
  "venv"
  # 本项目已建的目录
  "archive"                    # 归档目标自身
  "docs"                       # v2 项目文档层
  "scripts"                    # 本脚本所在
  # v2 新建(本次执行时还没创建,保留避免误移)
  "qkdx"
  "tests"
  "notebooks"
  "pyproject.toml"
  "uv.lock"
)

is_kept() {
  local item="$1"
  local kept
  for kept in "${KEEP_LIST[@]}"; do
    if [[ "$item" == "$kept" ]]; then
      return 0
    fi
  done
  return 1
}

# --------------------------------------------------------------------------
# Step 3: 归档 legacy
# --------------------------------------------------------------------------
ARCHIVE_DIR="archive/legacy-v1"
tag "Step 2-3: archive legacy items to ${ARCHIVE_DIR}/"
run mkdir -p "$ARCHIVE_DIR"

declare -a TO_ARCHIVE=()
declare -a TO_KEEP=()

for item in *; do
  if is_kept "$item"; then
    TO_KEEP+=("$item")
  else
    TO_ARCHIVE+=("$item")
  fi
done

tag ""
tag "  keep (${#TO_KEEP[@]} items):"
for k in "${TO_KEEP[@]}"; do
  tag "    ✓ $k"
done

tag ""
tag "  archive (${#TO_ARCHIVE[@]} items):"
for a in "${TO_ARCHIVE[@]}"; do
  tag "    → $a  →  $ARCHIVE_DIR/"
done
tag ""

# 真跑时执行 git mv
for item in "${TO_ARCHIVE[@]}"; do
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY] cmd: git mv -k -- %q %q\n' "$item" "$ARCHIVE_DIR/"
  else
    # git mv -k:skip 无法移动项;失败 fallback 到 mv + git add
    if ! git mv -k -- "$item" "$ARCHIVE_DIR/" 2>/dev/null; then
      mv -- "$item" "$ARCHIVE_DIR/"
      git add -A
    fi
  fi
done

# --------------------------------------------------------------------------
# Step 4: 写归档 README
# --------------------------------------------------------------------------
ARCHIVE_README="$ARCHIVE_DIR/README_ARCHIVE.md"
tag "Step 4: write archival README to $ARCHIVE_README"

if [[ "$DRY_RUN" == "1" ]]; then
  tag "  (dry-run: would write ~25 lines)"
else
  cat > "$ARCHIVE_README" <<'EOF'
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
EOF
  git add "$ARCHIVE_README"
fi

# --------------------------------------------------------------------------
# Step 5: Commit
# --------------------------------------------------------------------------
tag ""
tag "Step 5: commit archival changes"

if [[ "$DRY_RUN" == "1" ]]; then
  tag '  cmd: git commit -m "chore(migrate): archive legacy v1 → archive/legacy-v1/"'
else
  git commit -m "chore(migrate): archive legacy v1 → archive/legacy-v1/

Archived ${#TO_ARCHIVE[@]} top-level items (code + legacy docs + run 产物) to
archive/legacy-v1/. KEEP_LIST 保护 .git / docs / scripts / v2 新建目录。

Snapshot branch: ${SNAPSHOT_BRANCH}
Rollback: git checkout \$SNAPSHOT_BRANCH"
fi

# --------------------------------------------------------------------------
# 完成
# --------------------------------------------------------------------------
tag ""
tag "✓ migration complete"
tag "  snapshot branch (rollback): ${SNAPSHOT_BRANCH}"
tag "  archived:                   ${#TO_ARCHIVE[@]} items"
tag "  kept:                       ${#TO_KEEP[@]} items"
tag ""
tag "next steps:"
tag "  1. Verify with: git log -3 && git diff HEAD~1 --stat"
tag "  2. Create qkdx/ skeleton per docs/REFACTORING_PLAN.md §3"
tag "     (bash scripts/create_qkdx_skeleton.sh — 另发脚本)"
tag "  3. Start M1 WLC SDP BB84 TDD per docs/RESEARCH_PLAN.md §2.1"

if [[ "$DRY_RUN" == "1" ]]; then
  tag ""
  tag "(this was a dry-run; no changes made)"
fi
