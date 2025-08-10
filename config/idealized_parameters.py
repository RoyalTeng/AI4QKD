"""
理想化参数设置方案
===============

为AI4QKD科学研究的原理验证阶段设计的理想化参数配置。
该配置基于对参考文献的分析，采用合理的理想化假设以简化研究复杂度。

设计原则：
1. 消除硬件限制，专注于协议设计算法的验证
2. 保持物理合理性，不违反量子力学基本原理
3. 简化噪声模型，突出协议结构的影响
4. 为AI智能体提供清晰的优化信号
"""

from enum import Enum
from qcgf_dsl.node_types import NodeType, Party
from qcgf_dsl.edge_types import EdgeType

# ============================================================================
# 理想化设备参数模板
# ============================================================================

# 理想化节点类型参数模板
IDEALIZED_NODE_TEMPLATES = {
    NodeType.QSP: {
        "state": "|0⟩",
        "fidelity": 1.0,           # 理想态制备：100%保真度
        "preparation_time": 0.0,    # 理想化：瞬时态制备
        "party": Party.ALICE
    },
    NodeType.QC: {
        "loss": 0.0,               # 理想化：无损耗信道
        "noise": 0.0,              # 理想化：无噪声信道
        "distance": 100.0,         # 设定标准距离100km
        "channel_type": "ideal_quantum_channel",
        "transmission_time": 0.0    # 理想化：瞬时传输
    },
    NodeType.QM: {
        "basis": "computational",
        "efficiency": 1.0,         # 理想化：100%测量效率
        "dark_count_rate": 0.0,    # 理想化：无暗计数
        "measurement_time": 0.0,   # 理想化：瞬时测量
        "party": Party.BOB
    },
    NodeType.QG: {
        "gate_type": "H",
        "fidelity": 1.0,           # 理想化：完美量子门
        "gate_time": 0.0           # 理想化：瞬时量子门操作
    },
    NodeType.QD: {
        "detector_type": "ideal_SPD",
        "efficiency": 1.0,         # 理想化：100%检测效率
        "dark_count_rate": 0.0,    # 理想化：无暗计数
        "dead_time": 0.0,          # 理想化：无死时间
        "timing_jitter": 0.0       # 理想化：无时间抖动
    },
    NodeType.CLO: {
        "operation": "XOR",
        "processing_time": 0.0,    # 理想化：瞬时经典处理
        "error_rate": 0.0,         # 理想化：无经典处理错误
        "party": Party.ALICE
    },
    NodeType.CS: {
        "storage_type": "ideal_memory",
        "capacity": float('inf'),   # 理想化：无限存储容量
        "access_time": 0.0,        # 理想化：瞬时访问
        "error_rate": 0.0          # 理想化：无存储错误
    },
    NodeType.CC: {
        "bandwidth": float('inf'),  # 理想化：无限带宽
        "latency": 0.0,            # 理想化：零延迟
        "error_rate": 0.0          # 理想化：无传输错误
    },
    NodeType.BSM: {
        "efficiency": 1.0,         # 理想化：100%贝尔态测量效率
        "party": Party.CHARLIE,
        "measurement_time": 0.0    # 理想化：瞬时测量
    },
    NodeType.ATTACK: {
        "attack_type": "intercept_resend",
        "intercept_probability": 0.5,
        "party": Party.EVE,
        "detection_probability": 1.0  # 理想化：攻击总是被完美检测
    },
    NodeType.SINK: {
        "sink_type": "key_generation",
        "party": Party.BOB,
        "processing_efficiency": 1.0  # 理想化：完美密钥生成
    }
}

# 理想化边类型参数模板
IDEALIZED_EDGE_TEMPLATES = {
    EdgeType.QUANTUM: {
        "loss": 0.0,               # 理想化：无损耗
        "noise": 0.0,              # 理想化：无噪声
        "distance": 100.0,         # 标准距离
        "wavelength": 1550.0,      # 标准通信波长
        "bandwidth": float('inf'), # 理想化：无限带宽
        "transmission_fidelity": 1.0,  # 理想化：完美传输保真度
        "decoherence_time": float('inf')  # 理想化：无退相干
    },
    EdgeType.CLASSICAL: {
        "bandwidth": float('inf'), # 理想化：无限带宽
        "latency": 0.0,           # 理想化：零延迟
        "error_rate": 0.0,        # 理想化：无错误
        "security": "perfect"      # 理想化：完美安全经典信道
    },
    EdgeType.CONTROL: {
        "signal_type": "ideal_digital",
        "voltage": 3.3,
        "frequency": float('inf'), # 理想化：无限频率
        "response_time": 0.0       # 理想化：瞬时响应
    },
    EdgeType.DATA: {
        "data_type": "raw_key",
        "compression_ratio": 1.0,
        "encryption": True,        # 保持安全性要求
        "throughput": float('inf') # 理想化：无限吞吐量
    },
    EdgeType.FEEDBACK: {
        "feedback_type": "error_correction",
        "delay": 0.0,             # 理想化：即时反馈
        "accuracy": 1.0           # 理想化：完美反馈准确性
    },
    EdgeType.SYNCHRONIZATION: {
        "sync_type": "perfect_clock",
        "frequency": 1e9,
        "jitter": 0.0,           # 理想化：无时钟抖动
        "phase_accuracy": 1.0     # 理想化：完美相位精度
    }
}

# ============================================================================
# 理想化协议配置
# ============================================================================

# 理想化BB84协议参数
IDEALIZED_BB84_PARAMS = {
    'qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
        'state_fidelity': 1.0,     # 理想化：完美态制备
        'preparation_efficiency': 1.0
    },
    'qc': {
        'loss': 0.0,              # 理想化：无损耗
        'error_rate': 0.0,        # 理想化：无信道错误
        'decoherence_rate': 0.0   # 理想化：无退相干
    },
    'qm': {
        'basis_choice': ['Z', 'X'],
        'efficiency': 1.0,        # 理想化：完美探测
        'dark_count_rate': 0.0,   # 理想化：无暗计数
        'timing_resolution': 0.0   # 理想化：完美时间分辨率
    },
    'security': {
        'protocol_type': 'Idealized-BB84',
        'params': {
            'p_signal': 1.0,
            'leakage': 0.0,       # 理想化：无信息泄露
            'privacy_amplification_efficiency': 1.0  # 理想化：完美隐私放大
        }
    }
}

# 理想化MDI-QKD协议参数
IDEALIZED_MDI_QKD_PARAMS = {
    'alice_qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
        'state_fidelity': 1.0
    },
    'bob_qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
        'state_fidelity': 1.0
    },
    'alice_qc': {
        'loss': 0.0,
        'error_rate': 0.0
    },
    'bob_qc': {
        'loss': 0.0,
        'error_rate': 0.0
    },
    'charlie_bsm': {
        'efficiency': 1.0,        # 理想化：完美贝尔态测量
        'success_probability': 1.0  # 理想化：贝尔态测量总是成功
    },
    'security': {
        'protocol_type': 'Idealized-MDI-QKD',
        'params': {
            'measurement_device_trust': 0.0  # 理想化：测量设备不可信但完美工作
        }
    }
}

# 理想化诱骗态协议参数
IDEALIZED_DECOY_BB84_PARAMS = {
    'intensities': {
        'signal': {'value': 0.5, 'probability': 0.8, 'fidelity': 1.0},
        'decoy': {'value': 0.1, 'probability': 0.1, 'fidelity': 1.0},
        'vacuum': {'value': 0.0, 'probability': 0.1, 'fidelity': 1.0},
    },
    'qsp': {
        'basis_choice': ['Z', 'X'],
        'num_states': 100000,
        'intensity_control_precision': 1.0  # 理想化：完美强度控制
    },
    'qc': {
        'loss': 0.0,
        'error_rate': 0.0,
        'multi_photon_suppression': 1.0  # 理想化：完美多光子抑制
    },
    'qm': {
        'basis_choice': ['Z', 'X'],
        'efficiency': 1.0,
        'photon_number_resolution': True   # 理想化：完美光子数分辨
    },
    'security': {
        'protocol_type': 'Idealized-Decoy-BB84',
        'params': {
            'f_ec': 1.0,          # 理想化：完美纠错效率
            'statistical_fluctuation': 0.0  # 理想化：无统计涨落
        }
    }
}

# ============================================================================
# 理想化环境参数
# ============================================================================

# 理想化环境设置
IDEALIZED_ENVIRONMENT_PARAMS = {
    # 物理环境
    'temperature': 273.15,         # 标准温度（0°C），无温度涨落
    'temperature_stability': 0.0,  # 理想化：完美温度稳定性
    'humidity': 0.0,              # 理想化：无湿度影响
    'vibration': 0.0,             # 理想化：无机械振动
    'electromagnetic_interference': 0.0,  # 理想化：无电磁干扰
    
    # 量子环境
    'vacuum_quality': 1.0,        # 理想化：完美真空
    'stray_light': 0.0,           # 理想化：无杂散光
    'cosmic_ray_interference': 0.0,  # 理想化：无宇宙射线干扰
    
    # 经典环境
    'computational_noise': 0.0,   # 理想化：无计算噪声
    'clock_drift': 0.0,           # 理想化：无时钟漂移
    'power_supply_stability': 1.0  # 理想化：完美电源稳定性
}

# ============================================================================
# 安全性分析的理想化参数
# ============================================================================

# 理想化安全性评估参数
IDEALIZED_SECURITY_PARAMS = {
    # Eve的攻击能力限制
    'eve_constraints': {
        'storage_capacity': float('inf'),    # Eve有无限量子存储能力
        'computational_power': float('inf'), # Eve有无限计算能力
        'measurement_precision': 1.0,        # Eve有完美测量能力
        'quantum_memory_coherence': float('inf'),  # Eve有完美量子记忆
        'but_follows_physics': True          # 但仍需遵循量子力学定律
    },
    
    # 合法方的能力
    'legitimate_parties': {
        'alice_bob_authenticated_channel': True,  # Alice和Bob有完美认证信道
        'perfect_randomness_source': True,        # 完美随机数源
        'error_correction_efficiency': 1.0,       # 理想化：完美纠错
        'privacy_amplification_efficiency': 1.0,  # 理想化：完美隐私放大
        'key_consumption_for_authentication': 0.0  # 理想化：认证不消耗密钥
    },
    
    # 信息论安全性
    'information_theoretic_security': {
        'epsilon_correctness': 0.0,     # 理想化：完美正确性
        'epsilon_secrecy': 0.0,         # 理想化：完美保密性
        'finite_key_effects': False,    # 忽略有限密钥效应
        'composable_security': True     # 保持可组合安全性要求
    }
}

# ============================================================================
# AI智能体训练的理想化参数
# ============================================================================

# 理想化AI训练环境
IDEALIZED_AI_TRAINING_PARAMS = {
    # 训练效率优化
    'num_episodes': 50,              # 增加训练轮数用于更充分的探索
    'max_steps_per_episode': 30,    # 增加每轮步数
    'convergence_threshold': 1e-6,   # 理想化：精确收敛判据
    
    # 奖励函数理想化
    'reward_calculation': {
        'keyrate_weight': 1.0,
        'security_weight': 1.0,
        'implementation_complexity_weight': 0.0,  # 忽略实现复杂度
        'hardware_cost_weight': 0.0,             # 忽略硬件成本
        'noise_tolerance_weight': 0.0,           # 忽略噪声容忍度
    },
    
    # 理想化学习环境
    'perfect_simulator': True,        # 仿真器无计算误差
    'deterministic_evaluation': True, # 确定性评估，无随机涨落
    'infinite_computational_budget': True,  # 无计算资源限制
}

# ============================================================================
# 使用说明
# ============================================================================

def get_idealized_config(protocol_type='BB84'):
    """
    获取指定协议的理想化配置
    
    Args:
        protocol_type: 协议类型 ('BB84', 'MDI-QKD', 'Decoy-BB84')
    
    Returns:
        dict: 理想化配置字典
    """
    configs = {
        'BB84': IDEALIZED_BB84_PARAMS,
        'MDI-QKD': IDEALIZED_MDI_QKD_PARAMS,
        'Decoy-BB84': IDEALIZED_DECOY_BB84_PARAMS
    }
    
    base_config = {
        'node_templates': IDEALIZED_NODE_TEMPLATES,
        'edge_templates': IDEALIZED_EDGE_TEMPLATES,
        'environment': IDEALIZED_ENVIRONMENT_PARAMS,
        'security': IDEALIZED_SECURITY_PARAMS,
        'ai_training': IDEALIZED_AI_TRAINING_PARAMS
    }
    
    if protocol_type in configs:
        base_config['protocol_specific'] = configs[protocol_type]
    
    return base_config

# ============================================================================
# 理论验证说明
# ============================================================================

"""
理想化假设的理论合理性：

1. 物理合理性：
   - 所有理想化参数都在量子力学允许的范围内
   - 不违反no-cloning定理、不确定性原理等基本定律
   - 保持量子信息的幺正性和局域性

2. 信息论合理性：
   - 遵循Shannon-Holevo定理的信息传输限制
   - 保持量子密码学的信息论安全基础
   - 不超越物理可实现的信息处理极限

3. 科学研究价值：
   - 消除硬件噪声的干扰，专注于协议设计算法验证
   - 为AI智能体提供清晰的优化目标和奖励信号
   - 建立协议性能的理论上界基准

4. 渐进扩展可能：
   - 理想化参数可以逐步向现实参数过渡
   - 为未来的硬件改进提供性能目标
   - 建立从理论到实践的完整研究路径

使用建议：
- 在研究初期使用理想化配置验证AI算法有效性
- 逐步引入现实的硬件限制，验证算法鲁棒性
- 对比理想与现实情况，量化硬件限制的影响
"""