"""
密钥率计算模块（通用版本）

基于信息论的通用QKD协议密钥率计算。支持任意协议结构的安全密钥率分析。

新功能（v2.0）：
- 基于信息论的通用密钥率公式 R = I(A:B) - χ(A:E) - δ(n) - ε
- 协议无关的互信息和Holevo信息计算
- 现代量子密码学理论集成
- 完全向后兼容的接口

支持的协议：
- 传统协议：BB84、诱骗态BB84、MDI-QKD
- 任意AI生成的新颖协议结构

参考文献：
- Renner, R. (2008). Security of quantum key distribution
- Tomamichel, M., et al. (2012). Tight finite-key analysis for quantum cryptography
- Lim, C. C. W., et al. (2014). Concise security bounds for practical decoy-state quantum key distribution
- Renner & Wolf (2023): Quantum Advantage in Cryptography
- Metger et al. (2024): Generalised Entropy Accumulation
"""

import numpy as np
import logging
import warnings
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
from .ac_framework import ProtocolType, SecurityParameters

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

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class KeyRateParameters:
    """密钥率计算参数"""
    # 基础参数
    qber: float  # 量子比特错误率
    gain: float  # 信道增益
    n_pulses: int  # 发送脉冲数量
    
    # 诱骗态参数（仅诱骗态协议）
    mu_signal: float = 0.5  # 信号态强度
    mu_decoy1: float = 0.1  # 诱骗态1强度
    mu_decoy2: float = 0.0  # 诱骗态2强度（真空态）
    p_signal: float = 0.7   # 信号态概率
    p_decoy1: float = 0.2   # 诱骗态1概率
    p_decoy2: float = 0.1   # 诱骗态2概率
    
    # 安全参数
    security_params: SecurityParameters = field(default_factory=SecurityParameters)
    
    # 纠错参数
    f_ec: float = 1.16  # 纠错效率因子
    
    # 有限密钥参数
    n_raw: Optional[int] = None  # 原始密钥长度
    n_final: Optional[int] = None  # 最终密钥长度


@dataclass
class KeyRateResult:
    """密钥率计算结果（通用版本）"""
    # 最终结果
    final_key_rate: float  # 最终密钥率 (bit/pulse)
    final_key_length: int  # 最终密钥长度
    
    # 中间计算结果
    raw_key_rate: float    # 原始密钥率
    secret_key_rate: float # 秘密密钥率
    privacy_amplification_rate: float  # 隐私放大率
    
    # 各项贡献
    h_min: float          # 最小熵 H_min(X|E)
    leak_ec: float        # 纠错泄露
    leak_pe: float        # 参数估计泄露
    leak_sk: float        # 安全密钥泄露
    
    # 有限密钥效应
    delta_1: float        # 参数估计误差项
    delta_2: float        # 统计波动项
    
    # 协议特定参数（向后兼容）
    protocol_type: Optional[ProtocolType] = None
    parameters: Optional[KeyRateParameters] = None
    
    # 通用框架结果（新增）
    mutual_information: float = 0.0      # 互信息 I(A:B)
    holevo_information: float = 0.0      # Holevo信息 χ(A:E)
    finite_key_correction: float = 0.0   # 有限密钥修正 δ(n)
    protocol_features: Optional[Any] = None
    
    # 计算详情
    calculation_details: Dict[str, float] = field(default_factory=dict)


class KeyRateCalculator:
    """
    密钥率计算器
    
    基于抽象密码学框架计算QKD协议的安全密钥率。
    支持有限密钥分析和多种协议类型。
    """
    
    def __init__(self,
                 qber: Optional[float] = None,
                 gain: Optional[float] = None,
                 protocol_type: ProtocolType = ProtocolType.BB84,
                 params: Optional[Dict] = None,
                 config: Optional[Dict] = None):
        """
        初始化密钥率计算器
        
        Args:
            qber: 量子比特错误率
            gain: 信道增益
            protocol_type: 协议类型
            params: 其他协议特定参数
            config: 配置参数字典
        """
        self.config = config or {}
        self.qber = qber
        self.gain = gain
        self.protocol_type = protocol_type
        self.params = params or {}
        self.logger = logging.getLogger(f"{__name__}.KeyRateCalculator")
        
        # 设置默认参数
        self.default_params = {
            'epsilon_sec': 1e-10,
            'epsilon_cor': 1e-10, 
            'epsilon_pe': 1e-10,
            'f_ec': 1.16,
            'mu_signal': 0.5,
            'mu_decoy1': 0.1,
            'mu_decoy2': 0.0,
            'p_signal': 0.7,
            'p_decoy1': 0.2,
            'p_decoy2': 0.1
        }
        
        # 更新默认参数
        self.default_params.update(self.config)
        self.default_params.update(self.params)
        
    def calculate_key_rate(self) -> float:
        """
        计算密钥率
        
        Returns:
            float: 最终密钥率 (bit/pulse)
        """
        if self.qber is None or self.gain is None:
            raise ValueError("必须提供QBER和Gain才能计算密钥率。")

        # 从参数中获取 n_pulses，如果不存在则使用一个大的默认值
        n_pulses = self.default_params.get('n_pulses', 10**12)

        result = self.compute(
            qber=self.qber,
            gain=self.gain,
            n_pulses=n_pulses,
            protocol_type=self.protocol_type,
            **self.default_params
        )
        return result.final_key_rate
    
    def compute(self, 
                qber: float,
                gain: float, 
                n_pulses: int,
                protocol_type: ProtocolType = ProtocolType.BB84,
                **kwargs) -> KeyRateResult:
        """
        计算密钥率（向后兼容接口）
        
        Args:
            qber: 量子比特错误率
            gain: 信道增益
            n_pulses: 发送脉冲数量
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            KeyRateResult: 密钥率计算结果
        """
        # 参数验证
        if not (0 <= qber < 1):
             raise ValueError(f"QBER必须在[0, 1)范围内，当前值: {qber}")
        if gain < 0:
            raise ValueError(f"增益必须大于等于0，当前值: {gain}")
        if n_pulses <= 0:
            raise ValueError(f"脉冲数量必须大于0，当前值: {n_pulses}")

        # 如果QBER过高，物理上无法产生安全密钥，直接返回零速率
        if qber >= 0.5:
            self.logger.warning(f"QBER ({qber:.4f}) >= 0.5，物理上无法生成安全密钥。返回零密钥率。")
            params = self._build_parameters(qber, gain, n_pulses, protocol_type, **kwargs)
            return KeyRateResult(
                final_key_rate=0.0, final_key_length=0,
                raw_key_rate=0, secret_key_rate=0, privacy_amplification_rate=0,
                h_min=0, leak_ec=0, leak_pe=0, leak_sk=0,
                delta_1=0, delta_2=0, protocol_type=protocol_type,
                parameters=params, calculation_details={'error': 'QBER >= 0.5'}
            )

        self.logger.info(f"开始计算{protocol_type.value}协议密钥率")
        self.logger.info(f"输入参数: QBER={qber:.4f}, Gain={gain:.4f}, N_pulses={n_pulses}")
        
        # 构建参数对象
        params = self._build_parameters(qber, gain, n_pulses, protocol_type, **kwargs)
        
        # 根据协议类型选择计算方法
        if protocol_type == ProtocolType.BB84:
            result = self._compute_bb84_key_rate(params)
        elif protocol_type == ProtocolType.MDI_QKD:
            result = self._compute_mdi_qkd_key_rate(params)
        elif protocol_type == ProtocolType.DECOY_BB84:
            result = self._compute_decoy_bb84_key_rate(params)
        else:
            raise ValueError(f"不支持的协议类型: {protocol_type}")
            
        self.logger.info(f"密钥率计算完成: {result.final_key_rate:.6f} bit/pulse")
        return result
    
    # ==================== 通用密钥率计算方法（新增） ====================
    
    def compute_universal(self,
                         simulation_results: Dict[str, Any],
                         protocol_features,
                         security_params) -> KeyRateResult:
        """
        通用密钥率计算方法
        
        基于信息论的通用公式：R = I(A:B) - χ(A:E) - δ(n) - ε
        
        Args:
            simulation_results: 仿真结果数据
            protocol_features: 协议特征描述
            security_params: 通用安全参数
            
        Returns:
            KeyRateResult: 密钥率计算结果
        """
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework not available")
        
        self.logger.info(f"开始通用密钥率计算: {protocol_features.name}")
        
        # 1. 计算互信息 I(A:B)
        mutual_information = self.compute_mutual_information(simulation_results, protocol_features)
        
        # 2. 计算Holevo信息 χ(A:E)  
        holevo_information = self.compute_holevo_information(simulation_results, protocol_features)
        
        # 3. 计算有限密钥修正 δ(n)
        n_pulses = simulation_results.get('channel_statistics', {}).get('total_pulses', 1000000)
        finite_key_correction = self.compute_finite_key_correction(n_pulses, security_params)
        
        # 4. 应用通用密钥率公式
        secret_key_rate = (mutual_information - 
                          holevo_information - 
                          finite_key_correction - 
                          security_params.epsilon_sec)
        
        # 确保非负
        final_key_rate = max(0.0, secret_key_rate)
        
        # 5. 计算其他统计量
        raw_stats = simulation_results.get('raw_statistics', {})
        channel_stats = simulation_results.get('channel_statistics', {})
        
        gain = channel_stats.get('transmission_probability', 0.5)
        n_final = int(n_pulses * final_key_rate)
        
        # 计算传统兼容量
        h_min = mutual_information
        leak_ec = holevo_information * 0.5  # 近似纠错泄露
        leak_pe = finite_key_correction * 0.3  # 近似参数估计泄露
        leak_sk = finite_key_correction * 0.7  # 近似安全密钥泄露
        
        # 6. 构建结果
        result = KeyRateResult(
            final_key_rate=final_key_rate,
            final_key_length=n_final,
            raw_key_rate=gain,
            secret_key_rate=secret_key_rate,
            privacy_amplification_rate=mutual_information - holevo_information,
            h_min=h_min,
            leak_ec=leak_ec,
            leak_pe=leak_pe,
            leak_sk=leak_sk,
            delta_1=finite_key_correction * 0.3,
            delta_2=finite_key_correction * 0.7,
            # 通用框架特定结果
            mutual_information=mutual_information,
            holevo_information=holevo_information,
            finite_key_correction=finite_key_correction,
            protocol_features=protocol_features,
            calculation_details={
                'mutual_information': mutual_information,
                'holevo_information': holevo_information,
                'finite_key_correction': finite_key_correction,
                'security_epsilon': security_params.epsilon_sec,
                'n_pulses': n_pulses,
                'gain': gain
            }
        )
        
        self._log_universal_calculation_details(result)
        return result
    
    def compute_mutual_information(self,
                                  simulation_results: Dict[str, Any],
                                  protocol_features) -> float:
        """
        计算Alice和Bob之间的互信息 I(A:B)
        
        基于仿真结果计算实际的信息论互信息。
        
        Args:
            simulation_results: 仿真结果数据
            protocol_features: 协议特征
            
        Returns:
            float: 互信息值 (bits)
        """
        raw_stats = simulation_results.get('raw_statistics', {})
        
        alice_bits = raw_stats.get('alice_bits', [])
        bob_bits = raw_stats.get('bob_bits', [])
        alice_bases = raw_stats.get('alice_bases', [])
        bob_bases = raw_stats.get('bob_bases', [])
        detections = raw_stats.get('detections', [])
        
        if not all([alice_bits, bob_bits, alice_bases, bob_bases, detections]):
            # 回退到理论计算
            return self._compute_theoretical_mutual_information(simulation_results)
        
        # 过滤有效的检测事件和匹配基
        valid_data = []
        for i in range(min(len(alice_bits), len(bob_bits), len(detections))):
            if (detections[i] and 
                i < len(alice_bases) and i < len(bob_bases) and
                alice_bases[i] == bob_bases[i]):  # 基匹配
                valid_data.append((alice_bits[i], bob_bits[i]))
        
        if len(valid_data) < 10:  # 数据不足
            return self._compute_theoretical_mutual_information(simulation_results)
        
        # 计算联合概率分布
        joint_counts = {'00': 0, '01': 0, '10': 0, '11': 0}
        for a_bit, b_bit in valid_data:
            key = f'{a_bit}{b_bit}'
            joint_counts[key] += 1
        
        n_total = len(valid_data)
        joint_probs = {k: v/n_total for k, v in joint_counts.items()}
        
        # 计算边缘概率
        p_a0 = joint_probs['00'] + joint_probs['01']
        p_a1 = joint_probs['10'] + joint_probs['11'] 
        p_b0 = joint_probs['00'] + joint_probs['10']
        p_b1 = joint_probs['01'] + joint_probs['11']
        
        # 计算互信息 I(A:B) = Σ p(a,b) log2[p(a,b)/(p(a)p(b))]
        mutual_info = 0.0
        for ab, p_ab in joint_probs.items():
            if p_ab > 0:
                a, b = int(ab[0]), int(ab[1])
                p_a = p_a1 if a else p_a0
                p_b = p_b1 if b else p_b0
                
                if p_a > 0 and p_b > 0:
                    mutual_info += p_ab * np.log2(p_ab / (p_a * p_b))
        
        self.logger.debug(f"互信息计算: I(A:B) = {mutual_info:.6f} bits")
        return max(0.0, mutual_info)
    
    def compute_holevo_information(self,
                                  simulation_results: Dict[str, Any],
                                  protocol_features) -> float:
        """
        计算窃听者的Holevo信息 χ(A:E)
        
        基于信道模型估计窃听者可获得的信息上界。
        
        Args:
            simulation_results: 仿真结果数据
            protocol_features: 协议特征
            
        Returns:
            float: Holevo信息值 (bits)
        """
        channel_stats = simulation_results.get('channel_statistics', {})
        error_prob = channel_stats.get('error_probability', 0.0)
        
        # 对于标准的攻击模型，Holevo信息约等于错误率的二元熵
        if error_prob <= 0 or error_prob >= 1:
            return 0.0
        
        # 计算二元熵 h(p) = -p*log2(p) - (1-p)*log2(1-p)
        if error_prob >= 0.5:
            # 高错误率情况，使用1-p
            p = 1.0 - error_prob
        else:
            p = error_prob
            
        if p <= 0:
            holevo_info = 0.0
        else:
            holevo_info = -p * np.log2(p) - (1-p) * np.log2(1-p)
        
        # 应用协议特定的修正因子
        if hasattr(protocol_features, 'name'):
            if 'MDI' in protocol_features.name:
                holevo_info *= 0.8  # MDI-QKD的窃听信息较少
            elif 'decoy' in protocol_features.name.lower():
                holevo_info *= 0.9  # 诱骗态提供额外安全性
        
        self.logger.debug(f"Holevo信息计算: χ(A:E) = {holevo_info:.6f} bits")
        return max(0.0, holevo_info)
    
    def compute_finite_key_correction(self,
                                    n_pulses: int,
                                    security_params) -> float:
        """
        计算有限密钥修正项 δ(n)
        
        基于现代有限密钥分析理论。
        
        Args:
            n_pulses: 脉冲数量
            security_params: 安全参数
            
        Returns:
            float: 有限密钥修正值 (bits per pulse)
        """
        if n_pulses <= 0:
            return float('inf')
        
        # 基于Tomamichel et al. 2012的紧致分析
        # δ(n) ≈ sqrt(log(1/ε) / (2n))
        
        # 主要的安全参数贡献
        eps_total = (security_params.epsilon_sec + 
                    security_params.epsilon_cor + 
                    security_params.epsilon_pe)
        
        if eps_total <= 0:
            eps_total = 1e-12  # 防止log(0)
        
        # 有限密钥修正的平方根渐近行为
        correction = np.sqrt(np.log(1 / eps_total) / (2 * n_pulses))
        
        # 添加额外的熵平滑和可组合性修正
        if hasattr(security_params, 'entropy_smoothing_param'):
            smoothing_correction = np.sqrt(np.log(1 / security_params.entropy_smoothing_param) / n_pulses)
            correction += smoothing_correction
        
        if hasattr(security_params, 'composability_param'):
            composability_correction = np.sqrt(np.log(1 / security_params.composability_param) / n_pulses)
            correction += composability_correction * 0.5
        
        self.logger.debug(f"有限密钥修正: δ(n) = {correction:.6f} bits/pulse")
        return correction
    
    def _compute_theoretical_mutual_information(self, simulation_results: Dict[str, Any]) -> float:
        """计算理论互信息（当仿真数据不足时）"""
        channel_stats = simulation_results.get('channel_statistics', {})
        error_prob = channel_stats.get('error_probability', 0.05)
        
        # 对于二元对称信道，I(A:B) = 1 - h(error_prob)
        if error_prob <= 0:
            return 1.0
        elif error_prob >= 0.5:
            return 0.0
        else:
            h_error = -error_prob * np.log2(error_prob) - (1-error_prob) * np.log2(1-error_prob)
            return 1.0 - h_error
    
    def _log_universal_calculation_details(self, result: KeyRateResult):
        """记录通用计算详情"""
        self.logger.info("=== 通用密钥率计算详情 ===")
        if result.protocol_features:
            self.logger.info(f"协议: {result.protocol_features.name}")
        self.logger.info(f"最终密钥率: {result.final_key_rate:.6f} bit/pulse")
        self.logger.info(f"互信息 I(A:B): {result.mutual_information:.6f}")
        self.logger.info(f"Holevo信息 χ(A:E): {result.holevo_information:.6f}")
        self.logger.info(f"有限密钥修正 δ(n): {result.finite_key_correction:.6f}")
        self.logger.info(f"安全密钥率: {result.secret_key_rate:.6f}")
        self.logger.info("==========================")
    
    # ==================== 向后兼容性辅助方法 ====================
    
    def _compute_via_universal_framework(self, params: KeyRateParameters, protocol_name: str) -> KeyRateResult:
        """
        通过通用框架计算密钥率（向后兼容辅助方法）
        
        将传统参数转换为通用框架格式并计算。
        """
        # 构造仿真结果
        simulation_results = {
            'raw_statistics': {
                'alice_bits': [],
                'bob_bits': [],
                'alice_bases': [],
                'bob_bases': [],
                'detections': []
            },
            'channel_statistics': {
                'transmission_probability': params.gain,
                'error_probability': params.qber,
                'total_pulses': params.n_pulses
            }
        }
        
        # 选择协议特征
        if protocol_name == 'BB84':
            protocol_features = create_bb84_protocol()
        elif protocol_name == 'MDI_QKD':
            protocol_features = create_mdi_qkd_protocol()
        elif protocol_name == 'DECOY_BB84':
            protocol_features = create_decoy_bb84_protocol()
        else:
            raise ValueError(f"Unknown protocol: {protocol_name}")
        
        # 转换安全参数
        universal_security_params = UniversalSecurityParameters(
            epsilon_sec=params.security_params.epsilon_sec,
            epsilon_cor=params.security_params.epsilon_cor,
            epsilon_pe=params.security_params.epsilon_pe,
            entropy_smoothing_param=params.security_params.epsilon_bar,
            composability_param=params.security_params.epsilon_sec * 0.1,
            finite_key_param=params.security_params.epsilon_rob
        )
        
        # 使用通用框架计算
        return self.compute_universal(simulation_results, protocol_features, universal_security_params)
    
    def convert_legacy_to_universal(self, 
                                   qber: float,
                                   gain: float,
                                   n_pulses: int,
                                   protocol_type: ProtocolType) -> Tuple[Dict, Any, Any]:
        """
        将传统参数转换为通用框架格式
        
        这是一个公共辅助方法，帮助用户迁移到新的通用接口。
        
        Args:
            qber: 量子比特错误率
            gain: 信道增益
            n_pulses: 脉冲数量
            protocol_type: 协议类型
            
        Returns:
            Tuple[simulation_results, protocol_features, security_params]
        """
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework not available")
        
        # 构造基本仿真结果
        simulation_results = {
            'raw_statistics': {
                'alice_bits': [],
                'bob_bits': [],
                'alice_bases': [],
                'bob_bases': [],
                'detections': []
            },
            'channel_statistics': {
                'transmission_probability': gain,
                'error_probability': qber,
                'total_pulses': n_pulses
            }
        }
        
        # 根据协议类型选择特征
        protocol_map = {
            ProtocolType.BB84: create_bb84_protocol,
            ProtocolType.MDI_QKD: create_mdi_qkd_protocol,
            ProtocolType.DECOY_BB84: create_decoy_bb84_protocol
        }
        
        if protocol_type in protocol_map:
            protocol_features = protocol_map[protocol_type]()
        else:
            # 创建通用协议特征
            protocol_features = ProtocolFeatures(
                name=protocol_type.value,
                operations=[],
                parties=['Alice', 'Bob']
            )
        
        # 默认安全参数
        security_params = UniversalSecurityParameters(
            epsilon_sec=1e-10,
            epsilon_cor=1e-10,
            epsilon_pe=1e-10,
            entropy_smoothing_param=1e-8,
            composability_param=1e-9,
            finite_key_param=1e-7
        )
        
        return simulation_results, protocol_features, security_params
    
    def _build_parameters(self, 
                         qber: float,
                         gain: float,
                         n_pulses: int,
                         protocol_type: ProtocolType,
                         **kwargs) -> KeyRateParameters:
        """构建参数对象"""
        # 1. 收集所有参数
        all_params = self.default_params.copy()
        all_params.update(kwargs)
        all_params.update({
            'qber': qber,
            'gain': gain,
            'n_pulses': n_pulses
        })

        # 2. 创建 SecurityParameters 实例
        # 从 all_params 中提取 epsilon 相关参数
        sec_param_keys = [k for k in all_params if k.startswith('epsilon_')]
        sec_param_dict = {}
        for key in sec_param_keys:
            # 适配 ac_framework.py 中的命名
            if key == "epsilon_e": 
                sec_param_dict["epsilon_pe"] = all_params.pop(key)
            elif key in SecurityParameters.__annotations__:
                 sec_param_dict[key] = all_params.pop(key)
        
        security_params = SecurityParameters(**sec_param_dict)
        
        # 3. 创建 KeyRateParameters 实例
        # 移除已用于 SecurityParameters 的键后，剩下的传递给 KeyRateParameters
        key_rate_params_dict = {
            k: v for k, v in all_params.items() 
            if k in KeyRateParameters.__annotations__
        }
        key_rate_params_dict['security_params'] = security_params
        
        return KeyRateParameters(**key_rate_params_dict)
    
    def _compute_bb84_key_rate(self, params: KeyRateParameters) -> KeyRateResult:
        """
        计算BB84协议密钥率（向后兼容接口）
        
        基于Renner 2008的抽象密码学框架
        
        警告：此方法已重构为使用通用框架。建议使用 compute_universal() 方法。
        """
        warnings.warn(
            "_compute_bb84_key_rate is deprecated. Use compute_universal() with BB84 protocol features.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # 尝试使用通用框架
        if _UNIVERSAL_FRAMEWORK_AVAILABLE:
            return self._compute_via_universal_framework(params, 'BB84')
        
        # 回退到传统实现
        self.logger.info("使用BB84协议计算密钥率（传统方法）")
        
        # 1. 计算原始密钥率
        raw_key_rate = params.gain * (1 - params.qber)
        
        # 2. 计算最小熵 H_min(X|E)
        # 基于Renner 2008, H_min(X|E) ≥ 1 - h(QBER)
        h_min = self._calculate_min_entropy_bb84(params.qber)
        
        # 3. 计算纠错泄露
        leak_ec = params.f_ec * params.qber * params.gain
        
        # 4. 计算有限密钥效应
        delta_1, delta_2 = self._calculate_finite_key_effects(params)
        
        # 5. 计算秘密密钥率
        # R = H_min(X|E) - leak_ec - leak_pe - leak_sk - finite_key_terms
        leak_pe = delta_1  # 参数估计泄露
        leak_sk = delta_2  # 安全密钥泄露
        
        secret_key_rate = h_min - leak_ec - leak_pe - leak_sk
        
        # 确保非负
        secret_key_rate = max(0, secret_key_rate)
        
        # 6. 计算最终密钥率
        final_key_rate = secret_key_rate * params.gain
        
        # 7. 计算密钥长度
        n_raw = int(params.n_pulses * params.gain)
        n_final = int(n_raw * secret_key_rate)
        
        # 8. 构建结果
        result = KeyRateResult(
            final_key_rate=final_key_rate,
            final_key_length=n_final,
            raw_key_rate=raw_key_rate,
            secret_key_rate=secret_key_rate,
            privacy_amplification_rate=secret_key_rate,
            h_min=h_min,
            leak_ec=leak_ec,
            leak_pe=leak_pe,
            leak_sk=leak_sk,
            delta_1=delta_1,
            delta_2=delta_2,
            protocol_type=ProtocolType.BB84,
            parameters=params,
            calculation_details={
                'raw_key_rate': raw_key_rate,
                'h_min': h_min,
                'leak_ec': leak_ec,
                'leak_pe': leak_pe,
                'leak_sk': leak_sk,
                'secret_key_rate': secret_key_rate,
                'n_raw': n_raw,
                'n_final': n_final
            }
        )
        
        self._log_calculation_details(result)
        return result
    
    def _compute_decoy_bb84_key_rate(self, params: KeyRateParameters) -> KeyRateResult:
        """
        计算诱骗态BB84协议的密钥率（向后兼容接口）
        
        警告：此方法已重构为使用通用框架。建议使用 compute_universal() 方法。
        """
        warnings.warn(
            "_compute_decoy_bb84_key_rate is deprecated. Use compute_universal() with decoy BB84 protocol features.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # 尝试使用通用框架
        if _UNIVERSAL_FRAMEWORK_AVAILABLE:
            return self._compute_via_universal_framework(params, 'DECOY_BB84')
        
        # 回退到传统实现
        self.logger.info("使用诱骗态BB84协议的简化模型计算密钥率（传统方法）")

        # 从参数中获取信号态的仿真结果 (这是个简化，真实情况下需要从多组结果中估算)
        qber_signal = params.qber # 直接使用传入的整体qber作为信号态qber的估计
        gain_signal = params.gain # 同上

        # 假设我们通过诱骗态分析，完美得到了单光子产率Y1和单光子误码率e1
        # 在此简化模型中，我们用信号态的增益和QBER来近似
        # TODO: 未来应实现完整的GLLP估算过程
        yield_1 = gain_signal  # Y1的粗略估计
        error_rate_1 = qber_signal # e1的粗略估计

        if error_rate_1 <= 0 or error_rate_1 >= 0.5:
            h_e1 = 0
        else:
            h_e1 = -error_rate_1 * np.log2(error_rate_1) - (1 - error_rate_1) * np.log2(1 - error_rate_1)

        # 纠错泄露
        leak_ec = params.f_ec * h_e1

        # 最终密钥率 (bit per pulse)
        # R ≈ Y1 * (1 - h(e1)) - Q_signal * f_ec * h(Q_signal)
        # 这是一个更常见的简化公式
        final_key_rate = yield_1 * (1 - h_e1) - gain_signal * leak_ec
        final_key_rate = max(0, final_key_rate)
        
        n_final = int(params.n_pulses * final_key_rate)
        
        return KeyRateResult(
            final_key_rate=final_key_rate,
            final_key_length=n_final,
            raw_key_rate=gain_signal,
            secret_key_rate=final_key_rate / gain_signal if gain_signal > 0 else 0,
            privacy_amplification_rate=1-h_e1,
            h_min=(1 - h_e1),
            leak_ec=leak_ec,
            leak_pe=0, # 简化模型未考虑
            leak_sk=0, # 简化模型未考虑
            delta_1=0,
            delta_2=0,
            protocol_type=ProtocolType.DECOY_BB84,
            parameters=params,
            calculation_details={
                'yield_1': yield_1,
                'error_rate_1': error_rate_1,
                'h_e1': h_e1,
                'leak_ec': leak_ec
            }
        )
    
    def _compute_mdi_qkd_key_rate(self, params: KeyRateParameters) -> KeyRateResult:
        """
        计算MDI-QKD协议的密钥率（向后兼容接口）
        
        警告：此方法已重构为使用通用框架。建议使用 compute_universal() 方法。
        """
        warnings.warn(
            "_compute_mdi_qkd_key_rate is deprecated. Use compute_universal() with MDI-QKD protocol features.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # 尝试使用通用框架
        if _UNIVERSAL_FRAMEWORK_AVAILABLE:
            return self._compute_via_universal_framework(params, 'MDI_QKD')
        
        # 回退到传统实现
        self.logger.info("使用MDI-QKD协议的简化模型计算密钥率（传统方法）")

        # 使用总的QBER和Gain作为单光子参数的粗略估计
        # TODO: 未来应从仿真器获取更精确的 e_11 和 gain_11
        qber_11 = params.qber
        gain_11 = params.gain

        if qber_11 <= 0 or qber_11 >= 0.5:
            h_e11 = 0
        else:
            h_e11 = -qber_11 * np.log2(qber_11) - (1 - qber_11) * np.log2(1 - qber_11)
        
        # 纠错泄露
        leak_ec = params.f_ec * h_e11

        # 秘密密钥率 (bit per successful BSM event)
        secret_key_rate_per_event = (1 - h_e11) - leak_ec
        secret_key_rate_per_event = max(0, secret_key_rate_per_event)

        # 最终密钥率 (bit per pulse)
        final_key_rate = gain_11 * secret_key_rate_per_event
        
        n_final = int(params.n_pulses * final_key_rate)

        # 构建结果对象
        return KeyRateResult(
            final_key_rate=final_key_rate,
            final_key_length=n_final,
            raw_key_rate=params.gain,
            secret_key_rate=secret_key_rate_per_event,
            privacy_amplification_rate=secret_key_rate_per_event,
            h_min=(1 - h_e11),
            leak_ec=leak_ec,
            leak_pe=0, # 简化模型未考虑
            leak_sk=0, # 简化模型未考虑
            delta_1=0,
            delta_2=0,
            protocol_type=ProtocolType.MDI_QKD,
            parameters=params,
            calculation_details={
                'estimated_qber_11': qber_11,
                'estimated_gain_11': gain_11,
                'h_e11': h_e11,
                'leak_ec': leak_ec
            }
        )
    
    def _calculate_min_entropy_bb84(self, qber: float) -> float:
        """
        计算BB84协议的最小熵 H_min(X|E)
        
        基于Renner 2008: H_min(X|E) ≥ 1 - h(QBER)
        其中 h(x) = -x*log2(x) - (1-x)*log2(1-x) 是二元熵函数
        """
        if qber <= 0 or qber >= 0.5:
            return 0.0
            
        # 二元熵函数
        h_qber = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
        h_min = 1 - h_qber
        
        self.logger.debug(f"BB84最小熵计算: QBER={qber:.4f}, h(QBER)={h_qber:.4f}, H_min={h_min:.4f}")
        return h_min
    
    def _calculate_min_entropy_decoy(self, q_1: float, e_1: float, params: KeyRateParameters) -> float:
        """
        计算诱骗态协议的最小熵
        
        基于Lim et al. 2014的紧致分析
        """
        if e_1 <= 0 or e_1 >= 0.5:
            return 0.0
            
        # 单光子错误率的二元熵
        h_e1 = -e_1 * np.log2(e_1) - (1 - e_1) * np.log2(1 - e_1)
        
        # 最小熵 H_min(X|E) ≥ q_1 * (1 - h(e_1))
        h_min = q_1 * (1 - h_e1)
        
        self.logger.debug(f"诱骗态最小熵计算: q_1={q_1:.6f}, e_1={e_1:.4f}, h(e_1)={h_e1:.4f}, H_min={h_min:.6f}")
        return h_min
    
    def _calculate_gain_for_intensity(self, mu: float, gain: float) -> float:
        """
        计算给定强度下的增益
        
        假设增益与强度成正比（简化模型）
        """
        return gain * mu / 0.5  # 归一化到标准强度0.5
    
    def _estimate_single_photon_parameters(self, 
                                         q_signal: float, 
                                         q_decoy1: float, 
                                         q_decoy2: float,
                                         mu_signal: float,
                                         mu_decoy1: float, 
                                         mu_decoy2: float) -> Tuple[float, float]:
        """
        估计单光子增益和错误率
        
        基于诱骗态方法（Ma et al. 2005）
        """
        # 简化的单光子参数估计
        # 实际应用中需要更复杂的数值方法
        
        # 估计单光子增益
        q_1 = max(0, (q_signal - q_decoy2) / (mu_signal - mu_decoy2))
        
        # 估计单光子错误率（简化）
        e_1 = 0.02  # 假设单光子错误率为2%
        
        self.logger.debug(f"单光子参数估计: q_1={q_1:.6f}, e_1={e_1:.4f}")
        return q_1, e_1
    
    def _calculate_finite_key_effects(self, params: KeyRateParameters) -> Tuple[float, float]:
        """
        计算有限密钥效应
        
        基于Tomamichel et al. 2012
        """
        n = params.n_pulses
        
        # 参数估计误差项
        delta_1 = np.sqrt(np.log(1 / params.security_params.epsilon_pe) / (2 * n))
        
        # 统计波动项
        delta_2 = np.sqrt(np.log(1 / params.security_params.epsilon_sec) / (2 * n))
        
        self.logger.debug(f"有限密钥效应: delta_1={delta_1:.6f}, delta_2={delta_2:.6f}")
        return delta_1, delta_2
    
    def _calculate_finite_key_effects_decoy(self, params: KeyRateParameters) -> Tuple[float, float]:
        """
        计算诱骗态协议的有限密钥效应
        
        基于Lim et al. 2014的紧致分析
        """
        n = params.n_pulses
        
        # 更紧致的有限密钥效应
        # 考虑诱骗态统计
        n_signal = int(n * params.p_signal)
        n_decoy1 = int(n * params.p_decoy1)
        
        # 参数估计误差
        delta_1 = np.sqrt(np.log(1 / params.security_params.epsilon_pe) / (2 * min(n_signal, n_decoy1)))
        
        # 安全密钥误差
        delta_2 = np.sqrt(np.log(1 / params.security_params.epsilon_sec) / (2 * n_signal))
        
        self.logger.debug(f"诱骗态有限密钥效应: delta_1={delta_1:.6f}, delta_2={delta_2:.6f}")
        return delta_1, delta_2
    
    def _log_calculation_details(self, result: KeyRateResult):
        """记录计算详情"""
        self.logger.info("=== 密钥率计算详情 ===")
        self.logger.info(f"协议类型: {result.protocol_type.value}")
        self.logger.info(f"最终密钥率: {result.final_key_rate:.6f} bit/pulse")
        self.logger.info(f"最终密钥长度: {result.final_key_length}")
        self.logger.info(f"最小熵 H_min: {result.h_min:.6f}")
        self.logger.info(f"纠错泄露: {result.leak_ec:.6f}")
        self.logger.info(f"参数估计泄露: {result.leak_pe:.6f}")
        self.logger.info(f"安全密钥泄露: {result.leak_sk:.6f}")
        self.logger.info(f"秘密密钥率: {result.secret_key_rate:.6f}")
        self.logger.info("=====================")
    
    def compare_protocols(self, 
                         qber: float,
                         gain: float,
                         n_pulses: int,
                         **kwargs) -> Dict[ProtocolType, KeyRateResult]:
        """
        比较不同协议的密钥率
        
        Args:
            qber: 量子比特错误率
            gain: 信道增益
            n_pulses: 发送脉冲数量
            **kwargs: 其他参数
            
        Returns:
            Dict: 各协议的密钥率结果
        """
        protocols = [ProtocolType.BB84, ProtocolType.DECOY_BB84]
        results = {}
        
        for protocol in protocols:
            try:
                result = self.compute(qber, gain, n_pulses, protocol, **kwargs)
                results[protocol] = result
            except Exception as e:
                self.logger.error(f"计算{protocol.value}协议密钥率失败: {e}")
                results[protocol] = None
                
        return results
    
    def analyze_parameter_sensitivity(self,
                                    base_qber: float,
                                    base_gain: float,
                                    n_pulses: int,
                                    protocol_type: ProtocolType = ProtocolType.BB84,
                                    **kwargs) -> Dict[str, List[float]]:
        """
        分析参数敏感性
        
        Args:
            base_qber: 基准QBER
            base_gain: 基准增益
            n_pulses: 脉冲数量
            protocol_type: 协议类型
            **kwargs: 其他参数
            
        Returns:
            Dict: 敏感性分析结果
        """
        # QBER敏感性分析
        qber_range = np.linspace(0.01, 0.1, 10)
        qber_sensitivity = []
        
        for qber in qber_range:
            result = self.compute(qber, base_gain, n_pulses, protocol_type, **kwargs)
            qber_sensitivity.append(result.final_key_rate)
        
        # 增益敏感性分析
        gain_range = np.linspace(0.05, 0.2, 10)
        gain_sensitivity = []
        
        for gain in gain_range:
            result = self.compute(base_qber, gain, n_pulses, protocol_type, **kwargs)
            gain_sensitivity.append(result.final_key_rate)
        
        return {
            'qber_range': qber_range.tolist(),
            'qber_sensitivity': qber_sensitivity,
            'gain_range': gain_range.tolist(),
            'gain_sensitivity': gain_sensitivity
        }


# ==================== 向后兼容性和迁移指导 ====================

def create_universal_key_rate_calculator():
    """
    创建通用密钥率计算器的便利函数
    
    这是推荐的创建方式，自动使用通用框架（如果可用）。
    
    Returns:
        KeyRateCalculator: 配置好的计算器实例
    """
    calculator = KeyRateCalculator()
    
    if _UNIVERSAL_FRAMEWORK_AVAILABLE:
        logger.info("使用通用密钥率计算框架")
    else:
        logger.warning("通用框架不可用，回退到传统实现")
    
    return calculator


def migrate_legacy_calculation(qber: float, 
                              gain: float, 
                              n_pulses: int,
                              protocol_type: ProtocolType,
                              **kwargs) -> KeyRateResult:
    """
    迁移助手函数：将传统计算迁移到通用框架
    
    这个函数演示如何将旧的计算方式转换为新的通用方法。
    
    Args:
        qber: 量子比特错误率
        gain: 信道增益
        n_pulses: 脉冲数量
        protocol_type: 协议类型
        **kwargs: 其他参数
        
    Returns:
        KeyRateResult: 密钥率计算结果
        
    Example:
        # 旧方式
        calculator = KeyRateCalculator(qber=0.05, gain=0.5, protocol_type=ProtocolType.BB84)
        result = calculator.calculate_key_rate()
        
        # 新方式（推荐）
        result = migrate_legacy_calculation(
            qber=0.05, 
            gain=0.5, 
            n_pulses=1000000,
            protocol_type=ProtocolType.BB84
        )
    """
    calculator = KeyRateCalculator()
    
    if _UNIVERSAL_FRAMEWORK_AVAILABLE:
        # 使用通用框架
        simulation_results, protocol_features, security_params = calculator.convert_legacy_to_universal(
            qber, gain, n_pulses, protocol_type
        )
        
        # 应用额外参数
        if 'epsilon_sec' in kwargs:
            security_params.epsilon_sec = kwargs['epsilon_sec']
        if 'epsilon_cor' in kwargs:
            security_params.epsilon_cor = kwargs['epsilon_cor']
        
        return calculator.compute_universal(simulation_results, protocol_features, security_params)
    else:
        # 回退到传统方法
        return calculator.compute(qber, gain, n_pulses, protocol_type, **kwargs)


# ==================== 导出 ====================

__all__ = [
    'KeyRateCalculator',
    'KeyRateParameters', 
    'KeyRateResult',
    'create_universal_key_rate_calculator',
    'migrate_legacy_calculation'
]

# 如果通用框架可用，也导出相关类
if _UNIVERSAL_FRAMEWORK_AVAILABLE:
    __all__.extend([
        'ProtocolFeatures',
        'UniversalSecurityParameters'
    ]) 