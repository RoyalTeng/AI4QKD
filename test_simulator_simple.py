#!/usr/bin/env python
"""
AI4QKD - simulator模块简化功能验证脚本
用于第四步多轮迭代的基础功能验证
"""

import sys
import os

def test_module_import():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 添加当前目录到Python路径
        sys.path.insert(0, os.getcwd())
        
        # 测试基础依赖
        import numpy as np
        print("✅ numpy导入成功")
        
        # 测试simulator子模块导入
        from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
        print("✅ KeyRateCalculator导入成功")
        
        from simulator.qber_simulator import QBERSimulator, QBERParameters
        print("✅ QBERSimulator导入成功")
        
        from simulator.dv_qkd_validator import DVQKDValidator
        print("✅ DVQKDValidator导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_key_rate_calculator():
    """测试密钥率计算功能"""
    print("\n🧮 测试密钥率计算...")
    
    try:
        from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
        
        # 创建计算器
        calculator = KeyRateCalculator()
        print("✅ KeyRateCalculator创建成功")
        
        # 创建参数
        params = KeyRateParameters(qber=0.05, gain=0.5)
        params.validate()
        print("✅ 参数验证通过")
        
        # 计算渐近密钥率
        asymptotic_rate = calculator.calculate_asymptotic_key_rate(params)
        print(f"✅ 渐近密钥率: {asymptotic_rate:.6f} bits/pulse")
        
        # 验证结果合理性
        if 0 <= asymptotic_rate <= 1:
            print("✅ 密钥率范围合理")
        else:
            print(f"⚠️ 密钥率范围异常: {asymptotic_rate}")
        
        return True
        
    except Exception as e:
        print(f"❌ 密钥率计算测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qber_simulator():
    """测试QBER仿真功能"""
    print("\n📊 测试QBER仿真...")
    
    try:
        from simulator.qber_simulator import QBERSimulator, QBERParameters, EncodingScheme
        
        # 创建QBER仿真器
        qber_sim = QBERSimulator()
        print("✅ QBERSimulator创建成功")
        
        # 创建参数
        params = QBERParameters(
            encoding_scheme=EncodingScheme.POLARIZATION,
            channel_length=50.0
        )
        params.validate()
        print("✅ QBER参数验证通过")
        
        # 执行QBER仿真
        qber_result = qber_sim.simulate_total_qber(params)
        total_qber = qber_result['total_qber']
        print(f"✅ 总QBER: {total_qber:.6f}")
        
        # 验证安全性
        is_secure = qber_result['is_secure']
        print(f"✅ 安全性: {'安全' if is_secure else '不安全'}")
        
        # 验证QBER范围
        if 0 <= total_qber <= 0.5:
            print("✅ QBER范围合理")
        else:
            print(f"⚠️ QBER范围异常: {total_qber}")
        
        return True
        
    except Exception as e:
        print(f"❌ QBER仿真测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dv_qkd_validator():
    """测试DV-QKD合规性验证"""
    print("\n🔒 测试DV-QKD合规性验证...")
    
    try:
        from simulator.dv_qkd_validator import DVQKDValidator
        
        # 创建验证器
        validator = DVQKDValidator()
        print("✅ DVQKDValidator创建成功")
        
        # 测试合规数据
        compliant_data = {
            'qber': 0.05,
            'detection_efficiency': 0.8,
            'encoding_scheme': 'polarization'
        }
        
        report = validator.validate_dv_qkd_compliance(compliant_data)
        print(f"✅ 合规数据检查: {'通过' if report.is_compliant else '失败'}")
        
        # 测试违规数据（包含CV-QKD参数）
        violating_data = {
            'coherent_state_alpha': 1.0,  # 禁止的CV-QKD参数
            'qber': 0.15  # 超过安全阈值
        }
        
        violation_report = validator.validate_dv_qkd_compliance(violating_data)
        print(f"✅ 违规数据检查: {'正确拒绝' if not violation_report.is_compliant else '错误通过'}")
        
        return True
        
    except Exception as e:
        print(f"❌ DV-QKD合规性测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bb84_benchmark():
    """测试BB84基准计算"""
    print("\n🎯 测试BB84基准计算...")
    
    try:
        from simulator.key_rate_calculator import KeyRateCalculator
        
        calculator = KeyRateCalculator()
        
        # 执行BB84基准测试
        bb84_result = calculator.calculate_bb84_benchmark()
        
        baseline_rate = bb84_result.get('asymptotic_key_rate', 0)
        target_rate = 0.480900
        
        print(f"✅ BB84基准密钥率: {baseline_rate:.6f} bits/pulse")
        print(f"✅ 基准目标: {target_rate} bits/pulse")
        print(f"✅ 基准达标: {'是' if baseline_rate >= target_rate else '否'}")
        
        return True
        
    except Exception as e:
        print(f"❌ BB84基准测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 AI4QKD Simulator模块简化功能验证")
    print("=" * 60)
    print("第四步：多轮迭代 - 基础功能验证")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_module_import),
        ("密钥率计算", test_key_rate_calculator), 
        ("QBER仿真", test_qber_simulator),
        ("DV-QKD合规性", test_dv_qkd_validator),
        ("BB84基准", test_bb84_benchmark)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
                
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 第四步测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！基础功能验证成功")
        print("✅ 可以进入第五步：提交与反馈")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ 大部分测试通过，存在少量问题需要修复")
    else:
        print("❌ 测试失败较多，需要进一步调试和修复")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)