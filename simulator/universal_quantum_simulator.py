"""
通用量子仿真器（Universal Quantum Simulator）

基于量子信息论的通用仿真框架，支持任意协议结构的物理精确仿真。
该模块实现了现代量子仿真的核心功能：

- 通用协议仿真：支持基于ProtocolFeatures的任意协议
- 量子操作解析：自动解析和执行量子操作序列
- 量子态演化：物理精确的量子态演化仿真
- 向后兼容性：保持与传统协议图的兼容

理论基础：
- Nielsen & Chuang: Quantum Computation and Quantum Information
- Preskill: Quantum Information Theory
- 现代量子仿真技术和优化方法

作者：AI4QKD Team
版本：2.0 - Universal Simulation Framework
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
import warnings
from tqdm import tqdm

# 导入子模块
from .state_preparation import StatePreparation
from .channel_model import ChannelModel
from .measurement import Measurement
from .performance_metrics import PerformanceMetrics
from utils.logger import setup_logger

# 导入协议图相关（向后兼容）
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType

# 导入通用框架
try:
    from security_evaluator.universal_framework import (
        QuantumOperation,
        ProtocolFeatures,
        QuantumOperationType
    )
    UNIVERSAL_FRAMEWORK_AVAILABLE = True
except ImportError:
    UNIVERSAL_FRAMEWORK_AVAILABLE = False
    warnings.warn(
        "Universal framework not available. Some features will be limited.",
        ImportWarning
    )


@dataclass
class SimulationResult:
    """仿真结果数据类"""
    qber: float
    gain: float
    raw_measurements: Optional[int] = None
    successful_measurements: Optional[int] = None
    total_pulses: Optional[int] = None
    protocol_specific_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class UniversalQuantumSimulator:
    """
    通用量子仿真器
    
    基于量子信息论的通用仿真框架，支持任意协议结构的
    物理精确仿真。
    """
    
    def __init__(self, protocol_graph: Optional[ProtocolGraph] = None):
        """
        初始化通用量子仿真器
        
        Args:
            protocol_graph: 可选的传统协议图（向后兼容）
        """
        self.logger = setup_logger(__name__)
        self.protocol_graph = protocol_graph
        
        # 初始化子组件
        self.state_preparation = StatePreparation()
        self.channel_model = ChannelModel()
        self.measurement = Measurement()
        self.performance_metrics = PerformanceMetrics()
        
        # 向后兼容：提取传统协议图节点
        if self.protocol_graph:
            self._extract_legacy_nodes()
        
        self.logger.info("通用量子仿真器已初始化")
    
    def _extract_legacy_nodes(self):
        """提取传统协议图的节点（向后兼容）"""
        try:
            self.qsp_nodes = self.protocol_graph.get_nodes_by_type(NodeType.QSP)
            self.qc_nodes = self.protocol_graph.get_nodes_by_type(NodeType.QC)
            self.qm_node = self.protocol_graph.find_first_node_by_type(NodeType.QM)
            self.bsm_node = self.protocol_graph.find_first_node_by_type(NodeType.BSM)
        except Exception as e:
            self.logger.warning(f"提取传统协议图节点失败: {e}")
            self.qsp_nodes = []
            self.qc_nodes = []
            self.qm_node = None
            self.bsm_node = None
    
    def simulate_universal_protocol(self, 
                                  protocol_features: 'ProtocolFeatures',
                                  experimental_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用协议仿真
        
        基于ProtocolFeatures描述的协议特征进行物理精确仿真
        
        Args:
            protocol_features: 协议特征描述
            experimental_params: 实验参数
            
        Returns:
            仿真结果字典
        """
        if not UNIVERSAL_FRAMEWORK_AVAILABLE:
            raise ImportError("Universal framework required for universal protocol simulation")
        
        self.logger.info(f"开始通用协议仿真: {protocol_features.name}")
        
        try:
            # 1. 解析量子操作序列
            operation_sequence = self.parse_quantum_operations(protocol_features.operations)
            
            # 2. 根据协议特征确定仿真策略
            simulation_strategy = self._determine_simulation_strategy(
                protocol_features, experimental_params
            )
            
            # 3. 执行仿真
            if simulation_strategy == 'decoy_state':
                result = self._simulate_decoy_state_protocol(
                    protocol_features, operation_sequence, experimental_params
                )
            elif simulation_strategy == 'mdi_qkd':
                result = self._simulate_mdi_protocol(
                    protocol_features, operation_sequence, experimental_params
                )
            else:
                result = self._simulate_standard_protocol(
                    protocol_features, operation_sequence, experimental_params
                )
            
            self.logger.info(f"协议仿真完成: QBER={result.get('qber', 0):.6f}, Gain={result.get('gain', 0):.6f}")
            return result
            
        except Exception as e:
            self.logger.error(f"通用协议仿真失败: {e}")
            return {
                'qber': 1.0,
                'gain': 0.0,
                'error': str(e)
            }
    
    def parse_quantum_operations(self, operations: List['QuantumOperation']) -> List[Dict[str, Any]]:
        """
        解析量子操作序列
        
        将ProtocolFeatures中的QuantumOperation对象解析为
        仿真器可执行的操作序列
        
        Args:
            operations: 量子操作列表
            
        Returns:
            解析后的操作序列
        """
        parsed_operations = []
        
        for i, op in enumerate(operations):
            try:
                parsed_op = {
                    'id': i,
                    'name': op.name,
                    'type': self._map_operation_type(op.operation_type),
                    'parameters': op.parameters.copy() if op.parameters else {},
                    'matrix': op.matrix,
                    'dimension': op.dimension
                }
                
                # 验证操作的有效性
                self._validate_operation(parsed_op)
                
                parsed_operations.append(parsed_op)
                
            except Exception as e:
                self.logger.error(f"解析操作 {op.name} 失败: {e}")
                raise ValueError(f"Invalid operation {op.name}: {e}")
        
        self.logger.debug(f"成功解析 {len(parsed_operations)} 个量子操作")
        return parsed_operations
    
    def _map_operation_type(self, op_type: Union['QuantumOperationType', str]) -> str:
        """映射操作类型到仿真器内部格式"""
        if hasattr(op_type, 'value'):
            return op_type.value
        return str(op_type).lower()
    
    def _validate_operation(self, operation: Dict[str, Any]):
        """验证操作的有效性"""
        op_type = operation['type']
        
        if op_type == 'unitary':
            # 验证幺正矩阵
            if operation['matrix'] is not None:
                matrix = np.array(operation['matrix'])
                if not self._is_unitary(matrix):
                    raise ValueError(f"Matrix for {operation['name']} is not unitary")
        
        elif op_type == 'measurement':
            # 验证测量参数
            if 'basis' not in operation['parameters']:
                self.logger.warning(f"Measurement {operation['name']} missing basis parameter")
        
        elif op_type == 'channel':
            # 验证信道参数
            params = operation['parameters']
            if 'loss' in params and not (0 <= params['loss'] <= 1):
                raise ValueError(f"Invalid loss parameter for {operation['name']}")
    
    def _is_unitary(self, matrix: np.ndarray, tolerance: float = 1e-10) -> bool:
        """检查矩阵是否为幺正矩阵"""
        try:
            U = np.array(matrix, dtype=complex)
            U_dag = U.conj().T
            identity = np.eye(U.shape[0])
            
            return (np.allclose(U @ U_dag, identity, atol=tolerance) and
                   np.allclose(U_dag @ U, identity, atol=tolerance))
        except:
            return False
    
    def evolve_quantum_state(self, 
                           state: np.ndarray,
                           operation_type: str,
                           **kwargs) -> Union[np.ndarray, Dict[str, Any]]:
        """
        量子态演化
        
        根据指定的操作类型演化量子态
        
        Args:
            state: 输入量子态（密度矩阵）
            operation_type: 操作类型
            **kwargs: 操作参数
            
        Returns:
            演化后的量子态或测量结果
        """
        try:
            if operation_type == 'unitary':
                return self._evolve_unitary(state, kwargs.get('operation_matrix'))
            
            elif operation_type == 'channel':
                return self._evolve_channel(state, kwargs.get('channel_params', {}))
            
            elif operation_type == 'measurement':
                return self._evolve_measurement(state, kwargs.get('measurement_basis', 'Z'))
            
            else:
                raise ValueError(f"Unknown operation type: {operation_type}")
                
        except Exception as e:
            self.logger.error(f"量子态演化失败: {e}")
            raise
    
    def _evolve_unitary(self, state: np.ndarray, unitary_matrix: np.ndarray) -> np.ndarray:
        """幺正演化"""
        if unitary_matrix is None:
            return state
        
        U = np.array(unitary_matrix, dtype=complex)
        return U @ state @ U.conj().T
    
    def _evolve_channel(self, state: np.ndarray, channel_params: Dict[str, Any]) -> np.ndarray:
        """信道演化"""
        channel_type = channel_params.get('type', 'identity')
        
        if channel_type == 'depolarizing':
            p = channel_params.get('probability', 0.0)
            d = state.shape[0]
            identity = np.eye(d) / d
            return (1 - p) * state + p * identity
        
        elif channel_type == 'amplitude_damping':
            gamma = channel_params.get('damping_rate', 0.0)
            # 简化的振幅阻尼模型
            return (1 - gamma) * state + gamma * np.array([[1, 0], [0, 0]])
        
        else:
            # 默认：恒等信道
            return state
    
    def _evolve_measurement(self, state: np.ndarray, basis: str) -> Dict[str, Any]:
        """测量演化"""
        if basis == 'Z':
            # Z基测量算子
            M_0 = np.array([[1, 0], [0, 0]], dtype=complex)
            M_1 = np.array([[0, 0], [0, 1]], dtype=complex)
        elif basis == 'X':
            # X基测量算子
            M_plus = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
            M_minus = 0.5 * np.array([[1, -1], [-1, 1]], dtype=complex)
            M_0, M_1 = M_plus, M_minus
        else:
            raise ValueError(f"Unknown measurement basis: {basis}")
        
        # 计算测量概率
        prob_0 = np.real(np.trace(M_0 @ state))
        prob_1 = np.real(np.trace(M_1 @ state))
        
        # 归一化概率
        total_prob = prob_0 + prob_1
        if total_prob > 1e-12:
            prob_0 /= total_prob
            prob_1 /= total_prob
        
        # 计算后验态
        post_state_0 = (M_0 @ state @ M_0.conj().T) / prob_0 if prob_0 > 1e-12 else None
        post_state_1 = (M_1 @ state @ M_1.conj().T) / prob_1 if prob_1 > 1e-12 else None
        
        return {
            'probabilities': [prob_0, prob_1],
            'post_states': [post_state_0, post_state_1],
            'measurement_operators': [M_0, M_1]
        }
    
    def _determine_simulation_strategy(self, 
                                     protocol_features: 'ProtocolFeatures',
                                     experimental_params: Dict[str, Any]) -> str:
        """确定仿真策略"""
        # 检查是否为诱骗态协议
        if (protocol_features.decoy_states or 
            'intensity_settings' in experimental_params):
            return 'decoy_state'
        
        # 检查是否为MDI-QKD协议
        if (len(protocol_features.untrusted_parties) > 0 or
            'alice_channel_loss' in experimental_params):
            return 'mdi_qkd'
        
        # 默认：标准协议
        return 'standard'
    
    def _simulate_standard_protocol(self,
                                  protocol_features: 'ProtocolFeatures',
                                  operation_sequence: List[Dict[str, Any]],
                                  experimental_params: Dict[str, Any]) -> Dict[str, Any]:
        """仿真标准协议（如BB84）"""
        num_pulses = experimental_params.get('num_pulses', 100000)
        basis_choices = experimental_params.get('basis_choices', ['Z', 'X'])
        channel_loss = experimental_params.get('channel_loss', 0.1)
        channel_error_rate = experimental_params.get('channel_error_rate', 0.02)
        
        alice_bits = []
        bob_bits = []
        
        for _ in tqdm(range(num_pulses), desc=f"仿真{protocol_features.name}脉冲"):
            # 随机选择基和比特
            alice_basis = np.random.choice(basis_choices)
            alice_bit = np.random.randint(0, 2)
            bob_basis = np.random.choice(basis_choices)
            
            # 仿真单脉冲
            result = self.simulate_single_pulse(
                alice_params={'basis': alice_basis, 'bit': alice_bit},
                channel_params={'loss': channel_loss, 'error_rate': channel_error_rate},
                bob_params={'basis': bob_basis}
            )
            
            # 收集匹配基的结果
            if result['detected'] and alice_basis == bob_basis:
                alice_bits.append(alice_bit)
                measured_bit = 0 if (result['outcome'] == 0 or result['outcome'] == '+') else 1
                bob_bits.append(measured_bit)
        
        # 计算性能指标
        qber = self.performance_metrics.calculate_qber(alice_bits, bob_bits)
        gain = self.performance_metrics.calculate_gain(num_pulses, len(bob_bits))
        
        return {
            'qber': qber,
            'gain': gain,
            'raw_measurements': len(bob_bits),
            'total_pulses': num_pulses
        }
    
    def _simulate_mdi_protocol(self,
                             protocol_features: 'ProtocolFeatures',
                             operation_sequence: List[Dict[str, Any]],
                             experimental_params: Dict[str, Any]) -> Dict[str, Any]:
        """仿真MDI-QKD协议"""
        num_pulses = experimental_params.get('num_pulses', 100000)
        alice_loss = experimental_params.get('alice_channel_loss', 0.15)
        bob_loss = experimental_params.get('bob_channel_loss', 0.15)
        alice_error = experimental_params.get('alice_channel_error', 0.01)
        bob_error = experimental_params.get('bob_channel_error', 0.01)
        basis_choices = experimental_params.get('basis_choices', ['Z', 'X'])
        
        successful_measurements = 0
        mismatched_bits = 0
        
        for _ in tqdm(range(num_pulses), desc=f"仿真{protocol_features.name}脉冲"):
            # Alice和Bob独立准备态
            alice_basis = np.random.choice(basis_choices)
            alice_bit = np.random.randint(0, 2)
            bob_basis = np.random.choice(basis_choices)
            bob_bit = np.random.randint(0, 2)
            
            # 仿真双路径传输
            alice_detected = np.random.rand() > alice_loss
            bob_detected = np.random.rand() > bob_loss
            
            # 只有两个光子都到达时BSM才成功
            if alice_detected and bob_detected:
                successful_measurements += 1
                
                # 检查基匹配时的错误
                if alice_basis == bob_basis:
                    alice_has_error = np.random.rand() < alice_error
                    bob_has_error = np.random.rand() < bob_error
                    
                    # 一条路径有错误而另一条没有时发生错误
                    if alice_has_error != bob_has_error:
                        mismatched_bits += 1
        
        gain = successful_measurements / num_pulses
        qber = mismatched_bits / successful_measurements if successful_measurements > 0 else 0
        
        return {
            'qber': qber,
            'gain': gain,
            'successful_measurements': successful_measurements,
            'total_pulses': num_pulses
        }
    
    def _simulate_decoy_state_protocol(self,
                                     protocol_features: 'ProtocolFeatures',
                                     operation_sequence: List[Dict[str, Any]],
                                     experimental_params: Dict[str, Any]) -> Dict[str, Any]:
        """仿真诱骗态协议"""
        num_pulses = experimental_params.get('num_pulses', 100000)
        intensity_settings = experimental_params.get('intensity_settings', {
            'signal': {'value': 0.5, 'probability': 0.7},
            'decoy': {'value': 0.1, 'probability': 0.2},
            'vacuum': {'value': 0.0, 'probability': 0.1}
        })
        basis_choices = experimental_params.get('basis_choices', ['Z', 'X'])
        channel_loss = experimental_params.get('channel_loss', 0.1)
        channel_error_rate = experimental_params.get('channel_error_rate', 0.02)
        
        results_by_intensity = {}
        
        for intensity_name, intensity_config in intensity_settings.items():
            intensity_value = intensity_config['value']
            intensity_prob = intensity_config['probability']
            num_pulses_for_intensity = int(num_pulses * intensity_prob)
            
            if num_pulses_for_intensity == 0:
                continue
            
            self.logger.info(f"仿真强度 {intensity_name} (μ={intensity_value})")
            
            alice_bits, bob_bits = [], []
            
            for _ in tqdm(range(num_pulses_for_intensity), desc=f"强度 {intensity_name}"):
                alice_basis = np.random.choice(basis_choices)
                alice_bit = np.random.randint(0, 2)
                bob_basis = np.random.choice(basis_choices)
                
                # 仿真单脉冲（包含强度信息）
                result = self.simulate_single_pulse(
                    alice_params={'basis': alice_basis, 'bit': alice_bit, 'intensity': intensity_value},
                    channel_params={'loss': channel_loss, 'error_rate': channel_error_rate},
                    bob_params={'basis': bob_basis}
                )
                
                if result['detected'] and alice_basis == bob_basis:
                    alice_bits.append(alice_bit)
                    measured_bit = 0 if (result['outcome'] == 0 or result['outcome'] == '+') else 1
                    bob_bits.append(measured_bit)
            
            qber = self.performance_metrics.calculate_qber(alice_bits, bob_bits)
            gain = self.performance_metrics.calculate_gain(num_pulses_for_intensity, len(bob_bits))
            
            results_by_intensity[intensity_name] = {
                'qber': qber,
                'gain': gain,
                'raw_measurements': len(bob_bits),
                'pulses_for_intensity': num_pulses_for_intensity
            }
        
        return results_by_intensity
    
    # ==================== 向后兼容接口 ====================
    
    def run(self) -> Dict[str, Any]:
        """
        运行仿真（向后兼容接口）
        
        如果可能，优先使用通用仿真；否则回退到传统方法
        """
        if not self.protocol_graph:
            raise ValueError("仿真器未使用ProtocolGraph初始化")
        
        # 尝试转换为通用协议格式
        if UNIVERSAL_FRAMEWORK_AVAILABLE:
            try:
                protocol_features = self._convert_legacy_to_universal()
                experimental_params = self._extract_experimental_params()
                
                self.logger.info("使用通用仿真引擎")
                return self.simulate_universal_protocol(protocol_features, experimental_params)
                
            except Exception as e:
                self.logger.warning(f"通用仿真失败，回退到传统方法: {e}")
        
        # 回退到传统方法
        return self._run_legacy_simulation()
    
    def _convert_legacy_to_universal(self) -> 'ProtocolFeatures':
        """将传统协议图转换为通用协议特征"""
        from security_evaluator.universal_framework import ProtocolFeatures, QuantumOperation, QuantumOperationType
        
        # 根据节点结构推断协议类型
        operations = []
        parties = ['Alice', 'Bob']
        
        # 添加态准备操作
        if self.qsp_nodes:
            for i, qsp_node in enumerate(self.qsp_nodes):
                operations.append(QuantumOperation(
                    name=f"state_prep_{i}",
                    operation_type=QuantumOperationType.PREPARATION,
                    parameters=qsp_node.params
                ))
        
        # 添加信道操作
        if self.qc_nodes:
            for i, qc_node in enumerate(self.qc_nodes):
                operations.append(QuantumOperation(
                    name=f"channel_{i}",
                    operation_type=QuantumOperationType.CHANNEL,
                    parameters=qc_node.params
                ))
        
        # 添加测量操作
        if self.qm_node:
            operations.append(QuantumOperation(
                name="measurement",
                operation_type=QuantumOperationType.MEASUREMENT,
                parameters=self.qm_node.params
            ))
        elif self.bsm_node:
            operations.append(QuantumOperation(
                name="bell_measurement",
                operation_type=QuantumOperationType.MEASUREMENT,
                parameters=self.bsm_node.params
            ))
            parties.append('Charlie')  # MDI-QKD需要第三方
        
        # 检查协议特征
        is_decoy = self.qsp_nodes and 'intensities' in self.qsp_nodes[0].params
        is_mdi = self.bsm_node is not None
        
        return ProtocolFeatures(
            name="Legacy_Protocol",
            operations=operations,
            parties=parties,
            communication_rounds=1,
            measurement_bases=2,
            decoy_states=is_decoy,
            trusted_parties=['Alice', 'Bob'] if is_mdi else parties,
            untrusted_parties=['Charlie'] if is_mdi else []
        )
    
    def _extract_experimental_params(self) -> Dict[str, Any]:
        """从传统协议图提取实验参数"""
        params = {
            'num_pulses': 100000,  # 默认值
            'basis_choices': ['Z', 'X'],
            'channel_loss': 0.1,
            'channel_error_rate': 0.02
        }
        
        # 从QSP节点提取参数
        if self.qsp_nodes:
            qsp_params = self.qsp_nodes[0].params
            params['num_pulses'] = qsp_params.get('num_states', params['num_pulses'])
            params['basis_choices'] = qsp_params.get('basis_choice', params['basis_choices'])
            
            # 诱骗态参数
            if 'intensities' in qsp_params:
                params['intensity_settings'] = qsp_params['intensities']
        
        # 从QC节点提取信道参数
        if self.qc_nodes:
            qc_params = self.qc_nodes[0].params
            params['channel_loss'] = qc_params.get('loss', params['channel_loss'])
            params['channel_error_rate'] = qc_params.get('error_rate', params['channel_error_rate'])
            
            # MDI-QKD双信道参数
            if len(self.qc_nodes) >= 2:
                params['alice_channel_loss'] = self.qc_nodes[0].params.get('loss', 0.1)
                params['bob_channel_loss'] = self.qc_nodes[1].params.get('loss', 0.1)
                params['alice_channel_error'] = self.qc_nodes[0].params.get('error_rate', 0.01)
                params['bob_channel_error'] = self.qc_nodes[1].params.get('error_rate', 0.01)
        
        return params
    
    def _run_legacy_simulation(self) -> Dict[str, Any]:
        """运行传统仿真方法（完全向后兼容）"""
        # 检查诱骗态协议
        is_decoy = self.qsp_nodes and 'intensities' in self.qsp_nodes[0].params
        
        if is_decoy:
            return self._run_decoy_state_simulation()
        elif self.bsm_node:  # MDI-QKD类协议
            return self._run_mdi_simulation()
        elif self.qm_node:  # BB84类协议
            return self._run_bb84_simulation()
        else:
            self.logger.warning("协议结构不被支持或无效")
            return {'qber': 1.0, 'gain': 0.0, 'error': 'Unsupported protocol structure'}
    
    def simulate_single_pulse(self,
                            alice_params: Dict[str, Any],
                            channel_params: Dict[str, Any],
                            bob_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        仿真单个量子脉冲（向后兼容接口）
        
        这是核心的单脉冲仿真方法，保持与原有接口的完全兼容性
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
        
        # 4. 格式化结果
        outcome = measurement_result.get('outcome')
        detected = (outcome is not None and outcome != 'no_click')
        
        return {
            'outcome': outcome,
            'detected': detected,
            'final_state_info': measurement_result
        }
    
    # ==================== 传统仿真方法（将被移除） ====================
    
    def _run_bb84_simulation(self) -> Dict[str, float]:
        """运行BB84类协议的仿真（传统方法）"""
        warnings.warn(
            "_run_bb84_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning
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
        """运行MDI-QKD类协议的仿真（传统方法）"""
        warnings.warn(
            "_run_mdi_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning
        )
        
        self.logger.info("检测到MDI-QKD类协议，正在运行传统仿真...")
        alice_qsp, bob_qsp = self.qsp_nodes[0], self.qsp_nodes[1]
        alice_qc, bob_qc = self.qc_nodes[0], self.qc_nodes[1]
        
        num_pulses = alice_qsp.params.get('num_states', 100000)
        successful_measurements = 0
        mismatched_bits = 0

        for _ in tqdm(range(num_pulses), desc="仿真MDI-QKD脉冲"):
            alice_basis = np.random.choice(alice_qsp.params.get('basis_choice', ['Z', 'X']))
            alice_bit = np.random.randint(0, 2)
            bob_basis = np.random.choice(bob_qsp.params.get('basis_choice', ['Z', 'X']))
            bob_bit = np.random.randint(0, 2)
            
            alice_detected = np.random.rand() > alice_qc.params.get('loss', 0.1)
            bob_detected = np.random.rand() > bob_qc.params.get('loss', 0.1)
            
            if alice_detected and bob_detected:
                successful_measurements += 1
                if alice_basis == bob_basis:
                    alice_has_error = np.random.rand() < alice_qc.params.get('error_rate', 0.0)
                    bob_has_error = np.random.rand() < bob_qc.params.get('error_rate', 0.0)
                    
                    if alice_has_error != bob_has_error:
                         mismatched_bits += 1

        gain = successful_measurements / num_pulses
        qber = mismatched_bits / successful_measurements if successful_measurements > 0 else 0
        
        return {'qber': qber, 'gain': gain}
    
    def _run_decoy_state_simulation(self) -> Dict[str, Dict[str, float]]:
        """运行诱骗态BB84协议的仿真（传统方法）"""
        warnings.warn(
            "_run_decoy_state_simulation is deprecated. Use simulate_universal_protocol instead.",
            DeprecationWarning
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
            
            alice_bits, bob_bits = [], []
            for _ in tqdm(range(num_pulses_for_intensity), desc=f"强度 {name}"):
                alice_basis = np.random.choice(qsp_params.get('basis_choice', ['Z', 'X']))
                ideal_bit = np.random.randint(0, 2)
                bob_basis = np.random.choice(qm_params.get('basis_choice', ['Z', 'X']))
                
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


# ==================== 向后兼容性别名 ====================

# 保持原有类名的别名
RealQuantumSimulator = UniversalQuantumSimulator