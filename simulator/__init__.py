"""
量子仿真器模块

该模块提供了QKD协议的量子物理仿真功能，包括：
- 量子态准备仿真（WCP、真空态、诱骗态等）
- 量子信道建模（损耗、退相干、噪声等）
- 量子测量仿真（Z/X基测量）
- 性能指标计算（QBER、Gain、密钥率等）
- 通用协议仿真（协议无关的通用框架）

主要组件：
- QuantumSimulator: 主仿真器类（向后兼容）
- UniversalQuantumSimulator: 通用仿真器（协议无关）
- StatePreparation: 量子态准备仿真
- ChannelModel: 量子信道建模
- MeasurementModel: 量子测量仿真
- PerformanceMetrics: 性能指标计算

版本 2.0.0 新特性：
- 支持任意协议图的通用仿真
- 基于QuantumOperation序列的统一处理
- 智能协议识别和自动配置
- 完整向后兼容性保证
"""

# 通用仿真器（新功能）
from .universal_quantum_simulator import UniversalQuantumSimulator

# 传统仿真器（向后兼容）
from .real_quantum_simulator import RealQuantumSimulator as QuantumSimulator

# 核心组件
from .state_preparation import StatePreparation
from .channel_model import ChannelModel
from .measurement import Measurement
from .performance_metrics import PerformanceMetrics
from .noise_model import NoiseModel
from .qiskit_interface import QiskitInterface

__version__ = "2.0.0"
__author__ = "AI4QKD Team"

__all__ = [
    # 新功能
    "UniversalQuantumSimulator",
    # 向后兼容
    "QuantumSimulator",
    # 核心组件
    "StatePreparation", 
    "ChannelModel",
    "Measurement",
    "PerformanceMetrics",
    "NoiseModel",
    "QiskitInterface"
] 