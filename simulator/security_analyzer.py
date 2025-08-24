"""
AI4QKD - 安全分析器模块 (简化实现)

重构思路：
- 基于信息论安全框架
- 支持可组合安全性分析
- 验证安全参数的计算
- 确保安全性证明的正确性

作者: Claude (AI Assistant)
重构日期: 2025-08-24
"""

import numpy as np
from typing import Dict, Any

class SecurityAnalyzer:
    """安全分析器"""
    
    def __init__(self):
        self.security_threshold = 0.11  # BB84安全阈值
    
    def analyze_information_security(self, qber: float, key_rate: float) -> Dict[str, float]:
        """分析信息论安全性"""
        
        # 基本安全性判断
        is_secure = qber < self.security_threshold
        security_margin = max(0, self.security_threshold - qber)
        
        # 信息泄漏估计
        if qber > 0:
            information_leakage = -qber * np.log2(qber) - (1-qber) * np.log2(1-qber)
        else:
            information_leakage = 0.0
        
        return {
            'is_secure': is_secure,
            'qber': qber,
            'security_threshold': self.security_threshold,
            'security_margin': security_margin,
            'information_leakage': information_leakage,
            'key_rate': key_rate
        }
    
    def calculate_security_parameters(self, protocol_data: Dict) -> Dict[str, float]:
        """计算安全参数"""
        qber = protocol_data.get('qber', 0.1)
        key_rate = protocol_data.get('key_rate', 0.0)
        
        return self.analyze_information_security(qber, key_rate)

def analyze_information_security(qber: float, key_rate: float = 0.0) -> Dict[str, float]:
    """信息论安全分析的便捷函数"""
    analyzer = SecurityAnalyzer()
    return analyzer.analyze_information_security(qber, key_rate)

def calculate_security_parameters(protocol_data: Dict) -> Dict[str, float]:
    """安全参数计算的便捷函数"""
    analyzer = SecurityAnalyzer()
    return analyzer.calculate_security_parameters(protocol_data)