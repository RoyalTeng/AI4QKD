import logging
import pandas as pd
from z3 import sat
import matplotlib.pyplot as plt
from qcgf_dsl import ProtocolGraph, NodeType, EdgeType
from simulator import QuantumSimulator
from security_evaluator import KeyRateCalculator, ProtocolType, SecurityParameters
from formal_verification import ProtocolVerifier, SecurityProof, ModelChecker, TheoremProver
from ai_agent import HybridAgent
from utils.logger import setup_logger
from utils.visualization import plot_qber_gain_evolution # 假设有这个函数
from qcgf_dsl.visualizer import ProtocolVisualizer

def build_initial_protocol() -> ProtocolGraph:
    """Step 1: 构造一个简单的BB84协议图"""
    logging.info("构建初始协议图...")
    graph = ProtocolGraph(name="Simple_BB84")
    graph.add_node(node_type=NodeType.QSP, node_id="alice_qsp", params={"party": "Alice"})
    graph.add_node(node_type=NodeType.QC, node_id="quantum_channel")
    graph.add_node(node_type=NodeType.QM, node_id="bob_qm", params={"party": "Bob"})
    graph.add_node(node_type=NodeType.CC, node_id="classical_channel")
    graph.add_node(node_type=NodeType.CLO, node_id="alice_classical_logic", params={"party": "Alice"})
    
    graph.add_edge("alice_qsp", "quantum_channel", edge_type=EdgeType.QUANTUM)
    graph.add_edge("quantum_channel", "bob_qm", edge_type=EdgeType.QUANTUM)
    # 修正：经典信息流向一个新的处理节点，而不是回到起点
    graph.add_edge("bob_qm", "classical_channel", edge_type=EdgeType.CLASSICAL)
    graph.add_edge("classical_channel", "alice_classical_logic", edge_type=EdgeType.CLASSICAL)
    
    logging.info(f"初始协议图构建完成: {graph}")
    return graph

def run_simulation(graph: ProtocolGraph) -> dict:
    """Step 2: 调用仿真器进行仿真"""
    logging.info("开始协议仿真...")
    # 实际的simulator需要更复杂的配置和输入
    # 这里我们模拟一个仿真结果
    sim_result = {
        "qber": 0.03,
        "gain": 0.85,
        "n_pulses": 10**12
    }
    logging.info(f"仿真完成，结果: {sim_result}")
    return sim_result

def evaluate_security(sim_result: dict) -> dict:
    """Step 3: 调用安全性评估器计算密钥率"""
    logging.info("开始安全性评估...")
    calculator = KeyRateCalculator()
    key_rate_result = calculator.compute(
        qber=sim_result["qber"],
        gain=sim_result["gain"],
        n_pulses=sim_result["n_pulses"],
        protocol_type=ProtocolType.BB84
    )
    logging.info(f"密钥率计算完成: {key_rate_result.final_key_rate:.4e} bits/pulse")
    return {"key_rate": key_rate_result.final_key_rate}
    
def run_verification(graph: ProtocolGraph):
    """Step 4: 调用形式化验证模块"""
    logging.info("开始形式化验证...")
    verifier = ProtocolVerifier()
    report = verifier.verify(graph)
    assert report.is_valid, f"协议图结构验证失败: {report.errors}"
    logging.info("结构验证通过。")

    prover = TheoremProver()
    result = prover.prove_no_cloning()
    assert result != sat, "不可克隆定理证明失败！"
    logging.info("不可克隆定理证明通过。")

def optimize_protocol(graph: ProtocolGraph) -> ProtocolGraph:
    """Step 5: 调用AI智能体进行优化"""
    logging.info("开始AI辅助协议优化...")
    # AI Agent的初始化和配置比较复杂，这里我们模拟一个优化过程
    # 假设AI增加了一个纠错节点和一个隐私放大节点
    optimized_graph = graph
    optimized_graph.name = "Optimized_BB84"
    optimized_graph.add_node(node_type=NodeType.CLO, node_id="error_correction", params={"party": "Alice"})
    optimized_graph.add_node(node_type=NodeType.CLO, node_id="privacy_amplification", params={"party": "Bob"})
    logging.info(f"协议优化完成: {optimized_graph}")
    return optimized_graph

def main():
    """集成测试主流程"""
    setup_logger(__name__)
    
    # --- 原始协议流程 ---
    logging.info("\n--- 开始处理原始协议 ---")
    protocol_original = build_initial_protocol()
    sim_result_original = run_simulation(protocol_original)
    security_result_original = evaluate_security(sim_result_original)
    run_verification(protocol_original)

    # --- AI优化后流程 ---
    logging.info("\n--- 开始处理优化后协议 ---")
    protocol_optimized = optimize_protocol(protocol_original)
    # 假设优化后性能提升
    sim_result_optimized = {"qber": 0.025, "gain": 0.88, "n_pulses": 10**12}
    security_result_optimized = evaluate_security(sim_result_optimized)
    run_verification(protocol_optimized)

    # --- 结果对比与可视化 ---
    logging.info("\n--- 结果对比与可视化 ---")
    visualizer = ProtocolVisualizer()
    
    # 修正：创建一个包含两个子图的Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, 12))
    fig.suptitle("Protocol Comparison", fontsize=20, y=0.95)

    print("绘制原始协议图...")
    visualizer.visualize(protocol_original, ax=ax1)

    print("绘制优化后协议图...")
    visualizer.visualize(protocol_optimized, ax=ax2)
    
    # 只在最后统一显示整个Figure
    plt.show()
    
    # 打印性能对比表格
    summary_data = {
        "Protocol": ["Original", "Optimized"],
        "QBER": [sim_result_original["qber"], sim_result_optimized["qber"]],
        "Gain": [sim_result_original["gain"], sim_result_optimized["gain"]],
        "Key Rate (bits/pulse)": [security_result_original["key_rate"], security_result_optimized["key_rate"]]
    }
    summary_df = pd.DataFrame(summary_data)
    print("\n--- 性能对比总结 ---")
    print(summary_df.to_string(index=False))

if __name__ == '__main__':
    main()
