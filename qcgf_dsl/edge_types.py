"""
边类型定义模块

定义了QCGF DSL中支持的各种边类型，包括量子信道、经典信道、控制信号等。
"""

from enum import Enum
from typing import Dict, Any, Optional


class EdgeType(Enum):
    """
    边类型枚举
    
    定义了QCGF DSL中支持的各种边类型：
    - QUANTUM: 量子信道，用于传输量子态
    - CLASSICAL: 经典信道，用于传输经典信息
    - CONTROL: 控制信号，用于控制操作
    - DATA: 数据传输，用于传输处理后的数据
    - FEEDBACK: 反馈信号，用于协议反馈
    - SYNCHRONIZATION: 同步信号，用于时间同步
    """
    
    QUANTUM = "quantum"           # 量子信道
    CLASSICAL = "classical"       # 经典信道
    CONTROL = "control"           # 控制信号
    DATA = "data"                # 数据传输
    FEEDBACK = "feedback"        # 反馈信号
    SYNCHRONIZATION = "sync"     # 同步信号
    
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.name == value.upper() or member.value == value.lower():
                    return member
        return None

    @classmethod
    def get_quantum_edges(cls) -> list:
        """获取所有量子相关边类型"""
        return [cls.QUANTUM]
    
    @classmethod
    def get_classical_edges(cls) -> list:
        """获取所有经典相关边类型"""
        return [cls.CLASSICAL, cls.CONTROL, cls.DATA, cls.FEEDBACK, cls.SYNCHRONIZATION]
    
    @classmethod
    def is_quantum_edge(cls, edge_type) -> bool:
        """判断是否为量子边类型"""
        return edge_type in cls.get_quantum_edges()
    
    @classmethod
    def is_classical_edge(cls, edge_type) -> bool:
        """判断是否为经典边类型"""
        return edge_type in cls.get_classical_edges()


class EdgeDirection(Enum):
    """边方向枚举"""
    FORWARD = "forward"      # 前向
    BACKWARD = "backward"    # 后向
    BIDIRECTIONAL = "bidirectional"  # 双向


# 边类型默认参数模板
EDGE_TYPE_TEMPLATES = {
    EdgeType.QUANTUM: {
        "loss": 0.1,
        "noise": 0.01,
        "distance": 50.0,
        "wavelength": 1550.0,  # nm
        "bandwidth": 1e12,     # Hz
        "direction": EdgeDirection.FORWARD
    },
    EdgeType.CLASSICAL: {
        "bandwidth": 1e9,      # bps
        "latency": 1e-6,       # s
        "error_rate": 1e-9,
        "direction": EdgeDirection.BIDIRECTIONAL
    },
    EdgeType.CONTROL: {
        "signal_type": "digital",
        "voltage": 3.3,        # V
        "frequency": 1e6,      # Hz
        "direction": EdgeDirection.BIDIRECTIONAL
    },
    EdgeType.DATA: {
        "data_type": "raw_key",
        "compression_ratio": 1.0,
        "encryption": False,
        "direction": EdgeDirection.FORWARD
    },
    EdgeType.FEEDBACK: {
        "feedback_type": "error_correction",
        "delay": 1e-3,         # s
        "direction": EdgeDirection.BACKWARD
    },
    EdgeType.SYNCHRONIZATION: {
        "sync_type": "clock",
        "frequency": 1e9,      # Hz
        "jitter": 1e-12,       # s
        "direction": EdgeDirection.BIDIRECTIONAL
    }
}


def get_edge_template(edge_type: EdgeType) -> Dict[str, Any]:
    """
    获取指定边类型的默认参数模板
    
    Args:
        edge_type: 边类型
        
    Returns:
        包含默认参数的字典
    """
    return EDGE_TYPE_TEMPLATES.get(edge_type, {}).copy()


def validate_edge_params(edge_type: EdgeType, params: Dict[str, Any]) -> bool:
    """
    验证边参数的有效性
    
    Args:
        edge_type: 边类型
        params: 参数字典
        
    Returns:
        参数是否有效
    """
    template = get_edge_template(edge_type)
    
    # 基本验证：检查必需参数
    required_params = {
        EdgeType.QUANTUM: ["loss"],
        EdgeType.CLASSICAL: ["bandwidth"],
        EdgeType.CONTROL: ["signal_type"],
        EdgeType.DATA: ["data_type"],
        EdgeType.FEEDBACK: ["feedback_type"],
        EdgeType.SYNCHRONIZATION: ["sync_type"]
    }
    
    if edge_type in required_params:
        for param in required_params[edge_type]:
            if param not in params:
                return False
    
    # 数值范围验证
    if edge_type == EdgeType.QUANTUM:
        if "loss" in params and not (0 <= params["loss"] <= 1):
            return False
        if "noise" in params and not (0 <= params["noise"] <= 1):
            return False
        if "distance" in params and params["distance"] < 0:
            return False
    
    if edge_type == EdgeType.CLASSICAL:
        if "bandwidth" in params and params["bandwidth"] <= 0:
            return False
        if "error_rate" in params and not (0 <= params["error_rate"] <= 1):
            return False
    
    return True


class Edge:
    """
    边类
    
    表示协议图中的连接，包含源节点、目标节点、边类型和参数信息。
    """
    
    def __init__(self,
                 source_id: str,
                 target_id: str,
                 edge_type: EdgeType,
                 params: Optional[Dict[str, Any]] = None,
                 edge_id: Optional[str] = None):
        """
        初始化边
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
            params: 边参数字典
            edge_id: 边ID（可选，自动生成）
        """
        self.source_id = source_id
        self.target_id = target_id
        self.edge_type = edge_type
        self.params = params or {}
        self.edge_id = edge_id or f"{source_id}_to_{target_id}"
        
        # 设置默认参数
        self._set_default_params()
        
        # 验证参数
        if not validate_edge_params(edge_type, self.params):
            raise ValueError(f"Invalid parameters for edge type {edge_type}")
    
    def _set_default_params(self):
        """设置默认参数"""
        template = get_edge_template(self.edge_type)
        for key, value in template.items():
            if key not in self.params:
                self.params[key] = value
    
    def update_params(self, new_params: Dict[str, Any]):
        """
        更新边参数
        
        Args:
            new_params: 新的参数字典
        """
        self.params.update(new_params)
        if not validate_edge_params(self.edge_type, self.params):
            raise ValueError(f"Invalid parameters for edge type {self.edge_type}")
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """
        获取指定参数值
        
        Args:
            key: 参数名
            default: 默认值
            
        Returns:
            参数值
        """
        return self.params.get(key, default)
    
    def set_param(self, key: str, value: Any):
        """
        设置参数值
        
        Args:
            key: 参数名
            value: 参数值
        """
        self.params[key] = value
    
    def is_quantum_edge(self) -> bool:
        """判断是否为量子边"""
        return EdgeType.is_quantum_edge(self.edge_type)
    
    def is_classical_edge(self) -> bool:
        """判断是否为经典边"""
        return EdgeType.is_classical_edge(self.edge_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将边转换为字典表示
        
        Returns:
            边字典表示
        """
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type.value,
            "params": self.params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Edge':
        """
        从字典创建边
        
        Args:
            data: 边数据字典
            
        Returns:
            Edge实例
        """
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            edge_type=EdgeType(data["edge_type"]),
            params=data.get("params", {}),
            edge_id=data.get("edge_id")
        )
    
    def __str__(self) -> str:
        return f"Edge({self.source_id} -> {self.target_id}, {self.edge_type.value})"
    
    def __repr__(self) -> str:
        return self.__str__() 