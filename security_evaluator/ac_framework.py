"""
抽象密码学（AC）框架模块 - 向后兼容接口

此模块保持向后兼容性，同时提供到新通用框架的桥接。

警告：此模块中的部分功能已弃用，建议迁移到 universal_framework.py

新功能包括：
- 基于量子信息论的通用协议分析
- 熵累积理论应用  
- 可组合安全性分析
- 设备无关安全性评估

迁移指南：
- SecurityParameters -> UniversalSecurityParameters
- ProtocolType -> ProtocolFeatures
- 直接使用 UniversalSecurityFramework 进行安全性分析
"""

import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# 导入新的通用框架（优先使用）
try:
    from .universal_framework import (
        UniversalSecurityParameters,
        UniversalSecurityFramework,
        ProtocolFeatures,
        QuantumOperation,
        create_bb84_protocol,
        create_mdi_qkd_protocol,
        create_decoy_bb84_protocol
    )
    _UNIVERSAL_FRAMEWORK_AVAILABLE = True
except ImportError:
    _UNIVERSAL_FRAMEWORK_AVAILABLE = False
    warnings.warn(
        "Universal framework not available. Using legacy implementation.",
        ImportWarning
    )


class ProtocolType(Enum):
    """
    QKD协议类型（向后兼容）
    
    警告：此枚举已弃用。建议使用 ProtocolFeatures 类来描述协议特征。
    
    迁移示例：
    # 旧方式
    protocol_type = ProtocolType.BB84
    
    # 新方式
    protocol_features = create_bb84_protocol()
    """
    BB84 = "BB84"
    DECOY_BB84 = "Decoy-BB84"
    MDI_QKD = "MDI-QKD"
    TWIN_FIELD = "Twin-Field"
    
    def __init__(self, value):
        self._value_ = value
        warnings.warn(
            f"ProtocolType.{self.name} is deprecated. "
            f"Use create_{self.name.lower()}_protocol() from universal_framework instead.",
            DeprecationWarning,
            stacklevel=3
        )
    
    def to_protocol_features(self) -> 'ProtocolFeatures':
        """
        转换为新的 ProtocolFeatures 格式
        
        Returns:
            对应的 ProtocolFeatures 对象
        """
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework not available")
        
        factory_map = {
            'BB84': create_bb84_protocol,
            'DECOY_BB84': create_decoy_bb84_protocol,
            'MDI_QKD': create_mdi_qkd_protocol,
        }
        
        factory_func = factory_map.get(self.name)
        if factory_func:
            return factory_func()
        else:
            # 为未定义的协议创建基本特征
            return ProtocolFeatures(
                name=self.value,
                operations=[],
                parties=['Alice', 'Bob']
            )


@dataclass
class SecurityParameters:
    """
    安全性参数集合（向后兼容）
    
    定义了可组合安全性证明中所需的各种epsilon参数。
    
    警告：建议使用 UniversalSecurityParameters 以获得更完整的功能。
    
    迁移示例：
    # 旧方式
    params = SecurityParameters(epsilon_sec=1e-10)
    
    # 新方式（推荐）
    params = UniversalSecurityParameters(
        epsilon_sec=1e-10,
        entropy_smoothing_param=1e-8,
        composability_param=1e-7
    )
    """
    epsilon_sec: float = 1e-9  # 安全性参数 ( secrecy )
    epsilon_cor: float = 1e-15 # 正确性参数 ( correctness )
    epsilon_rob: float = 1e-9 # 鲁棒性参数 ( robustness )
    epsilon_pe: float = 1e-10 # 参数估计平滑参数
    epsilon_bar: float = 1e-10 # 最小熵平滑参数
    
    def get_total_privacy_error(self) -> float:
        """计算总的隐私错误预算"""
        return self.epsilon_sec + self.epsilon_pe
        
    def get_total_failure_prob(self) -> float:
        """计算总的协议失败概率"""
        return self.epsilon_cor + self.epsilon_rob
    
    def to_universal_parameters(self) -> 'UniversalSecurityParameters':
        """
        转换为新的 UniversalSecurityParameters 格式
        
        Returns:
            对应的 UniversalSecurityParameters 对象
        """
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework not available")
        
        return UniversalSecurityParameters(
            epsilon_sec=self.epsilon_sec,
            epsilon_cor=self.epsilon_cor,
            epsilon_rob=self.epsilon_rob,
            epsilon_pe=self.epsilon_pe,
            epsilon_bar=self.epsilon_bar,
            # 新框架的默认参数
            entropy_smoothing_param=self.epsilon_bar,
            composability_param=self.epsilon_sec * 0.1,
            device_independence_param=self.epsilon_sec * 0.01,
            finite_key_param=self.epsilon_rob
        )


# ==================== 便利函数 ====================

def create_legacy_security_analyzer():
    """
    创建传统安全性分析器的便利函数
    
    Returns:
        UniversalSecurityFramework 实例（如果可用）
    """
    if _UNIVERSAL_FRAMEWORK_AVAILABLE:
        return UniversalSecurityFramework()
    else:
        raise ImportError(
            "Universal framework not available. "
            "Please ensure universal_framework.py is properly installed."
        )


def migrate_protocol_type(old_type: ProtocolType) -> 'ProtocolFeatures':
    """
    迁移旧的协议类型到新格式
    
    Args:
        old_type: 旧的 ProtocolType 枚举值
        
    Returns:
        对应的 ProtocolFeatures 对象
    """
    warnings.warn(
        "migrate_protocol_type is a temporary migration aid. "
        "Please update your code to use ProtocolFeatures directly.",
        DeprecationWarning
    )
    
    return old_type.to_protocol_features()


def migrate_security_parameters(old_params: SecurityParameters) -> 'UniversalSecurityParameters':
    """
    迁移旧的安全参数到新格式
    
    Args:
        old_params: 旧的 SecurityParameters 对象
        
    Returns:
        对应的 UniversalSecurityParameters 对象
    """
    warnings.warn(
        "migrate_security_parameters is a temporary migration aid. "
        "Please update your code to use UniversalSecurityParameters directly.",
        DeprecationWarning
    )
    
    return old_params.to_universal_parameters()


# ==================== 向后兼容性导出 ====================

# 保持旧的导入路径可用
__all__ = [
    'ProtocolType',
    'SecurityParameters', 
    'create_legacy_security_analyzer',
    'migrate_protocol_type',
    'migrate_security_parameters'
]

# 如果新框架可用，也导出新的类
if _UNIVERSAL_FRAMEWORK_AVAILABLE:
    __all__.extend([
        'UniversalSecurityParameters',
        'UniversalSecurityFramework', 
        'ProtocolFeatures',
        'QuantumOperation'
    ]) 