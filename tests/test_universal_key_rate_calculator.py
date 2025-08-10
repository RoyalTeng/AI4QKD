"""
通用密钥率计算器的TDD测试模块

测试基于信息论的通用密钥率计算功能，确保数学正确性和与现有实现的兼容性。

测试覆盖：
1. 通用密钥率公式 R = I(A:B) - χ(A:E) - δ(n) - ε
2. 互信息计算
3. Holevo信息计算
4. 有限密钥效应
5. 向后兼容性
6. 协议无关性验证

作者：AI4QKD Team  
版本：2.0 - Universal Framework
"""

import pytest
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# 导入待测试模块
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入测试所需模块
try:
    from security_evaluator.key_rate_calculator import (
        KeyRateCalculator, 
        KeyRateParameters, 
        KeyRateResult
    )
    from security_evaluator.ac_framework import ProtocolType, SecurityParameters
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
    # 创建虚拟类以避免测试失败
    class DummyTest:
        pass


@pytest.mark.skipif(not _MODULES_AVAILABLE, reason="Required modules not available")
class TestUniversalKeyRateCalculator:
    """通用密钥率计算器测试类"""
    
    @pytest.fixture
    def sample_simulation_results(self):
        """模拟仿真结果数据"""
        return {
            'raw_statistics': {
                'alice_bits': [0, 1, 0, 1, 1, 0, 1, 0],
                'bob_bits': [0, 1, 1, 1, 1, 0, 1, 1],  # 1个错误
                'alice_bases': ['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X'],
                'bob_bases': ['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X'],
                'detections': [True, True, True, True, True, True, True, False]
            },
            'channel_statistics': {
                'transmission_probability': 0.5,
                'error_probability': 0.02,
                'total_pulses': 1000000,
                'detected_pulses': 500000
            }
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
    
    # ==================== 通用密钥率公式测试 ====================
    
    def test_universal_key_rate_formula_components(self, sample_simulation_results, bb84_protocol_features, universal_security_params):
        """测试通用密钥率公式各组件计算"""
        calculator = KeyRateCalculator()
        
        # 1. 测试互信息计算 I(A:B)
        mutual_info = calculator.compute_mutual_information(
            sample_simulation_results, bb84_protocol_features
        )
        assert 0 <= mutual_info <= 1, "互信息应在[0,1]范围内"
        
        # 2. 测试Holevo信息计算 χ(A:E)
        holevo_info = calculator.compute_holevo_information(
            sample_simulation_results, bb84_protocol_features
        )
        assert holevo_info >= 0, "Holevo信息应非负"
        
        # 3. 测试有限密钥修正 δ(n)
        finite_key_correction = calculator.compute_finite_key_correction(
            n_pulses=1000000, security_params=universal_security_params
        )
        assert finite_key_correction >= 0, "有限密钥修正应非负"
        
        # 4. 测试总体公式 R = I(A:B) - χ(A:E) - δ(n) - ε
        key_rate = mutual_info - holevo_info - finite_key_correction - universal_security_params.epsilon_sec
        assert key_rate >= -1, "密钥率下界检查"
    
    def test_universal_compute_method(self, sample_simulation_results, bb84_protocol_features, universal_security_params):
        """测试通用compute()方法"""
        calculator = KeyRateCalculator()
        
        # 使用新的通用接口
        result = calculator.compute_universal(
            simulation_results=sample_simulation_results,
            protocol_features=bb84_protocol_features,
            security_params=universal_security_params
        )
        
        # 验证返回结果结构
        assert hasattr(result, 'final_key_rate')
        assert hasattr(result, 'mutual_information')
        assert hasattr(result, 'holevo_information')
        assert hasattr(result, 'finite_key_correction')
        
        # 验证数学一致性
        expected_rate = (result.mutual_information - 
                        result.holevo_information - 
                        result.finite_key_correction - 
                        universal_security_params.epsilon_sec)
        
        assert abs(result.final_key_rate - max(0, expected_rate)) < 1e-10, "密钥率计算一致性检查"
    
    # ==================== 互信息计算测试 ====================
    
    def test_mutual_information_bb84_perfect_channel(self):
        """测试BB84在理想信道下的互信息计算"""
        calculator = KeyRateCalculator()
        
        # 构造理想信道仿真结果（无错误）
        perfect_results = {
            'raw_statistics': {
                'alice_bits': [0, 1, 0, 1] * 250,  # 1000个比特
                'bob_bits': [0, 1, 0, 1] * 250,    # 完全匹配
                'alice_bases': ['Z', 'X'] * 500,
                'bob_bases': ['Z', 'X'] * 500,     # 基选择匹配
                'detections': [True] * 1000
            }
        }
        
        bb84_features = create_bb84_protocol()
        mutual_info = calculator.compute_mutual_information(perfect_results, bb84_features)
        
        # 理想BB84的互信息应接近1
        assert abs(mutual_info - 1.0) < 0.01, f"理想BB84互信息应接近1，实际: {mutual_info}"
    
    def test_mutual_information_with_errors(self):
        """测试有错误情况下的互信息计算"""
        calculator = KeyRateCalculator()
        
        # 构造有10%错误率的仿真结果
        noisy_results = {
            'raw_statistics': {
                'alice_bits': [0] * 450 + [1] * 450,  # 900个比特
                'bob_bits': [0] * 405 + [1] * 45 + [0] * 45 + [1] * 405,  # 10%错误
                'alice_bases': ['Z'] * 900,
                'bob_bases': ['Z'] * 900,
                'detections': [True] * 900
            }
        }
        
        bb84_features = create_bb84_protocol()
        mutual_info = calculator.compute_mutual_information(noisy_results, bb84_features)
        
        # 根据二元对称信道理论，10%错误率应给出约0.53的互信息
        expected_mutual_info = 1 + 0.1 * np.log2(0.1) + 0.9 * np.log2(0.9)
        assert abs(mutual_info - expected_mutual_info) < 0.05, f"互信息计算错误: 期望{expected_mutual_info}, 实际{mutual_info}"
    
    # ==================== Holevo信息计算测试 ====================
    
    def test_holevo_information_bb84(self):
        """测试BB84协议的Holevo信息计算"""
        calculator = KeyRateCalculator()
        
        # BB84的标准信道模型
        channel_results = {
            'channel_statistics': {
                'transmission_probability': 0.5,
                'error_probability': 0.05,
                'eavesdropping_model': 'intercept_resend'
            }
        }
        
        bb84_features = create_bb84_protocol()
        holevo_info = calculator.compute_holevo_information(channel_results, bb84_features)
        
        # BB84在截获重发攻击下的Holevo信息应约为QBER的二元熵
        qber = 0.05
        expected_holevo = -qber * np.log2(qber) - (1-qber) * np.log2(1-qber)
        
        assert abs(holevo_info - expected_holevo) < 0.1, f"BB84 Holevo信息计算错误: 期望{expected_holevo}, 实际{holevo_info}"
    
    def test_holevo_information_bounds(self):
        """测试Holevo信息的数学边界"""
        calculator = KeyRateCalculator()
        
        # 测试边界情况
        test_cases = [
            {'error_probability': 0.0, 'expected_max': 0.0},     # 无错误
            {'error_probability': 0.5, 'expected_max': 1.0},     # 最大熵
            {'error_probability': 1.0, 'expected_max': 0.0}      # 完全错误
        ]
        
        bb84_features = create_bb84_protocol()
        
        for case in test_cases:
            channel_results = {
                'channel_statistics': {
                    'error_probability': case['error_probability']
                }
            }
            
            holevo_info = calculator.compute_holevo_information(channel_results, bb84_features)
            assert 0 <= holevo_info <= case['expected_max'] + 0.01, f"Holevo信息边界检查失败: {case}"
    
    # ==================== 有限密钥效应测试 ====================
    
    def test_finite_key_correction_scaling(self):
        """测试有限密钥修正的渐近行为"""
        calculator = KeyRateCalculator()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        # 测试不同脉冲数量下的修正项
        pulse_counts = [1000, 10000, 100000, 1000000]
        corrections = []
        
        for n in pulse_counts:
            correction = calculator.compute_finite_key_correction(n, security_params)
            corrections.append(correction)
        
        # 有限密钥修正应随√n减少
        for i in range(1, len(corrections)):
            ratio = corrections[i-1] / corrections[i]
            expected_ratio = np.sqrt(pulse_counts[i] / pulse_counts[i-1])
            assert abs(ratio - expected_ratio) < 0.2, f"有限密钥修正缩放错误: {ratio} vs {expected_ratio}"
    
    def test_finite_key_correction_security_parameter_dependence(self):
        """测试有限密钥修正对安全参数的依赖"""
        calculator = KeyRateCalculator()
        n_pulses = 100000
        
        # 测试不同安全参数
        epsilons = [1e-6, 1e-8, 1e-10, 1e-12]
        corrections = []
        
        for eps in epsilons:
            security_params = UniversalSecurityParameters(epsilon_sec=eps)
            correction = calculator.compute_finite_key_correction(n_pulses, security_params)
            corrections.append(correction)
        
        # 修正项应随log(1/ε)增长
        for i in range(1, len(corrections)):
            assert corrections[i] > corrections[i-1], "有限密钥修正应随ε减小而增大"
    
    # ==================== 协议无关性测试 ====================
    
    def test_protocol_agnostic_calculation(self):
        """测试通用框架的协议无关性"""
        calculator = KeyRateCalculator()
        
        # 相同仿真结果，不同协议
        simulation_results = {
            'raw_statistics': {
                'alice_bits': [0, 1] * 500,
                'bob_bits': [0, 1] * 500,
                'alice_bases': ['Z', 'X'] * 500,
                'bob_bases': ['Z', 'X'] * 500,
                'detections': [True] * 1000
            }
        }
        
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        # 测试不同协议
        protocols = [
            create_bb84_protocol(),
            create_mdi_qkd_protocol(),
            create_decoy_bb84_protocol()
        ]
        
        results = []
        for protocol in protocols:
            result = calculator.compute_universal(simulation_results, protocol, security_params)
            results.append(result)
        
        # 由于仿真结果相同，不同协议应给出相似的密钥率（在误差范围内）
        key_rates = [r.final_key_rate for r in results]
        max_diff = max(key_rates) - min(key_rates)
        assert max_diff < 0.1, f"相同仿真结果的不同协议密钥率差异过大: {max_diff}"
    
    # ==================== 向后兼容性测试 ====================
    
    def test_backward_compatibility_bb84(self):
        """测试与现有BB84计算的向后兼容性"""
        # 现有接口
        old_calculator = KeyRateCalculator(qber=0.05, gain=0.5, protocol_type=ProtocolType.BB84)
        old_result = old_calculator.calculate_key_rate()
        
        # 新通用接口
        new_calculator = KeyRateCalculator()
        
        # 构造等效的仿真结果
        n_pulses = 1000000
        n_detected = int(n_pulses * 0.5)
        n_errors = int(n_detected * 0.05)
        
        simulation_results = {
            'raw_statistics': {
                'alice_bits': [0] * (n_detected - n_errors) + [1] * n_errors,
                'bob_bits': [0] * n_detected,
                'alice_bases': ['Z'] * n_detected,
                'bob_bases': ['Z'] * n_detected,
                'detections': [True] * n_detected + [False] * (n_pulses - n_detected)
            },
            'channel_statistics': {
                'transmission_probability': 0.5,
                'error_probability': 0.05
            }
        }
        
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        new_result = new_calculator.compute_universal(simulation_results, bb84_features, security_params)
        
        # 结果应在10%误差范围内一致
        relative_error = abs(new_result.final_key_rate - old_result) / max(old_result, 1e-10)
        assert relative_error < 0.1, f"向后兼容性测试失败: 相对误差{relative_error:.3f}"
    
    def test_backward_compatibility_interface(self):
        """测试向后兼容的接口调用"""
        calculator = KeyRateCalculator()
        
        # 确保旧接口仍然可用
        assert hasattr(calculator, 'compute'), "compute方法必须保留"
        assert hasattr(calculator, 'calculate_key_rate'), "calculate_key_rate方法必须保留"
        
        # 测试旧接口调用
        result = calculator.compute(
            qber=0.05,
            gain=0.5,
            n_pulses=100000,
            protocol_type=ProtocolType.BB84
        )
        
        assert isinstance(result, KeyRateResult), "旧接口应返回KeyRateResult对象"
        assert result.final_key_rate >= 0, "密钥率应非负"
    
    # ==================== 数值稳定性测试 ====================
    
    def test_numerical_stability_extreme_parameters(self):
        """测试极端参数下的数值稳定性"""
        calculator = KeyRateCalculator()
        
        # 极端测试用例
        extreme_cases = [
            {'qber': 1e-10, 'gain': 1e-6, 'description': '极低错误率和增益'},
            {'qber': 0.49, 'gain': 0.99, 'description': '接近阈值的高错误率'},
            {'qber': 0.1, 'gain': 1e-8, 'description': '极低增益'},
        ]
        
        security_params = UniversalSecurityParameters(epsilon_sec=1e-12)
        bb84_features = create_bb84_protocol()
        
        for case in extreme_cases:
            # 构造仿真结果
            n_detected = int(1000000 * case['gain'])
            n_errors = int(n_detected * case['qber'])
            
            simulation_results = {
                'raw_statistics': {
                    'alice_bits': [0] * n_detected,
                    'bob_bits': [0] * (n_detected - n_errors) + [1] * n_errors,
                    'alice_bases': ['Z'] * n_detected,
                    'bob_bases': ['Z'] * n_detected,
                    'detections': [True] * n_detected
                },
                'channel_statistics': {
                    'transmission_probability': case['gain'],
                    'error_probability': case['qber']
                }
            }
            
            # 计算应该不抛出异常且返回有效结果
            result = calculator.compute_universal(simulation_results, bb84_features, security_params)
            
            assert np.isfinite(result.final_key_rate), f"极端情况下数值不稳定: {case['description']}"
            assert result.final_key_rate >= 0, f"密钥率应非负: {case['description']}"
    
    # ==================== 性能测试 ====================
    
    def test_computation_performance(self):
        """测试计算性能"""
        import time
        
        calculator = KeyRateCalculator()
        
        # 大规模仿真结果
        n_pulses = 1000000
        simulation_results = {
            'raw_statistics': {
                'alice_bits': np.random.randint(0, 2, n_pulses).tolist(),
                'bob_bits': np.random.randint(0, 2, n_pulses).tolist(),
                'alice_bases': np.random.choice(['Z', 'X'], n_pulses).tolist(),
                'bob_bases': np.random.choice(['Z', 'X'], n_pulses).tolist(),
                'detections': np.random.choice([True, False], n_pulses, p=[0.5, 0.5]).tolist()
            }
        }
        
        bb84_features = create_bb84_protocol()
        security_params = UniversalSecurityParameters(epsilon_sec=1e-10)
        
        # 性能计时
        start_time = time.time()
        result = calculator.compute_universal(simulation_results, bb84_features, security_params)
        end_time = time.time()
        
        computation_time = end_time - start_time
        
        # 计算应在合理时间内完成（< 10秒）
        assert computation_time < 10.0, f"计算耗时过长: {computation_time:.2f}秒"
        assert np.isfinite(result.final_key_rate), "大规模计算结果应有效"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])