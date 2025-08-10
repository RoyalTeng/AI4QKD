"""
真实量子仿真器（向后兼容接口）

该模块保持与原有代码的向后兼容性，同时提供到新的通用仿真器的桥接。

警告：此模块中的协议特定方法已弃用，建议迁移到 universal_quantum_simulator.py

新功能包括：
- 基于ProtocolFeatures的通用协议仿真
- 量子操作的自动解析和执行
- 物理精确的量子态演化仿真
- 完全向后兼容的接口

迁移指南：
- 使用 simulate_universal_protocol() 替代协议特定方法
- 使用 ProtocolFeatures 描述协议结构
- 利用通用量子操作框架
"""

import warnings
import numpy as np
from typing import Dict, Any, Optional

# 导入新的通用仿真器
try:
    from .universal_quantum_simulator import UniversalQuantumSimulator
    _UNIVERSAL_SIMULATOR_AVAILABLE = True
except ImportError:
    _UNIVERSAL_SIMULATOR_AVAILABLE = False
    warnings.warn(
        "Universal quantum simulator not available. Using legacy implementation.",
        ImportWarning
    )

# 向后兼容的导入
from .state_preparation import StatePreparation
from .channel_model import ChannelModel
from .measurement import Measurement
from utils.logger import setup_logger
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType
from .performance_metrics import PerformanceMetrics

class RealQuantumSimulator:
    """
    量子仿真器（向后兼容接口）
    
    该类保持与原有代码的向后兼容性，同时桥接到新的通用仿真器。
    
    警告：建议使用 UniversalQuantumSimulator 以获得完整的通用仿真功能。
    
    迁移示例：
    # 旧方式
    simulator = RealQuantumSimulator(protocol_graph)
    result = simulator.run()
    
    # 新方式（推荐）
    from .universal_quantum_simulator import UniversalQuantumSimulator
    simulator = UniversalQuantumSimulator()
    result = simulator.simulate_universal_protocol(protocol_features, params)
    """
    
    def __init__(self, protocol_graph: Optional[ProtocolGraph] = None):
        """
        初始化量子仿真器
        
        如果通用仿真器可用，将委托给它；否则使用传统实现。
        """
        self.logger = setup_logger(__name__)
        self.protocol_graph = protocol_graph
        
        # 优先使用通用仿真器
        if _UNIVERSAL_SIMULATOR_AVAILABLE:
            self._simulator = UniversalQuantumSimulator(protocol_graph)
            self._use_universal = True
            self.logger.info("使用通用量子仿真器")
        else:
            # 回退到传统实现
            self._use_universal = False
            self._init_legacy_simulator()
            self.logger.info("使用传统量子仿真器")
    
    def _init_legacy_simulator(self):
        """初始化传统仿真器组件"""
        # 初始化子组件
        self.state_preparation = StatePreparation()
        self.channel_model = ChannelModel()
        self.measurement = Measurement()
        self.performance_metrics = PerformanceMetrics()

        # 如果提供了图，则提取节点
        if self.protocol_graph:
            self.qsp_nodes = self.protocol_graph.get_nodes_by_type(NodeType.QSP)
            self.qc_nodes = self.protocol_graph.get_nodes_by_type(NodeType.QC)
            self.qm_node = self.protocol_graph.find_first_node_by_type(NodeType.QM)
            self.bsm_node = self.protocol_graph.find_first_node_by_type(NodeType.BSM)

    def run(self) -> Dict[str, Any]:
        """
        运行完整仿真（向后兼容接口）
        
        如果通用仿真器可用，优先使用通用方法；否则回退到传统方法。
        """
        if not self.protocol_graph:
            raise ValueError("仿真器未使用ProtocolGraph初始化")
        
        if self._use_universal:
            # 使用通用仿真器
            return self._simulator.run()
        else:
            # 使用传统方法
            return self._run_legacy_simulation()
    
    def _run_legacy_simulation(self) -> Dict[str, Any]:
        """运行传统仿真方法"""
        # 通过查看QSP参数中的'intensities'来检查诱骗态协议
        is_decoy = 'intensities' in self.qsp_nodes[0].params if self.qsp_nodes else False

        if is_decoy:
            return self._run_decoy_state_simulation()
        elif self.bsm_node: # MDI-QKD类协议
            return self._run_mdi_simulation()
        elif self.qm_node: # BB84类协议
            return self._run_bb84_simulation()
        else:
            self.logger.warning(
                "协议结构不被支持或无效（例如，缺少测量节点）。"
                "返回一个失败结果（qber=1, gain=0）。"
            )
            return {'qber': 1.0, 'gain': 0.0, 'error': 'Unsupported protocol structure'}
            
    # ==================== 新增通用接口 ====================
    
    def simulate_universal_protocol(self, protocol_features, experimental_params):
        """
        通用协议仿真接口
        
        如果通用仿真器可用，委托给它；否则抛出异常。
        """
        if self._use_universal:
            return self._simulator.simulate_universal_protocol(protocol_features, experimental_params)
        else:
            raise NotImplementedError(
                "Universal protocol simulation requires the universal framework. "
                "Please install the universal_quantum_simulator module."
            )
    
    def parse_quantum_operations(self, operations):
        """量子操作解析接口"""
        if self._use_universal:
            return self._simulator.parse_quantum_operations(operations)
        else:
            raise NotImplementedError(
                "Quantum operation parsing requires the universal framework."
            )
    
    def evolve_quantum_state(self, state, operation_type, **kwargs):
        """量子态演化接口"""
        if self._use_universal:
            return self._simulator.evolve_quantum_state(state, operation_type, **kwargs)
        else:
            raise NotImplementedError(
                "Quantum state evolution requires the universal framework."
            )
    
    # ==================== 传统仿真方法（已弃用） ====================
    
    def _run_bb84_simulation(self) -> Dict[str, float]:
        """运行BB84类协议的仿真（已弃用）"""
        warnings.warn(
            "_run_bb84_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        self.logger.info("检测到BB84类协议，正在运行传统仿真...")
        qsp_node = self.qsp_nodes[0]
        qc_node = self.qc_nodes[0]
        qm_node = self.qm_node

        num_pulses = qsp_node.params.get('num_states', 100000)
        channel_params = qc_node.params
        
        alice_bits = []
        bob_bits = []
        
        for _ in tqdm(range(num_pulses), desc="仿真BB84脉冲"):
            alice_basis = np.random.choice(qsp_node.params.get('basis_choice', ['Z', 'X']))
            ideal_bit = np.random.randint(0, 2)
            bob_basis = np.random.choice(qm_node.params.get('basis_choice', ['Z', 'X']))

            result = self.simulate_single_pulse(
                alice_params={'basis': alice_basis, 'bit': ideal_bit},
                channel_params=channel_params,
                bob_params={'basis': bob_basis}
            )

            if result['detected'] and alice_basis == bob_basis:
                alice_bits.append(ideal_bit)
                measured_bit = 0 if (result['outcome'] == 0 or result['outcome'] == '+') else 1
                bob_bits.append(measured_bit)

        qber = self.performance_metrics.calculate_qber(alice_bits, bob_bits)
        gain = self.performance_metrics.calculate_gain(num_pulses, len(bob_bits))

        return {'qber': qber, 'gain': gain}

    def _run_mdi_simulation(self) -> Dict[str, float]:
        """运行MDI-QKD类协议的仿真（已弃用）"""
        warnings.warn(
            "_run_mdi_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        self.logger.info("检测到MDI-QKD类协议，正在运行传统仿真...")
        # 假设有两个QSP节点（Alice和Bob）和两个信道
        alice_qsp, bob_qsp = self.qsp_nodes[0], self.qsp_nodes[1]
        alice_qc, bob_qc = self.qc_nodes[0], self.qc_nodes[1]
        
        num_pulses = alice_qsp.params.get('num_states', 100000)
        successful_measurements = 0
        mismatched_bits = 0

        for _ in tqdm(range(num_pulses), desc="仿真MDI-QKD脉冲"):
            # Alice和Bob独立准备他们的态
            alice_basis = np.random.choice(alice_qsp.params.get('basis_choice', ['Z', 'X']))
            alice_bit = np.random.randint(0, 2)
            bob_basis = np.random.choice(bob_qsp.params.get('basis_choice', ['Z', 'X']))
            bob_bit = np.random.randint(0, 2)
            
            # 这是BSM的高度简化模型。真实的模型要复杂得多。
            # 这里，我们只是检查两个光子是否都会到达以及基础是否匹配。
            # 在MDI中，如果Alice和Bob选择相同的基础，他们的比特应该相关。
            # 例如，对于Z基础，如果Alice发送0而Bob发送0，他们应该得到相关的结果。
            
            # 仿真两条路径的探测概率
            alice_detected = np.random.rand() > alice_qc.params.get('loss', 0.1)
            bob_detected = np.random.rand() > bob_qc.params.get('loss', 0.1)
            
            # 只有当两个光子都到达时，BSM才成功
            if alice_detected and bob_detected:
                successful_measurements += 1
                # 如果基础匹配，检查错误（由信道引入）
                if alice_basis == bob_basis:
                    # 仿真Alice和Bob的信道错误
                    alice_has_error = np.random.rand() < alice_qc.params.get('error_rate', 0.0)
                    bob_has_error = np.random.rand() < bob_qc.params.get('error_rate', 0.0)
                    
                    # 如果一条路径有错误而另一条没有，则发生错误
                    if alice_has_error != bob_has_error:
                         mismatched_bits += 1

        gain = successful_measurements / num_pulses
        qber = mismatched_bits / successful_measurements if successful_measurements > 0 else 0
        
        return {'qber': qber, 'gain': gain}

    def _run_decoy_state_simulation(self) -> Dict[str, Dict[str, float]]:
        """运行诱骗态BB84协议的仿真（已弃用）"""
        warnings.warn(
            "_run_decoy_state_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        self.logger.info("检测到诱骗态协议，正在运行传统仿真...")
        
        qsp_params = self.qsp_nodes[0].params
        qm_params = self.qm_node.params
        channel_params = self.qc_nodes[0].params
        intensities_config = qsp_params.get('intensities', {})
        
        results_by_intensity = {}

        for name, intensity_params in intensities_config.items():
            intensity_val = intensity_params['value']
            num_pulses_for_intensity = int(qsp_params['num_states'] * intensity_params['probability'])
            self.logger.info(f"正在仿真强度 '{name}' (μ={intensity_val})，使用 {num_pulses_for_intensity} 个脉冲...")

            # 我们需要将强度添加到态准备参数中
            # 如果它是光子数相关的，也要添加到信道模型中
            
            alice_bits, bob_bits = [], []
            for _ in tqdm(range(num_pulses_for_intensity), desc=f"强度 {name}"):
                alice_basis = np.random.choice(qsp_params.get('basis_choice', ['Z', 'X']))
                ideal_bit = np.random.randint(0, 2)
                bob_basis = np.random.choice(qm_params.get('basis_choice', ['Z', 'X']))
                
                # 这里，我们还应该将强度值传递给信道
                # 对于简单模型，我们可以假设损耗/错误影响所有光子
                # 更高级的模型会根据光子数有不同的效果。
                
                result = self.simulate_single_pulse(
                    alice_params={'basis': alice_basis, 'bit': ideal_bit, 'intensity': intensity_val},
                    channel_params=channel_params,
                    bob_params={'basis': bob_basis}
                )

                if result['detected'] and alice_basis == bob_basis:
                    alice_bits.append(ideal_bit)
                    measured_bit = 0 if (result['outcome'] == 0 or result['outcome'] == '+') else 1
                    bob_bits.append(measured_bit)

            qber = self.performance_metrics.calculate_qber(alice_bits, bob_bits)
            gain = self.performance_metrics.calculate_gain(num_pulses_for_intensity, len(bob_bits))
            results_by_intensity[name] = {'qber': qber, 'gain': gain}

        return results_by_intensity

    def simulate_single_pulse(self,
                              alice_params: Dict[str, Any],
                              channel_params: Dict[str, Any],
                              bob_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        仿真单个量子脉冲（向后兼容接口）
        
        该方法保持与原有代码的完全兼容性。
        如果通用仿真器可用，优先使用其实现。
        
        参数:
            alice_params: 态准备参数 (例如, {'basis': 'Z', 'bit': 0})
            channel_params: 信道参数 (例如, {'loss': 0.0, 'error_rate': 0.0})
            bob_params: 测量参数 (例如, {'basis': 'Z'})
        
        返回:
            包含脉冲仿真结果的字典
        """
        if self._use_universal:
            # 使用通用仿真器的实现
            return self._simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
        else:
            # 使用传统实现
            return self._simulate_single_pulse_legacy(alice_params, channel_params, bob_params)
    
    def _simulate_single_pulse_legacy(self,
                                    alice_params: Dict[str, Any],
                                    channel_params: Dict[str, Any],
                                    bob_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        传统单脉冲仿真实现
        
        这是原有的TDD方法的核心实现，保持完全向后兼容。
        """
        # 1. 态准备
        initial_state = self.state_preparation.simulate_state_preparation(alice_params)

        # 2. 信道传输
        state_after_channel = self.channel_model.simulate_channel_transmission(
            initial_state, channel_params
        )

        # 3. 测量
        measurement_result = self.measurement.simulate_measurement(
            state_after_channel, bob_params
        )

        # 4. 格式化和返回结果
        outcome = measurement_result.get('outcome')
        detected = (outcome is not None and outcome != 'no_click')
        
        return {
            'outcome': outcome,
            'detected': detected,
            'final_state_info': measurement_result
        }


# ==================== 向后兼容性导出 ====================

__all__ = [
    'RealQuantumSimulator',
    'UniversalQuantumSimulator' if _UNIVERSAL_SIMULATOR_AVAILABLE else None
]

# 移除None值
__all__ = [item for item in __all__ if item is not None]

# 如果通用仿真器可用，也导出它
if _UNIVERSAL_SIMULATOR_AVAILABLE:
    from .universal_quantum_simulator import UniversalQuantumSimulator
    
    # 为了完全向后兼容，确保导出的类可以正常使用
    assert hasattr(UniversalQuantumSimulator, 'simulate_universal_protocol')
    assert hasattr(UniversalQuantumSimulator, 'parse_quantum_operations')
    assert hasattr(UniversalQuantumSimulator, 'evolve_quantum_state') 