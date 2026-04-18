"""
混合智能体 - 简化版
"""

import random
from typing import Dict, Any, Optional
from dataclasses import dataclass
from qcgf_dsl import ProtocolGraph, NodeType, Party
from simulator import QuantumSimulator


@dataclass
class AgentConfig:
    """智能体配置"""
    population_size: int = 20
    mutation_rate: float = 0.1
    max_iterations: int = 50


class HybridAgent:
    """混合智能体"""
    
    def __init__(self, config=None):
        self.config = config or AgentConfig()
        self.simulator = QuantumSimulator()
        self.population = []
        self.best_protocol = None
        self.best_fitness = 0
    
    def initialize_population(self):
        """初始化种群"""
        self.population = []
        
        # 添加预定义协议
        self.population.append(ProtocolGraph.create_bb84())
        
        # 添加随机协议
        for i in range(self.config.population_size - 1):
            protocol = self._generate_random_protocol()
            self.population.append(protocol)
    
    def _generate_random_protocol(self):
        """生成随机协议"""
        protocol = ProtocolGraph(name=f"Random_Protocol_{random.randint(1000, 9999)}")
        
        # 随机节点数
        num_nodes = random.randint(3, 8)
        
        # 添加节点
        node_ids = []
        for i in range(num_nodes):
            node_type = random.choice([NodeType.QSP, NodeType.QC, NodeType.QM, NodeType.CC])
            party = random.choice([Party.ALICE, Party.BOB, None])
            
            params = {}
            if node_type == NodeType.QSP:
                params = {'state': random.choice(['|0⟩', '|1⟩', '|+⟩']), 'basis': random.choice(['Z', 'X'])}
            elif node_type == NodeType.QC:
                params = {'loss': random.uniform(0.05, 0.3)}
            elif node_type == NodeType.QM:
                params = {'basis': random.choice(['Z', 'X'])}
            elif node_type == NodeType.CC:
                params = {'capacity': random.uniform(0.5, 2.0)}
            
            node_id = protocol.add_node(node_type=node_type, params=params, party=party)
            node_ids.append(node_id)
        
        # 添加边（确保连通）
        if len(node_ids) > 1:
            for i in range(len(node_ids) - 1):
                protocol.add_edge(node_ids[i], node_ids[i + 1])
        
        return protocol
    
    def evaluate_fitness(self, protocol):
        """评估适应度"""
        try:
            result = self.simulator.simulate(protocol, pulse_count=5000)
            # 简单适应度：最大化增益，最小化QBER
            fitness = result.gain * (1 - result.qber)
            return fitness
        except:
            return 0.0
    
    def train(self, iterations=None):
        """训练智能体"""
        if iterations is None:
            iterations = self.config.max_iterations
        
        self.initialize_population()
        
        for iteration in range(iterations):
            # 评估所有协议
            fitness_scores = []
            for protocol in self.population:
                fitness = self.evaluate_fitness(protocol)
                fitness_scores.append(fitness)
            
            # 找到最佳
            best_idx = max(range(len(fitness_scores)), key=lambda i: fitness_scores[i])
            if fitness_scores[best_idx] > self.best_fitness:
                self.best_fitness = fitness_scores[best_idx]
                self.best_protocol = self.population[best_idx]
            
            # 演化：选择、变异
            new_population = []
            
            # 保留最佳
            new_population.append(self.population[best_idx])
            
            # 生成新个体
            while len(new_population) < self.config.population_size:
                # 选择父代（简单选择）
                parent = random.choice(self.population)
                
                # 变异
                if random.random() < self.config.mutation_rate:
                    child = self._mutate(parent)
                else:
                    child = parent
                
                new_population.append(child)
            
            self.population = new_population
            
            if iteration % 10 == 0:
                print(f"迭代 {iteration}: 最佳适应度 = {self.best_fitness:.4f}")
        
        return {
            'best_fitness': self.best_fitness,
            'best_protocol': self.best_protocol,
            'iterations': iterations
        }
    
    def _mutate(self, protocol):
        """变异操作"""
        # 简单变异：随机修改一个节点的参数
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
                edge_type=edge.edge_type
            )
        
        # 随机修改一个参数
        if mutated.graph.nodes():
            node_id = random.choice(list(mutated.graph.nodes()))
            node = mutated.graph.nodes[node_id]['node']
            
            if node.params:
                param_name = random.choice(list(node.params.keys()))
                if isinstance(node.params[param_name], (int, float)):
                    # 数值参数：随机扰动
                    current = node.params[param_name]
                    node.params[param_name] = max(0.01, current * random.uniform(0.8, 1.2))
        
        return mutated
    
    def design_protocol(self, constraints=None, iterations=None):
        """设计新协议"""
        print("开始设计新协议...")
        result = self.train(iterations)
        print(f"设计完成！最佳适应度: {result['best_fitness']:.4f}")
        return result['best_protocol']
    
    def evaluate_protocol(self, protocol):
        """评估协议"""
        fitness = self.evaluate_fitness(protocol)
        return {
            'protocol_name': protocol.name,
            'fitness': fitness,
            'protocol_stats': protocol.get_statistics()
        }