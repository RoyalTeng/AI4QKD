"""
协议图核心模块

实现了QCGF DSL的核心数据结构，包括：
- Node类：表示协议中的单个操作节点
- ProtocolGraph类：表示完整的协议图结构
- 支持添加、删除、查找、可视化等操作
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, List, Any, Optional, Tuple, Union
from enum import Enum
import uuid
import json

from .node_types import NodeType, Party, get_node_template, validate_node_params
from .edge_types import EdgeType, Edge


class Node:
    """
    协议节点类
    
    表示QKD协议中的一个操作节点，包含节点类型、参数、参与者等信息。
    """
    
    def __init__(self, 
                 node_id: str,
                 node_type: NodeType,
                 params: Optional[Dict[str, Any]] = None,
                 party: Optional[Party] = None,
                 position: Optional[Tuple[float, float]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        初始化节点
        
        Args:
            node_id: 节点唯一标识符
            node_type: 节点类型
            params: 节点参数字典
            party: 参与者
            position: 节点位置坐标 (x, y)
            metadata: 额外元数据
        """
        self.node_id = node_id
        self.node_type = node_type
        self.params = params if params is not None else {}
        self.party = party
        self.position = position or (0.0, 0.0)
        self.metadata = metadata or {}
        
        # 设置默认参数
        self._set_default_params()
        
        # 验证参数
        if not validate_node_params(node_type, self.params):
            raise ValueError(f"Invalid parameters for node type {node_type}")
    
    def _set_default_params(self):
        """设置默认参数"""
        template = get_node_template(self.node_type)
        for key, value in template.items():
            if key not in self.params:
                self.params[key] = value
        
        # 设置默认参与者
        if self.party is None and "party" in self.params:
            self.party = self.params["party"]
    
    def update_params(self, new_params: Dict[str, Any]):
        """
        更新节点参数
        
        Args:
            new_params: 新的参数字典
        """
        self.params.update(new_params)
        if not validate_node_params(self.node_type, self.params):
            raise ValueError(f"Invalid parameters for node type {self.node_type}")
    
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
    
    def is_quantum_node(self) -> bool:
        """判断是否为量子节点"""
        return NodeType.is_quantum_type(self.node_type)
    
    def is_classical_node(self) -> bool:
        """判断是否为经典节点"""
        return NodeType.is_classical_type(self.node_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """将节点转换为可序列化的字典"""
        # Create a copy of params to modify
        serializable_params = self.params.copy()
        # Ensure party in params is also a string value
        if 'party' in serializable_params and isinstance(serializable_params['party'], Party):
            serializable_params['party'] = serializable_params['party'].value

        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "params": serializable_params,
            "party": self.party.value if self.party else None,
            "position": self.position,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """
        从字典创建节点
        
        Args:
            data: 节点数据字典
            
        Returns:
            Node实例
        """
        return cls(
            node_id=data["node_id"],
            node_type=NodeType(data["node_type"]),
            params=data.get("params", {}),
            party=Party(data["party"]) if data.get("party") else None,
            position=data.get("position", (0.0, 0.0)),
            metadata=data.get("metadata", {})
        )
    
    def __str__(self) -> str:
        return f"Node({self.node_id}, {self.node_type.value}, {self.party.value if self.party else 'Unknown'})"
    
    def __repr__(self) -> str:
        return self.__str__()


class ProtocolGraph:
    """
    协议图类
    
    使用NetworkX实现的有向图，表示QKD协议的完整结构。
    支持节点的添加、删除、查找，边的管理，以及图的可视化。
    """
    
    def __init__(self, name: str = "QKD_Protocol"):
        """
        初始化协议图
        
        Args:
            name: 协议图名称
        """
        self.name = name
        self.graph = nx.DiGraph()
        self.node_counter = 0 # 只增不减的全局节点计数器
        
        # 节点类型统计
        self.node_stats = {node_type: 0 for node_type in NodeType}
        
        # 参与者统计
        self.party_stats = {party: 0 for party in Party}
    
    def add_node(self, 
                 node_type: NodeType,
                 params: Optional[Dict[str, Any]] = None,
                 party: Optional[Party] = None,
                 position: Optional[Tuple[float, float]] = None,
                 node_id: Optional[str] = None) -> str:
        """
        添加节点到协议图
        
        Args:
            node_type: 节点类型
            params: 节点参数
            party: 参与者
            position: 节点位置
            node_id: 节点ID（可选，如果为None，则自动生成唯一ID）
            
        Returns:
            节点ID
        """
        if node_id is None:
            # 使用全局计数器生成唯一ID
            node_id = f"{node_type.value.lower()}_{self.node_counter}"
            self.node_counter += 1
        
        # 检查节点ID是否已存在
        if self.has_node(node_id):
            raise ValueError(f"Node with ID {node_id} already exists")
        
        # 创建节点
        node = Node(
            node_id=node_id,
            node_type=node_type,
            params=params,
            party=party,
            position=position
        )
        
        # 添加到图中
        self.graph.add_node(node_id, node=node)
        
        # 更新统计
        self.node_stats[node_type] += 1
        if party:
            self.party_stats[party] += 1
        
        return node_id
    
    def remove_node(self, node_id: str) -> bool:
        """
        从协议图中删除节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            是否成功删除
        """
        if not self.has_node(node_id):
            return False
        
        # 获取节点信息用于统计更新
        node = self.get_node(node_id)
        if node:
            self.node_stats[node.node_type] -= 1
            if node.party:
                self.party_stats[node.party] -= 1
        
        # 删除节点（NetworkX会自动删除相关边）
        self.graph.remove_node(node_id)
        return True
    
    def add_edge(self, 
                 source_id: str,
                 target_id: str,
                 edge_type: EdgeType = EdgeType.QUANTUM,
                 params: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加边到协议图
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
            params: 边参数
            
        Returns:
            是否成功添加
        """
        if not self.has_node(source_id) or not self.has_node(target_id):
            return False
        
        # 检查是否形成环路
        if self._would_create_cycle(source_id, target_id):
            raise ValueError(f"Adding edge {source_id} -> {target_id} would create a cycle")
        
        # 添加边
        edge_data = {
            "edge_type": edge_type,
            "params": params or {}
        }
        self.graph.add_edge(source_id, target_id, **edge_data)
        return True
    
    def remove_edge(self, source_id: str, target_id: str) -> bool:
        """
        删除边
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            
        Returns:
            是否成功删除
        """
        if self.graph.has_edge(source_id, target_id):
            self.graph.remove_edge(source_id, target_id)
            return True
        return False
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """
        获取节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            Node实例或None
        """
        if self.has_node(node_id):
            return self.graph.nodes[node_id]["node"]
        return None
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        """
        根据类型获取节点列表
        
        Args:
            node_type: 节点类型
            
        Returns:
            节点列表
        """
        nodes = []
        for node_id, node_data in self.graph.nodes(data=True):
            node = node_data["node"]
            if node.node_type == node_type:
                nodes.append(node)
        return nodes
    
    def get_nodes_by_party(self, party: Party) -> List[Node]:
        """
        根据参与者获取节点列表
        
        Args:
            party: 参与者
            
        Returns:
            节点列表
        """
        nodes = []
        for node_id, node_data in self.graph.nodes(data=True):
            node = node_data["node"]
            if node.party == party:
                nodes.append(node)
        return nodes
    
    def get_neighbors(self, node_id: str, direction: str = "both") -> List[str]:
        """
        获取邻居节点
        
        Args:
            node_id: 节点ID
            direction: 方向 ("in", "out", "both")
            
        Returns:
            邻居节点ID列表
        """
        if not self.has_node(node_id):
            return []
        
        if direction == "in":
            return list(self.graph.predecessors(node_id))
        elif direction == "out":
            return list(self.graph.successors(node_id))
        else:  # both
            return list(self.graph.neighbors(node_id))
    
    def get_edges(self, node_id: str = None) -> List[Tuple[str, str, Dict]]:
        """
        获取边列表
        
        Args:
            node_id: 节点ID（可选，指定节点相关的边）
            
        Returns:
            边列表，每个元素为 (source, target, edge_data)
        """
        if node_id:
            edges = []
            for pred in self.graph.predecessors(node_id):
                edges.append((pred, node_id, self.graph.edges[pred, node_id]))
            for succ in self.graph.successors(node_id):
                edges.append((node_id, succ, self.graph.edges[node_id, succ]))
            return edges
        else:
            return list(self.graph.edges(data=True))
    
    def has_node(self, node_id: str) -> bool:
        """检查节点是否存在"""
        return self.graph.has_node(node_id)
    
    def has_edge(self, source_id: str, target_id: str) -> bool:
        """检查边是否存在"""
        return self.graph.has_edge(source_id, target_id)
    
    def get_node_count(self) -> int:
        """获取节点数量"""
        return self.graph.number_of_nodes()
    
    def get_edge_count(self) -> int:
        """获取边数量"""
        return self.graph.number_of_edges()
    
    def is_dag(self) -> bool:
        """检查是否为有向无环图"""
        return nx.is_directed_acyclic_graph(self.graph)
    
    def get_topological_order(self) -> List[str]:
        """获取图的拓扑排序"""
        if not self.is_dag():
            raise nx.NetworkXUnfeasible("图不是有向无环图（DAG），无法进行拓扑排序。")
        return list(nx.topological_sort(self.graph))
    
    def find_first_node_by_type(self, node_type: NodeType) -> Optional[Node]:
        """按拓扑顺序查找图中第一个指定类型的节点。"""
        for node_id in self.get_topological_order():
            node = self.get_node(node_id)
            if node and node.node_type == node_type:
                return node
        return None
    
    def _would_create_cycle(self, source_id: str, target_id: str) -> bool:
        """检查添加边是否会形成环路"""
        temp_graph = self.graph.copy()
        temp_graph.add_edge(source_id, target_id)
        return not nx.is_directed_acyclic_graph(temp_graph)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取协议图统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "name": self.name,
            "node_count": self.get_node_count(),
            "edge_count": self.get_edge_count(),
            "is_dag": self.is_dag(),
            "node_stats": {k.value: v for k, v in self.node_stats.items() if v > 0},
            "party_stats": {k.value: v for k, v in self.party_stats.items() if v > 0},
            "edge_types": self._get_edge_type_stats()
        }
    
    def _get_edge_type_stats(self) -> Dict[str, int]:
        """获取边类型统计"""
        edge_stats = {}
        for _, _, edge_data in self.graph.edges(data=True):
            edge_type = edge_data.get("edge_type", EdgeType.QUANTUM).value
            edge_stats[edge_type] = edge_stats.get(edge_type, 0) + 1
        return edge_stats
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将协议图转换为字典表示
        
        Returns:
            协议图字典表示
        """
        nodes = {}
        for node_id, node_data in self.graph.nodes(data=True):
            nodes[node_id] = node_data["node"].to_dict()
        
        edges = []
        for source, target, edge_data in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "edge_type": edge_data.get("edge_type", EdgeType.QUANTUM).value,
                "params": edge_data.get("params", {})
            })
        
        return {
            "name": self.name,
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "node_counter": self.node_counter,
                "node_stats": {k.value: v for k, v in self.node_stats.items()},
                "party_stats": {k.value: v for k, v in self.party_stats.items()}
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProtocolGraph':
        """
        从字典创建协议图
        
        Args:
            data: 协议图数据字典
            
        Returns:
            ProtocolGraph实例
        """
        graph = cls(data.get("name", "QKD_Protocol"))
        
        # 添加节点
        for node_id, node_data in data["nodes"].items():
            node = Node.from_dict(node_data)
            graph.graph.add_node(node_id, node=node)
            
            # 更新统计
            graph.node_stats[node.node_type] += 1
            if node.party:
                graph.party_stats[node.party] += 1
        
        # 添加边
        for edge_data in data["edges"]:
            source = edge_data["source"]
            target = edge_data["target"]
            edge_type = EdgeType(edge_data["edge_type"])
            params = edge_data.get("params", {})
            
            graph.graph.add_edge(source, target, edge_type=edge_type, params=params)
        
        # 恢复元数据
        metadata = data.get("metadata", {})
        graph.node_counter = metadata.get("node_counter", 0)
        
        return graph
    
    def save_to_file(self, filename: str):
        """
        保存协议图到文件
        
        Args:
            filename: 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'ProtocolGraph':
        """
        从文件加载协议图
        
        Args:
            filename: 文件名
            
        Returns:
            ProtocolGraph实例
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        stats = self.get_statistics()
        return f"ProtocolGraph({self.name}, nodes={stats['node_count']}, edges={stats['edge_count']})"
    
    def __repr__(self) -> str:
        return self.__str__() 