"""
Qiskit接口封装模块

实现Qiskit与本地仿真器的数据结构和接口适配。
"""
from typing import Any, Dict, Optional
from qiskit import QuantumCircuit
from qiskit_aer import Aer

class QiskitInterface:
    """
    Qiskit接口适配器，支持量子电路的构建、运行和结果解析。
    """
    def __init__(self, backend_name: str = 'aer_simulator'):
        self.backend_name = backend_name
        self.backend = Aer.get_backend(backend_name)

    def run_circuit(self, circuit: QuantumCircuit, shots: int = 1024, params: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
        """
        运行量子电路并返回测量结果统计。
        Args:
            circuit: Qiskit QuantumCircuit对象
            shots: 测量次数
            params: 可选的运行参数
        Returns:
            结果字典（比特串: 次数）
        """
        job = self.backend.run(circuit, shots=shots, **(params or {}))
        result = job.result()
        counts = result.get_counts()
        return counts

    def get_backend(self):
        """
        获取当前Qiskit后端。
        Returns:
            Qiskit后端对象
        """
        return self.backend 