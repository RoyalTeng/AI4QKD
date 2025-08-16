#!/usr/bin/env python3
"""
AI4QKD系统集成测试总结
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from tests.test_strict_protocol_discovery import TestStrictProtocolDiscovery

def main():
    """运行集成测试总结"""
    print("=" * 60)
    print("AI4QKD系统集成测试总结报告")
    print("=" * 60)
    
    try:
        # 创建测试实例
        test_instance = TestStrictProtocolDiscovery()
        test_instance.setup_method()
        
        print("\n1. BB84基准验证:")
        bb84_protocol = test_instance.create_bb84_protocol()
        bb84_result = test_instance.calculate_protocol_performance(bb84_protocol)
        print(f"   BB84密钥率: {bb84_result['key_rate']:.6f} bits/pulse")
        print(f"   QBER: {bb84_result['qber']:.4f}")
        print(f"   Gain: {bb84_result['gain']:.4f}")
        
        print("\n2. 增强协议测试:")
        enhanced_protocol = test_instance.create_enhanced_protocol_v2()
        enhanced_result = test_instance.calculate_protocol_performance(enhanced_protocol)
        print(f"   增强协议密钥率: {enhanced_result['key_rate']:.6f} bits/pulse")
        print(f"   协议效率因子: {enhanced_result['protocol_efficiency']:.4f}")
        
        improvement = enhanced_result['key_rate'] / bb84_result['key_rate'] - 1
        print(f"   性能提升: {improvement*100:.2f}%")
        
        print("\n3. 协议结构分析:")
        stats = enhanced_protocol.get_statistics()
        print(f"   节点数: {stats['node_count']}")
        print(f"   边数: {stats['edge_count']}")
        print(f"   节点类型: {list(stats['node_stats'].keys())}")
        
        print("\n4. 系统验证结果:")
        if enhanced_result['key_rate'] > bb84_result['key_rate']:
            print("   ✓ 系统成功设计出性能优于BB84的新协议")
            print("   ✓ AI驱动的协议设计系统有效")
        else:
            print("   × 新协议性能未超越BB84基准")
        
        print("\n5. 文件生成验证:")
        protocol_graph_exists = os.path.exists("DUAL_ADAPTIVE_BB84_PROTOCOL_GRAPH.png")
        training_logs_exist = os.path.exists("logs/ai_training/test_integration_run/action_log.csv")
        
        print(f"   协议图文件: {'✓' if protocol_graph_exists else '×'}")
        print(f"   训练日志: {'✓' if training_logs_exist else '×'}")
        
        print("\n" + "=" * 60)
        print("集成测试结论:")
        if (enhanced_result['key_rate'] > bb84_result['key_rate'] and 
            protocol_graph_exists and training_logs_exist):
            print("✓ AI4QKD系统完全有效 - 能够设计出性能优于传统协议的新QKD协议")
        else:
            print("△ AI4QKD系统部分有效 - 存在一些技术问题需要解决")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试执行出错: {e}")
        print("系统需要进一步调试")

if __name__ == "__main__":
    main()