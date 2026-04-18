#!/usr/bin/env python3
"""
TF-QKD快速实验（非交互式）
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random
import numpy as np


def run_tf_quick_experiment():
    """运行TF-QKD快速实验"""
    print("=" * 70)
    print("🚀 TF-QKD快速实验 (50代)")
    print("=" * 70)
    
    # 创建智能体
    agent = EnhancedHybridAgent()
    
    # 1. 创建TF-QKD模板
    print("\n1. 📋 创建TF-QKD模板...")
    tf_protocol = ProtocolGraph(name="TF-QKD Template")
    
    # 简化版TF模板（只包含核心特征）
    alice = tf_protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': 'coherent', 'phase': 'random'},
        party=Party.ALICE
    )
    
    bob = tf_protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': 'coherent', 'phase': 'random'},
        party=Party.BOB
    )
    
    channel1 = tf_protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.3, 'distance': 300},
        party=None
    )
    
    channel2 = tf_protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.3, 'distance': 300},
        party=None
    )
    
    interferometer = tf_protocol.add_node(
        node_type=NodeType.QG,
        params={'gate_type': 'beam_splitter'},
        party=Party.CHARLIE
    )
    
    detector = tf_protocol.add_node(
        node_type=NodeType.QD,
        params={'type': 'single_photon'},
        party=Party.CHARLIE
    )
    
    # 连接
    tf_protocol.add_edge(alice, channel1, EdgeType.QUANTUM)
    tf_protocol.add_edge(bob, channel2, EdgeType.QUANTUM)
    tf_protocol.add_edge(channel1, interferometer, EdgeType.QUANTUM)
    tf_protocol.add_edge(channel2, interferometer, EdgeType.QUANTUM)
    tf_protocol.add_edge(interferometer, detector, EdgeType.QUANTUM)
    
    tf_stats = tf_protocol.get_statistics()
    print(f"   TF模板: {tf_stats['node_count']}节点, {tf_stats['edge_count']}边")
    
    # 2. 评估基准协议
    print("\n2. 📊 评估基准协议...")
    
    # TF模板适应度
    tf_fitness = agent.evaluate_protocol(tf_protocol)
    print(f"   TF模板适应度: {tf_fitness:.4f}")
    
    # BB84适应度
    bb84_protocol = ProtocolGraph.create_bb84()
    bb84_fitness = agent.evaluate_protocol(bb84_protocol)
    print(f"   BB84适应度: {bb84_fitness:.4f}")
    
    # 3. 定义TF特征检测
    def detect_tf_simple(protocol):
        """简化TF特征检测"""
        features = {
            "two_senders": False,
            "coherent_state": False,
            "interference": False,
            "long_distance": False
        }
        
        senders = set()
        has_coherent = False
        has_interference = False
        long_distance = False
        
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            
            if node.node_type == NodeType.QSP:
                if node.party in [Party.ALICE, Party.BOB]:
                    senders.add(node.party)
                if node.params.get('state') == 'coherent':
                    has_coherent = True
            
            if node.node_type == NodeType.QG:
                if node.params.get('gate_type') == 'beam_splitter':
                    has_interference = True
            
            if node.node_type == NodeType.QC:
                if node.params.get('distance', 0) > 100:
                    long_distance = True
        
        features["two_senders"] = len(senders) >= 2
        features["coherent_state"] = has_coherent
        features["interference"] = has_interference
        features["long_distance"] = long_distance
        
        # 计算简单TF分数
        score = 0.0
        if features["two_senders"]:
            score += 0.3
        if features["coherent_state"]:
            score += 0.3
        if features["interference"]:
            score += 0.2
        if features["long_distance"]:
            score += 0.2
        
        features["tf_score"] = score
        features["is_tf_like"] = score >= 0.6
        
        return features
    
    # 4. TF增强适应度函数
    original_evaluate = agent.evaluate_protocol
    
    def tf_enhanced_fitness(protocol):
        base = original_evaluate(protocol)
        features = detect_tf_simple(protocol)
        
        bonus = 0.0
        if features["two_senders"]:
            bonus += 0.15
        if features["coherent_state"]:
            bonus += 0.10
        if features["interference"]:
            bonus += 0.10
        if features["long_distance"]:
            bonus += 0.05
        
        return min(base + bonus, 1.0)
    
    # 5. 运行AI训练
    print("\n3. 🧠 AI训练发现TF协议 (50代)...")
    agent.evaluate_protocol = tf_enhanced_fitness
    
    # 初始化种群
    agent.population = []
    agent.population.append(tf_protocol)  # TF模板
    agent.population.append(bb84_protocol)  # BB84
    
    for _ in range(13):  # 总种群大小15
        agent.population.append(agent.generate_random_protocol())
    
    # 训练参数
    agent.config.max_iterations = 50
    agent.config.population_size = 15
    agent.config.mutation_rate = 0.4
    
    # 运行训练
    result = agent.train(iterations=50, population_size=15)
    
    # 恢复原始评估函数
    agent.evaluate_protocol = original_evaluate
    
    # 6. 分析结果
    print("\n4. 📈 训练结果分析...")
    
    best_fitness = result.get('best_fitness', 0)
    best_protocol = result.get('best_protocol')
    
    if best_protocol:
        best_features = detect_tf_simple(best_protocol)
        best_stats = best_protocol.get_statistics()
        
        print(f"   最佳适应度: {best_fitness:.4f}")
        print(f"   TF分数: {best_features['tf_score']:.3f}")
        print(f"   类似TF协议: {'✅ 是' if best_features['is_tf_like'] else '❌ 否'}")
        print(f"   协议节点数: {best_stats['node_count']}")
        print(f"   协议边数: {best_stats['edge_count']}")
        
        print(f"\n   TF特征:")
        for feature, value in best_features.items():
            if feature not in ['tf_score', 'is_tf_like']:
                status = "✅" if value else "❌"
                print(f"     • {feature}: {status}")
    
    # 7. 性能对比
    print("\n5. 🔄 性能对比...")
    
    improvement_vs_tf = ((best_fitness - tf_fitness) / tf_fitness * 100) if tf_fitness > 0 else 0
    improvement_vs_bb84 = ((best_fitness - bb84_fitness) / bb84_fitness * 100) if bb84_fitness > 0 else 0
    
    print(f"   相对于TF模板: {improvement_vs_tf:+.1f}%")
    print(f"   相对于BB84: {improvement_vs_bb84:+.1f}%")
    
    # 8. 保存结果
    timestamp = int(time.time())
    result_data = {
        "experiment": "TF-QKD Quick Experiment",
        "baselines": {
            "tf_template": {"fitness": tf_fitness, "stats": tf_stats},
            "bb84": {"fitness": bb84_fitness, "stats": bb84_protocol.get_statistics()}
        },
        "ai_result": {
            "best_fitness": best_fitness,
            "best_protocol_stats": best_stats if best_protocol else {},
            "tf_features": best_features if best_protocol else {},
            "fitness_history": result.get('fitness_history', [])
        },
        "improvements": {
            "vs_tf": improvement_vs_tf,
            "vs_bb84": improvement_vs_bb84
        },
        "timestamp": timestamp
    }
    
    filename = f"results/tf_quick_experiment_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 结果已保存: {filename}")
    
    print("\n" + "=" * 70)
    print("✅ TF-QKD快速实验完成!")
    print("=" * 70)
    
    # 总结
    tf_success = best_features.get('is_tf_like', False) if best_protocol else False
    
    print("\n🎯 实验总结:")
    if tf_success:
        print(f"  ✅ 成功发现TF-like协议!")
        print(f"    适应度: {best_fitness:.4f}")
        print(f"    TF分数: {best_features['tf_score']:.3f}")
        print(f"    性能提升: {improvement_vs_tf:+.1f}%")
    else:
        print(f"  ⚠️ 未发现完整TF协议")
        if best_protocol:
            print(f"    最佳TF分数: {best_features['tf_score']:.3f}/0.6")
            print(f"    缺失特征:")
            for feature, value in best_features.items():
                if feature not in ['tf_score', 'is_tf_like'] and not value:
                    print(f"      • {feature}")
    
    return result_data


if __name__ == "__main__":
    run_tf_quick_experiment()