"""
AI4QKD - 信道模型模块 (简化实现)

重构思路：
- 基于光学传输理论建模
- 支持多种信道类型（光纤、自由空间）
- 考虑环境因素对传输的影响
- 提供信道损耗和噪声的准确计算

作者: Claude (AI Assistant)
重构日期: 2025-08-24
"""

import numpy as np
from typing import Dict, Any

class ChannelModel:
    """信道模型基类"""
    
    def calculate_loss(self, distance: float) -> float:
        """计算信道损耗"""
        return 0.0
    
    def calculate_noise(self, parameters: Dict) -> float:
        """计算信道噪声"""
        return 0.0

class FiberChannelModel(ChannelModel):
    """光纤信道模型"""
    
    def __init__(self, loss_coefficient: float = 0.2):
        self.loss_coefficient = loss_coefficient
    
    def calculate_loss(self, distance: float) -> float:
        """计算光纤损耗 (dB)"""
        return self.loss_coefficient * distance

class FreeSpaceChannelModel(ChannelModel):
    """自由空间信道模型"""
    
    def calculate_loss(self, distance: float) -> float:
        """计算自由空间损耗"""
        # 几何损耗 + 大气吸收
        geometric_loss = 20 * np.log10(distance * 1000)  # km to m
        atmospheric_loss = 0.1 * distance  # 简化大气损耗
        return geometric_loss + atmospheric_loss

def calculate_channel_loss(channel_type: str = "fiber", distance: float = 50.0, **kwargs) -> float:
    """计算信道损耗的便捷函数"""
    if channel_type == "fiber":
        model = FiberChannelModel(**kwargs)
    else:
        model = FreeSpaceChannelModel(**kwargs)
    
    return model.calculate_loss(distance)