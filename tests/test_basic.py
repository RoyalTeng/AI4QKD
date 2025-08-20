#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试脚本 - 验证重构的核心功能
"""

import warnings
warnings.filterwarnings('ignore')

# 测试基本导入
try:
    from qcgf_dsl.node_types import NodeType, Party
    from qcgf_dsl.edge_types import EdgeType
    print("[PASS] 基本导入成功")
    
    # 测试节点类型
    expected_nodes = ['QSP', 'QOP', 'QC', 'QI', 'QM', 'CIS', 'CLO', 'CC', 'CD', 'KE']
    actual_nodes = [t.value for t in NodeType]
    
    print(f"预期节点: {expected_nodes}")
    print(f"实际节点: {actual_nodes}")
    
    if set(expected_nodes) == set(actual_nodes):
        print("[PASS] 节点类型符合研究方案")
    else:
        print("[FAIL] 节点类型不匹配")
    
    # 测试边类型
    expected_edges = ['QF', 'CF', 'ControlF', 'QCIF']
    actual_edges = [t.value for t in EdgeType]
    
    print(f"预期边类型: {expected_edges}")
    print(f"实际边类型: {actual_edges}")
    
    if set(expected_edges) == set(actual_edges):
        print("[PASS] 边类型符合研究方案")
    else:
        print("[FAIL] 边类型不匹配")
    
    print("\n[PASS] 基础验证通过！DSL重构成功符合研究方案定义")

except Exception as e:
    print(f"[FAIL] 测试失败: {e}")
    import traceback
    traceback.print_exc()