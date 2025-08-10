"""
诱骗态BB84协议仿真示例
"""
import sys
import os
import argparse
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party, Intensity
from simulator import QuantumSimulator
from security_evaluator import KeyRateCalculator, ProtocolType
from utils.logger import setup_logger
from utils.visualization import plot_multi_curve_comparison
from config import settings
from config.qkd_protocols import DECOY_BB84_PARAMS

def build_decoy_protocol(config: dict) -> ProtocolGraph:
    """
    根据配置文件构建诱骗态BB84协议图。
    注意：此处的图结构与标准BB84相同，区别在于QSP节点的参数。
    """
    graph = ProtocolGraph(name="Decoy_BB84_from_Config")
    
    # 在QSP节点参数中，我们传入了完整的强度配置
    qsp_params = config['qsp'].copy()
    qsp_params['intensities'] = config['intensities']
    
    graph.add_node(node_type=NodeType.QSP, params=qsp_params, party=Party.ALICE, node_id="Alice_QSP")
    graph.add_node(node_type=NodeType.QC, params=config['qc'], node_id="QuantumChannel")
    graph.add_node(node_type=NodeType.QM, params=config['qm'], party=Party.BOB, node_id="Bob_QM")
    
    graph.add_edge("Alice_QSP", "QuantumChannel")
    graph.add_edge("QuantumChannel", "Bob_QM")
    
    return graph

def main():
    """
    诱骗态BB84协议仿真和评估的主函数。
    """
    logger = setup_logger(__name__, log_level=settings.LOG_LEVEL)
    logger.info("--- 开始执行诱骗态BB84协议示例 ---")

    # 1. 构建协议图 (包含强度信息)
    logger.info("步骤 1: 从配置文件构建协议图...")
    protocol_graph = build_decoy_protocol(DECOY_BB84_PARAMS)
    logger.info(f"协议图 '{protocol_graph.name}' 构建完成。")

    # 2. 运行仿真器
    logger.info("步骤 2: 使用真实物理仿真器进行多强度仿真...")
    simulator = QuantumSimulator(protocol_graph)
    # 仿真器内部会识别出这是诱骗态协议，并按强度分别仿真
    sim_results_by_intensity = simulator.run()
    
    logger.info("多强度仿真完成。结果如下:")
    for name, results in sim_results_by_intensity.items():
        logger.info(f"  - 强度 '{name}': QBER={results['qber']:.4f}, Gain={results['gain']:.4f}")

    # 3. 估算最终密钥率
    logger.info("步骤 3: 使用诱骗态结果估算安全密钥率...")
    security_config = DECOY_BB84_PARAMS.get('security', {})
    
    # 在GLLP分析中，我们需要所有强度态的结果来估算单光子参数
    # 我们的简化模型直接使用信号态的结果作为近似
    signal_results = sim_results_by_intensity.get('signal', {})
    
    key_rate_calculator = KeyRateCalculator(
        qber=signal_results.get('qber', 0),
        gain=signal_results.get('gain', 0),
        protocol_type=ProtocolType.DECOY_BB84,
        params=security_config.get('params', {})
    )
    secure_key_rate = key_rate_calculator.calculate_key_rate()
    logger.info(f"估算的安全密钥率: {secure_key_rate:.6f} bits/pulse")

    logger.info("--- 诱骗态BB84协议示例执行完毕 ---")

    return {
        "results_by_intensity": sim_results_by_intensity,
        "secure_key_rate": secure_key_rate
    }


if __name__ == '__main__':
    main() 