"""
量子信道建模模块

实现了各种量子信道的建模，包括：
- 光子损耗
- 退相干
- 背景噪声
- 相位漂移
- 偏振串扰
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from enum import Enum
import warnings

try:
    import qutip as qt
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False
    warnings.warn("QuTiP not available, using simplified models")


class ChannelType(Enum):
    """信道类型枚举"""
    LOSS = "loss"               # 损耗信道
    DEPHASING = "dephasing"     # 退相干信道
    AMPLITUDE_DAMPING = "amplitude_damping"  # 振幅阻尼
    PHASE_DAMPING = "phase_damping"          # 相位阻尼
    DEPOLARIZING = "depolarizing"            # 退偏振
    CUSTOM = "custom"           # 自定义信道


class ChannelModel:
    """
    量子信道建模器
    
    实现了各种量子信道的建模，包括损耗、退相干、噪声等效应。
    支持单光子态和多光子态的传输仿真。
    """
    
    def __init__(self, loss: float = 0.2, noise: float = 0.01, fiber_length: float = 50.0, max_photon_number: int = 10):
        """
        初始化信道建模器
        
        Args:
            loss: 损耗率 (0 ≤ loss ≤ 1)
            noise: 背景噪声率 (0 ≤ noise ≤ 1)
            fiber_length: 光纤长度 (单位: 米)
            max_photon_number: 最大光子数（用于截断）
        """
        self.loss = loss
        self.noise = noise
        self.fiber_length = fiber_length
        self.max_photon_number = max_photon_number
        
        # 预计算Fock态
        self._fock_states = self._initialize_fock_states()
    
    def _initialize_fock_states(self) -> Dict[int, np.ndarray]:
        """初始化Fock态"""
        fock_states = {}
        for n in range(self.max_photon_number + 1):
            state = np.zeros(self.max_photon_number + 1)
            state[n] = 1.0
            fock_states[n] = state
        return fock_states
    
    def apply_loss_channel(self, 
                          input_state: Dict[str, Any],
                          loss_rate: float) -> Dict[str, Any]:
        """
        应用损耗信道
        
        损耗信道：ρ' = Σₖ Eₖ ρ Eₖ†
        其中 Eₖ = √(Cₙᵏ) * (√η)ᵏ * (√(1-η))ⁿ⁻ᵏ * |k⟩⟨n|
        
        Args:
            input_state: 输入态信息
            loss_rate: 损耗率 (0 ≤ loss_rate ≤ 1)
            
        Returns:
            输出态信息
        """
        if not (0 <= loss_rate <= 1):
            raise ValueError("损耗率必须在[0,1]范围内")
        
        transmission = 1.0 - loss_rate
        photon_dist = input_state.get("photon_distribution", {})
        
        # 计算损耗后的光子数分布
        output_distribution = {}
        
        for n, p_n in photon_dist.items():
            for k in range(n + 1):
                # 二项分布概率：Cₙᵏ * ηᵏ * (1-η)ⁿ⁻ᵏ
                prob = np.math.comb(n, k) * (transmission ** k) * (loss_rate ** (n - k))
                output_distribution[k] = output_distribution.get(k, 0) + p_n * prob
        
        # 计算新的平均光子数
        new_mean_photon = sum(n * p for n, p in output_distribution.items())
        
        # 更新态向量（简化处理）
        output_state_vector = np.zeros(self.max_photon_number + 1)
        for n, p in output_distribution.items():
            if n < len(output_state_vector):
                output_state_vector[n] = np.sqrt(p)
        
        # 归一化
        norm = np.sqrt(np.sum(np.abs(output_state_vector) ** 2))
        if norm > 0:
            output_state_vector = output_state_vector / norm
        
        return {
            "type": input_state.get("type"),
            "state_vector": output_state_vector,
            "photon_distribution": output_distribution,
            "mean_photon_number": new_mean_photon,
            "transmission": transmission,
            "loss_rate": loss_rate
        }
    
    def apply_dephasing_channel(self, 
                               input_state: Dict[str, Any],
                               dephasing_rate: float) -> Dict[str, Any]:
        """
        应用退相干信道
        
        退相干信道：ρ' = (1-p)ρ + p * ZρZ
        其中 p 是退相干概率
        
        Args:
            input_state: 输入态信息
            dephasing_rate: 退相干率 (0 ≤ dephasing_rate ≤ 1)
            
        Returns:
            输出态信息
        """
        if not (0 <= dephasing_rate <= 1):
            raise ValueError("退相干率必须在[0,1]范围内")
        
        # 对于光子态，退相干主要影响相位
        # 简化处理：降低相干性
        state_vector = input_state.get("state_vector", np.array([]))
        
        if len(state_vector) > 0:
            # 应用退相干：混合原始态和相位翻转态
            phase_flipped = np.conj(state_vector)  # 相位翻转
            output_vector = (1 - dephasing_rate) * state_vector + dephasing_rate * phase_flipped
            
            # 归一化
            norm = np.sqrt(np.sum(np.abs(output_vector) ** 2))
            if norm > 0:
                output_vector = output_vector / norm
        else:
            output_vector = state_vector
        
        # 更新光子数分布（简化处理）
        photon_dist = input_state.get("photon_distribution", {}).copy()
        
        return {
            "type": input_state.get("type"),
            "state_vector": output_vector,
            "photon_distribution": photon_dist,
            "mean_photon_number": input_state.get("mean_photon_number", 0.0),
            "dephasing_rate": dephasing_rate,
            "coherence_length": (1 - dephasing_rate) * input_state.get("coherence_length", 1.0)
        }
    
    def apply_amplitude_damping_channel(self, 
                                       input_state: Dict[str, Any],
                                       damping_rate: float) -> Dict[str, Any]:
        """
        应用振幅阻尼信道
        
        振幅阻尼：|1⟩ → √γ|0⟩ + √(1-γ)|1⟩
        
        Args:
            input_state: 输入态信息
            damping_rate: 阻尼率 (0 ≤ damping_rate ≤ 1)
            
        Returns:
            输出态信息
        """
        if not (0 <= damping_rate <= 1):
            raise ValueError("阻尼率必须在[0,1]范围内")
        
        photon_dist = input_state.get("photon_distribution", {}).copy()
        output_distribution = {}
        
        # 应用振幅阻尼
        for n, p_n in photon_dist.items():
            if n == 0:
                # 真空态不变
                output_distribution[0] = output_distribution.get(0, 0) + p_n
            else:
                # 有光子时发生阻尼
                for k in range(n + 1):
                    # 从n个光子衰减到k个光子的概率
                    prob = np.math.comb(n, k) * ((1 - damping_rate) ** k) * (damping_rate ** (n - k))
                    output_distribution[k] = output_distribution.get(k, 0) + p_n * prob
        
        # 计算新的平均光子数
        new_mean_photon = sum(n * p for n, p in output_distribution.items())
        
        return {
            "type": input_state.get("type"),
            "photon_distribution": output_distribution,
            "mean_photon_number": new_mean_photon,
            "damping_rate": damping_rate
        }
    
    def apply_background_noise(self, 
                              input_state: Dict[str, Any],
                              dark_count_rate: float,
                              background_photon_rate: float = 0.0) -> Dict[str, Any]:
        """
        应用背景噪声
        
        Args:
            input_state: 输入态信息
            dark_count_rate: 暗计数率
            background_photon_rate: 背景光子率
            
        Returns:
            输出态信息
        """
        photon_dist = input_state.get("photon_distribution", {}).copy()
        
        # 添加背景光子（泊松分布）
        if background_photon_rate > 0:
            for n in range(self.max_photon_number + 1):
                # 背景光子概率
                bg_prob = np.exp(-background_photon_rate) * (background_photon_rate ** n) / np.math.factorial(n)
                
                # 与原始分布卷积
                new_dist = {}
                for orig_n, orig_p in photon_dist.items():
                    total_n = orig_n + n
                    if total_n <= self.max_photon_number:
                        new_dist[total_n] = new_dist.get(total_n, 0) + orig_p * bg_prob
                
                # 更新分布
                for total_n, prob in new_dist.items():
                    photon_dist[total_n] = photon_dist.get(total_n, 0) + prob
        
        # 添加暗计数（简化处理：增加单光子概率）
        if dark_count_rate > 0:
            photon_dist[1] = photon_dist.get(1, 0) + dark_count_rate
        
        # 重新归一化
        total_prob = sum(photon_dist.values())
        if total_prob > 0:
            for n in photon_dist:
                photon_dist[n] /= total_prob
        
        return {
            "type": input_state.get("type"),
            "photon_distribution": photon_dist,
            "mean_photon_number": sum(n * p for n, p in photon_dist.items()),
            "dark_count_rate": dark_count_rate,
            "background_photon_rate": background_photon_rate
        }
    
    def apply_phase_drift(self, 
                         input_state: Dict[str, Any],
                         phase_drift: float) -> Dict[str, Any]:
        """
        应用相位漂移
        
        Args:
            input_state: 输入态信息
            phase_drift: 相位漂移（弧度）
            
        Returns:
            输出态信息
        """
        state_vector = input_state.get("state_vector", np.array([]))
        
        if len(state_vector) > 0:
            # 应用相位漂移：|ψ⟩ → exp(iφ)|ψ⟩
            output_vector = state_vector * np.exp(1j * phase_drift)
        else:
            output_vector = state_vector
        
        return {
            "type": input_state.get("type"),
            "state_vector": output_vector,
            "photon_distribution": input_state.get("photon_distribution", {}),
            "mean_photon_number": input_state.get("mean_photon_number", 0.0),
            "phase_drift": phase_drift
        }
    
    def apply_polarization_crosstalk(self, 
                                    input_state: Dict[str, Any],
                                    crosstalk_rate: float) -> Dict[str, Any]:
        """
        应用偏振串扰
        
        Args:
            input_state: 输入态信息
            crosstalk_rate: 串扰率 (0 ≤ crosstalk_rate ≤ 1)
            
        Returns:
            输出态信息
        """
        if not (0 <= crosstalk_rate <= 1):
            raise ValueError("串扰率必须在[0,1]范围内")
        
        # 简化处理：降低偏振纯度
        photon_dist = input_state.get("photon_distribution", {}).copy()
        
        return {
            "type": input_state.get("type"),
            "photon_distribution": photon_dist,
            "mean_photon_number": input_state.get("mean_photon_number", 0.0),
            "polarization_purity": (1 - crosstalk_rate) * input_state.get("polarization_purity", 1.0),
            "crosstalk_rate": crosstalk_rate
        }
    
    def simulate_channel_transmission(self, 
                                     input_state: Dict[str, Any],
                                     channel_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟信道传输
        
        Args:
            input_state: 输入态信息字典，必须包含 'density_matrix'
            channel_params: 信道参数字典
            
        Returns:
            输出态信息字典
        """
        output_state = input_state.copy()
        
        # 应用损耗
        loss_rate = channel_params.get("loss", 0.0)
        # 损耗是一个概率事件，我们先记录下来，在测量时使用
        output_state['detected'] = (np.random.rand() > loss_rate)

        # 应用信道错误（退偏振信道模型）
        error_rate = channel_params.get("error_rate", 0.0)
        if error_rate > 0 and 'density_matrix' in output_state:
            density_matrix = output_state["density_matrix"]
            # I/2 是最大混合态
            mixed_state = np.eye(density_matrix.shape[0]) / density_matrix.shape[0]
            output_state["density_matrix"] = (1 - error_rate) * density_matrix + error_rate * mixed_state
        
        return output_state
    
    def calculate_channel_capacity(self, 
                                  channel_params: Dict[str, Any],
                                  input_mean_photon: float = 1.0) -> Dict[str, float]:
        """
        计算信道容量
        
        Args:
            channel_params: 信道参数
            input_mean_photon: 输入平均光子数
            
        Returns:
            信道容量信息
        """
        # 计算有效传输率
        transmission = 1.0 - channel_params.get("loss", 0.0)
        effective_photon = input_mean_photon * transmission
        
        # 计算噪声
        dark_count = channel_params.get("dark_count_rate", 0.0)
        background = channel_params.get("background_photon_rate", 0.0)
        total_noise = dark_count + background
        
        # 计算信噪比
        if total_noise > 0:
            snr = effective_photon / total_noise
        else:
            snr = float('inf')
        
        # 计算香农容量（简化）
        if snr > 0:
            capacity = np.log2(1 + snr)
        else:
            capacity = 0.0
        
        return {
            "transmission": transmission,
            "effective_photon_number": effective_photon,
            "total_noise": total_noise,
            "signal_to_noise_ratio": snr,
            "channel_capacity": capacity
        } 