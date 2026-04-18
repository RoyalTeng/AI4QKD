"""
量子仿真器 - 简化版
"""

import numpy as np
from typing import Dict, Any
from dataclasses import dataclass
import time


@dataclass
class SimulationResult:
    """仿真结果"""
    protocol_name: str
    pulse_count: int
    qber: float  # 量子比特错误率
    gain: float  # 增益
    raw_key_rate: float  # 原始密钥率
    simulation_time: float


class QuantumSimulator:
    """量子仿真器"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.rng = np.random.default_rng(42)
    
    def simulate(self, protocol, **kwargs):
        """仿真协议"""
        start_time = time.time()
        
        # 合并配置
        config = {**self.config, **kwargs}
        pulse_count = config.get('pulse_count', 10000)
        
        # 简单仿真逻辑
        channel_loss = config.get('channel_loss', 0.1)
        detector_efficiency = config.get('detector_efficiency', 0.8)
        phase_error = config.get('phase_error_rate', 0.01)
        
        # 计算有效脉冲
        transmitted = pulse_count
        lost = int(transmitted * channel_loss)
        detected = int((transmitted - lost) * detector_efficiency)
        
        # 计算错误
        error_pulses = int(detected * phase_error)
        
        # 计算匹配基（假设50%）
        matching_bases = detected // 2
        
        # 计算指标
        gain = detected / transmitted
        qber = error_pulses / detected if detected > 0 else 0
        raw_key_rate = matching_bases / transmitted
        
        simulation_time = time.time() - start_time
        
        return SimulationResult(
            protocol_name=protocol.name,
            pulse_count=pulse_count,
            qber=qber,
            gain=gain,
            raw_key_rate=raw_key_rate,
            simulation_time=simulation_time
        )