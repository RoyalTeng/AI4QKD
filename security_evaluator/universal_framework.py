"""
通用抽象密码学（Universal Abstract Cryptography）框架模块

基于量子信息论的通用安全性分析框架，支持任意QKD协议的安全性评估。
该模块实现了现代量子密码学的理论基础，包括：

- 通用量子操作表示
- 协议信息论特征分析  
- 熵累积理论应用
- 可组合安全性分析
- 设备无关安全性评估

理论基础：
- Renner & Wolf (2023): Quantum Advantage in Cryptography
- Metger et al. (2024): Generalised Entropy Accumulation
- Nielsen & Chuang: Quantum Computation and Quantum Information
- Gisin et al. (2002): Quantum Cryptography

作者：AI4QKD Team
版本：2.0 - Universal Framework
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import warnings

# 设置日志
logger = logging.getLogger(__name__)


# ==================== 量子操作相关类 ====================

class QuantumOperationType(Enum):
    """量子操作类型枚举"""
    UNITARY = "unitary"           # 幺正操作
    MEASUREMENT = "measurement"   # 测量操作
    CHANNEL = "channel"           # 量子信道
    PREPARATION = "preparation"   # 态准备
    CLASSICAL = "classical"       # 经典操作


@dataclass
class QuantumOperation:
    """
    通用量子操作类
    
    表示任意量子操作，包括幺正变换、测量、量子信道等。
    基于量子操作的数学表示提供统一接口。
    """
    name: str
    operation_type: Union[QuantumOperationType, str]
    matrix: Optional[Union[np.ndarray, List[np.ndarray]]] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    dimension: Optional[int] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 转换字符串类型为枚举
        if isinstance(self.operation_type, str):
            try:
                self.operation_type = QuantumOperationType(self.operation_type)
            except ValueError:
                logger.warning(f"Unknown operation type: {self.operation_type}")
        
        # 推断维度
        if self.matrix is not None and self.dimension is None:
            if isinstance(self.matrix, np.ndarray):
                self.dimension = self.matrix.shape[0]
            elif isinstance(self.matrix, list) and len(self.matrix) > 0:
                self.dimension = self.matrix[0].shape[0]
    
    def is_unitary(self, tolerance: float = 1e-10) -> bool:
        """
        检查操作是否为幺正操作
        
        验证条件：U†U = UU† = I
        """
        if self.operation_type != QuantumOperationType.UNITARY:
            return False
            
        if not isinstance(self.matrix, np.ndarray):
            return False
        
        U = self.matrix
        U_dag = U.conj().T
        
        # 检查 U†U = I
        product1 = U_dag @ U
        identity_check1 = np.allclose(product1, np.eye(U.shape[0]), atol=tolerance)
        
        # 检查 UU† = I
        product2 = U @ U_dag
        identity_check2 = np.allclose(product2, np.eye(U.shape[0]), atol=tolerance)
        
        return identity_check1 and identity_check2
    
    def is_valid_povm(self, tolerance: float = 1e-10) -> bool:
        """
        检查是否为有效的POVM（正算子值测量）
        
        验证条件：
        1. 每个算子都是半正定的
        2. 完备性：Σᵢ Mᵢ = I
        """
        if self.operation_type != QuantumOperationType.MEASUREMENT:
            return False
            
        if not isinstance(self.matrix, list):
            return False
        
        # 检查每个算子的半正定性
        for M in self.matrix:
            eigenvals = np.linalg.eigvals(M)
            if not np.all(eigenvals >= -tolerance):
                return False
        
        # 检查完备性
        total = sum(self.matrix)
        expected_identity = np.eye(self.matrix[0].shape[0])
        
        return np.allclose(total, expected_identity, atol=tolerance)
    
    def is_valid_channel(self, tolerance: float = 1e-10) -> bool:
        """
        检查是否为有效的量子信道
        
        验证条件：Σᵢ Kᵢ†Kᵢ = I（Kraus算子完备性）
        """
        if self.operation_type != QuantumOperationType.CHANNEL:
            return False
            
        if not isinstance(self.matrix, list):
            return False
        
        # 检查Kraus算子完备性
        total = sum(K.conj().T @ K for K in self.matrix)
        expected_identity = np.eye(self.matrix[0].shape[0])
        
        return np.allclose(total, expected_identity, atol=tolerance)
    
    def compose(self, other: 'QuantumOperation') -> 'QuantumOperation':
        """
        与另一个量子操作组合
        
        对于幺正操作：返回矩阵乘积
        对于其他操作：根据操作类型确定组合规则
        """
        if (self.operation_type == QuantumOperationType.UNITARY and 
            other.operation_type == QuantumOperationType.UNITARY):
            
            # 幺正操作的组合
            composed_matrix = self.matrix @ other.matrix
            return QuantumOperation(
                name=f"({self.name} ∘ {other.name})",
                operation_type=QuantumOperationType.UNITARY,
                matrix=composed_matrix,
                parameters={**other.parameters, **self.parameters}
            )
        else:
            raise NotImplementedError(
                f"Composition not implemented for {self.operation_type} and {other.operation_type}"
            )
    
    def apply_to_state(self, state: np.ndarray) -> Union[np.ndarray, List[Tuple[float, np.ndarray]]]:
        """
        将操作应用到量子态
        
        Args:
            state: 输入密度矩阵
            
        Returns:
            对于幺正操作：输出密度矩阵
            对于测量：(概率, 后验态) 的列表
            对于信道：输出密度矩阵
        """
        if self.operation_type == QuantumOperationType.UNITARY:
            U = self.matrix
            return U @ state @ U.conj().T
        
        elif self.operation_type == QuantumOperationType.MEASUREMENT:
            results = []
            for i, M in enumerate(self.matrix):
                prob = np.real(np.trace(M @ state))
                if prob > 1e-12:  # 避免数值零
                    post_state = (M @ state @ M.conj().T) / prob
                    results.append((prob, post_state))
                else:
                    results.append((0.0, None))
            return results
        
        elif self.operation_type == QuantumOperationType.CHANNEL:
            output_state = sum(K @ state @ K.conj().T for K in self.matrix)
            return output_state
        
        else:
            raise NotImplementedError(f"State application not implemented for {self.operation_type}")


# ==================== 协议特征相关类 ====================

@dataclass 
class ProtocolFeatures:
    """
    协议信息论特征类
    
    描述任意QKD协议的信息论特征和结构特性，
    用于通用安全性分析。
    """
    name: str
    operations: List[QuantumOperation]
    parties: List[str]
    communication_rounds: int = 1
    measurement_bases: int = 2
    
    # 可选的协议特性
    trusted_parties: Optional[List[str]] = None
    untrusted_parties: Optional[List[str]] = None
    intensity_settings: Optional[int] = None
    decoy_states: Optional[bool] = None
    device_independence: Optional[bool] = None
    
    # 信息论参数
    classical_capacity: Optional[float] = None
    quantum_capacity: Optional[float] = None
    private_capacity: Optional[float] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.trusted_parties is None:
            self.trusted_parties = self.parties.copy()
        if self.untrusted_parties is None:
            self.untrusted_parties = []
    
    def calculate_information_theoretic_features(self) -> Dict[str, Any]:
        """
        计算协议的信息论特征
        
        Returns:
            包含各种信息论度量的字典
        """
        features = {}
        
        # 基本容量界限
        features['max_classical_capacity'] = np.log2(self.measurement_bases)
        features['quantum_capacity'] = self._estimate_quantum_capacity()
        features['private_capacity'] = self._estimate_private_capacity()
        
        # 协议复杂度度量
        features['operation_complexity'] = len(self.operations)
        features['party_complexity'] = len(self.parties)
        features['round_complexity'] = self.communication_rounds
        
        # 安全性特征
        features['measurement_device_independence'] = len(self.untrusted_parties) > 0
        features['uses_decoy_states'] = self.decoy_states or False
        features['device_independence'] = self.device_independence or False
        
        # 协议分类
        features['protocol_class'] = self._classify_protocol()
        
        return features
    
    def _estimate_quantum_capacity(self) -> float:
        """估计量子容量"""
        # 简化估计：基于测量基数和操作复杂度
        base_capacity = np.log2(self.measurement_bases)
        complexity_factor = 1.0 / (1.0 + len(self.operations) * 0.1)
        return base_capacity * complexity_factor
    
    def _estimate_private_capacity(self) -> float:
        """估计私密容量"""
        # 简化估计：考虑不可信方的影响
        quantum_cap = self._estimate_quantum_capacity()
        trust_factor = len(self.trusted_parties) / len(self.parties)
        return quantum_cap * trust_factor
    
    def _classify_protocol(self) -> str:
        """协议分类"""
        if len(self.untrusted_parties) > 0:
            if any("measurement" in op.name.lower() for op in self.operations 
                   if hasattr(op, 'name')):
                return "MDI_QKD"
            else:
                return "RELAY_QKD"
        elif self.decoy_states:
            return "DECOY_STATE_QKD"
        elif self.device_independence:
            return "DEVICE_INDEPENDENT_QKD"
        else:
            return "STANDARD_QKD"
    
    def calculate_von_neumann_entropy(self, rho: np.ndarray) -> float:
        """
        计算冯·诺依曼熵 S(ρ) = -Tr(ρ log ρ)
        
        Args:
            rho: 密度矩阵
            
        Returns:
            冯·诺依曼熵
        """
        eigenvals = np.linalg.eigvals(rho)
        eigenvals = eigenvals[eigenvals > 1e-12]  # 移除数值零
        eigenvals = np.real(eigenvals)  # 确保实数
        
        if len(eigenvals) == 0:
            return 0.0
        
        return -np.sum(eigenvals * np.log2(eigenvals))
    
    def calculate_mutual_information(self, rho_AB: np.ndarray) -> float:
        """
        计算互信息 I(A:B) = S(A) + S(B) - S(AB)
        
        Args:
            rho_AB: 双体系统的密度矩阵
            
        Returns:
            互信息
        """
        # 计算约化密度矩阵
        d = int(np.sqrt(rho_AB.shape[0]))
        
        # 部分迹计算
        rho_A = self._partial_trace_B(rho_AB, d)
        rho_B = self._partial_trace_A(rho_AB, d)
        
        # 计算各个熵
        S_A = self.calculate_von_neumann_entropy(rho_A)
        S_B = self.calculate_von_neumann_entropy(rho_B)
        S_AB = self.calculate_von_neumann_entropy(rho_AB)
        
        return S_A + S_B - S_AB
    
    def _partial_trace_A(self, rho_AB: np.ndarray, dim: int) -> np.ndarray:
        """计算关于系统A的部分迹"""
        rho_B = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                for k in range(dim):
                    rho_B[i, j] += rho_AB[k*dim + i, k*dim + j]
        return rho_B
    
    def _partial_trace_B(self, rho_AB: np.ndarray, dim: int) -> np.ndarray:
        """计算关于系统B的部分迹"""
        rho_A = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                for k in range(dim):
                    rho_A[i, j] += rho_AB[i*dim + k, j*dim + k]
        return rho_A
    
    def compare_with(self, other: 'ProtocolFeatures') -> Dict[str, Any]:
        """
        与另一个协议进行比较
        
        Args:
            other: 另一个协议特征
            
        Returns:
            比较结果字典
        """
        comparison = {}
        
        # 复杂度比较
        complexity_diff = (
            len(other.operations) - len(self.operations) +
            len(other.parties) - len(self.parties) +
            other.communication_rounds - self.communication_rounds
        )
        comparison['complexity_difference'] = complexity_diff
        
        # 安全性增强比较
        security_enhancement = 0
        if other.decoy_states and not self.decoy_states:
            security_enhancement += 1
        if other.device_independence and not self.device_independence:
            security_enhancement += 2
        if len(other.untrusted_parties) < len(self.untrusted_parties):
            security_enhancement += 1
            
        comparison['security_enhancement'] = security_enhancement
        
        # 容量比较
        self_features = self.calculate_information_theoretic_features()
        other_features = other.calculate_information_theoretic_features()
        
        comparison['capacity_ratio'] = (
            other_features['private_capacity'] / self_features['private_capacity']
            if self_features['private_capacity'] > 0 else float('inf')
        )
        
        return comparison


# ==================== 通用安全参数类 ====================

@dataclass
class UniversalSecurityParameters:
    """
    通用安全参数类
    
    基于现代量子密码学理论的安全参数，支持：
    - 可组合安全性
    - 熵累积理论
    - 有限密钥分析
    - 设备无关安全性
    """
    # 基础安全参数（保持向后兼容）
    epsilon_sec: float = 1e-9    # 安全性参数
    epsilon_cor: float = 1e-15   # 正确性参数
    epsilon_rob: float = 1e-9    # 鲁棒性参数
    epsilon_pe: float = 1e-10    # 参数估计参数
    epsilon_bar: float = 1e-10   # 最小熵平滑参数
    
    # 通用安全参数
    entropy_smoothing_param: float = 1e-8     # 熵平滑参数
    composability_param: float = 1e-7         # 可组合性参数
    device_independence_param: float = 1e-6   # 设备无关参数
    finite_key_param: float = 1e-9           # 有限密钥参数
    
    # 高级安全参数
    bell_violation_param: float = 1e-5        # Bell不等式违反参数
    measurement_device_param: float = 1e-8    # 测量设备参数
    basis_reconciliation_param: float = 1e-10 # 基选择调和参数
    
    def get_total_privacy_error(self) -> float:
        """计算总的隐私错误预算（向后兼容）"""
        return self.epsilon_sec + self.epsilon_pe + self.entropy_smoothing_param
    
    def get_total_failure_prob(self) -> float:
        """计算总的协议失败概率（向后兼容）"""
        return self.epsilon_cor + self.epsilon_rob + self.finite_key_param
    
    def get_composability_bound(self, n_protocols: int) -> float:
        """
        计算可组合安全界限
        
        Args:
            n_protocols: 协议实例数量
            
        Returns:
            可组合安全界限
        """
        # 基于通用可组合性理论的界限
        return self.composability_param * np.sqrt(n_protocols)
    
    def calculate_information_theoretic_bounds(self, 
                                             min_entropy: float,
                                             mutual_information: float,
                                             protocol_rounds: int) -> Dict[str, float]:
        """
        计算信息论界限
        
        Args:
            min_entropy: 最小熵
            mutual_information: 互信息
            protocol_rounds: 协议轮数
            
        Returns:
            各种信息论界限
        """
        bounds = {}
        
        # 隐私放大界限
        bounds['privacy_amplification_bound'] = (
            min_entropy - mutual_information - 
            np.sqrt(np.log(1/self.epsilon_sec) / (2 * protocol_rounds))
        )
        
        # 纠错界限
        bounds['error_correction_bound'] = (
            mutual_information + 
            np.sqrt(np.log(1/self.epsilon_cor) / (2 * protocol_rounds))
        )
        
        # 有限密钥界限
        bounds['finite_key_bound'] = (
            min_entropy - 
            np.sqrt(np.log(1/self.finite_key_param) * protocol_rounds)
        )
        
        # 熵平滑界限
        bounds['smoothed_entropy_bound'] = (
            min_entropy - np.log2(1/self.entropy_smoothing_param)
        )
        
        return bounds
    
    def adapt_for_protocol(self, protocol_type: str) -> 'UniversalSecurityParameters':
        """
        为特定协议类型适应参数
        
        Args:
            protocol_type: 协议类型
            
        Returns:
            适应后的安全参数
        """
        adapted_params = UniversalSecurityParameters(
            epsilon_sec=self.epsilon_sec,
            epsilon_cor=self.epsilon_cor,
            epsilon_rob=self.epsilon_rob,
            epsilon_pe=self.epsilon_pe,
            epsilon_bar=self.epsilon_bar,
            entropy_smoothing_param=self.entropy_smoothing_param,
            composability_param=self.composability_param,
            device_independence_param=self.device_independence_param,
            finite_key_param=self.finite_key_param
        )
        
        # 根据协议类型调整参数
        if protocol_type.upper() == 'BB84':
            adapted_params.basis_reconciliation_param = 1e-10
            
        elif protocol_type.upper() == 'MDI_QKD':
            adapted_params.measurement_device_param = 1e-8
            adapted_params.device_independence_param = 1e-7
            
        elif protocol_type.upper() == 'DEVICE_INDEPENDENT':
            adapted_params.bell_violation_param = 1e-5
            adapted_params.device_independence_param = 1e-6
            
        return adapted_params


# ==================== 通用安全框架类 ====================

class UniversalSecurityFramework:
    """
    通用安全性分析框架
    
    基于现代量子密码学理论的通用安全性分析，支持：
    - 任意协议结构的安全性分析
    - 熵累积定理应用
    - 可组合安全性分析
    - 设备无关安全性评估
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化通用安全框架
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.UniversalSecurityFramework")
        
        # 初始化子组件
        self.entropy_estimator = self._init_entropy_estimator()
        self.composability_analyzer = self._init_composability_analyzer()
        self.finite_key_analyzer = self._init_finite_key_analyzer()
        
    def _init_entropy_estimator(self):
        """初始化熵估计器"""
        # 这里会集成真正的熵估计器
        return None
    
    def _init_composability_analyzer(self):
        """初始化可组合性分析器"""
        # 这里会集成可组合安全性分析器
        return None
    
    def _init_finite_key_analyzer(self):
        """初始化有限密钥分析器"""
        # 这里会集成有限密钥分析器
        return None
    
    def analyze_protocol_security(self, 
                                protocol_features: ProtocolFeatures,
                                experimental_data: Dict[str, Any],
                                security_params: Optional[UniversalSecurityParameters] = None) -> Dict[str, Any]:
        """
        协议无关的安全性分析
        
        Args:
            protocol_features: 协议信息论特征
            experimental_data: 实验数据
            security_params: 安全参数
            
        Returns:
            安全性分析结果
        """
        if security_params is None:
            security_params = UniversalSecurityParameters()
        
        self.logger.info(f"开始分析协议 {protocol_features.name} 的安全性")
        
        result = {}
        
        # 1. 基础信息论分析
        info_theory_result = self._analyze_information_theory(
            protocol_features, experimental_data
        )
        result.update(info_theory_result)
        
        # 2. 熵估计和累积
        entropy_result = self._estimate_entropy(
            experimental_data, security_params
        )
        result.update(entropy_result)
        
        # 3. 密钥率计算
        key_rate_result = self._calculate_universal_key_rate(
            info_theory_result, entropy_result, security_params
        )
        result.update(key_rate_result)
        
        # 4. 有限密钥分析
        finite_key_result = self._analyze_finite_key_effects(
            experimental_data, security_params
        )
        result.update(finite_key_result)
        
        self.logger.info(f"安全性分析完成，密钥率: {result.get('key_rate', 0):.6f}")
        
        return result
    
    def _analyze_information_theory(self, 
                                  protocol_features: ProtocolFeatures,
                                  experimental_data: Dict[str, Any]) -> Dict[str, Any]:
        """信息论分析"""
        result = {}
        
        # 计算基础信息论量
        qber = experimental_data.get('qber', 0.0)
        gain = experimental_data.get('gain', 0.0)
        
        # 互信息估计（简化）
        if qber > 0 and qber < 0.5:
            h_qber = -qber * np.log2(qber) - (1-qber) * np.log2(1-qber) if qber < 1 else 0
            mutual_info = gain * (1 - h_qber)
        else:
            mutual_info = 0.0
        
        result['mutual_information'] = mutual_info
        result['classical_capacity'] = gain  # 简化估计
        
        # 协议特定的信息论特征
        protocol_info = protocol_features.calculate_information_theoretic_features()
        result['protocol_features'] = protocol_info
        
        return result
    
    def _estimate_entropy(self, 
                         experimental_data: Dict[str, Any],
                         security_params: UniversalSecurityParameters) -> Dict[str, Any]:
        """熵估计"""
        result = {}
        
        qber = experimental_data.get('qber', 0.0)
        
        # 最小熵估计（基于QBER的简化估计）
        if qber > 0 and qber < 0.5:
            h_qber = -qber * np.log2(qber) - (1-qber) * np.log2(1-qber)
            min_entropy = 1 - h_qber
        else:
            min_entropy = 0.0
        
        # 平滑最小熵
        smoothed_min_entropy = max(0, min_entropy - np.log2(1/security_params.entropy_smoothing_param))
        
        result['min_entropy'] = min_entropy
        result['smoothed_min_entropy'] = smoothed_min_entropy
        
        return result
    
    def _calculate_universal_key_rate(self, 
                                    info_theory_result: Dict[str, Any],
                                    entropy_result: Dict[str, Any],
                                    security_params: UniversalSecurityParameters) -> Dict[str, Any]:
        """通用密钥率计算"""
        result = {}
        
        # 提取关键参数
        min_entropy = entropy_result.get('smoothed_min_entropy', 0.0)
        mutual_info = info_theory_result.get('mutual_information', 0.0)
        
        # 计算密钥率：R = H_min(X|E) - I(X:Y) - 安全性修正
        security_correction = (
            np.sqrt(np.log(1/security_params.epsilon_sec)) +
            np.sqrt(np.log(1/security_params.finite_key_param))
        ) / 1000  # 简化的安全性修正
        
        key_rate = max(0, min_entropy - mutual_info - security_correction)
        
        result['key_rate'] = key_rate
        result['security_parameter'] = security_params.epsilon_sec
        
        return result
    
    def _analyze_finite_key_effects(self, 
                                   experimental_data: Dict[str, Any],
                                   security_params: UniversalSecurityParameters) -> Dict[str, Any]:
        """有限密钥效应分析"""
        result = {}
        
        n_pulses = experimental_data.get('n_pulses', 100000)
        
        # 有限密钥长度估计
        finite_key_length = int(n_pulses * 0.1)  # 简化估计
        
        result['finite_key_length'] = finite_key_length
        result['finite_key_rate'] = finite_key_length / n_pulses
        
        return result
    
    def apply_entropy_accumulation(self, 
                                 rounds_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        应用熵累积定理
        
        Args:
            rounds_data: 多轮协议数据
            
        Returns:
            熵累积结果
        """
        result = {}
        
        # 简化的熵累积计算
        total_entropy = 0.0
        for round_data in rounds_data:
            round_qber = round_data.get('qber', 0.02)
            if round_qber < 0.5:
                h_qber = -round_qber * np.log2(round_qber) - (1-round_qber) * np.log2(1-round_qber)
                round_entropy = 1 - h_qber
                total_entropy += round_entropy
        
        result['accumulated_entropy'] = total_entropy
        result['smoothing_parameter'] = 1e-8
        result['finite_key_correction'] = np.sqrt(len(rounds_data)) * 0.01
        
        return result
    
    def analyze_composable_security(self, 
                                  protocol_instances: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析可组合安全性
        
        Args:
            protocol_instances: 协议实例列表
            
        Returns:
            可组合安全性结果
        """
        result = {}
        
        # 计算总安全参数
        total_epsilon = sum(instance.get('epsilon', 1e-10) for instance in protocol_instances)
        
        # 可组合性开销
        n_protocols = len(protocol_instances)
        composability_overhead = np.sqrt(n_protocols) * 1e-10
        
        total_security_param = total_epsilon + composability_overhead
        
        result['total_security_parameter'] = total_security_param
        result['composability_overhead'] = composability_overhead
        result['is_composable_secure'] = total_security_param <= 1e-6  # 阈值
        
        return result
    
    def analyze_device_independent_security(self, 
                                          di_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析设备无关安全性
        
        Args:
            di_data: 设备无关实验数据
            
        Returns:
            设备无关安全性结果
        """
        result = {}
        
        bell_violation = di_data.get('bell_violation', 2.0)
        detection_efficiency = di_data.get('detection_efficiency', 0.8)
        
        # Bell不等式违反检查
        is_bell_violated = bell_violation > 2.0
        
        # 最小熵界限（基于Bell违反的简化估计）
        if is_bell_violated:
            violation_margin = bell_violation - 2.0
            min_entropy_bound = violation_margin / 2.0 * detection_efficiency
        else:
            min_entropy_bound = 0.0
        
        # 随机性率
        randomness_rate = max(0, min_entropy_bound * 0.5)  # 简化估计
        
        result['min_entropy_bound'] = min_entropy_bound
        result['randomness_rate'] = randomness_rate
        result['device_independence_certified'] = is_bell_violated and detection_efficiency > 0.7
        result['bell_violation'] = bell_violation
        
        return result


# ==================== 向后兼容性 ====================

# 保持原有接口的向后兼容性
SecurityParameters = UniversalSecurityParameters

# 创建一个临时的 ProtocolType 枚举以保持兼容性
# 注意：这将在未来版本中被移除
class ProtocolType(Enum):
    """
    协议类型枚举（向后兼容性）
    
    警告：此枚举已弃用，请使用基于 ProtocolFeatures 的通用方法
    """
    BB84 = "BB84"
    DECOY_BB84 = "Decoy-BB84"  
    MDI_QKD = "MDI-QKD"
    TWIN_FIELD = "Twin-Field"
    
    def __init__(self, value):
        self._value_ = value
        warnings.warn(
            "ProtocolType enum is deprecated. Use ProtocolFeatures for universal protocol description.",
            DeprecationWarning,
            stacklevel=2
        )


# ==================== 工厂函数 ====================

def create_bb84_protocol() -> ProtocolFeatures:
    """创建 BB84 协议特征"""
    operations = [
        QuantumOperation("state_preparation", QuantumOperationType.PREPARATION),
        QuantumOperation("quantum_channel", QuantumOperationType.CHANNEL),
        QuantumOperation("measurement", QuantumOperationType.MEASUREMENT)
    ]
    
    return ProtocolFeatures(
        name="BB84",
        operations=operations,
        parties=['Alice', 'Bob'],
        communication_rounds=1,
        measurement_bases=2,
        decoy_states=False,
        device_independence=False
    )


def create_mdi_qkd_protocol() -> ProtocolFeatures:
    """创建 MDI-QKD 协议特征"""
    operations = [
        QuantumOperation("alice_preparation", QuantumOperationType.PREPARATION),
        QuantumOperation("bob_preparation", QuantumOperationType.PREPARATION),
        QuantumOperation("alice_channel", QuantumOperationType.CHANNEL),
        QuantumOperation("bob_channel", QuantumOperationType.CHANNEL),
        QuantumOperation("bell_measurement", QuantumOperationType.MEASUREMENT)
    ]
    
    return ProtocolFeatures(
        name="MDI_QKD",
        operations=operations,
        parties=['Alice', 'Bob', 'Charlie'],
        communication_rounds=1,
        measurement_bases=2,
        trusted_parties=['Alice', 'Bob'],
        untrusted_parties=['Charlie'],
        decoy_states=False,
        device_independence=False
    )


def create_decoy_bb84_protocol() -> ProtocolFeatures:
    """创建诱骗态 BB84 协议特征"""
    operations = [
        QuantumOperation("intensity_modulated_preparation", QuantumOperationType.PREPARATION),
        QuantumOperation("quantum_channel", QuantumOperationType.CHANNEL),
        QuantumOperation("measurement", QuantumOperationType.MEASUREMENT)
    ]
    
    return ProtocolFeatures(
        name="Decoy_BB84",
        operations=operations,
        parties=['Alice', 'Bob'],
        communication_rounds=1,
        measurement_bases=2,
        intensity_settings=3,
        decoy_states=True,
        device_independence=False
    )