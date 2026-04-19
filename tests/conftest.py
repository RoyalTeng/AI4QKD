"""
pytest 共享 fixtures
按 REFACTORING_PLAN §11.1 repro seed 启动 + §11.3 has_mosek() guard 对接。
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

# PROSPECTUS §11.1 / REFACTORING_PLAN §11.1 硬常量(基准日期)
DEFAULT_SEED: int = 20260418


@pytest.fixture(autouse=True)
def _seed_everything() -> None:
    """
    每个测试前设 seed;检查 PYTHONHASHSEED 与 DEFAULT_SEED 一致。

    PYTHONHASHSEED 必须在 Python 进程启动前设置;此处做 sanity check,
    不一致时发 stderr 警告(不 raise,允许本地快速测试)。
    """
    np.random.seed(DEFAULT_SEED)
    env_seed = os.environ.get("PYTHONHASHSEED")
    if env_seed != str(DEFAULT_SEED):
        print(
            f"[repro] WARN: PYTHONHASHSEED={env_seed!r}, expected {DEFAULT_SEED!r}. "
            f"Set it BEFORE starting python for deterministic hash ordering.",
            file=sys.stderr,
        )


@pytest.fixture
def rng() -> np.random.Generator:
    """固定种子 PRNG — 供随机测试使用"""
    return np.random.default_rng(DEFAULT_SEED)
