"""
主量子仿真器模块

整合了所有量子仿真子模块，提供完整的QKD协议仿真功能：
- 量子态准备仿真
- 量子信道建模
- 量子测量仿真
- 性能指标计算
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import time
import warnings

from .state_preparation import StatePreparation
from .channel_model import ChannelModel
from .measurement import Measurement
from .performance_metrics import PerformanceMetrics

try:
    from qcgf_dsl.protocol_graph import ProtocolGraph, Node
    from qcgf_dsl.node_types import NodeType, Party
    from qcgf_dsl.protocol_graph import EdgeType
    QCGF_AVAILABLE = True
except ImportError:
    QCGF_AVAILABLE = False
    warnings.warn("QCGF DSL not available, using simplified interface")


class QuantumSimulator:
    """
    主量子仿真器
    
    整合了所有量子仿真子模块，提供完整的QKD协议仿真功能。
    支持基于ProtocolGraph的协议仿真和性能分析。
    """
    
    def __init__(self, 
                 max_photon_number: int = 10,
                 pulse_rate: float = 1e9,
                 num_measurements: int = 1000):
        """
        初始化量子仿真器
        
        Args:
            max_photon_number: 最大光子数（用于截断）
            pulse_rate: 脉冲率（Hz）
            num_measurements: 每次仿真的测量次数
        """
        self.max_photon_number = max_photon_number
        self.pulse_rate = pulse_rate
        self.num_measurements = num_measurements
        
        # 初始化子模块
        self.state_preparation = StatePreparation(max_photon_number)
        self.channel_model = ChannelModel(max_photon_number)
        self.measurement = Measurement(max_photon_number)
        self.performance_metrics = PerformanceMetrics()
        
        # 仿真结果存储
        self.simulation_results = {}
        self.performance_analysis = {}
    
    def simulate_protocol_graph(self, 
                               protocol_graph: ProtocolGraph,
                               simulation_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        仿真完整的协议图
        
        Args:
            protocol_graph: 协议图
            simulation_params: 仿真参数字典
            
        Returns:
            仿真结果
        """
        if not QCGF_AVAILABLE:
            raise ImportError("QCGF DSL模块不可用")
        
        if not protocol_graph.is_dag():
            raise ValueError("协议图必须是有向无环图（DAG）")
        
        # 获取拓扑排序
        topo_order = protocol_graph.get_topological_order()
        
        # 初始化仿真状态
        simulation_state = {}
        measurement_results = []
        alice_bits = []
        bob_bits = []
        
        # 按拓扑顺序仿真每个节点
        for node_id in topo_order:
            node = protocol_graph.get_node(node_id)
            if node is None:
                continue
            
            # 根据节点类型进行仿真
            if node.node_type == NodeType.QSP:
                # 量子态准备
                state_info = self.state_preparation.simulate_state_preparation(node.params)
                simulation_state[node_id] = state_info
                
            elif node.node_type == NodeType.QC:
                # 量子信道传输
                # 找到输入节点
                input_nodes = protocol_graph.get_neighbors(node_id, "in")
                if input_nodes:
                    input_state = simulation_state.get(input_nodes[0], {})
                    output_state = self.channel_model.simulate_channel_transmission(
                        input_state, node.params
                    )
                    simulation_state[node_id] = output_state
                
            elif node.node_type == NodeType.QM:
                # 量子测量
                # 找到输入节点
                input_nodes = protocol_graph.get_neighbors(node_id, "in")
                if input_nodes:
                    input_state = simulation_state.get(input_nodes[0], {})
                    
                    # 进行多次测量
                    node_measurements = []
                    for _ in range(self.num_measurements):
                        measurement_result = self.measurement.simulate_measurement(
                            input_state, node.params
                        )
                        node_measurements.append(measurement_result)
                    
                    # 统计测量结果
                    measurement_stats = self.measurement.calculate_measurement_statistics(
                        node_measurements
                    )
                    
                    simulation_state[node_id] = {
                        "input_state": input_state,
                        "measurement_results": node_measurements,
                        "measurement_stats": measurement_stats
                    }
                    
                    # 记录比特（简化处理）
                    if node.party == Party.ALICE:
                        # Alice的比特（基于态准备）
                        for _ in range(self.num_measurements):
                            alice_bits.append(np.random.randint(0, 2))
                    elif node.party == Party.BOB:
                        # Bob的比特（基于测量结果）
                        for measurement in node_measurements:
                            outcome = measurement.get("outcome", "no_detection")
                            if outcome == "1" or outcome == "+":
                                bob_bits.append(1)
                            elif outcome == "0" or outcome == "-":
                                bob_bits.append(0)
                            else:
                                bob_bits.append(np.random.randint(0, 2))
        
        # 计算性能指标
        total_pulses = self.num_measurements
        detected_pulses = len([b for b in bob_bits if b is not None])
        
        # 确保比特序列长度一致
        min_length = min(len(alice_bits), len(bob_bits))
        alice_bits = alice_bits[:min_length]
        bob_bits = bob_bits[:min_length]
        
        # 存储仿真结果
        self.simulation_results = {
            "protocol_graph": protocol_graph,
            "simulation_state": simulation_state,
            "total_pulses": total_pulses,
            "detected_pulses": detected_pulses,
            "alice_bits": alice_bits,
            "bob_bits": bob_bits,
            "pulse_rate": self.pulse_rate,
            "photon_distribution": self._get_photon_distribution(simulation_state)
        }
        
        # 性能分析
        self.performance_analysis = self.performance_metrics.analyze_performance(
            self.simulation_results
        )
        
        return {
            "simulation_results": self.simulation_results,
            "performance_analysis": self.performance_analysis
        }
    
    def _get_photon_distribution(self, simulation_state: Dict[str, Any]) -> Dict[int, float]:
        """
        获取综合光子数分布
        
        Args:
            simulation_state: 仿真状态
            
        Returns:
            光子数分布
        """
        # 简化处理：返回平均分布
        return {0: 0.1, 1: 0.8, 2: 0.1}
    
    def simulate_bb84_protocol(self, 
                              alice_mean_photon: float = 0.1,
                              channel_loss: float = 0.1,
                              detector_efficiency: float = 0.8,
                              dark_count_rate: float = 1e-6) -> Dict[str, Any]:
        """
        仿真BB84协议
        
        Args:
            alice_mean_photon: Alice的平均光子数
            channel_loss: 信道损耗
            detector_efficiency: 探测器效率
            dark_count_rate: 暗计数率
            
        Returns:
            BB84协议仿真结果
        """
        # 创建BB84协议图
        if not QCGF_AVAILABLE:
            raise ImportError("QCGF DSL模块不可用")
        
        bb84_graph = ProtocolGraph("BB84协议")
        
        # Alice的量子态准备
        alice_qsp = bb84_graph.add_node(
            node_type=NodeType.QSP,
            params={"state": f"wcp:{alice_mean_photon}", "fidelity": 0.99},
            party=Party.ALICE
        )
        
        # 量子信道
        qc = bb84_graph.add_node(
            node_type=NodeType.QC,
            params={"loss": channel_loss, "dark_count_rate": dark_count_rate}
        )
        
        # Bob的测量
        bob_qm = bb84_graph.add_node(
            node_type=NodeType.QM,
            params={"basis": "Z", "efficiency": detector_efficiency},
            party=Party.BOB
        )
        
        # 添加边
        bb84_graph.add_edge(alice_qsp, qc, EdgeType.QUANTUM)
        bb84_graph.add_edge(qc, bob_qm, EdgeType.QUANTUM)
        
        # 仿真协议
        return self.simulate_protocol_graph(bb84_graph)
    
    def simulate_mdi_qkd_protocol(self, 
                                 alice_mean_photon: float = 0.1,
                                 bob_mean_photon: float = 0.1,
                                 channel_loss: float = 0.1,
                                 charlie_efficiency: float = 0.8) -> Dict[str, Any]:
        """
        仿真MDI-QKD协议
        
        Args:
            alice_mean_photon: Alice的平均光子数
            bob_mean_photon: Bob的平均光子数
            channel_loss: 信道损耗
            charlie_efficiency: Charlie的探测效率
            
        Returns:
            MDI-QKD协议仿真结果
        """
        if not QCGF_AVAILABLE:
            raise ImportError("QCGF DSL模块不可用")
        
        mdi_graph = ProtocolGraph("MDI-QKD协议")
        
        # Alice的量子态准备
        alice_qsp = mdi_graph.add_node(
            node_type=NodeType.QSP,
            params={"state": f"wcp:{alice_mean_photon}"},
            party=Party.ALICE
        )
        
        # Bob的量子态准备
        bob_qsp = mdi_graph.add_node(
            node_type=NodeType.QSP,
            params={"state": f"wcp:{bob_mean_photon}"},
            party=Party.BOB
        )
        
        # 量子信道
        qc1 = mdi_graph.add_node(
            node_type=NodeType.QC,
            params={"loss": channel_loss}
        )
        
        qc2 = mdi_graph.add_node(
            node_type=NodeType.QC,
            params={"loss": channel_loss}
        )
        
        # Charlie的测量
        charlie_qm = mdi_graph.add_node(
            node_type=NodeType.QM,
            params={"basis": "Z", "efficiency": charlie_efficiency},
            party=Party.CHARLIE
        )
        
        # 添加边
        mdi_graph.add_edge(alice_qsp, qc1, EdgeType.QUANTUM)
        mdi_graph.add_edge(bob_qsp, qc2, EdgeType.QUANTUM)
        mdi_graph.add_edge(qc1, charlie_qm, EdgeType.QUANTUM)
        mdi_graph.add_edge(qc2, charlie_qm, EdgeType.QUANTUM)
        
        # 仿真协议
        return self.simulate_protocol_graph(mdi_graph)
    
    def get_performance_report(self) -> str:
        """
        获取性能报告
        
        Returns:
            格式化的性能报告
        """
        if not self.performance_analysis:
            return "未进行仿真，无法生成性能报告"
        
        return self.performance_metrics.generate_performance_report(
            self.performance_analysis
        )
    
    def compare_protocols(self, 
                         protocol_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        比较多个协议的性能
        
        Args:
            protocol_results: 协议结果列表
            
        Returns:
            比较结果
        """
        comparison = {
            "protocols": [],
            "metrics": {}
        }
        
        for i, result in enumerate(protocol_results):
            protocol_name = result.get("protocol_name", f"Protocol_{i}")
            performance = result.get("performance_analysis", {})
            
            comparison["protocols"].append(protocol_name)
            
            # 收集各项指标
            for metric, value in performance.items():
                if metric not in comparison["metrics"]:
                    comparison["metrics"][metric] = []
                comparison["metrics"][metric].append(value)
        
        return comparison
    
    def export_results(self, 
                      filename: str,
                      format: str = "json") -> None:
        """
        导出仿真结果
        
        Args:
            filename: 文件名
            format: 导出格式 ("json", "csv")
        """
        import json
        import csv
        
        if format == "json":
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "simulation_results": self.simulation_results,
                    "performance_analysis": self.performance_analysis
                }, f, indent=2, ensure_ascii=False)
        
        elif format == "csv":
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                for metric, value in self.performance_analysis.items():
                    writer.writerow([metric, value])
        
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def get_simulation_statistics(self) -> Dict[str, Any]:
        """
        获取仿真统计信息
        
        Returns:
            仿真统计信息
        """
        if not self.simulation_results:
            return {"status": "未进行仿真"}
        
        protocol_graph = self.simulation_results.get("protocol_graph")
        protocol_name = protocol_graph.name if protocol_graph else "Unknown"
        
        return {
            "status": "仿真完成",
            "total_pulses": self.simulation_results.get("total_pulses", 0),
            "detected_pulses": self.simulation_results.get("detected_pulses", 0),
            "raw_key_length": len(self.simulation_results.get("alice_bits", [])),
            "simulation_time": time.time() - getattr(self, '_start_time', time.time()),
            "protocol_name": protocol_name
        } 