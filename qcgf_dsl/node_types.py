"""
QCGF DSL节点类型定义

定义量子密钥分发协议中的各种节点类型和参与者。
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class NodeType(Enum):
    """量子协议节点类型枚举"""
    
    # 量子操作节点
    QSP = "quantum_state_preparation"      # 量子态制备
    QC = "quantum_channel"                 # 量子信道
    QM = "quantum_measurement"             # 量子测量
    QG = "quantum_gate"                    # 量子门操作
    QD = "quantum_detector"                # 量子探测器
    
    # 经典操作节点  
    CC = "classical_channel"               # 经典信道
    CP = "classical_processing"            # 经典处理
    CV = "classical_verification"          # 经典验证
    CK = "classical_key_extraction"        # 经典密钥提取
    
    # 混合操作节点
    Q2C = "quantum_to_classical"           # 量子到经典转换
    C2Q = "classical_to_quantum"           # 经典到量子转换
    
    # 特殊节点
    SOURCE = "source"                      # 源节点
    SINK = "sink"                          # 汇节点
    NOISE = "noise"                        # 噪声节点


class EdgeType(Enum):
    """边类型枚举"""
    
    QUANTUM = "quantum"                    # 量子边
    CLASSICAL = "classical"                # 经典边
    CONTROL = "control"                    # 控制边
    FEEDBACK = "feedback"                  # 反馈边
    DATA = "data"                          # 数据边


class Party(Enum):
    """协议参与者枚举"""
    
    ALICE = "alice"        # 发送方
    BOB = "bob"            # 接收方
    EVE = "eve"            # 窃听者
    CHARLIE = "charlie"    # 第三方（如MDI-QKD）
    TRUSTED = "trusted"    # 可信第三方
    PUBLIC = "public"      # 公共参与者
    BOTH = "both"          # 双方（Alice和Bob）


@dataclass
class NodeTemplate:
    """节点模板类，定义节点的标准参数和验证规则"""
    
    node_type: NodeType
    required_params: Dict[str, type]
    optional_params: Dict[str, Any]
    default_party: Optional[Party] = None
    description: str = ""
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数是否符合模板要求"""
        # 检查必需参数
        for param_name, param_type in self.required_params.items():
            if param_name not in params:
                return False
            if not isinstance(params[param_name], param_type):
                return False
        
        # 检查可选参数类型
        for param_name, param_value in params.items():
            if param_name in self.required_params:
                continue
            if param_name in self.optional_params:
                expected_type = type(self.optional_params[param_name])
                if not isinstance(param_value, expected_type):
                    return False
        
        return True


# 预定义的节点模板
NODE_TEMPLATES = {
    NodeType.QSP: NodeTemplate(
        node_type=NodeType.QSP,
        required_params={'state': str, 'basis': str},
        optional_params={'intensity': float, 'phase': float, 'timing': float},
        default_party=Party.ALICE,
        description="量子态制备节点"
    ),
    
    NodeType.QC: NodeTemplate(
        node_type=NodeType.QC,
        required_params={'loss': float},
        optional_params={'noise': float, 'distance': float, 'type': str},
        default_party=None,
        description="量子信道节点"
    ),
    
    NodeType.QM: NodeTemplate(
        node_type=NodeType.QM,
        required_params={'basis': str},
        optional_params={'efficiency': float, 'dark_count': float, 'timing': float},
        default_party=Party.BOB,
        description="量子测量节点"
    ),
    
    NodeType.CC: NodeTemplate(
        node_type=NodeType.CC,
        required_params={'capacity': float},
        optional_params={'delay': float, 'reliability': float, 'security': str},
        default_party=None,
        description="经典信道节点"
    ),
    
    NodeType.CP: NodeTemplate(
        node_type=NodeType.CP,
        required_params={'operation': str},
        optional_params={'complexity': int, 'memory': int, 'time': float},
        default_party=None,
        description="经典处理节点"
    )
}


def get_node_template(node_type: NodeType) -> NodeTemplate:
    """获取指定节点类型的模板"""
    if node_type not in NODE_TEMPLATES:
        raise ValueError(f"未找到节点类型 {node_type} 的模板")
    return NODE_TEMPLATES[node_type]


def validate_node_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """验证节点参数"""
    template = get_node_template(node_type)
    return template.validate_params(params)


def create_default_params(node_type: NodeType) -> Dict[str, Any]:
    """创建节点的默认参数"""
    template = get_node_template(node_type)
    params = {}
    
    # 添加必需参数的默认值
    if node_type == NodeType.QSP:
        params.update({'state': '|0⟩', 'basis': 'Z'})
    elif node_type == NodeType.QC:
        params.update({'loss': 0.1})
    elif node_type == NodeType.QM:
        params.update({'basis': 'Z'})
    elif node_type == NodeType.CC:
        params.update({'capacity': 1.0})
    elif node_type == NodeType.CP:
        params.update({'operation': 'xor'})
    
    # 添加可选参数的默认值
    params.update(template.optional_params)
    
    return params