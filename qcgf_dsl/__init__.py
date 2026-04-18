"""
量子-经典图流领域特定语言 (QCGF DSL)

QCGF DSL是专门为量子密钥分发协议设计的领域特定语言，
用于表示和分析量子-经典混合协议图结构。
"""

from .node_types import NodeType, Party, EdgeType
from .protocol_graph import ProtocolGraph
from .visualizer import visualize_protocol

__all__ = [
    'NodeType',
    'Party',
    'EdgeType', 
    'ProtocolGraph',
    'visualize_protocol'
]

__version__ = '1.0.0'