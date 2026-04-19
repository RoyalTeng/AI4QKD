"""
增强版混合智能体 - 支持MDI-QKD实验
"""

import random
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from simulator import QuantumSimulator


@dataclass
class EnhancedAgentConfig:
    """增强智能体配置"""
    population_size: int = 20
    mutation_rate: float = 0.3
    crossover_rate: float = 0.2
    max_iterations: int = 100
    elite_size: int = 2


class EnhancedHybridAgent:
    """增强版混合智能体"""
    
    def __init__(self, config=None):
        self.config = config or EnhancedAgentConfig()
        self.simulator = QuantumSimulator()
        self.population = []
        self.best_protocol = None
        self.best_fitness = 0
    
    def generate_random_protocol(self, name_prefix="Random") -> ProtocolGraph:
        """生成随机协议"""
        protocol = ProtocolGraph(name=f"{name_prefix}_Protocol_{random.randint(1000, 9999)}")
        
        # 随机节点数
        num_nodes = random.randint(4, 10)
        
        # 可能的节点类型
        available_types = [
            NodeType.QSP, NodeType.QC, NodeType.QM, 
            NodeType.CC, NodeType.CP
        ]
        
        # 可能的参与方
        available_parties = [Party.ALICE, Party.BOB, Party.CHARLIE, None]
        
        # 添加节点
        node_ids = []
        for i in range(num_nodes):
            node_type = random.choice(available_types)
            party = random.choice(available_parties)
            
            params = {}
            if node_type == NodeType.QSP:
                params = {
                    'state': random.choice(['|0⟩', '|1⟩', '|+⟩', '|-⟩']),
                    'basis': random.choice(['Z', 'X']),
                    'intensity': random.uniform(0.5, 1.0)
                }
            elif node_type == NodeType.QC:
                params = {
                    'loss': random.uniform(0.05, 0.3),
                    'noise': random.uniform(0.01, 0.1)
                }
            elif node_type == NodeType.QM:
                params = {
                    'basis': random.choice(['Z', 'X']),
                    'efficiency': random.uniform(0.6, 0.9)
                }
            elif node_type == NodeType.CC:
                params = {
                    'capacity': random.uniform(0.5, 2.0),
                    'reliability': random.uniform(0.9, 1.0)
                }
            elif node_type == NodeType.CP:
                params = {
                    'operation': random.choice(['sifting', 'xor', 'hash', 'privacy_amplification'])
                }
            
            node_id = protocol.add_node(node_type=node_type, params=params, party=party)
            node_ids.append(node_id)
        
        # 添加边（确保基本连通性）
        if len(node_ids) > 1:
            # 创建基本链
            for i in range(len(node_ids) - 1):
                edge_type = random.choice([EdgeType.QUANTUM, EdgeType.CLASSICAL])
                protocol.add_edge(node_ids[i], node_ids[i + 1], edge_type=edge_type)
            
            # 添加一些随机边
            extra_edges = random.randint(0, min(5, num_nodes))
            for _ in range(extra_edges):
                source = random.choice(node_ids)
                target = random.choice(node_ids)
                if source != target and not protocol.graph.has_edge(source, target):
                    edge_type = random.choice([EdgeType.QUANTUM, EdgeType.CLASSICAL])
                    protocol.add_edge(source, target, edge_type=edge_type)
        
        return protocol
    
    def evaluate_protocol(self, protocol: ProtocolGraph) -> float:
        """评估协议适应度"""
        try:
            result = self.simulator.simulate(protocol, pulse_count=5000)
            # 适应度：最大化增益，最小化QBER，考虑密钥率
            fitness = result.gain * (1 - result.qber) * result.raw_key_rate
            return max(0.0, min(fitness, 1.0))
        except Exception as e:
            # 如果仿真失败，返回低适应度
            return 0.01
    
    def mutate_protocol(self, protocol: ProtocolGraph) -> ProtocolGraph:
        """变异操作"""
        mutated = ProtocolGraph(name=f"{protocol.name}_mutated")
        
        # 复制所有节点
        node_mapping = {}
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            new_id = mutated.add_node(
                node_type=node.node_type,
                params=node.params.copy(),
                party=node.party
            )
            node_mapping[node_id] = new_id
        
        # 复制所有边
        for source_id, target_id in protocol.graph.edges():
            edge = protocol.graph.edges[source_id, target_id]['edge']
            mutated.add_edge(
                node_mapping[source_id],
                node_mapping[target_id],
                edge_type=edge.edge_type,
                params=edge.params.copy()
            )
        
        # 随机选择变异操作
        mutation_ops = [
            self._mutate_node_params,
            self._add_random_node,
            self._remove_random_node,
            self._add_random_edge,
            self._remove_random_edge,
            self._change_edge_type
        ]
        
        # 应用1-3个变异操作
        num_mutations = random.randint(1, 3)
        for _ in range(num_mutations):
            mutation_op = random.choice(mutation_ops)
            mutation_op(mutated)
        
        return mutated
    
    def _mutate_node_params(self, protocol: ProtocolGraph):
        """变异节点参数"""
        if not protocol.graph.nodes():
            return
        
        node_id = random.choice(list(protocol.graph.nodes()))
        node = protocol.graph.nodes[node_id]['node']
        
        if node.params:
            param_name = random.choice(list(node.params.keys()))
            if isinstance(node.params[param_name], (int, float)):
                # 数值参数：随机扰动
                current = node.params[param_name]
                if param_name in ['loss', 'noise', 'qber']:
                    # 这些参数应该小
                    node.params[param_name] = max(0.001, current * random.uniform(0.5, 1.5))
                else:
                    node.params[param_name] = max(0.01, current * random.uniform(0.8, 1.2))
            elif isinstance(node.params[param_name], str):
                # 字符串参数：从选项中随机选择
                if param_name == 'basis':
                    node.params[param_name] = random.choice(['Z', 'X', 'Bell'])
                elif param_name == 'state':
                    node.params[param_name] = random.choice(['|0⟩', '|1⟩', '|+⟩', '|-⟩'])
                elif param_name == 'operation':
                    node.params[param_name] = random.choice(['sifting', 'xor', 'hash', 'privacy_amplification'])
    
    def _add_random_node(self, protocol: ProtocolGraph):
        """添加随机节点"""
        node_type = random.choice([NodeType.QSP, NodeType.QC, NodeType.QM, NodeType.CC, NodeType.CP])
        party = random.choice([Party.ALICE, Party.BOB, Party.CHARLIE, None])
        
        params = {}
        if node_type == NodeType.QSP:
            params = {'state': '|+⟩', 'basis': 'X'}
        elif node_type == NodeType.QC:
            params = {'loss': 0.1}
        elif node_type == NodeType.QM:
            params = {'basis': 'Z'}
        elif node_type == NodeType.CC:
            params = {'capacity': 1.0}
        elif node_type == NodeType.CP:
            params = {'operation': 'sifting'}
        
        new_node_id = protocol.add_node(node_type=node_type, params=params, party=party)
        
        # 连接到现有节点
        if protocol.graph.nodes():
            existing_node = random.choice(list(protocol.graph.nodes()))
            if existing_node != new_node_id:
                edge_type = EdgeType.QUANTUM if node_type in [NodeType.QSP, NodeType.QC, NodeType.QM] else EdgeType.CLASSICAL
                # 随机选择方向
                if random.random() < 0.5:
                    protocol.add_edge(existing_node, new_node_id, edge_type=edge_type)
                else:
                    protocol.add_edge(new_node_id, existing_node, edge_type=edge_type)
    
    def _remove_random_node(self, protocol: ProtocolGraph):
        """移除随机节点"""
        if len(protocol.graph.nodes()) <= 3:  # 保持最小节点数
            return
        
        node_id = random.choice(list(protocol.graph.nodes()))
        protocol.graph.remove_node(node_id)
    
    def _add_random_edge(self, protocol: ProtocolGraph):
        """添加随机边"""
        if len(protocol.graph.nodes()) < 2:
            return
        
        source = random.choice(list(protocol.graph.nodes()))
        target = random.choice(list(protocol.graph.nodes()))
        
        if source != target and not protocol.graph.has_edge(source, target):
            edge_type = random.choice([EdgeType.QUANTUM, EdgeType.CLASSICAL])
            protocol.add_edge(source, target, edge_type=edge_type)
    
    def _remove_random_edge(self, protocol: ProtocolGraph):
        """移除随机边"""
        if protocol.graph.number_of_edges() <= 1:  # 保持最小边数
            return
        
        edges = list(protocol.graph.edges())
        if edges:
            source, target = random.choice(edges)
            protocol.graph.remove_edge(source, target)
    
    def _change_edge_type(self, protocol: ProtocolGraph):
        """改变边类型"""
        edges = list(protocol.graph.edges())
        if edges:
            source, target = random.choice(edges)
            edge = protocol.graph.edges[source, target]['edge']
            current_type = edge.edge_type
            new_type = EdgeType.CLASSICAL if current_type == EdgeType.QUANTUM else EdgeType.QUANTUM
            edge.edge_type = new_type
    
    def train(self, iterations: int = None, population_size: int = None) -> Dict:
        """训练智能体"""
        if iterations is None:
            iterations = self.config.max_iterations
        if population_size is None:
            population_size = self.config.population_size
        
        # 初始化种群
        self.population = []
        self.population.append(ProtocolGraph.create_bb84())  # 加入BB84作为基准
        
        for _ in range(population_size - 1):
            self.population.append(self.generate_random_protocol())
        
        self.best_protocol = self.population[0]
        self.best_fitness = self.evaluate_protocol(self.best_protocol)
        
        fitness_history = []
        
        for iteration in range(iterations):
            # 评估所有协议
            fitness_scores = []
            for protocol in self.population:
                fitness = self.evaluate_protocol(protocol)
                fitness_scores.append(fitness)
            
            # 找到最佳
            best_idx = np.argmax(fitness_scores)
            current_best_fitness = fitness_scores[best_idx]
            current_best_protocol = self.population[best_idx]
            
            if current_best_fitness > self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_protocol = current_best_protocol
            
            fitness_history.append(self.best_fitness)
            
            # 选择（锦标赛选择）
            selected_indices = []
            for _ in range(population_size):
                # 随机选择3个个体，选择适应度最高的
                tournament = random.sample(range(population_size), 3)
                winner = max(tournament, key=lambda i: fitness_scores[i])
                selected_indices.append(winner)
            
            # 生成新一代
            new_population = []
            
            # 保留精英
            elite_indices = np.argsort(fitness_scores)[-self.config.elite_size:]
            for idx in elite_indices:
                new_population.append(self.population[idx])
            
            # 生成剩余个体
            while len(new_population) < population_size:
                parent_idx = random.choice(selected_indices)
                parent = self.population[parent_idx]
                
                if random.random() < self.config.mutation_rate:
                    child = self.mutate_protocol(parent)
                else:
                    child = parent
                
                new_population.append(child)
            
            self.population = new_population
            
            # 报告进度
            if (iteration + 1) % 20 == 0:
                stats = self.best_protocol.get_statistics()
                print(f"迭代 {iteration+1:3d}: 最佳适应度 = {self.best_fitness:.4f}, "
                      f"节点数 = {stats['node_count']}, 边数 = {stats['edge_count']}")
        
        return {
            'best_fitness': self.best_fitness,
            'best_protocol': self.best_protocol,
            'best_protocol_stats': self.best_protocol.get_statistics() if self.best_protocol else {},
            'fitness_history': fitness_history,
            'iterations': iterations,
            'population_size': population_size
        }


# 兼容性包装器
class HybridAgent(EnhancedHybridAgent):
    """兼容旧接口的智能体"""
    pass