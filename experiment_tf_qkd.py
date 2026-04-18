#!/usr/bin/env python3
"""
TF-QKD（双场量子密钥分发）协议发现实验
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random
import numpy as np
from typing import Dict, List, Any, Set, Tuple


class TFQKDExperiment:
    """TF-QKD实验类"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.base_evaluate = self.agent.evaluate_protocol
    
    def create_tf_qkd_template(self) -> ProtocolGraph:
        """创建TF-QKD协议模板"""
        protocol = ProtocolGraph(name="TF-QKD Template")
        
        print("  创建TF-QKD模板...")
        
        # 两个远程发送方（相干态光源）
        alice_source = protocol.add_node(
            node_type=NodeType.QSP,
            params={
                'state': 'coherent',
                'intensity': 0.5,
                'phase': 'random',
                'wavelength': 1550,
                'pulse_width': 100
            },
            party=Party.ALICE
        )
        
        bob_source = protocol.add_node(
            node_type=NodeType.QSP,
            params={
                'state': 'coherent', 
                'intensity': 0.5,
                'phase': 'random',
                'wavelength': 1550,
                'pulse_width': 100
            },
            party=Party.BOB
        )
        
        # 相位调制器
        alice_phase_mod = protocol.add_node(
            node_type=NodeType.QG,
            params={
                'gate_type': 'phase_modulator',
                'phase_range': '0,π',
                'modulation_speed': 'GHz',
                'accuracy': 0.01
            },
            party=Party.ALICE
        )
        
        bob_phase_mod = protocol.add_node(
            node_type=NodeType.QG,
            params={
                'gate_type': 'phase_modulator',
                'phase_range': '0,π',
                'modulation_speed': 'GHz',
                'accuracy': 0.01
            },
            party=Party.BOB
        )
        
        # 长距离量子信道（光纤）
        channel_alice = protocol.add_node(
            node_type=NodeType.QC,
            params={
                'loss': 0.3,
                'distance': 300,
                'type': 'optical_fiber',
                'dispersion': 17,
                'nonlinearity': 1.3
            },
            party=None
        )
        
        channel_bob = protocol.add_node(
            node_type=NodeType.QC,
            params={
                'loss': 0.3,
                'distance': 300,
                'type': 'optical_fiber',
                'dispersion': 17,
                'nonlinearity': 1.3
            },
            party=None
        )
        
        # 马赫-曾德尔干涉仪（中间节点）
        interferometer = protocol.add_node(
            node_type=NodeType.QG,
            params={
                'gate_type': 'beam_splitter',
                'configuration': 'mach_zehnder',
                'splitting_ratio': '50:50',
                'visibility': 0.98
            },
            party=Party.CHARLIE
        )
        
        # 相位稳定器
        phase_stabilizer = protocol.add_node(
            node_type=NodeType.QG,
            params={
                'gate_type': 'phase_stabilizer',
                'accuracy': 0.001,
                'bandwidth': 'kHz',
                'method': 'active_feedback'
            },
            party=Party.CHARLIE
        )
        
        # 单光子探测器
        detector = protocol.add_node(
            node_type=NodeType.QD,
            params={
                'type': 'single_photon',
                'efficiency': 0.7,
                'dark_count': 1e-6,
                'jitter': 50,
                'dead_time': 50
            },
            party=Party.CHARLIE
        )
        
        # 时间同步模块
        time_sync = protocol.add_node(
            node_type=NodeType.CP,
            params={
                'operation': 'time_synchronization',
                'accuracy': '10ps',
                'method': 'GPS+optical',
                'stability': 1e-12
            },
            party=None
        )
        
        # 相位后处理
        phase_processing = protocol.add_node(
            node_type=NodeType.CP,
            params={
                'operation': 'phase_error_correction',
                'algorithm': 'CASCADE+LDPC',
                'efficiency': 0.95
            },
            party=Party.BOTH
        )
        
        # 添加边（连接所有组件）
        # Alice端
        protocol.add_edge(alice_source, alice_phase_mod, EdgeType.QUANTUM)
        protocol.add_edge(alice_phase_mod, channel_alice, EdgeType.QUANTUM)
        protocol.add_edge(channel_alice, interferometer, EdgeType.QUANTUM)
        
        # Bob端
        protocol.add_edge(bob_source, bob_phase_mod, EdgeType.QUANTUM)
        protocol.add_edge(bob_phase_mod, channel_bob, EdgeType.QUANTUM)
        protocol.add_edge(channel_bob, interferometer, EdgeType.QUANTUM)
        
        # 干涉仪到探测器
        protocol.add_edge(interferometer, phase_stabilizer, EdgeType.QUANTUM)
        protocol.add_edge(phase_stabilizer, detector, EdgeType.QUANTUM)
        
        # 时间同步连接
        protocol.add_edge(time_sync, alice_phase_mod, EdgeType.CONTROL)
        protocol.add_edge(time_sync, bob_phase_mod, EdgeType.CONTROL)
        protocol.add_edge(time_sync, detector, EdgeType.CONTROL)
        
        # 后处理连接
        protocol.add_edge(detector, phase_processing, EdgeType.CLASSICAL)
        
        print(f"  模板创建完成: {protocol.get_statistics()['node_count']}节点, {protocol.get_statistics()['edge_count']}边")
        return protocol
    
    def detect_tf_features(self, protocol: ProtocolGraph) -> Dict:
        """检测TF-QKD特征"""
        features = {
            "structural": {
                "two_remote_senders": False,
                "interference_measurement": False,
                "phase_encoding": False,
                "coherent_state": False
            },
            "interference": {
                "mach_zehnder": False,
                "phase_stabilizer": False,
                "time_synchronization": False,
                "beam_splitter": False
            },
            "performance": {
                "long_distance": False,
                "fiber_channel": False,
                "single_photon_detection": False
            },
            "security": {
                "phase_randomization": False,
                "decoy_state": False,
                "phase_error_correction": False
            }
        }
        
        # 统计发送方
        sender_parties = set()
        coherent_sources = 0
        
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            
            # 检查发送方
            if node.node_type == NodeType.QSP:
                if node.party in [Party.ALICE, Party.BOB]:
                    sender_parties.add(node.party)
                
                # 检查相干态
                if node.params.get('state') == 'coherent':
                    features["structural"]["coherent_state"] = True
                    coherent_sources += 1
            
            # 检查相位编码
            if node.node_type == NodeType.QG:
                if node.params.get('gate_type') == 'phase_modulator':
                    features["structural"]["phase_encoding"] = True
            
            # 检查干涉仪
            if node.node_type == NodeType.QG:
                if node.params.get('gate_type') == 'beam_splitter':
                    features["interference"]["beam_splitter"] = True
                    if node.params.get('configuration') == 'mach_zehnder':
                        features["interference"]["mach_zehnder"] = True
                        features["structural"]["interference_measurement"] = True
            
            # 检查相位稳定器
            if node.node_type == NodeType.QG:
                if node.params.get('gate_type') == 'phase_stabilizer':
                    features["interference"]["phase_stabilizer"] = True
            
            # 检查时间同步
            if node.node_type == NodeType.CP:
                if 'time_synchronization' in str(node.params.get('operation', '')).lower():
                    features["interference"]["time_synchronization"] = True
            
            # 检查单光子探测器
            if node.node_type == NodeType.QD:
                if node.params.get('type') == 'single_photon':
                    features["performance"]["single_photon_detection"] = True
            
            # 检查光纤信道
            if node.node_type == NodeType.QC:
                if node.params.get('type') == 'optical_fiber':
                    features["performance"]["fiber_channel"] = True
                    if node.params.get('distance', 0) > 100:  # 长距离
                        features["performance"]["long_distance"] = True
            
            # 检查相位后处理
            if node.node_type == NodeType.CP:
                if 'phase_error' in str(node.params.get('operation', '')).lower():
                    features["security"]["phase_error_correction"] = True
        
        # 检查两个远程发送方
        features["structural"]["two_remote_senders"] = (
            len(sender_parties) >= 2 and 
            coherent_sources >= 2
        )
        
        # 检查相位随机化（如果有随机相位参数）
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.QSP:
                if node.params.get('phase') == 'random':
                    features["security"]["phase_randomization"] = True
                    break
        
        # 计算TF分数
        tf_score = self.calculate_tf_score(features)
        features["tf_score"] = tf_score
        features["is_tf_like"] = tf_score >= 0.65  # 稍低于MDI阈值，因为TF更复杂
        
        # 添加详细统计
        features["statistics"] = {
            "sender_parties": [p.value for p in sender_parties] if sender_parties else [],
            "coherent_sources": coherent_sources,
            "total_nodes": protocol.get_statistics()["node_count"],
            "total_edges": protocol.get_statistics()["edge_count"]
        }
        
        return features
    
    def calculate_tf_score(self, features: Dict) -> float:
        """计算TF-QKD特征分数"""
        weights = {
            "structural": 0.35,
            "interference": 0.30,
            "performance": 0.20,
            "security": 0.15
        }
        
        category_scores = {}
        
        # 结构特征分数
        structural_score = 0.0
        if features["structural"]["two_remote_senders"]:
            structural_score += 0.4
        if features["structural"]["interference_measurement"]:
            structural_score += 0.3
        if features["structural"]["phase_encoding"]:
            structural_score += 0.2
        if features["structural"]["coherent_state"]:
            structural_score += 0.1
        category_scores["structural"] = min(structural_score, 1.0)
        
        # 干涉特征分数
        interference_score = 0.0
        if features["interference"]["mach_zehnder"]:
            interference_score += 0.4
        if features["interference"]["phase_stabilizer"]:
            interference_score += 0.3
        if features["interference"]["time_synchronization"]:
            interference_score += 0.2
        if features["interference"]["beam_splitter"]:
            interference_score += 0.1
        category_scores["interference"] = min(interference_score, 1.0)
        
        # 性能特征分数
        performance_score = 0.0
        if features["performance"]["long_distance"]:
            performance_score += 0.5
        if features["performance"]["fiber_channel"]:
            performance_score += 0.3
        if features["performance"]["single_photon_detection"]:
            performance_score += 0.2
        category_scores["performance"] = min(performance_score, 1.0)
        
        # 安全特征分数
        security_score = 0.0
        if features["security"]["phase_randomization"]:
            security_score += 0.4
        if features["security"]["phase_error_correction"]:
            security_score += 0.4
        if features["security"]["decoy_state"]:
            security_score += 0.2
        category_scores["security"] = min(security_score, 1.0)
        
        # 加权总分
        total_score = sum(
            category_scores[category] * weights[category]
            for category in weights
        )
        
        return total_score
    
    def tf_enhanced_fitness(self, protocol: ProtocolGraph) -> float:
        """TF-QKD增强适应度函数"""
        # 基础适应度
        base_fitness = self.base_evaluate(protocol)
        
        # TF特征奖励
        features = self.detect_tf_features(protocol)
        tf_bonus = 0.0
        
        # 结构特征奖励
        if features["structural"]["two_remote_senders"]:
            tf_bonus += 0.15
        
        if features["structural"]["interference_measurement"]:
            tf_bonus += 0.10
        
        if features["structural"]["phase_encoding"]:
            tf_bonus += 0.05
        
        if features["structural"]["coherent_state"]:
            tf_bonus += 0.05
        
        # 干涉特征奖励
        if features["interference"]["mach_zehnder"]:
            tf_bonus += 0.10
        
        if features["interference"]["phase_stabilizer"]:
            tf_bonus += 0.08
        
        if features["interference"]["time_synchronization"]:
            tf_bonus += 0.07
        
        # 长距离性能奖励
        if features["performance"]["long_distance"]:
            tf_bonus += 0.10
        
        # 安全性奖励
        if features["security"]["phase_randomization"]:
            tf_bonus += 0.05
        
        if features["security"]["phase_error_correction"]:
            tf_bonus += 0.05
        
        total_fitness = base_fitness + tf_bonus
        return min(total_fitness, 1.0)
    
    def run_tf_experiment(self, iterations: int = 100, population_size: int = 15) -> Dict:
        """运行TF-QKD发现实验"""
        print("\n" + "=" * 70)
        print("🚀 开始TF-QKD协议发现实验")
        print("=" * 70)
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用TF增强适应度函数
        self.agent.evaluate_protocol = self.tf_enhanced_fitness
        
        # 初始化种群（包含TF模板）
        print("\n1. 🧬 初始化种群...")
        self.agent.population = []
        
        # 添加TF模板
        tf_template = self.create_tf_qkd_template()
        self.agent.population.append(tf_template)
        print(f"   添加TF模板: {tf_template.get_statistics()['node_count']}节点")
        
        # 添加BB84作为基准
        bb84_protocol = ProtocolGraph.create_bb84()
        self.agent.population.append(bb84_protocol)
        print(f"   添加BB84基准: {bb84_protocol.get_statistics()['node_count']}节点")
        
        # 添加随机协议
        for i in range(population_size - 2):
            random_protocol = self.agent.generate_random_protocol()
            self.agent.population.append(random_protocol)
        
        print(f"   种群大小: {len(self.agent.population)}")
        
        # 训练参数
        self.agent.config.max_iterations = iterations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.4  # 提高变异率以探索更多结构
        
        # 运行训练
        print(f"\n2. 🧠 开始训练 ({iterations}代)...")
        result = self.agent.train(iterations=iterations, population_size=population_size)
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 分析最佳协议
        print("\n3. 📊 分析最佳协议...")
        if result.get('best_protocol'):
            best_protocol = result['best_protocol']
            best_features = self.detect_tf_features(best_protocol)
            
            result['tf_features'] = best_features
            result['best_protocol_stats'] = best_protocol.get_statistics()
            
            print(f"   最佳适应度: {result['best_fitness']:.4f}")
            print(f"   TF分数: {best_features['tf_score']:.3f}")
            print(f"   类似TF协议: {'✅ 是' if best_features['is_tf_like'] else '❌ 否'}")
            
            # 显示关键特征
            print(f"\n   关键TF特征:")
            if best_features["structural"]["two_remote_senders"]:
                print(f"     • 两个远程发送方: ✅")
            if best_features["structural"]["interference_measurement"]:
                print(f"     • 干涉测量: ✅")
            if best_features["interference"]["mach_zehnder"]:
                print(f"     • 马赫-曾德尔干涉仪: ✅")
            if best_features["interference"]["phase_stabilizer"]:
                print(f"     • 相位稳定器: ✅")
            if best_features["interference"]["time_synchronization"]:
                print(f"     • 时间同步: ✅")
            if best_features["performance"]["long_distance"]:
                print(f"     • 长距离能力: ✅")
        
        # 评估TF模板作为对比
        print("\n4. 🔄 对比评估...")
        tf_template_fitness = self.base_evaluate(tf_template)
        tf_template_features = self.detect_tf_features(tf_template)
        
        bb84_fitness = self.base_evaluate(bb84_protocol)
        
        print(f"   TF模板适应度: {tf_template_fitness:.4f}")
        print(f"   TF模板TF分数: {tf_template_features['tf_score']:.3f}")
        print(f"   BB84适应度: {bb84_fitness:.4f}")
        
        if result.get('best_fitness', 0) > 0:
            improvement_vs_tf = ((result['best_fitness'] - tf_template_fitness) / tf_template_fitness * 100) if tf_template_fitness > 0 else 0
            improvement_vs_bb84 = ((result['best_fitness'] - bb84_fitness) / bb84_fitness * 100) if bb84_fitness > 0 else 0
            
            print(f"\n   🚀 性能提升:")
            print(f"     相对于TF模板: {improvement_vs_tf:+.1f}%")
            print(f"     相对于BB84: {improvement_vs_bb84:+.1f}%")
        
        # 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "TF-QKD Protocol Discovery",
            "config": {
                "iterations": iterations,
                "population_size": population_size,
                "mutation_rate": self.agent.config.mutation_rate
            },
            "baseline_results": {
                "tf_template": {
                    "fitness": tf_template_fitness,
                    "tf_score": tf_template_features['tf_score'],
                    "is_tf_like": tf_template_features['is_tf_like'],
                    "stats": tf_template.get_statistics()
                },
                "bb84": {
                    "fitness": bb84_fitness,
                    "stats": bb84_protocol.get_statistics()
                }
            },
            "ai_training_result": {
                "best_fitness": result.get('best_fitness', 0),
                "best_protocol_stats": result.get('best_protocol_stats', {}),
                "tf_features": result.get('tf_features', {}),
                "fitness_history": result.get('fitness_history', []),
                "iterations": iterations
            },
            "comparison": {
                "improvement_vs_tf_template": improvement_vs_tf if 'improvement_vs_tf' in locals() else 0,
                "improvement_vs_bb84": improvement_vs_bb84 if 'improvement_vs_bb84' in locals() else 0,
                "tf_discovery_success": result.get('tf_features', {}).get('is_tf_like', False)
            },
            "timestamp": timestamp
        }
        
        filename = f"results/tf_qkd_experiment_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 结果已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ TF-QKD实验完成!")
        print("=" * 70)
        
        return result_data


def main():
    """主函数"""
    print("=" * 70)
    print("🎯 TF-QKD（双场量子密钥分发）协议发现实验")
    print("=" * 70)
    
    experiment = TFQKDExperiment()
    
    # 询问实验参数
    print("\n选择实验模式:")
    print("  1. 快速实验 (50代)")
    print("  2. 标准实验 (100代)")
    print("  3. 完整实验 (200代)")
    
    choice = input("\n请输入选择 (1-3, 默认:2): ").strip()
    
    if choice == '1':
        iterations = 50
        population_size = 12
    elif choice == '3':
        iterations = 200
        population_size = 20
    else:
        iterations = 100
        population_size = 15
    
    print(f"\n实验配置:")
    print(f"  迭代次数: {iterations}")
    print(f"  种群大小: {population_size}")
    print(f"  开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行实验
    result = experiment.run_tf_experiment(
        iterations=iterations,
        population_size=population_size
    )
    
    # 显示总结
    print("\n📈 实验总结:")
    print(f"  最佳适应度: {result['ai_training_result']['best_fitness']:.4f}")
    print(f"  TF分数: {result['ai_training_result']['tf_features'].get('tf_score', 0):.3f}")
    
    tf_success = result['comparison']['tf_discovery_success']
    if tf_success:
        print(f"  TF协议发现: ✅ 成功!")
        improvement = result['comparison']['improvement_vs_tf_template']
        print(f"  性能提升: {improvement:+.1f}% (相对于TF模板)")
    else:
        print(f"  TF协议发现: ⚠️ 部分成功")
        print(f"  最佳协议TF分数: {result['ai_training_result']['tf_features'].get('tf_score', 0):.3f}/0.65")
    
    print(f"\n📁 结果文件: results/tf_qkd_experiment_*.json")
    
    print("\n🎯 下一步建议:")
    if tf_success:
        print("  1. 深入分析发现的TF协议结构")
        print("  2. 运行验证实验确认稳定性")
        print("  3. 将结果整合到论文中")
    else:
        print("  1. 调整TF特征权重和检测方法")
        print("  2. 增加训练代数和种群大小")
        print("  3. 优化引导式变异策略")
    
    print("  4. 尝试发现其他协议类型 (E91, CV-QKD等)")


if __name__ == "__main__":
    main()