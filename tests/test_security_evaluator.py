import pytest
from security_evaluator import (
    KeyRateCalculator,
    KeyRateParameters,
    ProtocolType,
    SecurityParameters,
    EntropyEstimator,
    FiniteKeyAnalyzer,
    ComposableSecurityAnalyzer,
)
import numpy as np

@pytest.fixture
def security_params():
    return SecurityParameters(epsilon_sec=1e-9, epsilon_cor=1e-15, epsilon_rob=1e-9, epsilon_pe=1e-10)

class TestKeyRateCalculator:
    def test_bb84_key_rate(self, security_params):
        calculator = KeyRateCalculator()
        params = KeyRateParameters(
            qber=0.02,
            gain=0.9,
            n_pulses=10**12,
            security_params=security_params
        )
        result = calculator._compute_bb84_key_rate(params)
        assert result.final_key_rate > 0

    def test_decoy_bb84_key_rate(self, security_params):
        calculator = KeyRateCalculator()
        params = KeyRateParameters(
            qber=0.02,
            gain=0.9,
            n_pulses=10**12,
            security_params=security_params,
            mu_signal=0.5,
            mu_decoy1=0.1,
            p_signal=0.8,
            p_decoy1=0.2,
        )
        result = calculator._compute_decoy_bb84_key_rate(params)
        assert result.final_key_rate > 0
        
    def test_invalid_qber(self):
        calculator = KeyRateCalculator()
        with pytest.raises(ValueError):
            calculator.compute(qber=0.6, gain=0.9, n_pulses=10**12)

class TestEntropyEstimator:
    def test_min_entropy(self):
        estimator = EntropyEstimator()
        result = estimator.calculate_min_entropy(qber=0.02)
        assert result.value > 0
        assert result.entropy_type == "min_entropy"

    def test_conditional_entropy(self):
        estimator = EntropyEstimator()
        joint_dist = np.array([[0.4, 0.1], [0.1, 0.4]])
        result = estimator.calculate_conditional_entropy(joint_dist)
        assert result.value >= 0

class TestFiniteKeyAnalyzer:
    def test_finite_key_analysis(self):
        analyzer = FiniteKeyAnalyzer()
        result = analyzer.analyze_finite_key_effects(n_raw=10**12, qber=0.02)
        assert result.secret_key_rate >= 0
        assert result.n_final >= 0

class TestComposableSecurity:
    def test_composable_analysis(self):
        analyzer = ComposableSecurityAnalyzer()
        result = analyzer.analyze_composable_security(
            n_protocols=2, protocol_epsilon=1e-10, epsilon_sec=1e-8
        )
        assert result.is_composable_secure is True
        assert result.epsilon_total > 0 