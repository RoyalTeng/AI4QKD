"""
AI4QKD - qcgf_dsl模块初始化文件

重构思路：
- 参考GitHub master分支的qcgf_dsl/__init__.py实现思路
- 保持原有模块导入接口的向后兼容性
- 简化了模块结构，减少不必要的抽象层
- 统一了模块对外接口的设计

设计原则：
- 清晰的模块边界定义
- 统一的对外接口暴露
- 简化的导入关系
- 完整的功能覆盖

主要改进：
- 减少了循环导入的可能性
- 简化了模块初始化逻辑
- 统一了版本和作者信息管理
- 改进了模块文档结构

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 qcgf_dsl/__init__.py
"""

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的qcgf_dsl/__init__.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化模块结构，提高可维护性和性能
# 主要改进: 统一导入接口，减少抽象层，改进文档结构
# 参考文件: qcgf_dsl/__init__.py
# =============================================================================

# 版本信息
__version__ = "2.0.0"  # 重构版本
__author__ = "AI4QKD Team (Refactored)"
__description__ = "量子-经典图流（QCGF）DSL - 重构版本"

# 核心组件导入（保持向后兼容性）
from .node_types import (
    NodeType,
    Party, 
    get_node_template,
    validate_node_params,
    # 理想化模式支持
    set_idealized_mode,
    is_idealized_mode,
    setup_idealized_research_mode,
    setup_realistic_deployment_mode
)

from .edge_types import (
    EdgeType,
    EdgeDirection,
    Edge,
    get_edge_template,
    validate_edge_params
)

from .protocol_graph import (
    ProtocolGraph,
    Node
)

from .parser import (
    QCGFParser,
    QCGFSerializer
)

from .visualizer import (
    ProtocolVisualizer,
    visualize_protocol
)

from .compiler import (
    QCGFCompiler,
    compile_protocol,
    compile_to_file
)

# 公共接口定义（保持与原版兼容）
__all__ = [
    # 版本和元信息
    "__version__",
    "__author__", 
    "__description__",
    
    # 核心数据结构
    "ProtocolGraph",
    "Node",
    "Edge",
    
    # 类型系统
    "NodeType",
    "Party",
    "EdgeType", 
    "EdgeDirection",
    
    # 参数管理
    "get_node_template",
    "validate_node_params",
    "get_edge_template",
    "validate_edge_params",
    
    # 理想化模式支持
    "set_idealized_mode",
    "is_idealized_mode", 
    "setup_idealized_research_mode",
    "setup_realistic_deployment_mode",
    
    # DSL解析和序列化
    "QCGFParser",
    "QCGFSerializer",
    
    # 可视化
    "ProtocolVisualizer",
    "visualize_protocol",
    
    # 代码生成
    "QCGFCompiler",
    "compile_protocol",
    "compile_to_file",
    
    # 便捷功能函数
    "create_bb84_protocol",
    "create_mdi_qkd_protocol",
    "parse_protocol_from_string",
    "save_protocol_to_file",
    "load_protocol_from_file"
]

# 便捷功能函数（新增）
def create_bb84_protocol():
    """
    创建标准BB84协议的便捷函数 - 严格按照研究方案重构
    
    重构思路：
    - 基于研究方案的节点和边类型定义
    - 使用重构后的标准类型（QF代替QUANTUM）
    - 创建符合研究方案的BB84协议结构
    
    返回值：
        ProtocolGraph: 配置好的BB84协议图
    """
    protocol = ProtocolGraph("BB84_Protocol")
    
    # Alice方：量子态准备 (QSP)
    alice_qsp = protocol.add_node(
        node_type=NodeType.QSP,
        party=Party.ALICE,
        params={"intensity": 0.1, "polarization": "H"}
    )
    
    # 量子信道 (QC)
    quantum_channel = protocol.add_node(
        node_type=NodeType.QC,
        params={"length": 50.0, "loss_per_unit": 0.2}
    )
    
    # Bob方：量子测量 (QM)
    bob_qm = protocol.add_node(
        node_type=NodeType.QM,
        party=Party.BOB,
        params={"detector_efficiency": 0.8, "basis_id": 0}
    )
    
    # 经典信息源 (Alice的随机比特) 
    alice_cis = protocol.add_node(
        node_type=NodeType.CIS,
        party=Party.ALICE,
        params={"length": 1000}
    )
    
    # 密钥提取 (Bob方)
    bob_ke = protocol.add_node(
        node_type=NodeType.KE,
        party=Party.BOB,
        params={"key_length": 256}
    )
    
    # 构建连接 - 使用研究方案定义的边类型
    protocol.add_edge(alice_qsp, quantum_channel, EdgeType.QF)  # 量子流
    protocol.add_edge(quantum_channel, bob_qm, EdgeType.QF)    # 量子流
    protocol.add_edge(bob_qm, bob_ke, EdgeType.QCIF)          # 量子-经典接口流
    protocol.add_edge(alice_cis, bob_ke, EdgeType.CF)         # 经典流
    
    return protocol


def create_mdi_qkd_protocol():
    """
    创建标准MDI-QKD协议的便捷函数 - 严格按照研究方案重构
    
    重构思路：
    - 基于研究方案的节点类型定义
    - 使用QI (量子干涉) 代替已删除的BSM类型
    - 创建符合研究方案的MDI-QKD协议结构
    
    返回值：
        ProtocolGraph: 配置好的MDI-QKD协议图
    """
    protocol = ProtocolGraph("MDI_QKD_Protocol")
    
    # Alice方：量子态准备 (QSP)
    alice_qsp = protocol.add_node(
        node_type=NodeType.QSP,
        party=Party.ALICE,
        params={"intensity": 0.1, "polarization": "D"}
    )
    
    # Bob方：量子态准备 (QSP)
    bob_qsp = protocol.add_node(
        node_type=NodeType.QSP,
        party=Party.BOB, 
        params={"intensity": 0.1, "polarization": "D"}
    )
    
    # Charlie方：量子干涉测量 (QI - Bell态测量的抽象)
    charlie_qi = protocol.add_node(
        node_type=NodeType.QI,
        party=Party.CHARLIE,
        params={"input_qubits": [0, 1], "reflectivity": 0.5}
    )
    
    # Charlie的量子测量 (QM)
    charlie_qm = protocol.add_node(
        node_type=NodeType.QM,
        party=Party.CHARLIE,
        params={"detector_efficiency": 0.8}
    )
    
    # 密钥提取节点
    alice_ke = protocol.add_node(
        node_type=NodeType.KE,
        party=Party.ALICE,
        params={"key_length": 256}
    )
    
    bob_ke = protocol.add_node(
        node_type=NodeType.KE,
        party=Party.BOB,
        params={"key_length": 256}
    )
    
    # 构建连接 - 使用研究方案定义的边类型
    protocol.add_edge(alice_qsp, charlie_qi, EdgeType.QF)     # Alice量子流到Charlie
    protocol.add_edge(bob_qsp, charlie_qi, EdgeType.QF)       # Bob量子流到Charlie
    protocol.add_edge(charlie_qi, charlie_qm, EdgeType.QF)    # 干涉结果到测量
    protocol.add_edge(charlie_qm, alice_ke, EdgeType.QCIF)    # 测量结果到Alice密钥
    protocol.add_edge(charlie_qm, bob_ke, EdgeType.QCIF)      # 测量结果到Bob密钥
    
    return protocol


def parse_protocol_from_string(dsl_text: str) -> ProtocolGraph:
    """
    从DSL字符串解析协议的便捷函数
    
    重构思路：
    - 简化DSL解析的调用接口
    - 提供统一的错误处理
    - 基于原有解析器功能封装
    
    参数：
        dsl_text: DSL格式的协议描述文本
        
    返回值：
        ProtocolGraph: 解析后的协议图
        
    异常：
        ValueError: DSL语法错误时抛出
    """
    parser = QCGFParser()
    return parser.parse(dsl_text)


def save_protocol_to_file(protocol: ProtocolGraph, filepath: str, format_type: str = "json"):
    """
    保存协议到文件的便捷函数
    
    重构思路：
    - 支持多种文件格式的保存
    - 统一的文件操作接口
    - 基于原有序列化功能扩展
    
    参数：
        protocol: 要保存的协议图
        filepath: 文件路径
        format_type: 文件格式 ("json", "dsl")
        
    异常：
        ValueError: 不支持的文件格式
        IOError: 文件写入错误
    """
    if format_type == "json":
        protocol.save_to_file(filepath)
    elif format_type == "dsl":
        serializer = QCGFSerializer()
        serializer.serialize_to_file(protocol, filepath)
    else:
        raise ValueError(f"不支持的格式: {format_type}")


def load_protocol_from_file(filepath: str) -> ProtocolGraph:
    """
    从文件加载协议的便捷函数
    
    重构思路：
    - 自动检测文件格式
    - 统一的文件加载接口
    - 基于文件扩展名选择解析器
    
    参数：
        filepath: 文件路径
        
    返回值：
        ProtocolGraph: 加载的协议图
        
    异常：
        ValueError: 不支持的文件格式
        IOError: 文件读取错误
    """
    import os
    
    _, ext = os.path.splitext(filepath)
    
    if ext.lower() == ".json":
        return ProtocolGraph.load_from_file(filepath)
    elif ext.lower() in [".qcgf", ".dsl", ".txt"]:
        parser = QCGFParser()
        return parser.parse_from_file(filepath)
    else:
        raise ValueError(f"不支持的文件扩展名: {ext}")


# 模块级别的配置检查
def _check_dependencies():
    """
    检查模块依赖的可用性
    
    重构思路：
    - 在模块加载时检查关键依赖
    - 提供友好的错误信息
    - 支持可选依赖的优雅降级
    """
    import sys
    import warnings
    
    # 检查networkx（核心依赖）
    try:
        import networkx
    except ImportError:
        raise ImportError("协议图功能需要NetworkX库，请安装NetworkX")
    
    # 检查matplotlib（可选，用于可视化）
    try:
        import matplotlib
    except ImportError:
        warnings.warn("Matplotlib不可用 - 可视化功能已禁用", ImportWarning)
    
    # 检查qiskit（可选，用于代码生成）
    try:
        import qiskit
    except ImportError:
        warnings.warn("Qiskit不可用 - 代码生成功能受限", ImportWarning)


# 执行依赖检查
_check_dependencies()