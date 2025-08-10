"""
安全性评估模块

本模块提供QKD协议的安全性评估功能，包括：
- 密钥率计算（基于抽象密码学框架）
- 熵估计（最小熵、条件熵）
- 有限密钥分析
- 可组合安全性分析
- 通用安全性分析（协议无关的通用框架）

版本 2.0.0 新特性：
- UniversalKeyRateCalculator: 支持任意协议的密钥率计算
- UniversalEntropyEstimator: 基于量子信息论的通用熵估计
- 协议无关的安全性分析框架
- 完整向后兼容性保证
"""

# 通用安全性分析器（新功能）
from .key_rate_calculator import UniversalKeyRateCalculator
from .entropy_estimator import UniversalEntropyEstimator

# 传统安全性分析器（向后兼容）
from .key_rate_calculator import KeyRateCalculator, KeyRateParameters, KeyRateResult
from .entropy_estimator import EntropyEstimator
from .finite_key_analysis import FiniteKeyAnalyzer
from .composable_security import ComposableSecurityAnalyzer, ComposableSecurityResult
from .ac_framework import ProtocolType, SecurityParameters

__all__ = [
    # 新功能
    "UniversalKeyRateCalculator",
    "UniversalEntropyEstimator",
    # 向后兼容
    "KeyRateCalculator",
    "KeyRateParameters", 
    "KeyRateResult",
    "EntropyEstimator",
    "FiniteKeyAnalyzer",
    "ComposableSecurityAnalyzer",
    "ComposableSecurityResult",
    "ProtocolType",
    "SecurityParameters",
]

__version__ = '2.0.0'
__author__ = 'AI4QKD Team' 