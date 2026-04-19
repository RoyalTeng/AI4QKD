#!/usr/bin/env python3
"""
基于元节点的QKD协议创新实验
核心：不再使用预定义节点类型，让AI组合基本操作
"""

import sys
sys.path.insert(0, '.')

import json
import time
import random
import numpy as np
from enum import Enum
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx


# ==================== 元节点系统 ====================

class BasicOperation(Enum):
    """基本量子/经典操作（原子操作）"""
    # 量子操作
    PREPARE_STATE = "prepare_state"          # 制备量子态
    SEND_PHOTON = "send_photon"              # 发送光子
    MEASURE = "measure"                      # 测量
    APPLY_GATE = "apply_gate"                # 应用量子门
    ENCODE_PHASE = "encode_phase"            # 相位编码
    ENCODE_POLARIZATION = "encode_polarization"  # 偏振编码
    
    # 经典操作
    SEND_CLASSICAL = "send_classical"        # 发送经典信息
    PROCESS_DATA = "process_data"            # 处理数据
    VERIFY = "verify"                        # 验证
    EXTRACT_KEY = "extract_key"              # 提取密钥
    
    # 特殊操作
    CREATE_ENTANGLEMENT = "create_entanglement"  # 产生纠缠
    PERFORM_INTERFERENCE = "perform_interference" # 执行干涉
    STABILIZE_PHASE = "stabilize_phase"      # 稳定相位


@dataclass
class OperationInstance:
    """操作实例"""
    op_type: BasicOperation
    parameters: Dict[str, Any] = field(default_factory=dict)
    order: int = 0
    
    def __str__(self):
        return f"{self.op_type.value}({self.parameters})"


@dataclass  
class MetaNode:
    """元节点：可组合的基本操作序列"""
    operations: List[OperationInstance] = field(default_factory=list)
    input_ports: List[str] = field(default_factory=list)
    output_ports: List[str] = field(default_factory=list)
    purpose: str = ""  # 目的描述（如"制备单光子"、"执行贝尔测量"）
    complexity: float = 1.0  # 复杂度评分
    
    def add_operation(self, op_type: BasicOperation, **params):
        """添加基本操作"""
        op = OperationInstance(
            op_type=op_type,
            parameters=params,
            order=len(self.operations)
        )
        self.operations.append(op)
        self._update_complexity()
    
    def _update_complexity(self):
        """更新复杂度评分"""
        base = len(self.operations) * 0.2
        special_ops = {
            BasicOperation.CREATE_ENTANGLEMENT: 0.3,
            BasicOperation.PERFORM_INTERFERENCE: 0.25,
            BasicOperation.STABILIZE_PHASE: 0.2
        }
        
        for op in self.operations:
            if op.op_type in special_ops:
                base += special_ops[op.op_type]
        
        self.complexity = min(base, 2.0)
    
    def infer_node_type(self):
        """推断节点类型（用于兼容现有系统）"""
        if not self.operations:
            return "unknown"
        
        # 根据操作序列推断
        op_types = {op.op_type for op in self.operations}
        
        # 量子态制备特征
        prep_ops = {BasicOperation.PREPARE_STATE, BasicOperation.SEND_PHOTON}
        if prep_ops.intersection(op_types):
            if BasicOperation.CREATE_ENTANGLEMENT in op_types:
                return "entanglement_source"
            elif BasicOperation.ENCODE_PHASE in op_types:
                return "phase_encoded_source"
            else:
                return "quantum_source"
        
        # 测量特征
        if BasicOperation.MEASURE in op_types:
            if BasicOperation.PERFORM_INTERFERENCE in op_types:
                return "interferometric_measurement"
            else:
                return "quantum_measurement"
        
        # 经典处理特征
        classic_ops = {BasicOperation.PROCESS_DATA, BasicOperation.VERIFY, BasicOperation.EXTRACT_KEY}
        if classic_ops.intersection(op_types):
            return "classical_processing"
        
        # 传输特征
        if BasicOperation.SEND_CLASSICAL in op_types:
            return "classical_channel"
        
        return "custom_component"
    
    def get_description(self):
        """获取人类可读描述"""
        if self.purpose:
            return self.purpose
        
        inferred = self.infer_node_type()
        op_count = len(self.operations)
        
        if op_count == 1:
            return f"{self.operations[0].op_type.value}"
        else:
            return f"{inferred} ({op_count} ops)"
    
    def copy(self):
        """深拷贝"""
        import copy
        return copy.deepcopy(self)


# ==================== 元图协议 ====================

@dataclass
class MetaEdge:
    """元边：连接元节点"""
    source_port: str
    target_port: str
    edge_type: str  # "quantum", "classical", "entanglement", "control"
    parameters: Dict[str, Any] = field(default_factory=dict)


class MetaGraphProtocol:
    """基于元图的协议表示"""
    
    def __init__(self, name: str = "MetaProtocol"):
        self.name = name
        self.graph = nx.DiGraph()  # 节点ID → MetaNode
        self.edges = {}  # (source_id, target_id) → MetaEdge
        self.next_node_id = 0
    
    def add_meta_node(self, meta_node: MetaNode) -> int:
        """添加元节点"""
        node_id = self.next_node_id
        self.graph.add_node(node_id, meta_node=meta_node)
        self.next_node_id += 1
        return node_id
    
    def add_meta_edge(self, source_id: int, target_id: int, meta_edge: MetaEdge):
        """添加元边"""
        if source_id not in self.graph or target_id not in self.graph:
            raise ValueError("Source or target node not found")
        
        self.graph.add_edge(source_id, target_id)
        self.edges[(source_id, target_id)] = meta_edge
    
    def generate_random_meta_node(self) -> MetaNode:
        """生成随机元节点"""
        meta_node = MetaNode()
        
        # 随机选择1-3个基本操作
        num_ops = random.randint(1, 3)
        all_ops = list(BasicOperation)
        
        for i in range(num_ops):
            op_type = random.choice(all_ops)
            
            # 生成随机参数
            params = {}
            if op_type == BasicOperation.PREPARE_STATE:
                params['state_type'] = random.choice(['single_photon', 'coherent', 'squeezed'])
                params['wavelength'] = random.choice([780, 850, 1310, 1550])
            elif op_type == BasicOperation.MEASURE:
                params['basis'] = random.choice(['rectilinear', 'diagonal', 'circular', 'random'])
                params['efficiency'] = round(random.uniform(0.7, 0.95), 2)
            elif op_type == BasicOperation.APPLY_GATE:
                params['gate_type'] = random.choice(['hadamard', 'phase', 'cnot', 'swap'])
            elif op_type == BasicOperation.CREATE_ENTANGLEMENT:
                params['state'] = random.choice(['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'])
                params['fidelity'] = round(random.uniform(0.8, 0.99), 2)
            
            meta_node.add_operation(op_type, **params)
        
        # 设置目的描述
        inferred = meta_node.infer_node_type()
        meta_node.purpose = f"Auto-generated {inferred}"
        
        return meta_node
    
    def mutate_meta_node(self, node_id: int) -> bool:
        """变异元节点"""
        if node_id not in self.graph:
            return False
        
        meta_node = self.graph.nodes[node_id]['meta_node']
        mutated = meta_node.copy()
        
        # 随机选择变异操作
        mutation_type = random.choice([
            'add_operation', 'remove_operation', 'modify_operation', 'reorder_operations'
        ])
        
        if mutation_type == 'add_operation' and len(mutated.operations) < 5:
            # 添加新操作
            available_ops = list(BasicOperation)
            new_op = random.choice(available_ops)
            mutated.add_operation(new_op, strength=random.random())
            
        elif mutation_type == 'remove_operation' and len(mutated.operations) > 1:
            # 删除操作
            idx = random.randrange(len(mutated.operations))
            mutated.operations.pop(idx)
            
        elif mutation_type == 'modify_operation' and mutated.operations:
            # 修改操作参数
            idx = random.randrange(len(mutated.operations))
            op = mutated.operations[idx]
            
            # 添加或修改一个随机参数
            param_key = f"param_{random.randint(1, 5)}"
            param_value = random.choice([random.random(), random.randint(1, 10), f"val_{random.randint(1, 100)}"])
            op.parameters[param_key] = param_value
            
        elif mutation_type == 'reorder_operations' and len(mutated.operations) > 1:
            # 重新排序操作
            random.shuffle(mutated.operations)
            for i, op in enumerate(mutated.operations):
                op.order = i
        
        # 更新节点
        self.graph.nodes[node_id]['meta_node'] = mutated
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取协议统计信息"""
        stats = {
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'meta_node_types': {},
            'operation_distribution': defaultdict(int),
            'total_operations': 0,
            'avg_complexity': 0.0
        }
        
        complexities = []
        for node_id in self.graph.nodes():
            meta_node = self.graph.nodes[node_id]['meta_node']
            node_type = meta_node.infer_node_type()
            
            # 统计节点类型
            stats['meta_node_types'][node_type] = stats['meta_node_types'].get(node_type, 0) + 1
            
            # 统计操作分布
            for op in meta_node.operations:
                stats['operation_distribution'][op.op_type.value] += 1
            
            stats['total_operations'] += len(meta_node.operations)
            complexities.append(meta_node.complexity)
        
        if complexities:
            stats['avg_complexity'] = np.mean(complexities)
        
        return stats
    
    def evaluate_novelty(self, other_protocols: List['MetaGraphProtocol']) -> float:
        """评估与其它协议的新颖性"""
        if not other_protocols:
            return 1.0
        
        # 提取特征向量
        my_features = self._extract_feature_vector()
        similarities = []
        
        for other in other_protocols:
            other_features = other._extract_feature_vector()
            similarity = self._cosine_similarity(my_features, other_features)
            similarities.append(similarity)
        
        max_similarity = max(similarities) if similarities else 0.0
        return 1.0 - max_similarity
    
    def _extract_feature_vector(self) -> Dict[str, float]:
        """提取特征向量"""
        stats = self.get_statistics()
        features = {}
        
        # 基本统计特征
        features['node_count'] = stats['node_count'] / 20.0
        features['edge_count'] = stats['edge_count'] / 40.0
        features['total_operations'] = stats['total_operations'] / 50.0
        features['avg_complexity'] = stats['avg_complexity'] / 2.0
        
        # 节点类型分布
        for node_type, count in stats['meta_node_types'].items():
            features[f'type_{node_type}'] = count / 10.0
        
        # 操作类型分布
        for op_type, count in stats['operation_distribution'].items():
            features[f'op_{op_type}'] = count / 20.0
        
        return features
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算余弦相似性"""
        all_keys = set(vec1.keys()) | set(vec2.keys())
        v1 = np.array([vec1.get(k, 0) for k in all_keys])
        v2 = np.array([vec2.get(k, 0) for k in all_keys])
        
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(np.dot(v1, v2) / (norm1 * norm2))
    
    def to_json(self) -> Dict[str, Any]:
        """转换为JSON可序列化格式"""
        data = {
            'name': self.name,
            'nodes': {},
            'edges': [],
            'statistics': self.get_statistics()
        }
        
        # 节点数据
        for node_id in self.graph.nodes():
            meta_node = self.graph.nodes[node_id]['meta_node']
            data['nodes'][str(node_id)] = {
                'operations': [
                    {
                        'type': op.op_type.value,
                        'parameters': op.parameters,
                        'order': op.order
                    }
                    for op in meta_node.operations
                ],
                'purpose': meta_node.purpose,
                'inferred_type': meta_node.infer_node_type(),
                'complexity': meta_node.complexity
            }
        
        # 边数据
        for (source, target), meta_edge in self.edges.items():
            data['edges'].append({
                'source': source,
                'target': target,
                'edge_type': meta_edge.edge_type,
                'source_port': meta_edge.source_port,
                'target_port': meta_edge.target_port,
                'parameters': meta_edge.parameters
            })
        
        return data


# ==================== 元节点实验 ====================

class MetaNodeExperiment:
    """元节点实验"""
    
    def __init__(self):
        self.protocols_history = []  # 历史协议库
        self.innovation_threshold = 0.7
    
    def generate_random_protocol(self, min_nodes=3, max_nodes=8) -> MetaGraphProtocol:
        """生成随机元图协议"""
        protocol = MetaGraphProtocol(name=f"Random_Meta_Protocol_{len(self.protocols_history)}")
        
        # 添加随机节点
        num_nodes = random.randint(min_nodes, max_nodes)
        node_ids = []
        
        for i in range(num_nodes):
            meta_node = protocol.generate_random_meta_node()
            node_id = protocol.add_meta_node(meta_node)
            node_ids.append(node_id)
        
        # 添加随机边（确保连通性）
        if len(node_ids) >= 2:
            # 创建简单路径确保连通
            for i in range(len(node_ids) - 1):
                source = node_ids[i]
                target = node_ids[i + 1]
                edge_type = random.choice(['quantum', 'classical'])
                meta_edge = MetaEdge(
                    source_port=f"out_{i}",
                    target_port=f"in_{i+1}",
                    edge_type=edge_type,
                    parameters={'weight': random.random()}
                )
                protocol.add_meta_edge(source, target, meta_edge)
            
            # 添加一些额外随机边
            extra_edges = random.randint(0, min(3, len(node_ids)))
            for _ in range(extra_edges):
                source = random.choice(node_ids)
                target = random.choice(node_ids)
                if source != target and not protocol.graph.has_edge(source, target):
                    edge_type = random.choice(['quantum', 'classical', 'control'])
                    meta_edge = MetaEdge(
                        source_port=f"extra_out_{source}",
                        target_port=f"extra_in_{target}",
                        edge_type=edge_type,
                        parameters={'weight': random.random()}
                    )
                    protocol.add_meta_edge(source, target, meta_edge)
        
        return protocol
    
    def evaluate_protocol_performance(self, protocol: MetaGraphProtocol) -> Dict[str, float]:
        """评估协议性能（启发式）"""
        stats = protocol.get_statistics()
        
        performance = {
            'security': self._estimate_security(protocol, stats),
            'efficiency': self._estimate_efficiency(protocol, stats),
            'robustness': self._estimate_robustness(protocol, stats),
            'feasibility': self._estimate_feasibility(protocol, stats),
            'innovation': protocol.evaluate_novelty(self.protocols_history)
        }
        
        return performance
    
    def _estimate_security(self, protocol: MetaGraphProtocol, stats: Dict) -> float:
        """估计安全性"""
        base = 0.4
        
        # 多样性奖励
        node_types = len(stats.get('meta_node_types', {}))
        if node_types >= 3:
            base += 0.15
        
        # 复杂性奖励（适度）
        complexity = stats.get('avg_complexity', 0)
        if 0.8 <= complexity <= 1.5:
            base += 0.1
        elif complexity > 1.5:
            base += 0.05  # 太复杂可能降低安全性
        
        # 检查是否有验证操作
        ops = stats.get('operation_distribution', {})
        if 'verify' in ops or 'extract_key' in ops:
            base += 0.1
        
        return min(base, 0.95)
    
    def _estimate_efficiency(self, protocol: MetaGraphProtocol, stats: Dict) -> float:
        """估计效率"""
        base = 0.5
        
        # 节点数适中奖励
        node_count = stats.get('node_count', 0)
        if 4 <= node_count <= 8:
            base += 0.2
        elif node_count < 4:
            base += node_count * 0.05
        else:
            base -= (node_count - 8) * 0.05
        
        # 边数适中奖励
        edge_count = stats.get('edge_count', 0)
        if edge_count >= node_count and edge_count <= node_count * 1.5:
            base += 0.1
        
        # 操作总数奖励（适度）
        total_ops = stats.get('total_operations', 0)
        if 5 <= total_ops <= 15:
            base += 0.1
        
        return max(0.2, min(base, 0.95))
    
    def _estimate_robustness(self, protocol: MetaGraphProtocol, stats: Dict) -> float:
        """估计鲁棒性"""
        base = 0.6
        
        # 冗余连接奖励
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        if edge_count > node_count:
            redundancy = (edge_count - node_count) / node_count
            base += min(redundancy * 0.2, 0.15)
        
        # 检查图连通性
        if nx.is_weakly_connected(protocol.graph):
            base += 0.1
        
        # 备份组件（同类型节点多个）
        node_types = stats.get('meta_node_types', {})
        for count in node_types.values():
            if count >= 2:
                base += 0.05
        
        return min(base, 0.95)
    
    def _estimate_feasibility(self, protocol: MetaGraphProtocol, stats: Dict) -> float:
        """估计技术可行性"""
        base = 0.7
        
        # 检查是否有明显不可行的组合
        issues = 0
        
        # 检查节点是否有输入输出
        for node_id in protocol.graph.nodes():
            in_degree = protocol.graph.in_degree(node_id)
            out_degree = protocol.graph.out_degree(node_id)
            
            meta_node = protocol.graph.nodes[node_id]['meta_node']
            node_type = meta_node.infer_node_type()
            
            # 源节点应该有输出
            if 'source' in node_type and out_degree == 0:
                issues += 1
            
            # 测量节点应该有输入
            if 'measurement' in node_type and in_degree == 0:
                issues += 1
        
        # 应用惩罚
        penalty = issues * 0.1
        base = max(0.3, base - penalty)
        
        # 复杂性惩罚（太复杂可能不可行）
        complexity = stats.get('avg_complexity', 0)
        if complexity > 1.8:
            base -= 0.1
        
        return max(0.2, base)
    
    def meta_fitness_function(self, protocol: MetaGraphProtocol) -> float:
        """元节点适应度函数"""
        performance = self.evaluate_protocol_performance(protocol)
        
        # 权重分配
        weights = {
            'security': 0.30,
            'efficiency': 0.25,
            'robustness': 0.20,
            'feasibility': 0.15,
            'innovation': 0.10  # 创新性权重
        }
        
        # 计算加权总分
        total_score = 0.0
        for metric, weight in weights.items():
            total_score += performance.get(metric, 0) * weight
        
        # 创新性特别奖励（如果高度创新）
        if performance['innovation'] > self.innovation_threshold:
            innovation_bonus = 0.15
            total_score = min(total_score + innovation_bonus, 1.0)
        
        return total_score
    
    def mutate_protocol(self, protocol: MetaGraphProtocol) -> MetaGraphProtocol:
        """变异协议"""
        mutated = MetaGraphProtocol(name=f"{protocol.name}_mutated")
        
        # 深拷贝原图
        node_mapping = {}
        for node_id in protocol.graph.nodes():
            meta_node = protocol.graph.nodes[node_id]['meta_node']
            new_id = mutated.add_meta_node(meta_node.copy())
            node_mapping[node_id] = new_id
        
        # 拷贝边
        for (source, target), meta_edge in protocol.edges.items():
            if source in node_mapping and target in node_mapping:
                new_edge = MetaEdge(
                    source_port=meta_edge.source_port,
                    target_port=meta_edge.target_port,
                    edge_type=meta_edge.edge_type,
                    parameters=meta_edge.parameters.copy()
                )
                mutated.add_meta_edge(node_mapping[source], node_mapping[target], new_edge)
        
        # 应用随机变异
        mutation_type = random.choice([
            'mutate_node', 'add_node', 'remove_node', 'add_edge', 'remove_edge'
        ])
        
        if mutation_type == 'mutate_node' and mutated.graph.nodes():
            # 变异一个随机节点
            node_id = random.choice(list(mutated.graph.nodes()))
            mutated.mutate_meta_node(node_id)
            
        elif mutation_type == 'add_node' and mutated.graph.number_of_nodes() < 12:
            # 添加新节点
            new_meta_node = mutated.generate_random_meta_node()
            new_id = mutated.add_meta_node(new_meta_node)
            
            # 连接到现有节点
            if mutated.graph.nodes():
                target = random.choice(list(mutated.graph.nodes()))
                edge_type = random.choice(['quantum', 'classical'])
                meta_edge = MetaEdge(
                    source_port=f"new_out",
                    target_port=f"existing_in",
                    edge_type=edge_type,
                    parameters={'weight': random.random()}
                )
                mutated.add_meta_edge(new_id, target, meta_edge)
                
        elif mutation_type == 'remove_node' and mutated.graph.number_of_nodes() > 2:
            # 删除随机节点（及其边）
            node_id = random.choice(list(mutated.graph.nodes()))
            mutated.graph.remove_node(node_id)
            # 需要清理相关的边记录
            edges_to_remove = []
            for (source, target) in mutated.edges.keys():
                if source == node_id or target == node_id:
                    edges_to_remove.append((source, target))
            for edge in edges_to_remove:
                if edge in mutated.edges:
                    del mutated.edges[edge]
        
        elif mutation_type == 'add_edge' and mutated.graph.number_of_nodes() >= 2:
            # 添加随机边
            nodes = list(mutated.graph.nodes())
            source = random.choice(nodes)
            target = random.choice(nodes)
            
            if source != target and not mutated.graph.has_edge(source, target):
                edge_type = random.choice(['quantum', 'classical', 'control'])
                meta_edge = MetaEdge(
                    source_port=f"add_out_{source}",
                    target_port=f"add_in_{target}",
                    edge_type=edge_type,
                    parameters={'weight': random.random()}
                )
                mutated.add_meta_edge(source, target, meta_edge)
        
        elif mutation_type == 'remove_edge' and mutated.graph.number_of_edges() > 1:
            # 删除随机边（确保不破坏连通性）
            edges = list(mutated.graph.edges())
            if edges:
                source, target = random.choice(edges)
                mutated.graph.remove_edge(source, target)
                if (source, target) in mutated.edges:
                    del mutated.edges[(source, target)]
        
        return mutated
    
    def run_meta_experiment(self, generations: int = 100, population_size: int = 20) -> Dict[str, Any]:
        """运行元节点实验"""
        print("\n" + "=" * 70)
        print("🚀 元节点QKD协议创新实验")
        print("=" * 70)
        print("核心：不再使用预定义节点类型，让AI组合基本操作")
        print("=" * 70)
        
        # 1. 初始化种群
        print(f"\n1. 🧬 初始化元节点种群 ({population_size}个协议)...")
        population = []
        
        for i in range(population_size):
            protocol = self.generate_random_protocol()
            protocol.name = f"Initial_Protocol_{i}"
            population.append(protocol)
        
        print(f"   种群初始化完成")
        
        # 2. 进化循环
        print(f"\n2. 🔄 开始进化 ({generations}代)...")
        
        best_fitness_history = []
        best_protocol = None
        best_fitness = 0.0
        
        for gen in range(generations):
            # 评估适应度
            fitness_scores = []
            for protocol in population:
                fitness = self.meta_fitness_function(protocol)
                fitness_scores.append((fitness, protocol))
            
            # 排序
            fitness_scores.sort(key=lambda x: x[0], reverse=True)
            
            # 更新最佳
            current_best_fitness, current_best = fitness_scores[0]
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_protocol = current_best
            
            best_fitness_history.append(best_fitness)
            
            # 每20代输出进度
            if (gen + 1) % 20 == 0 or gen == 0 or gen == generations - 1:
                avg_fitness = np.mean([f for f, _ in fitness_scores])
                print(f"   代 {gen+1:3d}: 最佳适应度 = {current_best_fitness:.4f}, 平均 = {avg_fitness:.4f}")
            
            # 选择（精英选择 + 轮盘赌）
            elite_count = max(2, population_size // 10)
            elites = [proto for _, proto in fitness_scores[:elite_count]]
            
            # 轮盘赌选择
            total_fitness = sum(f for f, _ in fitness_scores)
            if total_fitness > 0:
                probabilities = [f / total_fitness for f, _ in fitness_scores]
                selected = random.choices(
                    population, 
                    weights=probabilities, 
                    k=population_size - elite_count
                )
            else:
                selected = random.choices(population, k=population_size - elite_count)
            
            # 新种群 = 精英 + 选择的个体
            new_population = elites.copy()
            
            # 对选择的个体进行变异
            for protocol in selected:
                mutated = self.mutate_protocol(protocol)
                new_population.append(mutated)
            
            population = new_population
        
        # 3. 记录最佳协议到历史
        if best_protocol:
            self.protocols_history.append(best_protocol)
        
        # 4. 分析结果
        print(f"\n3. 📊 最终结果分析...")
        
        if best_protocol:
            best_stats = best_protocol.get_statistics()
            best_performance = self.evaluate_protocol_performance(best_protocol)
            
            print(f"   最佳适应度: {best_fitness:.4f}")
            print(f"   协议节点数: {best_stats['node_count']}")
            print(f"   协议边数: {best_stats['edge_count']}")
            print(f"   总操作数: {best_stats['total_operations']}")
            print(f"   平均复杂度: {best_stats['avg_complexity']:.3f}")
            
            print(f"\n   🎯 性能指标:")
            for metric, score in best_performance.items():
                print(f"     • {metric}: {score:.3f}")
            
            print(f"\n   💡 节点类型分布:")
            for node_type, count in best_stats.get('meta_node_types', {}).items():
                print(f"     • {node_type}: {count}")
            
            print(f"\n   🔧 操作分布 (前5):")
            op_dist = sorted(
                best_stats.get('operation_distribution', {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            for op_type, count in op_dist:
                print(f"     • {op_type}: {count}")
        
        # 5. 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "Meta-Node QKD Protocol Innovation",
            "philosophy": "Composable basic operations instead of predefined node types",
            "config": {
                "generations": generations,
                "population_size": population_size,
                "innovation_threshold": self.innovation_threshold
            },
            "results": {
                "best_fitness": float(best_fitness),
                "best_protocol_stats": best_stats if best_protocol else {},
                "best_performance": best_performance if best_protocol else {},
                "fitness_history": [float(f) for f in best_fitness_history],
                "total_protocols_evaluated": generations * population_size
            },
            "meta_node_system": {
                "basic_operations": [op.value for op in BasicOperation],
                "total_innovation_records": len(self.protocols_history)
            },
            "timestamp": timestamp
        }
        
        filename = f"results/meta_node_experiment_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ 元节点QKD协议创新实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 元节点QKD协议创新实验")
    print("=" * 70)
    print("范式突破：从预定义节点到可组合基本操作")
    print("=" * 70)
    
    print("\n📋 核心创新:")
    print("  1. ❌ 不再使用固定节点类型（QSP、QM、QC等）")
    print("  2. ✅ 使用15种基本量子/经典操作")
    print("  3. ✅ 让AI自由组合操作形成'元节点'")
    print("  4. ✅ 动态推断节点类型和功能")
    
    experiment = MetaNodeExperiment()
    
    # 实验参数
    generations = 100
    population_size = 20
    
    print(f"\n实验配置:")
    print(f"  进化代数: {generations}")
    print(f"  种群大小: {population_size}")
    print(f"  创新阈值: {experiment.innovation_threshold}")
    print(f"  开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行实验
    result = experiment.run_meta_experiment(
        generations=generations,
        population_size=population_size
    )
    
    # 显示总结
    print("\n📈 实验总结:")
    print(f"  最佳适应度: {result['results']['best_fitness']:.4f}")
    
    best_performance = result['results'].get('best_performance', {})
    innovation_score = best_performance.get('innovation', 0)
    
    if innovation_score > experiment.innovation_threshold:
        print(f"  创新性: ✅ 高度创新 (分数 {innovation_score:.3f})")
        print(f"  发现: 🎉 可能发现了全新类型的协议!")
    elif innovation_score > 0.5:
        print(f"  创新性: ⚠️ 中等创新 (分数 {innovation_score:.3f})")
        print(f"  发现: 🔄 可能是已知协议的创新变体")
    else:
        print(f"  创新性: ❌ 低创新性 (分数 {innovation_score:.3f})")
        print(f"  发现: 🔍 与已知协议高度相似")
    
    # 显示发现的元节点类型
    stats = result['results'].get('best_protocol_stats', {})
    meta_node_types = stats.get('meta_node_types', {})
    
    if meta_node_types:
        print(f"\n  🔬 发现的元节点类型:")
        for node_type, count in meta_node_types.items():
            if 'custom' in node_type or 'auto' in node_type:
                print(f"     • {node_type}: {count} (可能是新类型!)")
            else:
                print(f"     • {node_type}: {count}")
    
    print(f"\n📁 结果文件: results/meta_node_experiment_*.json")
    
    print("\n🎯 下一步研究方向:")
    if innovation_score > experiment.innovation_threshold:
        print("  1. 深入分析发现的'元节点'结构")
        print("  2. 理解AI如何组合基本操作")
        print("  3. 与传统节点类型进行对比")
        print("  4. 尝试解释新协议的工作原理")
    else:
        print("  1. 增加基本操作类型库")
        print("  2. 提高创新性奖励权重")
        print("  3. 尝试更激进的变异策略")
        print("  4. 分析为什么AI倾向于已知组合")


if __name__ == "__main__":
    main()
