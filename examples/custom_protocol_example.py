"""
自定义协议与AI优化展示示例
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party
from simulator import QuantumSimulator
from security_evaluator import KeyRateCalculator, ProtocolType
from ai_agent import HybridAgent
from utils.logger import setup_logger
from utils.visualization import plot_performance_comparison
from qcgf_dsl.visualizer import visualize_protocol
from config import settings

def build_custom_protocol() -> ProtocolGraph:
    """
    构建一个非对称的、包含经典逻辑处理的自定义协议图。
    """
    graph = ProtocolGraph(name="Asymmetric_CLO_Protocol")
    
    # 节点定义
    graph.add_node(node_type=NodeType.QSP, params={'num_states': 100000}, party=Party.ALICE, node_id="Alice_Source")
    graph.add_node(node_type=NodeType.QC, params={'loss': 0.25, 'error_rate': 0.03}, node_id="Channel_1")
    # 增加一个经典逻辑节点，模拟中间处理或有意的协议操作
    graph.add_node(node_type=NodeType.CLO, params={'operation': 'Pauli_X_Correction'}, party=Party.ALICE, node_id="Alice_Correction")
    graph.add_node(node_type=NodeType.QC, params={'loss': 0.25, 'error_rate': 0.03}, node_id="Channel_2")
    graph.add_node(node_type=NodeType.QM, params={}, party=Party.BOB, node_id="Bob_Detector")

    # 边定义
    graph.add_edge("Alice_Source", "Channel_1")
    graph.add_edge("Channel_1", "Alice_Correction") # 假设量子态被测量后，经典信息用于校正
    graph.add_edge("Alice_Correction", "Channel_2")
    graph.add_edge("Channel_2", "Bob_Detector")
    
    return graph

def evaluate_protocol(protocol: ProtocolGraph, logger) -> dict:
    """对给定的协议图进行仿真和评估。"""
    logger.info(f"--- 正在评估协议: '{protocol.name}' ---")
    
    simulator = QuantumSimulator(protocol)
    sim_results = simulator.run()
    qber = sim_results.get('qber', 0)
    gain = sim_results.get('gain', 0)
    logger.info(f"仿真完成: QBER={qber:.4f}, Gain={gain:.4f}")

    key_rate_calculator = KeyRateCalculator(
        qber=qber,
        gain=gain,
        protocol_type=ProtocolType.BB84 # 使用BB84作为基准模型进行评估
    )
    secure_key_rate = key_rate_calculator.calculate_key_rate()
    logger.info(f"估算的安全密钥率: {secure_key_rate:.6f} bits/pulse")
    
    return {"qber": qber, "gain": gain, "secure_key_rate": secure_key_rate}

def main():
    """主函数，执行自定义协议的评估、优化和对比流程。"""
    logger = setup_logger(__name__, log_level=settings.LOG_LEVEL)
    
    # 1. 构建并评估原始协议
    original_protocol = build_custom_protocol()
    logger.info(f"\n[阶段 1] 原始协议 '{original_protocol.name}' 构建完成。")
    original_metrics = evaluate_protocol(original_protocol, logger)

    # 2. 使用AI Agent进行优化
    logger.info(f"\n[阶段 2] AI智能体开始优化协议...")
    ai_agent = HybridAgent({}) # 使用默认配置
    optimized_protocol, suggestions = ai_agent.optimize(original_protocol)
    logger.info("AI优化完成。优化建议:")
    for s in suggestions:
        logger.info(f"  - {s}")

    # 3. 评估优化后的协议
    logger.info(f"\n[阶段 3] 评估优化后的协议 '{optimized_protocol.name}'...")
    optimized_metrics = evaluate_protocol(optimized_protocol, logger)
    
    # 4. 可视化对比
    parser = argparse.ArgumentParser()
    parser.add_argument('--visualize', action='store_true', help='是否进行可视化')
    args, _ = parser.parse_known_args()

    if args.visualize:
        logger.info("\n[阶段 4] 生成对比可视化图表...")
        # 对比性能指标
        plot_performance_comparison(
            original_metrics,
            optimized_metrics,
            title=f"协议 '{original_protocol.name}' 优化前后性能对比"
        )
        # 可视化原始协议图
        visualize_protocol(original_protocol, save_path="examples/custom_protocol_original.png")
        logger.info("原始协议图已保存。")
        # 可视化优化后协议图
        visualize_protocol(optimized_protocol, save_path="examples/custom_protocol_optimized.png")
        logger.info("优化后协议图已保存。")

if __name__ == '__main__':
    main() 