"""
熵估计器模块（通用版本）

基于信息论的通用熵估计框架，支持任意协议结构的熵分析。

新功能（v2.0）：
- 基于测量数据的通用熵估计
- 协议无关的互信息和Holevo信息计算
- 有限密钥效应和统计涨落处理
- 现代量子信息论理论集成
- 完全向后兼容的接口

支持的熵类型：
- 最小熵 H_min(X|E)
- 条件熵 H(X|E)
- 冯·诺依曼熵 S(ρ)
- 相对熵 D(p||q)
- 互信息 I(A:B)
- Holevo信息 χ(A:E)

参考文献：
- Nielsen & Chuang: Quantum Computation and Quantum Information
- Tomamichel et al. (2012): Tight finite-key analysis
- Renner & Wolf (2023): Quantum Advantage in Cryptography
- Metger et al. (2024): Generalised Entropy Accumulation
"""

import numpy as np
import logging
import warnings
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field

# 导入通用框架
try:
    from .universal_framework import (
        ProtocolFeatures,
        QuantumOperation,
        QuantumOperationType,
        UniversalSecurityParameters,
        create_bb84_protocol,
        create_mdi_qkd_protocol,
        create_decoy_bb84_protocol
    )
    _UNIVERSAL_FRAMEWORK_AVAILABLE = True
except ImportError:
    _UNIVERSAL_FRAMEWORK_AVAILABLE = False
    warnings.warn(
        "Universal framework not available. Some features will be limited.",
        ImportWarning
    )

logger = logging.getLogger(__name__)


@dataclass
class EntropyResult:
    """熵计算结果（通用版本）"""
    entropy_type: str
    value: float
    confidence_interval: Optional[Tuple[float, float]] = None
    parameters: Optional[Dict] = None
    
    # 通用框架结果（新增）
    mutual_information: float = 0.0      # 互信息 I(A:B)
    holevo_information: float = 0.0      # Holevo信息 χ(A:E)
    finite_key_correction: float = 0.0   # 有限密钥修正
    statistical_variance: float = 0.0    # 统计方差
    protocol_features: Optional[Any] = None
    
    # 计算详情
    calculation_details: Dict[str, Any] = field(default_factory=dict)


class EntropyEstimator:
    """
    熵估计器
    
    提供各种熵的计算和估计功能，支持QKD协议的安全性分析。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化熵估计器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.EntropyEstimator")
    
    def calculate_min_entropy(self, 
                            qber: float,
                            protocol_type: str = "BB84",
                            **kwargs) -> EntropyResult:
        """
        计算最小熵 H_min(X|E)
        
        Args:
            qber: 量子比特错误率
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            EntropyResult: 最小熵计算结果
        """
        if protocol_type == "BB84":
            h_min = self._calculate_min_entropy_bb84(qber)
        elif protocol_type == "Decoy-BB84":
            h_min = self._calculate_min_entropy_decoy(qber, **kwargs)
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")
        
        return EntropyResult(
            entropy_type="min_entropy",
            value=h_min,
            parameters={"qber": qber, "protocol_type": protocol_type}
        )
    
    def calculate_conditional_entropy(self,
                                    joint_dist: np.ndarray,
                                    **kwargs) -> EntropyResult:
        """
        计算条件熵 H(X|E)
        
        Args:
            joint_dist: 联合概率分布
            **kwargs: 其他参数
            
        Returns:
            EntropyResult: 条件熵计算结果
        """
        # 计算边缘分布
        p_x = np.sum(joint_dist, axis=1)
        p_e = np.sum(joint_dist, axis=0)
        
        # 计算条件分布 P(X|E)
        p_x_given_e = joint_dist / p_e[np.newaxis, :]
        
        # 计算条件熵
        h_conditional = 0
        for e in range(joint_dist.shape[1]):
            if p_e[e] > 0:
                h_e = 0
                for x in range(joint_dist.shape[0]):
                    if p_x_given_e[x, e] > 0:
                        h_e -= p_x_given_e[x, e] * np.log2(p_x_given_e[x, e])
                h_conditional += p_e[e] * h_e
        
        return EntropyResult(
            entropy_type="conditional_entropy",
            value=h_conditional,
            parameters={"joint_dist_shape": joint_dist.shape}
        )
    
    def calculate_von_neumann_entropy(self,
                                    density_matrix: np.ndarray) -> EntropyResult:
        """
        计算冯·诺依曼熵 S(ρ) = -Tr(ρ log ρ)
        
        Args:
            density_matrix: 密度矩阵
            
        Returns:
            EntropyResult: 冯·诺依曼熵计算结果
        """
        # 计算特征值
        eigenvalues = np.linalg.eigvals(density_matrix)
        
        # 计算熵
        entropy = 0
        for eigenval in eigenvalues:
            if eigenval > 0:
                entropy -= eigenval * np.log2(eigenval)
        
        return EntropyResult(
            entropy_type="von_neumann_entropy",
            value=entropy,
            parameters={"density_matrix_shape": density_matrix.shape}
        )
    
    def calculate_relative_entropy(self,
                                 p: np.ndarray,
                                 q: np.ndarray) -> EntropyResult:
        """
        计算相对熵 D(p||q) = Σ p_i log(p_i/q_i)
        
        Args:
            p: 概率分布p
            q: 概率分布q
            
        Returns:
            EntropyResult: 相对熵计算结果
        """
        if len(p) != len(q):
            raise ValueError("概率分布长度必须相同")
        
        # 检查概率分布的有效性
        if not (np.all(p >= 0) and np.allclose(np.sum(p), 1)):
            raise ValueError("p不是有效的概率分布")
        if not (np.all(q >= 0) and np.allclose(np.sum(q), 1)):
            raise ValueError("q不是有效的概率分布")
        
        # 计算相对熵
        entropy = 0
        for i in range(len(p)):
            if p[i] > 0 and q[i] > 0:
                entropy += p[i] * np.log2(p[i] / q[i])
        
        return EntropyResult(
            entropy_type="relative_entropy",
            value=entropy,
            parameters={"p_shape": p.shape, "q_shape": q.shape}
        )
    
    def _calculate_min_entropy_bb84(self, qber: float) -> float:
        """
        计算BB84协议的最小熵
        
        基于Renner 2008: H_min(X|E) ≥ 1 - h(QBER)
        """
        if qber <= 0 or qber >= 0.5:
            return 0.0
        
        # 二元熵函数
        h_qber = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
        h_min = 1 - h_qber
        
        return h_min
    
    def _calculate_min_entropy_decoy(self, qber: float, **kwargs) -> float:
        """
        计算诱骗态协议的最小熵
        
        基于Lim et al. 2014
        """
        # 简化的诱骗态最小熵计算
        # 实际应用中需要更复杂的数值方法
        
        # 假设单光子错误率
        e_1 = kwargs.get('e_1', 0.02)
        
        if e_1 <= 0 or e_1 >= 0.5:
            return 0.0
        
        # 单光子错误率的二元熵
        h_e1 = -e_1 * np.log2(e_1) - (1 - e_1) * np.log2(1 - e_1)
        
        # 假设单光子增益
        q_1 = kwargs.get('q_1', 0.1)
        
        h_min = q_1 * (1 - h_e1)
        
        return h_min
    
    def estimate_entropy_from_samples(self,
                                    samples: List[int],
                                    alphabet_size: int,
                                    method: str = "plugin") -> EntropyResult:
        """
        从样本估计熵
        
        Args:
            samples: 样本序列
            alphabet_size: 字母表大小
            method: 估计方法 ("plugin", "miller_madow", "jackknife")
            
        Returns:
            EntropyResult: 熵估计结果
        """
        # 计算经验分布
        counts = np.zeros(alphabet_size)
        for sample in samples:
            if 0 <= sample < alphabet_size:
                counts[sample] += 1
        
        p_hat = counts / len(samples)
        
        if method == "plugin":
            entropy = self._plugin_entropy_estimator(p_hat)
        elif method == "miller_madow":
            entropy = self._miller_madow_entropy_estimator(p_hat, len(samples))
        elif method == "jackknife":
            entropy = self._jackknife_entropy_estimator(samples, alphabet_size)
        else:
            raise ValueError(f"不支持的估计方法: {method}")
        
        return EntropyResult(
            entropy_type=f"estimated_entropy_{method}",
            value=entropy,
            parameters={
                "n_samples": len(samples),
                "alphabet_size": alphabet_size,
                "method": method
            }
        )
    
    def _plugin_entropy_estimator(self, p_hat: np.ndarray) -> float:
        """插件熵估计器"""
        entropy = 0
        for p in p_hat:
            if p > 0:
                entropy -= p * np.log2(p)
        return entropy
    
    def _miller_madow_entropy_estimator(self, p_hat: np.ndarray, n: int) -> float:
        """Miller-Madow熵估计器"""
        k = np.sum(p_hat > 0)  # 非零概率的数量
        plugin_entropy = self._plugin_entropy_estimator(p_hat)
        
        # Miller-Madow修正
        bias_correction = (k - 1) / (2 * n)
        
        return plugin_entropy + bias_correction
    
    def _jackknife_entropy_estimator(self, samples: List[int], alphabet_size: int) -> float:
        """Jackknife熵估计器"""
        n = len(samples)
        
        # 完整样本的熵
        full_entropy = self._plugin_entropy_estimator(
            np.bincount(samples, minlength=alphabet_size) / n
        )
        
        # 留一法估计
        jackknife_entropy = 0
        for i in range(n):
            # 移除第i个样本
            reduced_samples = samples[:i] + samples[i+1:]
            counts = np.bincount(reduced_samples, minlength=alphabet_size)
            p_hat = counts / (n - 1)
            jackknife_entropy += self._plugin_entropy_estimator(p_hat)
        
        jackknife_entropy /= n
        
        # Jackknife修正
        corrected_entropy = n * full_entropy - (n - 1) * jackknife_entropy
        
        return corrected_entropy
    
    def calculate_entropy_bounds(self,
                               qber: float,
                               protocol_type: str = "BB84",
                               confidence_level: float = 0.95,
                               **kwargs) -> EntropyResult:
        """
        计算熵的置信区间
        
        Args:
            qber: 量子比特错误率
            protocol_type: 协议类型
            confidence_level: 置信水平
            **kwargs: 其他参数
            
        Returns:
            EntropyResult: 包含置信区间的熵结果
        """
        # 计算点估计
        point_estimate = self.calculate_min_entropy(qber, protocol_type, **kwargs)
        
        # 计算置信区间（简化版本）
        # 实际应用中需要更复杂的统计方法
        
        # 假设正态分布
        std_error = 0.01  # 假设标准误差
        z_score = 1.96  # 95%置信水平对应的z分数
        
        lower_bound = point_estimate.value - z_score * std_error
        upper_bound = point_estimate.value + z_score * std_error
        
        return EntropyResult(
            entropy_type=point_estimate.entropy_type,
            value=point_estimate.value,
            confidence_interval=(lower_bound, upper_bound),
            parameters=point_estimate.parameters
        )
    
    # ==================== 通用熵估计方法（新增） ====================
    
    def estimate_universal_entropy(self,
                                  measurement_data: Dict[str, Any],
                                  protocol_features,
                                  security_params) -> EntropyResult:
        """
        通用熵估计方法
        
        基于测量数据和协议特征进行协议无关的熵估计。
        
        Args:
            measurement_data: 测量数据字典
            protocol_features: 协议特征描述
            security_params: 安全参数
            
        Returns:
            EntropyResult: 通用熵估计结果
        """
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework not available")
        
        self.logger.info(f"开始通用熵估计: {getattr(protocol_features, 'name', 'Unknown')}")
        
        # 1. 计算互信息 I(A:B)
        mutual_info = self.estimate_mutual_information(measurement_data, protocol_features)
        
        # 2. 计算Holevo信息 χ(A:E)
        holevo_info = self.estimate_holevo_information(measurement_data, protocol_features)
        
        # 3. 计算有限密钥效应
        n_samples = len(measurement_data.get('alice_measurements', []))
        finite_key_effect = self.estimate_finite_key_effects(n_samples, security_params)
        
        # 4. 计算统计方差
        stat_variance = self.estimate_statistical_variance(measurement_data, security_params)
        
        # 5. 计算通用熵
        # 基于信息论的通用熵估计：H_universal = H(A) - χ(A:E) - δ_finite - δ_statistical
        alice_entropy = self._calculate_shannon_entropy(measurement_data.get('alice_measurements', []))
        universal_entropy = alice_entropy - holevo_info - finite_key_effect - stat_variance
        
        # 确保非负
        universal_entropy = max(0.0, universal_entropy)
        
        # 6. 计算置信区间
        confidence_interval = self._calculate_entropy_confidence_interval(
            universal_entropy, n_samples, security_params
        )
        
        # 7. 构建结果
        result = EntropyResult(
            entropy_type="universal_entropy",
            value=universal_entropy,
            confidence_interval=confidence_interval,
            parameters={
                'n_samples': n_samples,
                'protocol_name': getattr(protocol_features, 'name', 'Unknown')
            },
            # 通用框架特定结果
            mutual_information=mutual_info,
            holevo_information=holevo_info,
            finite_key_correction=finite_key_effect,
            statistical_variance=stat_variance,
            protocol_features=protocol_features,
            calculation_details={
                'alice_entropy': alice_entropy,
                'mutual_information': mutual_info,
                'holevo_information': holevo_info,
                'finite_key_effect': finite_key_effect,
                'statistical_variance': stat_variance
            }
        )
        
        self._log_universal_entropy_details(result)
        return result
    
    def estimate_mutual_information(self,
                                   measurement_data: Dict[str, Any],
                                   protocol_features) -> float:
        """
        估计Alice和Bob之间的互信息 I(A:B)
        
        基于实际测量数据计算经验互信息。
        
        Args:
            measurement_data: 测量数据
            protocol_features: 协议特征
            
        Returns:
            float: 互信息估计值 (bits)
        """
        alice_data = measurement_data.get('alice_measurements', [])
        bob_data = measurement_data.get('bob_measurements', [])
        alice_bases = measurement_data.get('alice_bases', [])
        bob_bases = measurement_data.get('bob_bases', [])
        detections = measurement_data.get('detection_events', [])
        
        if not all([alice_data, bob_data]):
            self.logger.warning("测量数据不足，使用理论互信息估计")
            return self._estimate_theoretical_mutual_information(measurement_data)
        
        # 过滤有效的测量事件
        valid_pairs = []
        for i in range(min(len(alice_data), len(bob_data))):
            # 检查检测事件
            if i < len(detections) and not detections[i]:
                continue
            
            # 检查基匹配（如果有基信息）
            if (i < len(alice_bases) and i < len(bob_bases) and 
                alice_bases[i] != bob_bases[i]):
                continue
            
            valid_pairs.append((alice_data[i], bob_data[i]))
        
        if len(valid_pairs) < 10:
            self.logger.warning("有效数据点不足，使用理论估计")
            return self._estimate_theoretical_mutual_information(measurement_data)
        
        # 计算联合概率分布
        joint_counts = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
        for a, b in valid_pairs:
            if (a, b) in joint_counts:
                joint_counts[(a, b)] += 1
        
        n_total = len(valid_pairs)
        joint_probs = {k: v/n_total for k, v in joint_counts.items()}
        
        # 计算边缘概率
        p_a0 = joint_probs[(0, 0)] + joint_probs[(0, 1)]
        p_a1 = joint_probs[(1, 0)] + joint_probs[(1, 1)]
        p_b0 = joint_probs[(0, 0)] + joint_probs[(1, 0)]
        p_b1 = joint_probs[(0, 1)] + joint_probs[(1, 1)]
        
        # 计算互信息 I(A:B) = Σ p(a,b) log₂[p(a,b)/(p(a)p(b))]
        mutual_info = 0.0
        for (a, b), p_ab in joint_probs.items():
            if p_ab > 0:
                p_a = p_a1 if a else p_a0
                p_b = p_b1 if b else p_b0
                
                if p_a > 0 and p_b > 0:
                    mutual_info += p_ab * np.log2(p_ab / (p_a * p_b))
        
        self.logger.debug(f"互信息估计: I(A:B) = {mutual_info:.6f} bits")
        return max(0.0, mutual_info)
    
    def estimate_holevo_information(self,
                                   measurement_data: Dict[str, Any],
                                   protocol_features) -> float:
        """
        估计Holevo信息 χ(A:E)
        
        基于窃听者可获得的信息上界估计。
        
        Args:
            measurement_data: 测量数据
            protocol_features: 协议特征
            
        Returns:
            float: Holevo信息估计值 (bits)
        """
        # 方法1：基于测量不匹配率估计
        if 'eavesdropper_info' in measurement_data:
            # 如果有直接的窃听信息
            eavesdrop_data = measurement_data['eavesdropper_info']
            if eavesdrop_data:
                avg_eavesdrop_info = np.mean(eavesdrop_data)
                return self._binary_entropy(avg_eavesdrop_info)
        
        # 方法2：基于错误率估计
        alice_data = measurement_data.get('alice_measurements', [])
        bob_data = measurement_data.get('bob_measurements', [])
        alice_bases = measurement_data.get('alice_bases', [])
        bob_bases = measurement_data.get('bob_bases', [])
        
        if alice_data and bob_data:
            # 计算匹配基下的错误率
            errors = 0
            valid_comparisons = 0
            
            for i in range(min(len(alice_data), len(bob_data))):
                # 只考虑基匹配的情况
                if (i < len(alice_bases) and i < len(bob_bases) and 
                    alice_bases[i] == bob_bases[i]):
                    valid_comparisons += 1
                    if alice_data[i] != bob_data[i]:
                        errors += 1
            
            if valid_comparisons > 0:
                error_rate = errors / valid_comparisons
                holevo_info = self._binary_entropy(error_rate)
                
                # 应用协议特定的修正
                if hasattr(protocol_features, 'name'):
                    protocol_name = protocol_features.name.lower()
                    if 'mdi' in protocol_name:
                        holevo_info *= 0.8  # MDI-QKD的窃听信息较少
                    elif 'decoy' in protocol_name:
                        holevo_info *= 0.9  # 诱骗态提供额外安全性
                
                self.logger.debug(f"Holevo信息估计: χ(A:E) = {holevo_info:.6f} bits")
                return max(0.0, holevo_info)
        
        # 方法3：理论默认值
        self.logger.warning("无法从测量数据估计Holevo信息，使用理论默认值")
        return 0.1  # 保守的默认值
    
    def estimate_finite_key_effects(self,
                                   n_samples: int,
                                   security_params) -> float:
        """
        估计有限密钥效应
        
        基于样本数量和安全参数计算有限密钥修正项。
        
        Args:
            n_samples: 样本数量
            security_params: 安全参数
            
        Returns:
            float: 有限密钥效应估计值
        """
        if n_samples <= 0:
            return float('inf')
        
        # 基于现代有限密钥分析理论
        epsilon_total = getattr(security_params, 'epsilon_sec', 1e-10)
        epsilon_total += getattr(security_params, 'epsilon_cor', 1e-10)
        epsilon_total += getattr(security_params, 'epsilon_pe', 1e-10)
        
        if epsilon_total <= 0:
            epsilon_total = 1e-12
        
        # 主要的有限密钥修正：δ(n) ≈ sqrt(log(1/ε) / (2n))
        main_correction = np.sqrt(np.log(1 / epsilon_total) / (2 * n_samples))
        
        # 添加额外的熵平滑修正
        if hasattr(security_params, 'entropy_smoothing_param'):
            smoothing_param = security_params.entropy_smoothing_param
            smoothing_correction = np.sqrt(np.log(1 / smoothing_param) / n_samples)
            main_correction += smoothing_correction * 0.5
        
        # 添加可组合性修正
        if hasattr(security_params, 'composability_param'):
            comp_param = security_params.composability_param
            comp_correction = np.sqrt(np.log(1 / comp_param) / n_samples)
            main_correction += comp_correction * 0.3
        
        self.logger.debug(f"有限密钥效应: δ(n) = {main_correction:.6f}")
        return main_correction
    
    def estimate_statistical_variance(self,
                                     measurement_data: Dict[str, Any],
                                     security_params) -> float:
        """
        估计统计涨落方差
        
        基于测量数据的统计性质估计方差项。
        
        Args:
            measurement_data: 测量数据
            security_params: 安全参数
            
        Returns:
            float: 统计方差估计值
        """
        alice_data = measurement_data.get('alice_measurements', [])
        bob_data = measurement_data.get('bob_measurements', [])
        
        if not alice_data or not bob_data:
            return 0.01  # 默认小方差
        
        n_samples = len(alice_data)
        
        # 计算样本方差
        if n_samples > 1:
            alice_var = np.var(alice_data)
            bob_var = np.var(bob_data) if len(bob_data) > 1 else 0
            
            # 联合方差估计
            joint_var = (alice_var + bob_var) / 2
            
            # 归一化到每样本的贡献
            stat_variance = joint_var / np.sqrt(n_samples)
            
            # 应用安全参数的影响
            epsilon_factor = getattr(security_params, 'finite_key_param', 1e-7)
            stat_variance *= np.sqrt(np.log(1 / epsilon_factor))
            
            self.logger.debug(f"统计方差: σ² = {stat_variance:.6f}")
            return max(0.0, stat_variance)
        
        return 0.01  # 最小方差
    
    # ==================== 辅助方法（新增） ====================
    
    def _calculate_shannon_entropy(self, data: List[int]) -> float:
        """计算Shannon熵"""
        if len(data) == 0:
            return 0.0
        
        # 计算概率分布
        unique, counts = np.unique(data, return_counts=True)
        probs = counts / len(data)
        
        # 计算Shannon熵
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    def _binary_entropy(self, p: float) -> float:
        """计算二元熵函数"""
        if p <= 0 or p >= 1:
            return 0.0
        return -p * np.log2(p) - (1-p) * np.log2(1-p)
    
    def _estimate_theoretical_mutual_information(self, measurement_data: Dict[str, Any]) -> float:
        """理论互信息估计（当数据不足时）"""
        # 尝试从其他信息估计错误率
        error_rate = 0.05  # 默认值
        
        # 如果有窃听信息，使用它来估计错误率
        if 'eavesdropper_info' in measurement_data:
            eavesdrop_data = measurement_data['eavesdropper_info']
            if eavesdrop_data:
                error_rate = np.mean(eavesdrop_data)
        
        # 对于二元对称信道，I(A:B) = 1 - h(error_rate)
        return 1.0 - self._binary_entropy(error_rate)
    
    def _calculate_entropy_confidence_interval(self, 
                                             entropy_value: float,
                                             n_samples: int,
                                             security_params) -> Tuple[float, float]:
        """计算熵的置信区间"""
        if n_samples <= 1:
            return (entropy_value * 0.9, entropy_value * 1.1)
        
        # 基于中心极限定理的置信区间
        std_error = np.sqrt(entropy_value * (1 - entropy_value) / n_samples)
        
        # 应用安全参数的影响
        confidence_level = 1 - getattr(security_params, 'epsilon_sec', 1e-10)
        z_score = 1.96  # 95%置信水平
        
        if confidence_level > 0.99:
            z_score = 2.58  # 99%置信水平
        elif confidence_level > 0.999:
            z_score = 3.29  # 99.9%置信水平
        
        margin = z_score * std_error
        lower_bound = max(0.0, entropy_value - margin)
        upper_bound = min(1.0, entropy_value + margin)
        
        return (lower_bound, upper_bound)
    
    def _log_universal_entropy_details(self, result: EntropyResult):
        """记录通用熵估计详情"""
        self.logger.info("=== 通用熵估计详情 ===")
        if result.protocol_features:
            self.logger.info(f"协议: {getattr(result.protocol_features, 'name', 'Unknown')}")
        self.logger.info(f"通用熵: {result.value:.6f}")
        self.logger.info(f"互信息 I(A:B): {result.mutual_information:.6f}")
        self.logger.info(f"Holevo信息 χ(A:E): {result.holevo_information:.6f}")
        self.logger.info(f"有限密钥修正: {result.finite_key_correction:.6f}")
        self.logger.info(f"统计方差: {result.statistical_variance:.6f}")
        if result.confidence_interval:
            self.logger.info(f"置信区间: [{result.confidence_interval[0]:.6f}, {result.confidence_interval[1]:.6f}]")
        self.logger.info("=====================")
    
    # ==================== 重构现有方法（向后兼容） ====================
    
    def calculate_min_entropy(self, 
                            qber: float,
                            protocol_type: str = "BB84",
                            **kwargs) -> EntropyResult:
        """
        计算最小熵 H_min(X|E)（向后兼容接口）
        
        警告：建议使用 estimate_universal_entropy() 方法以获得完整功能。
        """
        warnings.warn(
            "calculate_min_entropy is partially deprecated. Use estimate_universal_entropy() for full universal estimation.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # 尝试使用通用框架
        if _UNIVERSAL_FRAMEWORK_AVAILABLE:
            return self._calculate_min_entropy_via_universal(qber, protocol_type, **kwargs)
        
        # 回退到传统实现
        if protocol_type == "BB84":
            h_min = self._calculate_min_entropy_bb84(qber)
        elif protocol_type == "Decoy-BB84":
            h_min = self._calculate_min_entropy_decoy(qber, **kwargs)
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")
        
        return EntropyResult(
            entropy_type="min_entropy",
            value=h_min,
            parameters={"qber": qber, "protocol_type": protocol_type}
        )
    
    def _calculate_min_entropy_via_universal(self, qber: float, protocol_type: str, **kwargs) -> EntropyResult:
        """通过通用框架计算最小熵（向后兼容辅助方法）"""
        # 构造测量数据
        n_samples = kwargs.get('n_samples', 10000)
        
        # 模拟数据
        alice_bits = np.random.randint(0, 2, n_samples)
        bob_bits = alice_bits.copy()
        
        # 引入错误
        n_errors = int(n_samples * qber)
        error_indices = np.random.choice(n_samples, n_errors, replace=False)
        bob_bits[error_indices] = 1 - bob_bits[error_indices]
        
        measurement_data = {
            'alice_measurements': alice_bits.tolist(),
            'bob_measurements': bob_bits.tolist(),
            'alice_bases': ['Z'] * n_samples,
            'bob_bases': ['Z'] * n_samples,
            'detection_events': [True] * n_samples
        }
        
        # 选择协议特征
        if protocol_type == "BB84":
            protocol_features = create_bb84_protocol()
        elif protocol_type == "Decoy-BB84":
            protocol_features = create_decoy_bb84_protocol()
        elif protocol_type == "MDI-QKD":
            protocol_features = create_mdi_qkd_protocol()
        else:
            # 创建通用协议特征
            from .universal_framework import ProtocolFeatures
            protocol_features = ProtocolFeatures(
                name=protocol_type,
                operations=[],
                parties=['Alice', 'Bob']
            )
        
        # 安全参数
        from .universal_framework import UniversalSecurityParameters
        security_params = UniversalSecurityParameters(
            epsilon_sec=kwargs.get('epsilon_sec', 1e-10),
            epsilon_cor=kwargs.get('epsilon_cor', 1e-10),
            epsilon_pe=kwargs.get('epsilon_pe', 1e-10)
        )
        
        # 使用通用估计
        universal_result = self.estimate_universal_entropy(measurement_data, protocol_features, security_params)
        
        # 转换为向后兼容格式
        return EntropyResult(
            entropy_type="min_entropy",
            value=universal_result.value,
            confidence_interval=universal_result.confidence_interval,
            parameters={"qber": qber, "protocol_type": protocol_type},
            # 保留通用框架信息
            mutual_information=universal_result.mutual_information,
            holevo_information=universal_result.holevo_information,
            finite_key_correction=universal_result.finite_key_correction,
            statistical_variance=universal_result.statistical_variance,
            protocol_features=universal_result.protocol_features,
            calculation_details=universal_result.calculation_details
        )


# ==================== 向后兼容性和迁移指导 ====================

def create_universal_entropy_estimator():
    """
    创建通用熵估计器的便利函数
    
    这是推荐的创建方式，自动使用通用框架（如果可用）。
    
    Returns:
        EntropyEstimator: 配置好的估计器实例
    """
    estimator = EntropyEstimator()
    
    if _UNIVERSAL_FRAMEWORK_AVAILABLE:
        logger.info("使用通用熵估计框架")
    else:
        logger.warning("通用框架不可用，回退到传统实现")
    
    return estimator


def migrate_legacy_entropy_calculation(qber: float, 
                                      protocol_type: str,
                                      n_samples: int = 10000,
                                      **kwargs) -> EntropyResult:
    """
    迁移助手函数：将传统熵计算迁移到通用框架
    
    Args:
        qber: 量子比特错误率
        protocol_type: 协议类型
        n_samples: 样本数量
        **kwargs: 其他参数
        
    Returns:
        EntropyResult: 熵估计结果
        
    Example:
        # 旧方式
        estimator = EntropyEstimator()
        result = estimator.calculate_min_entropy(qber=0.05, protocol_type="BB84")
        
        # 新方式（推荐）
        result = migrate_legacy_entropy_calculation(
            qber=0.05, 
            protocol_type="BB84",
            n_samples=50000
        )
    """
    estimator = EntropyEstimator()
    
    if _UNIVERSAL_FRAMEWORK_AVAILABLE:
        # 使用通用框架
        return estimator._calculate_min_entropy_via_universal(qber, protocol_type, n_samples=n_samples, **kwargs)
    else:
        # 回退到传统方法
        return estimator.calculate_min_entropy(qber, protocol_type, **kwargs)


# ==================== 导出 ====================

__all__ = [
    'EntropyEstimator',
    'EntropyResult',
    'create_universal_entropy_estimator',
    'migrate_legacy_entropy_calculation'
]

# 如果通用框架可用，也导出相关类
if _UNIVERSAL_FRAMEWORK_AVAILABLE:
    __all__.extend([
        'ProtocolFeatures',
        'UniversalSecurityParameters'
    ]) 