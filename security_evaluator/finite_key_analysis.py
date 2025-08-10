"""
有限密钥分析模块

提供有限密钥效应分析和修正功能，包括：
- 参数估计误差
- 统计波动
- 隐私放大
- 可组合安全性
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FiniteKeyResult:
    """有限密钥分析结果"""
    # 基础参数
    n_raw: int  # 原始密钥长度
    n_final: int  # 最终密钥长度
    
    # 有限密钥效应
    delta_1: float  # 参数估计误差
    delta_2: float  # 统计波动
    delta_3: float  # 隐私放大误差
    
    # 安全参数
    epsilon_sec: float  # 安全参数
    epsilon_cor: float  # 正确性参数
    epsilon_e: float    # 估计参数
    
    # 计算结果
    secret_key_rate: float  # 秘密密钥率
    privacy_amplification_rate: float  # 隐私放大率
    
    # 详细信息
    calculation_details: Dict[str, float]


class FiniteKeyAnalyzer:
    """
    有限密钥分析器
    
    分析有限密钥长度对QKD协议安全性的影响，并提供相应的修正。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化有限密钥分析器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.FiniteKeyAnalyzer")
        
        # 默认安全参数
        self.default_epsilons = {
            'epsilon_sec': 1e-10,
            'epsilon_cor': 1e-10,
            'epsilon_e': 1e-10,
            'epsilon_pa': 1e-10
        }
        
        # 更新默认参数
        self.default_epsilons.update(self.config)
    
    def analyze_finite_key_effects(self,
                                 n_raw: int,
                                 qber: float,
                                 protocol_type: str = "BB84",
                                 **kwargs) -> FiniteKeyResult:
        """
        分析有限密钥效应
        
        Args:
            n_raw: 原始密钥长度
            qber: 量子比特错误率
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            FiniteKeyResult: 有限密钥分析结果
        """
        self.logger.info(f"开始有限密钥分析: n_raw={n_raw}, QBER={qber:.4f}")
        
        # 获取安全参数
        epsilons = self._get_epsilons(**kwargs)
        
        # 计算有限密钥效应
        delta_1 = self._calculate_parameter_estimation_error(n_raw, epsilons['epsilon_e'])
        delta_2 = self._calculate_statistical_fluctuation(n_raw, epsilons['epsilon_sec'])
        delta_3 = self._calculate_privacy_amplification_error(epsilons['epsilon_pa'])
        
        # 计算秘密密钥率
        secret_key_rate = self._calculate_secret_key_rate_finite_key(
            qber, delta_1, delta_2, delta_3, protocol_type, **kwargs
        )
        
        # 计算最终密钥长度
        n_final = int(n_raw * secret_key_rate)
        
        # 计算隐私放大率
        privacy_amplification_rate = secret_key_rate
        
        # 构建结果
        result = FiniteKeyResult(
            n_raw=n_raw,
            n_final=n_final,
            delta_1=delta_1,
            delta_2=delta_2,
            delta_3=delta_3,
            epsilon_sec=epsilons['epsilon_sec'],
            epsilon_cor=epsilons['epsilon_cor'],
            epsilon_e=epsilons['epsilon_e'],
            secret_key_rate=secret_key_rate,
            privacy_amplification_rate=privacy_amplification_rate,
            calculation_details={
                'delta_1': delta_1,
                'delta_2': delta_2,
                'delta_3': delta_3,
                'secret_key_rate': secret_key_rate,
                'n_final': n_final
            }
        )
        
        self._log_analysis_details(result)
        return result
    
    def _get_epsilons(self, **kwargs) -> Dict[str, float]:
        """获取安全参数"""
        epsilons = self.default_epsilons.copy()
        epsilons.update(kwargs)
        return epsilons
    
    def _calculate_parameter_estimation_error(self, n: int, epsilon_e: float) -> float:
        """
        计算参数估计误差
        
        基于Tomamichel et al. 2012
        """
        if n <= 0:
            return 0.0
        
        # 参数估计误差项
        delta = np.sqrt(np.log(1 / epsilon_e) / (2 * n))
        
        self.logger.debug(f"参数估计误差: delta={delta:.6f} (n={n}, epsilon_e={epsilon_e})")
        return delta
    
    def _calculate_statistical_fluctuation(self, n: int, epsilon_sec: float) -> float:
        """
        计算统计波动
        
        基于Tomamichel et al. 2012
        """
        if n <= 0:
            return 0.0
        
        # 统计波动项
        delta = np.sqrt(np.log(1 / epsilon_sec) / (2 * n))
        
        self.logger.debug(f"统计波动: delta={delta:.6f} (n={n}, epsilon_sec={epsilon_sec})")
        return delta
    
    def _calculate_privacy_amplification_error(self, epsilon_pa: float) -> float:
        """
        计算隐私放大误差
        
        基于Renner 2008
        """
        # 隐私放大误差（简化模型）
        delta = epsilon_pa / 100  # 假设误差为安全参数的1%
        
        self.logger.debug(f"隐私放大误差: delta={delta:.6f} (epsilon_pa={epsilon_pa})")
        return delta
    
    def _calculate_secret_key_rate_finite_key(self,
                                            qber: float,
                                            delta_1: float,
                                            delta_2: float,
                                            delta_3: float,
                                            protocol_type: str,
                                            **kwargs) -> float:
        """
        计算有限密钥条件下的秘密密钥率
        
        Args:
            qber: 量子比特错误率
            delta_1: 参数估计误差
            delta_2: 统计波动
            delta_3: 隐私放大误差
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            float: 秘密密钥率
        """
        if protocol_type == "BB84":
            return self._calculate_bb84_secret_key_rate_finite_key(
                qber, delta_1, delta_2, delta_3, **kwargs
            )
        elif protocol_type == "Decoy-BB84":
            return self._calculate_decoy_bb84_secret_key_rate_finite_key(
                qber, delta_1, delta_2, delta_3, **kwargs
            )
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")
    
    def _calculate_bb84_secret_key_rate_finite_key(self,
                                                  qber: float,
                                                  delta_1: float,
                                                  delta_2: float,
                                                  delta_3: float,
                                                  **kwargs) -> float:
        """
        计算BB84协议的有限密钥秘密密钥率
        
        基于Renner 2008和Tomamichel et al. 2012
        """
        # 纠错效率因子
        f_ec = kwargs.get('f_ec', 1.16)
        
        # 计算最小熵（考虑有限密钥效应）
        h_min = self._calculate_min_entropy_with_finite_key_effects(qber, delta_1)
        
        # 计算纠错泄露
        leak_ec = f_ec * qber
        
        # 计算总泄露
        total_leak = leak_ec + delta_2 + delta_3
        
        # 计算秘密密钥率
        secret_key_rate = h_min - total_leak
        
        # 确保非负
        secret_key_rate = max(0, secret_key_rate)
        
        self.logger.debug(f"BB84有限密钥秘密密钥率: h_min={h_min:.6f}, leak_ec={leak_ec:.6f}, "
                         f"total_leak={total_leak:.6f}, rate={secret_key_rate:.6f}")
        
        return secret_key_rate
    
    def _calculate_decoy_bb84_secret_key_rate_finite_key(self,
                                                        qber: float,
                                                        delta_1: float,
                                                        delta_2: float,
                                                        delta_3: float,
                                                        **kwargs) -> float:
        """
        计算诱骗态BB84协议的有限密钥秘密密钥率
        
        基于Lim et al. 2014
        """
        # 获取诱骗态参数
        q_1 = kwargs.get('q_1', 0.1)  # 单光子增益
        e_1 = kwargs.get('e_1', 0.02)  # 单光子错误率
        f_ec = kwargs.get('f_ec', 1.16)  # 纠错效率因子
        
        # 计算最小熵（考虑有限密钥效应）
        h_min = self._calculate_decoy_min_entropy_with_finite_key_effects(
            q_1, e_1, delta_1, **kwargs
        )
        
        # 计算纠错泄露
        leak_ec = f_ec * qber
        
        # 计算总泄露
        total_leak = leak_ec + delta_2 + delta_3
        
        # 计算秘密密钥率
        secret_key_rate = h_min - total_leak
        
        # 确保非负
        secret_key_rate = max(0, secret_key_rate)
        
        self.logger.debug(f"诱骗态有限密钥秘密密钥率: h_min={h_min:.6f}, leak_ec={leak_ec:.6f}, "
                         f"total_leak={total_leak:.6f}, rate={secret_key_rate:.6f}")
        
        return secret_key_rate
    
    def _calculate_min_entropy_with_finite_key_effects(self,
                                                     qber: float,
                                                     delta_1: float) -> float:
        """
        计算考虑有限密钥效应的最小熵
        
        基于Tomamichel et al. 2012
        """
        # 调整QBER（考虑参数估计误差）
        qber_adjusted = qber + delta_1
        
        # 计算最小熵
        if qber_adjusted <= 0 or qber_adjusted >= 0.5:
            return 0.0
        
        # 二元熵函数
        h_qber = -qber_adjusted * np.log2(qber_adjusted) - (1 - qber_adjusted) * np.log2(1 - qber_adjusted)
        h_min = 1 - h_qber
        
        return h_min
    
    def _calculate_decoy_min_entropy_with_finite_key_effects(self,
                                                           q_1: float,
                                                           e_1: float,
                                                           delta_1: float,
                                                           **kwargs) -> float:
        """
        计算诱骗态协议考虑有限密钥效应的最小熵
        
        基于Lim et al. 2014
        """
        # 调整单光子错误率（考虑参数估计误差）
        e_1_adjusted = e_1 + delta_1
        
        if e_1_adjusted <= 0 or e_1_adjusted >= 0.5:
            return 0.0
        
        # 单光子错误率的二元熵
        h_e1 = -e_1_adjusted * np.log2(e_1_adjusted) - (1 - e_1_adjusted) * np.log2(1 - e_1_adjusted)
        
        # 最小熵
        h_min = q_1 * (1 - h_e1)
        
        return h_min
    
    def calculate_asymptotic_key_rate(self,
                                    qber: float,
                                    protocol_type: str = "BB84",
                                    **kwargs) -> float:
        """
        计算渐近密钥率（无限密钥长度）
        
        Args:
            qber: 量子比特错误率
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            float: 渐近密钥率
        """
        if protocol_type == "BB84":
            return self._calculate_asymptotic_bb84_key_rate(qber, **kwargs)
        elif protocol_type == "Decoy-BB84":
            return self._calculate_asymptotic_decoy_bb84_key_rate(qber, **kwargs)
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")
    
    def _calculate_asymptotic_bb84_key_rate(self, qber: float, **kwargs) -> float:
        """计算BB84协议的渐近密钥率"""
        f_ec = kwargs.get('f_ec', 1.16)
        
        # 最小熵
        if qber <= 0 or qber >= 0.5:
            return 0.0
        
        h_qber = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
        h_min = 1 - h_qber
        
        # 纠错泄露
        leak_ec = f_ec * qber
        
        # 渐近密钥率
        key_rate = h_min - leak_ec
        
        return max(0, key_rate)
    
    def _calculate_asymptotic_decoy_bb84_key_rate(self, qber: float, **kwargs) -> float:
        """计算诱骗态BB84协议的渐近密钥率"""
        q_1 = kwargs.get('q_1', 0.1)
        e_1 = kwargs.get('e_1', 0.02)
        f_ec = kwargs.get('f_ec', 1.16)
        
        # 最小熵
        if e_1 <= 0 or e_1 >= 0.5:
            return 0.0
        
        h_e1 = -e_1 * np.log2(e_1) - (1 - e_1) * np.log2(1 - e_1)
        h_min = q_1 * (1 - h_e1)
        
        # 纠错泄露
        leak_ec = f_ec * qber
        
        # 渐近密钥率
        key_rate = h_min - leak_ec
        
        return max(0, key_rate)
    
    def compare_finite_vs_asymptotic(self,
                                   n_raw: int,
                                   qber: float,
                                   protocol_type: str = "BB84",
                                   **kwargs) -> Dict[str, float]:
        """
        比较有限密钥和渐近密钥率
        
        Args:
            n_raw: 原始密钥长度
            qber: 量子比特错误率
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            Dict: 比较结果
        """
        # 有限密钥分析
        finite_result = self.analyze_finite_key_effects(n_raw, qber, protocol_type, **kwargs)
        
        # 渐近密钥率
        asymptotic_rate = self.calculate_asymptotic_key_rate(qber, protocol_type, **kwargs)
        
        # 计算差异
        rate_difference = asymptotic_rate - finite_result.secret_key_rate
        rate_ratio = finite_result.secret_key_rate / asymptotic_rate if asymptotic_rate > 0 else 0
        
        return {
            'finite_key_rate': finite_result.secret_key_rate,
            'asymptotic_key_rate': asymptotic_rate,
            'rate_difference': rate_difference,
            'rate_ratio': rate_ratio,
            'finite_key_length': finite_result.n_final,
            'efficiency': rate_ratio
        }
    
    def _log_analysis_details(self, result: FiniteKeyResult):
        """记录分析详情"""
        self.logger.info("=== 有限密钥分析详情 ===")
        self.logger.info(f"原始密钥长度: {result.n_raw}")
        self.logger.info(f"最终密钥长度: {result.n_final}")
        self.logger.info(f"参数估计误差: {result.delta_1:.6f}")
        self.logger.info(f"统计波动: {result.delta_2:.6f}")
        self.logger.info(f"隐私放大误差: {result.delta_3:.6f}")
        self.logger.info(f"秘密密钥率: {result.secret_key_rate:.6f}")
        self.logger.info(f"隐私放大率: {result.privacy_amplification_rate:.6f}")
        self.logger.info("=======================") 