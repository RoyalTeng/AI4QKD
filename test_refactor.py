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
        print('[测试] 创建BB84协议...')
        bb84 = create_bb84_protocol()
        print(f'[通过] BB84协议创建成功: {bb84.name}')
        print(f'   - 节点数量: {bb84.get_node_count()}')
        print(f'   - 边数量: {bb84.get_edge_count()}')
        
        # 测试DSL序列化
        print('\n[测试] 测试DSL序列化...')
        serializer = QCGFSerializer()
        dsl_text = serializer.serialize(bb84)
        print('[通过] DSL序列化成功')
        print(f'   - DSL长度: {len(dsl_text)} 字符')
        
        # 测试DSL解析
        print('\n[测试] 测试DSL解析...')
        parser = QCGFParser()
        parsed_protocol = parser.parse(dsl_text)
        print(f'[通过] DSL解析成功: {parsed_protocol.name}')
        
        # 测试理想化模式
        print('\n[测试] 测试理想化模式切换...')
        set_idealized_mode(True)
        print('[通过] 理想化模式已启用')
        
        set_idealized_mode(False)
        print('[通过] 现实模式已恢复')
        
        # 测试节点类型
        print('\n[测试] 测试节点类型系统...')
        qsp_template = get_node_template(NodeType.QSP)
        print(f'[通过] QSP模板获取成功: {len(qsp_template)} 个参数')
        
        # 测试边类型
        print('\n[测试] 测试边类型系统...')
        quantum_edge_template = get_edge_template(EdgeType.QUANTUM)
        print(f'[通过] 量子边模板获取成功: {len(quantum_edge_template)} 个参数')
        
        print('\n[成功] qcgf_dsl模块基本功能测试全部通过!')
        return True
        
    except Exception as e:
        print(f'[失败] 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_functionality()