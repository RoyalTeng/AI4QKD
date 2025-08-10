"""
测试通用抽象密码学框架

该测试文件验证重构后的 ac_framework.py (或 universal_framework.py) 的新通用功能
基于量子信息论的通用框架，支持任意协议类型的安全性分析。

测试内容：
1. QuantumOperation 类的基本功能
2. ProtocolFeatures 类的信息论特征计算
3. UniversalSecurityFramework 类的通用安全性分析
4. 重构后 SecurityParameters 的通用性
5. 向后兼容性验证
"""

import pytest
import numpy as np
import numpy.testing as npt
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 当前测试使用原有的导入（重构后会更新）
try:
    from security_evaluator.ac_framework import SecurityParameters, ProtocolType
    ORIGINAL_FRAMEWORK = True
except ImportError:
    ORIGINAL_FRAMEWORK = False

# 重构后的导入（目标导入，目前可能不存在）
try:
    from security_evaluator.universal_framework import (
        QuantumOperation, 
        ProtocolFeatures, 
        UniversalSecurityFramework,
        UniversalSecurityParameters
    )
    NEW_FRAMEWORK = True
except ImportError:
    NEW_FRAMEWORK = False


class TestQuantumOperation:
    """
    测试 QuantumOperation 类
    
    验证通用量子操作的数学性质和信息论特征
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-10
        
        # 如果新框架还未实现，跳过这些测试
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
    
    def test_unitary_operation_creation(self):
        """测试幺正操作的创建和验证"""
        # 定义 Pauli-X 门
        pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
        
        # 创建量子操作
        operation = QuantumOperation(
            name="pauli_x",
            matrix=pauli_x,
            operation_type="unitary"
        )
        
        # 验证操作属性
        assert operation.name == "pauli_x"
        assert operation.operation_type == "unitary"
        npt.assert_array_equal(operation.matrix, pauli_x)
        
        # 验证幺正性
        assert operation.is_unitary(), "Pauli-X should be unitary"
        
        # 验证幺正性的数学条件
        identity_check = operation.matrix.conj().T @ operation.matrix
        npt.assert_allclose(identity_check, np.eye(2), atol=self.tolerance)
    
    def test_measurement_operation_creation(self):
        """测试测量操作的创建和验证"""
        # 定义 Z 基测量的 POVM 元素
        M_0 = np.array([[1, 0], [0, 0]], dtype=complex)  # |0⟩⟨0|
        M_1 = np.array([[0, 0], [0, 1]], dtype=complex)  # |1⟩⟨1|
        
        # 创建测量操作
        measurement = QuantumOperation(
            name="z_measurement",
            matrix=[M_0, M_1],
            operation_type="measurement"
        )
        
        # 验证测量属性
        assert measurement.name == "z_measurement"
        assert measurement.operation_type == "measurement"
        assert len(measurement.matrix) == 2
        
        # 验证 POVM 完备性
        assert measurement.is_valid_povm(), "Z measurement should be a valid POVM"
        
        # 验证完备性关系：Σᵢ Mᵢ†Mᵢ = I
        completeness = sum(M.conj().T @ M for M in measurement.matrix)
        npt.assert_allclose(completeness, np.eye(2), atol=self.tolerance)
    
    def test_channel_operation_creation(self):
        """测试量子信道操作的创建和验证"""
        # 定义去极化信道的 Kraus 算子
        p = 0.1  # 去极化概率
        sqrt_p = np.sqrt(p)
        sqrt_1_minus_p = np.sqrt(1 - p)
        
        K_0 = sqrt_1_minus_p * np.eye(2)
        K_1 = sqrt_p/np.sqrt(3) * np.array([[0, 1], [1, 0]])  # Pauli-X
        K_2 = sqrt_p/np.sqrt(3) * np.array([[0, -1j], [1j, 0]])  # Pauli-Y
        K_3 = sqrt_p/np.sqrt(3) * np.array([[1, 0], [0, -1]])  # Pauli-Z
        
        # 创建信道操作
        channel = QuantumOperation(
            name="depolarizing_channel",
            matrix=[K_0, K_1, K_2, K_3],
            operation_type="channel",
            parameters={'depolarization_prob': p}
        )
        
        # 验证信道属性
        assert channel.name == "depolarizing_channel"
        assert channel.operation_type == "channel"
        assert channel.parameters['depolarization_prob'] == p
        
        # 验证 Kraus 算子的完备性
        assert channel.is_valid_channel(), "Should be a valid quantum channel"
        
        # 验证完备性关系：Σᵢ Kᵢ†Kᵢ = I
        completeness = sum(K.conj().T @ K for K in channel.matrix)
        npt.assert_allclose(completeness, np.eye(2), atol=self.tolerance)
    
    def test_operation_composition(self):
        """测试量子操作的组合"""
        # 创建两个幺正操作
        pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
        pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        op_x = QuantumOperation("pauli_x", pauli_x, "unitary")
        op_z = QuantumOperation("pauli_z", pauli_z, "unitary")
        
        # 组合操作：先 Z 后 X
        composed_op = op_x.compose(op_z)
        
        # 验证组合结果
        expected_matrix = pauli_x @ pauli_z
        npt.assert_allclose(composed_op.matrix, expected_matrix, atol=self.tolerance)
        
        # 验证组合操作仍然是幺正的
        assert composed_op.is_unitary(), "Composition of unitaries should be unitary"


class TestProtocolFeatures:
    """
    测试 ProtocolFeatures 类
    
    验证协议的信息论特征计算和分析
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-10
        
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
    
    def test_bb84_protocol_features(self):
        """测试 BB84 协议的信息论特征"""
        # 定义 BB84 协议的量子操作序列
        operations = [
            QuantumOperation("state_prep", None, "preparation"),
            QuantumOperation("quantum_channel", None, "channel"), 
            QuantumOperation("measurement", None, "measurement")
        ]
        
        # 创建协议特征
        bb84_features = ProtocolFeatures(
            name="BB84",
            operations=operations,
            parties=['Alice', 'Bob'],
            communication_rounds=1,
            measurement_bases=2
        )
        
        # 验证基本属性
        assert bb84_features.name == "BB84"
        assert len(bb84_features.parties) == 2
        assert bb84_features.communication_rounds == 1
        assert bb84_features.measurement_bases == 2
        
        # 计算信息论特征
        features = bb84_features.calculate_information_theoretic_features()
        
        # 验证信息论特征
        assert 'max_classical_capacity' in features
        assert 'quantum_capacity' in features
        assert 'private_capacity' in features
        assert features['max_classical_capacity'] >= 0
    
    def test_mdi_qkd_protocol_features(self):
        """测试 MDI-QKD 协议的信息论特征"""
        # 定义 MDI-QKD 协议的操作序列
        operations = [
            QuantumOperation("alice_prep", None, "preparation"),
            QuantumOperation("bob_prep", None, "preparation"),
            QuantumOperation("alice_channel", None, "channel"),
            QuantumOperation("bob_channel", None, "channel"),
            QuantumOperation("bell_measurement", None, "measurement")
        ]
        
        # 创建协议特征
        mdi_features = ProtocolFeatures(
            name="MDI_QKD",
            operations=operations,
            parties=['Alice', 'Bob', 'Charlie'],
            communication_rounds=1,
            measurement_bases=2,
            trusted_parties=['Alice', 'Bob'],
            untrusted_parties=['Charlie']
        )
        
        # 验证 MDI 特殊属性
        assert len(mdi_features.parties) == 3
        assert 'Charlie' in mdi_features.untrusted_parties
        assert len(mdi_features.trusted_parties) == 2
        
        # 计算信息论特征
        features = mdi_features.calculate_information_theoretic_features()
        
        # 验证 MDI 特有的安全性特征
        assert 'measurement_device_independence' in features
        assert features['measurement_device_independence'] == True
    
    def test_protocol_comparison(self):
        """测试不同协议的特征比较"""
        # 创建简化的协议特征进行比较
        bb84_simple = ProtocolFeatures(
            name="BB84_simple",
            operations=[],
            parties=['Alice', 'Bob'],
            communication_rounds=1,
            measurement_bases=2
        )
        
        decoy_bb84 = ProtocolFeatures(
            name="Decoy_BB84",
            operations=[],
            parties=['Alice', 'Bob'],
            communication_rounds=1,
            measurement_bases=2,
            intensity_settings=3  # signal, decoy, vacuum
        )
        
        # 比较协议特征
        comparison = bb84_simple.compare_with(decoy_bb84)
        
        # 验证比较结果
        assert 'complexity_difference' in comparison
        assert 'security_enhancement' in comparison
        assert comparison['complexity_difference'] > 0  # decoy state 更复杂
    
    def test_entropy_calculation(self):
        """测试协议的熵计算功能"""
        # 创建测试协议
        test_protocol = ProtocolFeatures(
            name="test_protocol",
            operations=[],
            parties=['Alice', 'Bob']
        )
        
        # 定义测试密度矩阵
        rho = np.array([[0.6, 0.1], [0.1, 0.4]], dtype=complex)
        
        # 计算各种熵
        von_neumann_entropy = test_protocol.calculate_von_neumann_entropy(rho)
        
        # 验证熵的基本性质
        assert von_neumann_entropy >= 0, "Entropy should be non-negative"
        assert von_neumann_entropy <= np.log2(2), "Entropy should not exceed maximum"
        
        # 验证纯态的熵为零
        pure_state = np.array([[1, 0], [0, 0]], dtype=complex)
        pure_entropy = test_protocol.calculate_von_neumann_entropy(pure_state)
        npt.assert_allclose(pure_entropy, 0.0, atol=self.tolerance)


class TestUniversalSecurityFramework:
    """
    测试 UniversalSecurityFramework 类
    
    验证通用安全性分析框架的功能
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-10
        
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
    
    def test_framework_initialization(self):
        """测试安全框架的初始化"""
        # 创建通用安全框架
        framework = UniversalSecurityFramework()
        
        # 验证默认配置
        assert hasattr(framework, 'entropy_estimator')
        assert hasattr(framework, 'composability_analyzer')
        assert hasattr(framework, 'finite_key_analyzer')
    
    def test_protocol_agnostic_security_analysis(self):
        """测试协议无关的安全性分析"""
        framework = UniversalSecurityFramework()
        
        # 定义任意协议的特征
        arbitrary_protocol = ProtocolFeatures(
            name="arbitrary_protocol",
            operations=[],
            parties=['Alice', 'Bob'],
            communication_rounds=2,
            measurement_bases=3
        )
        
        # 定义实验数据
        experimental_data = {
            'qber': 0.05,
            'gain': 0.1,
            'n_pulses': 100000,
            'basis_statistics': {'X': 0.5, 'Y': 0.3, 'Z': 0.2}
        }
        
        # 进行安全性分析
        security_result = framework.analyze_protocol_security(
            protocol_features=arbitrary_protocol,
            experimental_data=experimental_data
        )
        
        # 验证分析结果
        assert 'key_rate' in security_result
        assert 'security_parameter' in security_result
        assert 'finite_key_length' in security_result
        assert security_result['key_rate'] >= 0
    
    def test_entropy_accumulation_analysis(self):
        """测试熵累积分析"""
        framework = UniversalSecurityFramework()
        
        # 模拟多轮协议数据
        rounds_data = []
        for i in range(10):
            round_data = {
                'round': i,
                'measurements': np.random.randint(0, 2, 1000),
                'basis_choices': np.random.choice(['X', 'Z'], 1000),
                'qber': 0.02 + 0.001 * i  # 略微增加的错误率
            }
            rounds_data.append(round_data)
        
        # 应用熵累积定理
        entropy_result = framework.apply_entropy_accumulation(rounds_data)
        
        # 验证熵累积结果
        assert 'accumulated_entropy' in entropy_result
        assert 'smoothing_parameter' in entropy_result
        assert 'finite_key_correction' in entropy_result
        assert entropy_result['accumulated_entropy'] >= 0
    
    def test_composable_security_analysis(self):
        """测试可组合安全性分析"""
        framework = UniversalSecurityFramework()
        
        # 定义多个协议实例
        protocol_instances = [
            {'protocol_id': 'instance_1', 'epsilon': 1e-10},
            {'protocol_id': 'instance_2', 'epsilon': 1e-11},
            {'protocol_id': 'instance_3', 'epsilon': 1e-12},
        ]
        
        # 分析可组合安全性
        composability_result = framework.analyze_composable_security(protocol_instances)
        
        # 验证可组合性结果
        assert 'total_security_parameter' in composability_result
        assert 'composability_overhead' in composability_result
        assert 'is_composable_secure' in composability_result
        assert composability_result['total_security_parameter'] >= max(
            instance['epsilon'] for instance in protocol_instances
        )
    
    def test_device_independent_analysis(self):
        """测试设备无关安全性分析"""
        framework = UniversalSecurityFramework()
        
        # 定义设备无关实验数据
        di_data = {
            'bell_violation': 2.4,  # CHSH 不等式违反值
            'detection_efficiency': 0.8,
            'measurement_statistics': {
                '00': 0.25, '01': 0.25, '10': 0.25, '11': 0.25
            }
        }
        
        # 进行设备无关分析
        di_result = framework.analyze_device_independent_security(di_data)
        
        # 验证设备无关结果
        assert 'min_entropy_bound' in di_result
        assert 'randomness_rate' in di_result
        assert 'device_independence_certified' in di_result
        
        # 如果 Bell 不等式被违反，应该能证明设备无关性
        if di_data['bell_violation'] > 2.0:
            assert di_result['device_independence_certified'] == True


class TestUniversalSecurityParameters:
    """
    测试重构后的 UniversalSecurityParameters 类
    
    验证通用安全参数的功能和向后兼容性
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-15
    
    def test_backward_compatibility(self):
        """测试向后兼容性"""
        # 如果新框架未实现，使用原有框架
        if NEW_FRAMEWORK:
            # 使用新的通用参数类
            params = UniversalSecurityParameters()
        else:
            # 使用原有的参数类
            params = SecurityParameters()
        
        # 验证原有接口仍然可用
        assert hasattr(params, 'epsilon_sec')
        assert hasattr(params, 'epsilon_cor')
        assert hasattr(params, 'get_total_privacy_error')
        assert hasattr(params, 'get_total_failure_prob')
        
        # 验证默认值
        assert params.epsilon_sec > 0
        assert params.epsilon_cor > 0
    
    def test_universal_parameters_extension(self):
        """测试通用参数的扩展功能"""
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
        
        # 创建通用安全参数
        params = UniversalSecurityParameters(
            epsilon_sec=1e-10,
            epsilon_cor=1e-15,
            epsilon_rob=1e-9,
            # 新的通用参数
            entropy_smoothing_param=1e-8,
            composability_param=1e-7,
            device_independence_param=1e-6
        )
        
        # 验证新参数
        assert hasattr(params, 'entropy_smoothing_param')
        assert hasattr(params, 'composability_param')
        assert hasattr(params, 'device_independence_param')
        
        # 验证参数值
        assert params.entropy_smoothing_param == 1e-8
        assert params.composability_param == 1e-7
        assert params.device_independence_param == 1e-6
    
    def test_information_theoretic_bounds(self):
        """测试信息论界限的计算"""
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
        
        params = UniversalSecurityParameters()
        
        # 计算各种信息论界限
        bounds = params.calculate_information_theoretic_bounds(
            min_entropy=0.5,
            mutual_information=0.3,
            protocol_rounds=100
        )
        
        # 验证界限
        assert 'privacy_amplification_bound' in bounds
        assert 'error_correction_bound' in bounds
        assert 'finite_key_bound' in bounds
        assert all(bound >= 0 for bound in bounds.values())
    
    def test_protocol_adaptation(self):
        """测试参数对不同协议的自适应"""
        if not NEW_FRAMEWORK:
            pytest.skip("New universal framework not yet implemented")
        
        params = UniversalSecurityParameters()
        
        # 为不同协议类型适应参数
        bb84_params = params.adapt_for_protocol('BB84')
        mdi_params = params.adapt_for_protocol('MDI_QKD')
        di_params = params.adapt_for_protocol('DEVICE_INDEPENDENT')
        
        # 验证适应性
        assert bb84_params is not None
        assert mdi_params is not None
        assert di_params is not None
        
        # 不同协议可能有不同的参数要求
        assert hasattr(bb84_params, 'basis_reconciliation_param')
        assert hasattr(mdi_params, 'measurement_device_param')
        assert hasattr(di_params, 'bell_violation_param')


class TestBackwardCompatibility:
    """
    测试向后兼容性
    
    确保重构不会破坏现有代码
    """
    
    def test_existing_code_compatibility(self):
        """测试现有代码的兼容性"""
        # 如果原有框架存在，测试其功能
        if ORIGINAL_FRAMEWORK:
            # 测试原有的 ProtocolType 枚举
            assert hasattr(ProtocolType, 'BB84')
            assert hasattr(ProtocolType, 'MDI_QKD')
            assert ProtocolType.BB84.value == 'BB84'
            
            # 测试原有的 SecurityParameters
            params = SecurityParameters()
            assert params.epsilon_sec == 1e-9
            assert params.epsilon_cor == 1e-15
            
            # 测试原有方法
            privacy_error = params.get_total_privacy_error()
            failure_prob = params.get_total_failure_prob()
            assert privacy_error > 0
            assert failure_prob > 0
    
    def test_import_compatibility(self):
        """测试导入兼容性"""
        # 确保重构后的模块可以通过原有路径导入
        try:
            from security_evaluator.ac_framework import SecurityParameters
            old_import_works = True
        except ImportError:
            old_import_works = False
        
        # 如果重构到新文件，确保仍可通过原路径导入
        if not old_import_works:
            try:
                from security_evaluator.universal_framework import SecurityParameters
                new_import_works = True
            except ImportError:
                new_import_works = False
            
            assert new_import_works, "Should be able to import SecurityParameters from new location"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])