"""
量子测量仿真模块

实现了各种量子测量的仿真，包括：
- Z基测量（计算基）
- X基测量（Hadamard基）
- 投影测量
- POVM测量
- 探测效率建模
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple, List
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


class MeasurementBasis(Enum):
    """测量基枚举"""
    Z = "Z"  # 计算基 {|0⟩, |1⟩}
    X = "X"  # Hadamard基 {|+⟩, |-⟩}
    Y = "Y"  # Y基 {|+i⟩, |-i⟩}
    CUSTOM = "custom"  # 自定义基


class MeasurementType(Enum):
    """测量类型枚举"""
    PROJECTIVE = "projective"  # 投影测量
    POVM = "povm"             # POVM测量
    HOMODYNE = "homodyne"     # 零差测量
    HETERODYNE = "heterodyne" # 外差测量


class Measurement:
    """
    量子测量仿真器
    
    实现了各种量子测量的仿真，包括不同基的测量、
    探测效率建模、测量结果统计等。
    """
    
    def __init__(self, max_photon_number: int = 10):
        """
        初始化测量仿真器
        
        Args:
            max_photon_number: 最大光子数（用于截断）
        """
        self.max_photon_number = max_photon_number
        
        # 预定义测量基
        self._measurement_bases = self._initialize_measurement_bases()
    
    def _initialize_measurement_bases(self) -> Dict[str, Dict[str, np.ndarray]]:
        """初始化测量基"""
        bases = {}
        
        # Z基（计算基）
        z0 = np.array([1, 0])
        z1 = np.array([0, 1])
        bases["Z"] = {
            "0": np.outer(z0, z0.conj()),  # |0⟩⟨0|
            "1": np.outer(z1, z1.conj())   # |1⟩⟨1|
        }
        
        # X基（Hadamard基）
        x_plus = np.array([1, 1]) / np.sqrt(2)
        x_minus = np.array([1, -1]) / np.sqrt(2)
        bases["X"] = {
            "+": np.outer(x_plus, x_plus.conj()),   # |+⟩⟨+|
            "-": np.outer(x_minus, x_minus.conj())   # |-⟩⟨-|
        }
        
        # Y基
        y_plus_i = np.array([1, 1j]) / np.sqrt(2)
        y_minus_i = np.array([1, -1j]) / np.sqrt(2)
        bases["Y"] = {
            "+i": np.outer(y_plus_i, y_plus_i.conj()),  # |+i⟩⟨+i|
            "-i": np.outer(y_minus_i, y_minus_i.conj())  # |-i⟩⟨-i|
        }
        
        return bases
    
    def projective_measurement(self,
                              input_state: Dict[str, Any],
                              basis: str = "Z") -> Dict[str, Any]:
        """
        投影测量
        
        Args:
            input_state: 输入态信息字典，必须包含 'density_matrix'
            basis: 测量基 ("Z", "X", "Y")
            
        Returns:
            测量结果
        """
        density_matrix = input_state.get("density_matrix")
        if density_matrix is None:
            raise ValueError("输入的状态字典中没有找到 'density_matrix'。")

        if basis not in self._measurement_bases:
            raise ValueError(f"不支持的测量基: {basis}")

        basis_vectors = self._measurement_bases[basis]
    
        # 动态获取当前基的两个投影算符
        proj_0, proj_1 = list(basis_vectors.values())
        outcome_labels = list(basis_vectors.keys())
        
        prob_0 = np.trace(proj_0 @ density_matrix).real
        prob_1 = np.trace(proj_1 @ density_matrix).real

        # 归一化，考虑数值误差
        total_prob = prob_0 + prob_1
        if not np.isclose(total_prob, 0):
            prob_0 /= total_prob
            prob_1 /= total_prob

        # 根据概率随机选择一个结果
        is_outcome_0 = (np.random.rand() < prob_0)

        # 根据基和结果返回正确的输出 (整数或字符串)
        if basis == 'Z':
            return {"outcome": 0 if is_outcome_0 else 1}
        else: # X 或 Y 基
            return {"outcome": outcome_labels[0] if is_outcome_0 else outcome_labels[1]}
    
    def povm_measurement(self, 
                        input_state: Dict[str, Any],
                        povm_operators: List[np.ndarray],
                        efficiency: float = 1.0) -> Dict[str, Any]:
        """
        POVM测量
        
        Args:
            input_state: 输入态信息
            povm_operators: POVM算符列表
            efficiency: 探测效率
            
        Returns:
            测量结果
        """
        # 简化实现：使用投影测量
        return self.projective_measurement(input_state, "Z", efficiency)
    
    def homodyne_measurement(self, 
                            input_state: Dict[str, Any],
                            phase: float = 0.0,
                            efficiency: float = 1.0) -> Dict[str, Any]:
        """
        零差测量
        
        Args:
            input_state: 输入态信息
            phase: 本振相位
            efficiency: 探测效率
            
        Returns:
            测量结果
        """
        # 简化实现：返回连续值
        photon_dist = input_state.get("photon_distribution", {})
        mean_photon = sum(n * p for n, p in photon_dist.items())
        
        # 零差测量结果（连续值）
        measurement_value = np.sqrt(2 * mean_photon) * np.cos(phase) + np.random.normal(0, 0.1)
        
        return {
            "measurement_type": "homodyne",
            "value": measurement_value,
            "phase": phase,
            "efficiency": efficiency,
            "mean_photon_number": mean_photon
        }
    
    def simulate_measurement(self, 
                            input_state: Dict[str, Any],
                            measurement_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据参数模拟测量
        
        Args:
            input_state: 输入态信息字典，必须包含 'density_matrix' 和 'detected'
            measurement_params: 测量参数字典
            
        Returns:
            测量结果
        """
        # 如果信道判定脉冲已丢失，则直接返回无探测结果
        if not input_state.get('detected', True):
            return {"outcome": "no_click"}

        basis = measurement_params.get("basis", "Z")
        efficiency = measurement_params.get("efficiency", 1.0) # 探测器效率
        
        # 探测器自身也可能未探测到
        if np.random.rand() > efficiency:
            return {"outcome": "no_click"}

        # 选择测量类型
        measurement_type = measurement_params.get("measurement_type", "projective")
        
        if measurement_type == "projective":
            # 传递整个状态字典给投影测量函数
            result = self.projective_measurement(input_state, basis)
        elif measurement_type == "povm":
            result = self.povm_measurement(input_state, [], efficiency)
        elif measurement_type == "homodyne":
            phase = measurement_params.get("phase", 0.0)
            result = self.homodyne_measurement(input_state, phase, efficiency)
        else:
            raise ValueError(f"不支持的测量类型: {measurement_type}")
        
        return result
    
    def calculate_measurement_statistics(self, 
                                        measurement_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算测量统计特性
        
        Args:
            measurement_results: 测量结果列表
            
        Returns:
            统计特性
        """
        if not measurement_results:
            return {
                "total_measurements": 0,
                "detection_rate": 0.0,
                "outcome_distribution": {},
                "average_efficiency": 0.0
            }
        
        total_measurements = len(measurement_results)
        detection_count = 0
        outcome_counts = {}
        total_efficiency = 0.0
        
        for result in measurement_results:
            outcome = result.get("outcome", "no_detection")
            efficiency = result.get("efficiency", 0.0)
            
            if outcome != "no_detection":
                detection_count += 1
                outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
            
            total_efficiency += efficiency
        
        detection_rate = detection_count / total_measurements
        average_efficiency = total_efficiency / total_measurements
        
        # 计算结果分布
        outcome_distribution = {}
        for outcome, count in outcome_counts.items():
            outcome_distribution[outcome] = count / total_measurements
        
        return {
            "total_measurements": total_measurements,
            "detection_count": detection_count,
            "detection_rate": detection_rate,
            "outcome_distribution": outcome_distribution,
            "average_efficiency": average_efficiency
        }
    
    def simulate_multiple_measurements(self, 
                                     input_state: Dict[str, Any],
                                     measurement_params: Dict[str, Any],
                                     num_measurements: int = 1000) -> List[Dict[str, Any]]:
        """
        模拟多次测量
        
        Args:
            input_state: 输入态信息
            measurement_params: 测量参数
            num_measurements: 测量次数
            
        Returns:
            测量结果列表
        """
        results = []
        
        for _ in range(num_measurements):
            result = self.simulate_measurement(input_state, measurement_params)
            results.append(result)
        
        return results
    
    def calculate_quantum_bit_error_rate(self, 
                                        alice_bits: List[int],
                                        bob_bits: List[int]) -> float:
        """
        计算量子比特错误率（QBER）
        
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
        
        Args:
            total_pulses: 总脉冲数
            detected_pulses: 探测到的脉冲数
            
        Returns:
            增益值
        """
        if total_pulses == 0:
            return 0.0
        
        return detected_pulses / total_pulses 