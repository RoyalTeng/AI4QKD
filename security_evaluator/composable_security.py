"""
可组合安全性分析模块

提供QKD协议的可组合安全性分析，包括：
- 可组合安全性证明
- 安全性参数计算
- 协议组合分析
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ComposableSecurityResult:
    """可组合安全性分析结果"""
    # 基础参数
    epsilon_sec: float  # 安全参数
    epsilon_cor: float  # 正确性参数
    epsilon_ea: float   # 早期中止参数
    
    # 可组合安全性参数
    epsilon_composable: float  # 可组合安全参数
    epsilon_total: float       # 总安全参数
    
    # 协议参数
    n_protocols: int           # 协议数量
    protocol_epsilon: float    # 单个协议安全参数
    
    # 计算结果
    is_composable_secure: bool  # 是否满足可组合安全性
    security_level: float       # 安全级别
    
    # 详细信息
    calculation_details: Dict[str, float]


class ComposableSecurityAnalyzer:
    """
    可组合安全性分析器
    
    分析QKD协议的可组合安全性，确保协议在组合使用时的安全性。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化可组合安全性分析器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.ComposableSecurityAnalyzer")
        
        # 默认安全参数
        self.default_epsilons = {
            'epsilon_sec': 1e-10,
            'epsilon_cor': 1e-10,
            'epsilon_ea': 1e-10
        }
        
        # 更新默认参数
        self.default_epsilons.update(self.config)
    
    def analyze_composable_security(self,
                                  n_protocols: int,
                                  protocol_epsilon: float,
                                  **kwargs) -> ComposableSecurityResult:
        """
        分析可组合安全性
        
        Args:
            n_protocols: 协议数量
            protocol_epsilon: 单个协议安全参数
            **kwargs: 其他参数
            
        Returns:
            ComposableSecurityResult: 可组合安全性分析结果
        """
        self.logger.info(f"开始可组合安全性分析: n_protocols={n_protocols}, protocol_epsilon={protocol_epsilon}")
        
        # 获取安全参数
        epsilons = self._get_epsilons(**kwargs)
        
        # 计算可组合安全参数
        epsilon_composable = self._calculate_composable_epsilon(n_protocols, protocol_epsilon)
        
        # 计算总安全参数
        epsilon_total = self._calculate_total_epsilon(epsilons, epsilon_composable)
        
        # 判断是否满足可组合安全性
        is_composable_secure = epsilon_total <= epsilons['epsilon_sec']
        
        # 计算安全级别
        security_level = -np.log2(epsilon_total)
        
        # 构建结果
        result = ComposableSecurityResult(
            epsilon_sec=epsilons['epsilon_sec'],
            epsilon_cor=epsilons['epsilon_cor'],
            epsilon_ea=epsilons['epsilon_ea'],
            epsilon_composable=epsilon_composable,
            epsilon_total=epsilon_total,
            n_protocols=n_protocols,
            protocol_epsilon=protocol_epsilon,
            is_composable_secure=is_composable_secure,
            security_level=security_level,
            calculation_details={
                'epsilon_composable': epsilon_composable,
                'epsilon_total': epsilon_total,
                'security_level': security_level
            }
        )
        
        self._log_analysis_details(result)
        return result
    
    def _get_epsilons(self, **kwargs) -> Dict[str, float]:
        """获取安全参数"""
        epsilons = self.default_epsilons.copy()
        epsilons.update(kwargs)
        return epsilons
    
    def _calculate_composable_epsilon(self, n_protocols: int, protocol_epsilon: float) -> float:
        """
        计算可组合安全参数
        
        基于可组合安全性理论，多个协议组合时的安全参数
        """
        # 简化的可组合安全参数计算
        # 实际应用中需要更复杂的分析
        
        # 假设线性组合
        epsilon_composable = n_protocols * protocol_epsilon
        
        self.logger.debug(f"可组合安全参数: {epsilon_composable:.2e} "
                         f"(n_protocols={n_protocols}, protocol_epsilon={protocol_epsilon:.2e})")
        
        return epsilon_composable
    
    def _calculate_total_epsilon(self, epsilons: Dict[str, float], epsilon_composable: float) -> float:
        """
        计算总安全参数
        
        综合考虑各种安全参数
        """
        # 总安全参数 = 可组合安全参数 + 其他安全参数
        epsilon_total = epsilon_composable + epsilons['epsilon_cor'] + epsilons['epsilon_ea']
        
        self.logger.debug(f"总安全参数: {epsilon_total:.2e}")
        
        return epsilon_total
    
    def calculate_optimal_protocol_epsilon(self,
                                         n_protocols: int,
                                         target_epsilon: float,
                                         **kwargs) -> float:
        """
        计算满足目标安全参数的最优单个协议安全参数
        
        Args:
            n_protocols: 协议数量
            target_epsilon: 目标安全参数
            **kwargs: 其他参数
            
        Returns:
            float: 最优单个协议安全参数
        """
        epsilons = self._get_epsilons(**kwargs)
        
        # 计算其他安全参数的总和
        other_epsilons = epsilons['epsilon_cor'] + epsilons['epsilon_ea']
        
        # 计算可用于可组合安全性的安全参数
        available_epsilon = target_epsilon - other_epsilons
        
        if available_epsilon <= 0:
            raise ValueError("目标安全参数过小，无法满足可组合安全性要求")
        
        # 计算最优单个协议安全参数
        optimal_protocol_epsilon = available_epsilon / n_protocols
        
        self.logger.info(f"最优单个协议安全参数: {optimal_protocol_epsilon:.2e}")
        
        return optimal_protocol_epsilon
    
    def analyze_security_composition(self,
                                   protocol_epsilons: List[float],
                                   **kwargs) -> ComposableSecurityResult:
        """
        分析不同协议的安全参数组合
        
        Args:
            protocol_epsilons: 各协议的安全参数列表
            **kwargs: 其他参数
            
        Returns:
            ComposableSecurityResult: 组合安全性分析结果
        """
        n_protocols = len(protocol_epsilons)
        
        # 计算组合安全参数
        epsilon_composable = sum(protocol_epsilons)
        
        # 获取其他安全参数
        epsilons = self._get_epsilons(**kwargs)
        
        # 计算总安全参数
        epsilon_total = epsilon_composable + epsilons['epsilon_cor'] + epsilons['epsilon_ea']
        
        # 判断是否满足可组合安全性
        is_composable_secure = epsilon_total <= epsilons['epsilon_sec']
        
        # 计算安全级别
        security_level = -np.log2(epsilon_total)
        
        # 构建结果
        result = ComposableSecurityResult(
            epsilon_sec=epsilons['epsilon_sec'],
            epsilon_cor=epsilons['epsilon_cor'],
            epsilon_ea=epsilons['epsilon_ea'],
            epsilon_composable=epsilon_composable,
            epsilon_total=epsilon_total,
            n_protocols=n_protocols,
            protocol_epsilon=np.mean(protocol_epsilons),
            is_composable_secure=is_composable_secure,
            security_level=security_level,
            calculation_details={
                'epsilon_composable': epsilon_composable,
                'epsilon_total': epsilon_total,
                'security_level': security_level,
                'protocol_epsilons': protocol_epsilons
            }
        )
        
        self._log_analysis_details(result)
        return result
    
    def calculate_security_bounds(self,
                                n_protocols: int,
                                protocol_epsilon: float,
                                confidence_level: float = 0.95,
                                **kwargs) -> Dict[str, float]:
        """
        计算安全边界
        
        Args:
            n_protocols: 协议数量
            protocol_epsilon: 单个协议安全参数
            confidence_level: 置信水平
            **kwargs: 其他参数
            
        Returns:
            Dict: 安全边界
        """
        # 基础分析
        result = self.analyze_composable_security(n_protocols, protocol_epsilon, **kwargs)
        
        # 计算安全边界（简化版本）
        # 实际应用中需要更复杂的统计方法
        
        # 假设正态分布
        std_error = result.epsilon_total * 0.1  # 假设标准误差为10%
        z_score = 1.96  # 95%置信水平对应的z分数
        
        lower_bound = max(0, result.epsilon_total - z_score * std_error)
        upper_bound = result.epsilon_total + z_score * std_error
        
        return {
            'epsilon_total': result.epsilon_total,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'confidence_level': confidence_level,
            'is_secure': result.is_composable_secure
        }
    
    def optimize_protocol_distribution(self,
                                     total_epsilon: float,
                                     n_protocols: int,
                                     **kwargs) -> List[float]:
        """
        优化协议安全参数分布
        
        Args:
            total_epsilon: 总安全参数
            n_protocols: 协议数量
            **kwargs: 其他参数
            
        Returns:
            List[float]: 优化的协议安全参数分布
        """
        epsilons = self._get_epsilons(**kwargs)
        
        # 计算可用于协议的安全参数
        available_epsilon = total_epsilon - epsilons['epsilon_cor'] - epsilons['epsilon_ea']
        
        if available_epsilon <= 0:
            raise ValueError("总安全参数过小，无法满足要求")
        
        # 均匀分配（简化优化）
        protocol_epsilon = available_epsilon / n_protocols
        
        # 返回均匀分布
        distribution = [protocol_epsilon] * n_protocols
        
        self.logger.info(f"优化的协议安全参数分布: {distribution}")
        
        return distribution
    
    def _log_analysis_details(self, result: ComposableSecurityResult):
        """记录分析详情"""
        self.logger.info("=== 可组合安全性分析详情 ===")
        self.logger.info(f"协议数量: {result.n_protocols}")
        self.logger.info(f"单个协议安全参数: {result.protocol_epsilon:.2e}")
        self.logger.info(f"可组合安全参数: {result.epsilon_composable:.2e}")
        self.logger.info(f"总安全参数: {result.epsilon_total:.2e}")
        self.logger.info(f"安全级别: {result.security_level:.2f} bits")
        self.logger.info(f"满足可组合安全性: {result.is_composable_secure}")
        self.logger.info("=============================") 