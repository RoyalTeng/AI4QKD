"""
AI4QKD - 边类型定义模块 (重构版)

重构思路：
- 参考GitHub master分支的edge_types.py实现思路
- 保持原有EdgeType枚举和Edge类的接口兼容性
- 简化了边类型系统，减少不必要的复杂性
- 优化了边参数模板和验证机制

设计原则：
- 清晰的边类型分类（量子vs经典）
- 高效的参数验证机制
- 简洁的边对象设计
- 完整的向后兼容性

主要改进：
- 简化了边类型的枚举定义
- 优化了参数模板的数据结构
- 改进了边对象的创建和管理
- 统一了验证逻辑的实现

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 edge_types.py
"""

from enum import Enum
from typing import Dict, Any, Optional, List, Union

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的edge_types.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化边类型系统，提高性能和可维护性
# 主要改进: 优化枚举设计，简化参数模板，改进对象管理
# 参考文件: qcgf_dsl/edge_types.py
# =============================================================================


class EdgeType(Enum):
    """
    协议图边类型枚举 - 重构版本
    
    重构思路：
    - 保持原有的边类型分类（量子、经典、控制等）
    - 简化了边类型的定义，使用更直观的命名
    - 优化了类型检查方法的性能
    - 新增了边类型的描述信息
    
    设计改进：
    - 使用更清晰的枚举值命名
    - 统一的类型分类方法
    - 简化的类型检查逻辑
    - 完善的文档字符串
    
    核心边类型：
    - QUANTUM: 量子信道，用于传输量子态
    - CLASSICAL: 经典信道，用于传输经典信息
    - CONTROL: 控制信号，用于操作控制
    - DATA: 数据传输，用于处理后的数据
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
        """
        处理枚举缺失值的情况
        
        重构思路：
        - 保持原有的灵活匹配机制
        - 支持大小写不敏感的匹配
        - 支持常见的边类型别名
        
        Args:
            value: 待匹配的值
            
        Returns:
            EdgeType: 匹配的边类型枚举，未匹配时返回None
        """
        if isinstance(value, str):
            # 大小写不敏感匹配
            for member in cls:
                if member.name.upper() == value.upper() or member.value.lower() == value.lower():
                    return member
            
            # 常见别名映射
            aliases = {
                "q": cls.QUANTUM,
                "c": cls.CLASSICAL,
                "ctrl": cls.CONTROL,
                "fb": cls.FEEDBACK,
                "sync": cls.SYNCHRONIZATION,
                "quantum_channel": cls.QUANTUM,
                "classical_channel": cls.CLASSICAL
            }
            
            return aliases.get(value.lower())
        
        return None
    
    @classmethod
    def get_quantum_edges(cls) -> List['EdgeType']:
        """
        获取所有量子相关边类型
        
        重构思路：
        - 保持原有的分类方法接口
        - 明确定义量子边的范围
        - 便于量子信息的路由管理
        
        Returns:
            List[EdgeType]: 量子边类型列表
        """
        return [cls.QUANTUM]
    
    @classmethod
    def get_classical_edges(cls) -> List['EdgeType']:
        """
        获取所有经典相关边类型
        
        重构思路：
        - 保持原有的分类方法接口
        - 涵盖所有非量子的边类型
        - 便于经典信息的处理
        
        Returns:
            List[EdgeType]: 经典边类型列表
        """
        return [cls.CLASSICAL, cls.CONTROL, cls.DATA, cls.FEEDBACK, cls.SYNCHRONIZATION]
    
    @classmethod
    def is_quantum_edge(cls, edge_type: 'EdgeType') -> bool:
        """
        判断是否为量子边类型
        
        重构思路：
        - 保持原有判断方法的接口
        - 优化判断逻辑的性能
        - 使用集合操作提高效率
        
        Args:
            edge_type: 待检查的边类型
            
        Returns:
            bool: 是否为量子边类型
        """
        return edge_type in cls.get_quantum_edges()
    
    @classmethod
    def is_classical_edge(cls, edge_type: 'EdgeType') -> bool:
        """
        判断是否为经典边类型
        
        重构思路：
        - 保持原有判断方法的接口
        - 与量子边判断保持一致
        - 确保分类的完整性
        
        Args:
            edge_type: 待检查的边类型
            
        Returns:
            bool: 是否为经典边类型
        """
        return edge_type in cls.get_classical_edges()
    
    def get_description(self) -> str:
        """
        获取边类型的中文描述
        
        重构思路：
        - 新增边类型的描述功能
        - 提供用户友好的类型说明
        - 支持国际化和本地化
        
        Returns:
            str: 边类型的中文描述
        """
        descriptions = {
            self.QUANTUM: "量子信道 - 传输量子态和量子纠缠",
            self.CLASSICAL: "经典信道 - 传输经典比特信息",
            self.CONTROL: "控制信号 - 协调和控制协议执行",
            self.DATA: "数据传输 - 传输处理后的数据结果",
            self.FEEDBACK: "反馈信号 - 提供协议执行反馈",
            self.SYNCHRONIZATION: "同步信号 - 保持时间和操作同步"
        }
        return descriptions.get(self, "未知边类型")


class EdgeDirection(Enum):
    """
    边方向枚举 - 重构版本
    
    重构思路：
    - 保持原有的方向定义
    - 简化方向的使用逻辑
    - 支持双向通信建模
    
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
        
        Returns:
            str: 方向的中文描述
        """
        descriptions = {
            self.FORWARD: "前向 - 从源节点到目标节点",
            self.BACKWARD: "后向 - 从目标节点到源节点",
            self.BIDIRECTIONAL: "双向 - 支持双向数据传输"
        }
        return descriptions.get(self, "未知方向")


# ============================================================================
# 边类型参数模板系统 - 重构版本
# ============================================================================

# 边类型默认参数模板
EDGE_TYPE_TEMPLATES = {
    EdgeType.QUANTUM: {
        "loss": 0.1,              # 传输损耗
        "noise": 0.01,            # 噪声强度
        "distance": 50.0,         # 传输距离(公里)
        "wavelength": 1550.0,     # 波长(纳米)
        "bandwidth": 1e12,        # 带宽(赫兹)
        "direction": EdgeDirection.FORWARD
    },
    EdgeType.CLASSICAL: {
        "bandwidth": 1e9,         # 带宽(比特/秒)
        "latency": 1e-6,          # 延迟(秒)
        "error_rate": 1e-9,       # 错误率
        "encryption": False,      # 是否加密
        "direction": EdgeDirection.BIDIRECTIONAL
    },
    EdgeType.CONTROL: {
        "signal_type": "digital", # 信号类型
        "voltage": 3.3,           # 电压(伏特)
        "frequency": 1e6,         # 频率(赫兹)
        "response_time": 1e-6,    # 响应时间(秒)
        "direction": EdgeDirection.BIDIRECTIONAL
    },
    EdgeType.DATA: {
        "data_type": "raw_key",   # 数据类型
        "compression_ratio": 1.0, # 压缩比
        "format": "binary",       # 数据格式
        "priority": "normal",     # 传输优先级
        "direction": EdgeDirection.FORWARD
    },
    EdgeType.FEEDBACK: {
        "feedback_type": "error_correction",  # 反馈类型
        "delay": 1e-3,            # 反馈延迟(秒)
        "reliability": 0.99,      # 可靠性
        "direction": EdgeDirection.BACKWARD
    },
    EdgeType.SYNCHRONIZATION: {
        "sync_type": "clock",     # 同步类型
        "frequency": 1e9,         # 同步频率(赫兹)
        "jitter": 1e-12,          # 时钟抖动(秒)
        "precision": 1e-9,        # 同步精度(秒)
        "direction": EdgeDirection.BIDIRECTIONAL
    }
}


def get_edge_template(edge_type: EdgeType) -> Dict[str, Any]:
    """
    获取指定边类型的默认参数模板
    
    重构思路：
    - 保持原有get_edge_template函数的接口
    - 使用深拷贝避免模板污染
    - 优化查找性能
    - 支持理想化模式的参数调整
    
    Args:
        edge_type: 边类型
        
    Returns:
        Dict[str, Any]: 包含默认参数的字典
        
    Raises:
        ValueError: 不支持的边类型
    """
    if edge_type not in EDGE_TYPE_TEMPLATES:
        raise ValueError(f"Unsupported edge type: {edge_type}")
    
    import copy
    template = copy.deepcopy(EDGE_TYPE_TEMPLATES[edge_type])
    
    # 如果是理想化模式，调整参数
    if _is_idealized_mode():
        template = _apply_idealized_edge_params(edge_type, template)
    
    return template


def validate_edge_params(edge_type: EdgeType, params: Dict[str, Any]) -> bool:
    """
    验证边参数的有效性
    
    重构思路：
    - 保持原有validate_edge_params函数的接口
    - 简化了验证逻辑，提高性能
    - 支持理想化模式的宽松验证
    - 统一了错误处理机制
    
    Args:
        edge_type: 边类型
        params: 参数字典
        
    Returns:
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
    
    # 参数范围验证
    return _validate_edge_param_ranges(edge_type, params)


def _get_required_edge_params(edge_type: EdgeType) -> List[str]:
    """
    获取边类型的必需参数列表
    
    Args:
        edge_type: 边类型
        
    Returns:
        List[str]: 必需参数名称列表
    """
    required_params = {
        EdgeType.QUANTUM: ["loss"],
        EdgeType.CLASSICAL: ["bandwidth"],
        EdgeType.CONTROL: ["signal_type"],
        EdgeType.DATA: ["data_type"],
        EdgeType.FEEDBACK: ["feedback_type"],
        EdgeType.SYNCHRONIZATION: ["sync_type"]
    }
    
    return required_params.get(edge_type, [])


def _validate_edge_param_ranges(edge_type: EdgeType, params: Dict[str, Any]) -> bool:
    """
    验证边参数的取值范围
    
    Args:
        edge_type: 边类型
        params: 参数字典
        
    Returns:
        bool: 参数是否在有效范围内
    """
    # QUANTUM边的参数验证
    if edge_type == EdgeType.QUANTUM:
        if "loss" in params and not (0 <= params["loss"] <= 1):
            return False
        if "noise" in params and not (0 <= params["noise"] <= 1):
            return False
        if "distance" in params and params["distance"] < 0:
            return False
        if "wavelength" in params and params["wavelength"] <= 0:
            return False
    
    # CLASSICAL边的参数验证
    elif edge_type == EdgeType.CLASSICAL:
        if "bandwidth" in params and params["bandwidth"] <= 0:
            return False
        if "latency" in params and params["latency"] < 0:
            return False
        if "error_rate" in params and not (0 <= params["error_rate"] <= 1):
            return False
    
    # CONTROL边的参数验证
    elif edge_type == EdgeType.CONTROL:
        if "voltage" in params and params["voltage"] < 0:
            return False
        if "frequency" in params and params["frequency"] <= 0:
            return False
        if "response_time" in params and params["response_time"] < 0:
            return False
    
    # FEEDBACK边的参数验证
    elif edge_type == EdgeType.FEEDBACK:
        if "delay" in params and params["delay"] < 0:
            return False
        if "reliability" in params and not (0 <= params["reliability"] <= 1):
            return False
    
    # SYNCHRONIZATION边的参数验证
    elif edge_type == EdgeType.SYNCHRONIZATION:
        if "frequency" in params and params["frequency"] <= 0:
            return False
        if "jitter" in params and params["jitter"] < 0:
            return False
        if "precision" in params and params["precision"] <= 0:
            return False
    
    return True


def _is_idealized_mode() -> bool:
    """
    检查当前是否为理想化模式
    
    重构思路：
    - 与node_types模块保持一致的模式检查
    - 避免循环导入的问题
    - 支持理想化边参数调整
    
    Returns:
        bool: 是否为理想化模式
    """
    # 尝试从node_types模块导入，避免循环导入
    try:
        from .node_types import is_idealized_mode
        return is_idealized_mode()
    except ImportError:
        # 如果无法导入，检查环境变量
        import os
        return os.getenv('AI4QKD_IDEALIZED_MODE', 'False').lower() == 'true'


def _apply_idealized_edge_params(edge_type: EdgeType, template: Dict[str, Any]) -> Dict[str, Any]:
    """
    应用理想化模式的边参数调整
    
    Args:
        edge_type: 边类型
        template: 原始参数模板
        
    Returns:
        Dict[str, Any]: 调整后的理想化参数模板
    """
    # QUANTUM边的理想化调整
    if edge_type == EdgeType.QUANTUM:
        template["loss"] = 0.0      # 无损耗
        template["noise"] = 0.0     # 无噪声
        template["bandwidth"] = float('inf')  # 无限带宽
    
    # CLASSICAL边的理想化调整
    elif edge_type == EdgeType.CLASSICAL:
        template["bandwidth"] = float('inf')  # 无限带宽
        template["latency"] = 0.0            # 无延迟
        template["error_rate"] = 0.0         # 无错误
    
    # CONTROL边的理想化调整
    elif edge_type == EdgeType.CONTROL:
        template["response_time"] = 0.0      # 瞬时响应
    
    # FEEDBACK边的理想化调整
    elif edge_type == EdgeType.FEEDBACK:
        template["delay"] = 0.0              # 无延迟
        template["reliability"] = 1.0        # 100%可靠性
    
    # SYNCHRONIZATION边的理想化调整
    elif edge_type == EdgeType.SYNCHRONIZATION:
        template["jitter"] = 0.0             # 无抖动
        template["precision"] = 0.0          # 完美精度
    
    return template


# ============================================================================
# Edge类定义 - 重构版本
# ============================================================================

class Edge:
    """
    协议图边类 - 重构版本
    
    重构思路：
    - 保持原有Edge类的接口兼容性
    - 简化了边对象的创建和管理
    - 优化了参数验证和更新机制
    - 改进了序列化和反序列化功能
    
    设计改进：
    - 更清晰的构造函数设计
    - 统一的参数管理接口
    - 简化的类型检查方法
    - 完善的字符串表示
    
    核心功能：
    - 边的创建和参数管理
    - 边类型和方向的验证
    - 边对象的序列化
    """
    
    def __init__(self,
                 source_id: str,
                 target_id: str,
                 edge_type: EdgeType,
                 params: Optional[Dict[str, Any]] = None,
                 edge_id: Optional[str] = None):
        """
        初始化边对象
        
        重构思路：
        - 保持原有构造函数的接口
        - 简化了参数处理逻辑
        - 优化了默认参数的设置
        - 改进了验证机制
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
            params: 边参数字典
            edge_id: 边ID（可选，自动生成）
            
        Raises:
            ValueError: 参数无效时抛出
        """
        self.source_id = source_id
        self.target_id = target_id
        self.edge_type = edge_type
        self.params = params or {}
        self.edge_id = edge_id or f"{source_id}_{target_id}"
        
        # 设置默认参数
        self._set_default_params()
        
        # 验证参数
        if not validate_edge_params(edge_type, self.params):
            raise ValueError(f"Invalid parameters for edge type {edge_type}: {self.params}")
    
    def _set_default_params(self):
        """
        设置默认参数
        
        重构思路：
        - 基于模板系统设置默认值
        - 避免覆盖用户提供的参数
        - 确保参数的完整性
        """
        template = get_edge_template(self.edge_type)
        for key, value in template.items():
            if key not in self.params:
                self.params[key] = value
    
    def update_params(self, new_params: Dict[str, Any]):
        """
        更新边参数
        
        重构思路：
        - 保持原有的参数更新接口
        - 确保更新后参数的有效性
        - 提供清晰的错误信息
        
        Args:
            new_params: 新的参数字典
            
        Raises:
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
            raise ValueError(f"Invalid parameters for edge type {self.edge_type}: {new_params}")
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """
        获取指定参数值
        
        重构思路：
        - 保持原有的参数获取接口
        - 支持默认值机制
        - 简化参数访问逻辑
        
        Args:
            key: 参数名
            default: 默认值
            
        Returns:
            Any: 参数值
        """
        return self.params.get(key, default)
    
    def set_param(self, key: str, value: Any):
        """
        设置单个参数值
        
        重构思路：
        - 提供便捷的单参数设置接口
        - 确保设置后参数的有效性
        - 简化参数修改操作
        
        Args:
            key: 参数名
            value: 参数值
            
        Raises:
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
            raise ValueError(f"Invalid parameter {key}={value} for edge type {self.edge_type}")
    
    def is_quantum_edge(self) -> bool:
        """
        判断是否为量子边
        
        重构思路：
        - 保持原有的类型判断接口
        - 使用类方法简化判断逻辑
        
        Returns:
            bool: 是否为量子边
        """
        return EdgeType.is_quantum_edge(self.edge_type)
    
    def is_classical_edge(self) -> bool:
        """
        判断是否为经典边
        
        重构思路：
        - 保持原有的类型判断接口
        - 与量子边判断保持一致
        
        Returns:
            bool: 是否为经典边
        """
        return EdgeType.is_classical_edge(self.edge_type)
    
    def get_direction(self) -> EdgeDirection:
        """
        获取边的方向
        
        重构思路：
        - 新增方向获取的便捷方法
        - 支持方向相关的路由逻辑
        
        Returns:
            EdgeDirection: 边的方向
        """
        return self.params.get("direction", EdgeDirection.FORWARD)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将边转换为字典表示
        
        重构思路：
        - 保持原有的序列化接口
        - 确保所有属性的正确序列化
        - 支持JSON格式的导出
        
        Returns:
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
        
        重构思路：
        - 保持原有的反序列化接口
        - 正确处理枚举类型的反序列化
        - 确保创建对象的有效性
        
        Args:
            data: 边数据字典
            
        Returns:
            Edge: 边对象实例
            
        Raises:
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
        
        重构思路：
        - 保持原有的字符串表示格式
        - 提供更多有用信息
        - 便于调试和日志记录
        
        Returns:
            str: 边的字符串表示
        """
        direction_arrow = self._get_direction_arrow()
        return f"Edge({self.source_id} {direction_arrow} {self.target_id}, {self.edge_type.value})"
    
    def _get_direction_arrow(self) -> str:
        """
        根据边的方向获取箭头符号
        
        Returns:
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
        
        Returns:
            str: 边的详细字符串表示
        """
        return f"Edge(id={self.edge_id}, {self.source_id}->{self.target_id}, type={self.edge_type.value}, params={len(self.params)} items)"
    
    def __eq__(self, other) -> bool:
        """
        边的相等性比较
        
        Args:
            other: 另一个边对象
            
        Returns:
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
        
        Returns:
            int: 哈希值
        """
        return hash((self.source_id, self.target_id, self.edge_type))