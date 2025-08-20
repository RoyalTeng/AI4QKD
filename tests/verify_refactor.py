#!/usr/bin/env python3
"""
AI4QKD DSL重构验证脚本

目标：验证重构后的DSL框架是否严格符合研究方案定义
作者: Claude (AI Assistant)
日期: 2025-08-19
"""

import sys
import os
import warnings
warnings.filterwarnings('ignore')

def test_imports():
    """测试基本导入"""
    print("🔍 测试基本导入...")
    
    try:
        from qcgf_dsl.node_types import (
            NodeType, NodeSubType, Party, 
            get_node_template, validate_node_params,
            set_idealized_mode, is_idealized_mode
        )
        from qcgf_dsl.edge_types import (
            EdgeType, EdgeDirection, Edge,
            get_edge_template, validate_edge_params,
            validate_edge_connection
        )
        from qcgf_dsl.protocol_graph import ProtocolGraph, Node
        from qcgf_dsl.parser import QCGFParser, QCGFSerializer
        
        print("✅ 所有核心模块导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_research_compliance():
    """测试是否符合研究方案定义"""
    print("\n🔬 测试研究方案合规性...")
    
    try:
        from qcgf_dsl.node_types import NodeType
        from qcgf_dsl.edge_types import EdgeType
        
        # 检查10种标准节点类型（按研究方案2.2节）
        expected_node_types = {'QSP', 'QOP', 'QC', 'QI', 'QM', 'CIS', 'CLO', 'CC', 'CD', 'KE'}
        actual_node_types = {t.value for t in NodeType}
        
        print(f"   预期节点类型: {sorted(expected_node_types)}")
        print(f"   实际节点类型: {sorted(actual_node_types)}")
        
        if expected_node_types == actual_node_types:
            print("✅ 节点类型完全符合研究方案定义")
        else:
            missing = expected_node_types - actual_node_types
            extra = actual_node_types - expected_node_types
            if missing:
                print(f"❌ 缺失节点类型: {missing}")
            if extra:
                print(f"❌ 多余节点类型: {extra}")
            return False
        
        # 检查4种标准边类型（按研究方案2.3节）
        expected_edge_types = {'QF', 'CF', 'ControlF', 'QCIF'}
        actual_edge_types = {t.value for t in EdgeType}
        
        print(f"   预期边类型: {sorted(expected_edge_types)}")
        print(f"   实际边类型: {sorted(actual_edge_types)}")
        
        if expected_edge_types == actual_edge_types:
            print("✅ 边类型完全符合研究方案定义")
            return True
        else:
            missing = expected_edge_types - actual_edge_types
            extra = actual_edge_types - expected_edge_types
            if missing:
                print(f"❌ 缺失边类型: {missing}")
            if extra:
                print(f"❌ 多余边类型: {extra}")
            return False
            
    except Exception as e:
        print(f"❌ 研究方案合规性测试失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    try:
        from qcgf_dsl.protocol_graph import ProtocolGraph
        from qcgf_dsl.node_types import NodeType, Party
        from qcgf_dsl.edge_types import EdgeType
        
        # 创建协议图
        protocol = ProtocolGraph("TestProtocol")
        print("   ✅ 协议图创建成功")
        
        # 添加Alice的量子源节点
        alice_qsp = protocol.add_node(
            node_type=NodeType.QSP,
            party=Party.ALICE,
            params={"intensity": 0.1}
        )
        
        # 添加Bob的量子测量节点
        bob_qm = protocol.add_node(
            node_type=NodeType.QM,
            party=Party.BOB,
            params={"detector_efficiency": 0.8}
        )
        
        print(f"   ✅ 节点创建成功: {alice_qsp}, {bob_qm}")
        
        # 添加量子流边
        edge_id = protocol.add_edge(alice_qsp, bob_qm, EdgeType.QF)
        print(f"   ✅ 边创建成功: {edge_id}")
        
        # 检查统计信息
        stats = protocol.get_statistics()
        if stats['node_count'] == 2 and stats['edge_count'] == 1:
            print(f"   ✅ 协议统计正确: {stats['node_count']} 节点, {stats['edge_count']} 边")
            return True
        else:
            print(f"   ❌ 协议统计错误: {stats}")
            return False
            
    except Exception as e:
        print(f"   ❌ 基本功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates_and_validation():
    """测试模板和验证系统"""
    print("\n🧩 测试模板和验证系统...")
    
    try:
        from qcgf_dsl.node_types import NodeType, get_node_template, validate_node_params
        from qcgf_dsl.edge_types import EdgeType, get_edge_template, validate_edge_params
        
        # 测试节点模板
        print("   📋 测试节点模板...")
        for node_type in NodeType:
            template = get_node_template(node_type)
            if 'subtype' not in template:
                print(f"   ❌ {node_type.value} 缺少必需的subtype参数")
                return False
        print("   ✅ 所有节点类型模板验证通过")
        
        # 测试边模板
        print("   🔗 测试边模板...")
        for edge_type in EdgeType:
            template = get_edge_template(edge_type)
            if 'flow_type' not in template:
                print(f"   ❌ {edge_type.value} 缺少必需的flow_type参数")
                return False
        print("   ✅ 所有边类型模板验证通过")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 模板和验证测试失败: {e}")
        return False

def test_connection_constraints():
    """测试连接约束"""
    print("\n🔒 测试连接约束...")
    
    try:
        from qcgf_dsl.edge_types import EdgeType, validate_edge_connection
        
        # 测试有效连接
        valid_cases = [
            (EdgeType.QF, 'QSP', 'QM'),        # 量子流：量子源到量子测量
            (EdgeType.CF, 'CIS', 'KE'),        # 经典流：经典信息源到密钥提取
            (EdgeType.CONTROL_F, 'CD', 'QSP'), # 控制流：经典决策到量子源
            (EdgeType.QCIF, 'QM', 'CLO')       # 量子-经典接口：量子测量到经典逻辑
        ]
        
        for edge_type, source, target in valid_cases:
            if not validate_edge_connection(edge_type, source, target):
                print(f"   ❌ 有效连接验证失败: {source} -{edge_type.value}-> {target}")
                return False
        print("   ✅ 有效连接约束验证通过")
        
        # 测试无效连接
        invalid_cases = [
            (EdgeType.QF, 'CIS', 'KE'),        # 量子流不能连接经典节点
            (EdgeType.CF, 'QSP', 'QM'),        # 经典流不能连接纯量子节点
            (EdgeType.CONTROL_F, 'QSP', 'QM'), # 控制流只能从CD节点发出
            (EdgeType.QCIF, 'QSP', 'KE')       # QCIF只能从QM节点发出
        ]
        
        for edge_type, source, target in invalid_cases:
            if validate_edge_connection(edge_type, source, target):
                print(f"   ❌ 无效连接约束失败: {source} -{edge_type.value}-> {target} 应该被拒绝")
                return False
        print("   ✅ 无效连接约束验证通过")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 连接约束测试失败: {e}")
        return False

def test_idealized_mode():
    """测试理想化模式"""
    print("\n⚡ 测试理想化模式...")
    
    try:
        from qcgf_dsl.node_types import (
            set_idealized_mode, is_idealized_mode, 
            get_node_template, NodeType
        )
        
        # 测试模式切换
        set_idealized_mode(True)
        if not is_idealized_mode():
            print("   ❌ 理想化模式启用失败")
            return False
        print("   ✅ 理想化模式启用成功")
        
        # 测试理想化参数
        qc_template = get_node_template(NodeType.QC)
        if qc_template.get('loss_per_unit', 1.0) != 0.0:
            print(f"   ❌ 理想化参数错误: loss_per_unit={qc_template.get('loss_per_unit')}")
            return False
        print("   ✅ 理想化参数设置正确")
        
        # 恢复现实模式
        set_idealized_mode(False)
        if is_idealized_mode():
            print("   ❌ 现实模式恢复失败")
            return False
        print("   ✅ 现实模式恢复成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 理想化模式测试失败: {e}")
        return False

def test_dsl_parsing():
    """测试DSL解析和序列化"""
    print("\n📝 测试DSL解析和序列化...")
    
    try:
        from qcgf_dsl.protocol_graph import ProtocolGraph
        from qcgf_dsl.node_types import NodeType, Party
        from qcgf_dsl.edge_types import EdgeType
        from qcgf_dsl.parser import QCGFParser, QCGFSerializer
        
        # 创建简单协议
        protocol = ProtocolGraph("TestProtocol")
        alice_qsp = protocol.add_node(NodeType.QSP, {"party": Party.ALICE})
        bob_qm = protocol.add_node(NodeType.QM, {"party": Party.BOB})
        protocol.add_edge(alice_qsp, bob_qm, EdgeType.QF)
        
        # 序列化
        serializer = QCGFSerializer()
        dsl_text = serializer.serialize(protocol)
        print("   ✅ DSL序列化成功")
        
        # 解析
        parser = QCGFParser()
        parsed_protocol = parser.parse(dsl_text)
        print("   ✅ DSL解析成功")
        
        # 验证往返一致性
        if (protocol.get_node_count() == parsed_protocol.get_node_count() and
            protocol.get_edge_count() == parsed_protocol.get_edge_count()):
            print("   ✅ DSL往返一致性验证通过")
            return True
        else:
            print("   ❌ DSL往返一致性验证失败")
            return False
        
    except Exception as e:
        print(f"   ❌ DSL解析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 AI4QKD DSL重构验证测试")
    print("=" * 60)
    
    test_functions = [
        ("基本导入", test_imports),
        ("研究方案合规性", test_research_compliance),
        ("基本功能", test_basic_functionality),
        ("模板和验证", test_templates_and_validation),
        ("连接约束", test_connection_constraints),
        ("理想化模式", test_idealized_mode),
        ("DSL解析", test_dsl_parsing)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！qcgf_dsl模块重构成功")
        print("✅ 重构后的DSL框架完全符合研究方案定义")
        return True
    else:
        print("⚠️  部分测试失败，需要进一步修复")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)