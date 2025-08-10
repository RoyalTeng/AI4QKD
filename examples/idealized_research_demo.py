"""
理想化科学研究模式演示
=====================

本示例演示如何使用AI4QKD的理想化参数设置进行科学研究的原理验证。

理想化假设：
1. 单光子探测器效率 = 100%
2. 信道损耗 = 0
3. 噪声 = 0
4. 处理时间 = 0
5. 专注于协议设计算法的验证

运行方式：
python examples/idealized_research_demo.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcgf_dsl.node_types import (
    NodeType, Party, 
    setup_idealized_research_mode, 
    setup_realistic_deployment_mode,
    compare_mode_parameters,
    print_current_mode_info,
    get_node_template
)
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.edge_types import EdgeType
from config.idealized_parameters import get_idealized_config

def demonstrate_parameter_differences():
    """演示理想化模式与现实模式的参数差异"""
    print("📊 参数对比分析")
    print("=" * 60)
    
    # 关键节点类型的参数对比
    key_node_types = [NodeType.QSP, NodeType.QC, NodeType.QM, NodeType.QD]
    
    for node_type in key_node_types:
        print(f"\n🔍 {node_type.value} 节点参数对比：")
        comparison = compare_mode_parameters(node_type)
        
        if comparison["key_differences"]:
            for diff in comparison["key_differences"]:
                print(f"   • {diff}")
        else:
            print("   • 无差异")

def create_idealized_bb84_protocol():
    """创建理想化的BB84协议"""
    print("\n🧬 创建理想化BB84协议")
    print("=" * 60)
    
    # 创建协议图
    protocol = ProtocolGraph("Idealized_BB84")
    
    # 添加Alice的量子态制备节点
    alice_qsp = protocol.add_node(
        NodeType.QSP,
        params={"state": "|0⟩", "basis": "Z"},
        party=Party.ALICE,
        position=(0, 0)
    )
    print(f"✅ 添加Alice QSP节点: {alice_qsp}")
    
    # 添加量子信道
    quantum_channel = protocol.add_node(
        NodeType.QC,
        params={"distance": 100.0},  # 理想化参数会自动应用
        position=(1, 0)
    )
    print(f"✅ 添加量子信道节点: {quantum_channel}")
    
    # 添加Bob的量子测量节点
    bob_qm = protocol.add_node(
        NodeType.QM,
        params={"basis": "Z"},
        party=Party.BOB,
        position=(2, 0)
    )
    print(f"✅ 添加Bob QM节点: {bob_qm}")
    
    # 添加边连接
    protocol.add_edge(alice_qsp, quantum_channel, EdgeType.QUANTUM)
    protocol.add_edge(quantum_channel, bob_qm, EdgeType.QUANTUM)
    print("✅ 添加量子连接")
    
    # 添加经典通信信道
    classical_channel = protocol.add_node(
        NodeType.CC,
        position=(1, -1)
    )
    protocol.add_edge(alice_qsp, classical_channel, EdgeType.CLASSICAL)
    protocol.add_edge(classical_channel, bob_qm, EdgeType.CLASSICAL)
    print("✅ 添加经典通信")
    
    # 显示协议统计
    stats = protocol.get_statistics()
    print(f"\n📊 协议统计:")
    print(f"   节点数: {stats['node_count']}")
    print(f"   边数: {stats['edge_count']}")
    print(f"   节点类型: {list(stats['node_stats'].keys())}")
    
    return protocol

def analyze_idealized_performance():
    """分析理想化协议性能"""
    print("\n📈 理想化性能分析")
    print("=" * 60)
    
    # 获取理想化配置
    config = get_idealized_config('BB84')
    
    print("🎯 理想化性能指标:")
    print("   • 量子态制备保真度: 100%")
    print("   • 信道传输保真度: 100%") 
    print("   • 检测效率: 100%")
    print("   • 信道损耗: 0%")
    print("   • 噪声水平: 0%")
    print("   • 处理延迟: 0ms")
    
    print("\n🔬 科学研究价值:")
    print("   • 消除硬件噪声干扰")
    print("   • 专注协议结构优化")
    print("   • 建立性能理论上界")
    print("   • 验证AI算法有效性")

def compare_with_realistic_mode():
    """与现实模式对比"""
    print("\n⚖️ 理想化 vs 现实模式对比")
    print("=" * 60)
    
    print("🔬 理想化科学研究模式:")
    print("   优势: 突出算法创新，消除硬件限制")
    print("   目标: 验证协议设计算法原理")
    print("   应用: 早期研究阶段，算法验证")
    
    print("\n⚙️ 现实部署模式:")
    print("   优势: 考虑实际约束，面向工程应用") 
    print("   目标: 优化实际系统性能")
    print("   应用: 产品开发阶段，工程优化")
    
    print("\n🔄 研究路径建议:")
    print("   1. 理想化模式验证算法原理")
    print("   2. 逐步引入现实约束")
    print("   3. 现实模式优化实际性能")
    print("   4. 量化硬件限制影响")

def main():
    """主演示程序"""
    print("🧪 AI4QKD理想化科学研究模式演示")
    print("=" * 80)
    
    # 1. 设置理想化模式
    setup_idealized_research_mode()
    print_current_mode_info()
    
    # 2. 演示参数差异
    demonstrate_parameter_differences()
    
    # 3. 创建理想化协议
    protocol = create_idealized_bb84_protocol()
    
    # 4. 分析理想化性能
    analyze_idealized_performance()
    
    # 5. 模式对比
    compare_with_realistic_mode()
    
    print("\n" + "=" * 80)
    print("🎉 理想化模式演示完成！")
    print("💡 建议：先用理想化模式验证算法，再逐步向现实模式过渡")
    
    # 可选：切换到现实模式展示差异
    print("\n🔄 切换到现实模式:")
    setup_realistic_deployment_mode()
    print_current_mode_info()

if __name__ == "__main__":
    main()