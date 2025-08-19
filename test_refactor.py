#!/usr/bin/env python3
"""
AI4QKD DSL重构验证测试 - 基于研究方案严格定义

测试目标：
- 验证重构后的node和edge类型是否严格符合研究方案
- 测试DSL解析和序列化功能
- 验证理想化模式切换
- 确保基本协议创建功能正常

作者: Claude (AI Assistant)
测试日期: 2025-08-19
依据: f:\AI4QKD\研究方案\第一部分.pdf
"""

import warnings
warnings.filterwarnings('ignore')

from qcgf_dsl import *

def test_research_compliance():
    """测试是否符合研究方案定义"""
    print('🔬 测试研究方案合规性...')
    
    # 测试10种标准节点类型（按研究方案2.2节）
    expected_node_types = ['QSP', 'QOP', 'QC', 'QI', 'QM', 'CIS', 'CLO', 'CC', 'CD', 'KE']
    actual_node_types = [t.value for t in NodeType]
    
    print(f'   - 预期节点类型: {expected_node_types}')
    print(f'   - 实际节点类型: {actual_node_types}')
    
    if set(expected_node_types) == set(actual_node_types):
        print('✅ 节点类型完全符合研究方案定义')
    else:
        missing = set(expected_node_types) - set(actual_node_types)
        extra = set(actual_node_types) - set(expected_node_types)
        if missing:
            print(f'❌ 缺失节点类型: {missing}')
        if extra:
            print(f'❌ 多余节点类型: {extra}')
        return False
    
    # 测试4种标准边类型（按研究方案2.3节）
    expected_edge_types = ['QF', 'CF', 'ControlF', 'QCIF']
    actual_edge_types = [t.value for t in EdgeType]
    
    print(f'   - 预期边类型: {expected_edge_types}')
    print(f'   - 实际边类型: {actual_edge_types}')
    
    if set(expected_edge_types) == set(actual_edge_types):
        print('✅ 边类型完全符合研究方案定义')
    else:
        missing = set(expected_edge_types) - set(actual_edge_types)
        extra = set(actual_edge_types) - set(expected_edge_types)
        if missing:
            print(f'❌ 缺失边类型: {missing}')
        if extra:
            print(f'❌ 多余边类型: {extra}')
        return False
    
    return True

def test_basic_functionality():
    """测试基本功能"""
    print('\n🧪 测试基本功能...')
    
    try:
        # 测试创建BB84协议
        print('   📋 创建BB84协议...')
        bb84 = create_bb84_protocol()
        print(f'   ✅ BB84协议创建成功: {bb84.name}')
        print(f'      - 节点数量: {bb84.get_node_count()}')
        print(f'      - 边数量: {bb84.get_edge_count()}')
        
        # 测试DSL序列化
        print('   📝 测试DSL序列化...')
        serializer = QCGFSerializer()
        dsl_text = serializer.serialize(bb84)
        print('   ✅ DSL序列化成功')
        print(f'      - DSL长度: {len(dsl_text)} 字符')
        
        # 测试DSL解析
        print('   🔄 测试DSL解析...')
        parser = QCGFParser()
        parsed_protocol = parser.parse(dsl_text)
        print(f'   ✅ DSL解析成功: {parsed_protocol.name}')
        
        # 验证往返一致性
        if (bb84.get_node_count() == parsed_protocol.get_node_count() and
            bb84.get_edge_count() == parsed_protocol.get_edge_count()):
            print('   ✅ DSL序列化往返一致性验证通过')
        else:
            print('   ❌ DSL往返一致性验证失败')
            return False
        
        return True
        
    except Exception as e:
        print(f'   ❌ 基本功能测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_idealized_mode():
    """测试理想化模式"""
    print('\n⚡ 测试理想化模式...')
    
    try:
        # 测试模式切换
        print('   🔧 切换到理想化模式...')
        set_idealized_mode(True)
        if is_idealized_mode():
            print('   ✅ 理想化模式启用成功')
        else:
            print('   ❌ 理想化模式启用失败')
            return False
        
        # 测试理想化参数
        print('   📊 验证理想化参数...')
        qc_template = get_node_template(NodeType.QC)
        if qc_template.get('loss_per_unit', 1.0) == 0.0:
            print('   ✅ 理想化参数设置正确（无损耗）')
        else:
            print(f'   ❌ 理想化参数错误: loss_per_unit={qc_template.get("loss_per_unit")}')
            return False
        
        # 恢复现实模式
        print('   🔧 恢复现实模式...')
        set_idealized_mode(False)
        if not is_idealized_mode():
            print('   ✅ 现实模式恢复成功')
        else:
            print('   ❌ 现实模式恢复失败')
            return False
        
        return True
        
    except Exception as e:
        print(f'   ❌ 理想化模式测试失败: {e}')
        return False

def test_node_edge_templates():
    """测试节点和边模板系统"""
    print('\n🧩 测试模板系统...')
    
    try:
        # 测试所有节点类型的模板
        print('   📋 验证节点模板...')
        for node_type in NodeType:
            template = get_node_template(node_type)
            if 'subtype' not in template:
                print(f'   ❌ {node_type.value} 缺少必需的subtype参数')
                return False
        print('   ✅ 所有节点类型模板验证通过')
        
        # 测试所有边类型的模板
        print('   🔗 验证边模板...')
        for edge_type in EdgeType:
            template = get_edge_template(edge_type)
            if 'flow_type' not in template:
                print(f'   ❌ {edge_type.value} 缺少必需的flow_type参数')
                return False
        print('   ✅ 所有边类型模板验证通过')
        
        return True
        
    except Exception as e:
        print(f'   ❌ 模板系统测试失败: {e}')
        return False

def test_connection_constraints():
    """测试边连接约束"""
    print('\n🔒 测试连接约束...')
    
    try:
        from qcgf_dsl.edge_types import validate_edge_connection
        
        # 测试有效连接
        valid_cases = [
            (EdgeType.QF, 'QSP', 'QM'),      # 量子流：量子源到量子测量
            (EdgeType.CF, 'CIS', 'KE'),      # 经典流：经典信息源到密钥提取
            (EdgeType.CONTROL_F, 'CD', 'QSP'), # 控制流：经典决策到量子源
            (EdgeType.QCIF, 'QM', 'CLO')     # 量子-经典接口：量子测量到经典逻辑
        ]
        
        for edge_type, source, target in valid_cases:
            if not validate_edge_connection(edge_type, source, target):
                print(f'   ❌ 有效连接验证失败: {source} -{edge_type.value}-> {target}')
                return False
        print('   ✅ 有效连接约束验证通过')
        
        # 测试无效连接
        invalid_cases = [
            (EdgeType.QF, 'CIS', 'KE'),      # 量子流不能连接经典节点
            (EdgeType.CF, 'QSP', 'QM'),      # 经典流不能连接量子源到量子测量
            (EdgeType.CONTROL_F, 'QSP', 'QM'), # 控制流只能从CD节点发出
            (EdgeType.QCIF, 'QSP', 'KE')     # QCIF只能从QM节点发出
        ]
        
        for edge_type, source, target in invalid_cases:
            if validate_edge_connection(edge_type, source, target):
                print(f'   ❌ 无效连接约束失败: {source} -{edge_type.value}-> {target} 应该被拒绝')
                return False
        print('   ✅ 无效连接约束验证通过')
        
        return True
        
    except Exception as e:
        print(f'   ❌ 连接约束测试失败: {e}')
        return False

def main():
    """主测试函数"""
    print('🚀 AI4QKD DSL重构验证测试开始')
    print('=' * 60)
    
    test_functions = [
        ('研究方案合规性', test_research_compliance),
        ('基本功能', test_basic_functionality), 
        ('理想化模式', test_idealized_mode),
        ('模板系统', test_node_edge_templates),
        ('连接约束', test_connection_constraints)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            if test_func():
                passed += 1
            else:
                print(f'❌ {test_name}测试失败')
        except Exception as e:
            print(f'❌ {test_name}测试异常: {e}')
    
    print('\n' + '=' * 60)
    print(f'📊 测试结果: {passed}/{total} 通过')
    
    if passed == total:
        print('🎉 所有测试通过！qcgf_dsl模块重构成功')
        print('✅ 重构后的DSL框架完全符合研究方案定义')
        return True
    else:
        print('⚠️  部分测试失败，需要进一步修复')
        return False

if __name__ == "__main__":
    main()