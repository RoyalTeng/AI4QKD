"""
MDI-QKD 协议仿真示例
"""
import sys
import os
import argparse

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party
from simulator import QuantumSimulator
from security_evaluator import KeyRateCalculator, ProtocolType
from utils.logger import setup_logger
from qcgf_dsl.visualizer import visualize_protocol
from config import settings
from config.qkd_protocols import MDI_QKD_PARAMS

def build_mdi_qkd_protocol_from_config(config: dict) -> ProtocolGraph:
    """
    根据配置文件构建MDI-QKD协议图。
    """
    graph = ProtocolGraph(name="MDI-QKD_from_Config")
    
    # Alice, Bob, 和 Charlie (Bell State Measurement - BSM)
    graph.add_node(node_type=NodeType.QSP, params=config['alice_qsp'], party=Party.ALICE, node_id="Alice_QSP")
    graph.add_node(node_type=NodeType.QC, params=config['alice_qc'], node_id="Alice_Channel")
    
    graph.add_node(node_type=NodeType.QSP, params=config['bob_qsp'], party=Party.BOB, node_id="Bob_QSP")
    graph.add_node(node_type=NodeType.QC, params=config['bob_qc'], node_id="Bob_Channel")

    # 在MDI协议中，第三方Charlie执行BSM
    graph.add_node(node_type=NodeType.BSM, params=config['charlie_bsm'], party=Party.CHARLIE, node_id="Charlie_BSM")
    
    # 定义连接
    graph.add_edge("Alice_QSP", "Alice_Channel")
    graph.add_edge("Alice_Channel", "Charlie_BSM")
    
    graph.add_edge("Bob_QSP", "Bob_Channel")
    graph.add_edge("Bob_Channel", "Charlie_BSM")
    
    return graph

def main():
    """
    MDI-QKD协议仿真和评估的主函数。
    """
    logger = setup_logger(__name__, log_level=settings.LOG_LEVEL)
    logger.info("--- 开始执行 MDI-QKD 协议示例 ---")

    # 1. 构建协议图
    logger.info("步骤 1: 从配置文件构建MDI-QKD协议图...")
    protocol_graph = build_mdi_qkd_protocol_from_config(MDI_QKD_PARAMS)
    logger.info(f"协议图 '{protocol_graph.name}' 构建完成。")

    # 2. 运行真实仿真器
    logger.info("步骤 2: 使用真实物理仿真器进行仿真...")
    simulator = QuantumSimulator(protocol_graph)
    sim_results = simulator.run()
    qber = sim_results.get('qber', 0)
    gain = sim_results.get('gain', 0)
    logger.info(f"仿真完成。 性能指标: QBER={qber:.4f}, Gain={gain:.4f}")

    # 3. 估算最终密钥率
    logger.info("步骤 3: 估算安全密钥率...")
    security_config = MDI_QKD_PARAMS.get('security', {})
    key_rate_calculator = KeyRateCalculator(
        qber=qber,
        gain=gain,
        protocol_type=ProtocolType.MDI_QKD,
        params=security_config.get('params', {})
    )
    secure_key_rate = key_rate_calculator.calculate_key_rate()
    logger.info(f"估算的安全密钥率: {secure_key_rate:.6f} bits/pulse")

    # 4. 可选：可视化协议图
    parser = argparse.ArgumentParser()
    parser.add_argument('--visualize', action='store_true', help='是否可视化协议图')
    # 使用 parse_known_args 来避免与其他脚本的参数冲突
    args, _ = parser.parse_known_args()

    if args.visualize:
        logger.info("步骤 4: 可视化协议图...")
        vis_path = f"examples/mdi_qkd_protocol_structure.png"
        visualize_protocol(protocol_graph, save_path=vis_path)
        logger.info(f"协议图已保存至: {vis_path}")

    logger.info("--- MDI-QKD 协议示例执行完毕 ---")

    return {
        "qber": qber,
        "gain": gain,
        "secure_key_rate": secure_key_rate
    }


if __name__ == '__main__':
    main() 