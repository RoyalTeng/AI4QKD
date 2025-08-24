"""
AI4QKD - 探测器模型模块 (简化实现)

重构思路：
- 基于单光子探测原理建模
- 考虑探测器的各种非理想特性
- 支持多种探测器类型（APD、SPAD等）
- 验证探测效率和噪声的建模

作者: Claude (AI Assistant)
重构日期: 2025-08-24
"""

import numpy as np
from typing import Dict, Any

class DetectorModel:
    """探测器模型基类"""
    
    def __init__(self, efficiency: float = 0.8):
        self.efficiency = efficiency
    
    def detect_photon(self, photon_present: bool = True) -> bool:
        """模拟光子探测"""
        if photon_present:
            return np.random.random() < self.efficiency
        return False

class SinglePhotonDetector(DetectorModel):
    """单光子探测器模型"""
    
    def __init__(self, efficiency: float = 0.8, dark_count_rate: float = 1e-6):
        super().__init__(efficiency)
        self.dark_count_rate = dark_count_rate
    
    def detect_photon(self, photon_present: bool = True) -> bool:
        """考虑暗计数的光子探测"""
        # 暗计数概率
        dark_count = np.random.random() < self.dark_count_rate
        
        # 信号光子探测
        signal_detected = False
        if photon_present:
            signal_detected = np.random.random() < self.efficiency
        
        return signal_detected or dark_count

def simulate_detection_efficiency(efficiency: float = 0.8, 
                                photon_count: int = 1000) -> float:
    """仿真探测效率的便捷函数"""
    detector = SinglePhotonDetector(efficiency)
    detected_count = sum(detector.detect_photon(True) for _ in range(photon_count))
    return detected_count / photon_count