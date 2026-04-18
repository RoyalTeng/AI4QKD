"""
协议图核心模块 - 简化版
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
import json
from dataclasses import dataclass, field

from .node_types import NodeType, Party


@dataclass
class Node:
    """协议节点"""
    node_id: str
    node_type: NodeType
    params: Dict[str, Any]
    party: Optional[Party] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass  
class Edge:
    """协议边"""
    source_id: str
    target_id: str
    edge_type: str = "quantum"
    params: Dict[str, Any] = field(default_factory=dict)


class ProtocolGraph:
    """协议图类"""
    
    def __init__(self, name: str = "Unnamed Protocol"):
        self.name = name
        self.graph = nx.DiGraph()
        self.node_counter = 0
    
    def add_node(self, node_type: NodeType, params=None, party=None, node_id=None):
        """添加节点"""
        if node_id is None:
            node_id = f"node_{self.node_counter}"
            self.node_counter += 1
        
        if params is None:
            params = {}
        
        node = Node(node_id=node_id, node_type=node_type, params=params, party=party)
        self.graph.add_node(node_id, node=node)
        return node_id
    
    def add_edge(self, source_id: str, target_id: str, edge_type="quantum", params=None):
        """添加边"""
        if params is None:
            params = {}
        
        edge = Edge(source_id=source_id, target_id=target_id, edge_type=edge_type, params=params)
        self.graph.add_edge(source_id, target_id, edge=edge)
    
    def get_node_count(self):
        """获取节点数"""
        return self.graph.number_of_nodes()
    
    def get_edge_count(self):
        """获取边数"""
        return self.graph.number_of_edges()
    
    def get_statistics(self):
        """获取统计信息"""
        node_stats = {}
        party_stats = {}
        
        for node_id in self.graph.nodes():
            node = self.graph.nodes[node_id]['node']
            node_type = node.node_type.value
            node_stats[node_type] = node_stats.get(node_type, 0) + 1
            
            if node.party:
                party = node.party.value
                party_stats[party] = party_stats.get(party, 0) + 1
        
        return {
            'name': self.name,
            'node_count': self.get_node_count(),
            'edge_count': self.get_edge_count(),
            'node_stats': node_stats,
            'party_stats': party_stats
        }
    
    @classmethod
    def create_bb84(cls):
        """创建BB84协议"""
        protocol = cls(name="BB84 Protocol")
        
        # Alice的量子态制备
        alice_qsp = protocol.add_node(
            node_type=NodeType.QSP,
            params={'state': '|+⟩', 'basis': 'X'},
            party=Party.ALICE,
            node_id='Alice_QSP'
        )
        
        # 量子信道
        quantum_channel = protocol.add_node(
            node_type=NodeType.QC,
            params={'loss': 0.1},
            node_id='QuantumChannel'
        )
        
        # Bob的测量
        bob_qm = protocol.add_node(
            node_type=NodeType.QM,
            params={'basis': 'X'},
            party=Party.BOB,
            node_id='Bob_QM'
        )
        
        # 经典信道
        classical_channel = protocol.add_node(
            node_type=NodeType.CC,
            params={'capacity': 1.0},
            node_id='ClassicalChannel'
        )
        
        # 添加边
        protocol.add_edge(alice_qsp, quantum_channel)
        protocol.add_edge(quantum_channel, bob_qm)
        protocol.add_edge(alice_qsp, classical_channel, edge_type='classical')
        protocol.add_edge(bob_qm, classical_channel, edge_type='classical')
        
        return protocol
    
    def save_to_file(self, filepath: str):
        """保存到文件"""
        data = {
            'name': self.name,
            'nodes': [],
            'edges': []
        }
        
        for node_id in self.graph.nodes():
            node = self.graph.nodes[node_id]['node']
            data['nodes'].append({
                'node_id': node.node_id,
                'node_type': node.node_type.value,
                'params': node.params,
                'party': node.party.value if node.party else None
            })
        
        for source_id, target_id in self.graph.edges():
            edge = self.graph.edges[source_id, target_id]['edge']
            data['edges'].append({
                'source_id': edge.source_id,
                'target_id': edge.target_id,
                'edge_type': edge.edge_type,
                'params': edge.params
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)