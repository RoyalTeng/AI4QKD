#!/usr/bin/env python3
"""
快速MDI-QKD实验
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random


def create_mdi_qkd_protocol():
    """手动创建MDI-QKD协议"""
    protocol = ProtocolGraph(name="MDI-QKD Protocol")
    
    # Alice的量子态制备
    alice_qsp = protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': '|+⟩', 'basis': 'X', 'intensity': 0.5},
        party=Party.ALICE
    )
    
    # Bob的量子态制备
    bob_qsp = protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': '|0⟩', 'basis': 'Z', 'intensity': 0.5},
        party=Party.BOB
    )
    
    # 量子信道（Alice到Charlie）
    channel_alice = protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.1, 'noise': 0.01},
        party=None
    )
    
    # 量子信道（Bob到Charlie）
    channel_bob = protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.1, 'noise': 0.01},
        party=None
    )
    
    # 贝尔态测量（Charlie）
    bell_measurement = protocol.add_node(
        node_type=NodeType.QM,
        params={'basis': 'Bell', 'measurement_type': 'joint', 'efficiency': 0.8},
        party=Party.CHARLIE
    )
    
    # 经典信道（公布结果）
    classical_channel = protocol.add_node(
        node_type=NodeType.CC,
        params={'capacity': 1.0, 'reliability': 0.99},
        party=None
    )
    
    # 后处理
    post_processing = protocol.add_node(
        node_type=NodeType.CP,
        params={'operation': 'sifting+error_correction+privacy_amplification'},
        party=Party.ALICE
    )
    
    # 添加边
    protocol.add_edge(alice_qsp, channel_alice, EdgeType.QUANTUM)
    protocol.add_edge(bob_qsp, channel_bob, EdgeType.QUANTUM)
    protocol.add_edge(channel_alice, bell_measurement, EdgeType.QUANTUM)
    protocol.add_edge(channel_bob, bell_measurement, EdgeType.QUANTUM)
    protocol.add_edge(bell_measurement, classical_channel, EdgeType.CLASSICAL)
    protocol.add_edge(classical_channel, post_processing, EdgeType.CLASSICAL)
    
    return protocol


def analyze_mdi_features(protocol):
    """分析MDI特征"""
    features = {
        "has_bell_measurement": False,
        "has_two_senders": False,
        "sender_parties": set(),
        "measurement_nodes": 0,
        "joint_measurements": 0
    }
    
    for node_id in protocol.graph.nodes():
        node = protocol.graph.nodes[node_id]['node']
        
        # 检查发送方
        if node.node_type == NodeType.QSP:
            if node.party and node.party != None:
                features["sender_parties"].add(node.party.value if hasattr(node.party, 'value') else str(node.party))
        
        # 检查测量节点
        if node.node_type == NodeType.QM:
            features["measurement_nodes"] += 1
            if node.params.get('basis') == 'Bell' or node.params.get('measurement_type') == 'joint':
                features["has_bell_measurement"] = True
                features["joint_measurements"] += 1
    
    features["has_two_senders"] = len(features["sender_parties"]) >= 2
    features["sender_parties"] = list(features["sender_parties"])
    
    # 计算MDI分数
    mdi_score = 0.0
    if features["has_bell_measurement"]:
        mdi_score += 0.4
    if features["has_two_senders"]:
        mdi_score += 0.3
    if features["measurement_nodes"] >= 1:
        mdi_score += 0.1
    
    features["mdi_score"] = mdi_score
    features["is_mdi_like"] = mdi_score >= 0.6
    
    return features


def run_mdi_experiment():
    """运行MDI实验"""
    print("=" * 60)
    print("🚀 MDI-QKD协议发现实验")
    print("=" * 60)
    
    # 创建智能体
    agent = EnhancedHybridAgent()
    
    # 1. 创建并评估MDI-QKD协议
    print("\n1. 📋 创建MDI-QKD协议...")
    mdi_protocol = create_mdi_qkd_protocol()
    stats = mdi_protocol.get_statistics()
    
    print(f"   协议名称: {stats['name']}")
    print(f"   节点数: {stats['node_count']}")
    print(f"   边数: {stats['edge_count']}")
    
    # 分析MDI特征
    mdi_features = analyze_mdi_features(mdi_protocol)
    print(f"\n   MDI特征分析:")
    print(f"     • 贝尔态测量: {'✅ 是' if mdi_features['has_bell_measurement'] else '❌ 否'}")
    print(f"     • 两个发送方: {'✅ 是' if mdi_features['has_two_senders'] else '❌ 否'}")
    print(f"     • 发送方: {', '.join(mdi_features['sender_parties'])}")
    print(f"     • MDI分数: {mdi_features['mdi_score']:.2f}/1.0")
    print(f"     • 类似MDI: {'✅ 是' if mdi_features['is_mdi_like'] else '❌ 否'}")
    
    # 2. 评估MDI协议适应度
    print("\n2. 📊 评估MDI协议...")
    mdi_fitness = agent.evaluate_protocol(mdi_protocol)
    print(f"   MDI协议适应度: {mdi_fitness:.4f}")
    
    # 3. 评估BB84协议作为对比
    print("\n3. 🔄 对比BB84协议...")
    bb84_protocol = ProtocolGraph.create_bb84()
    bb84_fitness = agent.evaluate_protocol(bb84_protocol)
    print(f"   BB84协议适应度: {bb84_fitness:.4f}")
    
    # 4. 运行AI训练发现MDI-like协议
    print("\n4. 🧠 AI训练发现MDI-like协议...")
    print("   训练50代，种群大小15...")
    
    # 修改适应度函数以奖励MDI特征
    original_evaluate = agent.evaluate_protocol
    
    def mdi_enhanced_evaluate(protocol):
        base_fitness = original_evaluate(protocol)
        features = analyze_mdi_features(protocol)
        
        # 添加MDI奖励
        mdi_bonus = 0.0
        if features["has_bell_measurement"]:
            mdi_bonus += 0.2
        if features["has_two_senders"]:
            mdi_bonus += 0.15
        if features["joint_measurements"] >= 1:
            mdi_bonus += 0.1
        
        total_fitness = base_fitness + mdi_bonus
        return min(total_fitness, 1.0)
    
    # 临时替换评估函数
    agent.evaluate_protocol = mdi_enhanced_evaluate
    
    # 运行训练
    result = agent.train(iterations=50, population_size=15)
    
    # 恢复原始评估函数
    agent.evaluate_protocol = original_evaluate
    
    # 5. 分析结果
    print("\n5. 📈 训练结果:")
    print(f"   最佳适应度: {result['best_fitness']:.4f}")
    
    if result['best_protocol']:
        best_stats = result['best_protocol'].get_statistics()
        print(f"   最佳协议: {best_stats['name']}")
        print(f"   节点数: {best_stats['node_count']}")
        print(f"   边数: {best_stats['edge_count']}")
        
        # 分析最佳协议的MDI特征
        best_features = analyze_mdi_features(result['best_protocol'])
        print(f"\n   MDI特征分析:")
        print(f"     • 贝尔态测量: {'✅ 是' if best_features['has_bell_measurement'] else '❌ 否'}")
        print(f"     • 两个发送方: {'✅ 是' if best_features['has_two_senders'] else '❌ 否'}")
        print(f"     • 发送方: {', '.join(best_features['sender_parties'])}")
        print(f"     • MDI分数: {best_features['mdi_score']:.2f}/1.0")
        print(f"     • 类似MDI: {'✅ 是' if best_features['is_mdi_like'] else '❌ 否'}")
    
    # 6. 保存结果
    timestamp = int(time.time())
    result_data = {
        "experiment": "MDI-QKD Protocol Discovery (Quick)",
        "mdi_protocol": {
            "fitness": mdi_fitness,
            "stats": mdi_protocol.get_statistics(),
            "features": mdi_features
        },
        "bb84_protocol": {
            "fitness": bb84_fitness,
            "stats": bb84_protocol.get_statistics()
        },
        "ai_training": {
            "best_fitness": result.get("best_fitness", 0),
            "best_protocol_stats": result.get("best_protocol_stats", {}),
            "fitness_history": result.get("fitness_history", []),
            "iterations": result.get("iterations", 0),
            "population_size": result.get("population_size", 0)
        },
        "timestamp": timestamp
    }
    
    filename = f"results/mdi_quick_experiment_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 结果已保存: {filename}")
    
    print("\n" + "=" * 60)
    print("✅ MDI-QKD实验完成!")
    print("=" * 60)
    
    return result_data


if __name__ == "__main__":
    run_mdi_experiment()