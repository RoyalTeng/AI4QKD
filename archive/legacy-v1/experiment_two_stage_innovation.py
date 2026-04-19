#!/usr/bin/env python3
"""
两阶段创新实验（基于现有图结构）
阶段1：纯创新探索（100%新颖性）
阶段2：性能优化（70%性能 + 30%新颖性）
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


class TwoStageInnovationExperiment:
    """两阶段创新实验"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.base_evaluate = self.agent.evaluate_protocol
        
        # 已知协议库（用于新颖性检测）
        self.known_protocols = self._load_known_protocols()
        
        # 阶段1的创新发现
        self.phase1_innovations = []
        
        # 阶段2的优化结果
        self.phase2_results = []
    
    def _load_known_protocols(self):
        """加载已知协议库"""
        known = []
        
        # BB84
        bb84 = ProtocolGraph.create_bb84()
        known.append(bb84)
        
        # 简化MDI
        mdi = ProtocolGraph(name="MDI Simplified")
        alice = mdi.add_node(NodeType.QSP, {'state': 'single_photon'}, Party.ALICE)
        bob = mdi.add_node(NodeType.QSP, {'state': 'single_photon'}, Party.BOB)
        charlie = mdi.add_node(NodeType.QM, {'basis': 'bell'}, Party.CHARLIE)
        mdi.add_edge(alice, charlie, EdgeType.QUANTUM)
        mdi.add_edge(bob, charlie, EdgeType.QUANTUM)
        known.append(mdi)
        
        # 简化TF
        tf = ProtocolGraph(name="TF Simplified")
        alice = tf.add_node(NodeType.QSP, {'state': 'coherent'}, Party.ALICE)
        bob = tf.add_node(NodeType.QSP, {'state': 'coherent'}, Party.BOB)
        channel1 = tf.add_node(NodeType.QC, {'distance': 300}, None)
        channel2 = tf.add_node(NodeType.QC, {'distance': 300}, None)
        interferometer = tf.add_node(NodeType.QG, {'gate_type': 'beam_splitter'}, Party.CHARLIE)
        tf.add_edge(alice, channel1, EdgeType.QUANTUM)
        tf.add_edge(bob, channel2, EdgeType.QUANTUM)
        tf.add_edge(channel1, interferometer, EdgeType.QUANTUM)
        tf.add_edge(channel2, interferometer, EdgeType.QUANTUM)
        known.append(tf)
        
        return known
    
    def extract_protocol_features(self, protocol: ProtocolGraph) -> dict:
        """提取协议特征向量"""
        stats = protocol.get_statistics()
        features = defaultdict(float)
        
        # 基本统计
        features['node_count'] = stats.get('node_count', 0) / 20.0
        features['edge_count'] = stats.get('edge_count', 0) / 30.0
        
        # 节点类型分布
        node_stats = stats.get('node_stats', {})
        for node_type, count in node_stats.items():
            features[f'node_{node_type}'] = count / 10.0
        
        # 参与方分布
        party_stats = stats.get('party_stats', {})
        for party, count in party_stats.items():
            features[f'party_{party}'] = count / 5.0
        
        # 图拓扑特征
        graph = protocol.graph
        
        # 度分布
        if graph.number_of_nodes() > 0:
            degrees = [d for _, d in graph.degree()]
            features['avg_degree'] = np.mean(degrees) / 10.0
            features['max_degree'] = np.max(degrees) / 10.0
            features['min_degree'] = np.min(degrees) / 10.0
        
        # 连通性
        try:
            if nx.is_weakly_connected(graph):
                features['is_connected'] = 1.0
                # 平均路径长度
                undirected = graph.to_undirected()
                if nx.is_connected(undirected):
                    avg_path = nx.average_shortest_path_length(undirected)
                    features['avg_path_length'] = avg_path / 10.0
        except:
            pass
        
        return dict(features)
    
    def evaluate_novelty(self, protocol: ProtocolGraph) -> float:
        """评估协议新颖性（与已知协议不同）"""
        if not self.known_protocols:
            return 1.0
        
        # 提取特征向量
        my_features = self.extract_protocol_features(protocol)
        
        # 计算与每个已知协议的相似性
        similarities = []
        for known in self.known_protocols:
            known_features = self.extract_protocol_features(known)
            similarity = self._cosine_similarity(my_features, known_features)
            similarities.append(similarity)
        
        # 新颖性 = 1 - 最大相似性
        max_similarity = max(similarities) if similarities else 0.0
        novelty = 1.0 - max_similarity
        
        # 额外奖励高度新颖
        if novelty > 0.8:
            novelty = min(novelty * 1.2, 1.0)
        
        return novelty
    
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
    
    def evaluate_performance(self, protocol: ProtocolGraph) -> dict:
        """评估协议性能"""
        # 使用基础评估
        base_fitness = self.base_evaluate(protocol)
        
        # 启发式性能指标
        stats = protocol.get_statistics()
        
        performance = {
            'base_fitness': base_fitness,
            'security': self._estimate_security(stats),
            'efficiency': self._estimate_efficiency(stats),
            'robustness': self._estimate_robustness(stats),
            'complexity_penalty': self._estimate_complexity_penalty(stats)
        }
        
        # 综合性能分数
        performance['total'] = (
            performance['base_fitness'] * 0.4 +
            performance['security'] * 0.25 +
            performance['efficiency'] * 0.20 +
            performance['robustness'] * 0.15 -
            performance['complexity_penalty'] * 0.1
        )
        
        return performance
    
    def _estimate_security(self, stats: dict) -> float:
        """估计安全性"""
        base = 0.5
        
        # 多样性奖励
        node_types = len(stats.get('node_stats', {}))
        if node_types >= 3:
            base += 0.15
        
        # 经典验证存在性
        if stats.get('node_stats', {}).get('classical_verification', 0) > 0:
            base += 0.1
        
        # 测量多样性
        if stats.get('node_stats', {}).get('quantum_measurement', 0) >= 2:
            base += 0.05
        
        return min(base, 0.95)
    
    def _estimate_efficiency(self, stats: dict) -> float:
        """估计效率"""
        base = 0.6
        
        # 节点数适中
        node_count = stats.get('node_count', 0)
        if 4 <= node_count <= 8:
            base += 0.2
        elif node_count < 4:
            base += node_count * 0.05
        else:
            base -= (node_count - 8) * 0.05
        
        # 边数适中
        edge_count = stats.get('edge_count', 0)
        if edge_count >= node_count and edge_count <= node_count * 1.5:
            base += 0.1
        
        return max(0.3, min(base, 0.95))
    
    def _estimate_robustness(self, stats: dict) -> float:
        """估计鲁棒性"""
        base = 0.7
        
        # 冗余连接
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        if edge_count > node_count:
            redundancy = (edge_count - node_count) / node_count
            base += min(redundancy * 0.2, 0.15)
        
        # 备份组件
        for node_type, count in stats.get('node_stats', {}).items():
            if count >= 2:
                base += 0.03
        
        return min(base, 0.95)
    
    def _estimate_complexity_penalty(self, stats: dict) -> float:
        """估计复杂度惩罚"""
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        # 基础复杂度
        complexity = (node_count * 0.03) + (edge_count * 0.02)
        
        # 特殊节点惩罚
        special_nodes = ['quantum_gate', 'quantum_detector', 'quantum_to_classical']
        for node_type in special_nodes:
            count = stats.get('node_stats', {}).get(node_type, 0)
            complexity += count * 0.05
        
        return min(complexity, 0.5)
    
    def phase1_innovation_fitness(self, protocol: ProtocolGraph) -> float:
        """阶段1适应度函数：100%新颖性"""
        novelty = self.evaluate_novelty(protocol)
        
        # 额外奖励：结构多样性
        stats = protocol.get_statistics()
        node_types = len(stats.get('node_stats', {}))
        edge_count = stats.get('edge_count', 0)
        node_count = stats.get('node_count', 0)
        
        diversity_bonus = 0.0
        if node_types >= 4:
            diversity_bonus += 0.1
        if edge_count > node_count:  # 有冗余连接
            diversity_bonus += 0.05
        
        total = novelty + diversity_bonus
        return min(total, 1.0)
    
    def phase2_performance_fitness(self, protocol: ProtocolGraph) -> float:
        """阶段2适应度函数：70%性能 + 30%新颖性"""
        performance = self.evaluate_performance(protocol)
        novelty = self.evaluate_novelty(protocol)
        
        # 70%性能 + 30%新颖性
        total = performance['total'] * 0.7 + novelty * 0.3
        
        # 特别奖励：如果既有高性能又有高新颖性
        if performance['total'] > 0.7 and novelty > 0.6:
            total = min(total + 0.1, 1.0)
        
        return total
    
    def run_phase1_innovation_exploration(self, generations: int = 50, population_size: int = 25) -> list:
        """运行阶段1：创新探索"""
        print("\n" + "=" * 70)
        print("🚀 阶段1：纯创新探索")
        print("适应度：100% 新颖性")
        print("目标：发现尽可能不同的协议结构")
        print("=" * 70)
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用阶段1适应度函数
        self.agent.evaluate_protocol = self.phase1_innovation_fitness
        
        # 1. 初始化种群（完全随机）
        print(f"\n1. 🧬 初始化创新探索种群 ({population_size}个随机协议)...")
        self.agent.population = []
        
        for i in range(population_size):
            random_protocol = self.agent.generate_random_protocol()
            random_protocol.name = f"Phase1_Random_{i}"
            self.agent.population.append(random_protocol)
        
        print(f"   种群初始化完成")
        
        # 2. 配置训练参数（鼓励探索）
        self.agent.config.max_iterations = generations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.6  # 高变异率鼓励探索
        self.agent.config.elite_size = 2       # 小精英集
        self.agent.config.crossover_rate = 0.2
        
        # 3. 运行创新探索
        print(f"\n2. 🔍 开始创新探索 ({generations}代)...")
        
        result = self.agent.train(iterations=generations, population_size=population_size)
        
        # 4. 收集最创新的协议
        print(f"\n3. 📊 收集创新发现...")
        
        # 评估种群中所有协议的新颖性
        novelty_scores = []
        for protocol in self.agent.population:
            novelty = self.evaluate_novelty(protocol)
            performance = self.evaluate_performance(protocol)
            novelty_scores.append((novelty, performance['total'], protocol))
        
        # 按新颖性排序
        novelty_scores.sort(key=lambda x: x[0], reverse=True)
        
        # 选择前10个最创新的协议
        top_innovations = novelty_scores[:10]
        
        print(f"   发现 {len(top_innovations)} 个高度创新的协议")
        print(f"   最高新颖性: {top_innovations[0][0]:.3f}")
        print(f"   平均新颖性: {np.mean([n for n, _, _ in top_innovations]):.3f}")
        
        # 保存创新发现
        self.phase1_innovations = [(proto.name, novelty, perf) for novelty, perf, proto in top_innovations]
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 返回最创新的协议（用于阶段2）
        phase1_results = [proto for _, _, proto in top_innovations]
        
        print(f"\n✅ 阶段1完成：发现 {len(phase1_results)} 个创新协议")
        
        return phase1_results
    
    def run_phase2_performance_optimization(self, innovative_protocols: list, 
                                           generations: int = 50, population_size: int = 20) -> dict:
        """运行阶段2：性能优化"""
        print("\n" + "=" * 70)
        print("🚀 阶段2：性能优化")
        print("适应度：70% 性能 + 30% 新颖性")
        print("目标：优化创新结构的性能")
        print("=" * 70)
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用阶段2适应度函数
        self.agent.evaluate_protocol = self.phase2_performance_fitness
        
        # 1. 初始化种群（从阶段1的创新协议开始）
        print(f"\n1. 🧬 初始化性能优化种群...")
        print(f"   从阶段1的 {len(innovative_protocols)} 个创新协议开始")
        
        self.agent.population = []
        
        # 添加阶段1的创新协议
        for i, protocol in enumerate(innovative_protocols):
            protocol.name = f"Phase2_Innovative_{i}"
            self.agent.population.append(protocol)
        
        # 如果不够，添加随机协议
        while len(self.agent.population) < population_size:
            random_protocol = self.agent.generate_random_protocol()
            random_protocol.name = f"Phase2_Random_{len(self.agent.population)}"
            self.agent.population.append(random_protocol)
        
        print(f"   种群大小: {len(self.agent.population)}")
        
        # 2. 配置训练参数（平衡探索和优化）
        self.agent.config.max_iterations = generations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.4  # 中等变异率
        self.agent.config.elite_size = 4       # 中等精英集
        self.agent.config.crossover_rate = 0.3
        
        # 3. 运行性能优化
        print(f"\n2. ⚡ 开始性能优化 ({generations}代)...")
        
        result = self.agent.train(iterations=generations, population_size=population_size)
        
        # 4. 分析结果
        print(f"\n3. 📊 性能优化结果...")
        
        best_fitness = result.get('best_fitness', 0)
        best_protocol = result.get('best_protocol')
        
        if best_protocol:
            best_novelty = self.evaluate_novelty(best_protocol)
            best_performance = self.evaluate_performance(best_protocol)
            best_stats = best_protocol.get_statistics()
            
            print(f"   最佳适应度: {best_fitness:.4f}")
            print(f"   新颖性: {best_novelty:.3f}")
            print(f"   性能: {best_performance['total']:.3f}")
            print(f"   协议节点数: {best_stats['node_count']}")
            print(f"   协议边数: {best_stats['edge_count']}")
            
            # 与阶段1对比
            if self.phase1_innovations:
                phase1_best_novelty = self.phase1_innovations[0][1]
                phase1_best_perf = self.phase1_innovations[0][2]
                
                print(f"\n   🔄 与阶段1最佳对比:")
                print(f"     新颖性: {phase1_best_novelty:.3f} → {best_novelty:.3f}")
                print(f"     性能: {phase1_best_perf:.3f} → {best_performance['total']:.3f}")
                
                novelty_change = best_novelty - phase1_best_novelty
                perf_change = best_performance['total'] - phase1_best_perf
                
                print(f"     变化: 新颖性 {novelty_change:+.3f}, 性能 {perf_change:+.3f}")
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 保存阶段2结果
        self.phase2_results = {
            'best_fitness': best_fitness,
            'best_protocol': best_protocol,
            'best_novelty': best_novelty if best_protocol else 0,
            'best_performance': best_performance if best_protocol else {}
        }
        
        print(f"\n✅ 阶段2完成：优化创新协议的性能")
        
        return self.phase2_results
    
    def run_two_stage_experiment(self, phase1_gens=50, phase2_gens=50) -> dict:
        """运行完整的两阶段实验"""
        print("=" * 70)
        print("🎯 两阶段创新实验")
        print("=" * 70)
        print("阶段1：纯创新探索（100%新颖性）")
        print("阶段2：性能优化（70%性能 + 30%新颖性）")
        print("=" * 70)
        
        start_time = time.time()
        
        # 阶段1：创新探索
        phase1_start = time.time()
        innovative_protocols = self.run_phase1_innovation_exploration(
            generations=phase1_gens,
            population_size=25
        )
        phase1_time = time.time() - phase1_start
        
        # 阶段2：性能优化
        phase2_start = time.time()
        phase2_result = self.run_phase2_performance_optimization(
            innovative_protocols=innovative_protocols,
            generations=phase2_gens,
            population_size=20
        )
        phase2_time = time.time() - phase2_start
        
        total_time = time.time() - start_time
        
        # 综合结果分析
        print("\n" + "=" * 70)
        print("📈 两阶段实验综合结果")
        print("=" * 70)
        
        best_protocol = phase2_result.get('best_protocol')
        if best_protocol:
            final_novelty = self.evaluate_novelty(best_protocol)
            final_performance = self.evaluate_performance(best_protocol)
            final_stats = best_protocol.get_statistics()
            
            print(f"  最终协议:")
            print(f"    • 适应度: {phase2_result['best_fitness']:.4f}")
            print(f"    • 新颖性: {final_novelty:.3f}")
            print(f"    • 性能: {final_performance['total']:.3f}")
            print(f"    • 节点数: {final_stats['node_count']}")
            print(f"    • 边数: {final_stats['edge_count']}")
            
            # 评估创新性等级
            if final_novelty > 0.8:
                innovation_level = "🏆 高度创新"
            elif final_novelty > 0.6:
                innovation_level = "🥈 中等创新"
            elif final_novelty > 0.4:
                innovation_level = "🥉 轻度创新"
            else:
                innovation_level = "🔍 低创新性"
            
            # 评估性能等级
            if final_performance['total'] > 0.8:
                performance_level = "⚡ 高性能"
            elif final_performance['total'] > 0.6:
                performance_level = "📊 中等性能"
            else:
                performance_level = "🐌 低性能"
            
            print(f"\n  综合评价:")
            print(f"    • 创新性: {innovation_level}")
            print(f"    • 性能: {performance_level}")
            
            # 检查是否实现了"既有创新性又有性能"
            if final_novelty > 0.6 and final_performance['total'] > 0.7:
                print(f"    • 目标达成: ✅ 既有创新性又有性能!")
            elif final_novelty > 0.6:
                print(f"    • 目标: ⚠️ 有创新性但性能需改进")
            elif final_performance['total'] > 0.7:
                print(f"    • 目标: ⚠️ 有性能但创新性不足")
            else:
                print(f"    • 目标: ❌ 创新性和性能都需改进")
        
        print(f"\n  时间统计:")
        print(f"    • 阶段1: {phase1_time:.1f}秒")
        print(f"    • 阶段2: {phase2_time:.1f}秒")
        print(f"    • 总计: {total_time:.1f}秒")
        
        # 保存完整结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "Two-Stage Innovation Experiment",
            "philosophy": "Phase1: 100% novelty, Phase2: 70% performance + 30% novelty",
            "config": {
                "phase1_generations": phase1_gens,
                "phase2_generations": phase2_gens,
                "phase1_population": 25,
                "phase2_population": 20
            },
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
                )
            },
            "timestamp": timestamp
        }
        
        filename = f"results/two_stage_innovation_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ 两阶段创新实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 两阶段创新实验（基于现有图结构）")
    print("=" * 70)
    print("解决'新颖性-性能权衡'问题的聪明方案")
    print("=" * 70)
    
    print("\n📋 实验设计:")
    print("  阶段1（50代）: 100% 新颖性 - 发现不同结构")
    print("  阶段2（50代）: 70% 性能 + 30% 新颖性 - 优化创新结构")
    
    experiment = TwoStageInnovationExperiment()
    
    # 运行实验
    result = experiment.run_two_stage_experiment(
        phase1_gens=50,
        phase2_gens=50
    )
    
    # 显示最终总结
    print("\n📈 实验最终总结:")
    
    goal_achieved = result['final_assessment']['goal_achieved']
    innovation_level = result['final_assessment']['innovation_level']
    performance_level = result['final_assessment']['performance_level']
    
    if goal_achieved:
        print(f"  🎉 成功！实现了'既有创新性又有性能'的目标!")
        print(f"  创新性: {innovation_level}")
        print(f"  性能: {performance_level}")
        
        best_novelty = result['phase2_results']['best_novelty']
        best_perf = result['phase2_results']['best_performance'].get('total', 0)
        
        print(f"\n  🔬 具体指标:")
        print(f"    新颖性分数: {best_novelty:.3f} (目标 > 0.6)")
        print(f"    性能分数: {best_perf:.3f} (目标 > 0.7)")
        
    else:
        print(f"  ⚠️ 部分成功，目标未完全达成")
        print(f"  创新性: {innovation_level}")
        print(f"  性能: {performance_level}")
        
        # 分析原因
        best_novelty = result['phase2_results']['best_novelty']
        best_perf = result['phase2_results']['best_performance'].get('total', 0)
        
        print(f"\n  🔍 问题分析:")
        if best_novelty <= 0.6 and best_perf <= 0.7:
            print(f"    问题: 创新性和性能都不足")
            print(f"    建议: 增加两个阶段的训练强度")
        elif best_novelty <= 0.6:
            print(f"    问题: 创新性不足")
            print(f"    建议: 提高阶段1的新颖性奖励")
        else:
            print(f"    问题: 性能不足")
            print(f"    建议: 提高阶段2的性能优化强度")
    
    print(f"\n📁 结果文件: results/two_stage_innovation_*.json")
    
    print("\n🎯 下一步研究方向:")
    if goal_achieved:
        print("  1. 深入分析成功协议的结构")
        print("  2. 验证两阶段方法的可重复性")
        print("  3. 尝试不同的阶段权重分配")
        print("  4. 将成功协议与传统协议对比")
    else:
        print("  1. 调整阶段1的新颖性检测方法")
        print("  2. 增加训练代数和种群大小")
        print("  3. 尝试不同的阶段划分策略")
        print("  4. 分析创新性-性能权衡的具体机制")


if __name__ == "__main__":
    main()