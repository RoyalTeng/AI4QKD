import gymnasium as gym
from gymnasium import spaces
from typing import Dict, Any, Tuple, Optional
import random
import networkx as nx
import logging
import warnings

from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType
from qcgf_dsl.edge_types import EdgeType
from simulator.real_quantum_simulator import RealQuantumSimulator
from security_evaluator.key_rate_calculator import KeyRateCalculator
from security_evaluator.ac_framework import ProtocolType
from .reward_function import calculate_reward

# 导入通用框架
try:
    from simulator.universal_quantum_simulator import UniversalQuantumSimulator
    from security_evaluator.key_rate_calculator import create_universal_key_rate_calculator, migrate_legacy_calculation
    from security_evaluator.entropy_estimator import create_universal_entropy_estimator, migrate_legacy_entropy_calculation
    from security_evaluator.universal_framework import (
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

class QKDSimEnv(gym.Env):
    """
    一个符合Gymnasium接口的QKD协议设计环境（通用版本）。
    
    基于通用框架的AI Agent环境，支持任意协议结构的仿真和评估。
    移除协议类型约束，支持AI自动发现创新QKD协议。
    
    新功能（v2.0）：
    - 基于通用量子仿真器的协议无关仿真
    - 通用安全性分析和熵估计
    - 支持创新协议架构的动作空间
    - 实时性能优化和缓存机制
    - 完全向后兼容的接口
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # --- 通用框架配置 ---
        self.use_universal_framework = config.get("USE_UNIVERSAL_FRAMEWORK", True) and _UNIVERSAL_FRAMEWORK_AVAILABLE
        
        # --- 性能优化：缓存上一步的结果 ---
        self.last_observation = None
        self.last_reward = 0.0
        self.last_info = {}
        
        # --- 动作空间定义（扩展支持更多创新操作）---
        # 动作0: 增加节点 (支持所有节点类型)
        # 动作1: 删除随机节点
        # 动作2: 增加随机边
        # 动作3: 修改随机节点的参数
        # 动作4: 重组协议结构（新增）
        # 动作5: 优化协议参数（新增）
        self.action_space = spaces.Dict({
            "action_type": spaces.Discrete(6),  # 扩展动作空间
            "node_type_to_add": spaces.Discrete(len(NodeType)),
            "param_to_modify": spaces.Discrete(5),  # 扩展参数修改选项
            "param_value": spaces.Box(low=0, high=1, shape=(1,), dtype=float)
        })

        # --- 观察空间定义（扩展以支持更复杂协议）---
        # 观察空间扩展以支持更复杂的协议表示
        self.observation_space = spaces.Box(low=0, high=1, shape=(128,), dtype=float)

        # --- 初始化仿真器和分析器 ---
        self.protocol_graph = ProtocolGraph()
        self._init_simulators_and_analyzers()

    def _create_base_bb84_graph(self) -> ProtocolGraph:
        """创建一个基础的BB84协议图作为训练起点。"""
        graph = ProtocolGraph(name="Base_BB84_for_AI_Train")
        graph.add_node(node_type=NodeType.QSP, node_id="qsp_alice")
        graph.add_node(node_type=NodeType.QC, node_id="qc_channel")
        graph.add_node(node_type=NodeType.QM, node_id="qm_bob")
        graph.add_edge("qsp_alice", "qc_channel", edge_type=EdgeType.QUANTUM)
        graph.add_edge("qc_channel", "qm_bob", edge_type=EdgeType.QUANTUM)
        return graph
    
    def _init_simulators_and_analyzers(self):
        """初始化仿真器和安全分析器"""
        if self.use_universal_framework:
            # 使用通用框架
            try:
                self.universal_simulator = UniversalQuantumSimulator()
                self.universal_security_analyzer = create_universal_key_rate_calculator()
                self.universal_entropy_estimator = create_universal_entropy_estimator()
                self.logger.info("成功初始化通用框架组件")
            except Exception as e:
                self.logger.warning(f"通用框架初始化失败，回退到传统方法: {e}")
                self.use_universal_framework = False
        
        if not self.use_universal_framework:
            # 使用传统框架
            self.simulator = RealQuantumSimulator(self.protocol_graph)
            self.key_rate_calculator = KeyRateCalculator()
            self.logger.info("使用传统框架组件")
    
    def convert_protocol_to_features(self, protocol_graph: ProtocolGraph):
        """将协议图转换为通用框架的协议特征"""
        if not _UNIVERSAL_FRAMEWORK_AVAILABLE:
            return None
            
        try:
            # 分析协议结构
            operations = []

            # 添加量子态准备操作
            qsp_nodes = protocol_graph.get_nodes_by_type(NodeType.QSP)
            for index, node_id in enumerate(qsp_nodes):
                node = protocol_graph.get_node(node_id)
                operations.append(
                    QuantumOperation(
                        name=f"state_preparation_{index}",
                        operation_type=QuantumOperationType.PREPARATION,
                        parameters=node.params or {}
                    )
                )

            # 添加量子信道操作
            qc_nodes = protocol_graph.get_nodes_by_type(NodeType.QC)
            for index, node_id in enumerate(qc_nodes):
                node = protocol_graph.get_node(node_id)
                operations.append(
                    QuantumOperation(
                        name=f"quantum_channel_{index}",
                        operation_type=QuantumOperationType.CHANNEL,
                        parameters=node.params or {}
                    )
                )

            # 添加量子测量操作
            qm_nodes = protocol_graph.get_nodes_by_type(NodeType.QM)
            bsm_nodes = protocol_graph.get_nodes_by_type(NodeType.BSM)
            for index, node_id in enumerate(qm_nodes + bsm_nodes):
                node = protocol_graph.get_node(node_id)
                operations.append(
                    QuantumOperation(
                        name=f"measurement_{index}",
                        operation_type=QuantumOperationType.MEASUREMENT,
                        parameters=node.params or {}
                    )
                )

            # 创建协议特征
            protocol_features = ProtocolFeatures(
                name=protocol_graph.name or "AI_Generated_Protocol",
                operations=operations,
                parties=["Alice", "Bob"],
                communication_rounds=max(1, len(operations)),
                measurement_bases=(
                    max(1, len(qm_nodes)) if qm_nodes else 2
                ),
                decoy_states=any(
                    any(
                        key in (protocol_graph.get_node(node_id).params or {})
                        for key in ('intensity', 'intensities', 'decoy_states')
                    )
                    for node_id in qsp_nodes
                ) if qsp_nodes else False
            )

            return protocol_features

        except Exception as e:
            self.logger.error(f"协议特征转换失败: {e}")
            return None
    
    def run_universal_simulation(self) -> Dict[str, Any]:
        """运行通用仿真"""
        if not self.use_universal_framework:
            # 回退到传统仿真
            return self.simulator.run()
        
        try:
            # 转换协议图为通用特征
            protocol_features = self.convert_protocol_to_features(self.protocol_graph)
            if protocol_features is None:
                raise ValueError("协议特征转换失败")
            
            # 运行通用仿真
            simulation_config = {
                'n_pulses': self.config.get("DEFAULT_NUM_PULSES", 100000),
                'noise_model': 'realistic',
                'channel_model': 'lossy_fiber'
            }
            
            results = self.universal_simulator.simulate_universal_protocol(
                protocol_features, simulation_config
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"通用仿真失败: {e}")
            # 回退到传统仿真
            self.simulator.protocol_graph = self.protocol_graph
            return self.simulator.run()
    
    def analyze_protocol_security(self, protocol_graph: ProtocolGraph, simulation_results: Dict[str, Any]):
        """分析协议安全性"""
        if not self.use_universal_framework:
            # 使用传统安全分析
            compute_params = {
                "qber": simulation_results.get('qber', 0.1),
                "gain": simulation_results.get('gain', 0.5),
                "n_pulses": self.config.get("DEFAULT_NUM_PULSES", 100000),
                "protocol_type": ProtocolType.BB84
            }
            return self.key_rate_calculator.compute(**compute_params)
        
        try:
            # 使用通用安全分析
            protocol_features = self.convert_protocol_to_features(protocol_graph)
            if protocol_features is None:
                raise ValueError("协议特征转换失败")
            
            security_params = UniversalSecurityParameters(
                epsilon_sec=self.config.get("EPSILON_SEC", 1e-10),
                epsilon_cor=self.config.get("EPSILON_COR", 1e-10),
                epsilon_pe=self.config.get("EPSILON_PE", 1e-10)
            )
            
            security_result = self.universal_security_analyzer.compute_universal(
                simulation_results=simulation_results,
                protocol_features=protocol_features,
                security_params=security_params
            )
            
            return security_result
            
        except Exception as e:
            self.logger.error(f"通用安全分析失败: {e}")
            # 回退到传统分析
            return self._fallback_security_analysis(simulation_results)
    
    def estimate_protocol_entropy(self, protocol_graph: ProtocolGraph, measurement_data: Dict[str, Any]):
        """估计协议熵"""
        if not self.use_universal_framework:
            # 使用传统熵估计
            from security_evaluator.entropy_estimator import EntropyEstimator
            estimator = EntropyEstimator()
            return estimator.calculate_min_entropy(
                qber=measurement_data.get('error_rate', 0.1),
                protocol_type="BB84"
            )
        
        try:
            # 使用通用熵估计
            protocol_features = self.convert_protocol_to_features(protocol_graph)
            if protocol_features is None:
                raise ValueError("协议特征转换失败")
            
            security_params = UniversalSecurityParameters(
                epsilon_sec=self.config.get("EPSILON_SEC", 1e-10)
            )
            
            entropy_result = self.universal_entropy_estimator.estimate_universal_entropy(
                measurement_data=measurement_data,
                protocol_features=protocol_features,
                security_params=security_params
            )
            
            return entropy_result
            
        except Exception as e:
            self.logger.error(f"通用熵估计失败: {e}")
            # 回退到传统估计
            from security_evaluator.entropy_estimator import EntropyEstimator
            estimator = EntropyEstimator()
            return estimator.calculate_min_entropy(
                qber=measurement_data.get('error_rate', 0.1),
                protocol_type="BB84"
            )
    
    def evaluate_protocol(self) -> Dict[str, Any]:
        """评估当前协议（通用方法）"""
        try:
            # 1. 运行仿真
            simulation_results = self.run_universal_simulation()
            
            # 2. 安全性分析
            security_result = self.analyze_protocol_security(self.protocol_graph, simulation_results)
            
            # 3. 熵估计
            measurement_data = simulation_results.get('raw_statistics', {})
            entropy_result = self.estimate_protocol_entropy(self.protocol_graph, measurement_data)
            
            # 4. 性能指标
            performance_metrics = self._calculate_performance_metrics(simulation_results)
            
            # 5. 复杂度指标
            complexity_metrics = self._calculate_complexity_metrics(self.protocol_graph)
            
            evaluation = {
                'security_metrics': {
                    'final_key_rate': getattr(security_result, 'final_key_rate', 0.0),
                    'mutual_information': getattr(security_result, 'mutual_information', 0.0),
                    'holevo_information': getattr(security_result, 'holevo_information', 0.0)
                },
                'performance_metrics': performance_metrics,
                'complexity_metrics': complexity_metrics,
                'entropy_metrics': {
                    'entropy_value': getattr(entropy_result, 'value', 0.0),
                    'mutual_information': getattr(entropy_result, 'mutual_information', 0.0),
                    'holevo_information': getattr(entropy_result, 'holevo_information', 0.0)
                },
                'simulation_results': simulation_results
            }
            
            return evaluation
            
        except Exception as e:
            self.logger.error(f"协议评估失败: {e}")
            return self._fallback_evaluation()
    
    def evaluate_protocol_legacy(self) -> Dict[str, Any]:
        """传统协议评估方法（向后兼容）"""
        # 使用传统方法进行评估
        temp_use_universal = self.use_universal_framework
        self.use_universal_framework = False
        
        try:
            return self.evaluate_protocol()
        finally:
            self.use_universal_framework = temp_use_universal
    
    def _calculate_performance_metrics(self, simulation_results: Dict[str, Any]) -> Dict[str, float]:
        """计算性能指标"""
        channel_stats = simulation_results.get('channel_statistics', {})
        
        return {
            'transmission_efficiency': channel_stats.get('transmission_probability', 0.0),
            'error_rate': channel_stats.get('error_probability', 0.0),
            'detection_efficiency': channel_stats.get('detection_efficiency', 0.0),
            'total_pulses': channel_stats.get('total_pulses', 0)
        }
    
    def _calculate_complexity_metrics(self, protocol_graph: ProtocolGraph) -> Dict[str, int]:
        """计算协议复杂度指标"""
        return {
            'total_nodes': protocol_graph.get_node_count(),
            'total_edges': protocol_graph.get_edge_count(),
            'qsp_nodes': len(protocol_graph.get_nodes_by_type(NodeType.QSP)),
            'qc_nodes': len(protocol_graph.get_nodes_by_type(NodeType.QC)),
            'qm_nodes': len(protocol_graph.get_nodes_by_type(NodeType.QM)),
            'bsm_nodes': len(protocol_graph.get_nodes_by_type(NodeType.BSM))
        }
    
    def _fallback_security_analysis(self, simulation_results: Dict[str, Any]):
        """回退安全分析"""
        from security_evaluator.key_rate_calculator import KeyRateCalculator
        calculator = KeyRateCalculator()
        
        compute_params = {
            "qber": simulation_results.get('qber', 0.1),
            "gain": simulation_results.get('gain', 0.5),
            "n_pulses": self.config.get("DEFAULT_NUM_PULSES", 100000),
            "protocol_type": ProtocolType.BB84
        }
        
        return calculator.compute(**compute_params)
    
    def _fallback_evaluation(self) -> Dict[str, Any]:
        """回退评估方法"""
        return {
            'security_metrics': {'final_key_rate': 0.0, 'mutual_information': 0.0, 'holevo_information': 0.0},
            'performance_metrics': {'transmission_efficiency': 0.0, 'error_rate': 0.1, 'detection_efficiency': 0.0, 'total_pulses': 0},
            'complexity_metrics': {'total_nodes': 0, 'total_edges': 0, 'qsp_nodes': 0, 'qc_nodes': 0, 'qm_nodes': 0, 'bsm_nodes': 0},
            'entropy_metrics': {'entropy_value': 0.0, 'mutual_information': 0.0, 'holevo_information': 0.0},
            'simulation_results': {},
            'error': 'evaluation_failed'
        }

    def _apply_action(self, action: Dict[str, Any]) -> Tuple[bool, bool]:
        """
        根据动作字典修改协议图。
        返回: (is_valid, has_changed)
        """
        action_type = action["action_type"]
        graph = self.protocol_graph
        graph_before_dict = graph.to_dict() # 记录修改前的图状态
        has_changed = False

        if action_type == 0: # 增加节点
            node_type_enum = list(NodeType)[action["node_type_to_add"]]
            # 不再手动生成ID，让ProtocolGraph自动处理
            new_node_id = graph.add_node(node_type=node_type_enum)
            print(f"执行动作: 增加节点 {new_node_id} (类型: {node_type_enum.name})")

        elif action_type == 1: # 删除随机节点
            if graph.get_node_count() > 3: # 保护基础节点不被删除
                # 筛选出所有非QSP、QM、BSM的节点作为可删除候选
                nodes_to_consider = [
                    n for n, data in graph.graph.nodes(data=True)
                    if data.get('node_type') not in {NodeType.QSP, NodeType.QM, NodeType.BSM}
                ]
                if nodes_to_consider:
                    node_to_remove = random.choice(nodes_to_consider)
                    graph.remove_node(node_to_remove)
                    print(f"执行动作: 删除节点 {node_to_remove}")
                else:
                    print("跳过动作: 没有可安全删除的非核心节点。")

        elif action_type == 2: # 增加随机边
            nodes = list(graph.graph.nodes)
            if len(nodes) >= 2:
                source, target = random.sample(nodes, 2)
                
                # 检查添加这条边是否会形成环路
                temp_graph = graph.graph.copy()
                temp_graph.add_edge(source, target)
                
                if not nx.is_directed_acyclic_graph(temp_graph):
                    print(f"跳过动作: 增加边 {source} -> {target} 会形成环路。")
                elif not graph.graph.has_edge(source, target):
                    graph.add_edge(source, target)
                    print(f"执行动作: 增加边 {source} -> {target}")

        elif action_type == 3: # 修改随机节点的参数
            nodes = list(graph.graph.nodes)
            if not nodes: return (True, False) # Or handle as an invalid state if preferred

            node_to_modify_id = random.choice(nodes)
            node_to_modify = graph.get_node(node_to_modify_id)
            
            param_idx = action["param_to_modify"]
            param_value = action["param_value"][0]
            action_executed = False
            
            if param_idx == 0 and node_to_modify.node_type == NodeType.QC:
                node_to_modify.set_param('loss', param_value)
                print(f"执行动作: 修改节点 {node_to_modify_id} 的 loss 为 {param_value:.4f}")
                action_executed = True
            elif param_idx == 1 and node_to_modify.node_type == NodeType.QC:
                node_to_modify.set_param('error_rate', param_value / 10) # 假设错误率更小
                print(f"执行动作: 修改节点 {node_to_modify_id} 的 error_rate 为 {param_value/10:.4f}")
                action_executed = True
            elif param_idx == 2 and node_to_modify.node_type == NodeType.QM:
                node_to_modify.set_param('efficiency', param_value)
                print(f"执行动作: 修改节点 {node_to_modify_id} 的 efficiency 为 {param_value:.4f}")
                action_executed = True
            elif param_idx == 3 and node_to_modify.node_type == NodeType.QSP:
                node_to_modify.set_param('intensity', param_value)
                print(f"执行动作: 修改节点 {node_to_modify_id} 的 intensity 为 {param_value:.4f}")
                action_executed = True
            elif param_idx == 4 and node_to_modify.node_type in [NodeType.QC, NodeType.QM]:
                node_to_modify.set_param('noise_level', param_value)
                print(f"执行动作: 修改节点 {node_to_modify_id} 的 noise_level 为 {param_value:.4f}")
                action_executed = True
            
            if not action_executed:
                print("跳过动作: 尝试执行不符合物理的参数修改，协议未改变。")

        elif action_type == 4: # 重组协议结构
            # 随机重新连接一些节点，保持图的连通性
            nodes = list(graph.graph.nodes)
            if len(nodes) >= 3:
                # 随机选择两个节点，尝试重新连接
                node1, node2 = random.sample(nodes, 2)
                
                # 移除现有连接（如果存在）
                if graph.graph.has_edge(node1, node2):
                    graph.graph.remove_edge(node1, node2)
                    print(f"执行动作: 移除连接 {node1} -> {node2}")
                
                # 尝试添加反向连接
                if not graph.graph.has_edge(node2, node1):
                    # 检查是否会形成环路
                    temp_graph = graph.graph.copy()
                    temp_graph.add_edge(node2, node1)
                    
                    if nx.is_directed_acyclic_graph(temp_graph):
                        graph.add_edge(node2, node1)
                        print(f"执行动作: 重组连接 {node2} -> {node1}")
                    else:
                        print("跳过动作: 重组连接会形成环路")

        elif action_type == 5: # 优化协议参数
            # 批量优化多个节点的参数
            nodes = list(graph.graph.nodes)
            if nodes:
                # 随机选择1-3个节点进行参数优化
                num_nodes_to_optimize = random.randint(1, min(3, len(nodes)))
                nodes_to_optimize = random.sample(nodes, num_nodes_to_optimize)
                
                for node_id in nodes_to_optimize:
                    node = graph.get_node(node_id)
                    param_value = action["param_value"][0]
                    
                    if node.node_type == NodeType.QC:
                        # 优化信道参数
                        node.set_param('loss', max(0.0, node.params.get('loss', 0.1) - param_value * 0.1))
                        node.set_param('error_rate', max(0.0, node.params.get('error_rate', 0.05) - param_value * 0.05))
                    elif node.node_type == NodeType.QM:
                        # 优化测量参数
                        node.set_param('efficiency', min(1.0, node.params.get('efficiency', 0.8) + param_value * 0.2))
                    elif node.node_type == NodeType.QSP:
                        # 优化态制备参数
                        node.set_param('intensity', max(0.0, node.params.get('intensity', 0.1) + param_value * 0.1))
                
                print(f"执行动作: 优化了 {num_nodes_to_optimize} 个节点的参数")
        
        graph_after_dict = graph.to_dict()
        has_changed = (graph_before_dict != graph_after_dict)

        # 检查协议有效性
        return self._is_protocol_valid(), has_changed

    def _is_protocol_valid(self) -> bool:
        """检查当前协议图是否至少包含一个源和一个测量节点。"""
        has_source = len(self.protocol_graph.get_nodes_by_type(NodeType.QSP)) > 0
        has_measurement = (len(self.protocol_graph.get_nodes_by_type(NodeType.QM)) > 0 or
                           len(self.protocol_graph.get_nodes_by_type(NodeType.BSM)) > 0)
        
        if not has_source or not has_measurement:
            self.logger.warning("协议变得无效：缺少源节点或测量节点。")
            return False
        return True

    def step(self, action: Dict[str, Any]) -> Tuple[Any, float, bool, bool, Dict]:
        """
        执行一个时间步。
        1. AI Agent执行一个动作 (修改协议图)
        2. 环境运行仿真和评估
        3. 计算奖励
        4. 返回新的状态和奖励
        """
        # 1. 根据动作修改协议图，并检查其有效性和是否发生改变
        is_valid, has_changed = self._apply_action(action)

        if not is_valid:
            # 如果协议无效，立即结束并给予巨大负惩罚
            next_state = self.observation_space.sample() # 状态无所谓了
            reward = self.config.get("INVALID_PROTOCOL_PENALTY", -100.0)
            done = True
            # 更新缓存，即使是失败状态
            self.last_observation = next_state
            self.last_reward = reward
            self.last_info = {'error': 'Invalid protocol state'}
            return next_state, reward, done, False, self.last_info

        # --- 性能优化 ---
        if not has_changed:
            # 如果协议没有改变，直接返回上一步的缓存结果，跳过仿真
            self.logger.info("协议未改变，跳过仿真并使用缓存结果。")
            return self.last_observation, self.last_reward, False, False, self.last_info

        # 2. 运行通用仿真和评估
        sim_results = self.run_universal_simulation()
        
        # 使用通用安全分析
        security_results = self.analyze_protocol_security(self.protocol_graph, sim_results)

        # 3. 计算奖励
        complexity = self.protocol_graph.get_node_count()
        reward = calculate_reward(security_results, complexity)
        
        # 4. 获取新状态 (协议图的向量化表示)
        # next_state = self._get_observation()
        next_state = self.observation_space.sample() # 简化

        # 决定是否结束 (例如，达到最大节点数或密钥率稳定)
        done = False 

        # 将安全评估结果放入info字典返回
        info = {'security_results': security_results}
        
        # 更新缓存
        self.last_observation = next_state
        self.last_reward = reward
        self.last_info = info

        return next_state, reward, done, False, info

    def reset(self, seed=None, options=None):
        """
        重置环境。
        """
        super().reset(seed=seed)
        self.protocol_graph = self._create_base_bb84_graph()
        
        # 重新初始化仿真器和分析器
        self._init_simulators_and_analyzers()
        
        # 重置缓存
        self.last_observation = None
        self.last_reward = 0.0
        self.last_info = {}
        
        # obs = self._get_observation()
        obs = self.observation_space.sample() # 简化
        self.last_observation = obs # 初始化缓存
        return obs, {}

    def render(self, mode='human'):
        """
        渲染环境状态（例如，可视化协议图）。
        """
        self.protocol_graph.visualize() 