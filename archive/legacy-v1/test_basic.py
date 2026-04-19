#!/usr/bin/env python3
"""
基础测试
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))


def test_qcgf():
    """测试QCGF DSL"""
    print("测试QCGF DSL...")
    
    try:
        from qcgf_dsl import ProtocolGraph, NodeType
        
        # 创建协议
        protocol = ProtocolGraph("测试协议")
        
        # 添加节点
        node1 = protocol.add_node(NodeType.QSP, {'state': '|0⟩', 'basis': 'Z'})
        node2 = protocol.add_node(NodeType.QM, {'basis': 'Z'})
        
        # 添加边
        protocol.add_edge(node1, node2)
        
        # 验证
        assert protocol.get_node_count() == 2
        assert protocol.get_edge_count() == 1
        
        print("✅ QCGF DSL测试通过")
        return True
    except Exception as e:
        print(f"❌ QCGF测试失败: {e}")
        return False


def test_simulator():
    """测试仿真器"""
    print("\n测试仿真器...")
    
    try:
        from simulator import QuantumSimulator
        from qcgf_dsl import ProtocolGraph
        
        simulator = QuantumSimulator()
        protocol = ProtocolGraph("测试")
        protocol.add_node('QSP', {'state': '|0⟩', 'basis': 'Z'})
        
        result = simulator.simulate(protocol, pulse_count=100)
        
        assert hasattr(result, 'qber')
        assert hasattr(result, 'gain')
        assert 0 <= result.qber <= 1
        assert 0 <= result.gain <= 1
        
        print("✅ 仿真器测试通过")
        return True
    except Exception as e:
        print(f"❌ 仿真器测试失败: {e}")
        return False


def test_ai_agent():
    """测试AI智能体"""
    print("\n测试AI智能体...")
    
    try:
        from ai_agent import HybridAgent
        from qcgf_dsl import ProtocolGraph
        
        agent = HybridAgent()
        protocol = ProtocolGraph.create_bb84()
        
        evaluation = agent.evaluate_protocol(protocol)
        
        assert 'fitness' in evaluation
        assert 'protocol_name' in evaluation
        
        print("✅ AI智能体测试通过")
        return True
    except Exception as e:
        print(f"❌ AI智能体测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("AI4QKD基础测试")
    print("=" * 60)
    
    tests = [
        ("QCGF DSL", test_qcgf),
        ("仿真器", test_simulator),
        ("AI智能体", test_ai_agent)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"{name}测试失败")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  有测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())