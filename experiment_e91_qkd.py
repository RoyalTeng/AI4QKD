#!/usr/bin/env python3
"""
E91协议发现实验（基于纠缠的量子密钥分发）

E91协议特点：
1. 基于贝尔态纠缠
2. 使用贝尔不等式违反验证安全性
3. 不需要可信源
4. 天然抵御某些类型攻击
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random
import numpy as np


class E91Experiment:
    """E91协议实验类"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.base_evaluate = self.agent.evaluate_protocol
    
    def create_e91_template(self) -> ProtocolGraph:
        """创建E91协议模板"""
        protocol = ProtocolGraph(name="E91 Protocol Template")
        
        print("  创建E91协议模板...")
        
        # 纠缠源（产生贝尔态）
        entanglement_source = protocol.add_node(
            node_type=NodeType.QSP,
            params={
                'state': 'bell_state',
                'type': 'phi_plus',
                'fidelity': 0.95,
                'rate': 1e6
            },
            party=None  # 可以是第三方源
        )
        
        # 纠缠分发（到Alice和Bob）
        channel_to_alice = protocol.add_node(
            node_type=NodeType.QC,
            params={'loss': 0.1, 'distance': 50},
            party=None
        )
        
        channel_to_bob = protocol.add_node(
            node_type=NodeType.QC,
            params={'loss': 0.1, 'distance': 50},
            party=None
        )
        
        # Alice的测量装置
        alice_measurement = protocol.add_node(
            node_type=NodeType.QM,
            params={
                'basis': 'random_3settings',
                'settings': 'a1,a2,a3',
                'efficiency': 0.8
            },
            party=Party.ALICE
        )
        
        # Bob的测量装置
        bob_measurement = protocol.add_node(
            node_type=NodeType.QM,
            params={
                'basis': 'random_3settings',
                'settings': 'b1,b2,b3',
                'efficiency': 0.8
            },
            party=Party.BOB
        )
        
        # 经典信道（交换测量基信息）
        classical_channel = protocol.add_node(
            node_type=NodeType.CC,
            params={'capacity': 2.0, 'delay': 0.001},
            party=None
        )
        
        # 贝尔不等式验证
        bell_test = protocol.add_node(
            node_type=NodeType.CV,
            params={
                'test_type': 'CHSH_inequality',
                'threshold': 2.0,
                'significance': 0.05
            },
            party=Party.BOTH
        )
        
        # 密钥提取（基于违反贝尔不等式的结果）
        key_extraction = protocol.add_node(
            node_type=NodeType.CK,
            params={'method': 'bell_violation_based', 'privacy_amplification': True},
            party=Party.BOTH
        )
        
        # 添加边
        # 纠缠分发
        protocol.add_edge(entanglement_source, channel_to_alice, EdgeType.QUANTUM)
        protocol.add_edge(entanglement_source, channel_to_bob, EdgeType.QUANTUM)
        protocol.add_edge(channel_to_alice, alice_measurement, EdgeType.QUANTUM)
        protocol.add_edge(channel_to_bob, bob_measurement, EdgeType.QUANTUM)
        
        # 经典通信
        protocol.add_edge(alice_measurement, classical_channel, EdgeType.CLASSICAL)
        protocol.add_edge(bob_measurement, classical_channel, EdgeType.CLASSICAL)
        protocol.add_edge(classical_channel, bell_test, EdgeType.CLASSICAL)
        protocol.add_edge(bell_test, key_extraction, EdgeType.CLASSICAL)
        
        stats = protocol.get_statistics()
        print(f"  模板创建完成: {stats['node_count']}节点, {stats['edge_count']}边")
        return protocol
    
    def detect_e91_features(self, protocol: ProtocolGraph) -> dict:
        """检测E91协议特征"""
        features = {
            "entanglement": {
                "has_entanglement_source": False,
                "has_bell_state": False,
                "entanglement_distribution": False
            },
            "measurement": {
                "has_two_measurements": False,
                "has_random_basis": False,
                "has_multiple_settings": False
            },
            "verification": {
                "has_bell_test": False,
                "has_CHSH_test": False,
                "has_classical_communication": False
            },
            "security": {
                "device_independent": False,
                "bell_violation_based": False,
                "no_trusted_source": False
            }
        }
        
        # 统计
        entanglement_sources = 0
        measurement_nodes = 0
        bell_test_nodes = 0
        parties = set()
        
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            
            # 记录参与方
            if node.party:
                parties.add(node.party)
            
            # 检查纠缠源
            if node.node_type == NodeType.QSP:
                if node.params.get('state') == 'bell_state':
                    features["entanglement"]["has_bell_state"] = True
                    features["entanglement"]["has_entanglement_source"] = True
                    entanglement_sources += 1
            
            # 检查测量
            if node.node_type == NodeType.QM:
                measurement_nodes += 1
                if 'random' in str(node.params.get('basis', '')).lower():
                    features["measurement"]["has_random_basis"] = True
                if node.params.get('settings') and len(str(node.params.get('settings')).split(',')) >= 2:
                    features["measurement"]["has_multiple_settings"] = True
            
            # 检查贝尔测试
            if node.node_type == NodeType.CV:
                bell_test_nodes += 1
                features["verification"]["has_bell_test"] = True
                if 'CHSH' in str(node.params.get('test_type', '')).upper():
                    features["verification"]["has_CHSH_test"] = True
            
            # 检查经典通信
            if node.node_type == NodeType.CC:
                features["verification"]["has_classical_communication"] = True
        
        # 检查纠缠分发（两个量子信道从同一源出发）
        source_nodes = [
            nid for nid in protocol.graph.nodes()
            if protocol.graph.nodes[nid]['node'].node_type == NodeType.QSP
            and protocol.graph.nodes[nid]['node'].params.get('state') == 'bell_state'
        ]
        
        if source_nodes:
            # 检查是否有至少两个量子信道从纠缠源出发
            for source_id in source_nodes:
                outgoing_edges = list(protocol.graph.out_edges(source_id))
                quantum_channels = 0
                for _, target in outgoing_edges:
                    target_node = protocol.graph.nodes[target]['node']
                    if target_node.node_type == NodeType.QC:
                        quantum_channels += 1
                
                if quantum_channels >= 2:
                    features["entanglement"]["entanglement_distribution"] = True
                    break
        
        # 检查两个测量
        features["measurement"]["has_two_measurements"] = measurement_nodes >= 2
        
        # 安全性特征推断
        if (features["entanglement"]["has_bell_state"] and 
            features["verification"]["has_bell_test"] and
            features["measurement"]["has_two_measurements"]):
            features["security"]["device_independent"] = True
            features["security"]["bell_violation_based"] = True
            features["security"]["no_trusted_source"] = True
        
        # 计算E91分数
        e91_score = self.calculate_e91_score(features)
        features["e91_score"] = e91_score
        features["is_e91_like"] = e91_score >= 0.7
        
        # 添加统计信息
        features["statistics"] = {
            "entanglement_sources": entanglement_sources,
            "measurement_nodes": measurement_nodes,
            "bell_test_nodes": bell_test_nodes,
            "parties": [p.value for p in parties] if parties else [],
            "total_nodes": protocol.get_statistics()["node_count"],
            "total_edges": protocol.get_statistics()["edge_count"]
        }
        
        return features
    
    def calculate_e91_score(self, features: dict) -> float:
        """计算E91特征分数"""
        weights = {
            "entanglement": 0.35,  # 纠缠特征最重要
            "measurement": 0.25,   # 测量特征次重要
            "verification": 0.25,  # 验证特征
            "security": 0.15       # 安全特征
        }
        
        category_scores = {}
        
        # 纠缠特征分数
        entanglement_score = 0.0
        if features["entanglement"]["has_entanglement_source"]:
            entanglement_score += 0.4
        if features["entanglement"]["has_bell_state"]:
            entanglement_score += 0.3
        if features["entanglement"]["entanglement_distribution"]:
            entanglement_score += 0.3
        category_scores["entanglement"] = min(entanglement_score, 1.0)
        
        # 测量特征分数
        measurement_score = 0.0
        if features["measurement"]["has_two_measurements"]:
            measurement_score += 0.4
        if features["measurement"]["has_random_basis"]:
            measurement_score += 0.3
        if features["measurement"]["has_multiple_settings"]:
            measurement_score += 0.3
        category_scores["measurement"] = min(measurement_score, 1.0)
        
        # 验证特征分数
        verification_score = 0.0
        if features["verification"]["has_bell_test"]:
            verification_score += 0.5
        if features["verification"]["has_CHSH_test"]:
            verification_score += 0.3
        if features["verification"]["has_classical_communication"]:
            verification_score += 0.2
        category_scores["verification"] = min(verification_score, 1.0)
        
        # 安全特征分数
        security_score = 0.0
        if features["security"]["device_independent"]:
            security_score += 0.4
        if features["security"]["bell_violation_based"]:
            security_score += 0.4
        if features["security"]["no_trusted_source"]:
            security_score += 0.2
        category_scores["security"] = min(security_score, 1.0)
        
        # 加权总分
        total_score = sum(
            category_scores[category] * weights[category]
            for category in weights
        )
        
        return total_score
    
    def e91_enhanced_fitness(self, protocol: ProtocolGraph) -> float:
        """E91增强适应度函数"""
        # 基础适应度
        base_fitness = self.base_evaluate(protocol)
        
        # E91特征奖励
        features = self.detect_e91_features(protocol)
        e91_bonus = 0.0
        
        # 纠缠特征奖励
        if features["entanglement"]["has_entanglement_source"]:
            e91_bonus += 0.15
        
        if features["entanglement"]["has_bell_state"]:
            e91_bonus += 0.10
        
        if features["entanglement"]["entanglement_distribution"]:
            e91_bonus += 0.10
        
        # 测量特征奖励
        if features["measurement"]["has_two_measurements"]:
            e91_bonus += 0.10
        
        if features["measurement"]["has_random_basis"]:
            e91_bonus += 0.08
        
        if features["measurement"]["has_multiple_settings"]:
            e91_bonus += 0.07
        
        # 验证特征奖励
        if features["verification"]["has_bell_test"]:
            e91_bonus += 0.10
        
        if features["verification"]["has_CHSH_test"]:
            e91_bonus += 0.05
        
        # 安全特征奖励
        if features["security"]["device_independent"]:
            e91_bonus += 0.10
        
        if features["security"]["bell_violation_based"]:
            e91_bonus += 0.05
        
        total_fitness = base_fitness + e91_bonus
        return min(total_fitness, 1.0)
    
    def run_e91_experiment(self, iterations: int = 80, population_size: int = 18) -> dict:
        """运行E91协议发现实验"""
        print("\n" + "=" * 70)
        print("🚀 开始E91协议发现实验")
        print("=" * 70)
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用E91增强适应度函数
        self.agent.evaluate_protocol = self.e91_enhanced_fitness
        
        # 1. 创建并评估基准协议
        print("\n1. 📋 创建基准协议...")
        
        # E91模板
        e91_template = self.create_e91_template()
        e91_template_fitness = self.base_evaluate(e91_template)
        e91_template_features = self.detect_e91_features(e91_template)
        
        print(f"   E91模板适应度: {e91_template_fitness:.4f}")
        print(f"   E91模板E91分数: {e91_template_features['e91_score']:.3f}")
        
        # BB84基准
        bb84_protocol = ProtocolGraph.create_bb84()
        bb84_fitness = self.base_evaluate(bb84_protocol)
        print(f"   BB84适应度: {bb84_fitness:.4f}")
        
        # 2. 初始化种群
        print(f"\n2. 🧬 初始化种群 ({population_size}个协议)...")
        self.agent.population = []
        
        # 添加E91模板
        self.agent.population.append(e91_template)
        print(f"   添加E91模板")
        
        # 添加BB84
        self.agent.population.append(bb84_protocol)
        print(f"   添加BB84基准")
        
        # 添加随机协议
        for i in range(population_size - 2):
            random_protocol = self.agent.generate_random_protocol()
            self.agent.population.append(random_protocol)
        
        print(f"   种群初始化完成")
        
        # 3. 配置训练参数
        self.agent.config.max_iterations = iterations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.35
        self.agent.config.elite_size = 3
        
        # 4. 运行训练
        print(f"\n3. 🧠 开始训练 ({iterations}代)...")
        result = self.agent.train(iterations=iterations, population_size=population_size)
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 5. 分析结果
        print("\n4. 📊 分析最佳协议...")
        
        best_fitness = result.get('best_fitness', 0)
        best_protocol = result.get('best_protocol')
        
        if best_protocol:
            best_features = self.detect_e91_features(best_protocol)
            best_stats = best_protocol.get_statistics()
            
            print(f"   最佳适应度: {best_fitness:.4f}")
            print(f"   E91分数: {best_features['e91_score']:.3f}")
            print(f"   类似E91协议: {'✅ 是' if best_features['is_e91_like'] else '❌ 否'}")
            print(f"   协议节点数: {best_stats['node_count']}")
            print(f"   协议边数: {best_stats['edge_count']}")
            
            # 显示关键特征
            print(f"\n   关键E91特征:")
            key_features = [
                ("纠缠源", "entanglement", "has_entanglement_source"),
                ("贝尔态", "entanglement", "has_bell_state"),
                ("纠缠分发", "entanglement", "entanglement_distribution"),
                ("两个测量", "measurement", "has_two_measurements"),
                ("随机基", "measurement", "has_random_basis"),
                ("贝尔测试", "verification", "has_bell_test"),
                ("设备无关", "security", "device_independent")
            ]
            
            for name, category, key in key_features:
                value = best_features[category][key]
                status = "✅" if value else "❌"
                print(f"     • {name}: {status}")
        
        # 6. 性能对比
        print("\n5. 🔄 性能对比...")
        
        improvement_vs_e91 = ((best_fitness - e91_template_fitness) / e91_template_fitness * 100) if e91_template_fitness > 0 else 0
        improvement_vs_bb84 = ((best_fitness - bb84_fitness) / bb84_fitness * 100) if bb84_fitness > 0 else 0
        
        print(f"   相对于E91模板: {improvement_vs_e91:+.1f}%")
        print(f"   相对于BB84: {improvement_vs_bb84:+.1f}%")
        
        # 7. 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "E91 Protocol Discovery",
            "config": {
                "iterations": iterations,
                "population_size": population_size,
                "mutation_rate": self.agent.config.mutation_rate
            },
            "baseline_results": {
                "e91_template": {
                    "fitness": e91_template_fitness,
                    "e91_score": e91_template_features['e91_score'],
                    "is_e91_like": e91_template_features['is_e91_like'],
                    "stats": e91_template.get_statistics()
                },
                "bb84": {
                    "fitness": bb84_fitness,
                    "stats": bb84_protocol.get_statistics()
                }
            },
            "ai_training_result": {
                "best_fitness": best_fitness,
                "best_protocol_stats": best_stats if best_protocol else {},
                "e91_features": best_features if best_protocol else {},
                "fitness_history": result.get('fitness_history', []),
                "iterations": iterations
            },
            "comparison": {
                "improvement_vs_e91_template": improvement_vs_e91,
                "improvement_vs_bb84": improvement_vs_bb84,
                "e91_discovery_success": best_features.get('is_e91_like', False) if best_protocol else False
            },
            "timestamp": timestamp
        }
        
        filename = f"results/e91_qkd_experiment_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ E91协议发现实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 E91协议发现实验（基于纠缠的量子密钥分发）")
    print("=" * 70)
    
    experiment = E91Experiment()
    
    # 实验参数
    iterations = 80  # 比TF实验多，因为E91可能更容易收敛
    population_size = 18
    
    print(f"\n实验配置:")
    print(f"  迭代次数: {iterations}")
    print(f"  种群大小: {population_size}")
    print(f"  开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行实验
    result = experiment.run_e91_experiment(
        iterations=iterations,
        population_size=population_size
    )
    
    # 显示总结
    print("\n📈 实验总结:")
    print(f"  最佳适应度: {result['ai_training_result']['best_fitness']:.4f}")
    print(f"  E91分数: {result['ai_training_result']['e91_features'].get('e91_score', 0):.3f}")
    
    e91_success = result['comparison']['e91_discovery_success']
    if e91_success:
        print(f"  E91协议发现: ✅ 成功!")
        improvement = result['comparison']['improvement_vs_e91_template']
        print(f"  性能提升: {improvement:+.1f}% (相对于E91模板)")
        
        # 显示成功特征
        features = result['ai_training_result']['e91_features']
        print(f"\n  🎯 成功特征:")
        if features["entanglement"]["has_entanglement_source"]:
            print(f"     • 纠缠源: ✅")
        if features["entanglement"]["has_bell_state"]:
            print(f"     • 贝尔态: ✅")
        if features["measurement"]["has_two_measurements"]:
            print(f"     • 两个测量装置: ✅")
        if features["verification"]["has_bell_test"]:
            print(f"     • 贝尔测试: ✅")
    else:
        print(f"  E91协议发现: ⚠️ 部分成功")
        print(f"  最佳协议E91分数: {result['ai_training_result']['e91_features'].get('e91_score', 0):.3f}/0.7")
        
        # 分析缺失特征
        features = result['ai_training_result']['e91_features']
        print(f"\n  🔍 缺失的关键特征:")
        if not features["entanglement"]["has_entanglement_source"]:
            print(f"     • 纠缠源")
        if not features["entanglement"]["has_bell_state"]:
            print(f"     • 贝尔态")
        if not features["measurement"]["has_two_measurements"]:
            print(f"     • 两个测量装置")
        if not features["verification"]["has_bell_test"]:
            print(f"     • 贝尔测试")
    
    print(f"\n📁 结果文件: results/e91_qkd_experiment_*.json")
    
    print("\n🎯 下一步建议:")
    if e91_success:
        print("  1. 深入分析发现的E91协议结构")
        print("  2. 运行验证实验确认稳定性")
        print("  3. 尝试发现E91的变体协议")
        print("  4. 基于成功经验优化TF实验")
    else:
        print("  1. 增加训练代数和种群大小")
        print("  2. 调整E91特征权重")
        print("  3. 添加纠缠专用变异操作")
        print("  4. 分析失败原因并调整策略")


if __name__ == "__main__":
    main()