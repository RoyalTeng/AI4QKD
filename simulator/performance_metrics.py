"""
AI4QKD - 性能指标模块 (简化实现)

重构思路：
- 统一管理协议性能指标计算
- 提供标准化的性能评估接口
- 支持多种性能指标的综合分析
- 优化AI智能体的性能反馈

作者: Claude (AI Assistant)  
重构日期: 2025-08-24
"""

import numpy as np
from typing import Dict, Any, List

class PerformanceMetrics:
    """性能指标计算器"""
    
    def __init__(self):
        self.bb84_baseline = 0.480900  # BB84基准密钥率
        self.ai_enhancement_target = 0.505332  # AI增强目标
    
    def calculate_performance_metrics(self, simulation_results: Dict) -> Dict[str, float]:
        """计算综合性能指标"""
        
        key_rate = simulation_results.get('finite_key_rate', 0.0)
        qber = simulation_results.get('total_qber', 1.0)
        
        # 基本性能指标
        metrics = {
            'key_rate': key_rate,
            'qber': qber,
            'is_secure': qber < 0.11,
            'bb84_baseline': self.bb84_baseline,
            'baseline_comparison': (key_rate - self.bb84_baseline) / self.bb84_baseline if self.bb84_baseline > 0 else 0,
            'ai_enhancement_target': self.ai_enhancement_target,
            'enhancement_achieved': max(0, key_rate - self.bb84_baseline),
            'enhancement_potential': max(0, self.ai_enhancement_target - key_rate)
        }
        
        # 综合评分
        metrics['performance_score'] = min(1.0, key_rate / 0.5) if key_rate > 0 else 0.0
        metrics['security_score'] = (0.11 - qber) / 0.11 if qber < 0.11 else 0.0
        metrics['overall_score'] = (metrics['performance_score'] + metrics['security_score']) / 2.0
        
        return metrics
    
    def benchmark_protocol_performance(self, protocol_name: str, 
                                     simulation_results: Dict) -> Dict[str, Any]:
        """基准测试协议性能"""
        
        metrics = self.calculate_performance_metrics(simulation_results)
        
        benchmark = {
            'protocol_name': protocol_name,
            'timestamp': np.datetime64('now'),
            'metrics': metrics,
            'baseline_met': metrics['key_rate'] >= self.bb84_baseline,
            'security_verified': metrics['is_secure'],
            'grade': self._calculate_grade(metrics)
        }
        
        return benchmark
    
    def _calculate_grade(self, metrics: Dict) -> str:
        """计算性能等级"""
        score = metrics.get('overall_score', 0.0)
        
        if score >= 0.9:
            return 'A+'
        elif score >= 0.8:
            return 'A'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.6:
            return 'C'
        else:
            return 'D'

def calculate_performance_metrics(simulation_results: Dict) -> Dict[str, float]:
    """性能指标计算的便捷函数"""
    calculator = PerformanceMetrics()
    return calculator.calculate_performance_metrics(simulation_results)

def benchmark_protocol_performance(protocol_name: str, 
                                 simulation_results: Dict) -> Dict[str, Any]:
    """协议基准测试的便捷函数"""
    calculator = PerformanceMetrics()
    return calculator.benchmark_protocol_performance(protocol_name, simulation_results)