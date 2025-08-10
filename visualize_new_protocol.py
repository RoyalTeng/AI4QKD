#!/usr/bin/env python3
"""
新协议可视化脚本
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# 安装matplotlib后再取消注释
try:
    from qcgf_dsl.visualizer import visualize_protocol
    from tests.test_strict_protocol_discovery import TestStrictProtocolDiscovery
    
    # 创建测试实例并生成协议
    test_instance = TestStrictProtocolDiscovery()
    test_instance.setup_method()
    
    # 创建新协议
    dual_adaptive_protocol = test_instance.create_enhanced_protocol_v2()
    
    # 生成可视化
    print("生成双重自适应BB84协议图...")
    visualize_protocol(
        dual_adaptive_protocol, 
        save_path="DUAL_ADAPTIVE_BB84_PROTOCOL_GRAPH.png"
    )
    print("✅ 协议图已保存为: DUAL_ADAPTIVE_BB84_PROTOCOL_GRAPH.png")
    
except ImportError as e:
    print(f"暂时无法生成可视化图表，缺少依赖: {e}")
    print("协议结构：Alice_QSP -> Alice_CLO -> QC -> Bob_CLO -> Bob_QM")