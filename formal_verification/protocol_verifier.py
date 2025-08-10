from dataclasses import dataclass, field
from typing import List, Dict, Any
from qcgf_dsl.protocol_graph import ProtocolGraph, EdgeType

@dataclass
class VerificationReport:
    """
    协议验证报告。
    """
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ProtocolVerifier:
    """
    协议验证器，用于检查协议图的结构合法性。
    """
    def verify(self, graph: ProtocolGraph) -> VerificationReport:
        """
        验证协议图的结构属性。

        Args:
            graph (ProtocolGraph): 要验证的协议图。

        Returns:
            VerificationReport: 包含验证结果的报告。
        """
        errors = []
        warnings = []

        # 1. 检查是否为有向无环图 (DAG)
        if not graph.is_dag():
            errors.append("协议图包含环路，不是一个有效的有向无环图 (DAG)。")

        # 2. 检查节点连接性
        if not graph.graph or not len(graph.graph.nodes):
             errors.append("协议图为空，没有任何节点。")
        else:
            if not all(graph.graph.degree(n) > 0 for n in graph.graph.nodes()):
                warnings.append("协议图中存在孤立节点（未连接到任何其他节点）。")

        # 3. 检查信息流方向（简化版）
        # 示例：量子信道不应指向量子态制备节点
        for u, v, data in graph.get_edges():
            source_node = graph.get_node(u)
            target_node = graph.get_node(v)
            edge_type = data.get("edge_type", EdgeType.QUANTUM)

            if edge_type == EdgeType.QUANTUM and target_node.node_type.name == 'QSP':
                errors.append(f"信息流错误：量子信道 ({u} -> {v}) 不能指向量子态制备节点 (QSP)。")

        is_valid = not errors
        
        report = VerificationReport(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            metadata={"node_count": graph.get_node_count(), "edge_count": graph.get_edge_count()}
        )
        return report 