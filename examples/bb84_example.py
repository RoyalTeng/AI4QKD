"""
BB84协议示例 - 简化版
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from qcgf_dsl import ProtocolGraph
from simulator import QuantumSimulator
from ai_agent import HybridAgent
from config import Settings


def main():
    """主函数"""
    print("=" * 60)
    print("AI4QKD - BB84协议示例")
    print("=" * 60)
    
    # 1. 创建BB84协议
    print("\n1. 创建BB84协议...")
    bb84 = ProtocolGraph.create_bb84()
    stats = bb84.get_statistics()
    print(f"   协议名称: {stats['name']}")
    print(f"   节点数: {stats['node_count']}")
    print(f"   边数: {stats['edge_count']}")
    print(f"   节点统计: {stats['node_stats']}")
    
    # 2. 运行仿真
    print("\n2. 运行量子仿真...")
    simulator = QuantumSimulator()
    result = simulator.simulate(bb84, pulse_count=10000)
    
    print(f"   仿真脉冲数: {result.pulse_count}")
    print(f"   QBER: {result.qber:.6f}")
    print(f"   Gain: {result.gain:.6f}")
    print(f"   原始密钥率: {result.raw_key_rate:.6f}")
    print(f"   仿真时间: {result.simulation_time:.2f}秒")
    
    # 3. 使用AI评估
    print("\n3. 使用AI评估协议...")
    agent = HybridAgent()
    evaluation = agent.evaluate_protocol(bb84)
    print(f"   协议适应度: {evaluation['fitness']:.4f}")
    
    # 4. 设计新协议（快速演示）
    print("\n4. 尝试设计新协议（快速演示）...")
    print("   注意：完整训练需要时间，这里只做简单演示")
    
    # 快速训练
    training_result = agent.train(iterations=10)
    print(f"   训练完成！最佳适应度: {training_result['best_fitness']:.4f}")
    
    if training_result['best_protocol']:
        best_stats = training_result['best_protocol'].get_statistics()
        print(f"   最佳协议: {best_stats['name']}")
        print(f"   节点数: {best_stats['node_count']}")
    
    # 5. 保存结果
    print("\n5. 保存结果...")
    Settings.ensure_directories()
    
    # 保存协议
    bb84.save_to_file('results/bb84_protocol.json')
    
    # 保存仿真结果
    import json
    with open('results/bb84_result.json', 'w') as f:
        json.dump({
            'protocol_name': result.protocol_name,
            'pulse_count': result.pulse_count,
            'qber': result.qber,
            'gain': result.gain,
            'raw_key_rate': result.raw_key_rate,
            'simulation_time': result.simulation_time
        }, f, indent=2)
    
    print("   结果已保存到 results/ 目录")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)
    
    return {
        'protocol': bb84,
        'simulation_result': result,
        'evaluation': evaluation,
        'training_result': training_result
    }


if __name__ == "__main__":
    try:
        results = main()
        print("\n🎉 成功运行AI4QKD示例！")
        print("\n下一步:")
        print("1. 查看 results/ 目录中的文件")
        print("2. 修改参数重新运行")
        print("3. 探索其他功能模块")
    except Exception as e:
        print(f"\n❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()