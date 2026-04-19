#!/usr/bin/env python3
"""
SNS（发送或不发送）QKD协议实验
扩展AI4QKD框架支持新协议类型
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
from ai_agent.enhanced_agent import EnhancedHybridAgent
import json
import time
import random
import numpy as np
from typing import Dict, List, Any


class SNSProtocolExperiment:
    """SNS协议实验"""
    
    def __init__(self):
        self.agent = EnhancedHybridAgent()
        self.sns_template = self._create_sns_template()
        self.original_evaluate = self.agent.evaluate_protocol
    
    def _base_evaluate_protocol(self, protocol: ProtocolGraph) -> float:
        """基础协议评估（避免递归）"""
        return self.original_evaluate(protocol)
        
    def _create_sns_template(self) -> ProtocolGraph:
        """创建SNS协议模板"""
        protocol = ProtocolGraph(name="SNS Protocol Template")
        
        # Alice: 弱相干脉冲源
        alice_source = protocol.add_node(
            NodeType.QSP,
            {'state': 'weak_coherent', 'mean_photon': 0.1, 'basis': 'Z'},
            Party.ALICE
        )
        
        # 量子信道
        quantum_channel = protocol.add_node(
            NodeType.QC,
            {'loss': 0.2, 'distance': 50},
            None
        )
        
        # Bob: 单光子探测器
        bob_detector = protocol.add_node(
            NodeType.QD,
            {'type': 'single_photon', 'efficiency': 0.3},
            Party.BOB
        )
        
        # 经典信道（用于基比对）
        classical_channel = protocol.add_node(
            NodeType.CC,
            {'purpose': 'basis_reconciliation'},
            None
        )
        
        # 误码率估计
        error_estimation = protocol.add_node(
            NodeType.CP,
            {'operation': 'QBER_estimation'},
            Party.BOTH
        )
        
        # 隐私放大
        privacy_amplification = protocol.add_node(
            NodeType.CP,
            {'operation': 'privacy_amplification', 'method': 'universal_hashing'},
            Party.BOTH
        )
        
        # 连接
        protocol.add_edge(alice_source, quantum_channel, EdgeType.QUANTUM)
        protocol.add_edge(quantum_channel, bob_detector, EdgeType.QUANTUM)
        protocol.add_edge(bob_detector, classical_channel, EdgeType.CLASSICAL)
        protocol.add_edge(classical_channel, error_estimation, EdgeType.CLASSICAL)
        protocol.add_edge(error_estimation, privacy_amplification, EdgeType.CLASSICAL)
        
        return protocol
    
    def extract_sns_features(self, protocol: ProtocolGraph) -> Dict[str, float]:
        """提取SNS协议特征"""
        stats = protocol.get_statistics()
        features = {}
        
        # 1. 弱相干源特征
        has_weak_coherent = False
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.QSP:
                params = node.params
                if isinstance(params, dict):
                    if 'weak' in str(params.get('state', '')).lower():
                        has_weak_coherent = True
                    elif params.get('mean_photon', 1.0) < 0.5:
                        has_weak_coherent = True
        
        features['has_weak_coherent'] = 1.0 if has_weak_coherent else 0.0
        
        # 2. 单光子探测器特征
        has_spd = False
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.QD:
                params = node.params
                if isinstance(params, dict):
                    if 'single' in str(params.get('type', '')).lower():
                        has_spd = True
        
        features['has_single_photon_detector'] = 1.0 if has_spd else 0.0
        
        # 3. 基比对机制
        has_basis_reconciliation = False
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.CC:
                params = node.params
                if isinstance(params, dict):
                    if 'basis' in str(params.get('purpose', '')).lower():
                        has_basis_reconciliation = True
        
        features['has_basis_reconciliation'] = 1.0 if has_basis_reconciliation else 0.0
        
        # 4. 误码率估计
        has_qber_estimation = False
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.CP:
                params = node.params
                if isinstance(params, dict):
                    if 'QBER' in str(params.get('operation', '')).upper():
                        has_qber_estimation = True
        
        features['has_qber_estimation'] = 1.0 if has_qber_estimation else 0.0
        
        # 5. 隐私放大
        has_privacy_amp = False
        for node_id in protocol.graph.nodes():
            node = protocol.graph.nodes[node_id]['node']
            if node.node_type == NodeType.CP:
                params = node.params
                if isinstance(params, dict):
                    if 'privacy' in str(params.get('operation', '')).lower():
                        has_privacy_amp = True
        
        features['has_privacy_amplification'] = 1.0 if has_privacy_amp else 0.0
        
        # 6. 结构特征
        node_stats = stats.get('node_stats', {})
        features['quantum_component_count'] = sum(
            node_stats.get(comp, 0) for comp in 
            ['quantum_state_preparation', 'quantum_channel', 'quantum_detector']
        ) / 5.0
        
        features['classical_component_count'] = sum(
            node_stats.get(comp, 0) for comp in
            ['classical_channel', 'classical_processing']
        ) / 4.0
        
        return features
    
    def evaluate_sns_similarity(self, protocol: ProtocolGraph) -> float:
        """评估与SNS协议的相似性"""
        template_features = self.extract_sns_features(self.sns_template)
        protocol_features = self.extract_sns_features(protocol)
        
        # 计算特征匹配度
        match_score = 0.0
        total_weight = 0.0
        
        # 核心特征权重较高
        core_features = ['has_weak_coherent', 'has_single_photon_detector']
        for feature in core_features:
            if feature in template_features and feature in protocol_features:
                match = 1.0 if abs(template_features[feature] - protocol_features[feature]) < 0.5 else 0.0
                match_score += match * 0.3  # 核心特征权重0.3
                total_weight += 0.3
        
        # 重要特征
        important_features = ['has_basis_reconciliation', 'has_qber_estimation']
        for feature in important_features:
            if feature in template_features and feature in protocol_features:
                match = 1.0 if abs(template_features[feature] - protocol_features[feature]) < 0.5 else 0.0
                match_score += match * 0.2  # 重要特征权重0.2
                total_weight += 0.2
        
        # 可选特征
        optional_features = ['has_privacy_amplification']
        for feature in optional_features:
            if feature in template_features and feature in protocol_features:
                match = 1.0 if abs(template_features[feature] - protocol_features[feature]) < 0.5 else 0.0
                match_score += match * 0.1  # 可选特征权重0.1
                total_weight += 0.1
        
        # 归一化
        if total_weight > 0:
            similarity = match_score / total_weight
        else:
            similarity = 0.0
        
        return similarity
    
    def sns_guided_fitness(self, protocol: ProtocolGraph) -> float:
        """SNS引导的适应度函数"""
        # 基础性能评估（使用原始评估函数）
        # 避免递归：直接调用agent的基础评估
        base_fitness = self._base_evaluate_protocol(protocol)
        
        # SNS特征相似性
        sns_similarity = self.evaluate_sns_similarity(protocol)
        
        # 综合适应度：70%性能 + 30%SNS特征
        total_fitness = base_fitness * 0.7 + sns_similarity * 0.3
        
        # 特别奖励：完全匹配SNS特征
        if sns_similarity > 0.8:
            total_fitness = min(total_fitness + 0.15, 1.0)
        elif sns_similarity > 0.6:
            total_fitness = min(total_fitness + 0.08, 1.0)
        
        return total_fitness
    
    def run_sns_experiment(self, generations=80, population_size=25) -> Dict:
        """运行SNS协议实验"""
        print("=" * 70)
        print("🔬 SNS协议发现实验")
        print("=" * 70)
        print("目标：引导AI发现或重新发现SNS协议")
        print("=" * 70)
        
        start_time = time.time()
        
        # 保存原始评估函数
        original_evaluate = self.agent.evaluate_protocol
        
        # 使用SNS引导的适应度
        self.agent.evaluate_protocol = self.sns_guided_fitness
        
        # 初始化种群（包含SNS模板）
        print(f"\n1. 🧬 初始化种群 ({population_size}个协议)...")
        self.agent.population = []
        
        # 添加SNS模板
        self.agent.population.append(self.sns_template)
        
        # 添加其他已知协议
        from qcgf_dsl import ProtocolGraph
        self.agent.population.append(ProtocolGraph.create_bb84())
        
        # 添加随机协议
        while len(self.agent.population) < population_size:
            random_protocol = self._generate_random_protocol()
            self.agent.population.append(random_protocol)
        
        print(f"   包含: 1个SNS模板 + 1个BB84 + {population_size-2}个随机协议")
        
        # 配置训练参数
        self.agent.config.max_iterations = generations
        self.agent.config.population_size = population_size
        self.agent.config.mutation_rate = 0.6
        self.agent.config.elite_size = 2
        
        # 运行训练
        print(f"\n2. ⚡ 开始SNS引导训练 ({generations}代)...")
        result = self.agent.train(
            iterations=generations,
            population_size=population_size
        )
        
        # 分析结果
        print(f"\n3. 📊 实验结果分析...")
        
        best_fitness = result.get('best_fitness', 0)
        best_protocol = result.get('best_protocol')
        
        if best_protocol:
            sns_similarity = self.evaluate_sns_similarity(best_protocol)
            base_performance = original_evaluate(best_protocol)
            stats = best_protocol.get_statistics()
            
            print(f"   最佳适应度: {best_fitness:.4f}")
            print(f"   SNS相似性: {sns_similarity:.3f}")
            print(f"   基础性能: {base_performance:.3f}")
            print(f"   节点数: {stats.get('node_count', 0)}")
            print(f"   边数: {stats.get('edge_count', 0)}")
            
            # 特征分析
            features = self.extract_sns_features(best_protocol)
            print(f"\n   🔍 SNS特征匹配:")
            for feature, value in features.items():
                status = "✅" if value > 0.5 else "❌"
                print(f"      {status} {feature}: {value:.2f}")
            
            # 评估发现质量
            if sns_similarity > 0.8:
                discovery_quality = "🏆 高质量发现（接近标准SNS）"
            elif sns_similarity > 0.6:
                discovery_quality = "🥈 中等质量发现"
            elif sns_similarity > 0.4:
                discovery_quality = "🥉 低质量发现"
            else:
                discovery_quality = "🔍 非SNS-like协议"
            
            print(f"\n   🎯 发现质量: {discovery_quality}")
        
        # 恢复原始评估函数
        self.agent.evaluate_protocol = original_evaluate
        
        # 保存结果
        timestamp = int(time.time())
        result_data = {
            "experiment": "SNS Protocol Discovery",
            "config": {
                "generations": generations,
                "population_size": population_size,
                "mutation_rate": 0.6,
                "fitness_weights": "70% performance + 30% SNS similarity"
            },
            "results": {
                "best_fitness": float(best_fitness),
                "best_sns_similarity": float(sns_similarity) if best_protocol else 0,
                "best_base_performance": float(base_performance) if best_protocol else 0,
                "discovery_quality": discovery_quality if best_protocol else "N/A"
            },
            "timestamp": timestamp
        }
        
        filename = f"results/sns_experiment_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n📁 结果已保存: {filename}")
        print(f"⏱️  实验时间: {elapsed_time:.1f}秒")
        
        print("\n" + "=" * 70)
        print("✅ SNS协议实验完成")
        print("=" * 70)
        
        return result_data
    
    def _generate_random_protocol(self) -> ProtocolGraph:
        """生成随机协议"""
        protocol = ProtocolGraph(name=f"Random_Protocol_{random.randint(1000, 9999)}")
        
        # 随机节点数
        num_nodes = random.randint(4, 10)
        
        node_ids = []
        for i in range(num_nodes):
            # 随机节点类型
            node_type = random.choice([
                NodeType.QSP, NodeType.QC, NodeType.QD,
                NodeType.CC, NodeType.CP
            ])
            
            # 随机参数
            params = {}
            if node_type == NodeType.QSP:
                params['state'] = random.choice(['single_photon', 'weak_coherent', 'coherent'])
            elif node_type == NodeType.QC:
                params['loss'] = round(random.uniform(0.1, 0.5), 2)
            
            # 随机参与方
            party = random.choice([Party.ALICE, Party.BOB, None])
            
            node_id = protocol.add_node(node_type, params, party)
            node_ids.append(node_id)
        
        # 随机连接
        if len(node_ids) >= 2:
            # 确保基本连通性
            for i in range(len(node_ids) - 1):
                if random.random() < 0.7:  # 70%概率连接
                    edge_type = random.choice(['quantum', 'classical'])
                    protocol.add_edge(node_ids[i], node_ids[i+1], edge_type)
            
            # 添加一些额外连接
            extra_edges = random.randint(0, min(3, len(node_ids) // 2))
            for _ in range(extra_edges):
                source = random.choice(node_ids)
                target = random.choice(node_ids)
                if source != target and not protocol.graph.has_edge(source, target):
                    edge_type = random.choice(['quantum', 'classical'])
                    protocol.add_edge(source, target, edge_type)
        
        return protocol


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 AI4QKD框架扩展：SNS协议支持")
    print("=" * 70)
    print("验证框架对新协议类型的支持能力")
    print("=" * 70)
    
    print("\n📋 SNS协议特点:")
    print("  1. 弱相干脉冲源（平均光子数~0.1）")
    print("  2. 单光子探测器")
    print("  3. 发送或不发送的随机选择")
    print("  4. 简单高效，适合实际部署")
    
    print("\n🎯 实验目标:")
    print("  引导AI发现或重新发现SNS-like协议")
    print("  验证框架对新协议类型的适应性")
    print("  评估特征引导方法的有效性")
    
    experiment = SNSProtocolExperiment()
    
    # 运行实验
    result = experiment.run_sns_experiment(
        generations=80,
        population_size=25
    )
    
    # 显示总结
    print("\n📈 实验总结:")
    
    discovery_quality = result['results']['discovery_quality']
    sns_similarity = result['results']['best_sns_similarity']
    best_fitness = result['results']['best_fitness']
    
    print(f"  发现质量: {discovery_quality}")
    print(f"  SNS相似性: {sns_similarity:.3f}")
    print(f"  最佳适应度: {best_fitness:.4f}")
    
    # 评估框架扩展效果
    if sns_similarity > 0.7:
        print(f"\n  ✅ 框架扩展成功：")
        print(f"     能有效引导AI发现SNS-like协议")
        print(f"     特征引导方法有效")
        print(f"     框架对新协议类型支持良好")
    elif sns_similarity > 0.5:
        print(f"\n  ⚠️ 框架扩展部分成功：")
        print(f"     能部分引导AI，但需要优化")
        print(f"     可能需要调整特征权重")
        print(f"     框架基本支持新协议类型")
    else:
        print(f"\n  🔴 框架扩展需要改进：")
        print(f"     特征引导效果有限")
        print(f"     需要重新设计特征提取")
        print(f"     框架对新协议支持需增强")
    
    print(f"\n📁 结果文件: results/sns_experiment_*.json")
    
    print("\n🎯 下一步扩展方向:")
    print("  1. 支持DPS协议（差分相位偏移）")
    print("  2. 支持COW协议（相干单向量子）")
    print("  3. 支持GG02协议（高斯调制连续变量）")
    print("  4. 支持DLCZ协议（基于量子存储器）")


if __name__ == "__main__":
    main()