"""
AI 智能体模块

包含深度强化学习、演化算法、图编码器、混合智能体和强化学习环境。

版本 2.0.0 新特性：
- QKDSimEnv: 通用协议设计环境，支持协议无关的AI训练
- 扩展动作空间：从4种动作扩展到6种（新增协议重组和批量优化）
- 扩展观察空间：从64维扩展到128维，支持更复杂的协议表示
- 智能回退机制：确保在通用框架不可用时自动降级到传统方法
- 完整向后兼容性保证
"""

# 核心模块
from . import drl
from . import ea
from . import graph_encoder
from .hybrid_agent import HybridAgent

# 强化学习环境（新功能）
from .environment import QKDSimEnv

__all__ = [
    # 核心组件
    "drl",
    "ea", 
    "graph_encoder",
    "HybridAgent",
    # 新功能
    "QKDSimEnv",
]

__version__ = "2.0.0"
__author__ = "AI4QKD Team" 