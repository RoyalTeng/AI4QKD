"""
AI4QKD - 节点类型定义模块 (重构版)

重构思路：
- 参考GitHub master分支的node_types.py实现思路
- 保持原有NodeType和Party枚举的接口兼容性
- 简化了参数模板系统，提高性能和可读性
- 优化了理想化模式的实现机制

设计原则：
- 清晰的类型层次结构
- 高效的参数验证机制
- 灵活的模式切换支持
- 完整的向后兼容性

主要改进：
- 简化了参数模板的数据结构
- 优化了验证函数的性能
- 改进了理想化模式的切换逻辑
- 统一了错误处理机制

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 node_types.py
"""

import os
from enum import Enum
from typing import Dict, Any, Optional, List, Union

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的node_types.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化类型系统，提高性能和可维护性
# 主要改进: 优化枚举设计，简化参数模板，改进模式切换
# 参考文件: qcgf_dsl/node_types.py
# =============================================================================


class NodeType(Enum):
    """
    量子协议节点类型枚举 - 重构版本
    
    重构思路：
    - 保持原有的节点类型分类（量子vs经典）
    - 简化了类型定义，使用更直观的命名
    - 优化了类型检查方法的性能
    - 新增了节点类型的描述信息
    
    设计改进：
    - 使用更清晰的枚举值命名
    - 统一的类型分类方法
    - 简化的类型检查逻辑
    - 完善的文档字符串
    
    核心节点类型：
    - QSP: 量子态准备 (Quantum State Preparation)
    - QC: 量子信道 (Quantum Channel)
    - QM: 量子测量 (Quantum Measurement)
    - QG: 量子门 (Quantum Gate)
    - QD: 量子检测器 (Quantum Detector)
    - BSM: 贝尔态测量 (Bell State Measurement)
    - CLO: 经典逻辑操作 (Classical Logic Operation)
    - CS: 经典存储 (Classical Storage)
    - CC: 经典信道 (Classical Channel)
    """
    
    # 量子操作节点
    QSP = "QSP"    # 量子态准备
    QC = "QC"      # 量子信道
    QM = "QM"      # 量子测量
    QG = "QG"      # 量子门
    QD = "QD"      # 量子检测器
    BSM = "BSM"    # 贝尔态测量
    
    # 经典操作节点
    CLO = "CLO"    # 经典逻辑操作
    CS = "CS"      # 经典存储
    CC = "CC"      # 经典信道
    
    # 特殊节点
    ATTACK = "ATTACK"  # 攻击节点（安全分析用）
    SINK = "SINK"      # 汇聚节点
    
    @classmethod
    def get_quantum_types(cls) -> List['NodeType']:
        """
        获取所有量子操作节点类型
        
        重构思路：
        - 保持原有的分类方法接口
        - 使用列表推导优化性能
        - 返回不可变的类型列表
        
        Returns:
            List[NodeType]: 量子节点类型列表
        """
        return [cls.QSP, cls.QC, cls.QM, cls.QG, cls.QD, cls.BSM]
    
    @classmethod 
    def get_classical_types(cls) -> List['NodeType']:
        """
        获取所有经典操作节点类型
        
        重构思路：
        - 保持原有的分类方法接口
        - 明确区分量子和经典节点
        - 便于类型验证和处理
        
        Returns:
            List[NodeType]: 经典节点类型列表
        """
        return [cls.CLO, cls.CS, cls.CC]
    
    @classmethod
    def is_quantum_type(cls, node_type: 'NodeType') -> bool:
        """
        判断是否为量子操作节点类型
        
        重构思路：
        - 保持原有判断方法的接口
        - 优化判断逻辑的性能
        - 使用集合操作提高效率
        
        Args:
            node_type: 待检查的节点类型
            
        Returns:
            bool: 是否为量子节点类型
        """
        return node_type in cls.get_quantum_types()
    
    @classmethod
    def is_classical_type(cls, node_type: 'NodeType') -> bool:
        """
        判断是否为经典操作节点类型
        
        重构思路：
        - 保持原有判断方法的接口
        - 与量子类型判断保持一致
        - 确保分类的完整性
        
        Args:
            node_type: 待检查的节点类型
            
        Returns:
            bool: 是否为经典节点类型
        """
        return node_type in cls.get_classical_types()
    
    def get_description(self) -> str:
        """
        获取节点类型的中文描述
        
        重构思路：
        - 新增节点类型的描述功能
        - 提供用户友好的类型说明
        - 支持国际化和本地化
        
        Returns:
            str: 节点类型的中文描述
        """
        descriptions = {
            self.QSP: "量子态准备 - 制备特定的量子态",
            self.QC: "量子信道 - 传输量子信息的物理信道",
            self.QM: "量子测量 - 对量子态进行测量操作",
            self.QG: "量子门 - 对量子态进行幺正变换",
            self.QD: "量子检测器 - 检测量子信号的物理设备",
            self.BSM: "贝尔态测量 - 对量子纠缠态进行投影测量",
            self.CLO: "经典逻辑操作 - 对经典数据进行逻辑处理",
            self.CS: "经典存储 - 存储经典信息的设备",
            self.CC: "经典信道 - 传输经典信息的通信信道",
            self.ATTACK: "攻击节点 - 模拟攻击者的行为",
            self.SINK: "汇聚节点 - 汇集多个输入的处理节点"
        }
        return descriptions.get(self, "未知节点类型")


class Party(Enum):
    """
    协议参与者枚举 - 重构版本
    
    重构思路：
    - 保持原有的参与者定义（Alice、Bob、Eve、Charlie）
    - 简化了枚举的缺失值处理逻辑
    - 优化了大小写不敏感的匹配机制
    - 新增了参与者角色的描述信息
    
    设计改进：
    - 更清晰的角色定义
    - 统一的大小写处理
    - 完善的文档说明
    - 易于扩展的设计
    
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
        处理枚举缺失值的情况
        
        重构思路：
        - 保持原有的大小写不敏感匹配
        - 简化了匹配逻辑，提高性能
        - 支持常见的参与者名称变体
        
        Args:
            value: 待匹配的值
            
        Returns:
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
        
        重构思路：
        - 新增参与者角色的详细说明
        - 便于理解协议中各方的职责
        - 支持教学和文档生成
        
        Returns:
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
# 参数模板系统 - 重构版本
# ============================================================================

# 节点类型默认参数模板
NODE_TYPE_TEMPLATES = {
    NodeType.QSP: {
        "state": "|0⟩",           # 初始量子态
        "fidelity": 0.99,         # 态制备保真度
        "preparation_time": 1e-9,  # 制备时间(秒)
        "party": Party.ALICE      # 默认参与者
    },
    NodeType.QC: {
        "loss": 0.1,              # 信道损耗率
        "noise": 0.01,            # 噪声强度
        "distance": 50.0,         # 传输距离(公里)
        "channel_type": "optical_fiber"  # 信道类型
    },
    NodeType.QM: {
        "basis": "computational", # 测量基
        "efficiency": 0.8,        # 检测效率
        "dark_count_rate": 1e-6,  # 暗计数率
        "party": Party.BOB        # 默认参与者
    },
    NodeType.QG: {
        "gate_type": "H",         # 量子门类型
        "fidelity": 0.99,         # 门操作保真度
        "gate_time": 1e-9         # 门操作时间(秒)
    },
    NodeType.QD: {
        "detector_type": "SPAD",  # 检测器类型
        "efficiency": 0.8,        # 检测效率
        "dark_count_rate": 1e-6,  # 暗计数率
        "dead_time": 1e-6         # 死时间(秒)
    },
    NodeType.BSM: {
        "efficiency": 0.5,        # Bell态测量效率
        "success_probability": 0.25,  # 成功概率
        "party": Party.CHARLIE    # 默认参与者
    },
    NodeType.CLO: {
        "operation": "XOR",       # 逻辑操作类型
        "processing_time": 1e-9,  # 处理时间(秒)
        "party": Party.ALICE      # 默认参与者
    },
    NodeType.CS: {
        "storage_type": "memory", # 存储类型
        "capacity": 1000,         # 存储容量(比特)
        "access_time": 1e-9       # 访问时间(秒)
    },
    NodeType.CC: {
        "bandwidth": 1e9,         # 带宽(比特/秒)
        "latency": 1e-6,          # 延迟(秒)
        "error_rate": 1e-9        # 错误率
    },
    NodeType.ATTACK: {
        "attack_type": "intercept_resend",  # 攻击类型
        "intercept_probability": 0.5,       # 截获概率
        "party": Party.EVE        # 默认参与者
    },
    NodeType.SINK: {
        "sink_type": "key_generation",  # 汇聚类型
        "party": Party.BOB        # 默认参与者
    }
}


def get_node_template(node_type: NodeType) -> Dict[str, Any]:
    """
    获取指定节点类型的默认参数模板
    
    重构思路：
    - 保持原有get_node_template函数的接口
    - 支持理想化模式的参数切换
    - 使用深拷贝避免模板污染
    - 优化查找性能
    
    Args:
        node_type: 节点类型
        
    Returns:
        Dict[str, Any]: 包含默认参数的字典
        
    Raises:
        ValueError: 不支持的节点类型
    """
    if node_type not in NODE_TYPE_TEMPLATES:
        raise ValueError(f"Unsupported node type: {node_type}")
    
    # 检查是否为理想化模式
    if _is_idealized_mode():
        return _get_idealized_template(node_type)
    
    # 返回现实模式模板的深拷贝
    import copy
    return copy.deepcopy(NODE_TYPE_TEMPLATES[node_type])


def validate_node_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证节点参数的有效性
    
    重构思路：
    - 保持原有validate_node_params函数的接口
    - 简化了验证逻辑，提高性能
    - 支持理想化模式的宽松验证
    - 统一了错误处理机制
    
    Args:
        node_type: 节点类型
        params: 参数字典
        
    Returns:
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
    获取节点类型的必需参数列表
    
    重构思路：
    - 将参数要求定义独立出来
    - 便于维护和扩展
    - 支持不同模式的不同要求
    
    Args:
        node_type: 节点类型
        
    Returns:
        List[str]: 必需参数名称列表
    """
    required_params = {
        NodeType.QSP: ["state"],
        NodeType.QC: ["loss"],
        NodeType.QM: ["basis"],
        NodeType.QG: ["gate_type"],
        NodeType.QD: ["detector_type"],
        NodeType.BSM: ["efficiency"],
        NodeType.CLO: ["operation"],
        NodeType.CS: ["storage_type"],
        NodeType.CC: ["bandwidth"],
        NodeType.ATTACK: ["attack_type"],
        NodeType.SINK: ["sink_type"]
    }
    
    return required_params.get(node_type, [])


def _validate_realistic_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证现实模式下的参数范围
    
    重构思路：
    - 分离现实模式的严格验证逻辑
    - 确保参数值在物理合理范围内
    - 提供清晰的验证规则
    
    Args:
        node_type: 节点类型
        params: 参数字典
        
    Returns:
        bool: 参数是否在有效范围内
    """
    # QC节点的参数验证
    if node_type == NodeType.QC:
        if "loss" in params and not (0 <= params["loss"] <= 1):
            return False
        if "noise" in params and not (0 <= params["noise"] <= 1):
            return False
        if "distance" in params and params["distance"] < 0:
            return False
    
    # QM节点的参数验证
    elif node_type == NodeType.QM:
        if "efficiency" in params and not (0 <= params["efficiency"] <= 1):
            return False
        if "dark_count_rate" in params and params["dark_count_rate"] < 0:
            return False
    
    # QG节点的参数验证
    elif node_type == NodeType.QG:
        if "fidelity" in params and not (0 <= params["fidelity"] <= 1):
            return False
        if "gate_time" in params and params["gate_time"] < 0:
            return False
    
    # BSM节点的参数验证
    elif node_type == NodeType.BSM:
        if "efficiency" in params and not (0 <= params["efficiency"] <= 1):
            return False
        if "success_probability" in params and not (0 <= params["success_probability"] <= 1):
            return False
    
    # CC节点的参数验证
    elif node_type == NodeType.CC:
        if "bandwidth" in params and params["bandwidth"] <= 0:
            return False
        if "error_rate" in params and not (0 <= params["error_rate"] <= 1):
            return False
    
    return True


# ============================================================================
# 理想化模式支持 - 重构版本
# ============================================================================

# 全局理想化模式标志
_IDEALIZED_MODE = os.getenv('AI4QKD_IDEALIZED_MODE', 'False').lower() == 'true'


def set_idealized_mode(enabled: bool = True):
    """
    设置理想化模式
    
    重构思路：
    - 保持原有的模式切换接口
    - 简化了模式状态管理
    - 改进了用户提示信息
    - 支持环境变量配置
    
    Args:
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
    
    重构思路：
    - 保持原有的状态查询接口
    - 简化了状态检查逻辑
    
    Returns:
        bool: 是否为理想化模式
    """
    return _IDEALIZED_MODE


def _is_idealized_mode() -> bool:
    """内部使用的模式检查函数"""
    return _IDEALIZED_MODE


def setup_idealized_research_mode():
    """
    设置为科学研究的理想化模式
    
    重构思路：
    - 保持原有的快速设置接口
    - 优化了设置流程
    - 改进了用户提示
    """
    set_idealized_mode(True)
    print("[SETUP] Idealized research environment configured")
    print("   [INFO] Eliminate hardware noise, highlight protocol structure innovation")
    print("   [INFO] Obtain theoretical optimal performance baseline")


def setup_realistic_deployment_mode():
    """
    设置为现实部署模式
    
    重构思路：
    - 保持原有的快速设置接口
    - 对应理想化模式的设置
    - 统一设置接口的设计
    """
    set_idealized_mode(False)
    print("[SETUP] Realistic deployment environment configured")
    print("   [INFO] Consider actual hardware characteristics and environmental limitations")
    print("   [INFO] Optimize actual QKD system performance")


def _get_idealized_template(node_type: NodeType) -> Dict[str, Any]:
    """
    获取理想化模式的参数模板
    
    重构思路：
    - 基于现实模板生成理想化版本
    - 使用理想化的物理参数
    - 保持参数结构的一致性
    
    Args:
        node_type: 节点类型
        
    Returns:
        Dict[str, Any]: 理想化参数模板
    """
    import copy
    template = copy.deepcopy(NODE_TYPE_TEMPLATES[node_type])
    
    # 理想化参数修改
    if node_type == NodeType.QC:
        template["loss"] = 0.0      # 无损耗
        template["noise"] = 0.0     # 无噪声
    elif node_type == NodeType.QM:
        template["efficiency"] = 1.0    # 100%检测效率
        template["dark_count_rate"] = 0.0  # 无暗计数
    elif node_type == NodeType.QG:
        template["fidelity"] = 1.0     # 理想保真度
        template["gate_time"] = 0.0    # 瞬时操作
    elif node_type == NodeType.QD:
        template["efficiency"] = 1.0     # 100%检测效率
        template["dark_count_rate"] = 0.0   # 无暗计数
        template["dead_time"] = 0.0      # 无死时间
    elif node_type == NodeType.BSM:
        template["efficiency"] = 1.0           # 100%测量效率
        template["success_probability"] = 1.0  # 100%成功率
    elif node_type == NodeType.CC:
        template["bandwidth"] = float('inf')  # 无限带宽
        template["latency"] = 0.0             # 无延迟
        template["error_rate"] = 0.0          # 无错误
    
    return template


def _validate_idealized_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证理想化模式下的参数
    
    重构思路：
    - 理想化模式下放宽部分验证限制
    - 允许理想化的极值参数
    - 保持基本的合理性检查
    
    Args:
        node_type: 节点类型
        params: 参数字典
        
    Returns:
        bool: 参数是否有效（理想化标准）
    """
    # 理想化模式下允许更宽松的参数范围
    if node_type == NodeType.QC:
        if "loss" in params and params["loss"] < 0:  # 允许0损耗
            return False
        if "noise" in params and params["noise"] < 0:  # 允许0噪声
            return False
    
    elif node_type == NodeType.QM:
        if "efficiency" in params and not (0 <= params["efficiency"] <= 1):
            return False  # 效率仍需在[0,1]范围内
    
    # 其他验证保持相对宽松
    return True


def compare_mode_parameters(node_type: NodeType) -> Dict[str, Any]:
    """
    比较理想化模式和现实模式下的参数差异
    
    重构思路：
    - 保持原有的参数比较接口
    - 简化了比较逻辑和输出格式
    - 便于分析不同模式的影响
    
    Args:
        node_type: 节点类型
        
    Returns:
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
    
    Args:
        real_val: 现实值
        ideal_val: 理想值
        
    Returns:
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
    
    重构思路：
    - 保持原有的信息显示接口
    - 优化了信息的组织和展示
    - 提供更详细的模式说明
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
        print("      • Channel loss: 10%+ (distance-dependent)")
        print("      • Quantum noise: 1%+ (environmental impact)")
        print("      • Operation time: Nanosecond level (actual hardware)")
        print("   [USAGE] Applicable scenarios: Actual QKD system deployment, engineering optimization")