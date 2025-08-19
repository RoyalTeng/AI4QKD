"""
AI4QKD - 边类型定义模块 (严格按照研究方案)

设计依据：
- 严格遵循f:\AI4QKD\研究方案\第一部分.pdf中2.3节的定义
- 实现研究方案要求的4种标准边类型
- 移除不在研究方案中的多余边类型
- 简化参数模板专注于信息流抽象

核心边类型（按研究方案2.3节）：
- QF: 量子流 (Quantum Flow) - 量子比特从量子操作节点流向量子操作节点
- CF: 经典流 (Classical Flow) - 经典信息在经典操作节点间传递
- ControlF: 控制流 (Control Flow) - 操作执行顺序或条件依赖
- QCIF: 量子-经典接口流 (Quantum-Classical Interface Flow) - 量子测量结果转为经典比特

重要变更：
- 移除了不在研究方案中的边类型（DATA、FEEDBACK、SYNCHRONIZATION）
- 修正了边类型命名以精确匹配研究方案
- 移除了大量物理传输参数，专注信息流抽象
- 实现了研究方案要求的严格连接约束

作者: Claude (AI Assistant) 
重构日期: 2025-08-19
依据文档: f:\AI4QKD\研究方案\第一部分.pdf 第2.3节
"""

from enum import Enum
from typing import Dict, Any, Optional, List, Union


# =============================================================================
# 研究方案标准边类型定义  
# 依据: f:\AI4QKD\研究方案\第一部分.pdf 第2.3节
# =============================================================================

class EdgeType(Enum):
    """
    协议图边类型枚举 - 严格按照研究方案第一部分PDF 2.3节定义
    
    研究方案定义的4种标准边类型：
    
    - QF (Quantum Flow): 量子流
      目的: 表示量子比特从一个量子操作节点流向另一个量子操作节点
      约束: 只能连接量子操作节点（QSP, QOP, QC, QI, QM 的量子输入/输出）
      
    - CF (Classical Flow): 经典流  
      目的: 表示经典信息（如测量结果、协商信息、原始密钥、纠错后的密钥等）在经典操作节点间的传递
      约束: 适用于CIS, CLO, CC, CD, KE 的输入/输出，以及 QM 的经典测量结果输出
      
    - ControlF (Control Flow): 控制流
      目的: 表示操作的执行顺序或条件依赖。通常由CD节点发出，控制其他节点的执行
      约束: 连接 CD 节点的输出到任何其他操作节点的输入，指示该操作何时、在何种条件下被触发
      
    - QCIF (Quantum-Classical Interface Flow): 量子-经典接口流
      目的: 特殊的混合流，表示量子测量结果转化为经典比特后，传递给经典逻辑操作或决策节点
      约束: 只能从 QM 节点的经典输出连接到 CLO 或 CD 节点的输入
    """
    
    # 研究方案标准边类型（严格按照PDF 2.3节）
    QF = "QF"           # 量子流 (Quantum Flow)
    CF = "CF"           # 经典流 (Classical Flow) 
    CONTROL_F = "ControlF"  # 控制流 (Control Flow)
    QCIF = "QCIF"       # 量子-经典接口流 (Quantum-Classical Interface Flow)
    
    @classmethod
    def _missing_(cls, value):
        """
        处理枚举缺失值的情况，支持大小写不敏感匹配和常见别名
        
        参数：
            value: 待匹配的值
            
        返回值：
            EdgeType: 匹配的边类型枚举，未匹配时返回None
        """
        if isinstance(value, str):
            # 大小写不敏感匹配
            for member in cls:
                if member.name.upper() == value.upper() or member.value.upper() == value.upper():
                    return member
            
            # 常见别名映射
            aliases = {
                "quantum": cls.QF,
                "classical": cls.CF,
                "control": cls.CONTROL_F,
                "quantum_flow": cls.QF,
                "classical_flow": cls.CF,
                "control_flow": cls.CONTROL_F,
                "qci": cls.QCIF,
                "interface": cls.QCIF
            }
            
            return aliases.get(value.lower())
        
        return None
    
    @classmethod
    def get_quantum_flow_types(cls) -> List['EdgeType']:
        """
        获取量子信息流类型（按研究方案定义）
        
        返回值：
            List[EdgeType]: 量子信息流类型列表
        """
        return [cls.QF, cls.QCIF]  # QCIF包含量子信息转换
    
    @classmethod
    def get_classical_flow_types(cls) -> List['EdgeType']:
        """
        获取经典信息流类型（按研究方案定义）
        
        返回值：
            List[EdgeType]: 经典信息流类型列表
        """
        return [cls.CF, cls.QCIF]  # QCIF输出经典信息
    
    @classmethod
    def get_control_flow_types(cls) -> List['EdgeType']:
        """
        获取控制流类型（按研究方案定义）
        
        返回值：
            List[EdgeType]: 控制流类型列表
        """
        return [cls.CONTROL_F]
    
    @classmethod
    def is_quantum_flow(cls, edge_type: 'EdgeType') -> bool:
        """
        判断是否为量子信息流类型
        
        参数：
            edge_type: 待检查的边类型
            
        返回值：
            bool: 是否为量子信息流
        """
        return edge_type in cls.get_quantum_flow_types()
    
    @classmethod
    def is_classical_flow(cls, edge_type: 'EdgeType') -> bool:
        """
        判断是否为经典信息流类型
        
        参数：
            edge_type: 待检查的边类型
            
        返回值：
            bool: 是否为经典信息流
        """
        return edge_type in cls.get_classical_flow_types()
    
    @classmethod
    def is_control_flow(cls, edge_type: 'EdgeType') -> bool:
        """
        判断是否为控制流类型
        
        参数：
            edge_type: 待检查的边类型
            
        返回值：
            bool: 是否为控制流
        """
        return edge_type in cls.get_control_flow_types()
    
    def get_description(self) -> str:
        """
        获取边类型的详细描述（基于研究方案定义）
        
        返回值：
            str: 边类型的中文描述
        """
        descriptions = {
            self.QF: "量子流 - 表示量子比特从一个量子操作节点流向另一个量子操作节点",
            self.CF: "经典流 - 表示经典信息在经典操作节点间的传递",
            self.CONTROL_F: "控制流 - 表示操作的执行顺序或条件依赖",
            self.QCIF: "量子-经典接口流 - 量子测量结果转化为经典比特后的特殊接口"
        }
        return descriptions.get(self, "未知边类型")


class EdgeDirection(Enum):
    """
    边方向枚举 - 简化版本专注于信息流方向
    
    方向类型：
    - FORWARD: 前向传输（默认方向）
    - BACKWARD: 后向传输（反馈方向）
    - BIDIRECTIONAL: 双向传输（双向信道）
    """
    
    FORWARD = "forward"          # 前向
    BACKWARD = "backward"        # 后向
    BIDIRECTIONAL = "bidirectional"  # 双向
    
    def get_description(self) -> str:
        """
        获取方向的中文描述
        
        返回值：
            str: 方向的中文描述
        """
        descriptions = {
            self.FORWARD: "前向 - 从源节点到目标节点",
            self.BACKWARD: "后向 - 从目标节点到源节点",
            self.BIDIRECTIONAL: "双向 - 支持双向数据传输"
        }
        return descriptions.get(self, "未知方向")


# =============================================================================
# 基于研究方案的边类型连接约束
# 实现研究方案2.3节要求的严格连接约束规则
# =============================================================================

# 边类型连接约束（基于研究方案精确定义）
EDGE_CONNECTION_CONSTRAINTS = {
    EdgeType.QF: {
        "allowed_source_nodes": ["QSP", "QOP", "QC", "QI"],
        "allowed_target_nodes": ["QOP", "QC", "QI", "QM"],
        "description": "量子态从量子操作节点到量子操作节点",
        "flow_type": "quantum_state"
    },
    
    EdgeType.CF: {
        "allowed_source_nodes": ["CIS", "CLO", "CC", "CD", "QM"],
        "allowed_target_nodes": ["CLO", "CC", "CD", "KE"],
        "description": "经典信息在经典操作节点间传递",
        "flow_type": "classical_bits"
    },
    
    EdgeType.CONTROL_F: {
        "allowed_source_nodes": ["CD"],  # 只能从决策节点发出
        "allowed_target_nodes": ["QSP", "QOP", "QC", "QI", "QM", "CIS", "CLO", "CC", "CD", "KE"],  # 可以控制任何节点
        "description": "控制执行顺序和条件依赖",
        "flow_type": "control_signal"
    },
    
    EdgeType.QCIF: {
        "allowed_source_nodes": ["QM"],  # 只能从量子测量节点发出
        "allowed_target_nodes": ["CLO", "CD"],  # 连接到经典处理节点
        "description": "量子测量结果转为经典信息的特殊接口",
        "flow_type": "measurement_result"
    }
}


def validate_edge_connection(edge_type: EdgeType, source_node_type: str, target_node_type: str) -> bool:
    """
    验证边连接是否符合研究方案的约束规则
    
    参数：
        edge_type: 边类型
        source_node_type: 源节点类型字符串
        target_node_type: 目标节点类型字符串
        
    返回值：
        bool: 连接是否有效
    """
    if edge_type not in EDGE_CONNECTION_CONSTRAINTS:
        return False
    
    constraints = EDGE_CONNECTION_CONSTRAINTS[edge_type]
    
    # 检查源节点类型是否允许
    if source_node_type not in constraints["allowed_source_nodes"]:
        return False
    
    # 检查目标节点类型是否允许
    if target_node_type not in constraints["allowed_target_nodes"]:
        return False
    
    return True


def get_allowed_edges_for_connection(source_node_type: str, target_node_type: str) -> List[EdgeType]:
    """
    获取两个节点类型之间允许的边类型列表
    
    参数：
        source_node_type: 源节点类型字符串
        target_node_type: 目标节点类型字符串
        
    返回值：
        List[EdgeType]: 允许的边类型列表
    """
    allowed_edges = []
    
    for edge_type, constraints in EDGE_CONNECTION_CONSTRAINTS.items():
        if (source_node_type in constraints["allowed_source_nodes"] and
            target_node_type in constraints["allowed_target_nodes"]):
            allowed_edges.append(edge_type)
    
    return allowed_edges


# ============================================================================
# 简化的边参数模板系统 - 专注信息流抽象
# 移除物理传输参数，只保留信息流的抽象特性
# ============================================================================

# 边类型参数模板 - 严格按照研究方案简化设计
EDGE_TYPE_TEMPLATES = {
    EdgeType.QF: {
        "flow_type": "quantum_state",    # 流动的信息类型
        "direction": EdgeDirection.FORWARD,
        "description": "量子态信息流"
    },
    
    EdgeType.CF: {
        "flow_type": "classical_bits",   # 流动的信息类型
        "data_category": "measurement_result",  # 数据类别
        "direction": EdgeDirection.BIDIRECTIONAL,
        "description": "经典比特信息流"
    },
    
    EdgeType.CONTROL_F: {
        "flow_type": "control_signal",   # 控制信号类型
        "control_type": "execution_order", # 控制类型
        "condition": "always",           # 触发条件
        "direction": EdgeDirection.FORWARD,
        "description": "执行控制信号流"
    },
    
    EdgeType.QCIF: {
        "flow_type": "interface_conversion", # 接口转换类型
        "conversion_type": "measurement_to_classical",
        "direction": EdgeDirection.FORWARD,
        "description": "量子-经典接口转换流"
    }
}


def get_edge_template(edge_type: EdgeType) -> Dict[str, Any]:
    """
    获取指定边类型的默认参数模板
    
    参数：
        edge_type: 边类型
        
    返回值：
        Dict[str, Any]: 包含默认参数的字典
        
    异常：
        ValueError: 不支持的边类型
    """
    if edge_type not in EDGE_TYPE_TEMPLATES:
        raise ValueError(f"不支持的边类型: {edge_type}")
    
    import copy
    template = copy.deepcopy(EDGE_TYPE_TEMPLATES[edge_type])
    
    # 理想化模式下无需调整，边代表抽象信息流
    return template


def validate_edge_params(edge_type: EdgeType, params: Dict[str, Any]) -> bool:
    """
    验证边参数的有效性
    
    参数：
        edge_type: 边类型
        params: 参数字典
        
    返回值：
        bool: 参数是否有效
    """
    # 检查边类型是否支持
    if edge_type not in EDGE_TYPE_TEMPLATES:
        return False
    
    # 获取必需参数列表
    required_params = _get_required_edge_params(edge_type)
    
    # 检查必需参数是否存在
    for param in required_params:
        if param not in params:
            return False
    
    return True


def _get_required_edge_params(edge_type: EdgeType) -> List[str]:
    """
    获取边类型的必需参数列表
    
    参数：
        edge_type: 边类型
        
    返回值：
        List[str]: 必需参数名称列表
    """
    required_params = {
        EdgeType.QF: ["flow_type"],
        EdgeType.CF: ["flow_type", "data_category"],
        EdgeType.CONTROL_F: ["control_type"],
        EdgeType.QCIF: ["conversion_type"]
    }
    
    return required_params.get(edge_type, [])


# ============================================================================
# Edge类定义 - 重构版本专注信息流抽象
# ============================================================================

class Edge:
    """
    协议图边类 - 严格按照研究方案重构
    
    重构思路：
    - 移除了大量物理传输参数，专注信息流抽象
    - 增强了连接约束验证
    - 简化了参数管理，突出信息流特性
    - 完善了序列化支持
    
    核心功能：
    - 信息流的抽象表示
    - 节点间连接约束验证
    - 边类型和方向管理
    """
    
    def __init__(self,
                 source_id: str,
                 target_id: str,
                 edge_type: EdgeType,
                 params: Optional[Dict[str, Any]] = None,
                 edge_id: Optional[str] = None):
        """
        初始化边对象
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
            params: 边参数字典
            edge_id: 边ID（可选，自动生成）
            
        异常：
            ValueError: 参数无效时抛出
        """
        self.source_id = source_id
        self.target_id = target_id
        self.edge_type = edge_type
        self.params = params or {}
        self.edge_id = edge_id or f"{source_id}_{target_id}_{edge_type.value}"
        
        # 设置默认参数
        self._set_default_params()
        
        # 验证参数
        if not validate_edge_params(edge_type, self.params):
            raise ValueError(f"边类型 {edge_type} 的参数无效: {self.params}")
    
    def _set_default_params(self):
        """
        设置默认参数
        """
        template = get_edge_template(self.edge_type)
        for key, value in template.items():
            if key not in self.params:
                self.params[key] = value
    
    def validate_connection(self, source_node_type: str, target_node_type: str) -> bool:
        """
        验证此边是否可以连接给定的节点类型
        
        参数：
            source_node_type: 源节点类型
            target_node_type: 目标节点类型
            
        返回值：
            bool: 是否可以连接
        """
        return validate_edge_connection(self.edge_type, source_node_type, target_node_type)
    
    def update_params(self, new_params: Dict[str, Any]):
        """
        更新边参数
        
        参数：
            new_params: 新的参数字典
            
        异常：
            ValueError: 参数无效时抛出
        """
        # 备份原参数
        old_params = self.params.copy()
        
        # 更新参数
        self.params.update(new_params)
        
        # 验证更新后的参数
        if not validate_edge_params(self.edge_type, self.params):
            # 恢复原参数
            self.params = old_params
            raise ValueError(f"边类型 {self.edge_type} 的参数无效: {new_params}")
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """
        获取指定参数值
        
        参数：
            key: 参数名
            default: 默认值
            
        返回值：
            Any: 参数值
        """
        return self.params.get(key, default)
    
    def set_param(self, key: str, value: Any):
        """
        设置单个参数值
        
        参数：
            key: 参数名
            value: 参数值
            
        异常：
            ValueError: 参数无效时抛出
        """
        # 备份原值
        old_value = self.params.get(key)
        
        # 设置新值
        self.params[key] = value
        
        # 验证参数
        if not validate_edge_params(self.edge_type, self.params):
            # 恢复原值
            if old_value is not None:
                self.params[key] = old_value
            else:
                self.params.pop(key, None)
            raise ValueError(f"边类型 {self.edge_type} 的参数无效: {key}={value}")
    
    def is_quantum_flow(self) -> bool:
        """
        判断是否为量子信息流
        
        返回值：
            bool: 是否为量子信息流
        """
        return EdgeType.is_quantum_flow(self.edge_type)
    
    def is_classical_flow(self) -> bool:
        """
        判断是否为经典信息流
        
        返回值：
            bool: 是否为经典信息流
        """
        return EdgeType.is_classical_flow(self.edge_type)
    
    def is_control_flow(self) -> bool:
        """
        判断是否为控制流
        
        返回值：
            bool: 是否为控制流
        """
        return EdgeType.is_control_flow(self.edge_type)
    
    def get_direction(self) -> EdgeDirection:
        """
        获取边的方向
        
        返回值：
            EdgeDirection: 边的方向
        """
        direction_value = self.params.get("direction", EdgeDirection.FORWARD)
        if isinstance(direction_value, str):
            return EdgeDirection(direction_value)
        return direction_value
    
    def get_flow_type(self) -> str:
        """
        获取信息流类型
        
        返回值：
            str: 信息流类型
        """
        return self.params.get("flow_type", "unknown")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将边转换为字典表示
        
        返回值：
            Dict[str, Any]: 边的字典表示
        """
        # 处理枚举类型的序列化
        serializable_params = {}
        for key, value in self.params.items():
            if isinstance(value, Enum):
                serializable_params[key] = value.value
            else:
                serializable_params[key] = value
        
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type.value,
            "params": serializable_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Edge':
        """
        从字典创建边对象
        
        参数：
            data: 边数据字典
            
        返回值：
            Edge: 边对象实例
            
        异常：
            ValueError: 数据格式错误时抛出
        """
        # 处理枚举类型的反序列化
        params = data.get("params", {}).copy()
        if "direction" in params and isinstance(params["direction"], str):
            try:
                params["direction"] = EdgeDirection(params["direction"])
            except ValueError:
                # 如果无法解析，使用默认方向
                params["direction"] = EdgeDirection.FORWARD
        
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            edge_type=EdgeType(data["edge_type"]),
            params=params,
            edge_id=data.get("edge_id")
        )
    
    def __str__(self) -> str:
        """
        字符串表示
        
        返回值：
            str: 边的字符串表示
        """
        direction_arrow = self._get_direction_arrow()
        flow_type = self.get_flow_type()
        return f"Edge({self.source_id} {direction_arrow} {self.target_id}, {self.edge_type.value}[{flow_type}])"
    
    def _get_direction_arrow(self) -> str:
        """
        根据边的方向获取箭头符号
        
        返回值：
            str: 方向箭头符号
        """
        direction = self.get_direction()
        if direction == EdgeDirection.FORWARD:
            return "->"
        elif direction == EdgeDirection.BACKWARD:
            return "<-"
        elif direction == EdgeDirection.BIDIRECTIONAL:
            return "<->"
        else:
            return "-?"
    
    def __repr__(self) -> str:
        """
        详细字符串表示
        
        返回值：
            str: 边的详细字符串表示
        """
        return f"Edge(id={self.edge_id}, {self.source_id}->{self.target_id}, type={self.edge_type.value}, flow={self.get_flow_type()})"
    
    def __eq__(self, other) -> bool:
        """
        边的相等性比较
        
        参数：
            other: 另一个边对象
            
        返回值：
            bool: 是否相等
        """
        if not isinstance(other, Edge):
            return False
        
        return (self.source_id == other.source_id and
                self.target_id == other.target_id and
                self.edge_type == other.edge_type)
    
    def __hash__(self) -> int:
        """
        边的哈希值计算
        
        返回值：
            int: 哈希值
        """
        return hash((self.source_id, self.target_id, self.edge_type))


# ============================================================================
# 连接验证辅助函数
# ============================================================================

def get_edge_constraints_summary() -> Dict[str, Any]:
    """
    获取所有边类型连接约束的汇总信息
    
    返回值：
        Dict[str, Any]: 约束汇总信息
    """
    return {
        "constraints": EDGE_CONNECTION_CONSTRAINTS,
        "total_edge_types": len(EdgeType),
        "connection_rules": {
            "QF": "量子操作节点间的量子态流动",
            "CF": "经典操作节点间的经典信息传递",
            "ControlF": "CD节点控制其他所有节点的执行",
            "QCIF": "QM节点到CLO/CD节点的量子-经典转换"
        }
    }


def validate_protocol_graph_edges(edges: List[Dict[str, Any]], nodes: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    验证协议图中所有边的连接约束
    
    参数：
        edges: 边列表
        nodes: 节点字典 {node_id: node_info}
        
    返回值：
        List[str]: 违规信息列表，空列表表示全部有效
    """
    violations = []
    
    for edge in edges:
        source_id = edge.get("source_id")
        target_id = edge.get("target_id") 
        edge_type = edge.get("edge_type")
        
        # 检查节点是否存在
        if source_id not in nodes:
            violations.append(f"源节点 {source_id} 不存在")
            continue
        if target_id not in nodes:
            violations.append(f"目标节点 {target_id} 不存在")
            continue
        
        # 获取节点类型
        source_node_type = nodes[source_id].get("node_type", "")
        target_node_type = nodes[target_id].get("node_type", "")
        
        # 验证连接约束
        try:
            edge_type_enum = EdgeType(edge_type)
            if not validate_edge_connection(edge_type_enum, source_node_type, target_node_type):
                violations.append(f"无效连接: {source_node_type}({source_id}) -{edge_type}-> {target_node_type}({target_id})")
        except ValueError:
            violations.append(f"未知边类型: {edge_type}")
    
    return violations