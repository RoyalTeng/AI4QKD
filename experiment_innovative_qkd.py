#!/usr/bin/env python3
"""
创新性QKD协议设计实验
核心思想：不给特征提示，只给性能目标，让AI真正创新
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


class InnovativeProtocolDesigner:
    """创新性协议设计器"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.base_evaluate = self.agent.evaluate_protocol
        
        # 已知协议库（用于新颖性检测）
        self.known_protocols = self._load_known_protocols()
        
        # 创新特征库
        self.innovation_history = []
        
        # 性能目标权重
        self.performance_weights = {
            "security": 0.35,      # 安全性最重要
            "distance": 0.25,      # 传输距离
            "key_rate": 0.20,      # 密钥率
            "robustness": 0.15,    # 鲁棒性
            "cost": 0.05           # 成本（负权重）
        }
    
    def _load_known_protocols(self):
        """加载已知协议作为新颖性对比基准"""
        known = []
        
        # BB84
        bb84 = ProtocolGraph.create_bb84()
        known.append(bb84)
        
        # 简化MDI（仅用于对比）
        mdi = ProtocolGraph(name="MDI Simplified")
        alice = mdi.add_node(NodeType.QSP, {'state': 'single_photon'}, Party.ALICE)
        bob = mdi.add_node(NodeType.QSP, {'state': 'single_photon'}, Party.BOB)
        charlie = mdi.add_node(NodeType.QM, {'basis': 'bell'}, Party.CHARLIE)
        mdi.add_edge(alice, charlie, EdgeType.QUANTUM)
        mdi.add_edge(bob, charlie, EdgeType.QUANTUM)
        known.append(mdi)
        
        return known
    
    def evaluate_performance(self, protocol: ProtocolGraph) -> dict:
        """评估协议性能（不基于具体特征）"""
        stats = protocol.get_statistics()
        
        # 模拟性能评估（实际应用中需要真实仿真）
        performance = {
            "security": self._estimate_security(protocol, stats),
            "distance": self._estimate_distance(protocol, stats),
            "key_rate": self._estimate_key_rate(protocol, stats),
            "robustness": self._estimate_robustness(protocol, stats),
            "cost": self._estimate_cost(protocol, stats)
        }
        
        return performance
    
    def _estimate_security(self, protocol: ProtocolGraph, stats: dict) -> float:
        """估计安全性（基于结构复杂性等启发式）"""
        base_security = 0.3
        
        # 多样性奖励
        node_types = set(stats.get('node_stats', {}).keys())
        if len(node_types) >= 4:
            base_security += 0.1
        
        # 冗余性奖励
        if stats.get('edge_count', 0) > stats.get('node_count', 0):
            base_security += 0.05
        
        # 经典通信存在性（通常增加安全性）
        if 'classical_channel' in str(stats.get('node_stats', {})):
            base_security += 0.1
        
        # 测量多样性
        if stats.get('node_stats', {}).get('quantum_measurement', 0) >= 2:
            base_security += 0.05
        
        return min(base_security, 0.9)
    
    def _estimate_distance(self, protocol: ProtocolGraph, stats: dict) -> float:
        """估计最大传输距离"""
        base_distance = 0.5
        
        # 量子信道数量和质量
        qc_count = stats.get('node_stats', {}).get('quantum_channel', 0)
        if qc_count >= 2:
            base_distance += 0.2
        
        # 中继节点存在性
        has_charlie = any(
            protocol.graph.nodes[nid]['node'].party == Party.CHARLIE
            for nid in protocol.graph.nodes()
        )
        if has_charlie:
            base_distance += 0.15
        
        # 经典信道支持
        cc_count = stats.get('node_stats', {}).get('classical_channel', 0)
        if cc_count >= 1:
            base_distance += 0.05
        
        return min(base_distance, 0.95)
    
    def _estimate_key_rate(self, protocol: ProtocolGraph, stats: dict) -> float:
        """估计密钥率"""
        base_rate = 0.4
        
        # 并行性（多个发送方/接收方）
        parties = set()
        for nid in protocol.graph.nodes():
            party = protocol.graph.nodes[nid]['node'].party
            if party:
                parties.add(party)
        
        if len(parties) >= 2:
            base_rate += 0.2
        
        # 效率（节点数适中）
        node_count = stats.get('node_count', 0)
        if 5 <= node_count <= 10:
            base_rate += 0.15
        elif node_count > 10:
            base_rate -= 0.1  # 太复杂可能降低速率
        
        # 经典处理能力
        if stats.get('node_stats', {}).get('classical_processing', 0) >= 1:
            base_rate += 0.05
        
        return max(0.1, min(base_rate, 0.9))
    
    def _estimate_robustness(self, protocol: ProtocolGraph, stats: dict) -> float:
        """估计鲁棒性"""
        base_robustness = 0.5
        
        # 冗余路径
        edge_count = stats.get('edge_count', 0)
        node_count = stats.get('node_count', 0)
        
        if edge_count > node_count:  # 有冗余连接
            base_robustness += 0.15
        
        # 备份组件
        qsp_count = stats.get('node_stats', {}).get('quantum_state_preparation', 0)
        if qsp_count >= 2:
            base_robustness += 0.1
        
        # 错误处理机制
        has_verification = stats.get('node_stats', {}).get('classical_verification', 0) > 0
        if has_verification:
            base_robustness += 0.1
        
        return min(base_robustness, 0.95)
    
    def _estimate_cost(self, protocol: ProtocolGraph, stats: dict) -> float:
        """估计成本（越低越好，所以返回负值）"""
        base_cost = 0.0
        
        # 节点数成本
        node_count = stats.get('node_count', 0)
        base_cost += node_count * 0.03
        
        # 特殊组件成本
        special_nodes = ['quantum_gate', 'quantum_detector', 'quantum_to_classical']
        for node_type in special_nodes:
            count = stats.get('node_stats', {}).get(node_type, 0)
            base_cost += count * 0.05
        
        # 复杂性成本
        if node_count > 8:
            base_cost += 0.1
        
        return -min(base_cost, 0.5)  # 负值，成本越高分数越低
    
    def evaluate_novelty(self, protocol: ProtocolGraph) -> float:
        """评估协议新颖性（与已知协议不同）"""
        if not self.known_protocols:
            return 1.0  # 第一个协议，完全新颖
        
        similarities = []
        for known in self.known_protocols:
            similarity = self._compare_protocols(protocol, known)
            similarities.append(similarity)
        
        max_similarity = max(similarities) if similarities else 0.0
        novelty = 1.0 - max_similarity
        
        # 额外奖励完全不同的结构
        if novelty > 0.8:
            novelty = min(novelty * 1.2, 1.0)
        
        return novelty
    
    def _compare_protocols(self, p1: ProtocolGraph, p2: ProtocolGraph) -> float:
        """比较两个协议的相似性（基于图结构）"""
        # 提取图特征
        features1 = self._extract_graph_features(p1)
        features2 = self._extract_graph_features(p2)
        
        # 计算余弦相似性
        all_keys = set(features1.keys()) | set(features2.keys())
        vec1 = np.array([features1.get(k, 0) for k in all_keys])
        vec2 = np.array([features2.get(k, 0) for k in all_keys])
        
        # 避免除零
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return float(similarity)
    
    def _extract_graph_features(self, protocol: ProtocolGraph) -> dict:
        """提取图结构特征"""
        features = defaultdict(float)
        
        # 基本统计
        stats = protocol.get_statistics()
        features['node_count'] = stats.get('node_count', 0) / 20.0  # 归一化
        features['edge_count'] = stats.get('edge_count', 0) / 30.0
        
        # 节点类型分布
        node_stats = stats.get('node_stats', {})
        for node_type, count in node_stats.items():
            features[f'node_{node_type}'] = count / 10.0
        
        # 图拓扑特征
        graph = protocol.graph
        
        # 度分布特征
        if graph.number_of_nodes() > 0:
            degrees = [d for _, d in graph.degree()]
            features['avg_degree'] = np.mean(degrees) / 10.0
            features['max_degree'] = np.max(degrees) / 10.0
        
        # 连通性特征
        if nx.is_weakly_connected(graph):
            features['is_connected'] = 1.0
        
        # 路径特征
        if graph.number_of_nodes() >= 2:
            try:
                # 计算平均最短路径长度
                if nx.is_weakly_connected(graph):
                    avg_path = nx.average_shortest_path_length(graph.to_undirected())
                    features['avg_path_length'] = avg_path / 10.0
            except:
                pass
        
        return dict(features)
    
    def evaluate_structural_elegance(self, protocol: ProtocolGraph) -> float:
        """评估结构优雅性（简洁而有效）"""
        stats = protocol.get_statistics()
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        # 理想比例：边数 ≈ 节点数 * 1.5
        ideal_ratio = 1.5
        actual_ratio = edge_count / node_count if node_count > 0 else 0
        
        ratio_score = 1.0 - min(abs(actual_ratio - ideal_ratio) / ideal_ratio, 1.0)
        
        # 节点数适中奖励（5-12个节点）
        if 5 <= node_count <= 12:
            size_score = 1.0
        elif node_count < 5:
            size_score = node_count / 5.0
        else:
            size_score = max(0, 1.0 - (node_count - 12) / 20.0)
        
        # 对称性奖励（如果适用）
        symmetry_score = self._evaluate_symmetry(protocol)
        
        return (ratio_score * 0.4 + size_score * 0.4 + symmetry_score * 0.2)
    
    def _evaluate_symmetry(self, protocol: ProtocolGraph) -> float:
        """评估协议对称性"""
        # 检查是否有对称的发送方-接收方结构
        alice_nodes = [
            nid for nid in protocol.graph.nodes()
            if protocol.graph.nodes[nid]['node'].party == Party.ALICE
        ]
        bob_nodes = [
            nid for nid in protocol.graph.nodes()
            if protocol.graph.nodes[nid]['node'].party == Party.BOB
        ]
        
        if len(alice_nodes) == len(bob_nodes) and len(alice_nodes) > 0:
            # 检查节点类型对称性
            alice_types = [
                protocol.graph.nodes[nid]['node'].node_type.value
                for nid in alice_nodes
            ]
            bob_types = [
                protocol.graph.nodes[nid]['node'].node_type.value
                for nid in bob_nodes
            ]
            
            if sorted(alice_types) == sorted(bob_types):
                return 0.8  # 高度对称
            else:
                return 0.3  # 部分对称
        else:
            return 0.0  # 不对称
    
    def evaluate_feasibility(self, protocol: ProtocolGraph) -> float:
        """评估技术可行性"""
        stats = protocol.get_statistics()
        feasibility = 0.7  # 基础可行性
        
        # 检查是否有明显不可行的组合
        issues = []
        
        # 量子测量没有输入
        qm_nodes = [
            nid for nid in protocol.graph.nodes()
            if protocol.graph.nodes[nid]['node'].node_type == NodeType.QM
        ]
        for qm in qm_nodes:
            in_edges = list(protocol.graph.in_edges(qm))
            if len(in_edges) == 0:
                issues.append("measurement_no_input")
        
        # 量子态制备没有输出
        qsp_nodes = [
            nid for nid in protocol.graph.nodes()
            if protocol.graph.nodes[nid]['node'].node_type == NodeType.QSP
        ]
        for qsp in qsp_nodes:
            out_edges = list(protocol.graph.out_edges(qsp))
            if len(out_edges) == 0:
                issues.append("source_no_output")
        
        # 应用可行性惩罚
        penalty = len(issues) * 0.1
        feasibility = max(0.3, feasibility - penalty)
        
        return feasibility
    
    def innovative_fitness(self, protocol: ProtocolGraph) -> float:
        """创新性适应度函数（核心）"""
        # 1. 性能评估（40%）
        performance = self.evaluate_performance(protocol)
        performance_score = 0.0
        for metric, weight in self.performance_weights.items():
            performance_score += performance.get(metric, 0) * weight
        
        # 2. 新颖性奖励（30%）
        novelty_score = self.evaluate_novelty(protocol)
        
        # 3. 结构优雅性（20%）
        elegance_score = self.evaluate_structural_elegance(protocol)
        
        # 4. 可行性（10%）
        feasibility_score = self.evaluate_feasibility(protocol)
        
        # 加权总分
        total_score = (
            performance_score * 0.4 +
            novelty_score * 0.3 +
            elegance_score * 0.2 +
            feasibility_score * 0.1
        )
        
        # 记录创新特征
        if novelty_score > 0.7:
            self._record_innovation(protocol, novelty_score)
        
        return min(total_score, 1.0)
    
    def _record_innovation(self, protocol: ProtocolGraph, novelty_score: float):
        """记录创新发现"""
        stats = protocol.get_statistics()
        innovation = {
            "timestamp": time.time(),
            "novelty_score": novelty_score,
            "node_count": stats.get('node_count', 0),
            "edge_count": stats.get('edge_count', 0),
            "node_stats": stats.get('node_stats', {}),
            "performance": self.evaluate_performance(protocol)
        }
        self.innovation_history.append(innovation)
        
        # 添加到已知协议库（用于后续新颖性检测）
        self.known_protocols.append(protocol)
    
    def run_innovative_experiment(self, iterations: int = 150, population_size: int = 25) -> dict:
        """运行创新性实验"""
        print("\n" + "=" * 70)
        print("🚀 创新性QKD协议设计实验")
        print("=" * 70)
        print("核心原则：不给特征提示，只给性能目标，让AI真正创新")
        print("=" * 70)
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用创新性适应度函数
        self.agent.evaluate_protocol = self.innovative_fitness
        
        # 1. 初始化种群（完全随机，不添加已知协议）
        print(f"\n1. 🧬 初始化创新种群 ({population_size}个完全随机协议)...")
        self.agent.population = []
        
        for i in range(population_size):
            random_protocol = self.agent.generate_random_protocol()
            random_protocol.name = f"Random_Protocol_{i+1}"
            self.agent.population.append(random_protocol)
        
        print(f"   种群初始化完成（完全随机起点）")
        
        # 2. 配置训练参数（鼓励探索）
        self.agent.config.max_iterations = iterations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.5  # 高变异率鼓励探索
        self.agent.config.elite_size = 2       # 小精英集，避免过早收敛
        self.agent.config.crossover_rate = 0.3
        
        # 3. 运行创新性训练
        print(f"\n2. 🧠 开始创新性训练 ({iterations}代)...")
        print(f"   目标：发现全新、高性能、优雅的QKD协议")
        
        result = self.agent.train(iterations=iterations, population_size=population_size)
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 4. 分析结果
        print("\n3. 📊 创新性结果分析...")
        
        best_fitness = result.get('best_fitness', 0)
        best_protocol = result.get('best_protocol')
        
        if best_protocol:
            best_stats = best_protocol.get_statistics()
            best_performance = self.evaluate_performance(best_protocol)
            best_novelty = self.evaluate_novelty(best_protocol)
            best_elegance = self.evaluate_structural_elegance(best_protocol)
            
            print(f"   最佳创新适应度: {best_fitness:.4f}")
            print(f"   新颖性分数: {best_novelty:.3f}")
            print(f"   结构优雅性: {best_elegance:.3f}")
            print(f"   协议节点数: {best_stats['node_count']}")
            print(f"   协议边数: {best_stats['edge_count']}")
            
            print(f"\n   🎯 性能指标:")
            for metric, score in best_performance.items():
                print(f"     • {metric}: {score:.3f}")
            
            # 创新特征分析
            print(f"\n   💡 创新特征:")
            if best_novelty > 0.8:
                print(f"     • 高度新颖: ✅ (分数 {best_novelty:.3f})")
            elif best_novelty > 0.6:
                print(f"     • 中等新颖: ⚠️ (分数 {best_novelty:.3f})")
            else:
                print(f"     • 低新颖性: ❌ (分数 {best_novelty:.3f})")
            
            # 与已知协议对比
            print(f"\n   🔄 与已知协议对比:")
            similarities = []
            for known in self.known_protocols[:3]:  # 前3个已知协议
                similarity = self._compare_protocols(best_protocol, known)
                similarities.append(similarity)
            
            avg_similarity = np.mean(similarities) if similarities else 0.0
            print(f"     平均相似度: {avg_similarity:.3f}")
            if avg_similarity < 0.3:
                print(f"     状态: ✅ 高度不同（可能是新协议）")
            elif avg_similarity < 0.6:
                print(f"     状态: ⚠️ 部分不同")
            else:
                print(f"     状态: ❌ 高度相似（可能是已知协议变体）")
        
        # 5. 创新发现统计
        print(f"\n4. 📈 创新发现统计...")
        print(f"   总创新记录: {len(self.innovation_history)}")
        
        novelty_scores = []
        top_innovations = []
        
        if self.innovation_history:
            novelty_scores = [float(i['novelty_score']) for i in self.innovation_history]
            avg_novelty = np.mean(novelty_scores)
            max_novelty = np.max(novelty_scores)
            
            print(f"   平均新颖性: {avg_novelty:.3f}")
            print(f"   最高新颖性: {max_novelty:.3f}")
            
            # 按新颖性排序
            top_innovations = sorted(
                self.innovation_history,
                key=lambda x: x['novelty_score'],
                reverse=True
            )[:3]
            
            print(f"\n   🏆 最具创新性的3个发现:")
            for i, innovation in enumerate(top_innovations, 1):
                print(f"     {i}. 新颖性: {innovation['novelty_score']:.3f}")
                print(f"        节点数: {innovation['node_count']}, 边数: {innovation['edge_count']}")
        
        # 6. 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "Innovative QKD Protocol Design",
            "philosophy": "No feature hints, only performance goals, true innovation",
            "config": {
                "iterations": iterations,
                "population_size": population_size,
                "mutation_rate": float(self.agent.config.mutation_rate),
                "performance_weights": {k: float(v) for k, v in self.performance_weights.items()}
            },
            "ai_training_result": {
                "best_fitness": float(best_fitness),
                "best_protocol_stats": best_stats if best_protocol else {},
                "best_performance": {k: float(v) for k, v in best_performance.items()} if best_protocol else {},
                "best_novelty": float(best_novelty) if best_protocol else 0.0,
                "best_elegance": float(best_elegance) if best_protocol else 0.0,
                "fitness_history": [float(f) for f in result.get('fitness_history', [])],
                "iterations": iterations
            },
            "innovation_discoveries": {
                "total_count": len(self.innovation_history),
                "novelty_scores": novelty_scores,
                "top_innovations": top_innovations
            },
            "comparison_with_known": {
                "average_similarity": float(avg_similarity) if best_protocol else 0.0,
                "is_likely_new": bool(avg_similarity < 0.3) if best_protocol else False
            },
            "timestamp": timestamp
        }
        
        filename = f"results/innovative_qkd_experiment_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ 创新性QKD协议设计实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 创新性QKD协议设计实验")
    print("=" * 70)
    print("范式转变：从'特征匹配'到'真正创新'")
    print("=" * 70)
    
    print("\n📋 实验设计原则:")
    print("  1. ❌ 不给特征提示（不告诉AI'应该有干涉仪'等）")
    print("  2. ✅ 只给性能目标（安全性、距离、速率等）")
    print("  3. ✅ 奖励新颖性（与已知协议不同）")
    print("  4. ✅ 奖励结构优雅性（简洁而有效）")
    print("  5. ✅ 检查技术可行性")
    
    experiment = InnovativeProtocolDesigner()
    
    # 实验参数（鼓励探索）
    iterations = 150  # 更多迭代鼓励充分探索
    population_size = 25  # 更大种群增加多样性
    
    print(f"\n实验配置:")
    print(f"  迭代次数: {iterations}（鼓励充分探索）")
    print(f"  种群大小: {population_size}（增加多样性）")
    print(f"  变异率: 0.5（高变异鼓励探索）")
    print(f"  开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行实验
    result = experiment.run_innovative_experiment(
        iterations=iterations,
        population_size=population_size
    )
    
    # 显示总结
    print("\n📈 实验总结:")
    print(f"  最佳创新适应度: {result['ai_training_result']['best_fitness']:.4f}")
    print(f"  最佳新颖性分数: {result['ai_training_result']['best_novelty']:.3f}")
    
    is_likely_new = result['comparison_with_known']['is_likely_new']
    avg_similarity = result['comparison_with_known']['average_similarity']
    
    if is_likely_new:
        print(f"  协议类型: ✅ 可能是全新协议!")
        print(f"  与已知协议相似度: {avg_similarity:.3f}（低相似度）")
        
        # 分析创新性
        novelty = result['ai_training_result']['best_novelty']
        if novelty > 0.8:
            print(f"  创新等级: 🏆 高度创新")
        elif novelty > 0.6:
            print(f"  创新等级: 🥈 中等创新")
        else:
            print(f"  创新等级: 🥉 轻度创新")
    else:
        print(f"  协议类型: ⚠️ 可能是已知协议变体")
        print(f"  与已知协议相似度: {avg_similarity:.3f}（较高相似度）")
    
    print(f"\n📁 结果文件: results/innovative_qkd_experiment_*.json")
    
    print("\n🎯 下一步研究方向:")
    if is_likely_new:
        print("  1. 深入分析发现的'可能是新协议'的结构")
        print("  2. 运行详细仿真验证其真实性能")
        print("  3. 与传统协议进行对比分析")
        print("  4. 尝试理解AI的创新思路")
    else:
        print("  1. 进一步增加探索性（更高变异率，更大种群）")
        print("  2. 调整新颖性奖励权重")
        print("  3. 添加更多'意外发现'奖励机制")
        print("  4. 尝试不同的性能目标组合")


if __name__ == "__main__":
    main()