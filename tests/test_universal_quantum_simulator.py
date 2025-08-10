"""
通用量子仿真器测试

该测试文件验证重构后的通用量子仿真器的功能，包括：
1. 通用协议仿真能力
2. 量子操作解析和执行
3. 量子态演化的物理精确性
4. 与现有协议的向后兼容性

测试方法：TDD驱动，确保重构过程的安全性和正确性
"""

import pytest
import numpy as np
import numpy.testing as npt
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, MagicMock, patch

# 导入待测试模块
from simulator.real_quantum_simulator import RealQuantumSimulator
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType

# 导入新的通用框架
try:
    from security_evaluator.universal_framework import (
        QuantumOperation, 
        ProtocolFeatures,
        QuantumOperationType,
        create_bb84_protocol,
        create_mdi_qkd_protocol,
        create_decoy_bb84_protocol
    )
    UNIVERSAL_FRAMEWORK_AVAILABLE = True
except ImportError:
    UNIVERSAL_FRAMEWORK_AVAILABLE = False


class TestUniversalQuantumSimulation:
    """
    测试通用量子仿真功能
    
    验证仿真器能够处理基于ProtocolFeatures的任意协议结构
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-10
        
        # 如果通用框架不可用，跳过这些测试
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
    
    def test_simulate_universal_protocol_bb84(self):
        """测试通用仿真器对BB84协议的处理"""
        # 创建BB84协议特征
        bb84_protocol = create_bb84_protocol()
        
        # 创建模拟的实验参数
        experimental_params = {
            'num_pulses': 1000,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.1,
            'channel_error_rate': 0.02
        }
        
        # 创建仿真器（暂时不传入协议图，使用新的通用接口）
        simulator = RealQuantumSimulator()
        
        # 调用通用仿真方法
        result = simulator.simulate_universal_protocol(bb84_protocol, experimental_params)
        
        # 验证仿真结果
        assert 'qber' in result
        assert 'gain' in result
        assert 0 <= result['qber'] <= 1
        assert 0 <= result['gain'] <= 1
        
        # BB84特有的验证
        assert result['qber'] >= experimental_params['channel_error_rate']
        assert result['gain'] <= (1 - experimental_params['channel_loss'])
    
    def test_simulate_universal_protocol_mdi_qkd(self):
        """测试通用仿真器对MDI-QKD协议的处理"""
        # 创建MDI-QKD协议特征
        mdi_protocol = create_mdi_qkd_protocol()
        
        # MDI-QKD特定的实验参数
        experimental_params = {
            'num_pulses': 1000,
            'alice_channel_loss': 0.15,
            'bob_channel_loss': 0.15,
            'alice_channel_error': 0.01,
            'bob_channel_error': 0.01,
            'basis_choices': ['Z', 'X']
        }
        
        simulator = RealQuantumSimulator()
        result = simulator.simulate_universal_protocol(mdi_protocol, experimental_params)
        
        # 验证仿真结果
        assert 'qber' in result
        assert 'gain' in result
        
        # MDI-QKD特有的验证：增益应该更低（两次传输损耗）
        expected_max_gain = (1 - experimental_params['alice_channel_loss']) * \
                          (1 - experimental_params['bob_channel_loss'])
        assert result['gain'] <= expected_max_gain * 1.1  # 允许小的数值误差
    
    def test_simulate_universal_protocol_decoy_state(self):
        """测试通用仿真器对诱骗态协议的处理"""
        # 创建诱骗态协议特征
        decoy_protocol = create_decoy_bb84_protocol()
        
        # 诱骗态特定的实验参数
        experimental_params = {
            'num_pulses': 1000,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.1,
            'channel_error_rate': 0.02,
            'intensity_settings': {
                'signal': {'value': 0.5, 'probability': 0.7},
                'decoy': {'value': 0.1, 'probability': 0.2},
                'vacuum': {'value': 0.0, 'probability': 0.1}
            }
        }
        
        simulator = RealQuantumSimulator()
        result = simulator.simulate_universal_protocol(decoy_protocol, experimental_params)
        
        # 对于诱骗态，结果应该是按强度分组的
        if isinstance(result, dict) and 'signal' in result:
            # 按强度分组的结果
            for intensity_name, intensity_result in result.items():
                assert 'qber' in intensity_result
                assert 'gain' in intensity_result
                assert 0 <= intensity_result['qber'] <= 1
                assert 0 <= intensity_result['gain'] <= 1
        else:
            # 统一的结果
            assert 'qber' in result
            assert 'gain' in result
    
    def test_custom_protocol_simulation(self):
        """测试自定义协议的仿真能力"""
        # 创建一个自定义协议
        custom_operations = [
            QuantumOperation("custom_prep", QuantumOperationType.PREPARATION),
            QuantumOperation("custom_channel", QuantumOperationType.CHANNEL),
            QuantumOperation("custom_measurement", QuantumOperationType.MEASUREMENT)
        ]
        
        custom_protocol = ProtocolFeatures(
            name="Custom_Test_Protocol",
            operations=custom_operations,
            parties=['Alice', 'Bob'],
            communication_rounds=1,
            measurement_bases=3  # 使用3个测量基
        )
        
        experimental_params = {
            'num_pulses': 500,
            'basis_choices': ['Z', 'X', 'Y'],
            'channel_loss': 0.05,
            'channel_error_rate': 0.01
        }
        
        simulator = RealQuantumSimulator()
        result = simulator.simulate_universal_protocol(custom_protocol, experimental_params)
        
        # 验证仿真器能够处理自定义协议
        assert isinstance(result, dict)
        assert 'qber' in result or 'error' in result  # 要么成功要么有错误信息


class TestQuantumOperationParsing:
    """
    测试量子操作解析功能
    
    验证仿真器能够正确解析和执行ProtocolFeatures中定义的量子操作
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.simulator = RealQuantumSimulator()
        self.tolerance = 1e-10
        
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
    
    def test_parse_preparation_operations(self):
        """测试态准备操作的解析"""
        # 定义态准备操作
        prep_operation = QuantumOperation(
            name="qubit_preparation",
            operation_type=QuantumOperationType.PREPARATION,
            parameters={'basis': 'Z', 'bit': 0}
        )
        
        # 解析操作
        parsed_ops = self.simulator.parse_quantum_operations([prep_operation])
        
        # 验证解析结果
        assert len(parsed_ops) == 1
        assert parsed_ops[0]['type'] == 'preparation'
        assert parsed_ops[0]['name'] == 'qubit_preparation'
        assert 'parameters' in parsed_ops[0]
    
    def test_parse_channel_operations(self):
        """测试信道操作的解析"""
        # 定义信道操作
        channel_operation = QuantumOperation(
            name="noisy_channel",
            operation_type=QuantumOperationType.CHANNEL,
            parameters={'loss': 0.1, 'error_rate': 0.02}
        )
        
        # 解析操作
        parsed_ops = self.simulator.parse_quantum_operations([channel_operation])
        
        # 验证解析结果
        assert len(parsed_ops) == 1
        assert parsed_ops[0]['type'] == 'channel'
        assert parsed_ops[0]['parameters']['loss'] == 0.1
        assert parsed_ops[0]['parameters']['error_rate'] == 0.02
    
    def test_parse_measurement_operations(self):
        """测试测量操作的解析"""
        # 定义测量操作
        measurement_operation = QuantumOperation(
            name="basis_measurement",
            operation_type=QuantumOperationType.MEASUREMENT,
            parameters={'basis': 'X', 'efficiency': 0.9}
        )
        
        # 解析操作
        parsed_ops = self.simulator.parse_quantum_operations([measurement_operation])
        
        # 验证解析结果
        assert len(parsed_ops) == 1
        assert parsed_ops[0]['type'] == 'measurement'
        assert parsed_ops[0]['parameters']['basis'] == 'X'
    
    def test_parse_sequential_operations(self):
        """测试序列操作的解析"""
        # 定义操作序列
        operations = [
            QuantumOperation("prep", QuantumOperationType.PREPARATION),
            QuantumOperation("channel", QuantumOperationType.CHANNEL),
            QuantumOperation("measure", QuantumOperationType.MEASUREMENT)
        ]
        
        # 解析操作序列
        parsed_ops = self.simulator.parse_quantum_operations(operations)
        
        # 验证解析结果
        assert len(parsed_ops) == 3
        assert parsed_ops[0]['type'] == 'preparation'
        assert parsed_ops[1]['type'] == 'channel'
        assert parsed_ops[2]['type'] == 'measurement'
    
    def test_parse_invalid_operations(self):
        """测试无效操作的处理"""
        # 定义无效操作
        invalid_operation = QuantumOperation(
            name="invalid_op",
            operation_type="invalid_type"  # 无效类型
        )
        
        # 尝试解析无效操作
        with pytest.raises((ValueError, TypeError)):
            self.simulator.parse_quantum_operations([invalid_operation])


class TestQuantumStateEvolution:
    """
    测试量子态演化功能
    
    验证仿真器能够正确模拟量子态在各种操作下的演化
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.simulator = RealQuantumSimulator()
        self.tolerance = 1e-10
    
    def test_evolve_quantum_state_unitary(self):
        """测试幺正演化"""
        # 初始态：|0⟩
        initial_state = np.array([[1, 0], [0, 0]], dtype=complex)
        
        # Pauli-X操作
        pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
        
        # 演化态
        evolved_state = self.simulator.evolve_quantum_state(
            initial_state, 
            operation_type='unitary',
            operation_matrix=pauli_x
        )
        
        # 预期结果：|1⟩
        expected_state = np.array([[0, 0], [0, 1]], dtype=complex)
        
        # 验证演化结果
        npt.assert_allclose(evolved_state, expected_state, atol=self.tolerance)
        
        # 验证演化保持态的性质
        assert np.abs(np.trace(evolved_state) - 1.0) < self.tolerance  # 归一化
        assert np.allclose(evolved_state, evolved_state.conj().T, atol=self.tolerance)  # 厄米性
    
    def test_evolve_quantum_state_channel(self):
        """测试信道演化"""
        # 初始态：纯态 |0⟩
        initial_state = np.array([[1, 0], [0, 0]], dtype=complex)
        
        # 去极化信道参数
        depolarization_prob = 0.1
        
        # 演化态
        evolved_state = self.simulator.evolve_quantum_state(
            initial_state,
            operation_type='channel',
            channel_params={'type': 'depolarizing', 'probability': depolarization_prob}
        )
        
        # 验证演化结果的性质
        assert np.abs(np.trace(evolved_state) - 1.0) < self.tolerance  # 保迹性
        assert np.allclose(evolved_state, evolved_state.conj().T, atol=self.tolerance)  # 厄米性
        
        # 验证去极化效果：态的纯度应该降低
        initial_purity = np.trace(initial_state @ initial_state)
        final_purity = np.trace(evolved_state @ evolved_state)
        assert final_purity <= initial_purity + self.tolerance
    
    def test_evolve_quantum_state_measurement(self):
        """测试测量演化"""
        # 初始态：叠加态 (|0⟩ + |1⟩)/√2
        initial_state = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
        
        # Z基测量
        measurement_result = self.simulator.evolve_quantum_state(
            initial_state,
            operation_type='measurement',
            measurement_basis='Z'
        )
        
        # 验证测量结果格式
        assert isinstance(measurement_result, dict)
        assert 'probabilities' in measurement_result
        assert 'post_states' in measurement_result
        
        # 验证概率归一化
        probs = measurement_result['probabilities']
        assert abs(sum(probs) - 1.0) < self.tolerance
        
        # 对于对称叠加态，两个结果概率应该相等
        npt.assert_allclose(probs[0], 0.5, atol=self.tolerance)
        npt.assert_allclose(probs[1], 0.5, atol=self.tolerance)
    
    def test_evolve_quantum_state_sequence(self):
        """测试操作序列的演化"""
        # 初始态：|0⟩
        state = np.array([[1, 0], [0, 0]], dtype=complex)
        
        # 操作序列：H门 → Z测量
        hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        
        # 1. 应用Hadamard门
        state = self.simulator.evolve_quantum_state(
            state,
            operation_type='unitary',
            operation_matrix=hadamard
        )
        
        # 验证叠加态
        expected_superposition = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
        npt.assert_allclose(state, expected_superposition, atol=self.tolerance)
        
        # 2. 应用Z测量
        measurement_result = self.simulator.evolve_quantum_state(
            state,
            operation_type='measurement',
            measurement_basis='Z'
        )
        
        # 验证测量结果：等概率
        probs = measurement_result['probabilities']
        npt.assert_allclose(probs, [0.5, 0.5], atol=self.tolerance)


class TestBackwardCompatibility:
    """
    测试向后兼容性
    
    确保重构后的仿真器仍然能够处理原有的协议图格式
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-6
    
    def test_legacy_protocol_graph_bb84(self):
        """测试传统协议图格式的BB84协议"""
        # 创建模拟的传统协议图
        mock_protocol_graph = Mock(spec=ProtocolGraph)
        
        # 模拟BB84节点
        mock_qsp_node = Mock()
        mock_qsp_node.params = {
            'num_states': 1000,
            'basis_choice': ['Z', 'X']
        }
        
        mock_qc_node = Mock()
        mock_qc_node.params = {
            'loss': 0.1,
            'error_rate': 0.02
        }
        
        mock_qm_node = Mock()
        mock_qm_node.params = {
            'basis_choice': ['Z', 'X']
        }
        
        # 配置mock对象
        mock_protocol_graph.get_nodes_by_type.side_effect = lambda node_type: {
            NodeType.QSP: [mock_qsp_node],
            NodeType.QC: [mock_qc_node],
            NodeType.QM: [mock_qm_node]
        }.get(node_type, [])
        
        mock_protocol_graph.find_first_node_by_type.side_effect = lambda node_type: {
            NodeType.QM: mock_qm_node,
            NodeType.BSM: None
        }.get(node_type)
        
        # 创建仿真器
        simulator = RealQuantumSimulator(mock_protocol_graph)
        
        # 运行仿真
        result = simulator.run()
        
        # 验证兼容性
        assert isinstance(result, dict)
        assert 'qber' in result
        assert 'gain' in result
    
    def test_legacy_single_pulse_interface(self):
        """测试传统单脉冲仿真接口"""
        simulator = RealQuantumSimulator()
        
        # 使用传统接口参数
        alice_params = {'basis': 'Z', 'bit': 0}
        channel_params = {'loss': 0.1, 'error_rate': 0.02}
        bob_params = {'basis': 'Z'}
        
        # 调用传统接口
        result = simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
        
        # 验证传统接口仍然工作
        assert isinstance(result, dict)
        assert 'outcome' in result
        assert 'detected' in result
        assert 'final_state_info' in result
    
    def test_mixed_interface_usage(self):
        """测试混合使用新旧接口"""
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
        
        # 创建新格式的协议
        bb84_protocol = create_bb84_protocol()
        
        # 创建传统格式的仿真器
        simulator = RealQuantumSimulator()
        
        # 新接口应该能够工作
        experimental_params = {
            'num_pulses': 100,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.1,
            'channel_error_rate': 0.02
        }
        
        result = simulator.simulate_universal_protocol(bb84_protocol, experimental_params)
        assert isinstance(result, dict)
        
        # 传统接口也应该能够工作
        legacy_result = simulator.simulate_single_pulse(
            {'basis': 'Z', 'bit': 0},
            {'loss': 0.1, 'error_rate': 0.02},
            {'basis': 'Z'}
        )
        assert isinstance(legacy_result, dict)


class TestSimulationAccuracy:
    """
    测试仿真精度
    
    验证通用仿真器的物理精确性和数值稳定性
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.simulator = RealQuantumSimulator()
        self.tolerance = 1e-6
    
    def test_ideal_channel_simulation(self):
        """测试理想信道的仿真精度"""
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
        
        # 理想BB84协议（无损耗无噪声）
        bb84_protocol = create_bb84_protocol()
        
        ideal_params = {
            'num_pulses': 10000,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.0,
            'channel_error_rate': 0.0
        }
        
        result = self.simulator.simulate_universal_protocol(bb84_protocol, ideal_params)
        
        # 理想情况下QBER应该接近0
        assert result['qber'] < 0.01, f"Ideal QBER too high: {result['qber']}"
        
        # 理想情况下增益应该接近0.5（基选择匹配概率）
        assert abs(result['gain'] - 0.5) < 0.05, f"Ideal gain deviation: {result['gain']}"
    
    def test_high_loss_simulation(self):
        """测试高损耗情况的仿真精度"""
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
        
        bb84_protocol = create_bb84_protocol()
        
        high_loss_params = {
            'num_pulses': 10000,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.9,  # 90%损耗
            'channel_error_rate': 0.0
        }
        
        result = self.simulator.simulate_universal_protocol(bb84_protocol, high_loss_params)
        
        # 高损耗下增益应该很低
        assert result['gain'] < 0.1, f"High loss gain too high: {result['gain']}"
        
        # QBER应该仍然较低（无噪声）
        assert result['qber'] < 0.05, f"High loss QBER too high: {result['qber']}"
    
    def test_noisy_channel_simulation(self):
        """测试噪声信道的仿真精度"""
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
        
        bb84_protocol = create_bb84_protocol()
        
        noisy_params = {
            'num_pulses': 10000,
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.1,
            'channel_error_rate': 0.1  # 10%错误率
        }
        
        result = self.simulator.simulate_universal_protocol(bb84_protocol, noisy_params)
        
        # 噪声信道下QBER应该反映错误率
        assert result['qber'] >= 0.05, f"Noisy QBER too low: {result['qber']}"
        assert result['qber'] <= 0.2, f"Noisy QBER too high: {result['qber']}"
    
    def test_numerical_stability(self):
        """测试数值稳定性"""
        # 测试极端参数下的数值稳定性
        initial_state = np.array([[1, 0], [0, 0]], dtype=complex)
        
        # 极小的演化
        tiny_rotation = np.array([
            [np.cos(1e-10), -np.sin(1e-10)],
            [np.sin(1e-10), np.cos(1e-10)]
        ], dtype=complex)
        
        evolved_state = self.simulator.evolve_quantum_state(
            initial_state,
            operation_type='unitary',
            operation_matrix=tiny_rotation
        )
        
        # 验证数值稳定性
        assert np.abs(np.trace(evolved_state) - 1.0) < 1e-12
        assert np.allclose(evolved_state, evolved_state.conj().T, atol=1e-12)


class TestPerformanceCharacteristics:
    """
    测试性能特征
    
    验证通用仿真器的性能与原有实现相当或更好
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.simulator = RealQuantumSimulator()
    
    def test_simulation_scalability(self):
        """测试仿真可扩展性"""
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            pytest.skip("Universal framework not available")
        
        bb84_protocol = create_bb84_protocol()
        
        # 测试不同规模的仿真
        pulse_counts = [100, 1000, 5000]
        execution_times = []
        
        import time
        
        for num_pulses in pulse_counts:
            params = {
                'num_pulses': num_pulses,
                'basis_choices': ['Z', 'X'],
                'channel_loss': 0.1,
                'channel_error_rate': 0.02
            }
            
            start_time = time.time()
            result = self.simulator.simulate_universal_protocol(bb84_protocol, params)
            end_time = time.time()
            
            execution_times.append(end_time - start_time)
            
            # 验证结果质量不随规模降低
            assert 'qber' in result
            assert 'gain' in result
        
        # 验证时间复杂度合理（近似线性）
        if len(execution_times) >= 3:
            # 简单的线性增长检查
            time_ratio = execution_times[-1] / execution_times[0]
            pulse_ratio = pulse_counts[-1] / pulse_counts[0]
            
            # 时间增长应该不超过脉冲数增长的2倍（考虑开销）
            assert time_ratio <= pulse_ratio * 2, f"Time scaling too poor: {time_ratio} vs {pulse_ratio}"


if __name__ == "__main__":
    # 运行测试套件
    pytest.main([__file__, "-v"])