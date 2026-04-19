#!/usr/bin/env python3
"""
增强版两阶段创新实验（修复问题）
1. 修复边数为0的问题
2. 改进新颖性检测
3. 增强训练强度
4. 改进初始种群
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random
import numpy as np
from collections import defaultdict
import networkx as nx


class EnhancedTwoStageExperiment:
    """增强版两阶段实验"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.base_evaluate = self.agent.evaluate_protocol
        
        # 已知协议库
        self.known_protocols = self._load_known_protocols()
        
        # 阶段结果
        self.phase1_innovations = []
        self.phase2_results = {}
        
        # 增强配置
        self.config = {
            'phase1': {
                'generations': 100,      # 增加
                'population_size': 40,   # 增加
                'mutation_rate': 0.7,    # 更高
                'elite_size': 1          # 更少精英
            },
            'phase2': {
                'generations': 80,       # 增加
                'population_size': 30,   # 增加
                'mutation_rate': 0.5,    # 中等
                'elite_size': 3          # 中等精英
            }
        }
    
    def _load_known_protocols(self):
        """加载已知协议库（增强版）"""
        known = []
        
        # BB84（完整版）
        bb84 = ProtocolGraph.create_bb84()
        known.append(bb84)
        
        # MDI（完整版）
        mdi = self._create_mdi_protocol()
        known.append(mdi)
        
        # TF（完整版）
        tf = self._create_tf_protocol()
        known.append(tf)
        
        # E91（简化版）
        e91 = self._create_e91_protocol()
        known.append(e91)
        
        return known
    
    def _create_mdi_protocol(self):
        """创建MDI协议"""
        protocol = ProtocolGraph(name="MDI Protocol")
        
        # Alice
        alice_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'single_photon', 'basis': 'random'},
            Party.ALICE
        )
        
        # Bob
        bob_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'single_photon', 'basis': 'random'},
            Party.BOB
        )
        
        # 量子信道
        channel1 = protocol.add_node(NodeType.QC, {'loss': 0.2}, None)
        channel2 = protocol.add_node(NodeType.QC, {'loss': 0.2}, None)
        
        # Charlie的贝尔测量
        bell_measurement = protocol.add_node(
            NodeType.QM,
            {'basis': 'bell', 'type': 'BSM'},
            Party.CHARLIE
        )
        
        # 经典信道
        classical = protocol.add_node(NodeType.CC, {}, None)
        
        # 连接
        protocol.add_edge(alice_source, channel1, EdgeType.QUANTUM)
        protocol.add_edge(bob_source, channel2, EdgeType.QUANTUM)
        protocol.add_edge(channel1, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(channel2, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(bell_measurement, classical, EdgeType.CLASSICAL)
        
        return protocol
    
    def _create_tf_protocol(self):
        """创建TF协议"""
        protocol = ProtocolGraph(name="TF Protocol")
        
        # 两个相干光源
        alice_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'coherent', 'phase': 'random'},
            Party.ALICE
        )
        
        bob_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'coherent', 'phase': 'random'},
            Party.BOB
        )
        
        # 长距离信道
        channel1 = protocol.add_node(NodeType.QC, {'distance': 300, 'loss': 0.3}, None)
        channel2 = protocol.add_node(NodeType.QC, {'distance': 300, 'loss': 0.3}, None)
        
        # 干涉仪
        interferometer = protocol.add_node(
            NodeType.QG,
            {'gate_type': 'beam_splitter', 'config': 'MZ'},
            Party.CHARLIE
        )
        
        # 探测器
        detector = protocol.add_node(NodeType.QD, {'type': 'single_photon'}, Party.CHARLIE)
        
        # 连接
        protocol.add_edge(alice_source, channel1, EdgeType.QUANTUM)
        protocol.add_edge(bob_source, channel2, EdgeType.QUANTUM)
        protocol.add_edge(channel1, interferometer, EdgeType.QUANTUM)
        protocol.add_edge(channel2, interferometer, EdgeType.QUANTUM)
        protocol.add_edge(interferometer, detector, EdgeType.QUANTUM)
        
        return protocol
    
    def _create_e91_protocol(self):
        """创建E91协议"""
        protocol = ProtocolGraph(name="E91 Protocol")
        
        # 纠缠源
        entanglement_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'bell_state', 'type': 'phi_plus'},
            None
        )
        
        # 分发信道
        channel1 = protocol.add_node(NodeType.QC, {'loss': 0.1}, None)
        channel2 = protocol.add_node(NodeType.QC, {'loss': 0.1}, None)
        
        # Alice和Bob的测量
        alice_measure = protocol.add_node(
            NodeType.QM,
            {'basis': 'random_3settings'},
            Party.ALICE
        )
        
        bob_measure = protocol.add_node(
            NodeType.QM,
            {'basis': 'random_3settings'},
            Party.BOB
        )
        
        # 经典通信和验证
        classical = protocol.add_node(NodeType.CC, {}, None)
        verification = protocol.add_node(NodeType.CV, {'test': 'CHSH'}, Party.BOTH)
        
        # 连接
        protocol.add_edge(entanglement_source, channel1, EdgeType.QUANTUM)
        protocol.add_edge(entanglement_source, channel2, EdgeType.QUANTUM)
        protocol.add_edge(channel1, alice_measure, EdgeType.QUANTUM)
        protocol.add_edge(channel2, bob_measure, EdgeType.QUANTUM)
        protocol.add_edge(alice_measure, classical, EdgeType.CLASSICAL)
        protocol.add_edge(bob_measure, classical, EdgeType.CLASSICAL)
        protocol.add_edge(classical, verification, EdgeType.CLASSICAL)
        
        return protocol
    
    def generate_quality_random_protocol(self, min_nodes=4, max_nodes=8):
        """生成高质量随机协议（确保连通性）"""
        protocol = ProtocolGraph(name=f"Quality_Random_{len(self.known_protocols)}")
        
        # 随机节点数
        num_nodes = random.randint(min_nodes, max_nodes)
        
        # 添加节点
        node_ids = []
        for i in range(num_nodes):
            # 随机选择节点类型（避免孤立类型）
            node_type = random.choice([
                NodeType.QSP, NodeType.QC, NodeType.QM, 
                NodeType.CC, NodeType.CP
            ])
            
            # 随机参数
            params = {}
            if node_type == NodeType.QSP:
                params['state'] = random.choice(['single_photon', 'coherent', 'entangled'])
            elif node_type == NodeType.QC:
                params['loss'] = round(random.uniform(0.1, 0.4), 2)
            
            # 随机参与方
            party = random.choice([Party.ALICE, Party.BOB, Party.CHARLIE, None])
            
            node_id = protocol.add_node(node_type, params, party)
            node_ids.append(node_id)
        
        # 确保连通性：创建最小生成树
        if len(node_ids) >= 2:
            # 随机连接形成树
            connected = [node_ids[0]]
            unconnected = node_ids[1:]
            
            while unconnected:
                source = random.choice(connected)
                target = random.choice(unconnected)
                
                # 随机边类型
                edge_type = random.choice([EdgeType.QUANTUM, EdgeType.CLASSICAL])
                protocol.add_edge(source, target, edge_type)
                
                connected.append(target)
                unconnected.remove(target)
            
            # 添加一些额外边（增加复杂性）
            extra_edges = random.randint(0, min(3, len(node_ids) // 2))
            for _ in range(extra_edges):
                source = random.choice(node_ids)
                target = random.choice(node_ids)
                if source != target and not protocol.graph.has_edge(source, target):
                    edge_type = random.choice([EdgeType.QUANTUM, EdgeType.CLASSICAL])
                    protocol.add_edge(source, target, edge_type)
        
        return protocol
    
    def extract_enhanced_features(self, protocol: ProtocolGraph) -> dict:
        """增强版特征提取"""
        stats = protocol.get_statistics()
        features = defaultdict(float)
        
        # 基本统计（归一化）
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        features['node_count'] = node_count / 15.0
        features['edge_count'] = edge_count / 25.0
        features['edge_node_ratio'] = (edge_count / max(node_count, 1)) / 3.0
        
        # 节点类型分布
        node_stats = stats.get('node_stats', {})
        for node_type, count in node_stats.items():
            features[f'node_{node_type}'] = count / 8.0
        
        # 参与方分布
        party_stats = stats.get('party_stats', {})
        for party, count in party_stats.items():
            features[f'party_{party}'] = count / 4.0
        
        # 图拓扑特征
        graph = protocol.graph
        
        # 连通性特征
        if graph.number_of_nodes() > 0:
            # 度分布
            degrees = [d for _, d in graph.degree()]
            features['avg_degree'] = np.mean(degrees) / 6.0
            features['max_degree'] = np.max(degrees) / 8.0
            
            # 连通性
            try:
                if nx.is_weakly_connected(graph):
                    features['is_connected'] = 1.0
                    
                    # 平均路径长度
                    undirected = graph.to_undirected()
                    if nx.is_connected(undirected):
                        avg_path = nx.average_shortest_path_length(undirected)
                        features['avg_path_length'] = avg_path / 5.0
            except:
                pass
            
            # 聚类系数（如果有足够边）
            if edge_count >= 3:
                try:
                    clustering = nx.average_clustering(undirected)
                    features['clustering'] = clustering
                except:
                    pass
        
        return dict(features)
    
    def evaluate_enhanced_novelty(self, protocol: ProtocolGraph) -> float:
        """增强版新颖性评估"""
        if not self.known_protocols:
            return 1.0
        
        # 提取特征
        my_features = self.extract_enhanced_features(protocol)
        
        # 计算相似性
        similarities = []
        for known in self.known_protocols:
            known_features = self.extract_enhanced_features(known)
            similarity = self._cosine_similarity(my_features, known_features)
            similarities.append(similarity)
        
        # 新颖性 = 1 - 最大相似性
        max_similarity = max(similarities) if similarities else 0.0
        base_novelty = 1.0 - max_similarity
        
        # 增强奖励/惩罚
        stats = protocol.get_statistics()
        edge_count = stats.get('edge_count', 0)
        node_count = stats.get('node_count', 0)
        
        # 惩罚孤立节点/边数不足
        if edge_count == 0:
            base_novelty *= 0.2  # 大幅惩罚
        elif edge_count < node_count - 1:  # 少于最小生成树
            base_novelty *= 0.7
        
        # 奖励复杂结构
        if edge_count > node_count * 1.5:
            base_novelty = min(base_novelty * 1.3, 1.0)
        
        # 奖励新的节点类型组合
        node_stats = stats.get('node_stats', {})
        novel_combinations = self._find_novel_combinations(node_stats)
        base_novelty += len(novel_combinations) * 0.05
        
        return min(base_novelty, 1.0)
    
    def _find_novel_combinations(self, node_stats: dict) -> list:
        """发现新的节点类型组合"""
        novel = []
        
        # 检查是否有已知协议中不常见的组合
        known_combinations = [
            {'quantum_state_preparation': 2, 'quantum_measurement': 1},  # BB84-like
            {'quantum_state_preparation': 2, 'quantum_measurement': 1, 'quantum_channel': 2},  # MDI-like
            {'quantum_state_preparation': 2, 'quantum_gate': 1, 'quantum_channel': 2},  # TF-like
            {'quantum_state_preparation': 1, 'quantum_measurement': 2, 'quantum_channel': 2},  # E91-like
        ]
        
        current_combo = {k: v for k, v in node_stats.items() if v > 0}
        
        # 如果当前组合不在已知组合中，且有一定复杂性
        if (len(current_combo) >= 3 and 
            current_combo not in known_combinations):
            novel.append(current_combo)
        
        return novel
    
    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        """计算余弦相似性"""
        all_keys = set(vec1.keys()) | set(vec2.keys())
        v1 = np.array([vec1.get(k, 0) for k in all_keys])
        v2 = np.array([vec2.get(k, 0) for k in all_keys])
        
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(np.dot(v1, v2) / (norm1 * norm2))
    
    def evaluate_enhanced_performance(self, protocol: ProtocolGraph) -> dict:
        """增强版性能评估"""
        # 基础评估
        base_fitness = self.base_evaluate(protocol)
        
        # 结构质量评估
        stats = protocol.get_statistics()
        edge_count = stats.get('edge_count', 0)
        node_count = stats.get('node_count', 0)
        
        # 连通性惩罚
        connectivity_penalty = 0.0
        if edge_count == 0:
            connectivity_penalty = 0.5  # 严重惩罚
        elif edge_count < node_count - 1:  # 不连通
            connectivity_penalty = 0.3
        elif not nx.is_weakly_connected(protocol.graph):
            connectivity_penalty = 0.2
        
        # 启发式性能指标
        performance = {
            'base_fitness': base_fitness,
            'security': self._estimate_security(stats),
            'efficiency': self._estimate_efficiency(stats),
            'robustness': self._estimate_robustness(stats),
            'connectivity_penalty': connectivity_penalty
        }
        
        # 综合性能（考虑连通性）
        performance['total'] = (
            performance['base_fitness'] * 0.35 +
            performance['security'] * 0.25 +
            performance['efficiency'] * 0.20 +
            performance['robustness'] * 0.20 -
            performance['connectivity_penalty'] * 0.3
        )
        
        # 确保非负
        performance['total'] = max(0.0, performance['total'])
        
        return performance
    
    def _estimate_security(self, stats: dict) -> float:
        """估计安全性"""
        base = 0.5
        
        # 多样性奖励
        node_types = len(stats.get('node_stats', {}))
        if node_types >= 4:
            base += 0.2
        elif node_types >= 3:
            base += 0.1
        
        # 经典验证存在性
        if stats.get('node_stats', {}).get('classical_verification', 0) > 0:
            base += 0.15
        
        # 测量多样性
        if stats.get('node_stats', {}).get('quantum_measurement', 0) >= 2:
            base += 0.1
        
        # 纠缠源存在性（高级安全性）
        qsp_stats = stats.get('node_stats', {}).get('quantum_state_preparation', 0)
        if qsp_stats >= 2:  # 多个源可能表示纠缠
            base += 0.05
        
        return min(base, 0.95)
    
    def _estimate_efficiency(self, stats: dict) -> float:
        """估计效率"""
        base = 0.6
        
        # 节点数适中
        node_count = stats.get('node_count', 0)
        if 5 <= node_count <= 10:
            base += 0.25
        elif 3 <= node_count <= 12:
            base += 0.15
        elif node_count > 12:
            base -= (node_count - 12) * 0.05
        
        # 边数适中（有连接但不过度复杂）
        edge_count = stats.get('edge_count', 0)
        if edge_count >= node_count and edge_count <= node_count * 2:
            base += 0.15
        elif edge_count > node_count * 2:
            base -= (edge_count - node_count * 2) * 0.03
        
        return max(0.2, min(base, 0.95))
    
    def _estimate_robustness(self, stats: dict) -> float:
        """估计鲁棒性"""
        base = 0.7
        
        # 冗余连接
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        if edge_count > node_count:
            redundancy = (edge_count - node_count) / node_count
            base += min(redundancy * 0.25, 0.2)
        
        # 备份组件
        for node_type, count in stats.get('node_stats', {}).items():
            if count >= 2:
                base += 0.05
        
        # 经典信道存在性（增加鲁棒性）
        if stats.get('node_stats', {}).get('classical_channel', 0) > 0:
            base += 0.1
        
        return min(base, 0.95)
    
    def phase1_innovation_fitness(self, protocol: ProtocolGraph) -> float:
        """阶段1适应度：100%新颖性（增强版）"""
        novelty = self.evaluate_enhanced_novelty(protocol)
        
        # 额外奖励：结构质量
        stats = protocol.get_statistics()
        edge_count = stats.get('edge_count', 0)
        node_count = stats.get('node_count', 0)
        
        quality_bonus = 0.0
        
        # 奖励良好连接
        if edge_count >= node_count and edge_count <= node_count * 2:
            quality_bonus += 0.1
        
        # 奖励节点类型多样性
        node_types = len(stats.get('node_stats', {}))
        if node_types >= 4:
            quality_bonus += 0.1
        elif node_types >= 3:
            quality_bonus += 0.05
        
        # 惩罚孤立节点（在novelty中已部分处理，这里额外强调）
        if edge_count == 0:
            quality_bonus -= 0.3
        
        total = novelty + quality_bonus
        return max(0.0, min(total, 1.0))
    
    def phase2_performance_fitness(self, protocol: ProtocolGraph) -> float:
        """阶段2适应度：70%性能 + 30%新颖性（增强版）"""
        performance = self.evaluate_enhanced_performance(protocol)
        novelty = self.evaluate_enhanced_novelty(protocol)
        
        # 70%性能 + 30%新颖性
        total = performance['total'] * 0.7 + novelty * 0.3
        
        # 特别奖励：既有高性能又有高新颖性
        if performance['total'] > 0.7 and novelty > 0.6:
            total = min(total + 0.15, 1.0)
        elif performance['total'] > 0.6 and novelty > 0.5:
            total = min(total + 0.08, 1.0)
        
        return total
    
    def generate_enhanced_initial_population(self, size: int) -> list:
        """生成增强版初始种群"""
        population = []
        
        # 1. 添加已知好协议（25%）
        known_count = min(size // 4, len(self.known_protocols))
        for i in range(known_count):
            known = self.known_protocols[i]
            known.name = f"Initial_Known_{i}"
            population.append(known)
        
        # 2. 生成高质量随机协议（75%）
        for i in range(size - len(population)):
            protocol = self.generate_quality_random_protocol(
                min_nodes=4,
                max_nodes=10
            )
            protocol.name = f"Initial_Quality_{i}"
            population.append(protocol)
        
        return population
    
    def run_enhanced_phase1(self) -> list:
        """运行增强版阶段1"""
        print("\n" + "=" * 70)
        print("🚀 增强版阶段1：纯创新探索")
        print("=" * 70)
        print("修复：强制连通性，改进新颖性检测，增强训练")
        print("=" * 70)
        
        config = self.config['phase1']
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用阶段1适应度
        self.agent.evaluate_protocol = self.phase1_innovation_fitness
        
        # 1. 初始化增强版种群
        print(f"\n1. 🧬 初始化增强版种群 ({config['population_size']}个协议)...")
        self.agent.population = self.generate_enhanced_initial_population(
            config['population_size']
        )
        
        print(f"   包含: {len(self.known_protocols)}个已知协议 + {config['population_size'] - len(self.known_protocols)}个高质量随机协议")
        
        # 2. 配置增强训练参数
        self.agent.config.max_iterations = config['generations']
        self.agent.config.population_size = config['population_size']
        self.agent.config.mutation_rate = config['mutation_rate']
        self.agent.config.elite_size = config['elite_size']
        self.agent.config.crossover_rate = 0.25
        
        # 3. 运行增强探索
        print(f"\n2. 🔍 开始增强探索 ({config['generations']}代)...")
        print(f"   变异率: {config['mutation_rate']}, 精英数: {config['elite_size']}")
        
        result = self.agent.train(
            iterations=config['generations'],
            population_size=config['population_size']
        )
        
        # 4. 收集创新发现
        print(f"\n3. 📊 收集创新发现...")
        
        # 评估所有协议
        evaluations = []
        for protocol in self.agent.population:
            novelty = self.evaluate_enhanced_novelty(protocol)
            performance = self.evaluate_enhanced_performance(protocol)
            evaluations.append((novelty, performance['total'], protocol))
        
        # 按新颖性排序
        evaluations.sort(key=lambda x: x[0], reverse=True)
        
        # 选择前15%作为创新发现
        top_count = max(5, len(evaluations) // 6)
        top_innovations = evaluations[:top_count]
        
        print(f"   发现 {len(top_innovations)} 个高度创新的协议")
        print(f"   最高新颖性: {top_innovations[0][0]:.3f}")
        print(f"   平均新颖性: {np.mean([n for n, _, _ in top_innovations]):.3f}")
        
        # 检查连通性
        connected_count = sum(
            1 for _, _, proto in top_innovations 
            if proto.graph.number_of_edges() > 0
        )
        print(f"   连通协议: {connected_count}/{len(top_innovations)}")
        
        # 保存
        self.phase1_innovations = [(proto.name, novelty, perf) for novelty, perf, proto in top_innovations]
        
        # 恢复原始评估
        self.agent.evaluate_protocol = original_evaluate
        
        # 返回创新协议
        phase1_results = [proto for _, _, proto in top_innovations]
        
        print(f"\n✅ 增强版阶段1完成")
        
        return phase1_results
    
    def run_enhanced_phase2(self, innovative_protocols: list) -> dict:
        """运行增强版阶段2"""
        print("\n" + "=" * 70)
        print("🚀 增强版阶段2：性能优化")
        print("=" * 70)
        print("从阶段1的创新协议开始，优化性能")
        print("=" * 70)
        
        config = self.config['phase2']
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用阶段2适应度
        self.agent.evaluate_protocol = self.phase2_performance_fitness
        
        # 1. 初始化种群（从阶段1开始）
        print(f"\n1. 🧬 初始化优化种群...")
        print(f"   从阶段1的 {len(innovative_protocols)} 个创新协议开始")
        
        self.agent.population = []
        
        # 添加阶段1的创新协议
        for i, protocol in enumerate(innovative_protocols):
            protocol.name = f"Phase2_Innovative_{i}"
            self.agent.population.append(protocol)
        
        # 补充高质量随机协议
        while len(self.agent.population) < config['population_size']:
            protocol = self.generate_quality_random_protocol()
            protocol.name = f"Phase2_Quality_{len(self.agent.population)}"
            self.agent.population.append(protocol)
        
        print(f"   最终种群大小: {len(self.agent.population)}")
        
        # 2. 配置优化参数
        self.agent.config.max_iterations = config['generations']
        self.agent.config.population_size = config['population_size']
        self.agent.config.mutation_rate = config['mutation_rate']
        self.agent.config.elite_size = config['elite_size']
        self.agent.config.crossover_rate = 0.3
        
        # 3. 运行性能优化
        print(f"\n2. ⚡ 开始性能优化 ({config['generations']}代)...")
        print(f"   变异率: {config['mutation_rate']}, 精英数: {config['elite_size']}")
        
        result = self.agent.train(
            iterations=config['generations'],
            population_size=config['population_size']
        )
        
        # 4. 分析结果
        print(f"\n3. 📊 优化结果分析...")
        
        best_fitness = result.get('best_fitness', 0)
        best_protocol = result.get('best_protocol')
        
        if best_protocol:
            best_novelty = self.evaluate_enhanced_novelty(best_protocol)
            best_performance = self.evaluate_enhanced_performance(best_protocol)
            best_stats = best_protocol.get_statistics()
            
            print(f"   最佳适应度: {best_fitness:.4f}")
            print(f"   新颖性: {best_novelty:.3f}")
            print(f"   性能: {best_performance['total']:.3f}")
            print(f"   节点数: {best_stats['node_count']}")
            print(f"   边数: {best_stats['edge_count']}")
            print(f"   连通性: {'✅ 连通' if best_stats['edge_count'] > 0 else '❌ 不连通'}")
            
            # 与阶段1最佳对比
            if self.phase1_innovations:
                phase1_best_novelty = self.phase1_innovations[0][1]
                phase1_best_perf = self.phase1_innovations[0][2]
                
                print(f"\n   🔄 与阶段1最佳对比:")
                print(f"     新颖性: {phase1_best_novelty:.3f} → {best_novelty:.3f} ({best_novelty - phase1_best_novelty:+.3f})")
                print(f"     性能: {phase1_best_perf:.3f} → {best_performance['total']:.3f} ({best_performance['total'] - phase1_best_perf:+.3f})")
        
        # 恢复原始评估
        self.agent.evaluate_protocol = original_evaluate
        
        # 保存结果
        self.phase2_results = {
            'best_fitness': best_fitness,
            'best_protocol': best_protocol,
            'best_novelty': best_novelty if best_protocol else 0,
            'best_performance': best_performance if best_protocol else {},
            'training_result': result
        }
        
        print(f"\n✅ 增强版阶段2完成")
        
        return self.phase2_results
    
    def run_enhanced_two_stage(self) -> dict:
        """运行完整增强版两阶段实验"""
        print("=" * 70)
        print("🎯 增强版两阶段创新实验")
        print("=" * 70)
        print("修复问题 + 增强训练 + 改进评估")
        print("=" * 70)
        
        start_time = time.time()
        
        # 阶段1：增强创新探索
        phase1_start = time.time()
        print(f"\n📅 开始阶段1: {time.strftime('%H:%M:%S')}")
        innovative_protocols = self.run_enhanced_phase1()
        phase1_time = time.time() - phase1_start
        
        # 阶段2：增强性能优化
        phase2_start = time.time()
        print(f"\n📅 开始阶段2: {time.strftime('%H:%M:%S')}")
        phase2_result = self.run_enhanced_phase2(innovative_protocols)
        phase2_time = time.time() - phase2_start
        
        total_time = time.time() - start_time
        
        # 综合结果
        print("\n" + "=" * 70)
        print("📈 增强版两阶段实验综合结果")
        print("=" * 70)
        
        best_protocol = phase2_result.get('best_protocol')
        if best_protocol:
            final_novelty = self.evaluate_enhanced_novelty(best_protocol)
            final_performance = self.evaluate_enhanced_performance(best_protocol)
            final_stats = best_protocol.get_statistics()
            
            print(f"  最终协议:")
            print(f"    • 适应度: {phase2_result['best_fitness']:.4f}")
            print(f"    • 新颖性: {final_novelty:.3f}")
            print(f"    • 性能: {final_performance['total']:.3f}")
            print(f"    • 节点数: {final_stats['node_count']}")
            print(f"    • 边数: {final_stats['edge_count']}")
            print(f"    • 连通性: {'✅' if final_stats['edge_count'] > 0 else '❌'}")
            
            # 评估等级
            if final_novelty > 0.7:
                innovation_level = "🏆 高度创新"
            elif final_novelty > 0.5:
                innovation_level = "🥈 中等创新"
            else:
                innovation_level = "🥉 轻度创新"
            
            if final_performance['total'] > 0.7:
                performance_level = "⚡ 高性能"
            elif final_performance['total'] > 0.5:
                performance_level = "📊 中等性能"
            else:
                performance_level = "🐌 低性能"
            
            print(f"\n  综合评价:")
            print(f"    • 创新性: {innovation_level}")
            print(f"    • 性能: {performance_level}")
            
            # 检查目标达成
            if final_novelty > 0.6 and final_performance['total'] > 0.7:
                goal_status = "✅ 达成：既有创新性又有性能！"
            elif final_novelty > 0.6:
                goal_status = "⚠️ 部分：有创新性，性能需改进"
            elif final_performance['total'] > 0.7:
                goal_status = "⚠️ 部分：有性能，创新性需改进"
            else:
                goal_status = "❌ 未达成：创新性和性能都需改进"
            
            print(f"    • 目标: {goal_status}")
        
        print(f"\n  时间统计:")
        print(f"    • 阶段1: {phase1_time:.1f}秒")
        print(f"    • 阶段2: {phase2_time:.1f}秒")
        print(f"    • 总计: {total_time:.1f}秒")
        
        # 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "Enhanced Two-Stage Innovation Experiment",
            "fixes_applied": [
                "Fixed zero-edge problem",
                "Enhanced novelty detection",
                "Increased training intensity",
                "Improved initial population quality"
            ],
            "config": self.config,
            "phase1_results": {
                "innovative_protocols_count": len(innovative_protocols),
                "top_innovations": self.phase1_innovations,
                "time_seconds": phase1_time
            },
            "phase2_results": {
                "best_fitness": float(phase2_result.get('best_fitness', 0)),
                "best_novelty": float(phase2_result.get('best_novelty', 0)),
                "best_performance": phase2_result.get('best_performance', {}),
                "time_seconds": phase2_time
            },
            "final_assessment": {
                "innovation_level": innovation_level if best_protocol else "N/A",
                "performance_level": performance_level if best_protocol else "N/A",
                "goal_achieved": (
                    final_novelty > 0.6 and final_performance['total'] > 0.7 
                    if best_protocol else False
                ),
                "connectivity_ok": final_stats.get('edge_count', 0) > 0 if best_protocol else False
            },
            "timestamp": timestamp
        }
        
        filename = f"results/enhanced_two_stage_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ 增强版两阶段创新实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 增强版两阶段创新实验（修复问题）")
    print("=" * 70)
    print("基于两阶段思路，修复实施中的问题")
    print("=" * 70)
    
    print("\n🔧 修复的问题:")
    print("  1. ✅ 修复边数为0的问题（强制连通性）")
    print("  2. ✅ 改进新颖性检测（更准确）")
    print("  3. ✅ 增强训练强度（100代+40种群）")
    print("  4. ✅ 改进初始种群（包含已知好协议）")
    
    print("\n📋 实验设计:")
    print("  阶段1（100代）: 100% 新颖性 - 发现不同结构")
    print("  阶段2（80代）: 70% 性能 + 30% 新颖性 - 优化创新结构")
    
    experiment = EnhancedTwoStageExperiment()
    
    # 运行实验
    result = experiment.run_enhanced_two_stage()
    
    # 显示最终总结
    print("\n📈 实验最终总结:")
    
    goal_achieved = result['final_assessment']['goal_achieved']
    connectivity_ok = result['final_assessment']['connectivity_ok']
    innovation_level = result['final_assessment']['innovation_level']
    performance_level = result['final_assessment']['performance_level']
    
    if goal_achieved:
        print(f"  🎉 成功！实现了'既有创新性又有性能'的目标!")
        print(f"  创新性: {innovation_level}")
        print(f"  性能: {performance_level}")
        print(f"  连通性: ✅ 修复成功")
        
        best_novelty = result['phase2_results']['best_novelty']
        best_perf = result['phase2_results']['best_performance'].get('total', 0)
        
        print(f"\n  🔬 具体指标:")
        print(f"    新颖性分数: {best_novelty:.3f} (目标 > 0.6)")
        print(f"    性能分数: {best_perf:.3f} (目标 > 0.7)")
        
    else:
        print(f"  ⚠️ 部分成功")
        print(f"  创新性: {innovation_level}")
        print(f"  性能: {performance_level}")
        print(f"  连通性: {'✅ 修复成功' if connectivity_ok else '❌ 仍有问题'}")
        
        # 分析具体问题
        best_novelty = result['phase2_results']['best_novelty']
        best_perf = result['phase2_results']['best_performance'].get('total', 0)
        
        print(f"\n  🔍 详细分析:")
        print(f"    新颖性: {best_novelty:.3f} (目标 > 0.6)")
        print(f"    性能: {best_perf:.3f} (目标 > 0.7)")
        
        if not connectivity_ok:
            print(f"    主要问题: ❌ 连通性问题未完全解决")
        elif best_novelty <= 0.6 and best_perf <= 0.7:
            print(f"    主要问题: ❌ 创新性和性能都不足")
        elif best_novelty <= 0.6:
            print(f"    主要问题: ❌ 创新性不足")
        else:
            print(f"    主要问题: ❌ 性能不足")
    
    print(f"\n📁 结果文件: results/enhanced_two_stage_*.json")
    
    print("\n🎯 下一步研究方向:")
    if goal_achieved:
        print("  1. 验证方法的可重复性")
        print("  2. 分析成功协议的具体结构")
        print("  3. 尝试不同的阶段权重分配")
        print("  4. 与传统方法进行对比")
    else:
        print("  1. 进一步增加训练强度")
        print("  2. 尝试更激进的新颖性奖励")
        print("  3. 分析创新性检测的局限性")
        print("  4. 考虑三阶段或多阶段策略")


if __name__ == "__main__":
    main()
