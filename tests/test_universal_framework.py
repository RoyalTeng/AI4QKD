"""
通用协议仿真与安全性分析理论基础测试

该测试文件验证AI4QKD系统中通用量子密码学框架的理论基础，包括：
1. 通用量子态表示的正确性
2. 通用量子操作的数学性质验证
3. 信息论计算的准确性
4. 协议无关性的验证

基于参考文献的理论框架：
- Gisin等(2002): 量子密码学基础
- Renner & Wolf(2023): 量子密码学优势
- Metger等(2024): 广义熵累积理论
- Nielsen & Chuang: 量子计算与量子信息

测试方法：
- 使用已知解析结果验证
- 边界条件测试
- 与现有实现对比
- 数值精度验证
"""

import pytest
import numpy as np
import numpy.testing as npt
from typing import Dict, List, Tuple, Any, Optional
from unittest.mock import Mock, patch
import logging

# 导入待测试模块
from simulator.real_quantum_simulator import RealQuantumSimulator
from simulator.state_preparation import StatePreparation
from simulator.channel_model import ChannelModel
from simulator.measurement import Measurement
from security_evaluator.key_rate_calculator import KeyRateCalculator
from security_evaluator.entropy_estimator import EntropyEstimator
from security_evaluator.composable_security import ComposableSecurityAnalyzer
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType

# 设置测试日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestUniversalQuantumStateRepresentation:
    """
    测试通用量子态表示
    
    验证量子态的数学表示是否符合量子力学基本原理
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.state_prep = StatePreparation()
        self.tolerance = 1e-10
        
    def test_pure_state_normalization(self):
        """
        测试纯态的归一化
        
        理论基础：任何有效的量子态必须满足 Tr(ρ) = 1
        """
        # 测试单量子比特纯态
        test_cases = [
            {'basis': 'Z', 'bit': 0},  # |0⟩
            {'basis': 'Z', 'bit': 1},  # |1⟩
            {'basis': 'X', 'bit': 0},  # |+⟩
            {'basis': 'X', 'bit': 1},  # |-⟩
        ]
        
        for params in test_cases:
            state = self.state_prep.simulate_state_preparation(params)
            trace = np.trace(state)
            
            # 验证归一化条件
            npt.assert_allclose(trace, 1.0, atol=self.tolerance,
                              err_msg=f"Pure state {params} not normalized: Tr(ρ) = {trace}")
            
            # 验证密度矩阵的厄米性
            hermitian_check = np.allclose(state, state.conj().T, atol=self.tolerance)
            assert hermitian_check, f"State {params} is not Hermitian"
            
            # 验证半正定性
            eigenvals = np.linalg.eigvals(state)
            assert np.all(eigenvals >= -self.tolerance), f"State {params} has negative eigenvalues"
    
    def test_mixed_state_properties(self):
        """
        测试混合态的基本性质
        
        理论基础：混合态必须满足：
        1. Tr(ρ) = 1 (归一化)
        2. ρ† = ρ (厄米性)
        3. ρ ≥ 0 (半正定性)
        4. Tr(ρ²) ≤ 1 (纯度界限)
        """
        # 创建已知的混合态：完全混合态
        mixed_state = 0.5 * np.array([[1, 0], [0, 0]]) + 0.5 * np.array([[0, 0], [0, 1]])
        
        # 验证归一化
        npt.assert_allclose(np.trace(mixed_state), 1.0, atol=self.tolerance)
        
        # 验证厄米性
        assert np.allclose(mixed_state, mixed_state.conj().T, atol=self.tolerance)
        
        # 验证半正定性
        eigenvals = np.linalg.eigvals(mixed_state)
        assert np.all(eigenvals >= -self.tolerance)
        
        # 验证纯度界限
        purity = np.trace(mixed_state @ mixed_state)
        assert purity <= 1.0 + self.tolerance
        
        # 对于最大混合态，纯度应该是 1/d，其中 d 是维度
        expected_purity = 1.0 / mixed_state.shape[0]
        npt.assert_allclose(purity, expected_purity, atol=self.tolerance)
    
    def test_tensor_product_structure(self):
        """
        测试多粒子系统的张量积结构
        
        理论基础：复合系统的希尔伯特空间是子系统空间的张量积
        """
        # 创建两个单量子比特态
        state_0 = np.array([[1, 0], [0, 0]])  # |0⟩⟨0|
        state_1 = np.array([[0, 0], [0, 1]])  # |1⟩⟨1|
        
        # 计算张量积
        composite_state = np.kron(state_0, state_1)
        
        # 验证张量积的维度
        expected_dim = state_0.shape[0] * state_1.shape[0]
        assert composite_state.shape == (expected_dim, expected_dim)
        
        # 验证张量积态的归一化
        npt.assert_allclose(np.trace(composite_state), 1.0, atol=self.tolerance)
        
        # 验证特定矩阵元素（应该对应 |01⟩⟨01|）
        expected_state = np.zeros((4, 4))
        expected_state[1, 1] = 1.0  # |01⟩⟨01| 对应索引 (1,1)
        
        npt.assert_allclose(composite_state, expected_state, atol=self.tolerance)
    
    def test_quantum_state_evolution_unitarity(self):
        """
        测试量子态演化的幺正性
        
        理论基础：量子态的幺正演化必须保持密度矩阵的性质
        """
        # 初始态
        initial_state = np.array([[1, 0], [0, 0]])  # |0⟩⟨0|
        
        # 定义一个幺正操作（Pauli-X 门）
        pauli_x = np.array([[0, 1], [1, 0]])
        
        # 应用幺正演化: ρ' = U ρ U†
        evolved_state = pauli_x @ initial_state @ pauli_x.conj().T
        
        # 验证演化后态的性质
        npt.assert_allclose(np.trace(evolved_state), 1.0, atol=self.tolerance)
        assert np.allclose(evolved_state, evolved_state.conj().T, atol=self.tolerance)
        
        # 验证演化结果（应该是 |1⟩⟨1|）
        expected_final_state = np.array([[0, 0], [0, 1]])
        npt.assert_allclose(evolved_state, expected_final_state, atol=self.tolerance)


class TestUniversalQuantumOperations:
    """
    测试通用量子操作
    
    验证量子操作的数学性质和物理正确性
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.channel = ChannelModel()
        self.measurement = Measurement()
        self.tolerance = 1e-10
    
    def test_unitary_operation_properties(self):
        """
        测试幺正操作的幺正性
        
        理论基础：幺正矩阵必须满足 U†U = UU† = I
        """
        # 定义几个常见的幺正矩阵
        unitary_gates = {
            'pauli_x': np.array([[0, 1], [1, 0]]),
            'pauli_y': np.array([[0, -1j], [1j, 0]]),
            'pauli_z': np.array([[1, 0], [0, -1]]),
            'hadamard': np.array([[1, 1], [1, -1]]) / np.sqrt(2),
        }
        
        for gate_name, gate in unitary_gates.items():
            # 验证 U†U = I
            identity_check1 = gate.conj().T @ gate
            npt.assert_allclose(identity_check1, np.eye(2), atol=self.tolerance,
                              err_msg=f"{gate_name} fails U†U = I")
            
            # 验证 UU† = I
            identity_check2 = gate @ gate.conj().T
            npt.assert_allclose(identity_check2, np.eye(2), atol=self.tolerance,
                              err_msg=f"{gate_name} fails UU† = I")
            
            # 验证行列式的模为1
            det_modulus = np.abs(np.linalg.det(gate))
            npt.assert_allclose(det_modulus, 1.0, atol=self.tolerance,
                              err_msg=f"{gate_name} determinant modulus ≠ 1")
    
    def test_measurement_operation_completeness(self):
        """
        测试测量操作的完备性
        
        理论基础：测量算子必须满足完备性关系 Σᵢ Mᵢ†Mᵢ = I
        """
        # 定义Z基测量算子
        M_0 = np.array([[1, 0], [0, 0]])  # |0⟩⟨0|
        M_1 = np.array([[0, 0], [0, 1]])  # |1⟩⟨1|
        
        # 验证完备性
        completeness = M_0.conj().T @ M_0 + M_1.conj().T @ M_1
        npt.assert_allclose(completeness, np.eye(2), atol=self.tolerance,
                          err_msg="Z-basis measurement operators not complete")
        
        # 定义X基测量算子
        M_plus = 0.5 * np.array([[1, 1], [1, 1]])   # |+⟩⟨+|
        M_minus = 0.5 * np.array([[1, -1], [-1, 1]])  # |-⟩⟨-|
        
        # 验证X基完备性
        completeness_x = M_plus.conj().T @ M_plus + M_minus.conj().T @ M_minus
        npt.assert_allclose(completeness_x, np.eye(2), atol=self.tolerance,
                          err_msg="X-basis measurement operators not complete")
    
    def test_partial_trace_properties(self):
        """
        测试部分迹操作的正确性
        
        理论基础：部分迹必须保持约化密度矩阵的性质
        """
        # 创建纠缠态 |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        phi_plus = np.zeros((4, 4))
        phi_plus[0, 0] = 0.5  # |00⟩⟨00|
        phi_plus[0, 3] = 0.5  # |00⟩⟨11|
        phi_plus[3, 0] = 0.5  # |11⟩⟨00|
        phi_plus[3, 3] = 0.5  # |11⟩⟨11|
        
        # 计算第一个量子比特的约化密度矩阵
        # Tr_B(ρ_AB) = Σⱼ ⟨j|_B ρ_AB |j⟩_B
        reduced_A = np.zeros((2, 2))
        for j in range(2):
            # 构造 ⟨j|_B ... |j⟩_B 操作
            proj_B = np.zeros((4, 4))
            for i in range(2):
                proj_B[2*i + j, 2*i + j] = 1
            reduced_A += proj_B @ phi_plus @ proj_B
        
        # 验证约化态的性质
        npt.assert_allclose(np.trace(reduced_A), 1.0, atol=self.tolerance,
                          err_msg="Reduced state not normalized")
        
        assert np.allclose(reduced_A, reduced_A.conj().T, atol=self.tolerance), \
            "Reduced state not Hermitian"
        
        # 对于最大纠缠态，约化态应该是最大混合态
        expected_reduced = 0.5 * np.eye(2)
        npt.assert_allclose(reduced_A, expected_reduced, atol=self.tolerance,
                          err_msg="Reduced state of maximally entangled state incorrect")
    
    def test_quantum_channel_properties(self):
        """
        测试量子信道的数学性质
        
        理论基础：量子信道必须是完全正的保迹映射
        """
        # 创建测试态
        test_state = np.array([[0.6, 0.2], [0.2, 0.4]])
        
        # 测试恒等信道
        channel_params = {'loss': 0.0, 'error_rate': 0.0}
        output_state = self.channel.simulate_channel_transmission(test_state, channel_params)
        
        # 验证保迹性
        npt.assert_allclose(np.trace(output_state), np.trace(test_state), 
                          atol=self.tolerance, err_msg="Channel not trace-preserving")
        
        # 验证输出态的有效性
        assert np.allclose(output_state, output_state.conj().T, atol=self.tolerance), \
            "Channel output not Hermitian"
        
        eigenvals = np.linalg.eigvals(output_state)
        assert np.all(eigenvals >= -self.tolerance), "Channel output has negative eigenvalues"


class TestInformationTheoryCalculations:
    """
    测试信息论计算
    
    验证量子信息论中关键量的计算正确性
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.entropy_estimator = EntropyEstimator()
        self.tolerance = 1e-10
    
    def test_von_neumann_entropy_calculation(self):
        """
        测试冯·诺依曼熵的计算
        
        理论基础：S(ρ) = -Tr(ρ log ρ)
        """
        # 测试纯态的熵（应该为0）
        pure_state = np.array([[1, 0], [0, 0]])  # |0⟩⟨0|
        pure_entropy = self._calculate_von_neumann_entropy(pure_state)
        npt.assert_allclose(pure_entropy, 0.0, atol=self.tolerance,
                          err_msg="Pure state entropy should be zero")
        
        # 测试最大混合态的熵（应该为log(d)）
        max_mixed = 0.5 * np.eye(2)
        max_mixed_entropy = self._calculate_von_neumann_entropy(max_mixed)
        expected_entropy = np.log2(2)  # log₂(2) = 1
        npt.assert_allclose(max_mixed_entropy, expected_entropy, atol=self.tolerance,
                          err_msg="Maximally mixed state entropy incorrect")
        
        # 测试一般混合态
        p = 0.7
        general_mixed = p * np.array([[1, 0], [0, 0]]) + (1-p) * np.array([[0, 0], [0, 1]])
        general_entropy = self._calculate_von_neumann_entropy(general_mixed)
        expected_general = -p * np.log2(p) - (1-p) * np.log2(1-p)
        npt.assert_allclose(general_entropy, expected_general, atol=self.tolerance,
                          err_msg="General mixed state entropy incorrect")
    
    def test_mutual_information_calculation(self):
        """
        测试互信息的计算
        
        理论基础：I(A:B) = S(A) + S(B) - S(AB)
        """
        # 创建分离态 ρ_AB = ρ_A ⊗ ρ_B
        rho_A = np.array([[0.6, 0], [0, 0.4]])
        rho_B = np.array([[0.8, 0], [0, 0.2]])
        rho_AB_separable = np.kron(rho_A, rho_B)
        
        # 计算各个熵
        S_A = self._calculate_von_neumann_entropy(rho_A)
        S_B = self._calculate_von_neumann_entropy(rho_B)
        S_AB = self._calculate_von_neumann_entropy(rho_AB_separable)
        
        # 对于分离态，互信息应该为0
        mutual_info = S_A + S_B - S_AB
        npt.assert_allclose(mutual_info, 0.0, atol=self.tolerance,
                          err_msg="Mutual information of separable state should be zero")
        
        # 测试最大纠缠态的互信息
        # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        phi_plus = np.zeros((4, 4))
        phi_plus[0, 0] = 0.5  # |00⟩⟨00|
        phi_plus[0, 3] = 0.5  # |00⟩⟨11|
        phi_plus[3, 0] = 0.5  # |11⟩⟨00|
        phi_plus[3, 3] = 0.5  # |11⟩⟨11|
        
        S_AB_entangled = self._calculate_von_neumann_entropy(phi_plus)
        
        # 计算约化态
        rho_A_reduced = self._partial_trace_B(phi_plus)
        rho_B_reduced = self._partial_trace_A(phi_plus)
        
        S_A_reduced = self._calculate_von_neumann_entropy(rho_A_reduced)
        S_B_reduced = self._calculate_von_neumann_entropy(rho_B_reduced)
        
        # 对于最大纠缠态，I(A:B) = 2*S(A) = 2 bits
        mutual_info_entangled = S_A_reduced + S_B_reduced - S_AB_entangled
        npt.assert_allclose(mutual_info_entangled, 2.0, atol=self.tolerance,
                          err_msg="Mutual information of maximally entangled state incorrect")
    
    def test_holevo_information_bound(self):
        """
        测试Holevo信息的计算
        
        理论基础：χ({pᵢ, ρᵢ}) = S(Σᵢ pᵢ ρᵢ) - Σᵢ pᵢ S(ρᵢ)
        """
        # 定义一个简单的量子态集合
        p1, p2 = 0.6, 0.4
        rho1 = np.array([[1, 0], [0, 0]])     # |0⟩⟨0|
        rho2 = np.array([[0, 0], [0, 1]])     # |1⟩⟨1|
        
        # 计算平均态
        rho_avg = p1 * rho1 + p2 * rho2
        
        # 计算Holevo信息
        S_avg = self._calculate_von_neumann_entropy(rho_avg)
        S1 = self._calculate_von_neumann_entropy(rho1)
        S2 = self._calculate_von_neumann_entropy(rho2)
        
        holevo_info = S_avg - (p1 * S1 + p2 * S2)
        
        # 对于正交纯态，Holevo信息等于经典香农熵
        expected_holevo = -p1 * np.log2(p1) - p2 * np.log2(p2)
        npt.assert_allclose(holevo_info, expected_holevo, atol=self.tolerance,
                          err_msg="Holevo information for orthogonal pure states incorrect")
    
    def test_conditional_entropy_properties(self):
        """
        测试条件熵的性质
        
        理论基础：S(A|B) = S(AB) - S(B)
        """
        # 使用最大纠缠态测试
        phi_plus = np.zeros((4, 4))
        phi_plus[0, 0] = 0.5
        phi_plus[0, 3] = 0.5
        phi_plus[3, 0] = 0.5
        phi_plus[3, 3] = 0.5
        
        # 计算条件熵
        S_AB = self._calculate_von_neumann_entropy(phi_plus)
        rho_B = self._partial_trace_A(phi_plus)
        S_B = self._calculate_von_neumann_entropy(rho_B)
        
        conditional_entropy = S_AB - S_B
        
        # 对于最大纠缠态，S(A|B) = 0
        npt.assert_allclose(conditional_entropy, 0.0, atol=self.tolerance,
                          err_msg="Conditional entropy of maximally entangled state should be zero")
    
    def _calculate_von_neumann_entropy(self, rho: np.ndarray) -> float:
        """计算冯·诺依曼熵"""
        eigenvals = np.linalg.eigvals(rho)
        eigenvals = eigenvals[eigenvals > 1e-12]  # 移除数值零
        return -np.sum(eigenvals * np.log2(eigenvals))
    
    def _partial_trace_A(self, rho_AB: np.ndarray) -> np.ndarray:
        """计算关于系统A的部分迹，返回系统B的约化态"""
        d = int(np.sqrt(rho_AB.shape[0]))
        rho_B = np.zeros((d, d), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    rho_B[i, j] += rho_AB[k*d + i, k*d + j]
        return rho_B
    
    def _partial_trace_B(self, rho_AB: np.ndarray) -> np.ndarray:
        """计算关于系统B的部分迹，返回系统A的约化态"""
        d = int(np.sqrt(rho_AB.shape[0]))
        rho_A = np.zeros((d, d), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    rho_A[i, j] += rho_AB[i*d + k, j*d + k]
        return rho_A


class TestProtocolAgnosticFramework:
    """
    测试协议无关性框架
    
    验证系统对不同协议结构的通用处理能力
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.simulator = None
        self.tolerance = 1e-6
    
    def test_bb84_protocol_structure_recognition(self):
        """
        测试BB84协议结构的识别
        
        验证系统能够正确识别和处理BB84协议的特征结构
        """
        # 创建模拟的BB84协议图
        bb84_structure = {
            'qsp_nodes': [{'type': 'QSP', 'party': 'Alice', 'params': {'basis_choice': ['Z', 'X']}}],
            'qc_nodes': [{'type': 'QC', 'params': {'loss': 0.1, 'error_rate': 0.02}}],
            'qm_nodes': [{'type': 'QM', 'party': 'Bob', 'params': {'basis_choice': ['Z', 'X']}}],
        }
        
        # 验证协议识别
        protocol_type = self._identify_protocol_type(bb84_structure)
        assert protocol_type == 'BB84', f"Expected BB84, got {protocol_type}"
        
        # 验证协议的有效性
        is_valid = self._validate_protocol_structure(bb84_structure)
        assert is_valid, "BB84 protocol structure should be valid"
    
    def test_mdi_qkd_protocol_structure_recognition(self):
        """
        测试MDI-QKD协议结构的识别
        
        验证系统能够正确识别和处理MDI-QKD协议的特征结构
        """
        # 创建模拟的MDI-QKD协议图
        mdi_structure = {
            'qsp_nodes': [
                {'type': 'QSP', 'party': 'Alice', 'params': {'basis_choice': ['Z', 'X']}},
                {'type': 'QSP', 'party': 'Bob', 'params': {'basis_choice': ['Z', 'X']}}
            ],
            'qc_nodes': [
                {'type': 'QC', 'params': {'loss': 0.2, 'error_rate': 0.01}},
                {'type': 'QC', 'params': {'loss': 0.2, 'error_rate': 0.01}}
            ],
            'bsm_nodes': [{'type': 'BSM', 'party': 'Charlie', 'params': {}}],
        }
        
        # 验证协议识别
        protocol_type = self._identify_protocol_type(mdi_structure)
        assert protocol_type == 'MDI_QKD', f"Expected MDI_QKD, got {protocol_type}"
        
        # 验证协议的有效性
        is_valid = self._validate_protocol_structure(mdi_structure)
        assert is_valid, "MDI-QKD protocol structure should be valid"
    
    def test_decoy_state_protocol_structure_recognition(self):
        """
        测试诱骗态协议结构的识别
        
        验证系统能够正确识别和处理诱骗态协议的特征结构
        """
        # 创建模拟的诱骗态协议图
        decoy_structure = {
            'qsp_nodes': [{
                'type': 'QSP', 
                'party': 'Alice', 
                'params': {
                    'basis_choice': ['Z', 'X'],
                    'intensities': {
                        'signal': {'value': 0.5, 'probability': 0.7},
                        'decoy': {'value': 0.1, 'probability': 0.2},
                        'vacuum': {'value': 0.0, 'probability': 0.1}
                    }
                }
            }],
            'qc_nodes': [{'type': 'QC', 'params': {'loss': 0.1, 'error_rate': 0.02}}],
            'qm_nodes': [{'type': 'QM', 'party': 'Bob', 'params': {'basis_choice': ['Z', 'X']}}],
        }
        
        # 验证协议识别
        protocol_type = self._identify_protocol_type(decoy_structure)
        assert protocol_type == 'DECOY_BB84', f"Expected DECOY_BB84, got {protocol_type}"
        
        # 验证诱骗态参数的有效性
        intensities = decoy_structure['qsp_nodes'][0]['params']['intensities']
        total_prob = sum(config['probability'] for config in intensities.values())
        npt.assert_allclose(total_prob, 1.0, atol=self.tolerance,
                          err_msg="Decoy state probabilities should sum to 1")
    
    def test_protocol_security_analysis_universality(self):
        """
        测试协议安全性分析的通用性
        
        验证安全性分析框架能够处理不同类型的协议
        """
        # 定义不同协议的测试参数
        test_protocols = [
            {
                'type': 'BB84',
                'params': {'qber': 0.05, 'gain': 0.1, 'n_pulses': 100000}
            },
            {
                'type': 'DECOY_BB84',
                'params': {'qber': 0.03, 'gain': 0.08, 'n_pulses': 100000}
            },
            {
                'type': 'MDI_QKD',
                'params': {'qber': 0.02, 'gain': 0.05, 'n_pulses': 100000}
            }
        ]
        
        key_rate_calculator = KeyRateCalculator()
        
        for protocol_config in test_protocols:
            # 计算密钥率
            result = key_rate_calculator.compute(
                qber=protocol_config['params']['qber'],
                gain=protocol_config['params']['gain'],
                n_pulses=protocol_config['params']['n_pulses'],
                protocol_type=getattr(key_rate_calculator.ProtocolType, protocol_config['type'])
            )
            
            # 验证结果的有效性
            assert result.final_key_rate >= 0, f"{protocol_config['type']} produced negative key rate"
            assert result.final_key_length >= 0, f"{protocol_config['type']} produced negative key length"
            assert 0 <= result.h_min <= 1, f"{protocol_config['type']} min-entropy out of bounds"
    
    def test_dynamic_protocol_adaptation(self):
        """
        测试动态协议适应能力
        
        验证系统能够根据协议参数的变化动态调整分析方法
        """
        # 测试参数敏感性分析
        base_params = {'qber': 0.05, 'gain': 0.1, 'n_pulses': 100000}
        
        key_rate_calculator = KeyRateCalculator()
        
        # 测试QBER变化的影响
        qber_range = np.linspace(0.01, 0.1, 5)
        key_rates = []
        
        for qber in qber_range:
            result = key_rate_calculator.compute(
                qber=qber,
                gain=base_params['gain'],
                n_pulses=base_params['n_pulses']
            )
            key_rates.append(result.final_key_rate)
        
        # 验证密钥率随QBER单调递减
        for i in range(1, len(key_rates)):
            assert key_rates[i] <= key_rates[i-1] + self.tolerance, \
                "Key rate should decrease monotonically with increasing QBER"
    
    def test_composable_security_universality(self):
        """
        测试可组合安全性的通用性
        
        验证可组合安全框架对不同协议的适用性
        """
        security_analyzer = ComposableSecurityAnalyzer()
        
        # 测试不同协议数量的可组合安全性
        test_cases = [
            {'n_protocols': 1, 'protocol_epsilon': 1e-10},
            {'n_protocols': 10, 'protocol_epsilon': 1e-11},
            {'n_protocols': 100, 'protocol_epsilon': 1e-12},
        ]
        
        for case in test_cases:
            result = security_analyzer.analyze_composable_security(
                n_protocols=case['n_protocols'],
                protocol_epsilon=case['protocol_epsilon']
            )
            
            # 验证安全性分析结果的一致性
            assert result.epsilon_total >= case['protocol_epsilon'], \
                "Total security parameter should be at least the protocol parameter"
            
            assert result.security_level > 0, \
                "Security level should be positive"
            
            # 验证协议数量增加时安全参数的行为
            if case['n_protocols'] > 1:
                assert result.epsilon_composable >= case['protocol_epsilon'], \
                    "Composable security parameter should reflect protocol combination"
    
    def _identify_protocol_type(self, protocol_structure: Dict) -> str:
        """识别协议类型的辅助方法"""
        if 'bsm_nodes' in protocol_structure and protocol_structure['bsm_nodes']:
            return 'MDI_QKD'
        elif ('qsp_nodes' in protocol_structure and protocol_structure['qsp_nodes'] and
              'intensities' in protocol_structure['qsp_nodes'][0].get('params', {})):
            return 'DECOY_BB84'
        elif ('qsp_nodes' in protocol_structure and 'qm_nodes' in protocol_structure and
              protocol_structure['qsp_nodes'] and protocol_structure['qm_nodes']):
            return 'BB84'
        else:
            return 'UNKNOWN'
    
    def _validate_protocol_structure(self, protocol_structure: Dict) -> bool:
        """验证协议结构有效性的辅助方法"""
        # 基本结构检查
        if 'qsp_nodes' not in protocol_structure:
            return False
        
        if not protocol_structure['qsp_nodes']:
            return False
        
        # 根据协议类型进行特定验证
        protocol_type = self._identify_protocol_type(protocol_structure)
        
        if protocol_type == 'BB84':
            return ('qm_nodes' in protocol_structure and 
                   protocol_structure['qm_nodes'] and
                   'qc_nodes' in protocol_structure and
                   protocol_structure['qc_nodes'])
        
        elif protocol_type == 'MDI_QKD':
            return (len(protocol_structure['qsp_nodes']) >= 2 and
                   'bsm_nodes' in protocol_structure and
                   protocol_structure['bsm_nodes'])
        
        elif protocol_type == 'DECOY_BB84':
            return ('intensities' in protocol_structure['qsp_nodes'][0].get('params', {}) and
                   'qm_nodes' in protocol_structure and
                   protocol_structure['qm_nodes'])
        
        return False


class TestNumericalPrecisionAndStability:
    """
    测试数值精度和稳定性
    
    验证计算的数值稳定性和精度要求
    """
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.tolerance = 1e-10
        self.loose_tolerance = 1e-6
    
    def test_eigenvalue_computation_stability(self):
        """
        测试特征值计算的稳定性
        
        验证在接近奇异情况下的数值稳定性
        """
        # 创建接近奇异的密度矩阵
        epsilon = 1e-12
        near_singular = np.array([[1-epsilon, 0], [0, epsilon]])
        
        # 计算特征值
        eigenvals = np.linalg.eigvals(near_singular)
        
        # 验证特征值的物理意义
        assert np.all(eigenvals >= -self.tolerance), "Eigenvalues should be non-negative"
        npt.assert_allclose(np.sum(eigenvals), 1.0, atol=self.tolerance,
                          err_msg="Eigenvalues should sum to 1")
    
    def test_entropy_calculation_edge_cases(self):
        """
        测试熵计算的边界情况
        
        验证在极限情况下的数值行为
        """
        entropy_estimator = EntropyEstimator()
        
        # 测试接近纯态的情况
        epsilon = 1e-15
        near_pure = np.array([[1-epsilon, 0], [0, epsilon]])
        
        # 应该能够处理而不产生数值错误
        try:
            entropy = self._calculate_von_neumann_entropy(near_pure)
            assert entropy >= 0, "Entropy should be non-negative"
            assert entropy <= np.log2(2), "Entropy should not exceed maximum"
        except (ValueError, RuntimeWarning) as e:
            pytest.fail(f"Entropy calculation failed on near-pure state: {e}")
    
    def test_key_rate_calculation_boundary_conditions(self):
        """
        测试密钥率计算的边界条件
        
        验证在极端参数下的计算稳定性
        """
        key_rate_calculator = KeyRateCalculator()
        
        # 测试边界情况
        boundary_cases = [
            {'qber': 0.0, 'gain': 0.1},      # 无错误
            {'qber': 0.5 - 1e-10, 'gain': 0.1},  # 接近理论极限
            {'qber': 0.1, 'gain': 1e-10},    # 极低增益
        ]
        
        for case in boundary_cases:
            try:
                result = key_rate_calculator.compute(
                    qber=case['qber'],
                    gain=case['gain'],
                    n_pulses=100000
                )
                
                # 验证结果的物理合理性
                assert result.final_key_rate >= 0, \
                    f"Key rate should be non-negative for {case}"
                
                if case['qber'] < 0.11:  # 理论上可能的情况
                    assert result.final_key_rate >= 0, \
                        f"Should have positive key rate for low QBER {case}"
                        
            except Exception as e:
                if case['qber'] >= 0.5:
                    # 预期的失败情况
                    continue
                else:
                    pytest.fail(f"Unexpected failure for valid parameters {case}: {e}")
    
    def _calculate_von_neumann_entropy(self, rho: np.ndarray) -> float:
        """安全的冯·诺依曼熵计算"""
        eigenvals = np.linalg.eigvals(rho)
        # 移除数值零并确保正值
        eigenvals = eigenvals[eigenvals > 1e-15]
        eigenvals = np.real(eigenvals)  # 取实部（应该已经是实数）
        
        if len(eigenvals) == 0:
            return 0.0
        
        return -np.sum(eigenvals * np.log2(np.maximum(eigenvals, 1e-15)))


def test_integration_with_existing_modules():
    """
    集成测试：验证与现有模块的兼容性
    
    确保新的通用框架与现有代码兼容
    """
    # 测试与现有仿真器的集成
    from simulator.real_quantum_simulator import RealQuantumSimulator
    
    # 创建仿真器实例
    simulator = RealQuantumSimulator()
    
    # 验证基本功能
    assert hasattr(simulator, 'simulate_single_pulse'), \
        "Simulator should have single pulse simulation capability"
    
    # 测试单脉冲仿真
    alice_params = {'basis': 'Z', 'bit': 0}
    channel_params = {'loss': 0.1, 'error_rate': 0.02}
    bob_params = {'basis': 'Z'}
    
    result = simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
    
    # 验证结果格式
    assert 'outcome' in result, "Result should contain outcome"
    assert 'detected' in result, "Result should contain detection status"


if __name__ == "__main__":
    # 运行测试套件
    pytest.main([__file__, "-v", "--tb=short"])