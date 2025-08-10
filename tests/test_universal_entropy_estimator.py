"""
通用熵估计器的TDD测试模块

测试基于信息论的通用熵估计功能，确保数学正确性和计算精度。

测试覆盖：
1. 通用熵估计方法
2. 互信息和Holevo信息估计
3. 有限密钥效应处理
4. 统计涨落处理
5. 向后兼容性
6. 协议无关性验证
7. 数值稳定性
8. 估计精度和收敛性

作者：AI4QKD Team  
版本：2.0 - Universal Framework
"""

import pytest
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any
import warnings

# 导入待测试模块
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from security_evaluator.entropy_estimator import (
        EntropyEstimator, 
        EntropyResult
    )
    from security_evaluator.universal_framework import (
        ProtocolFeatures,
        QuantumOperation,
        QuantumOperationType,
        UniversalSecurityParameters,
        create_bb84_protocol,
        create_mdi_qkd_protocol,
        create_decoy_bb84_protocol
    )
    _MODULES_AVAILABLE = True
except ImportError as e:
    _MODULES_AVAILABLE = False
    print(f"Warning: Could not import modules: {e}")


@pytest.mark.skipif(not _MODULES_AVAILABLE, reason="Required modules not available")
class TestUniversalEntropyEstimator:
    """通用熵估计器测试类"""
    
    @pytest.fixture
    def sample_measurement_data(self):
        """模拟测量数据"""
        np.random.seed(42)  # 确保可重现性
        return {
            'alice_measurements': np.random.randint(0, 2, 10000),
            'bob_measurements': np.random.randint(0, 2, 10000),
            'alice_bases': np.random.choice(['Z', 'X'], 10000),
            'bob_bases': np.random.choice(['Z', 'X'], 10000),
            'eavesdropper_info': np.random.random(10000),
            'detection_events': np.random.choice([True, False], 10000, p=[0.7, 0.3])
        }
    
    @pytest.fixture
    def bb84_protocol_features(self):
        """BB84协议特征"""
        return create_bb84_protocol()
    
    @pytest.fixture 
    def universal_security_params(self):
        """通用安全参数"""
        return UniversalSecurityParameters(
            epsilon_sec=1e-10,
            epsilon_cor=1e-10,
            epsilon_pe=1e-10,
            entropy_smoothing_param=1e-8,
            composability_param=1e-9,
            finite_key_param=1e-7
        )
    
    # ==================== 通用熵估计方法测试 ====================
    
    def test_estimate_universal_entropy_interface(self, sample_measurement_data, bb84_protocol_features, universal_security_params):
        """测试通用熵估计接口"""
        estimator = EntropyEstimator()
        
        # 测试新的通用接口是否存在
        assert hasattr(estimator, 'estimate_universal_entropy'), "必须实现 estimate_universal_entropy 方法"
        assert hasattr(estimator, 'estimate_mutual_information'), "必须实现 estimate_mutual_information 方法"
        assert hasattr(estimator, 'estimate_holevo_information'), "必须实现 estimate_holevo_information 方法"
        
        # 测试通用熵估计
        result = estimator.estimate_universal_entropy(
            measurement_data=sample_measurement_data,
            protocol_features=bb84_protocol_features,
            security_params=universal_security_params
        )
        
        # 验证返回结果结构
        assert isinstance(result, EntropyResult), "必须返回 EntropyResult 对象"
        assert hasattr(result, 'entropy_type'), "结果必须包含熵类型"
        assert hasattr(result, 'value'), "结果必须包含熵值"
        assert result.value >= 0, "熵值必须非负"
    
    def test_estimate_universal_entropy_bb84_perfect_channel(self):
        """测试BB84在理想信道下的通用熵估计"""
        estimator = EntropyEstimator()
        
        # 构造理想信道数据（无错误）
        n_samples = 10000
        perfect_data = {
            'alice_measurements': [0, 1] * (n_samples // 2),
            'bob_measurements': [0, 1] * (n_samples // 2),  # 完全匹配
            'alice_bases': ['Z', 'X'] * (n_samples // 2),
            'bob_bases': ['Z', 'X'] * (n_samples // 2),    # 基匹配
            'eavesdropper_info': [0.0] * n_samples,         # 无窃听
            'detection_events': [True] * n_samples
        }
        
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        result = estimator.estimate_universal_entropy(perfect_data, bb84_features, security_params)
        
        # 理想BB84的熵应接近最大值
        assert result.value > 0.9, f"理想BB84熵应接近1，实际: {result.value}"
        assert result.entropy_type == "universal_entropy", "熵类型应为通用熵"
    
    def test_estimate_universal_entropy_with_noise(self):
        """测试有噪声情况下的通用熵估计"""
        estimator = EntropyEstimator()
        
        # 构造有噪声的数据（10%错误率）
        n_samples = 10000
        noise_rate = 0.1
        
        np.random.seed(123)
        alice_bits = np.random.randint(0, 2, n_samples)
        # 引入错误
        bob_bits = alice_bits.copy()
        error_indices = np.random.choice(n_samples, int(n_samples * noise_rate), replace=False)
        bob_bits[error_indices] = 1 - bob_bits[error_indices]
        
        noisy_data = {
            'alice_measurements': alice_bits.tolist(),
            'bob_measurements': bob_bits.tolist(),
            'alice_bases': ['Z'] * n_samples,
            'bob_bases': ['Z'] * n_samples,
            'eavesdropper_info': np.random.random(n_samples).tolist(),
            'detection_events': [True] * n_samples
        }
        
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        result = estimator.estimate_universal_entropy(noisy_data, bb84_features, security_params)
        
        # 噪声应降低可用熵
        assert 0.4 < result.value < 0.9, f"有噪声BB84熵应在合理范围，实际: {result.value}"
    
    # ==================== 互信息估计测试 ====================
    
    def test_estimate_mutual_information_basic(self, sample_measurement_data, bb84_protocol_features):
        """测试基本互信息估计"""
        estimator = EntropyEstimator()
        
        mutual_info = estimator.estimate_mutual_information(
            measurement_data=sample_measurement_data,
            protocol_features=bb84_protocol_features
        )
        
        assert isinstance(mutual_info, float), "互信息应为浮点数"
        assert 0 <= mutual_info <= 1, f"互信息应在[0,1]范围内，实际: {mutual_info}"
    
    def test_estimate_mutual_information_perfect_correlation(self):
        """测试完全相关时的互信息估计"""
        estimator = EntropyEstimator()
        
        # 构造完全相关的数据
        n_samples = 5000
        bits = np.random.randint(0, 2, n_samples)
        
        perfect_correlation_data = {
            'alice_measurements': bits.tolist(),
            'bob_measurements': bits.tolist(),  # 完全相同
            'alice_bases': ['Z'] * n_samples,
            'bob_bases': ['Z'] * n_samples,
            'detection_events': [True] * n_samples
        }
        
        bb84_features = create_bb84_protocol()
        mutual_info = estimator.estimate_mutual_information(perfect_correlation_data, bb84_features)
        
        # 完全相关的互信息应接近1
        assert mutual_info > 0.9, f"完全相关的互信息应接近1，实际: {mutual_info}"
    
    def test_estimate_mutual_information_no_correlation(self):
        """测试无相关时的互信息估计"""
        estimator = EntropyEstimator()
        
        # 构造无相关的数据
        n_samples = 5000
        np.random.seed(456)
        
        no_correlation_data = {
            'alice_measurements': np.random.randint(0, 2, n_samples).tolist(),
            'bob_measurements': np.random.randint(0, 2, n_samples).tolist(),  # 独立随机
            'alice_bases': ['Z'] * n_samples,
            'bob_bases': ['Z'] * n_samples,
            'detection_events': [True] * n_samples
        }
        
        bb84_features = create_bb84_protocol()
        mutual_info = estimator.estimate_mutual_information(no_correlation_data, bb84_features)
        
        # 无相关的互信息应接近0
        assert mutual_info < 0.1, f"无相关的互信息应接近0，实际: {mutual_info}"
    
    # ==================== Holevo信息估计测试 ====================
    
    def test_estimate_holevo_information_basic(self, sample_measurement_data, bb84_protocol_features):
        """测试基本Holevo信息估计"""
        estimator = EntropyEstimator()
        
        holevo_info = estimator.estimate_holevo_information(
            measurement_data=sample_measurement_data,
            protocol_features=bb84_protocol_features
        )
        
        assert isinstance(holevo_info, float), "Holevo信息应为浮点数"
        assert holevo_info >= 0, f"Holevo信息应非负，实际: {holevo_info}"
    
    def test_estimate_holevo_information_bounds(self):
        """测试Holevo信息的数学边界"""
        estimator = EntropyEstimator()
        
        # 测试不同错误率下的Holevo信息
        bb84_features = create_bb84_protocol()
        
        test_cases = [
            {'error_rate': 0.0, 'expected_max': 0.1},
            {'error_rate': 0.1, 'expected_range': (0.3, 0.5)},
            {'error_rate': 0.25, 'expected_range': (0.7, 1.0)},
            {'error_rate': 0.49, 'expected_range': (0.9, 1.0)}
        ]
        
        for case in test_cases:
            # 构造数据
            n_samples = 2000
            error_rate = case['error_rate']
            
            alice_bits = np.random.randint(0, 2, n_samples)
            bob_bits = alice_bits.copy()
            
            # 引入错误
            if error_rate > 0:
                n_errors = int(n_samples * error_rate)
                error_indices = np.random.choice(n_samples, n_errors, replace=False)
                bob_bits[error_indices] = 1 - bob_bits[error_indices]
            
            data = {
                'alice_measurements': alice_bits.tolist(),
                'bob_measurements': bob_bits.tolist(),
                'alice_bases': ['Z'] * n_samples,
                'bob_bases': ['Z'] * n_samples,
                'eavesdropper_info': [error_rate] * n_samples,
                'detection_events': [True] * n_samples
            }
            
            holevo_info = estimator.estimate_holevo_information(data, bb84_features)
            
            if 'expected_max' in case:
                assert holevo_info <= case['expected_max'], f"错误率{error_rate}下Holevo信息超出预期: {holevo_info}"
            elif 'expected_range' in case:
                low, high = case['expected_range']
                assert low <= holevo_info <= high, f"错误率{error_rate}下Holevo信息{holevo_info}不在预期范围{case['expected_range']}"
    
    # ==================== 有限密钥效应测试 ====================
    
    def test_finite_key_effects_estimation(self, universal_security_params):
        """测试有限密钥效应估计"""
        estimator = EntropyEstimator()
        
        # 测试不同样本数量下的有限密钥效应
        sample_sizes = [1000, 10000, 100000, 1000000]
        finite_key_effects = []
        
        for n in sample_sizes:
            effect = estimator.estimate_finite_key_effects(
                n_samples=n,
                security_params=universal_security_params
            )
            finite_key_effects.append(effect)
        
        # 有限密钥效应应随样本数量增加而减少
        for i in range(1, len(finite_key_effects)):
            assert finite_key_effects[i] < finite_key_effects[i-1], \
                f"有限密钥效应应随样本数增加而减少: {finite_key_effects}"
    
    def test_statistical_fluctuation_handling(self, sample_measurement_data, universal_security_params):
        """测试统计涨落处理"""
        estimator = EntropyEstimator()
        
        # 测试多次重复估计的统计性质
        estimates = []
        for seed in range(10):
            np.random.seed(seed)
            # 添加随机噪声
            noisy_data = sample_measurement_data.copy()
            n_samples = len(noisy_data['alice_measurements'])
            
            # 随机翻转一些比特
            flip_rate = 0.02
            n_flips = int(n_samples * flip_rate)
            flip_indices = np.random.choice(n_samples, n_flips, replace=False)
            
            alice_bits = np.array(noisy_data['alice_measurements'])
            alice_bits[flip_indices] = 1 - alice_bits[flip_indices]
            noisy_data['alice_measurements'] = alice_bits.tolist()
            
            variance = estimator.estimate_statistical_variance(
                measurement_data=noisy_data,
                security_params=universal_security_params
            )
            estimates.append(variance)
        
        # 验证统计性质
        mean_variance = np.mean(estimates)
        std_variance = np.std(estimates)
        
        assert mean_variance > 0, "平均方差应为正"
        assert std_variance < mean_variance, "方差的标准差应小于均值"
    
    # ==================== 协议无关性测试 ====================
    
    def test_protocol_agnostic_entropy_estimation(self, sample_measurement_data, universal_security_params):
        """测试协议无关的熵估计"""
        estimator = EntropyEstimator()
        
        # 测试不同协议的熵估计
        protocols = [
            create_bb84_protocol(),
            create_mdi_qkd_protocol(),
            create_decoy_bb84_protocol()
        ]
        
        entropies = []
        for protocol in protocols:
            entropy = estimator.estimate_universal_entropy(
                measurement_data=sample_measurement_data,
                protocol_features=protocol,
                security_params=universal_security_params
            )
            entropies.append(entropy.value)
        
        # 对于相同的测量数据，不同协议应给出合理范围内的熵估计
        entropy_range = max(entropies) - min(entropies)
        assert entropy_range < 0.5, f"协议间熵估计差异过大: {entropy_range}"
    
    # ==================== 向后兼容性测试 ====================
    
    def test_backward_compatibility_min_entropy(self):
        """测试最小熵计算的向后兼容性"""
        estimator = EntropyEstimator()
        
        # 测试原有接口
        legacy_result = estimator.calculate_min_entropy(qber=0.05, protocol_type="BB84")
        
        # 测试新接口  
        bb84_features = create_bb84_protocol()
        measurement_data = {
            'alice_measurements': [0, 1] * 500,
            'bob_measurements': [0, 1, 1, 1] * 250,  # 25% error
            'alice_bases': ['Z'] * 1000,
            'bob_bases': ['Z'] * 1000,
            'detection_events': [True] * 1000
        }
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        universal_result = estimator.estimate_universal_entropy(
            measurement_data, bb84_features, security_params
        )
        
        # 结果应在合理范围内一致
        relative_diff = abs(legacy_result.value - universal_result.value) / max(legacy_result.value, 1e-10)
        assert relative_diff < 0.2, f"向后兼容性测试失败: 相对差异{relative_diff:.3f}"
    
    def test_backward_compatibility_interface(self):
        """测试向后兼容的接口调用"""
        estimator = EntropyEstimator()
        
        # 确保旧接口仍然可用
        assert hasattr(estimator, 'calculate_min_entropy'), "必须保留 calculate_min_entropy 方法"
        assert hasattr(estimator, 'calculate_conditional_entropy'), "必须保留 calculate_conditional_entropy 方法"
        assert hasattr(estimator, 'calculate_von_neumann_entropy'), "必须保留 calculate_von_neumann_entropy 方法"
        
        # 测试旧接口调用
        result = estimator.calculate_min_entropy(qber=0.05, protocol_type="BB84")
        assert isinstance(result, EntropyResult), "旧接口应返回 EntropyResult 对象"
        assert result.value >= 0, "熵值应非负"
    
    # ==================== 数值稳定性测试 ====================
    
    def test_numerical_stability_extreme_cases(self):
        """测试极端情况下的数值稳定性"""
        estimator = EntropyEstimator()
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-12)
        
        # 极端测试用例
        extreme_cases = [
            {
                'name': '极少样本',
                'data': {
                    'alice_measurements': [0, 1],
                    'bob_measurements': [0, 0],
                    'alice_bases': ['Z', 'X'],
                    'bob_bases': ['Z', 'X'],
                    'detection_events': [True, True]
                }
            },
            {
                'name': '全零数据',
                'data': {
                    'alice_measurements': [0] * 1000,
                    'bob_measurements': [0] * 1000,
                    'alice_bases': ['Z'] * 1000,
                    'bob_bases': ['Z'] * 1000,
                    'detection_events': [True] * 1000
                }
            },
            {
                'name': '交替数据',
                'data': {
                    'alice_measurements': [0, 1] * 500,
                    'bob_measurements': [1, 0] * 500,  # 完全反相关
                    'alice_bases': ['Z'] * 1000,
                    'bob_bases': ['Z'] * 1000,
                    'detection_events': [True] * 1000
                }
            }
        ]
        
        for case in extreme_cases:
            # 计算应该不抛出异常且返回有效结果
            result = estimator.estimate_universal_entropy(
                case['data'], bb84_features, security_params
            )
            
            assert np.isfinite(result.value), f"极端情况下数值不稳定: {case['name']}"
            assert result.value >= 0, f"熵值应非负: {case['name']}"
    
    # ==================== 估计精度和收敛性测试 ====================
    
    def test_estimation_convergence(self):
        """测试估计精度的收敛性"""
        estimator = EntropyEstimator()
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        # 理论值：BB84在5%错误率下的熵
        theoretical_entropy = 1 + 0.05 * np.log2(0.05) + 0.95 * np.log2(0.95)
        
        # 测试不同样本数量下的估计精度
        sample_sizes = [1000, 5000, 10000, 50000]
        estimation_errors = []
        
        for n in sample_sizes:
            # 构造具有已知熵的数据
            np.random.seed(789)
            alice_bits = np.random.randint(0, 2, n)
            bob_bits = alice_bits.copy()
            
            # 引入5%错误
            error_indices = np.random.choice(n, int(n * 0.05), replace=False)
            bob_bits[error_indices] = 1 - bob_bits[error_indices]
            
            data = {
                'alice_measurements': alice_bits.tolist(),
                'bob_measurements': bob_bits.tolist(),
                'alice_bases': ['Z'] * n,
                'bob_bases': ['Z'] * n,
                'detection_events': [True] * n
            }
            
            result = estimator.estimate_universal_entropy(data, bb84_features, security_params)
            error = abs(result.value - theoretical_entropy)
            estimation_errors.append(error)
        
        # 估计误差应随样本数增加而减少
        for i in range(1, len(estimation_errors)):
            # 允许一些统计涨落，但总体趋势应该是减少的
            assert estimation_errors[i] <= estimation_errors[i-1] + 0.1, \
                f"估计精度应随样本数增加而提高: {estimation_errors}"
    
    # ==================== 性能测试 ====================
    
    def test_computation_performance(self):
        """测试计算性能"""
        import time
        
        estimator = EntropyEstimator()
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        # 大规模数据
        n_samples = 100000
        np.random.seed(999)
        
        large_data = {
            'alice_measurements': np.random.randint(0, 2, n_samples).tolist(),
            'bob_measurements': np.random.randint(0, 2, n_samples).tolist(),
            'alice_bases': np.random.choice(['Z', 'X'], n_samples).tolist(),
            'bob_bases': np.random.choice(['Z', 'X'], n_samples).tolist(),
            'detection_events': np.random.choice([True, False], n_samples, p=[0.7, 0.3]).tolist()
        }
        
        # 性能计时
        start_time = time.time()
        result = estimator.estimate_universal_entropy(large_data, bb84_features, security_params)
        end_time = time.time()
        
        computation_time = end_time - start_time
        
        # 计算应在合理时间内完成（< 5秒）
        assert computation_time < 5.0, f"计算耗时过长: {computation_time:.2f}秒"
        assert np.isfinite(result.value), "大规模计算结果应有效"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])