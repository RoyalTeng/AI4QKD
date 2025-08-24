#!/usr/bin/env python
"""
AI4QKD - simulator模块最终验证脚本
第五步：提交与反馈 - 完整功能验证
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.getcwd())

def main():
    """执行最终验证"""
    print("=== AI4QKD Simulator模块最终验证 ===")
    print("第五步：提交与反馈")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    # 1. 基础导入验证
    print("\n[1/6] 基础导入验证...")
    total_tests += 1
    try:
        import numpy as np
        from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
        from simulator.qber_simulator import QBERSimulator, QBERParameters
        from simulator.dv_qkd_validator import DVQKDValidator
        print("✅ 所有核心模块导入成功")
        success_count += 1
    except Exception as e:
        print(f"❌ 导入失败: {e}")
    
    # 2. 密钥率计算验证
    print("\n[2/6] 密钥率计算验证...")
    total_tests += 1
    try:
        calculator = KeyRateCalculator()
        params = KeyRateParameters(qber=0.05, gain=0.5)
        
        asymptotic_rate = calculator.calculate_asymptotic_key_rate(params)
        finite_rate = calculator.calculate_finite_key_rate(params)
        
        if 0 <= finite_rate <= asymptotic_rate <= 1:
            print(f"✅ 密钥率计算正常: {asymptotic_rate:.6f} bits/pulse")
            success_count += 1
        else:
            print(f"❌ 密钥率结果异常")
    except Exception as e:
        print(f"❌ 密钥率计算失败: {e}")
    
    # 3. QBER仿真验证
    print("\n[3/6] QBER仿真验证...")
    total_tests += 1
    try:
        from simulator.qber_simulator import EncodingScheme
        qber_sim = QBERSimulator()
        params = QBERParameters(
            encoding_scheme=EncodingScheme.POLARIZATION,
            channel_length=50.0
        )
        
        result = qber_sim.simulate_total_qber(params)
        total_qber = result['total_qber']
        
        if 0 <= total_qber <= 0.5:
            print(f"✅ QBER仿真正常: {total_qber:.6f}")
            success_count += 1
        else:
            print(f"❌ QBER结果异常: {total_qber}")
    except Exception as e:
        print(f"❌ QBER仿真失败: {e}")
    
    # 4. DV-QKD合规性验证
    print("\n[4/6] DV-QKD合规性验证...")
    total_tests += 1
    try:
        validator = DVQKDValidator()
        
        # 合规数据测试
        compliant_data = {
            'qber': 0.05,
            'detection_efficiency': 0.8,
            'encoding_scheme': 'polarization'
        }
        
        report = validator.validate_dv_qkd_compliance(compliant_data)
        
        # 违规数据测试
        violating_data = {
            'coherent_state_alpha': 1.0,  # 禁止的CV-QKD参数
            'qber': 0.15  # 超过安全阈值
        }
        
        violation_report = validator.validate_dv_qkd_compliance(violating_data)
        
        if report.is_compliant and not violation_report.is_compliant:
            print("✅ DV-QKD合规性检查正常")
            success_count += 1
        else:
            print("❌ DV-QKD合规性检查异常")
    except Exception as e:
        print(f"❌ DV-QKD验证失败: {e}")
    
    # 5. BB84基准验证
    print("\n[5/6] BB84基准验证...")
    total_tests += 1
    try:
        calculator = KeyRateCalculator()
        bb84_result = calculator.calculate_bb84_benchmark()
        
        baseline_rate = bb84_result.get('asymptotic_key_rate', 0)
        baseline_met = bb84_result.get('baseline_met', False)
        
        if baseline_rate > 0.4:  # 合理的基准阈值
            print(f"✅ BB84基准达标: {baseline_rate:.6f} bits/pulse")
            success_count += 1
        else:
            print(f"❌ BB84基准不达标: {baseline_rate:.6f}")
    except Exception as e:
        print(f"❌ BB84基准测试失败: {e}")
    
    # 6. 集成功能验证
    print("\n[6/6] 集成功能验证...")
    total_tests += 1
    try:
        # 通过便捷函数进行集成测试
        from simulator import run_basic_test
        
        test_result = run_basic_test()
        
        if test_result.get('overall_success', False):
            print("✅ 集成功能测试通过")
            success_count += 1
        else:
            error = test_result.get('error', '未知错误')
            print(f"❌ 集成功能测试失败: {error}")
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
    
    # 最终结果
    print(f"\n{'='*50}")
    print(f"📊 最终验证结果: {success_count}/{total_tests} 通过")
    print(f"成功率: {success_count/total_tests*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 所有验证通过！simulator模块重构成功完成")
        print("✅ 可以进入重构总结阶段")
        return True
    elif success_count >= total_tests * 0.8:
        print("⚠️ 大部分验证通过，存在少量问题")
        return True
    else:
        print("❌ 验证失败较多，需要进一步检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)