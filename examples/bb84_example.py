"""
BB84 协议仿真示例
"""
import sys
import os
import argparse

# 将项目根目录添加到Python路径，以便导入模块
# 这对于从命令行直接运行脚本，或者被其他模块（如测试）导入时，都能找到正确的模块路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入系统核心模块
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party
from simulator import QuantumSimulator
from security_evaluator import KeyRateCalculator, ProtocolType
from utils.logger import setup_logger
from qcgf_dsl.visualizer import visualize_protocol

# 从配置文件导入参数
from config import settings
from config.qkd_protocols import BB84_PARAMS

def build_bb84_protocol_from_config(config: dict) -> ProtocolGraph:
    """
    根据配置文件构建BB84协议图。
    """
    graph = ProtocolGraph(name="BB84_from_Config")
    
    graph.add_node(node_type=NodeType.QSP, params=config['qsp'], party=Party.ALICE, node_id="Alice_QSP")
    graph.add_node(node_type=NodeType.QC, params=config['qc'], node_id="QuantumChannel")
    graph.add_node(node_type=NodeType.QM, params=config['qm'], party=Party.BOB, node_id="Bob_QM")
    
    graph.add_edge("Alice_QSP", "QuantumChannel")
    graph.add_edge("QuantumChannel", "Bob_QM")
    
    return graph

def main():
    """
    BB84协议仿真和评估的主函数。
    """
    # 1. 设置日志记录器
    logger = setup_logger(__name__, log_level=settings.LOG_LEVEL)
    logger.info("--- 开始执行 BB84 协议示例 ---")

    # 2. 构建协议图
    logger.info("步骤 1: 从配置文件构建协议图...")
    protocol_graph = build_bb84_protocol_from_config(BB84_PARAMS)
    logger.info(f"协议图 '{protocol_graph.name}' 构建完成。")

    # 3. 运行真实仿真器
    logger.info("步骤 2: 使用真实物理仿真器进行仿真...")
    simulator = QuantumSimulator(protocol_graph)
    sim_results = simulator.run()
    qber = sim_results.get('qber', 0)
    gain = sim_results.get('gain', 0)
    logger.info(f"仿真完成。 性能指标: QBER={qber:.4f}, Gain={gain:.4f}")

    # 4. 估算最终密钥率
    logger.info("步骤 3: 估算安全密钥率...")
    security_config = BB84_PARAMS.get('security', {})
    key_rate_calculator = KeyRateCalculator(
        qber=qber,
        gain=gain,
        protocol_type=ProtocolType.BB84,
        params=security_config.get('params', {})
    )
    secure_key_rate = key_rate_calculator.calculate_key_rate()
    logger.info(f"估算的安全密钥率: {secure_key_rate:.6f} bits/pulse")

    # 5. 可选：可视化协议图
    parser = argparse.ArgumentParser()
    parser.add_argument('--visualize', action='store_true', help='是否可视化协议图')
    args = parser.parse_args()

    if args.visualize:
        logger.info("步骤 4: 可视化协议图...")
        vis_path = f"examples/bb84_protocol_structure.png"
        visualize_protocol(protocol_graph, save_path=vis_path)
        logger.info(f"协议图已保存至: {vis_path}")

    logger.info("--- BB84 协议示例执行完毕 ---")

    # 返回结果，便于测试脚本调用和验证
    return {
        "qber": qber,
        "gain": gain,
        "secure_key_rate": secure_key_rate
    }


if __name__ == '__main__':
    main() 