#!/usr/bin/env python3
"""
实验：引导AI算法收敛到MDI-QKD协议

MDI-QKD（Measurement-Device-Independent QKD）特点：
1. 两个发送方（Alice和Bob）发送量子态
2. 一个不可信的测量方（Charlie）进行贝尔态测量
3. 通过经典后处理建立密钥
4. 防御所有测量端的攻击
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from simulator import QuantumSimulator
from ai_agent.enhanced_agent import EnhancedHybridAgent as HybridAgent
import json
import time
import numpy as np
from typing import Dict, List, Any, Optional
import random


class MDIQKDExperiment:
    """MDI-QKD实验设计"""
    
    def __init__(self):
        self.simulator = QuantumSimulator()
        self.agent = HybridAgent()
        
    def create_mdi_qkd_template(self) -> ProtocolGraph:
        """创建MDI-QKD协议模板"""
        protocol = ProtocolGraph(name="MDI-QKD Template")
        
        # MDI-QKD的核心结构
        # 1. 两个发送方：Alice和Bob
        alice_qsp = protocol.add_node(
            node_type=NodeType.QUANTUM_STATE_PREPARATION,
            params={"basis": "X", "state": "|+⟩"},
            party="Alice"
        )
        
        bob_qsp = protocol.add_node(
            node_type=NodeType.QUANTUM_STATE_PREPARATION,
            params={"basis": "Z", "state": "|0⟩"},
            party="Bob"
        )
        
        # 2. 两个量子信道
        channel_to_charlie1 = protocol.add_node(
            node_type=NodeType.QUANTUM_CHANNEL,
            params={"loss": 0.1, "noise": 0.01},
            party="None"
        )
        
        channel_to_charlie2 = protocol.add_node(
            node_type=NodeType.QUANTUM_CHANNEL,
            params={"loss": 0.1, "noise": 0.01},
            party="None"
        )
        
        # 3. 贝尔态测量（Charlie）
        bell_measurement = protocol.add_node(
            node_type=NodeType.QUANTUM_MEASUREMENT,
            params={"basis": "Bell", "measurement_type": "joint"},
            party="Charlie"
        )
        
        # 4. 经典信道（公布测量结果）
        classical_channel = protocol.add_node(
            node_type=NodeType.CLASSICAL_CHANNEL,
            params={"capacity": 1.0, "security": "authenticated"},
            party="None"
        )
        
        # 5. 后处理节点
        post_processing = protocol.add_node(
            node_type=NodeType.CLASSICAL_PROCESSING,
            params={"algorithm": "sifting+error_correction+privacy_amplification"},
            party="Both"
        )
        
        # 添加边（连接节点）
        protocol.add_edge(alice_qsp, channel_to_charlie1, EdgeType.QUANTUM)
        protocol.add_edge(bob_qsp, channel_to_charlie2, EdgeType.QUANTUM)
        protocol.add_edge(channel_to_charlie1, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(channel_to_charlie2, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(bell_measurement, classical_channel, EdgeType.CLASSICAL)
        protocol.add_edge(classical_channel, post_processing, EdgeType.CLASSICAL)
        
        return protocol
    
    def create_mdi_fitness_function(self, protocol: ProtocolGraph) -> float:
        """专门为MDI-QKD设计的适应度函数"""
        stats = protocol.get_statistics()
        
        # 基础适应度（来自标准评估）
        base_fitness = self.agent.evaluate_protocol(protocol)
        
        # MDI-specific特征奖励
        mdi_bonus = 0.0
        
        # 1. 检查是否有贝尔态测量
        has_bell_measurement = False
        for node_id, node in protocol.nodes.items():
            if node.node_type == NodeType.QUANTUM_MEASUREMENT:
                if node.params.get("measurement_type") == "joint":
                    has_bell_measurement = True
                    mdi_bonus += 0.2
        
        # 2. 检查是否有两个发送方
        parties = set()
        for node_id, node in protocol.nodes.items():
            if node.party and node.party != "None":
                parties.add(node.party)
        
        if len(parties) >= 2:  # 至少有两个参与方
            mdi_bonus += 0.1
        
        # 3. 检查是否有经典后处理
        has_post_processing = False
        for node_id, node in protocol.nodes.items():
            if node.node_type == NodeType.CLASSICAL_PROCESSING:
                has_post_processing = True
                mdi_bonus += 0.1
        
        # 4. 结构复杂性奖励（MDI比BB84更复杂）
        complexity_score = min(stats["node_count"] / 10, 0.2)
        mdi_bonus += complexity_score
        
        # 5. 安全性奖励（MDI提供测量设备无关安全性）
        security_bonus = 0.0
        if has_bell_measurement:
            security_bonus = 0.15  # MDI特有的安全性优势
        
        total_fitness = base_fitness + mdi_bonus + security_bonus
        
        # 确保适应度在合理范围内
        return min(total_fitness, 1.0)
    
    def guided_mutation(self, protocol: ProtocolGraph) -> ProtocolGraph:
        """引导式变异：倾向于产生MDI结构"""
        mutated = protocol.copy()
        
        # 随机选择变异操作
        mutation_type = random.choice([
            "add_bell_measurement",
            "add_second_sender", 
            "add_post_processing",
            "standard_mutation"
        ])
        
        if mutation_type == "add_bell_measurement":
            # 添加贝尔态测量节点
            bell_node = mutated.add_node(
                node_type=NodeType.QUANTUM_MEASUREMENT,
                params={"basis": "Bell", "measurement_type": "joint"},
                party="Charlie"
            )
            
            # 连接到现有的量子节点
            quantum_nodes = [
                nid for nid, node in mutated.nodes.items()
                if node.node_type in [NodeType.QUANTUM_STATE_PREPARATION, NodeType.QUANTUM_CHANNEL]
            ]
            
            if quantum_nodes:
                for qnode in random.sample(quantum_nodes, min(2, len(quantum_nodes))):
                    mutated.add_edge(qnode, bell_node, EdgeType.QUANTUM)
        
        elif mutation_type == "add_second_sender":
            # 添加第二个发送方
            bob_node = mutated.add_node(
                node_type=NodeType.QUANTUM_STATE_PREPARATION,
                params={"basis": random.choice(["X", "Z"]), "state": random.choice(["|0⟩", "|1⟩", "|+⟩", "|-⟩"])},
                party="Bob"
            )
            
            # 添加量子信道
            channel_node = mutated.add_node(
                node_type=NodeType.QUANTUM_CHANNEL,
                params={"loss": 0.1, "noise": 0.01},
                party="None"
            )
            
            mutated.add_edge(bob_node, channel_node, EdgeType.QUANTUM)
        
        elif mutation_type == "add_post_processing":
            # 添加后处理节点
            pp_node = mutated.add_node(
                node_type=NodeType.CLASSICAL_PROCESSING,
                params={"algorithm": random.choice(["sifting", "error_correction", "privacy_amplification"])},
                party=random.choice(["Alice", "Bob", "Both"])
            )
            
            # 连接到经典信道
            classical_nodes = [
                nid for nid, node in mutated.nodes.items()
                if node.node_type == NodeType.CLASSICAL_CHANNEL
            ]
            
            if classical_nodes:
                mutated.add_edge(random.choice(classical_nodes), pp_node, EdgeType.CLASSICAL)
        
        else:  # standard_mutation
            # 使用智能体的标准变异
            mutated = self.agent.mutate_protocol(protocol)
        
        return mutated
    
    def train_for_mdi(self, iterations: int = 200, population_size: int = 20) -> Dict:
        """专门训练AI发现MDI-QKD协议"""
        print("=" * 70)
        print("🚀 开始MDI-QKD协议发现实验")
        print("=" * 70)
        
        # 初始化种群
        population = []
        
        # 包含MDI模板作为种子
        mdi_template = self.create_mdi_qkd_template()
        population.append(mdi_template)
        
        # 添加其他随机协议
        for _ in range(population_size - 1):
            population.append(self.agent.generate_random_protocol())
        
        best_protocol = None
        best_fitness = 0.0
        fitness_history = []
        
        for iteration in range(iterations):
            # 评估适应度
            fitness_scores = []
            for protocol in population:
                fitness = self.create_mdi_fitness_function(protocol)
                fitness_scores.append(fitness)
            
            # 选择最佳协议
            best_idx = np.argmax(fitness_scores)
            current_best_fitness = fitness_scores[best_idx]
            current_best_protocol = population[best_idx]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_protocol = current_best_protocol
                print(f"迭代 {iteration+1:3d}: 新最佳适应度 = {best_fitness:.4f}")
            
            fitness_history.append(best_fitness)
            
            # 选择父代（锦标赛选择）
            selected_indices = []
            for _ in range(population_size):
                # 随机选择3个个体，选择适应度最高的
                tournament = random.sample(range(population_size), 3)
                winner = max(tournament, key=lambda i: fitness_scores[i])
                selected_indices.append(winner)
            
            # 生成新一代
            new_population = []
            for idx in selected_indices:
                parent = population[idx]
                
                # 80%概率使用引导变异，20%概率使用标准变异
                if random.random() < 0.8:
                    child = self.guided_mutation(parent)
                else:
                    child = self.agent.mutate_protocol(parent)
                
                new_population.append(child)
            
            population = new_population
            
            # 每50代报告进度
            if (iteration + 1) % 50 == 0:
                stats = best_protocol.get_statistics() if best_protocol else {}
                print(f"--- 第 {iteration+1} 代 ---")
                print(f"   最佳适应度: {best_fitness:.4f}")
                print(f"   协议节点数: {stats.get('node_count', 0)}")
                print(f"   协议边数: {stats.get('edge_count', 0)}")
        
        print("=" * 70)
        print("✅ MDI-QKD实验完成!")
        print("=" * 70)
        
        # 分析最佳协议
        if best_protocol:
            stats = best_protocol.get_statistics()
            
            # 检查MDI特征
            mdi_features = self.analyze_mdi_features(best_protocol)
            
            result = {
                "experiment": "MDI-QKD Protocol Discovery",
                "iterations": iterations,
                "population_size": population_size,
                "best_fitness": best_fitness,
                "best_protocol_stats": stats,
                "mdi_features": mdi_features,
                "fitness_history": fitness_history,
                "timestamp": time.time()
            }
            
            return result
        else:
            return {"error": "No protocol found"}
    
    def analyze_mdi_features(self, protocol: ProtocolGraph) -> Dict:
        """分析协议的MDI特征"""
        features = {
            "has_bell_measurement": False,
            "has_two_senders": False,
            "has_post_processing": False,
            "sender_parties": set(),
            "measurement_nodes": 0,
            "joint_measurements": 0
        }
        
        for node_id, node in protocol.nodes.items():
            # 检查发送方
            if node.node_type == NodeType.QUANTUM_STATE_PREPARATION:
                if node.party and node.party != "None":
                    features["sender_parties"].add(node.party)
            
            # 检查测量节点
            if node.node_type == NodeType.QUANTUM_MEASUREMENT:
                features["measurement_nodes"] += 1
                if node.params.get("measurement_type") == "joint":
                    features["has_bell_measurement"] = True
                    features["joint_measurements"] += 1
            
            # 检查后处理
            if node.node_type == NodeType.CLASSICAL_PROCESSING:
                features["has_post_processing"] = True
        
        features["has_two_senders"] = len(features["sender_parties"]) >= 2
        features["sender_parties"] = list(features["sender_parties"])
        
        # 计算MDI分数
        mdi_score = 0.0
        if features["has_bell_measurement"]:
            mdi_score += 0.4
        if features["has_two_senders"]:
            mdi_score += 0.3
        if features["has_post_processing"]:
            mdi_score += 0.2
        if features["joint_measurements"] >= 1:
            mdi_score += 0.1
        
        features["mdi_score"] = mdi_score
        features["is_mdi_like"] = mdi_score >= 0.7  # 70%相似度阈值
        
        return features
    
    def run_comparison_experiment(self):
        """运行比较实验：标准AI vs MDI引导AI"""
        print("\n" + "=" * 70)
        print("🔬 比较实验：标准AI vs MDI引导AI")
        print("=" * 70)
        
        # 标准AI训练
        print("\n1. 标准AI训练（无MDI引导）...")
        standard_result = self.agent.train(iterations=100, population_size=10)
        
        # MDI引导训练
        print("\n2. MDI引导AI训练...")
        mdi_result = self.train_for_mdi(iterations=100, population_size=10)
        
        # 比较结果
        print("\n" + "=" * 70)
        print("📊 比较结果")
        print("=" * 70)
        
        print(f"\n标准AI:")
        print(f"  最佳适应度: {standard_result.get('best_fitness', 0):.4f}")
        print(f"  最佳协议: {standard_result.get('best_protocol_stats', {}).get('name', 'Unknown')}")
        
        print(f"\nMDI引导AI:")
        print(f"  最佳适应度: {mdi_result.get('best_fitness', 0):.4f}")
        print(f"  MDI分数: {mdi_result.get('mdi_features', {}).get('mdi_score', 0):.2f}")
        print(f"  类似MDI: {'是' if mdi_result.get('mdi_features', {}).get('is_mdi_like', False) else '否'}")
        
        # 保存结果
        timestamp = int(time.time())
        
        standard_filename = f"results/standard_ai_mdi_comparison_{timestamp}.json"
        with open(standard_filename, 'w') as f:
            json.dump(standard_result, f, indent=2, ensure_ascii=False)
        
        mdi_filename = f"results/mdi_guided_ai_result_{timestamp}.json"
        with open(mdi_filename, 'w') as f:
            json.dump(mdi_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存:")
        print(f"  • {standard_filename}")
        print(f"  • {mdi_filename}")
        
        return {
            "standard": standard_result,
            "mdi_guided": mdi_result,
            "comparison": {
                "fitness_improvement": mdi_result.get('best_fitness', 0) - standard_result.get('best_fitness', 0),
                "mdi_achieved": mdi_result.get('mdi_features', {}).get('is_mdi_like', False)
            }
        }


def main():
    """主函数：运行MDI-QKD实验"""
    print("=" * 70)
    print("🎯 AI4QKD: 引导AI发现MDI-QKD协议")
    print("=" * 70)
    
    experiment = MDIQKDExperiment()
    
    # 1. 显示MDI-QKD模板
    print("\n1. 📋 MDI-QKD协议模板:")
    mdi_template = experiment.create_mdi_qkd_template()
    stats = mdi_template.get_statistics()
    print(f"   名称: {stats['name']}")
    print(f"   节点数: {stats['node_count']}")
    print(f"   边数: {stats['edge_count']}")
    
    # 2. 评估MDI模板
    print("\n2. 📊 MDI模板评估:")
    mdi_fitness = experiment.create_mdi_fitness_function(mdi_template)
    print(f"   MDI适应度: {mdi_fitness:.4f}")
    
    mdi_features = experiment.analyze_mdi_features(mdi_template)
    print(f"   MDI特征分析:")
    print(f"     • 贝尔态测量: {'是' if mdi_features['has_bell_measurement'] else '否'}")
    print(f"     • 两个发送方: {'是' if mdi_features['has_two_senders'] else '否'}")
    print(f"     • 后处理: {'是' if mdi_features['has_post_processing'] else '否'}")
    print(f"     • MDI分数: {mdi_features['mdi_score']:.2f}")
    
    # 3. 运行MDI引导训练
    print("\n3. 🚀 运行MDI引导训练...")
    choice = input("   运行完整实验(200代)还是快速实验(50代)? [f]完整/[q]快速 (默认:快速): ").strip().lower()
    
    iterations = 200 if choice == 'f' else 50
    print(f"   将运行 {iterations} 代训练...")
    
    mdi_result = experiment.train_for_mdi(iterations=iterations, population_size=15)
    
    # 4. 显示结果
    print("\n4. 📈 训练结果:")
    print(f"   最佳适应度: {mdi_result.get('best_fitness', 0):.4f}")
    
    if mdi_result.get('best_protocol_stats'):
        stats = mdi_result['best_protocol_stats']
        print(f"   最佳协议: {stats.get('name', 'Unknown')}")
        print(f"   节点数: {stats.get('node_count', 0)}")
        print(f"   边数: {stats.get('edge_count', 0)}")
    
    if mdi_result.get('mdi_features'):
        features = mdi_result['mdi_features']
        print(f"\n   MDI特征:")
        print(f"     • 类似MDI协议: {'✅ 是' if features.get('is_mdi_like') else '❌ 否'}")
        print(f"     • MDI分数: {features.get('mdi_score', 0):.2f}/1.0")
        print(f"     • 发送方: {', '.join(features.get('sender_parties', []))}")
        print(f"     • 贝尔态测量: {features.get('joint_measurements', 0)} 个")
    
    # 5. 保存结果
    timestamp = int(time.time())
    filename = f"results/mdi_qkd_discovery_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(mdi_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 结果已保存: {filename}")
    
    # 6. 运行比较实验（可选）
    print("\n5. 🔬 运行比较实验?")
    run_comparison = input("   运行标准AI vs MDI引导AI比较实验? [y]是/[n]否 (默认:否): ").strip().lower()
    
    if run_comparison == 'y':
        comparison_result = experiment.run_comparison_experiment()
        
        # 保存比较结果
        comp_filename = f"results/mdi_comparison_{timestamp}.json"
        with open(comp_filename, 'w') as f:
            json.dump(comparison_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 比较结果已保存: {comp_filename}")
    
    print("\n" + "=" * 70)
    print("✅ MDI-QKD实验完成!")
    print("=" * 70)
    
    print("\n🎯 下一步建议:")
    print("1. 分析生成的MDI-like协议")
    print("2. 调整适应度函数权重")
    print("3. 尝试其他引导策略")
    print("4. 将发现的协议集成到AI4QKD框架")
    
    return mdi_result


if __name__ == "__main__":
    main()