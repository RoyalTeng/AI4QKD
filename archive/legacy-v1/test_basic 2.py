#!/usr/bin/env python3
"""
AI4QKD项目基础测试
测试核心模块是否能正常导入和运行
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def test_qcgf_dsl():
    """测试QCGF DSL模块"""
    print("🧪 测试QCGF DSL模块...")
    try:
        from qcgf_dsl.protocol_graph import ProtocolGraph
        from qcgf_dsl.node_types import NodeType, Party
        
        # 创建协议图
        graph = ProtocolGraph(name='BB84_Test')
        
        # 添加节点
        graph.add_node(node_type=NodeType.QSP, 
                      params={'state': '|+⟩', 'basis': 'X'}, 
                      party=Party.ALICE, 
                      node_id='Alice_QSP')
        
        graph.add_node(node_type=NodeType.QC, 
                      params={'loss': 0.1, 'noise': 0.01}, 
                      node_id='QuantumChannel')
        
        graph.add_node(node_type=NodeType.QM, 
                      params={'basis': 'X'}, 
                      party=Party.BOB, 
                      node_id='Bob_QM')
        
        # 添加边
        graph.add_edge('Alice_QSP', 'QuantumChannel')
        graph.add_edge('QuantumChannel', 'Bob_QM')
        
        # 验证
        print(f"  ✅ 协议图创建成功: {graph.name}")
        print(f"     节点数: {graph.get_node_count()}")
        print(f"     边数: {graph.get_edge_count()}")
        print(f"     是否为DAG: {graph.is_dag()}")
        
        # 获取统计信息
        stats = graph.get_statistics()
        print(f"     统计信息: {stats}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ QCGF DSL测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置模块"""
    print("\n🧪 测试配置模块...")
    try:
        from config import settings
        from config.qkd_protocols import BB84_PARAMS
        
        print(f"  ✅ 配置导入成功")
        print(f"     日志级别: {settings.LOG_LEVEL}")
        print(f"     BB84参数: {list(BB84_PARAMS.keys())}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        return False

def test_utils():
    """测试工具模块"""
    print("\n🧪 测试工具模块...")
    try:
        from utils.logger import setup_logger
        
        logger = setup_logger('test_logger', log_level='INFO')
        logger.info("测试日志消息")
        
        print(f"  ✅ 工具模块导入成功")
        return True
        
    except Exception as e:
        print(f"  ❌ 工具模块测试失败: {e}")
        return False

def test_simulator():
    """测试仿真器模块"""
    print("\n🧪 测试仿真器模块...")
    try:
        # 先导入基础模块
        from simulator.quantum_simulator import QuantumSimulator
        
        print(f"  ✅ 仿真器模块导入成功")
        print(f"     可用类: QuantumSimulator")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 仿真器模块测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("AI4QKD项目基础测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("QCGF DSL", test_qcgf_dsl()))
    results.append(("配置模块", test_config()))
    results.append(("工具模块", test_utils()))
    results.append(("仿真器模块", test_simulator()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for module_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{module_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有基础测试通过！项目可以正常开发。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，需要修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())