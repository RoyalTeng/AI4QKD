"""
量子态准备仿真模块

实现了各种量子态的制备仿真，包括：
- 弱相干脉冲（WCP）
- 真空态
- 诱骗态
- 单光子态
- 纠缠态
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

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit_aer import Aer
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    warnings.warn("Qiskit not available, using simplified models")


class StateType(Enum):
    """量子态类型枚举"""
    VACUUM = "vacuum"           # 真空态 |0⟩
    SINGLE_PHOTON = "single"    # 单光子态 |1⟩
    WCP = "wcp"                 # 弱相干脉冲
    DECOY = "decoy"             # 诱骗态
    ENTANGLED = "entangled"     # 纠缠态
    CUSTOM = "custom"           # 自定义态


class StatePreparation:
    """
    量子态准备仿真器
    
    支持多种量子态的制备和仿真，包括光子数分布计算、
    密度矩阵生成、量子线路构建等。
    """
    
    def __init__(self, mu: float = 0.1, decoy_mu: float = 0.2, max_photon_number: int = 10):
        """
        初始化态准备器
        
        Args:
            mu: 弱相干脉冲的平均光子数
            decoy_mu: 诱骗态的平均光子数
            max_photon_number: 最大光子数（用于截断）
        """
        self.mu = mu
        self.decoy_mu = decoy_mu
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
    
    def prepare_vacuum_state(self) -> Dict[str, Any]:
        """
        制备真空态 |0⟩
        
        Returns:
            包含态信息的字典
        """
        state_vector = self._fock_states[0]
        
        return {
            "type": StateType.VACUUM,
            "state_vector": state_vector,
            "photon_distribution": {0: 1.0},
            "mean_photon_number": 0.0,
            "fidelity": 1.0
        }
    
    def prepare_single_photon_state(self) -> Dict[str, Any]:
        """
        制备单光子态 |1⟩
        
        Returns:
            包含态信息的字典
        """
        state_vector = self._fock_states[1]
        
        return {
            "type": StateType.SINGLE_PHOTON,
            "state_vector": state_vector,
            "photon_distribution": {1: 1.0},
            "mean_photon_number": 1.0,
            "fidelity": 1.0
        }
    
    def prepare_wcp_state(self, mu: Optional[float] = None) -> Dict[str, Any]:
        """
        制备弱相干脉冲（WCP）态
        
        WCP态：|α⟩ = exp(-|α|²/2) * Σ(αⁿ/√n!) |n⟩
        
        Args:
            mu: 平均光子数 μ = |α|²
            
        Returns:
            包含态信息的字典
        """
        if mu is None:
            mu = self.mu
        
        if mu < 0:
            raise ValueError("平均光子数必须非负")
        
        # 计算相干态参数
        alpha = np.sqrt(mu) * np.exp(1j * 0.0)
        
        # 计算光子数分布（泊松分布）
        photon_distribution = {}
        state_vector = np.zeros(self.max_photon_number + 1)
        
        for n in range(self.max_photon_number + 1):
            # 泊松分布概率
            prob = np.exp(-mu) * (mu ** n) / np.math.factorial(n)
            photon_distribution[n] = prob
            
            # 相干态系数
            coeff = np.exp(-mu/2) * (alpha ** n) / np.sqrt(np.math.factorial(n))
            state_vector[n] = coeff
        
        # 归一化
        norm = np.sqrt(np.sum(np.abs(state_vector) ** 2))
        state_vector = state_vector / norm
        
        return {
            "type": StateType.WCP,
            "state_vector": state_vector,
            "photon_distribution": photon_distribution,
            "mean_photon_number": mu,
            "phase": 0.0,
            "alpha": alpha,
            "fidelity": 1.0
        }
    
    def prepare_decoy_state(self, mu: Optional[float] = None) -> Dict[str, Any]:
        """
        制备诱骗态
        
        Args:
            mu: 平均光子数
            
        Returns:
            包含态信息的字典
        """
        if mu is None:
            mu = self.decoy_mu
        
        if mu < 0:
            raise ValueError("平均光子数必须非负")
        
        # 弱诱骗态，通常μ ≈ 0.1
        return self.prepare_wcp_state(mu)
    
    def prepare_entangled_state(self, 
                               state_type: str = "bell") -> Dict[str, Any]:
        """
        制备纠缠态
        
        Args:
            state_type: 纠缠态类型 ("bell", "ghz", "w")
            
        Returns:
            包含态信息的字典
        """
        if state_type == "bell":
            # Bell态 |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
            if QISKIT_AVAILABLE:
                qc = QuantumCircuit(2)
                qc.h(0)
                qc.cx(0, 1)
                
                backend = Aer.get_backend('statevector_simulator')
                job = backend.run(qc)
                state_vector = job.result().get_statevector()
                
                return {
                    "type": StateType.ENTANGLED,
                    "state_type": "bell",
                    "quantum_circuit": qc,
                    "state_vector": state_vector,
                    "entanglement_measure": 1.0
                }
            else:
                # 简化实现
                state_vector = np.array([1, 0, 0, 1]) / np.sqrt(2)
                return {
                    "type": StateType.ENTANGLED,
                    "state_type": "bell",
                    "state_vector": state_vector,
                    "entanglement_measure": 1.0
                }
        else:
            raise ValueError(f"不支持的纠缠态类型: {state_type}")
    
    def get_photon_statistics(self, state_info: Dict[str, Any]) -> Dict[str, float]:
        """
        计算光子统计特性
        
        Args:
            state_info: 态信息字典
            
        Returns:
            统计特性字典
        """
        photon_dist = state_info.get("photon_distribution", {})
        
        if not photon_dist:
            return {
                "mean_photon_number": 0.0,
                "photon_number_variance": 0.0,
                "g2": 0.0,  # 二阶关联函数
                "single_photon_probability": 0.0
            }
        
        # 计算平均光子数
        mean_n = sum(n * p for n, p in photon_dist.items())
        
        # 计算方差
        var_n = sum((n - mean_n) ** 2 * p for n, p in photon_dist.items())
        
        # 计算二阶关联函数 g²
        if mean_n > 0:
            g2 = sum(n * (n - 1) * p for n, p in photon_dist.items()) / (mean_n ** 2)
        else:
            g2 = 0.0
        
        # 单光子概率
        single_photon_prob = photon_dist.get(1, 0.0)
        
        return {
            "mean_photon_number": mean_n,
            "photon_number_variance": var_n,
            "g2": g2,
            "single_photon_probability": single_photon_prob
        }
    
    def calculate_fidelity(self, 
                          state1: Dict[str, Any], 
                          state2: Dict[str, Any]) -> float:
        """
        计算两个态的保真度
        
        Args:
            state1: 第一个态信息
            state2: 第二个态信息
            
        Returns:
            保真度值
        """
        vec1 = state1.get("state_vector", np.array([]))
        vec2 = state2.get("state_vector", np.array([]))
        
        if len(vec1) == 0 or len(vec2) == 0:
            return 0.0
        
        # 确保向量长度一致
        max_len = max(len(vec1), len(vec2))
        vec1_pad = np.pad(vec1, (0, max_len - len(vec1)))
        vec2_pad = np.pad(vec2, (0, max_len - len(vec2)))
        
        # 计算保真度 |⟨ψ₁|ψ₂⟩|²
        overlap = np.abs(np.dot(np.conj(vec1_pad), vec2_pad)) ** 2
        return overlap
    
    def simulate_state_preparation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据参数模拟量子态的制备
        
        Args:
            params: 包含量子态参数的字典 (期望有 'basis' 和 'bit')
            
        Returns:
            包含量子态信息的字典，必须包含 'density_matrix'
        """
        basis = params.get('basis', 'Z')
        bit = params.get('bit', 0)
        
        # 核心逻辑：根据基和比特生成密度矩阵
        if basis == 'Z':
            state_vector = np.array([1, 0]) if bit == 0 else np.array([0, 1])
        elif basis == 'X':
            state_vector = np.array([1, 1])/np.sqrt(2) if bit == 0 else np.array([1, -1])/np.sqrt(2)
        else:
            raise ValueError(f"不支持的基: {basis}")
            
        density_matrix = np.outer(state_vector, state_vector.conj())

        return {
            "density_matrix": density_matrix,
            "basis": basis,
            "ideal_bit": bit
        } 