"""
DSL解析器模块

实现了QCGF DSL的解析功能，支持从文本描述解析协议图结构。
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from .node_types import NodeType, Party, get_node_template, validate_node_params
from .edge_types import EdgeType, get_edge_template, validate_edge_params
from .protocol_graph import ProtocolGraph, Node
from enum import Enum


class QCGFParser:
    """
    QCGF DSL解析器
    
    支持解析文本格式的协议描述，转换为ProtocolGraph对象。
    """
    
    def __init__(self):
        """初始化解析器"""
        self.node_regex = re.compile(
            r"^(?P<type>[A-Z_]+)\s+(?P<id>\w+)\s*(?::\s*(?P<params>.+))?$"
        )
        self.edge_regex = re.compile(
            r"^(?P<source>\w+)\s*->\s*(?P<target>\w+)\s*\[(?P<type>\w+)\]\s*(?::\s*(?P<params>.+))?$"
        )
        self.param_regex = re.compile(r"(\w+)=('([^']*)'|\"([^\"]*)\"|([\w.-]+))")

    def _parse_params(self, param_str: Optional[str]) -> Dict[str, Any]:
        """解析参数字符串"""
        params = {}
        if not param_str:
            return params
        for match in self.param_regex.finditer(param_str):
            key = match.group(1)
            # a bit convoluted to get the value since it can be quoted or not
            value = match.group(3) or match.group(4) or match.group(5)
            try:
                # Try to convert to float or int
                if "." in value:
                    params[key] = float(value)
                else:
                    params[key] = int(value)
            except (ValueError, TypeError):
                # Otherwise, it's a string
                params[key] = value
        return params

    def parse(self, text: str) -> ProtocolGraph:
        """
        解析协议文本

        Args:
            text: 包含协议描述的字符串

        Returns:
            一个ProtocolGraph实例
        """
        graph = ProtocolGraph()
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]

        for line in lines:
            node_match = self.node_regex.match(line)
            edge_match = self.edge_regex.match(line)

            if node_match:
                data = node_match.groupdict()
                node_type = NodeType(data["type"])
                node_id = data["id"]
                params = self._parse_params(data.get("params"))
                party = Party(params["party"]) if "party" in params else None
                graph.add_node(node_type=node_type, node_id=node_id, params=params, party=party)
            elif edge_match:
                data = edge_match.groupdict()
                source_id = data["source"]
                target_id = data["target"]
                edge_type = EdgeType(data["type"])
                params = self._parse_params(data.get("params"))
                graph.add_edge(source_id, target_id, edge_type=edge_type, params=params)
            else:
                raise ValueError(f"Invalid DSL syntax on line: {line}")

        return graph

    def parse_from_file(self, filepath: str) -> ProtocolGraph:
        """
        从文件解析协议

        Args:
            filepath: 文件路径

        Returns:
            一个ProtocolGraph实例
        """
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        return self.parse(text)


class QCGFSerializer:
    """将ProtocolGraph序列化为DSL文本"""

    def serialize(self, graph: ProtocolGraph) -> str:
        """
        序列化协议图

        Args:
            graph: ProtocolGraph实例

        Returns:
            协议的DSL文本表示
        """
        lines = [f"# Protocol: {graph.name}\n"]

        lines.append("# Nodes")
        for node_id in sorted(graph.graph.nodes):
            node = graph.get_node(node_id)
            if node:
                # Make a copy of params to avoid modifying the original
                params_to_format = node.params.copy()
                if node.party:
                    # Add party to the params for formatting, ensuring it's not duplicated
                    params_to_format['party'] = node.party
                
                param_str = self._format_params(params_to_format)
                lines.append(f"{node.node_type.value} {node.node_id}" + (f": {param_str}" if param_str else ""))

        lines.append("\n# Edges")
        for source, target, data in sorted(graph.get_edges(), key=lambda x: (x[0], x[1])):
            param_str = self._format_params(data.get("params", {}))
            edge_type = data.get("edge_type", EdgeType.QUANTUM)
            lines.append(f"{source} -> {target} [{edge_type.value}]" + (f": {param_str}" if param_str else ""))
        
        return "\n".join(lines)

    def _format_params(self, params: Dict[str, Any]) -> str:
        """格式化参数字典为字符串"""
        if not params:
            return ""
        parts = []
        for key, value in sorted(params.items()):
            if isinstance(value, Enum):
                # Get the enum's value and quote it if it's a string
                val_str = f'"{value.value}"'
                parts.append(f'{key}={val_str}')
            elif isinstance(value, str):
                # Ensure all strings are quoted
                parts.append(f'{key}="{value}"')
            else:
                parts.append(f"{key}={value}")
        return ", ".join(parts)

    def serialize_to_file(self, graph: ProtocolGraph, filepath: str):
        """
        序列化协议图到文件

        Args:
            graph: ProtocolGraph实例
            filepath: 输出文件路径
        """
        text = self.serialize(graph)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)