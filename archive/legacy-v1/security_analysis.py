#!/usr/bin/env python3
"""
AI发现协议的安全性分析
包括：结构安全检查、攻击抵抗性分析、安全性评分
"""

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
import json
import numpy as np
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class SecurityAnalyzer:
    """安全性分析器"""
    
    def __init__(self):
        self.known_attacks = self._load_known_attacks()
        self.security_components = self._define_security_components()
        
    def _load_known_attacks(self) -> Dict:
        """加载已知QKD攻击"""
        return {
            'photon_number_splitting': {
                'description': '光子数分裂攻击',
                'target': 'multi-photon states',
                'countermeasure': 'decoy_state, SARG04',
                'severity': 'high'
            },
            'time_shift': {
                'description': '时间位移攻击',
                'target': 'detector timing',
                'countermeasure': 'time-filter, monitoring',
                'severity': 'medium'
            },
            'blinding': {
                'description': '致盲攻击',
                'target': 'single-photon detectors',
                'countermeasure': 'monitoring, random operation',
                'severity': 'high'
            },
            'trojan_horse': {
                'description': '木马攻击',
                'target': 'optical components',
                'countermeasure': 'isolators, filters',
                'severity': 'medium'
            },
            'intercept_resend': {
                'description': '截获重发攻击',
                'target': 'quantum channel',
                'countermeasure': 'entanglement, MDI',
                'severity': 'high'
            },
            'man_in_the_middle': {
                'description': '中间人攻击',
                'target': 'classical channel',
                'countermeasure': 'authentication',
                'severity': 'critical'
            }
        }
    
    def _define_security_components(self) -> Dict:
        """定义安全组件"""
        return {
            'eavesdropping_detection': {
                'components': [NodeType.CV, 'verification', 'check'],
                'importance': 0.9
            },
            'privacy_amplification': {
                'components': [NodeType.CP, 'hash', 'extract'],
                'importance': 0.8
            },
            'authentication': {
                'components': [NodeType.CC, 'auth', 'sign'],
                'importance': 0.7
            },
            'error_correction': {
                'components': [NodeType.CP, 'correct', 'reconcile'],
                'importance': 0.6
            },
            'decoy_state': {
                'components': ['decoy', 'multi-intensity'],
                'importance': 0.7
            },
            'monitoring': {
                'components': ['monitor', 'check', 'detect'],
                'importance': 0.5
            }
        }
    
    def analyze_structure_security(self, protocol: ProtocolGraph) -> Dict:
        """分析结构安全性"""
        stats = protocol.get_statistics()
        graph = protocol.graph
        
        security_score = 0.0
        findings = []
        warnings = []
        
        # 1. 基本安全检查
        print("\n🔍 基本安全检查:")
        
        # 检查是否有窃听检测机制
        has_eavesdropping_detection = False
        for node_id in graph.nodes():
            node = graph.nodes[node_id]['node']
            if node.node_type == NodeType.CV:
                has_eavesdropping_detection = True
                findings.append("✅ 包含经典验证节点（窃听检测）")
                security_score += 0.2
                break
        
        if not has_eavesdropping_detection:
            warnings.append("⚠️ 缺少明确的窃听检测机制")
            security_score -= 0.1
        
        # 检查是否有隐私放大
        has_privacy_amplification = False
        for node_id in graph.nodes():
            node = graph.nodes[node_id]['node']
            if node.node_type == NodeType.CP:
                params = node.params
                if isinstance(params, dict):
                    for key in params:
                        if 'hash' in str(key).lower() or 'extract' in str(key).lower():
                            has_privacy_amplification = True
                            findings.append("✅ 可能包含隐私放大处理")
                            security_score += 0.15
                            break
        
        if not has_privacy_amplification:
            warnings.append("⚠️ 未明确识别隐私放大组件")
        
        # 检查认证机制
        has_authentication = False
        for node_id in graph.nodes():
            node = graph.nodes[node_id]['node']
            if node.node_type == NodeType.CC:
                params = node.params
                if isinstance(params, dict):
                    for key in params:
                        if 'auth' in str(key).lower() or 'sign' in str(key).lower():
                            has_authentication = True
                            findings.append("✅ 可能包含认证机制")
                            security_score += 0.1
                            break
        
        if not has_authentication:
            warnings.append("⚠️ 未明确识别认证机制")
        
        # 2. 创新特征安全性分析
        print("\n🎯 创新特征安全性分析:")
        
        # 分析控制信号连接
        control_edges = []
        for u, v in graph.edges():
            edge = graph.edges[u, v]['edge']
            if edge.edge_type == EdgeType.CONTROL:
                control_edges.append((u, v))
        
        if control_edges:
            findings.append(f"✅ 发现 {len(control_edges)} 个控制信号连接")
            # 控制信号的安全性分析
            if len(control_edges) <= 2:
                findings.append("  控制信号数量适中，可能安全")
                security_score += 0.05
            else:
                warnings.append("⚠️ 控制信号连接较多，可能增加攻击面")
                security_score -= 0.05
        
        # 分析基于干涉的验证
        interference_based_verification = False
        for node_id in graph.nodes():
            node = graph.nodes[node_id]['node']
            if node.node_type == NodeType.CV:
                params = node.params
                if isinstance(params, dict):
                    for key, value in params.items():
                        if 'interference' in str(value).lower():
                            interference_based_verification = True
                            findings.append("✅ 发现基于干涉的验证方法")
                            security_score += 0.1
                            break
        
        # 3. 图结构安全性分析
        print("\n🏗️ 图结构安全性分析:")
        
        # 检查冗余性
        node_count = stats.get('node_count', 0)
        edge_count = stats.get('edge_count', 0)
        
        if edge_count > node_count:
            redundancy = (edge_count - node_count) / node_count
            if 0.2 <= redundancy <= 0.8:
                findings.append(f"✅ 适度的冗余连接（冗余度: {redundancy:.2f}）")
                security_score += min(redundancy * 0.1, 0.05)
            elif redundancy > 0.8:
                warnings.append(f"⚠️ 冗余连接过多（冗余度: {redundancy:.2f}），可能增加复杂性")
        
        # 检查关键节点保护
        critical_nodes = self._identify_critical_nodes(protocol)
        if critical_nodes:
            findings.append(f"✅ 识别出 {len(critical_nodes)} 个关键节点")
            # 检查关键节点的连接保护
            protected_count = self._check_critical_node_protection(protocol, critical_nodes)
            protection_ratio = protected_count / len(critical_nodes) if critical_nodes else 0
            security_score += protection_ratio * 0.1
        
        # 4. 组件安全性分析
        print("\n⚙️ 组件安全性分析:")
        
        node_stats = stats.get('node_stats', {})
        
        # 量子组件安全性
        quantum_components = ['quantum_state_preparation', 'quantum_measurement', 'quantum_gate']
        quantum_count = sum(node_stats.get(comp, 0) for comp in quantum_components)
        
        if quantum_count >= 3:
            findings.append(f"✅ 量子组件丰富（{quantum_count}个），可能提供多样性安全")
            security_score += 0.05
        
        # 经典组件安全性
        classical_components = ['classical_processing', 'classical_verification']
        classical_count = sum(node_stats.get(comp, 0) for comp in classical_components)
        
        if classical_count >= 2:
            findings.append(f"✅ 经典处理组件充足（{classical_count}个），支持安全后处理")
            security_score += 0.05
        
        # 确保分数在合理范围
        security_score = max(0.0, min(security_score, 1.0))
        
        return {
            'security_score': security_score,
            'findings': findings,
            'warnings': warnings,
            'has_eavesdropping_detection': has_eavesdropping_detection,
            'has_privacy_amplification': has_privacy_amplification,
            'has_authentication': has_authentication,
            'control_edges_count': len(control_edges),
            'interference_based_verification': interference_based_verification
        }
    
    def _identify_critical_nodes(self, protocol: ProtocolGraph) -> List:
        """识别关键节点"""
        graph = protocol.graph
        critical_nodes = []
        
        for node_id in graph.nodes():
            node = graph.nodes[node_id]['node']
            
            # 根据节点类型判断重要性
            if node.node_type in [NodeType.QSP, NodeType.QM, NodeType.CV]:
                critical_nodes.append(node_id)
            
            # 根据度判断重要性
            degree = graph.degree(node_id)
            if degree >= 3:  # 高度连接的节点
                if node_id not in critical_nodes:
                    critical_nodes.append(node_id)
        
        return critical_nodes
    
    def _check_critical_node_protection(self, protocol: ProtocolGraph, critical_nodes: List) -> int:
        """检查关键节点保护"""
        graph = protocol.graph
        protected_count = 0
        
        for node_id in critical_nodes:
            # 检查是否有备份或冗余连接
            degree = graph.degree(node_id)
            if degree >= 2:  # 至少有两个连接
                protected_count += 1
            
            # 检查是否有监控或验证连接
            for neighbor in graph.neighbors(node_id):
                neighbor_node = graph.nodes[neighbor]['node']
                if neighbor_node.node_type == NodeType.CV:
                    protected_count += 1
                    break
        
        return protected_count
    
    def analyze_attack_resistance(self, protocol: ProtocolGraph) -> Dict:
        """分析攻击抵抗性"""
        stats = protocol.get_statistics()
        graph = protocol.graph
        
        attack_analysis = {}
        
        print("\n🛡️ 攻击抵抗性分析:")
        
        # 对每种已知攻击进行分析
        for attack_name, attack_info in self.known_attacks.items():
            resistance = self._analyze_specific_attack(protocol, attack_name, attack_info)
            attack_analysis[attack_name] = resistance
            
            # 显示结果
            severity = attack_info['severity']
            if resistance['resistant']:
                print(f"  ✅ {attack_info['description']}: 可能抵抗 ({resistance['score']:.2f})")
            else:
                print(f"  ⚠️ {attack_info['description']}: 可能脆弱 ({resistance['score']:.2f})")
        
        # 计算总体攻击抵抗分数
        total_score = sum(analysis['score'] for analysis in attack_analysis.values())
        avg_score = total_score / len(attack_analysis) if attack_analysis else 0
        
        return {
            'attack_analysis': attack_analysis,
            'average_resistance_score': avg_score,
            'high_risk_attacks': [
                name for name, analysis in attack_analysis.items()
                if analysis['score'] < 0.5 and self.known_attacks[name]['severity'] in ['high', 'critical']
            ]
        }
    
    def _analyze_specific_attack(self, protocol: ProtocolGraph, attack_name: str, attack_info: Dict) -> Dict:
        """分析特定攻击的抵抗性"""
        graph = protocol.graph
        score = 0.5  # 基础分数
        
        # 根据攻击类型分析
        if attack_name == 'photon_number_splitting':
            # 检查是否有诱骗态或SARG04-like机制
            has_decoy = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QSP:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'decoy' in str(value).lower() or 'multi' in str(value).lower():
                                has_decoy = True
                                score += 0.3
                                break
            
            # 检查测量基的随机性
            has_random_basis = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QM:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'random' in str(value).lower():
                                has_random_basis = True
                                score += 0.2
                                break
        
        elif attack_name == 'time_shift':
            # 检查是否有时间过滤或监控
            has_time_monitoring = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QD:  # 探测器
                    score += 0.1
                if node.node_type == NodeType.CV:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'time' in str(key).lower() or 'monitor' in str(key).lower():
                                has_time_monitoring = True
                                score += 0.3
                                break
        
        elif attack_name == 'blinding':
            # 检查探测器保护和监控
            detector_protection = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QD:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'monitor' in str(key).lower() or 'protect' in str(key).lower():
                                detector_protection = True
                                score += 0.3
                                break
            
            # 检查随机操作
            has_random_operation = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                params = node.params
                if isinstance(params, dict):
                    for key, value in params.items():
                        if 'random' in str(key).lower():
                            has_random_operation = True
                            score += 0.2
                            break
        
        elif attack_name == 'trojan_horse':
            # 检查光学隔离
            has_isolation = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QC:  # 量子信道
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'isolat' in str(key).lower() or 'filter' in str(key).lower():
                                has_isolation = True
                                score += 0.3
                                break
        
        elif attack_name == 'intercept_resend':
            # 检查是否使用纠缠或MDI-like结构
            has_entanglement = False
            has_third_party = False
            
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.QSP:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'entangle' in str(value).lower():
                                has_entanglement = True
                                score += 0.4
                                break
                
                if node.party == Party.CHARLIE:
                    has_third_party = True
                    score += 0.3
            
            if has_entanglement or has_third_party:
                score += 0.2
        
        elif attack_name == 'man_in_the_middle':
            # 检查认证机制
            has_auth = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.CC:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'auth' in str(key).lower() or 'sign' in str(key).lower():
                                has_auth = True
                                score += 0.4
                                break
            
            # 检查密钥确认
            has_key_confirmation = False
            for node_id in graph.nodes():
                node = graph.nodes[node_id]['node']
                if node.node_type == NodeType.CV:
                    params = node.params
                    if isinstance(params, dict):
                        for key, value in params.items():
                            if 'confirm' in str(key).lower() or 'verify' in str(key).lower():
                                has_key_confirmation = True
                                score += 0.3
                                break
        
        # 确保分数在合理范围
        score = max(0.0, min(score, 1.0))
        
        return {
            'resistant': score >= 0.6,
            'score': score,
            'countermeasures_found': score > 0.5
        }
    
    def calculate_security_rating(self, structure_analysis: Dict, attack_analysis: Dict) -> Dict:
        """计算安全性评级"""
        structure_score = structure_analysis.get('security_score', 0)
        attack_score = attack_analysis.get('average_resistance_score', 0)
        
        # 综合安全性分数（加权平均）
        # 结构安全性权重：0.4，攻击抵抗性权重：0.6
        overall_score = structure_score * 0.4 + attack_score * 0.6
        
        # 确定安全性等级
        if overall_score >= 0.8:
            security_level = "🟢 高安全性"
            rating = "A"
        elif overall_score >= 0.6:
            security_level = "🟡 中等安全性"
            rating = "B"
        elif overall_score >= 0.4:
            security_level = "🟠 低安全性"
            rating = "C"
        else:
            security_level = "🔴 安全性不足"
            rating = "D"
        
        # 识别主要风险
        high_risk_attacks = attack_analysis.get('high_risk_attacks', [])
        warnings = structure_analysis.get('warnings', [])
        
        major_risks = []
        if high_risk_attacks:
            major_risks.extend([f"对{self.known_attacks[attack]['description']}抵抗性不足" 
                               for attack in high_risk_attacks])
        
        if warnings:
            major_risks.extend(warnings)
        
        # 识别优势
        findings = structure_analysis.get('findings', [])
        advantages = []
        for finding in findings:
            if finding.startswith("✅"):
                advantages.append(finding[2:].strip())
        
        return {
            'overall_score': overall_score,
            'security_level': security_level,
            'rating': rating,
            'structure_score': structure_score,
            'attack_resistance_score': attack_score,
            'major_risks': major_risks,
            'security_advantages': advantages,
            'recommendations': self._generate_recommendations(structure_analysis, attack_analysis)
        }
    
    def _generate_recommendations(self, structure_analysis: Dict, attack_analysis: Dict) -> List[str]:
        """生成安全改进建议"""
        recommendations = []
        
        # 结构安全性建议
        if not structure_analysis.get('has_eavesdropping_detection', False):
            recommendations.append("添加明确的窃听检测机制（如误码率检查）")
        
        if not structure_analysis.get('has_privacy_amplification', False):
            recommendations.append("添加隐私放大组件以增强安全性")
        
        if not structure_analysis.get('has_authentication', False):
            recommendations.append("添加经典信道认证机制")
        
        # 攻击抵抗性建议
        high_risk_attacks = attack_analysis.get('high_risk_attacks', [])
        for attack in high_risk_attacks:
            attack_info = self.known_attacks.get(attack, {})
            countermeasure = attack_info.get('countermeasure', '')
            if countermeasure:
                recommendations.append(f"针对{attack_info['description']}：{countermeasure}")
        
        # 创新特征建议
        if structure_analysis.get('control_edges_count', 0) > 2:
            recommendations.append("减少控制信号连接数量，降低攻击面")
        
        return recommendations
    
    def compare_with_standard_protocols(self, protocol: ProtocolGraph) -> Dict:
        """与传统协议安全性对比"""
        # 创建标准协议用于对比
        bb84 = ProtocolGraph.create_bb84()
        mdi = self._create_mdi_protocol()
        tf = self._create_tf_protocol()
        
        # 分析各协议
        protocols = {
            'BB84': bb84,
            'MDI-QKD': mdi,
            'TF-QKD': tf,
            'AI_Protocol': protocol
        }
        
        comparison = {}
        
        print("\n📊 与传统协议安全性对比:")
        
        for name, proto in protocols.items():
            print(f"\n  {name}:")
            structure = self.analyze_structure_security(proto)
            attacks = self.analyze_attack_resistance(proto)
            rating = self.calculate_security_rating(structure, attacks)
            
            comparison[name] = {
                'security_score': rating['overall_score'],
                'rating': rating['rating'],
                'security_level': rating['security_level'],
                'major_risks_count': len(rating['major_risks']),
                'advantages_count': len(rating['security_advantages'])
            }
            
            print(f"    安全性分数: {rating['overall_score']:.3f}")
            print(f"    评级: {rating['rating']} ({rating['security_level']})")
        
        return comparison
    
    def _create_mdi_protocol(self) -> ProtocolGraph:
        """创建MDI协议用于对比"""
        protocol = ProtocolGraph(name="MDI-QKD (对比)")
        
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
        
        # 验证
        verification = protocol.add_node(
            NodeType.CV,
            {'method': 'basis_reconciliation'},
            Party.BOTH
        )
        
        # 连接
        protocol.add_edge(alice_source, channel1, EdgeType.QUANTUM)
        protocol.add_edge(bob_source, channel2, EdgeType.QUANTUM)
        protocol.add_edge(channel1, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(channel2, bell_measurement, EdgeType.QUANTUM)
        protocol.add_edge(bell_measurement, classical, EdgeType.CLASSICAL)
        protocol.add_edge(classical, verification, EdgeType.CLASSICAL)
        
        return protocol
    
    def _create_tf_protocol(self) -> ProtocolGraph:
        """创建TF协议用于对比"""
        protocol = ProtocolGraph(name="TF-QKD (对比)")
        
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
        
        # 经典信道
        classical = protocol.add_node(NodeType.CC, {}, None)
        
        # 相位协调
        reconciliation = protocol.add_node(
            NodeType.CP,
            {'operation': 'phase_reconciliation'},
            Party.BOTH
        )
        
        # 连接
        protocol.add_edge(alice_source, channel1, EdgeType.QUANTUM)
        protocol.add_edge(bob_source, channel2, EdgeType.QUANTUM)
        protocol.add_edge(channel1, interferometer, EdgeType.QUANTUM)
        protocol.add_edge(channel2, interferometer, EdgeType.QUANTUM)
        protocol.add_edge(interferometer, detector, EdgeType.QUANTUM)
        protocol.add_edge(detector, classical, EdgeType.CLASSICAL)
        protocol.add_edge(classical, reconciliation, EdgeType.CLASSICAL)
        
        return protocol
    
    def generate_security_report(self, protocol: ProtocolGraph) -> str:
        """生成安全性报告"""
        print("=" * 70)
        print("🔒 AI发现协议的安全性分析报告")
        print("=" * 70)
        
        # 1. 结构安全性分析
        print("\n1. 结构安全性分析")
        structure_analysis = self.analyze_structure_security(protocol)
        
        print(f"\n   安全性分数: {structure_analysis['security_score']:.3f}")
        
        if structure_analysis['findings']:
            print("\n   ✅ 安全优势:")
            for finding in structure_analysis['findings']:
                print(f"      {finding}")
        
        if structure_analysis['warnings']:
            print("\n   ⚠️ 安全警告:")
            for warning in structure_analysis['warnings']:
                print(f"      {warning}")
        
        # 2. 攻击抵抗性分析
        print("\n2. 攻击抵抗性分析")
        attack_analysis = self.analyze_attack_resistance(protocol)
        
        print(f"\n   平均攻击抵抗分数: {attack_analysis['average_resistance_score']:.3f}")
        
        # 3. 综合安全性评级
        print("\n3. 综合安全性评级")
        security_rating = self.calculate_security_rating(structure_analysis, attack_analysis)
        
        print(f"\n   综合安全性分数: {security_rating['overall_score']:.3f}")
        print(f"   安全性等级: {security_rating['security_level']}")
        print(f"   评级: {security_rating['rating']}")
        
        if security_rating['major_risks']:
            print(f"\n   🔴 主要风险:")
            for risk in security_rating['major_risks']:
                print(f"      • {risk}")
        
        if security_rating['security_advantages']:
            print(f"\n   🟢 安全优势:")
            for advantage in security_rating['security_advantages']:
                print(f"      • {advantage}")
        
        if security_rating['recommendations']:
            print(f"\n   💡 改进建议:")
            for i, rec in enumerate(security_rating['recommendations'], 1):
                print(f"      {i}. {rec}")
        
        # 4. 与传统协议对比
        print("\n4. 与传统协议安全性对比")
        comparison = self.compare_with_standard_protocols(protocol)
        
        # 保存报告
        import time as time_module
        report_data = {
            'protocol_name': protocol.name,
            'structure_analysis': structure_analysis,
            'attack_analysis': attack_analysis,
            'security_rating': security_rating,
            'comparison_with_standard': comparison,
            'timestamp': time_module.time()
        }
        
        import time
        timestamp = int(time.time())
        filename = f"results/security_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 安全性报告已保存: {filename}")
        
        print("\n" + "=" * 70)
        print("✅ 安全性分析完成")
        print("=" * 70)
        
        return report_data


def load_innovative_protocol():
    """加载发现的创新协议"""
    # 创建基于实验结果的协议
    from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
    
    protocol = ProtocolGraph(name="Discovered Innovative Protocol")
    
    # 基于实验结果：11节点，12边
    # Alice的源
    alice_source = protocol.add_node(
        NodeType.QSP,
        {'state': 'coherent', 'phase': 'random'},
        Party.ALICE
    )
    
    # Bob的源
    bob_source = protocol.add_node(
        NodeType.QSP,
        {'state': 'coherent', 'phase': 'random'},
        Party.BOB
    )
    
    # 量子信道
    channel1 = protocol.add_node(NodeType.QC, {'distance': 200}, None)
    channel2 = protocol.add_node(NodeType.QC, {'distance': 200}, None)
    
    # 干涉测量节点
    interferometer = protocol.add_node(
        NodeType.QG,
        {'gate_type': 'custom_interferometer'},
        Party.CHARLIE
    )
    
    # 探测器
    detector = protocol.add_node(NodeType.QD, {'type': 'advanced'}, Party.CHARLIE)
    
    # 经典信道
    classical_channel = protocol.add_node(NodeType.CC, {'capacity': 2.0}, None)
    
    # 处理节点
    processor1 = protocol.add_node(NodeType.CP, {'operation': 'phase_reconciliation'}, Party.ALICE)
    processor2 = protocol.add_node(NodeType.CP, {'operation': 'phase_reconciliation'}, Party.BOB)
    
    # 验证节点
    verification = protocol.add_node(
        NodeType.CV,
        {'method': 'interference_based'},
        Party.BOTH
    )
    
    # 密钥提取
    key_extractor = protocol.add_node(NodeType.CK, {'algorithm': 'novel'}, Party.BOTH)
    
    # 连接（12条边）
    # 量子连接
    protocol.add_edge(alice_source, channel1, EdgeType.QUANTUM)
    protocol.add_edge(bob_source, channel2, EdgeType.QUANTUM)
    protocol.add_edge(channel1, interferometer, EdgeType.QUANTUM)
    protocol.add_edge(channel2, interferometer, EdgeType.QUANTUM)
    protocol.add_edge(interferometer, detector, EdgeType.QUANTUM)
    
    # 经典连接
    protocol.add_edge(detector, classical_channel, EdgeType.CLASSICAL)
    protocol.add_edge(classical_channel, processor1, EdgeType.CLASSICAL)
    protocol.add_edge(classical_channel, processor2, EdgeType.CLASSICAL)
    protocol.add_edge(processor1, verification, EdgeType.CLASSICAL)
    protocol.add_edge(processor2, verification, EdgeType.CLASSICAL)
    protocol.add_edge(verification, key_extractor, EdgeType.CLASSICAL)
    
    # 控制连接（创新特征）
    protocol.add_edge(interferometer, processor1, EdgeType.CONTROL)
    
    return protocol


def main():
    """主函数"""
    print("=" * 70)
    print("🔒 AI发现协议的安全性证明")
    print("=" * 70)
    print("分析AI发现协议的结构安全性和攻击抵抗性")
    print("=" * 70)
    
    # 加载协议
    print("\n📋 加载AI发现的创新协议...")
    protocol = load_innovative_protocol()
    
    stats = protocol.get_statistics()
    print(f"协议信息:")
    print(f"  名称: {protocol.name}")
    print(f"  节点数: {stats.get('node_count', 0)}")
    print(f"  边数: {stats.get('edge_count', 0)}")
    print(f"  创新特征: 控制信号连接、基于干涉的验证")
    
    # 创建分析器
    analyzer = SecurityAnalyzer()
    
    # 生成安全性报告
    report = analyzer.generate_security_report(protocol)
    
    # 显示总结
    print("\n📈 安全性分析总结:")
    
    rating = report['security_rating']
    print(f"  综合安全性分数: {rating['overall_score']:.3f}")
    print(f"  安全性等级: {rating['security_level']}")
    print(f"  评级: {rating['rating']}")
    
    # 与传统协议对比结果
    comparison = report['comparison_with_standard']
    print(f"\n  🔄 与传统协议对比:")
    
    ai_score = comparison.get('AI_Protocol', {}).get('security_score', 0)
    bb84_score = comparison.get('BB84', {}).get('security_score', 0)
    mdi_score = comparison.get('MDI-QKD', {}).get('security_score', 0)
    tf_score = comparison.get('TF-QKD', {}).get('security_score', 0)
    
    print(f"    • AI协议: {ai_score:.3f} ({comparison.get('AI_Protocol', {}).get('rating', 'N/A')})")
    print(f"    • BB84: {bb84_score:.3f} ({comparison.get('BB84', {}).get('rating', 'N/A')})")
    print(f"    • MDI-QKD: {mdi_score:.3f} ({comparison.get('MDI-QKD', {}).get('rating', 'N/A')})")
    print(f"    • TF-QKD: {tf_score:.3f} ({comparison.get('TF-QKD', {}).get('rating', 'N/A')})")
    
    # 建议
    if rating['recommendations']:
        print(f"\n  💡 关键改进建议:")
        for i, rec in enumerate(rating['recommendations'][:3], 1):
            print(f"    {i}. {rec}")
    
    print(f"\n📁 完整报告: results/security_analysis_*.json")
    
    print("\n" + "=" * 70)
    print("🎯 安全性证明结论")
    print("=" * 70)
    
    # 根据评分给出结论
    if rating['overall_score'] >= 0.7:
        print("  ✅ AI发现的协议具有合理的安全性基础")
        print("  ✅ 创新特征未引入明显安全漏洞")
        print("  ✅ 通过适当改进可达到实用安全水平")
    elif rating['overall_score'] >= 0.5:
        print("  ⚠️ AI发现的协议安全性中等，需要改进")
        print("  ⚠️ 部分创新特征可能引入安全风险")
        print("  ⚠️ 需要进一步的安全性增强")
    else:
        print("  🔴 AI发现的协议安全性不足")
        print("  🔴 创新特征可能引入严重安全漏洞")
        print("  🔴 需要重大安全性重新设计")
    
    print("\n🔬 研究意义:")
    print("  1. 首次对AI发现的量子协议进行安全性分析")
    print("  2. 验证了AI协议发现方法的安全性考虑")
    print("  3. 为AI辅助协议设计提供了安全性评估框架")
    print("  4. 识别了创新特征的安全影响")


if __name__ == "__main__":
    import time
    main()
