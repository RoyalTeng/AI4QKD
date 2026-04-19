
# AI4QKD 实验代码
# 实验类型: ai_design
# 设计时间: 2026-03-30T13:41:19.688978

import sys
sys.path.insert(0, '.')

from qcgf_dsl import ProtocolGraph
from simulator import QuantumSimulator
from ai_agent import HybridAgent
import json

def run_experiment():
    """运行实验"""
    print("=" * 60)
    print("AI4QKD 实验")
    print("=" * 60)
    
    # 实验设置
    
    # AI设计设置
    agent = HybridAgent()
    iterations = 50
            
    
    # 运行实验
    
    # 运行AI设计
    print(f"🚀 AI正在设计新协议 ({iterations}次迭代)...")
    training_result = agent.train(iterations=iterations)
    
    print(f"🎯 最佳适应度: {training_result['best_fitness']:.4f}")
    
    if training_result['best_protocol']:
        best_protocol = training_result['best_protocol']
        stats = best_protocol.get_statistics()
        print(f"📊 最佳协议: {stats['name']}")
        print(f"   节点数: {stats['node_count']}")
        print(f"   边数: {stats['edge_count']}")
            
    
    # 保存结果
    
    # 保存AI设计结果
    import time
    timestamp = int(time.time())
    filename = f"results/ai_design_{timestamp}.json"
    
    result_data = {
        "experiment": "AI协议设计",
        "iterations": iterations,
        "best_fitness": training_result['best_fitness'],
        "best_protocol": training_result['best_protocol'].get_statistics() if training_result['best_protocol'] else None,
        "timestamp": timestamp
    }
    
    with open(filename, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {filename}")
            
    
    print("\n✅ 实验完成!")

if __name__ == "__main__":
    run_experiment()
