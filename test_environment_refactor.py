#!/usr/bin/env python3
"""
简化测试脚本：验证AI Agent环境重构是否完成
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment_import():
    """测试环境模块导入"""
    try:
        from ai_agent.environment import QKDSimEnv
        print("✅ 成功导入QKDSimEnv")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_environment_initialization():
    """测试环境初始化"""
    try:
        from ai_agent.environment import QKDSimEnv
        
        config = {
            "DEFAULT_NUM_PULSES": 1000,
            "INVALID_PROTOCOL_PENALTY": -100.0,
            "USE_UNIVERSAL_FRAMEWORK": True
        }
        
        env = QKDSimEnv(config)
        print("✅ 成功初始化环境")
        
        # 检查关键属性
        assert hasattr(env, 'action_space'), "缺少action_space"
        assert hasattr(env, 'observation_space'), "缺少observation_space"
        assert hasattr(env, 'protocol_graph'), "缺少protocol_graph"
        assert hasattr(env, 'use_universal_framework'), "缺少use_universal_framework"
        
        print("✅ 环境属性检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 环境初始化失败: {e}")
        return False

def test_universal_methods():
    """测试通用方法"""
    try:
        from ai_agent.environment import QKDSimEnv
        
        config = {
            "DEFAULT_NUM_PULSES": 1000,
            "USE_UNIVERSAL_FRAMEWORK": True
        }
        
        env = QKDSimEnv(config)
        
        # 检查通用方法
        assert hasattr(env, 'run_universal_simulation'), "缺少run_universal_simulation"
        assert hasattr(env, 'analyze_protocol_security'), "缺少analyze_protocol_security"
        assert hasattr(env, 'estimate_protocol_entropy'), "缺少estimate_protocol_entropy"
        assert hasattr(env, 'evaluate_protocol'), "缺少evaluate_protocol"
        assert hasattr(env, 'convert_protocol_to_features'), "缺少convert_protocol_to_features"
        
        print("✅ 通用方法检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 通用方法检查失败: {e}")
        return False

def test_action_processing():
    """测试动作处理"""
    try:
        from ai_agent.environment import QKDSimEnv
        import numpy as np
        
        config = {
            "DEFAULT_NUM_PULSES": 1000,
            "USE_UNIVERSAL_FRAMEWORK": True
        }
        
        env = QKDSimEnv(config)
        
        # 测试动作空间
        assert env.action_space.contains({
            "action_type": 0,
            "node_type_to_add": 0,
            "param_to_modify": 0,
            "param_value": np.array([0.5])
        }), "动作空间验证失败"
        
        print("✅ 动作处理检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 动作处理检查失败: {e}")
        return False

def test_backward_compatibility():
    """测试向后兼容性"""
    try:
        from ai_agent.environment import QKDSimEnv
        
        config = {
            "DEFAULT_NUM_PULSES": 1000,
            "USE_UNIVERSAL_FRAMEWORK": False  # 使用传统框架
        }
        
        env = QKDSimEnv(config)
        
        # 检查传统方法
        assert hasattr(env, 'evaluate_protocol_legacy'), "缺少evaluate_protocol_legacy"
        assert hasattr(env, '_fallback_security_analysis'), "缺少_fallback_security_analysis"
        assert hasattr(env, '_fallback_evaluation'), "缺少_fallback_evaluation"
        
        print("✅ 向后兼容性检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 向后兼容性检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔍 开始AI Agent环境重构验证...")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_environment_import),
        ("环境初始化", test_environment_initialization),
        ("通用方法", test_universal_methods),
        ("动作处理", test_action_processing),
        ("向后兼容性", test_backward_compatibility),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 测试: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！AI Agent环境重构完成！")
        return True
    else:
        print("⚠️  部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 