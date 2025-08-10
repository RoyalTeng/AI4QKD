"""
预定义的QKD协议物理参数配置
"""

# BB84 协议的默认参数
BB84_PARAMS = {
    # 量子态制备 (QSP) 节点参数
    'qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
    },
    # 量子信道 (QC) 节点参数
    'qc': {
        'loss': 0.1,        # 10% 信道损耗
        'error_rate': 0.02, # 2% 信道错误率 (退偏振)
    },
    # 量子测量 (QM) 节点参数
    'qm': {
        'basis_choice': ['Z', 'X'],
        'efficiency': 0.8, # 80% 探测效率
    },
    # 安全性评估参数
    'security': {
        'protocol_type': 'BB84',
        'params': {'p_signal': 1.0, 'leakage': 0.01}
    }
}

# MDI-QKD 协议的默认参数
MDI_QKD_PARAMS = {
    'alice_qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
    },
    'bob_qsp': {
        'num_states': 100000,
        'basis_choice': ['Z', 'X'],
    },
    'alice_qc': {
        'loss': 0.25,
        'error_rate': 0.01,
    },
    'bob_qc': {
        'loss': 0.25,
        'error_rate': 0.01,
    },
    'charlie_bsm': {
        'efficiency': 0.5, # 贝尔态测量效率
    },
    'security': {
        'protocol_type': 'MDI-QKD',
        'params': {}
    }
}

# 诱骗态 BB84 协议的参数
DECOY_BB84_PARAMS = {
    # 定义三种强度: 信号 (signal), 弱诱骗 (decoy), 真空 (vacuum)
    'intensities': {
        'signal': {'value': 0.5, 'probability': 0.8},
        'decoy': {'value': 0.1, 'probability': 0.1},
        'vacuum': {'value': 0.0, 'probability': 0.1},
    },
    'qsp': {
        'basis_choice': ['Z', 'X'],
        'num_states': 100000 
    },
    'qc': {
        'loss': 0.2,       # 20% 信道损耗
        'error_rate': 0.01, # 1% 信道错误率
    },
    'qm': {
        'basis_choice': ['Z', 'X'],
        'efficiency': 0.8,
    },
    'security': {
        'protocol_type': 'Decoy-BB84',
        'params': {'f_ec': 1.16} # 纠错效率因子
    }
}

# 更多协议的参数可以继续添加...
# DECOY_STATE_BB84_PARAMS = { ... } 