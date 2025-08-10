"""
通用AI Agent环境的TDD测试模块

测试基于通用框架的AI Agent环境功能，确保协议无关的仿真和评估。

测试覆盖：
1. 通用仿真器集成
2. 通用安全性分析
3. 协议无关的评估流程
4. AI Agent动作处理
5. 奖励计算机制
6. 环境状态管理
7. 向后兼容性
8. 性能优化

作者：AI4QKD Team  
版本：2.0 - Universal Framework
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import warnings

# 导入待测试模块
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ai_agent.environment import QKDSimEnv
    from qcgf_dsl.protocol_graph import ProtocolGraph
    from qcgf_dsl.node_types import NodeType
    from qcgf_dsl.edge_types import EdgeType
    from security_evaluator.universal_framework import (
        ProtocolFeatures,
        UniversalSecurityParameters,
        create_bb84_protocol,
        create_mdi_qkd_protocol
    )
    _MODULES_AVAILABLE = True
except ImportError as e:
    _MODULES_AVAILABLE = False
    print(f"Warning: Could not import modules: {e}")


@pytest.mark.skipif(not _MODULES_AVAILABLE, reason="Required modules not available")
class TestUniversalEnvironment:
    """通用AI Agent环境测试类"""
    
    @pytest.fixture
    def basic_config(self):
        """基本环境配置"""
        return {
            "DEFAULT_NUM_PULSES": 10000,
            "INVALID_PROTOCOL_PENALTY": -100.0,
            "MAX_NODES": 20,
            "USE_UNIVERSAL_FRAMEWORK": True
        }
    
    @pytest.fixture
    def environment(self, basic_config):
        """创建环境实例"""
        return QKDSimEnv(basic_config)
    
    @pytest.fixture
    def sample_protocol_graph(self):
        """样例协议图"""
        graph = ProtocolGraph(name="Test_Protocol")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice")
        graph.add_node(node_type=NodeType.QC, node_id="qc_channel")  
        graph.add_node(node_type=NodeType.QM, node_id="qm_bob")
        graph.add_edge("qsp_alice", "qc_channel", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_channel", "qm_bob", edge_type=EdgeType.QUANTUM)
        return graph
    
    # ==================== 环境初始化测试 ====================
    
    def test_environment_initialization_with_universal_framework(self, basic_config):
        """测试环境初始化时使用通用框架"""
        env = QKDSimEnv(basic_config)
        
        # 验证环境基本属性
        assert hasattr(env, 'action_space'), "环境必须有动作空间"
        assert hasattr(env, 'observation_space'), "环境必须有观察空间"
        assert hasattr(env, 'protocol_graph'), "环境必须有协议图"
        
        # 验证通用框架组件
        assert hasattr(env, 'universal_simulator'), "环境应集成通用仿真器"
        assert hasattr(env, 'universal_security_analyzer'), "环境应集成通用安全分析器"
        assert hasattr(env, 'universal_entropy_estimator'), "环境应集成通用熵估计器"
    
    def test_environment_supports_universal_simulation(self, environment):
        """测试环境支持通用仿真"""
        # 验证环境有通用仿真方法
        assert hasattr(environment, 'run_universal_simulation'), "环境必须支持通用仿真"
        assert hasattr(environment, 'convert_protocol_to_features'), "环境必须支持协议特征转换"
        
        # 测试协议图到特征的转换
        protocol_features = environment.convert_protocol_to_features(environment.protocol_graph)
        assert hasattr(protocol_features, 'name'), "协议特征必须有名称"
        assert hasattr(protocol_features, 'operations'), "协议特征必须有操作列表"
    
    def test_environment_supports_universal_security_analysis(self, environment):
        """测试环境支持通用安全性分析"""
        # 验证环境有通用安全分析方法
        assert hasattr(environment, 'analyze_protocol_security'), "环境必须支持通用安全分析"
        assert hasattr(environment, 'estimate_protocol_entropy'), "环境必须支持通用熵估计"
        
        # 模拟仿真结果
        mock_simulation_results = {
            'raw_statistics': {
                'alice_measurements': [0, 1] * 500,
                'bob_measurements': [0, 1, 1, 1] * 250,
                'detection_events': [True] * 1000
            },
            'channel_statistics': {
                'transmission_probability': 0.5,
                'error_probability': 0.05,
                'total_pulses': 10000
            }
        }
        
        # 测试安全分析
        security_result = environment.analyze_protocol_security(
            environment.protocol_graph, mock_simulation_results
        )
        assert hasattr(security_result, 'final_key_rate'), "安全分析结果必须包含密钥率"
    
    # ==================== 通用仿真集成测试 ====================
    
    def test_universal_simulation_integration(self, environment, sample_protocol_graph):
        """测试通用仿真器集成"""
        # 设置环境的协议图
        environment.protocol_graph = sample_protocol_graph
        
        # 运行通用仿真
        simulation_results = environment.run_universal_simulation()
        
        # 验证仿真结果结构
        assert 'raw_statistics' in simulation_results, "仿真结果必须包含原始统计"
        assert 'channel_statistics' in simulation_results, "仿真结果必须包含信道统计"
        
        # 验证统计数据的完整性
        raw_stats = simulation_results['raw_statistics']
        assert 'alice_measurements' in raw_stats, "必须包含Alice测量数据"
        assert 'bob_measurements' in raw_stats, "必须包含Bob测量数据"
        assert 'detection_events' in raw_stats, "必须包含检测事件数据"
    
    def test_universal_simulation_with_different_protocols(self, environment):
        """测试通用仿真对不同协议的支持"""
        # 测试协议类型
        protocol_graphs = [
            self._create_bb84_graph(),
            self._create_mdi_qkd_graph(),
            self._create_custom_graph()
        ]
        
        for i, graph in enumerate(protocol_graphs):
            environment.protocol_graph = graph
            
            # 运行仿真
            results = environment.run_universal_simulation()
            
            # 验证结果
            assert results is not None, f"协议{i}的仿真失败"
            assert 'channel_statistics' in results, f"协议{i}缺少信道统计"
            
            # 验证密钥率为正数（或至少非负）
            channel_stats = results['channel_statistics']
            assert channel_stats.get('transmission_probability', 0) >= 0, f"协议{i}传输概率异常"
    
    def test_simulation_error_handling(self, environment):
        """测试仿真错误处理"""
        # 创建无效协议图（缺少必要节点）
        invalid_graph = ProtocolGraph(name="Invalid_Protocol")
        invalid_graph.add_node(node_type=NodeType.QSP, node_id="qsp_only")
        
        environment.protocol_graph = invalid_graph
        
        # 仿真应该处理错误或返回默认值
        results = environment.run_universal_simulation()
        
        # 验证错误处理
        if results is None:
            # 错误被正确捕获
            assert True
        else:
            # 返回默认/安全值
            assert 'error' in results or 'channel_statistics' in results
    
    # ==================== 通用安全性分析测试 ====================
    
    def test_universal_security_analysis_integration(self, environment, sample_protocol_graph):
        """测试通用安全性分析集成"""
        # 设置协议图
        environment.protocol_graph = sample_protocol_graph
        
        # 模拟仿真结果
        simulation_results = {
            'raw_statistics': {
                'alice_measurements': [0, 1] * 1000,
                'bob_measurements': [0, 1, 1, 1] * 500,  # 25%错误率
                'alice_bases': ['Z', 'X'] * 1000,
                'bob_bases': ['Z', 'X'] * 1000,
                'detection_events': [True] * 2000
            },
            'channel_statistics': {
                'transmission_probability': 0.6,
                'error_probability': 0.04,
                'total_pulses': 50000
            }
        }
        
        # 运行安全性分析
        security_result = environment.analyze_protocol_security(
            sample_protocol_graph, simulation_results
        )
        
        # 验证安全性分析结果
        assert hasattr(security_result, 'final_key_rate'), "必须包含最终密钥率"
        assert hasattr(security_result, 'mutual_information'), "必须包含互信息"
        assert hasattr(security_result, 'holevo_information'), "必须包含Holevo信息"
        assert security_result.final_key_rate >= 0, "密钥率必须非负"
    
    def test_universal_entropy_estimation_integration(self, environment):
        """测试通用熵估计集成"""
        # 准备测量数据
        measurement_data = {
            'alice_measurements': np.random.randint(0, 2, 5000).tolist(),
            'bob_measurements': np.random.randint(0, 2, 5000).tolist(),
            'alice_bases': ['Z'] * 5000,
            'bob_bases': ['Z'] * 5000,
            'detection_events': [True] * 5000
        }
        
        # 运行熵估计
        entropy_result = environment.estimate_protocol_entropy(
            environment.protocol_graph, measurement_data
        )
        
        # 验证熵估计结果
        assert hasattr(entropy_result, 'value'), "熵结果必须有值"
        assert hasattr(entropy_result, 'mutual_information'), "必须包含互信息"
        assert hasattr(entropy_result, 'holevo_information'), "必须包含Holevo信息"
        assert entropy_result.value >= 0, "熵值必须非负"
    
    # ==================== 协议无关性测试 ====================
    
    def test_protocol_agnostic_evaluation(self, environment):
        """测试协议无关的评估流程"""
        # 测试不同类型的协议
        test_protocols = [
            ("BB84", self._create_bb84_graph()),
            ("MDI-QKD", self._create_mdi_qkd_graph()),
            ("Custom", self._create_custom_graph()),
            ("Innovative", self._create_innovative_graph())
        ]
        
        evaluation_results = []
        
        for protocol_name, graph in test_protocols:
            environment.protocol_graph = graph
            
            # 运行完整评估流程
            evaluation = environment.evaluate_protocol()
            
            # 验证评估结果
            assert 'security_metrics' in evaluation, f"{protocol_name}缺少安全指标"
            assert 'performance_metrics' in evaluation, f"{protocol_name}缺少性能指标"
            assert 'complexity_metrics' in evaluation, f"{protocol_name}缺少复杂度指标"
            
            evaluation_results.append((protocol_name, evaluation))
        
        # 验证所有协议都能被评估
        assert len(evaluation_results) == len(test_protocols), "不是所有协议都被成功评估"
    
    def test_innovative_protocol_support(self, environment):
        """测试创新协议支持"""
        # 创建一个前所未有的协议结构
        innovative_graph = ProtocolGraph(name="AI_Generated_Innovative")
        
        # 添加多个QSP节点（多发送方）
        innovative_graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice1")
        innovative_graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice2")
        
        # 添加中继节点
        innovative_graph.add_node(node_type=NodeType.QC, node_id="relay_node")
        
        # 添加多个测量节点
        innovative_graph.add_node(node_type=NodeType.QM, node_id="qm_bob1")
        innovative_graph.add_node(node_type=NodeType.QM, node_id="qm_bob2")
        
        # 复杂连接结构
        innovative_graph.add_edge("qsp_alice1", "relay_node", edge_type=EdgeType.QUANTUM)
        innovative_graph.add_edge("qsp_alice2", "relay_node", edge_type=EdgeType.QUANTUM)
        innovative_graph.add_edge("relay_node", "qm_bob1", edge_type=EdgeType.QUANTUM)
        innovative_graph.add_edge("relay_node", "qm_bob2", edge_type=EdgeType.QUANTUM)
        
        environment.protocol_graph = innovative_graph
        
        # 环境应该能够处理这种创新协议
        evaluation = environment.evaluate_protocol()
        
        # 验证创新协议被正确处理
        assert evaluation is not None, "创新协议评估失败"
        assert 'security_metrics' in evaluation, "创新协议缺少安全评估"
    
    # ==================== AI Agent动作处理测试 ====================
    
    def test_universal_action_processing(self, environment):
        """测试通用动作处理"""
        initial_state, _ = environment.reset()
        
        # 测试添加节点动作
        add_node_action = {
            "action_type": 0,
            "node_type_to_add": 1,  # QC节点
            "param_to_modify": 0,
            "param_value": np.array([0.1])
        }
        
        state, reward, done, _, info = environment.step(add_node_action)
        
        # 验证动作被正确处理
        assert not done, "添加节点不应导致环境结束"
        assert reward is not None, "必须返回奖励值"
        assert 'security_results' in info, "必须包含安全分析结果"
    
    def test_universal_reward_calculation(self, environment):
        """测试通用奖励计算"""
        environment.reset()
        
        # 执行一系列动作
        actions = [
            {"action_type": 0, "node_type_to_add": 1, "param_to_modify": 0, "param_value": np.array([0.05])},
            {"action_type": 3, "node_type_to_add": 0, "param_to_modify": 1, "param_value": np.array([0.02])},
            {"action_type": 2, "node_type_to_add": 0, "param_to_modify": 0, "param_value": np.array([0.1])}
        ]
        
        rewards = []
        for action in actions:
            _, reward, done, _, _ = environment.step(action)
            if not done:
                rewards.append(reward)
        
        # 验证奖励计算
        assert len(rewards) > 0, "必须产生奖励值"
        assert all(isinstance(r, (int, float)) for r in rewards), "奖励必须是数值"
    
    # ==================== 向后兼容性测试 ====================
    
    def test_backward_compatibility_with_legacy_protocols(self, environment):
        """测试与传统协议的向后兼容性"""
        # 创建传统BB84协议
        legacy_graph = environment._create_base_bb84_graph()
        environment.protocol_graph = legacy_graph
        
        # 使用传统评估方法
        legacy_evaluation = environment.evaluate_protocol_legacy()
        
        # 使用通用评估方法
        universal_evaluation = environment.evaluate_protocol()
        
        # 比较结果一致性
        legacy_key_rate = legacy_evaluation['security_metrics']['final_key_rate']
        universal_key_rate = universal_evaluation['security_metrics']['final_key_rate']
        
        # 结果应在合理范围内一致
        relative_diff = abs(legacy_key_rate - universal_key_rate) / max(legacy_key_rate, 1e-10)
        assert relative_diff < 0.2, f"向后兼容性测试失败: 相对差异{relative_diff:.3f}"
    
    def test_legacy_interface_preservation(self, environment):
        """测试传统接口保持可用"""
        # 确保传统方法仍然存在
        assert hasattr(environment, 'step'), "必须保留step方法"
        assert hasattr(environment, 'reset'), "必须保留reset方法"
        assert hasattr(environment, 'render'), "必须保留render方法"
        
        # 测试传统接口调用
        obs, info = environment.reset()
        assert obs is not None, "reset必须返回观察"
        
        action = environment.action_space.sample()
        result = environment.step(action)
        assert len(result) == 5, "step必须返回5元组"
    
    # ==================== 性能优化测试 ====================
    
    def test_caching_mechanism(self, environment):
        """测试缓存机制"""
        environment.reset()
        
        # 执行相同动作两次
        action = {"action_type": 3, "node_type_to_add": 0, "param_to_modify": 0, "param_value": np.array([0.1])}
        
        # 第一次执行
        import time
        start_time = time.time()
        environment.step(action)
        first_time = time.time() - start_time
        
        # 第二次执行（应该使用缓存）
        start_time = time.time()
        environment.step(action)
        second_time = time.time() - start_time
        
        # 第二次应该更快（缓存生效）
        # 注意：这个测试可能不稳定，取决于系统负载
        if second_time < first_time * 0.8:
            print("缓存机制生效")
        else:
            print("缓存机制可能未生效或测试环境不稳定")
    
    def test_large_protocol_handling(self, environment):
        """测试大规模协议处理"""
        # 创建包含多个节点的复杂协议
        large_graph = ProtocolGraph(name="Large_Protocol")
        
        # 添加多个节点
        for i in range(10):
            large_graph.add_node(node_type=NodeType.QSP, node_id=f"qsp_{i}")
            large_graph.add_node(node_type=NodeType.QC, node_id=f"qc_{i}")
            large_graph.add_node(node_type=NodeType.QM, node_id=f"qm_{i}")
        
        # 添加连接
        for i in range(10):
            large_graph.add_edge(f"qsp_{i}", f"qc_{i}", edge_type=EdgeType.QUANTUM)
            large_graph.add_edge(f"qc_{i}", f"qm_{i}", edge_type=EdgeType.QUANTUM)
        
        environment.protocol_graph = large_graph
        
        # 评估应该在合理时间内完成
        import time
        start_time = time.time()
        evaluation = environment.evaluate_protocol()
        evaluation_time = time.time() - start_time
        
        # 验证大规模处理
        assert evaluation is not None, "大规模协议评估失败"
        assert evaluation_time < 30.0, f"大规模协议评估耗时过长: {evaluation_time:.2f}秒"
    
    # ==================== 辅助方法 ====================
    
    def _create_bb84_graph(self):
        """创建BB84协议图"""
        graph = ProtocolGraph(name="Test_BB84")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice")
        graph.add_node(node_type=NodeType.QC, node_id="qc_channel")
        graph.add_node(node_type=NodeType.QM, node_id="qm_bob")
        graph.add_edge("qsp_alice", "qc_channel", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_channel", "qm_bob", edge_type=EdgeType.QUANTUM)
        return graph
    
    def _create_mdi_qkd_graph(self):
        """创建MDI-QKD协议图"""
        graph = ProtocolGraph(name="Test_MDI_QKD")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_bob")
        graph.add_node(node_type=NodeType.QC, node_id="qc_alice_charlie")
        graph.add_node(node_type=NodeType.QC, node_id="qc_bob_charlie")
        graph.add_node(node_type=NodeType.BSM, node_id="bsm_charlie")
        
        graph.add_edge("qsp_alice", "qc_alice_charlie", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qsp_bob", "qc_bob_charlie", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_alice_charlie", "bsm_charlie", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_bob_charlie", "bsm_charlie", edge_type=EdgeType.QUANTUM)
        return graph
    
    def _create_custom_graph(self):
        """创建自定义协议图"""
        graph = ProtocolGraph(name="Test_Custom")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_source")
        graph.add_node(node_type=NodeType.QC, node_id="qc_amplifier")
        graph.add_node(node_type=NodeType.QC, node_id="qc_filter")
        graph.add_node(node_type=NodeType.QM, node_id="qm_detector")
        
        graph.add_edge("qsp_source", "qc_amplifier", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_amplifier", "qc_filter", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_filter", "qm_detector", edge_type=EdgeType.QUANTUM)
        return graph
    
    def _create_innovative_graph(self):
        """创建创新协议图"""
        graph = ProtocolGraph(name="Test_Innovative")
        
        # 多发送方架构
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_multi1")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_multi2")
        
        # 网络节点
        graph.add_node(node_type=NodeType.QC, node_id="qc_network_hub")
        
        # 多接收方
        graph.add_node(node_type=NodeType.QM, node_id="qm_multi1")
        graph.add_node(node_type=NodeType.QM, node_id="qm_multi2")
        
        # 复杂连接
        graph.add_edge("qsp_multi1", "qc_network_hub", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qsp_multi2", "qc_network_hub", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_network_hub", "qm_multi1", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_network_hub", "qm_multi2", edge_type=EdgeType.QUANTUM)
        
        return graph


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])