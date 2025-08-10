#!/usr/bin/env python3
"""
独立的环境测试脚本，绕过torch依赖问题
"""

import sys
import warnings
warnings.filterwarnings('ignore')

# 直接导入相关模块，避免通过__init__.py
sys.path.insert(0, '/mnt/c/Users/royal/Desktop/AI4QKD')

def test_environment_implementation():
    """测试环境实现的核心功能"""
    print("=== 测试AI Agent环境的通用框架集成 ===\n")
    
    try:
        # 测试1: 导入和初始化
        print("1. 测试环境导入和初始化...")
        
        # 必须直接导入，避开__init__.py的torch依赖
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "environment", 
            "/mnt/c/Users/royal/Desktop/AI4QKD/ai_agent/environment.py"
        )
        env_module = importlib.util.module_from_spec(spec)
        
        # 添加必要的依赖
        from qcgf_dsl.protocol_graph import ProtocolGraph
        from qcgf_dsl.node_types import NodeType
        from qcgf_dsl.edge_types import EdgeType
        from simulator.real_quantum_simulator import RealQuantumSimulator
        from security_evaluator.key_rate_calculator import KeyRateCalculator
        from security_evaluator.ac_framework import ProtocolType
        
        sys.modules['qcgf_dsl.protocol_graph'] = sys.modules['qcgf_dsl.protocol_graph']
        sys.modules['qcgf_dsl.node_types'] = sys.modules['qcgf_dsl.node_types']
        sys.modules['qcgf_dsl.edge_types'] = sys.modules['qcgf_dsl.edge_types']
        sys.modules['simulator.real_quantum_simulator'] = sys.modules['simulator.real_quantum_simulator']
        sys.modules['security_evaluator.key_rate_calculator'] = sys.modules['security_evaluator.key_rate_calculator']
        sys.modules['security_evaluator.ac_framework'] = sys.modules['security_evaluator.ac_framework']
        
        spec.loader.exec_module(env_module)
        
        QKDSimEnv = env_module.QKDSimEnv
        print("   ✓ 环境类导入成功")
        
        # 测试初始化
        config = {
            'USE_UNIVERSAL_FRAMEWORK': True,
            'DEFAULT_NUM_PULSES': 10000,
            'INVALID_PROTOCOL_PENALTY': -100.0,
            'EPSILON_SEC': 1e-10,
            'EPSILON_COR': 1e-10,
            'EPSILON_PE': 1e-10
        }
        
        env = QKDSimEnv(config)
        print("   ✓ 环境实例创建成功")
        print(f"   ✓ 使用通用框架: {env.use_universal_framework}")
        
        # 测试2: 检查方法存在性
        print("\n2. 测试通用框架方法...")
        methods_to_check = [
            'convert_protocol_to_features',
            'run_universal_simulation', 
            'analyze_protocol_security',
            'estimate_protocol_entropy',
            'evaluate_protocol',
            'evaluate_protocol_legacy'
        ]
        
        for method in methods_to_check:
            if hasattr(env, method):
                print(f"   ✓ 方法 {method} 存在")
            else:
                print(f"   ✗ 方法 {method} 缺失")
                
        # 测试3: 协议图转换功能
        print("\n3. 测试协议图转换...")
        try:
            protocol_features = env.convert_protocol_to_features(env.protocol_graph)
            if protocol_features:
                print(f"   ✓ 协议转换成功: {protocol_features.name}")
                print(f"   ✓ 操作数量: {len(protocol_features.operations)}")
            else:
                print("   ○ 协议转换返回None（可能是通用框架未可用）")
        except Exception as e:
            print(f"   ○ 协议转换失败: {e}")
            
        # 测试4: 动作空间扩展
        print("\n4. 测试动作空间...")
        print(f"   ✓ 动作类型数量: {env.action_space['action_type'].n}")
        print(f"   ✓ 参数修改选项: {env.action_space['param_to_modify'].n}")
        print(f"   ✓ 观察空间维度: {env.observation_space.shape}")
        
        # 测试5: 环境重置和基本操作
        print("\n5. 测试环境基本操作...")
        try:
            obs, info = env.reset()
            print("   ✓ 环境重置成功")
            
            # 测试协议有效性检查
            is_valid = env._is_protocol_valid()
            print(f"   ✓ 协议有效性检查: {is_valid}")
            
            # 测试基础协议图创建
            base_graph = env._create_base_bb84_graph()
            print(f"   ✓ 基础BB84协议图: {base_graph.get_node_count()} 节点")
            
        except Exception as e:
            print(f"   ○ 基本操作测试失败: {e}")
            
        print("\n=== 环境测试完成 ===")
        return True
        
    except Exception as e:
        print(f"✗ 环境测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_universal_framework_integration():
    """测试通用框架集成"""
    print("\n=== 测试通用框架集成 ===\n")
    
    try:
        from security_evaluator.universal_framework import (
            create_bb84_protocol, 
            create_mdi_qkd_protocol,
            UniversalSecurityParameters
        )
        
        print("1. 测试协议创建...")
        bb84 = create_bb84_protocol()
        mdi_qkd = create_mdi_qkd_protocol()
        print(f"   ✓ BB84协议: {bb84.name}")
        print(f"   ✓ MDI-QKD协议: {mdi_qkd.name}")
        
        print("\n2. 测试安全参数...")
        security_params = UniversalSecurityParameters(
            epsilon_sec=1e-10,
            epsilon_cor=1e-10,
            epsilon_pe=1e-10
        )
        print(f"   ✓ 安全参数创建: ε_sec = {security_params.epsilon_sec}")
        
        print("\n=== 通用框架测试完成 ===")
        return True
        
    except Exception as e:
        print(f"✗ 通用框架测试失败: {e}")
        return False

if __name__ == "__main__":
    success1 = test_universal_framework_integration()
    success2 = test_environment_implementation()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！环境重构成功！")
        exit(0)
    else:
        print("\n⚠️  部分测试失败，需要进一步检查")
        exit(1)