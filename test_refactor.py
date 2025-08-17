#!/usr/bin/env python3
"""
快速测试重构后的qcgf_dsl模块功能
"""

import warnings
warnings.filterwarnings('ignore')

from qcgf_dsl import *

def test_basic_functionality():
    """测试基本功能"""
    try:
        
        # 测试创建BB84协议
        print('[TEST] Creating BB84 protocol...')
        bb84 = create_bb84_protocol()
        print(f'[PASS] BB84 protocol created: {bb84.name}')
        print(f'   - Node count: {bb84.get_node_count()}')
        print(f'   - Edge count: {bb84.get_edge_count()}')
        
        # 测试DSL序列化
        print('\n[TEST] Testing DSL serialization...')
        serializer = QCGFSerializer()
        dsl_text = serializer.serialize(bb84)
        print('[PASS] DSL serialization successful')
        print(f'   - DSL length: {len(dsl_text)} characters')
        
        # 测试DSL解析
        print('\n[TEST] Testing DSL parsing...')
        parser = QCGFParser()
        parsed_protocol = parser.parse(dsl_text)
        print(f'[PASS] DSL parsing successful: {parsed_protocol.name}')
        
        # 测试理想化模式
        print('\n[TEST] Testing idealized mode switching...')
        set_idealized_mode(True)
        print('[PASS] Idealized mode enabled')
        
        set_idealized_mode(False)
        print('[PASS] Realistic mode restored')
        
        # 测试节点类型
        print('\n[TEST] Testing node type system...')
        qsp_template = get_node_template(NodeType.QSP)
        print(f'[PASS] QSP template retrieved: {len(qsp_template)} parameters')
        
        # 测试边类型
        print('\n[TEST] Testing edge type system...')
        quantum_edge_template = get_edge_template(EdgeType.QUANTUM)
        print(f'[PASS] QUANTUM edge template retrieved: {len(quantum_edge_template)} parameters')
        
        print('\n[SUCCESS] All qcgf_dsl module basic functionality tests passed!')
        return True
        
    except Exception as e:
        print(f'[FAIL] Test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_functionality()