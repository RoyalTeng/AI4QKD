"""
噪声模型模块

实现常见的量子噪声模型，包括退相干、振幅阻尼、相位噪声等。
"""
from typing import Optional
import numpy as np

class NoiseModel:
    """
    量子噪声模型类，支持多种常见噪声类型。
    """
    def __init__(self, dephasing_rate: float = 0.0, amplitude_damping_rate: float = 0.0, phase_noise_std: float = 0.0):
        self.dephasing_rate = dephasing_rate
        self.amplitude_damping_rate = amplitude_damping_rate
        self.phase_noise_std = phase_noise_std

    def apply_dephasing(self, state: np.ndarray) -> np.ndarray:
        """
        对输入量子态施加退相干噪声。
        Args:
            state: 输入的密度矩阵
        Returns:
            施加退相干后的密度矩阵
        """
        p = self.dephasing_rate
        if p == 0:
            return state
        # 退相干操作: ρ -> (1-p)ρ + p ZρZ
        Z = np.array([[1, 0], [0, -1]])
        return (1 - p) * state + p * Z @ state @ Z

    def apply_amplitude_damping(self, state: np.ndarray) -> np.ndarray:
        """
        对输入量子态施加振幅阻尼噪声。
        Args:
            state: 输入的密度矩阵
        Returns:
            施加振幅阻尼后的密度矩阵
        """
        gamma = self.amplitude_damping_rate
        if gamma == 0:
            return state
        K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]])
        K1 = np.array([[0, np.sqrt(gamma)], [0, 0]])
        return K0 @ state @ K0.T.conj() + K1 @ state @ K1.T.conj()

    def apply_phase_noise(self, state: np.ndarray) -> np.ndarray:
        """
        对输入量子态施加高斯相位噪声。
        Args:
            state: 输入的密度矩阵
        Returns:
            施加相位噪声后的密度矩阵
        """
        std = self.phase_noise_std
        if std == 0:
            return state
        theta = np.random.normal(0, std)
        U = np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]])
        return U @ state @ U.T.conj()

    def apply_all(self, state: np.ndarray) -> np.ndarray:
        """
        依次施加所有噪声模型。
        Args:
            state: 输入的密度矩阵
        Returns:
            施加所有噪声后的密度矩阵
        """
        state = self.apply_dephasing(state)
        state = self.apply_amplitude_damping(state)
        state = self.apply_phase_noise(state)
        return state 