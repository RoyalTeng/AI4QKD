"""
AI4QKD - 节点类型定义模块 (严格按照研究方案)

设计依据：
- 严格遵循f:\AI4QKD\研究方案\第一部分.pdf中2.2节的定义
- 实现研究方案要求的10种标准节点类型
- 完整实现每种节点类型的子类型系统
- 确保参数模板与研究方案精确匹配

核心节点类型（按研究方案）：
量子层：QSP(量子源), QOP(量子操作), QC(量子信道), QI(量子干涉), QM(量子测量)
经典层：CIS(经典信息源), CLO(经典逻辑操作), CC(经典信道), CD(经典决策)
输出层：KE(密钥提取)

重要变更：
- 移除了不在研究方案中的节点类型（QG、QD、BSM、CS、ATTACK、SINK）
- 新增了缺失的核心节点类型（QOP、QI、CIS、CD、KE）
- 实现了完整的子类型系统
- 重新设计了参数模板以符合研究方案

作者: Claude (AI Assistant) 
重构日期: 2025-08-19
依据文档: f:\AI4QKD\研究方案\第一部分.pdf
"""

import os
from enum import Enum
from typing import Dict, Any, Optional, List, Union


# =============================================================================
# 研究方案标准节点类型定义
# 依据: f:\AI4QKD\研究方案\第一部分.pdf 第2.2节
# =============================================================================

class NodeType(Enum):
    """
    量子协议节点类型枚举 - 严格按照研究方案第一部分PDF 2.2节定义
    
    研究方案定义的10种标准节点类型：
    
    量子层节点：
    - QSP: 量子源 (Quantum Source) - 量子态的初始制备
    - QOP: 量子操作 (Quantum Operation) - 酉变换和量子噪声模拟
    - QC: 量子信道 (Quantum Channel) - 量子比特传输媒介
    - QI: 量子干涉 (Quantum Interaction) - 多量子态物理相互作用
    - QM: 量子测量 (Quantum Measurement) - 量子态到经典结果转换
    
    经典层节点：
    - CIS: 经典信息源 (Classical Information Source) - 随机数生成等
    - CLO: 经典逻辑操作 (Classical Logic Operation) - 逻辑和密码学操作
    - CC: 经典信道 (Classical Channel) - 经典信息传输
    - CD: 经典决策 (Classical Decision) - 协议控制流程
    
    输出层节点：
    - KE: 密钥提取 (Key Extraction) - 安全密钥最终输出
    """
    
    # 量子层节点（按研究方案）
    QSP = "QSP"    # 量子源 (Quantum Source)
    QOP = "QOP"    # 量子操作 (Quantum Operation) 
    QC = "QC"      # 量子信道 (Quantum Channel)
    QI = "QI"      # 量子干涉 (Quantum Interaction)
    QM = "QM"      # 量子测量 (Quantum Measurement)
    
    # 经典层节点（按研究方案）
    CIS = "CIS"    # 经典信息源 (Classical Information Source)
    CLO = "CLO"    # 经典逻辑操作 (Classical Logic Operation)
    CC = "CC"      # 经典信道 (Classical Channel)
    CD = "CD"      # 经典决策 (Classical Decision)
    
    # 输出层节点（按研究方案）
    KE = "KE"      # 密钥提取 (Key Extraction)

    @classmethod
    def get_quantum_types(cls) -> List['NodeType']:
        """
        获取所有量子层节点类型（按研究方案定义）
        
        返回值：
            List[NodeType]: 量子层节点类型列表
        """
        return [cls.QSP, cls.QOP, cls.QC, cls.QI, cls.QM]
    
    @classmethod 
    def get_classical_types(cls) -> List['NodeType']:
        """
        获取所有经典层节点类型（按研究方案定义）
        
        返回值：
            List[NodeType]: 经典层节点类型列表
        """
        return [cls.CIS, cls.CLO, cls.CC, cls.CD]
    
    @classmethod
    def get_output_types(cls) -> List['NodeType']:
        """
        获取输出层节点类型
        
        返回值：
            List[NodeType]: 输出层节点类型列表
        """
        return [cls.KE]
    
    @classmethod
    def is_quantum_type(cls, node_type: 'NodeType') -> bool:
        """
        判断是否为量子层节点类型
        
        参数：
            node_type: 待检查的节点类型
            
        返回值：
            bool: 是否为量子节点类型
        """
        return node_type in cls.get_quantum_types()
    
    @classmethod
    def is_classical_type(cls, node_type: 'NodeType') -> bool:
        """
        判断是否为经典层节点类型
        
        参数：
            node_type: 待检查的节点类型
            
        返回值：
            bool: 是否为经典节点类型
        """
        return node_type in cls.get_classical_types()
    
    @classmethod
    def is_output_type(cls, node_type: 'NodeType') -> bool:
        """
        判断是否为输出层节点类型
        
        参数：
            node_type: 待检查的节点类型
            
        返回值：
            bool: 是否为输出节点类型
        """
        return node_type in cls.get_output_types()
    
    def get_description(self) -> str:
        """
        获取节点类型的详细描述（基于研究方案定义）
        
        返回值：
            str: 节点类型的中文描述
        """
        descriptions = {
            self.QSP: "量子源 - 定义量子态的初始制备方式，是协议中量子信息产生的起点",
            self.QOP: "量子操作 - 对量子比特进行酉变换或模拟信道中的局部量子噪声",
            self.QC: "量子信道 - 模拟量子比特在不同物理介质中的传输，引入损耗和噪声", 
            self.QI: "量子干涉 - 模拟多个量子态之间的物理相互作用，用于贝尔态测量或干涉结构",
            self.QM: "量子测量 - 将量子态转化为经典测量结果，是量子层与经典层之间的接口",
            self.CIS: "经典信息源 - 协议中经典信息的起点，如随机数生成",
            self.CLO: "经典逻辑操作 - 对经典数据执行各种逻辑、算术或密码学操作",
            self.CC: "经典信道 - 模拟经典信息在公共信道中的传输",
            self.CD: "经典决策 - 基于经典信息控制协议的执行流程，引入分支和循环",
            self.KE: "密钥提取 - 协议的最终目标，表示安全密钥的最终产出点"
        }
        return descriptions.get(self, "未知节点类型")


class NodeSubType(Enum):
    """
    节点子类型枚举 - 实现研究方案的详细子类型系统
    
    基于研究方案PDF第2-5页的详细定义，每种节点类型都有特定的子类型
    """
    
    # QSP(量子源)子类型 - PDF第2页
    IDEAL_SINGLE_PHOTON = "IdealSinglePhoton"              # 完美单光子态理想光源
    WEAK_COHERENT_PULSE = "WeakCoherentPulse"             # 弱相干脉冲(实际QKD最常用)
    ENTANGLED_PAIR = "EntangledPair"                       # 纠缠态光子对源
    ARBITRARY_QSTATE = "ArbitraryQState"                   # 通用量子态制备
    
    # QOP(量子操作)子类型 - PDF第2-3页
    HADAMARD = "Hadamard"                                  # 哈达玛门
    PHASE_SHIFT = "PhaseShift"                            # 相位门
    CNOT = "CNOT"                                         # 控制非门
    SWAP = "SWAP"                                         # 交换门
    UNITARY_GATE = "UnitaryGate"                          # 通用酉门
    PHOTON_LOSS = "PhotonLoss"                            # 光子损耗模拟
    DEPHASING = "Dephasing"                               # 相位退相干
    DEPOLARIZATION = "Depolarization"                     # 去极化噪声
    
    # QC(量子信道)子类型 - PDF第3页
    FIBER = "Fiber"                                       # 光纤信道
    FREE_SPACE = "FreeSpace"                              # 自由空间信道
    
    # QI(量子干涉)子类型 - PDF第3-4页
    BEAM_SPLITTER = "BeamSplitter"                        # 分束器
    INTERFEROMETER = "Interferometer"                     # 通用干涉仪
    MZI = "MZI"                                          # 马赫-曾德尔干涉仪
    SAGNAC_LOOP = "SagnacLoop"                           # 萨格纳克干涉仪
    
    # QM(量子测量)子类型 - PDF第4页
    PROJECTIVE_MEASUREMENT = "ProjectiveMeasurement"      # 投影测量
    POVM_MEASUREMENT = "POVM_Measurement"                 # 广义测量(POVM)
    BELL_STATE_MEASUREMENT = "BellStateMeasurement"       # 贝尔态测量
    
    # CIS(经典信息源)子类型 - PDF第4-5页
    RANDOM_BIT_GENERATOR = "RandomBitGenerator"           # 随机比特生成器
    PREDEFINED_STRING = "PredefinedString"                # 预定义字符串
    HASH_FUNCTION = "HashFunction"                        # 哈希函数
    RANDOM_PERMUTATION_GENERATOR = "RandomPermutationGenerator"  # 随机置换生成器
    
    # CLO(经典逻辑操作)子类型 - PDF第5页
    XOR = "XOR"                                          # 异或门
    AND = "AND"                                          # 与门
    OR = "OR"                                            # 或门
    NOT = "NOT"                                          # 非门
    COMPARISON = "Comparison"                            # 比较操作
    CONCATENATE = "Concatenate"                          # 连接操作
    SPLIT = "Split"                                      # 分割操作
    BITWISE_OP = "BitwiseOp"                            # 按位操作
    HASHING = "Hashing"                                  # 哈希运算
    PARITY_CHECK = "ParityCheck"                         # 奇偶校验
    SYNDROME_CALCULATION = "SyndromeCalculation"          # 伴随式计算
    LOOKUP_TABLE = "LookupTable"                         # 查找表映射
    
    # CC(经典信道)子类型 - PDF第5页
    PUBLIC_CHANNEL = "PublicChannel"                      # 带认证的公共信道
    SECURE_CHANNEL = "SecureChannel"                      # 理想安全信道
    
    # CD(经典决策)子类型 - PDF第5-6页
    IF_ELSE = "IfElse"                                   # 条件分支
    LOOP = "Loop"                                        # 循环执行
    SWITCH = "Switch"                                    # 多路选择
    
    # KE(密钥提取)子类型 - 从上下文推断
    KEY_EXTRACTION = "KeyExtraction"                     # 标准密钥提取


class Party(Enum):
    """
    协议参与者枚举 - 保持与研究方案一致的参与者定义
    
    标准参与者：
    - ALICE: 发送方，通常负责量子态的准备和发送
    - BOB: 接收方，通常负责量子态的接收和测量
    - EVE: 窃听者，模拟攻击者的行为
    - CHARLIE: 第三方，如MDI-QKD中的测量方
    - UNKNOWN: 未知或不指定参与者
    """
    
    ALICE = "Alice"
    BOB = "Bob"
    EVE = "Eve"
    CHARLIE = "Charlie"
    UNKNOWN = "Unknown"
    
    @classmethod
    def _missing_(cls, value):
        """
        处理枚举缺失值的情况，支持大小写不敏感匹配和常见别名
        
        参数：
            value: 待匹配的值
            
        返回值：
            Party: 匹配的参与者枚举，未匹配时返回None
        """
        if isinstance(value, str):
            # 大小写不敏感匹配
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
            
            # 常见别名映射
            aliases = {
                "a": cls.ALICE,
                "b": cls.BOB,
                "e": cls.EVE,
                "c": cls.CHARLIE,
                "charlie": cls.CHARLIE,
                "third_party": cls.CHARLIE,
                "eavesdropper": cls.EVE
            }
            
            return aliases.get(value.lower())
        
        return None
    
    def get_description(self) -> str:
        """
        获取参与者的角色描述
        
        返回值：
            str: 参与者角色的中文描述
        """
        descriptions = {
            self.ALICE: "发送方 - 负责量子态的准备和发送",
            self.BOB: "接收方 - 负责量子态的接收和测量",
            self.EVE: "窃听者 - 模拟攻击者，尝试获取密钥信息",
            self.CHARLIE: "第三方 - 可信或不可信的中介方",
            self.UNKNOWN: "未指定 - 角色未明确定义的参与者"
        }
        return descriptions.get(self, "未知角色")


# ============================================================================
# 基于研究方案的参数模板系统
# 参数设计严格按照PDF第2-6页的详细定义
# ============================================================================

# 基于子类型的动态参数模板系统 - 严格按照研究方案PDF第2.2节设计
# 每种节点类型的不同子类型具有不同的参数集合

# QSP子类型参数模板 - 基于研究方案PDF第2页详细定义
QSP_SUBTYPE_TEMPLATES = {
    NodeSubType.IDEAL_SINGLE_PHOTON: {
        "polarization": "H",                 # 偏振方向 (H, V, D, A)
        "phase": 0.0,                       # 相位 (0.0 到 2*PI)
        "wavelength": 1550e-9,              # 光子波长 (米)
        "party": Party.ALICE
        # 注意：理想单光子不需要intensity参数
    },
    
    NodeSubType.WEAK_COHERENT_PULSE: {
        "intensity": 0.1,                   # 平均光子数μ (WCP特有)
        "polarization": "H",                # 偏振方向
        "phase": 0.0,                      # 相位
        "wavelength": 1550e-9,             # 光子波长
        "coherence_time": 1e-9,            # 相干时间 (WCP特有)
        "mode_matching_efficiency": 0.99,   # 模式匹配效率
        "party": Party.ALICE
    },
    
    NodeSubType.ENTANGLED_PAIR: {
        "entanglement_fidelity": 0.95,     # 纠缠保真度 (纠缠对特有)
        "pair_generation_rate": 1e6,       # 对产生率 (纠缠对特有)
        "wavelength": 1550e-9,             # 光子波长
        "party": Party.ALICE
        # 注意：纠缠对不需要polarization和intensity参数
    },
    
    NodeSubType.ARBITRARY_QSTATE: {
        "state_vector": "|+⟩",              # 态矢量 (任意态特有)
        "preparation_fidelity": 0.98,       # 制备保真度 (任意态特有)
        "wavelength": 1550e-9,             # 光子波长
        "party": Party.ALICE
        # 注意：任意量子态有自己独特的参数集
    }
}

# QOP子类型参数模板 - 基于研究方案PDF第2-3页定义
QOP_SUBTYPE_TEMPLATES = {
    # 酉门操作类
    NodeSubType.HADAMARD: {
        "target_qubit_id": 0,              # 目标量子比特ID
        "gate_fidelity": 0.99,             # 门保真度
        "gate_time": 1e-9                  # 门操作时间
    },
    
    NodeSubType.PHASE_SHIFT: {
        "target_qubit_id": 0,              # 目标量子比特ID
        "phase_angle": 0.0,                # 相位角度 (PhaseShift特有)
        "gate_fidelity": 0.99,             # 门保真度
        "gate_time": 1e-9                  # 门操作时间
    },
    
    NodeSubType.CNOT: {
        "control_qubit_id": 0,             # 控制比特ID (CNOT特有)
        "target_qubit_id": 1,              # 目标比特ID (CNOT特有)
        "gate_fidelity": 0.98,             # 两比特门保真度通常更低
        "gate_time": 2e-9                  # 两比特门时间更长
    },
    
    NodeSubType.UNITARY_GATE: {
        "unitary_matrix": "I",             # 酉矩阵 (通用酉门特有)
        "target_qubits": [0],              # 目标量子比特列表
        "gate_fidelity": 0.95,             # 通用门保真度
        "gate_time": 5e-9                  # 通用门时间更长
    },
    
    # 噪声模拟类
    NodeSubType.PHOTON_LOSS: {
        "loss_probability": 0.1,           # 损耗概率 (光子损耗特有)
        "affected_modes": [0],             # 受影响的模式
    },
    
    NodeSubType.DEPHASING: {
        "dephasing_rate": 0.01,            # 退相干率 (相位退相干特有)
        "coherence_time": 1e-6,            # 相干时间
        "affected_qubits": [0]             # 受影响的量子比特
    },
    
    NodeSubType.DEPOLARIZATION: {
        "depolarization_rate": 0.005,      # 去极化率 (去极化特有)
        "affected_qubits": [0]             # 受影响的量子比特
    }
}

# QC子类型参数模板 - 基于研究方案PDF第3页定义
QC_SUBTYPE_TEMPLATES = {
    NodeSubType.FIBER: {
        "length": 50.0,                    # 光纤长度(公里) (光纤特有)
        "loss_per_km": 0.2,               # 每公里损耗(dB/km) (光纤特有)
        "dispersion_parameter": 17e-6      # 色散参数 (光纤特有)
    },
    
    NodeSubType.FREE_SPACE: {
        "distance": 10.0,                  # 传输距离(公里) (自由空间特有)
        "atmospheric_transmission": 0.8,   # 大气透射率 (自由空间特有)
        "turbulence_parameter": 0.1        # 湍流参数 (自由空间特有)
    }
}

# 节点类型默认参数模板 - 使用默认子类型
NODE_TYPE_TEMPLATES = {
    # QSP(量子源) - 默认使用WCP子类型
    NodeType.QSP: {
        "subtype": NodeSubType.WEAK_COHERENT_PULSE,
        **QSP_SUBTYPE_TEMPLATES[NodeSubType.WEAK_COHERENT_PULSE]
    },
    
    # QOP(量子操作) - 默认使用Hadamard子类型
    NodeType.QOP: {
        "subtype": NodeSubType.HADAMARD,
        **QOP_SUBTYPE_TEMPLATES[NodeSubType.HADAMARD]
    },
    
    # QC(量子信道) - 默认使用光纤子类型
    NodeType.QC: {
        "subtype": NodeSubType.FIBER,
        **QC_SUBTYPE_TEMPLATES[NodeSubType.FIBER]
    },
    
    # QI(量子干涉) - PDF第3-4页参数定义
    NodeType.QI: {
        "subtype": NodeSubType.BEAM_SPLITTER,
        "input_qubits": [],                 # 进入干涉设备的量子比特ID列表
        "reflectivity": 0.5,                # 分束器反射率参数
        "path_length_difference": 0.0       # 路径长度差参数
    },
    
    # QM(量子测量) - PDF第4页参数定义
    NodeType.QM: {
        "subtype": NodeSubType.PROJECTIVE_MEASUREMENT,
        "target_qubit": 0,                  # 被测量的量子比特ID
        "basis_id": 0,                      # 测量基的ID，与QSP或QOP生成的基关联
        "detector_efficiency": 0.8,         # 探测器量子效率(0到1)
        "dark_count_rate": 1e-6,            # 暗计数率(每秒假阳性计数)
        "afterpulse_probability": 1e-3,     # 余脉冲概率
        "dead_time": 1e-6,                  # 探测器死时间
        "party": Party.BOB
    },
    
    # CIS(经典信息源) - PDF第4-5页参数定义
    NodeType.CIS: {
        "subtype": NodeSubType.RANDOM_BIT_GENERATOR,
        "seed": None,                       # 随机种子
        "length": 1000,                     # 生成长度
        "hash_algorithm": "SHA256",         # 哈希算法类型
        "party": Party.ALICE
    },
    
    # CLO(经典逻辑操作) - PDF第5页参数定义
    NodeType.CLO: {
        "subtype": NodeSubType.XOR,
        "input_data_ids": [],               # 输入经典数据流的ID列表
        "operation_params": {},             # 操作符、查找表内容等
        "error_correction_type": "LDPC",    # 纠错码类型 (LDPC, Turbo Code等)
        "party": Party.ALICE
    },
    
    # CC(经典信道) - PDF第5页参数定义
    NodeType.CC: {
        "subtype": NodeSubType.PUBLIC_CHANNEL,
        "error_rate": 1e-9,                 # 信道比特错误率
        "latency": 1e-6,                    # 传输延迟(秒)
        "bandwidth": 1e9                    # 信道带宽(比特/秒)
    },
    
    # CD(经典决策) - PDF第5-6页参数定义
    NodeType.CD: {
        "subtype": NodeSubType.IF_ELSE,
        "condition_input_id": None,         # 决策依据的经典数据ID
        "action_if_true_id": None,          # 指向DSL中其他节点的ID，控制执行流
        "action_if_false_id": None,         # 指向DSL中其他节点的ID，控制执行流
        "loop_count_id": None,              # 循环次数控制ID
        "condition_params": {},             # 具体条件表达式等
        "party": Party.ALICE
    },
    
    # KE(密钥提取) - PDF第6页参数定义
    NodeType.KE: {
        "subtype": NodeSubType.KEY_EXTRACTION,
        "input_key_id": None,               # 最终经过保密放大后的密钥流ID
        "key_length": 256,                  # 目标密钥长度
        "party": Party.BOB
    }
}

# QI子类型参数模板
QI_SUBTYPE_TEMPLATES = {
    NodeSubType.BEAM_SPLITTER: {
        "reflectivity": 0.5,               # 分束器反射率
        "transmission_efficiency": 0.95    # 传输效率
    },
    
    NodeSubType.INTERFEROMETER: {
        "visibility": 0.99,                # 干涉可见度
        "phase_stability": 0.01,           # 相位稳定性
        "path_length_difference": 0.0      # 路径长度差
    },
    
    NodeSubType.MZI: {
        "arm_length_difference": 0.0,      # 臂长差
        "phase_modulation_depth": 1.0      # 相位调制深度
    }
}

# QM子类型参数模板
QM_SUBTYPE_TEMPLATES = {
    NodeSubType.PROJECTIVE_MEASUREMENT: {
        "measurement_basis": "Z",          # 测量基
        "detector_efficiency": 0.8,        # 探测器效率
        "dark_count_rate": 1e-6,          # 暗计数率
        "party": Party.BOB
    },
    
    NodeSubType.POVM_MEASUREMENT: {
        "povm_elements": ["I", "X", "Y", "Z"], # POVM元素
        "measurement_efficiency": 0.85,     # 测量效率
        "party": Party.BOB
    },
    
    NodeSubType.BELL_STATE_MEASUREMENT: {
        "bell_measurement_efficiency": 0.5, # Bell态测量效率
        "basis_choice_strategy": "random",  # 基选择策略
        "party": Party.CHARLIE
    }
}

# CIS子类型参数模板  
CIS_SUBTYPE_TEMPLATES = {
    NodeSubType.RANDOM_BIT_GENERATOR: {
        "entropy_rate": 1.0,               # 熵率
        "seed_value": None,                # 种子值
        "party": Party.ALICE
    },
    
    NodeSubType.PREDEFINED_STRING: {
        "bit_string": "101010",            # 比特串
        "encoding_type": "binary",         # 编码类型
        "party": Party.ALICE
    },
    
    NodeSubType.HASH_FUNCTION: {
        "hash_algorithm": "SHA256",        # 哈希算法
        "input_length": 256,               # 输入长度
        "output_length": 256,              # 输出长度
        "party": Party.ALICE
    }
}

# 更新其他节点类型模板，添加子类型支持
NODE_TYPE_TEMPLATES.update({
    # QI(量子干涉) - 默认使用分束器
    NodeType.QI: {
        "subtype": NodeSubType.BEAM_SPLITTER,
        "input_qubits": [],
        **QI_SUBTYPE_TEMPLATES[NodeSubType.BEAM_SPLITTER]
    },
    
    # QM(量子测量) - 默认使用投影测量
    NodeType.QM: {
        "subtype": NodeSubType.PROJECTIVE_MEASUREMENT,
        "target_qubit": 0,
        "basis_id": 0,
        **QM_SUBTYPE_TEMPLATES[NodeSubType.PROJECTIVE_MEASUREMENT]
    },
    
    # CIS(经典信息源) - 默认使用随机比特生成器
    NodeType.CIS: {
        "subtype": NodeSubType.RANDOM_BIT_GENERATOR,
        "length": 1000,
        **CIS_SUBTYPE_TEMPLATES[NodeSubType.RANDOM_BIT_GENERATOR]
    }
})


def get_node_template(node_type: NodeType, subtype: Optional['NodeSubType'] = None) -> Dict[str, Any]:
    """
    获取指定节点类型和子类型的参数模板 - 基于研究方案的精确子类型定义
    
    重构改进：
    - 支持基于子类型的动态参数模板
    - 不同子类型具有不同的参数集合
    - 严格按照研究方案PDF第2.2节的子类型定义
    
    参数：
        node_type: 节点类型
        subtype: 可选的子类型，如果未指定则使用默认子类型
        
    返回值：
        Dict[str, Any]: 包含默认参数的字典
        
    异常：
        ValueError: 不支持的节点类型或子类型
    """
    import copy
    
    if node_type not in NODE_TYPE_TEMPLATES:
        raise ValueError(f"不支持的节点类型: {node_type}")
    
    # 如果没有指定子类型，使用默认模板
    if subtype is None:
        template = copy.deepcopy(NODE_TYPE_TEMPLATES[node_type])
    else:
        # 根据节点类型和子类型获取特定模板
        template = _get_subtype_template(node_type, subtype)
    
    # 检查是否为理想化模式
    if _is_idealized_mode():
        template = _apply_idealized_modifications(template, node_type, subtype)
    
    return template


def _get_subtype_template(node_type: NodeType, subtype: 'NodeSubType') -> Dict[str, Any]:
    """
    根据节点类型和子类型获取特定的参数模板
    
    参数：
        node_type: 节点类型
        subtype: 子类型
        
    返回值：
        Dict[str, Any]: 子类型特定的参数模板
        
    异常：
        ValueError: 不支持的节点类型和子类型组合
    """
    import copy
    
    # 基础参数（所有子类型共有）
    base_template = {"subtype": subtype}
    
    # 根据节点类型选择对应的子类型模板
    if node_type == NodeType.QSP:
        if subtype in QSP_SUBTYPE_TEMPLATES:
            subtype_params = QSP_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"QSP节点不支持子类型: {subtype}")
            
    elif node_type == NodeType.QOP:
        if subtype in QOP_SUBTYPE_TEMPLATES:
            subtype_params = QOP_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"QOP节点不支持子类型: {subtype}")
            
    elif node_type == NodeType.QC:
        if subtype in QC_SUBTYPE_TEMPLATES:
            subtype_params = QC_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"QC节点不支持子类型: {subtype}")
            
    elif node_type == NodeType.QI:
        if subtype in QI_SUBTYPE_TEMPLATES:
            subtype_params = QI_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"QI节点不支持子类型: {subtype}")
            
    elif node_type == NodeType.QM:
        if subtype in QM_SUBTYPE_TEMPLATES:
            subtype_params = QM_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"QM节点不支持子类型: {subtype}")
            
    elif node_type == NodeType.CIS:
        if subtype in CIS_SUBTYPE_TEMPLATES:
            subtype_params = CIS_SUBTYPE_TEMPLATES[subtype]
        else:
            raise ValueError(f"CIS节点不支持子类型: {subtype}")
            
    else:
        # 对于没有特殊子类型的节点，使用默认模板
        return copy.deepcopy(NODE_TYPE_TEMPLATES[node_type])
    
    # 合并基础参数和子类型特定参数
    template = {**base_template, **subtype_params}
    return copy.deepcopy(template)


def get_supported_subtypes(node_type: NodeType) -> List['NodeSubType']:
    """
    获取指定节点类型支持的所有子类型
    
    参数：
        node_type: 节点类型
        
    返回值：
        List[NodeSubType]: 支持的子类型列表
    """
    subtype_mapping = {
        NodeType.QSP: list(QSP_SUBTYPE_TEMPLATES.keys()),
        NodeType.QOP: list(QOP_SUBTYPE_TEMPLATES.keys()),
        NodeType.QC: list(QC_SUBTYPE_TEMPLATES.keys()),
        NodeType.QI: list(QI_SUBTYPE_TEMPLATES.keys()),
        NodeType.QM: list(QM_SUBTYPE_TEMPLATES.keys()),
        NodeType.CIS: list(CIS_SUBTYPE_TEMPLATES.keys()),
        # 其他节点类型暂时使用单一子类型
        NodeType.CLO: [NodeSubType.XOR],
        NodeType.CC: [NodeSubType.PUBLIC_CHANNEL],
        NodeType.CD: [NodeSubType.IF_ELSE],
        NodeType.KE: [NodeSubType.KEY_EXTRACTION]
    }
    
    return subtype_mapping.get(node_type, [])


def validate_node_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证节点参数的有效性
    
    参数：
        node_type: 节点类型
        params: 参数字典
        
    返回值：
        bool: 参数是否有效
    """
    # 检查节点类型是否支持
    if node_type not in NODE_TYPE_TEMPLATES:
        return False
    
    # 获取必需参数列表
    required_params = _get_required_params(node_type)
    
    # 检查必需参数是否存在
    for param in required_params:
        if param not in params:
            return False
    
    # 根据模式选择验证策略
    if _is_idealized_mode():
        return _validate_idealized_params(node_type, params)
    else:
        return _validate_realistic_params(node_type, params)


def _get_required_params(node_type: NodeType) -> List[str]:
    """
    获取节点类型的必需参数列表 - 基于研究方案定义
    
    参数：
        node_type: 节点类型
        
    返回值：
        List[str]: 必需参数名称列表
    """
    required_params = {
        NodeType.QSP: ["subtype", "party"],
        NodeType.QOP: ["subtype", "target_qubits"],
        NodeType.QC: ["subtype"],
        NodeType.QI: ["subtype", "input_qubits"],
        NodeType.QM: ["subtype", "target_qubit", "party"],
        NodeType.CIS: ["subtype", "party"],
        NodeType.CLO: ["subtype", "input_data_ids", "party"],
        NodeType.CC: ["subtype"],
        NodeType.CD: ["subtype", "condition_input_id", "party"],
        NodeType.KE: ["subtype", "input_key_id", "party"]
    }
    
    return required_params.get(node_type, [])


def _validate_realistic_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证现实模式下的参数范围 - 基于物理约束
    
    参数：
        node_type: 节点类型
        params: 参数字典
        
    返回值：
        bool: 参数是否在有效范围内
    """
    # QSP节点的参数验证
    if node_type == NodeType.QSP:
        if "intensity" in params and not (0 <= params["intensity"] <= 1):
            return False
        if "phase" in params and not (0 <= params["phase"] <= 2*3.14159):
            return False
    
    # QOP节点的参数验证
    elif node_type == NodeType.QOP:
        if "fidelity" in params and not (0 <= params["fidelity"] <= 1):
            return False
        if "gate_time" in params and params["gate_time"] < 0:
            return False
    
    # QC节点的参数验证
    elif node_type == NodeType.QC:
        if "length" in params and params["length"] < 0:
            return False
        if "loss_per_unit" in params and params["loss_per_unit"] < 0:
            return False
        if "depolarization_rate" in params and not (0 <= params["depolarization_rate"] <= 1):
            return False
    
    # QM节点的参数验证
    elif node_type == NodeType.QM:
        if "detector_efficiency" in params and not (0 <= params["detector_efficiency"] <= 1):
            return False
        if "dark_count_rate" in params and params["dark_count_rate"] < 0:
            return False
    
    # CC节点的参数验证
    elif node_type == NodeType.CC:
        if "bandwidth" in params and params["bandwidth"] <= 0:
            return False
        if "error_rate" in params and not (0 <= params["error_rate"] <= 1):
            return False
    
    return True


# ============================================================================
# 理想化模式支持 - 保持与原有系统兼容
# ============================================================================

# 全局理想化模式标志
_IDEALIZED_MODE = os.getenv('AI4QKD_IDEALIZED_MODE', 'False').lower() == 'true'


def set_idealized_mode(enabled: bool = True):
    """
    设置理想化模式
    
    参数：
        enabled: 是否启用理想化模式
    """
    global _IDEALIZED_MODE
    _IDEALIZED_MODE = enabled
    
    mode_name = "Idealized Research Mode" if enabled else "Realistic Deployment Mode"
    print(f"[MODE] AI4QKD switched to {mode_name}")
    
    if enabled:
        print("   [INFO] Idealized parameters enabled (100% efficiency, no noise, instant operations)")
        print("   [INFO] Focus on protocol design algorithm principle verification")
    else:
        print("   [INFO] Realistic parameters enabled (considering hardware limitations and environmental noise)")
        print("   [INFO] Oriented towards actual QKD system deployment optimization")


def is_idealized_mode() -> bool:
    """
    检查当前是否为理想化模式
    
    返回值：
        bool: 是否为理想化模式
    """
    return _IDEALIZED_MODE


def _is_idealized_mode() -> bool:
    """内部使用的模式检查函数"""
    return _IDEALIZED_MODE


def setup_idealized_research_mode():
    """
    设置为科学研究的理想化模式
    """
    set_idealized_mode(True)
    print("[SETUP] Idealized research environment configured")
    print("   [INFO] Eliminate hardware noise, highlight protocol structure innovation")
    print("   [INFO] Obtain theoretical optimal performance baseline")


def setup_realistic_deployment_mode():
    """
    设置为现实部署模式
    """
    set_idealized_mode(False)
    print("[SETUP] Realistic deployment environment configured")
    print("   [INFO] Consider actual hardware characteristics and environmental limitations")
    print("   [INFO] Optimize actual QKD system performance")


def _apply_idealized_modifications(template: Dict[str, Any], node_type: NodeType, subtype: Optional['NodeSubType'] = None) -> Dict[str, Any]:
    """
    对参数模板应用理想化修改 - 支持子类型特定的理想化
    
    参数：
        template: 原始参数模板
        node_type: 节点类型
        subtype: 子类型（可选）
        
    返回值：
        Dict[str, Any]: 应用理想化修改后的模板
    """
    import copy
    idealized_template = copy.deepcopy(template)
    
    # QSP节点的理想化修改
    if node_type == NodeType.QSP:
        if "mode_matching_efficiency" in idealized_template:
            idealized_template["mode_matching_efficiency"] = 1.0  # 理想模式匹配
        if "coherence_time" in idealized_template:
            idealized_template["coherence_time"] = float('inf')   # 无限相干时间
            
    # QOP节点的理想化修改
    elif node_type == NodeType.QOP:
        if "gate_fidelity" in idealized_template:
            idealized_template["gate_fidelity"] = 1.0            # 理想保真度
        if "fidelity" in idealized_template:
            idealized_template["fidelity"] = 1.0                # 理想保真度
        if "gate_time" in idealized_template:
            idealized_template["gate_time"] = 0.0               # 瞬时操作
        # 噪声模拟类的理想化
        if "loss_probability" in idealized_template:
            idealized_template["loss_probability"] = 0.0        # 无损耗
        if "dephasing_rate" in idealized_template:
            idealized_template["dephasing_rate"] = 0.0          # 无退相干
        if "depolarization_rate" in idealized_template:
            idealized_template["depolarization_rate"] = 0.0     # 无去极化
            
    # QC节点的理想化修改
    elif node_type == NodeType.QC:
        if "loss_per_km" in idealized_template:
            idealized_template["loss_per_km"] = 0.0             # 无损耗
        if "loss_per_unit" in idealized_template:
            idealized_template["loss_per_unit"] = 0.0           # 无损耗
        if "atmospheric_transmission" in idealized_template:
            idealized_template["atmospheric_transmission"] = 1.0 # 完美透射
        if "turbulence_parameter" in idealized_template:
            idealized_template["turbulence_parameter"] = 0.0    # 无湍流
            
    # QI节点的理想化修改
    elif node_type == NodeType.QI:
        if "transmission_efficiency" in idealized_template:
            idealized_template["transmission_efficiency"] = 1.0  # 完美传输
        if "visibility" in idealized_template:
            idealized_template["visibility"] = 1.0              # 完美可见度
        if "phase_stability" in idealized_template:
            idealized_template["phase_stability"] = 0.0         # 完美稳定
            
    # QM节点的理想化修改
    elif node_type == NodeType.QM:
        if "detector_efficiency" in idealized_template:
            idealized_template["detector_efficiency"] = 1.0     # 100%检测效率
        if "measurement_efficiency" in idealized_template:
            idealized_template["measurement_efficiency"] = 1.0   # 100%测量效率
        if "bell_measurement_efficiency" in idealized_template:
            idealized_template["bell_measurement_efficiency"] = 1.0 # 100% Bell态测量效率
        if "dark_count_rate" in idealized_template:
            idealized_template["dark_count_rate"] = 0.0         # 无暗计数
        if "afterpulse_probability" in idealized_template:
            idealized_template["afterpulse_probability"] = 0.0  # 无余脉冲
        if "dead_time" in idealized_template:
            idealized_template["dead_time"] = 0.0               # 无死时间
            
    # CC节点的理想化修改
    elif node_type == NodeType.CC:
        if "bandwidth" in idealized_template:
            idealized_template["bandwidth"] = float('inf')      # 无限带宽
        if "latency" in idealized_template:
            idealized_template["latency"] = 0.0                 # 无延迟
        if "error_rate" in idealized_template:
            idealized_template["error_rate"] = 0.0              # 无错误
    
    return idealized_template


def _validate_idealized_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证理想化模式下的参数
    
    参数：
        node_type: 节点类型
        params: 参数字典
        
    返回值：
        bool: 参数是否有效（理想化标准）
    """
    # 理想化模式下允许更宽松的参数范围
    if node_type == NodeType.QC:
        if "loss_per_unit" in params and params["loss_per_unit"] < 0:
            return False
    elif node_type == NodeType.QM:
        if "detector_efficiency" in params and not (0 <= params["detector_efficiency"] <= 1):
            return False
    
    # 其他验证保持相对宽松
    return True


def compare_mode_parameters(node_type: NodeType) -> Dict[str, Any]:
    """
    比较理想化模式和现实模式下的参数差异
    
    参数：
        node_type: 节点类型
        
    返回值：
        Dict[str, Any]: 参数比较结果
    """
    # 保存当前模式
    current_mode = _is_idealized_mode()
    
    try:
        # 获取现实模式参数
        set_idealized_mode(False)
        realistic_params = get_node_template(node_type)
        
        # 获取理想化模式参数
        set_idealized_mode(True)
        idealized_params = get_node_template(node_type)
        
        # 分析差异
        differences = []
        all_keys = set(realistic_params.keys()) | set(idealized_params.keys())
        
        for key in all_keys:
            real_val = realistic_params.get(key, "未设置")
            ideal_val = idealized_params.get(key, "未设置")
            
            if real_val != ideal_val:
                differences.append({
                    "parameter": key,
                    "realistic": real_val,
                    "idealized": ideal_val,
                    "improvement": _calculate_improvement(real_val, ideal_val)
                })
        
        return {
            "node_type": node_type.value,
            "realistic_params": realistic_params,
            "idealized_params": idealized_params,
            "differences": differences
        }
    
    finally:
        # 恢复原始模式
        set_idealized_mode(current_mode)


def _calculate_improvement(real_val, ideal_val) -> str:
    """
    计算参数改进描述
    
    参数：
        real_val: 现实值
        ideal_val: 理想值
        
    返回值：
        str: 改进描述
    """
    if isinstance(real_val, (int, float)) and isinstance(ideal_val, (int, float)):
        if ideal_val > real_val:
            return f"提升{ideal_val/real_val:.2f}倍"
        elif ideal_val < real_val:
            return f"减少{real_val/ideal_val:.2f}倍"
        else:
            return "无变化"
    else:
        return f"{real_val} → {ideal_val}"


def print_current_mode_info():
    """
    打印当前模式的详细信息
    """
    if _is_idealized_mode():
        print("[MODE] Current mode: Idealized Scientific Research Mode")
        print("   [FEATURES] Mode characteristics:")
        print("      • Detection efficiency: 100% (no detector loss)")
        print("      • Channel loss: 0% (perfect transmission)")
        print("      • Quantum noise: 0% (ideal environment)")
        print("      • Operation time: Instantaneous (no delay)")
        print("   [USAGE] Applicable scenarios: Protocol algorithm principle verification, theoretical performance baseline")
    else:
        print("[MODE] Current mode: Realistic Deployment Mode")
        print("   [FEATURES] Mode characteristics:")
        print("      • Detection efficiency: ~80% (considering detector limitations)")
        print("      • Channel loss: Based on distance and medium")
        print("      • Quantum noise: Environmental impact included")
        print("      • Operation time: Physical hardware limitations")
        print("   [USAGE] Applicable scenarios: Actual QKD system deployment, engineering optimization")