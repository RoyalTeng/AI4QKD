"""
量子-经典图流（QCGF）DSL模块

该模块提供了用于表示和操作量子密钥分发（QKD）协议结构的图流语言。
主要包含协议图数据结构、节点类型定义、边类型定义等核心组件。

主要组件：
- ProtocolGraph: 协议图核心数据结构
- Node: 协议节点类
- 各种节点类型（QSP, QC, QM, CLO等）
- 可视化工具
"""

from .protocol_graph import ProtocolGraph, Node
from .node_types import NodeType, Party, get_node_template
from .edge_types import EdgeType, Edge, get_edge_template
from .parser import QCGFParser, QCGFSerializer
from .compiler import QCGFCompiler
from .visualizer import ProtocolVisualizer, visualize_protocol

__version__ = "1.0.0"
__author__ = "AI4QKD Team"

__all__ = [
    # protocol_graph
    "ProtocolGraph",
    "Node",
    
    # node_types
    "NodeType",
    "Party",
    "get_node_template",
    
    # edge_types
    "EdgeType",
    "Edge",
    "get_edge_template",
    
    # parser
    "QCGFParser",
    "QCGFSerializer",
    
    # compiler
    "QCGFCompiler",
    
    # visualizer
    "ProtocolVisualizer",
    "visualize_protocol",
] 