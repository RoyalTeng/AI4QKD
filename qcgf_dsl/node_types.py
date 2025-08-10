"""
节点类型定义模块

定义了QCGF DSL中支持的各种节点类型，包括量子操作和经典操作。
支持理想化模式和现实模式的参数切换。
"""

from enum import Enum
from typing import Dict, Any, Optional, List
import os


class NodeType(Enum):
    """
    节点类型枚举
    
    定义了QCGF DSL中支持的各种节点类型：
    - QSP: 量子态准备 (Quantum State Preparation)
    - QC: 量子信道 (Quantum Channel) 
    - QM: 量子测量 (Quantum Measurement)
    - CLO: 经典逻辑操作 (Classical Logic Operation)
    - QG: 量子门 (Quantum Gate)
    - QD: 量子检测器 (Quantum Detector)
    - CS: 经典存储 (Classical Storage)
    - CC: 经典信道 (Classical Channel)
    - BSM: 贝尔态测量 (Bell State Measurement)
    """
    
    # 量子操作节点
    QSP = "QSP"  # 量子态准备
    QC = "QC"    # 量子信道
    QM = "QM"    # 量子测量
    QG = "QG"    # 量子门
    QD = "QD"    # 量子检测器
    BSM = "BSM"  # 贝尔态测量
    
    # 经典操作节点
    CLO = "CLO"  # 经典逻辑操作
    CS = "CS"    # 经典存储
    CC = "CC"    # 经典信道
    
    # 特殊节点
    ATTACK = "ATTACK"  # 攻击节点（用于安全分析）
    SINK = "SINK"      # 汇聚节点
    
    @classmethod
    def get_quantum_types(cls) -> list:
        """获取所有量子操作节点类型"""
        return [cls.QSP, cls.QC, cls.QM, cls.QG, cls.QD, cls.BSM]
    
    @classmethod
    def get_classical_types(cls) -> list:
        """获取所有经典操作节点类型"""
        return [cls.CLO, cls.CS, cls.CC]
    
    @classmethod
    def is_quantum_type(cls, node_type) -> bool:
        """判断是否为量子操作节点类型"""
        return node_type in cls.get_quantum_types()
    
    @classmethod
    def is_classical_type(cls, node_type) -> bool:
        """判断是否为经典操作节点类型"""
        return node_type in cls.get_classical_types()


class Intensity(Enum):
    """
    光源强度类型枚举，用于诱骗态协议。
    """
    SIGNAL = "signal"   # 信号态
    DECOY = "decoy"     # 诱骗态
    VACUUM = "vacuum"   # 真空态


class Party(Enum):
    """
    参与者枚举
    
    定义了协议中的主要参与者：
    - Alice: 发送方
    - Bob: 接收方  
    - Eve: 窃听者
    - Charlie: 第三方（如MDI-QKD中的测量方）
    """
    
    ALICE = "Alice"
    BOB = "Bob"
    EVE = "Eve"
    CHARLIE = "Charlie"
    UNKNOWN = "Unknown"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


# 节点类型默认参数模板
NODE_TYPE_TEMPLATES = {
    NodeType.QSP: {
        "state": "|0⟩",
        "fidelity": 0.99,
        "preparation_time": 1e-9,
        "party": Party.ALICE
    },
    NodeType.QC: {
        "loss": 0.1,
        "noise": 0.01,
        "distance": 50.0,
        "channel_type": "optical_fiber"
    },
    NodeType.QM: {
        "basis": "computational",
        "efficiency": 0.8,
        "dark_count_rate": 1e-6,
        "party": Party.BOB
    },
    NodeType.QG: {
        "gate_type": "H",
        "fidelity": 0.99,
        "gate_time": 1e-9
    },
    NodeType.QD: {
        "detector_type": "SPAD",
        "efficiency": 0.8,
        "dark_count_rate": 1e-6,
        "dead_time": 1e-6
    },
    NodeType.CLO: {
        "operation": "XOR",
        "processing_time": 1e-9,
        "party": Party.ALICE
    },
    NodeType.CS: {
        "storage_type": "memory",
        "capacity": 1000,
        "access_time": 1e-9
    },
    NodeType.CC: {
        "bandwidth": 1e9,
        "latency": 1e-6,
        "error_rate": 1e-9
    },
    NodeType.ATTACK: {
        "attack_type": "intercept_resend",
        "intercept_probability": 0.5,
        "party": Party.EVE
    },
    NodeType.SINK: {
        "sink_type": "key_generation",
        "party": Party.BOB
    },
    NodeType.BSM: {
        "efficiency": 0.5, # 贝尔态测量效率
        "party": Party.CHARLIE
    }
}


def get_node_template(node_type: NodeType) -> Dict[str, Any]:
    """
    获取指定节点类型的默认参数模板
    
    Args:
        node_type: 节点类型
        
    Returns:
        包含默认参数的字典
    """
    return NODE_TYPE_TEMPLATES.get(node_type, {}).copy()


def validate_node_params(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    验证节点参数的有效性
    
    Args:
        node_type: 节点类型
        params: 参数字典
        
    Returns:
        参数是否有效
    """
    template = get_node_template(node_type)
    
    # 基本验证：检查必需参数
    required_params = {
        NodeType.QSP: ["state"],
        NodeType.QC: ["loss"],
        NodeType.QM: ["basis"],
        NodeType.QG: ["gate_type"],
        NodeType.QD: ["detector_type"],
        NodeType.CLO: ["operation"],
        NodeType.CS: ["storage_type"],
        NodeType.CC: ["bandwidth"],
        NodeType.ATTACK: ["attack_type"],
        NodeType.SINK: ["sink_type"],
        NodeType.BSM: ["efficiency"]
    }
    
    if node_type in required_params:
        for param in required_params[node_type]:
            if param not in params:
                return False
    
    # 数值范围验证
    if node_type == NodeType.QC:
        if "loss" in params and not (0 <= params["loss"] <= 1):
            return False
        if "noise" in params and not (0 <= params["noise"] <= 1):
            return False
    
    if node_type == NodeType.QM:
        if "efficiency" in params and not (0 <= params["efficiency"] <= 1):
            return False
    
    return True


# ============================================================================
# 理想化模式支持
# ============================================================================

# 全局理想化模式标志
_IDEALIZED_MODE = os.getenv('AI4QKD_IDEALIZED_MODE', 'False').lower() == 'true'

def set_idealized_mode(enabled: bool = True):
    """
    设置理想化模式
    
    Args:
        enabled: 是否启用理想化模式
    """
    global _IDEALIZED_MODE
    _IDEALIZED_MODE = enabled
    print(f"🔬 AI4QKD理想化模式: {'已启用' if enabled else '已禁用'}")
    if enabled:
        print("   📌 使用理想化参数（探测效率100%，无噪声，瞬时操作）")
        print("   🎯 专注于协议设计算法的原理验证")
    else:
        print("   📌 使用现实参数（考虑硬件限制和环境噪声）")

def is_idealized_mode() -> bool:
    """检查当前是否为理想化模式"""
    return _IDEALIZED_MODE

def get_node_template_with_mode(node_type: NodeType) -> Dict[str, Any]:
    """
    根据当前模式获取节点参数模板
    
    Args:
        node_type: 节点类型
        
    Returns:
        节点参数模板字典
    """
    if _IDEALIZED_MODE:
        try:
            # 尝试导入理想化参数
            from config.idealized_parameters import IDEALIZED_NODE_TEMPLATES
            template = IDEALIZED_NODE_TEMPLATES.get(node_type, {}).copy()
            if template:
                return template
            print(f"⚠️ 警告：未找到{node_type}的理想化参数，使用默认参数")
        except ImportError:
            print("⚠️ 警告：无法导入理想化参数配置，使用默认参数")
    
    # 使用默认参数
    return get_node_template(node_type)

# 重写get_node_template函数以支持模式切换
def get_node_template(node_type: NodeType) -> Dict[str, Any]:
    """
    获取指定节点类型的参数模板（支持理想化模式）
    
    Args:
        node_type: 节点类型
        
    Returns:
        包含参数的字典
    """
    if _IDEALIZED_MODE:
        return get_node_template_with_mode(node_type)
    else:
        return NODE_TYPE_TEMPLATES.get(node_type, {}).copy()

def validate_node_params_with_mode(node_type: NodeType, params: Dict[str, Any]) -> bool:
    """
    根据当前模式验证节点参数的有效性
    
    Args:
        node_type: 节点类型
        params: 参数字典
        
    Returns:
        参数是否有效
    """
    # 在理想化模式下，放松一些验证限制
    if _IDEALIZED_MODE:
        # 基本验证：检查必需参数（理想化模式下某些参数可选）
        relaxed_required_params = {
            NodeType.QSP: ["state"],
            NodeType.QC: [],  # 理想化模式下loss可以为0
            NodeType.QM: ["basis"],
            NodeType.QG: ["gate_type"],
            NodeType.QD: ["detector_type"],
            NodeType.CLO: ["operation"],
            NodeType.CS: ["storage_type"],
            NodeType.CC: [],  # 理想化模式下bandwidth可以为无限
            NodeType.ATTACK: ["attack_type"],
            NodeType.SINK: ["sink_type"],
            NodeType.BSM: []  # 理想化模式下efficiency可以为1.0
        }
        
        if node_type in relaxed_required_params:
            for param in relaxed_required_params[node_type]:
                if param not in params:
                    return False
        
        # 理想化模式下允许特殊值
        if node_type == NodeType.QC:
            if "loss" in params and params["loss"] < 0:  # 允许0
                return False
            if "noise" in params and params["noise"] < 0:  # 允许0
                return False
        
        if node_type == NodeType.QM:
            if "efficiency" in params and not (0 <= params["efficiency"] <= 1):
                return False
        
        return True
    else:
        # 现实模式下使用原有的严格验证
        return validate_node_params(node_type, params)

# 提供便捷的配置函数
def setup_idealized_research_mode():
    """
    设置AI4QKD为科学研究的理想化模式
    
    该模式下：
    - 探测效率 = 100%
    - 信道损耗 = 0
    - 噪声 = 0  
    - 处理时间 = 0
    - 专注于协议设计算法的原理验证
    """
    set_idealized_mode(True)
    print("🧬 科学研究模式已启动")
    print("   ✨ 理想化物理参数已加载")
    print("   🔍 专注于AI协议设计算法验证")
    print("   📊 消除硬件噪声，突出协议结构影响")

def setup_realistic_deployment_mode():
    """
    设置AI4QKD为现实部署模式
    
    该模式下：
    - 使用真实硬件参数
    - 考虑噪声和损耗
    - 面向实际部署优化
    """
    set_idealized_mode(False)
    print("⚙️ 现实部署模式已启动")
    print("   📡 真实硬件参数已加载")
    print("   🌍 考虑环境噪声和硬件限制")
    print("   🚀 面向实际QKD系统部署")

# 参数比较和分析功能
def compare_mode_parameters(node_type: NodeType) -> Dict[str, Any]:
    """
    比较理想化模式和现实模式下的参数差异
    
    Args:
        node_type: 节点类型
        
    Returns:
        参数比较结果
    """
    # 获取现实参数
    realistic_params = NODE_TYPE_TEMPLATES.get(node_type, {}).copy()
    
    # 获取理想化参数
    try:
        from config.idealized_parameters import IDEALIZED_NODE_TEMPLATES
        idealized_params = IDEALIZED_NODE_TEMPLATES.get(node_type, {}).copy()
    except ImportError:
        idealized_params = {}
    
    return {
        "node_type": node_type.value,
        "realistic_params": realistic_params,
        "idealized_params": idealized_params,
        "key_differences": _analyze_parameter_differences(realistic_params, idealized_params)
    }

def _analyze_parameter_differences(realistic: Dict, idealized: Dict) -> List[str]:
    """分析参数差异"""
    differences = []
    
    for key in set(realistic.keys()) | set(idealized.keys()):
        real_val = realistic.get(key, "未设置")
        ideal_val = idealized.get(key, "未设置")
        
        if real_val != ideal_val:
            differences.append(f"{key}: {real_val} → {ideal_val}")
    
    return differences

def print_current_mode_info():
    """打印当前模式的信息"""
    if _IDEALIZED_MODE:
        print("🔬 当前模式：理想化科学研究模式")
        print("   目标：验证AI协议设计算法的原理有效性")
        print("   特点：消除硬件限制，专注算法创新")
    else:
        print("⚙️ 当前模式：现实部署模式") 
        print("   目标：优化面向实际部署的QKD协议")
        print("   特点：考虑硬件限制，追求实用性能")