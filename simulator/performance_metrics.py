"""
性能指标计算模块

实现了QKD协议的各种性能指标计算，包括：
- QBER（量子比特错误率）
- Gain（增益）
- Raw Key Rate（原始密钥率）
- 测量成功率
- 单光子概率估计
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class MetricType(Enum):
    """性能指标类型枚举"""
    QBER = "qber"                    # 量子比特错误率
    GAIN = "gain"                    # 增益
    RAW_KEY_RATE = "raw_key_rate"    # 原始密钥率
    DETECTION_RATE = "detection_rate" # 探测率
    SINGLE_PHOTON_RATE = "single_photon_rate"  # 单光子率
    SECRET_KEY_RATE = "secret_key_rate"        # 秘密密钥率


class PerformanceMetrics:
    """
    性能指标计算器
    
    实现了QKD协议的各种性能指标计算和分析。
    """
    
    def __init__(self):
        """初始化性能指标计算器"""
        pass
    
    def calculate_qber(self, 
                      alice_bits: List[int],
                      bob_bits: List[int]) -> float:
        """
        计算量子比特错误率（QBER）
        
        QBER = (错误比特数) / (总比特数)
        
        Args:
            alice_bits: Alice的比特序列
            bob_bits: Bob的比特序列
            
        Returns:
            QBER值
        """
        if len(alice_bits) != len(bob_bits):
            raise ValueError("比特序列长度不匹配")
        
        if len(alice_bits) == 0:
            return 0.0
        
        error_count = sum(1 for a, b in zip(alice_bits, bob_bits) if a != b)
        qber = error_count / len(alice_bits)
        
        return qber
    
    def calculate_gain(self, 
                      total_pulses: int,
                      detected_pulses: int) -> float:
        """
        计算增益（Gain）
        
        Gain = (探测到的脉冲数) / (总脉冲数)
        
        Args:
            total_pulses: 总脉冲数
            detected_pulses: 探测到的脉冲数
            
        Returns:
            增益值
        """
        if total_pulses == 0:
            return 0.0
        
        return detected_pulses / total_pulses
    
    def calculate_raw_key_rate(self, 
                              gain: float,
                              pulse_rate: float,
                              sifting_efficiency: float = 0.5) -> float:
        """
        计算原始密钥率
        
        Raw Key Rate = Gain × Pulse Rate × Sifting Efficiency
        
        Args:
            gain: 增益
            pulse_rate: 脉冲率（Hz）
            sifting_efficiency: 筛选效率
            
        Returns:
            原始密钥率（bit/s）
        """
        return gain * pulse_rate * sifting_efficiency
    
    def calculate_detection_rate(self, 
                                total_measurements: int,
                                successful_detections: int) -> float:
        """
        计算探测率
        
        Detection Rate = (成功探测次数) / (总测量次数)
        
        Args:
            total_measurements: 总测量次数
            successful_detections: 成功探测次数
            
        Returns:
            探测率
        """
        if total_measurements == 0:
            return 0.0
        
        return successful_detections / total_measurements
    
    def estimate_single_photon_probability(self, 
                                         photon_distribution: Dict[int, float]) -> float:
        """
        估计单光子概率
        
        Args:
            photon_distribution: 光子数分布
            
        Returns:
            单光子概率
        """
        return photon_distribution.get(1, 0.0)
    
    def calculate_secret_key_rate(self, 
                                 qber: float, 
                                 gain: float,
                                 f_ec: float = 1.16,
                                 protocol: str = "BB84") -> float:
        """
        计算秘密密钥率
        
        Secret Key Rate = Raw Key Rate × (1 - h(QBER)) × Privacy Amplification Factor
        
        其中 h(x) = -x log₂(x) - (1-x) log₂(1-x) 是二元熵函数
        
        Args:
            qber: 量子比特错误率
            gain: 增益
            f_ec: 纠错效率因子
            protocol: 协议类型
            
        Returns:
            秘密密钥率（bit/s）
        """
        if qber <= 0 or qber >= 1:
            return 0.0
        
        if protocol == "BB84":
            # GLLP公式
            shannon_term = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber) if 0 < qber < 1 else 0
            leak_ec = f_ec * shannon_term
            key_rate = gain * (1 - shannon_term - leak_ec)
            return max(0, key_rate)
        else:
            # 其他协议的实现
            return 0.0
    
    def calculate_finite_key_effects(self, 
                                   raw_key_length: int,
                                   qber: float,
                                   security_parameter: float = 1e-10) -> Dict[str, float]:
        """
        计算有限密钥效应
        
        Args:
            raw_key_length: 原始密钥长度
            qber: 量子比特错误率
            security_parameter: 安全参数
            
        Returns:
            有限密钥效应参数
        """
        # 处理边界情况
        if raw_key_length <= 0:
            return {
                "confidence_interval": float('inf'),
                "corrected_qber": qber,
                "key_reduction": 0.0,
                "final_key_length": 0.0
            }
        
        # 计算统计波动
        confidence_interval = np.sqrt(-np.log(security_parameter) / (2 * raw_key_length))
        
        # 修正的QBER
        corrected_qber = qber + confidence_interval
        
        # 密钥长度减少
        key_reduction = raw_key_length * confidence_interval
        
        return {
            "confidence_interval": confidence_interval,
            "corrected_qber": corrected_qber,
            "key_reduction": key_reduction,
            "final_key_length": max(0.0, raw_key_length - key_reduction)
        }
    
    def calculate_channel_capacity(self, 
                                  transmission: float,
                                  noise_rate: float) -> float:
        """
        计算信道容量
        
        Channel Capacity = log₂(1 + SNR)
        其中 SNR = (传输率) / (噪声率)
        
        Args:
            transmission: 传输率
            noise_rate: 噪声率
            
        Returns:
            信道容量（bit/use）
        """
        if noise_rate <= 0:
            return float('inf')
        
        snr = transmission / noise_rate
        if snr <= 0:
            return 0.0
        
        return np.log2(1 + snr)
    
    def calculate_secure_distance(self, 
                                 attenuation_coefficient: float,
                                 max_qber: float = 0.11) -> float:
        """
        计算安全传输距离
        
        Args:
            attenuation_coefficient: 衰减系数（dB/km）
            max_qber: 最大允许QBER
            
        Returns:
            安全传输距离（km）
        """
        # 简化模型：基于QBER阈值
        # 实际应用中需要更复杂的模型
        if attenuation_coefficient <= 0:
            return float('inf')
        
        # 假设QBER随距离指数增长
        # QBER = QBER₀ × exp(αL)
        # 其中 α 是衰减系数，L 是距离
        qber_0 = 0.01  # 初始QBER
        secure_distance = np.log(max_qber / qber_0) / attenuation_coefficient
        
        return max(0.0, secure_distance)
    
    def analyze_performance(self, 
                           simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合分析性能指标
        
        Args:
            simulation_results: 仿真结果字典
            
        Returns:
            性能分析结果
        """
        # 提取关键参数
        total_pulses = simulation_results.get("total_pulses", 0)
        detected_pulses = simulation_results.get("detected_pulses", 0)
        alice_bits = simulation_results.get("alice_bits", [])
        bob_bits = simulation_results.get("bob_bits", [])
        pulse_rate = simulation_results.get("pulse_rate", 1e9)  # 1 GHz
        photon_distribution = simulation_results.get("photon_distribution", {})
        
        # 计算各项指标
        gain = self.calculate_gain(total_pulses, detected_pulses)
        qber = self.calculate_qber(alice_bits, bob_bits)
        raw_key_rate = self.calculate_raw_key_rate(gain, pulse_rate)
        secret_key_rate = self.calculate_secret_key_rate(qber, gain)
        single_photon_prob = self.estimate_single_photon_probability(photon_distribution)
        
        # 有限密钥效应
        finite_key_effects = self.calculate_finite_key_effects(
            len(alice_bits), qber
        )
        
        return {
            "gain": gain,
            "qber": qber,
            "raw_key_rate": raw_key_rate,
            "secret_key_rate": secret_key_rate,
            "single_photon_probability": single_photon_prob,
            "detection_rate": detected_pulses / max(1, total_pulses),
            "finite_key_effects": finite_key_effects,
            "total_pulses": total_pulses,
            "detected_pulses": detected_pulses,
            "raw_key_length": len(alice_bits),
            "final_key_length": finite_key_effects["final_key_length"]
        }
    
    def generate_performance_report(self, 
                                   analysis_results: Dict[str, Any]) -> str:
        """
        生成性能报告
        
        Args:
            analysis_results: 性能分析结果
            
        Returns:
            格式化的性能报告
        """
        report = []
        report.append("=" * 50)
        report.append("QKD协议性能分析报告")
        report.append("=" * 50)
        
        # 基本统计
        report.append(f"总脉冲数: {analysis_results.get('total_pulses', 0):,}")
        report.append(f"探测脉冲数: {analysis_results.get('detected_pulses', 0):,}")
        report.append(f"原始密钥长度: {analysis_results.get('raw_key_length', 0):,}")
        
        # 性能指标
        report.append("\n性能指标:")
        report.append(f"  增益 (Gain): {analysis_results.get('gain', 0):.6f}")
        report.append(f"  量子比特错误率 (QBER): {analysis_results.get('qber', 0):.6f}")
        report.append(f"  探测率: {analysis_results.get('detection_rate', 0):.6f}")
        report.append(f"  单光子概率: {analysis_results.get('single_photon_probability', 0):.6f}")
        
        # 密钥率
        report.append("\n密钥率:")
        report.append(f"  原始密钥率: {analysis_results.get('raw_key_rate', 0):.2f} bit/s")
        report.append(f"  秘密密钥率: {analysis_results.get('secret_key_rate', 0):.2f} bit/s")
        
        # 有限密钥效应
        finite_effects = analysis_results.get('finite_key_effects', {})
        if finite_effects:
            report.append("\n有限密钥效应:")
            report.append(f"  置信区间: {finite_effects.get('confidence_interval', 0):.6f}")
            report.append(f"  修正QBER: {finite_effects.get('corrected_qber', 0):.6f}")
            report.append(f"  密钥长度减少: {finite_effects.get('key_reduction', 0):.0f}")
            report.append(f"  最终密钥长度: {finite_effects.get('final_key_length', 0):.0f}")
        
        report.append("=" * 50)
        
        return "\n".join(report) 