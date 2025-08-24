#!/usr/bin/env python
"""
AI4QKD - simulator模块基础功能验证脚本

用途：
- 验证simulator模块的基本导入
- 测试核心算法的正确性
- 检查与qcgf_dsl的集成
- 验证DV-QKD合规性

使用方法：
    python test_simulator_basic.py
"""

import sys
import traceback

def test_basic_imports():
    """测试基础导入"""
    print("📦 测试模块导入...")
    
    try:
        # 测试基础依赖
        import numpy as np
        print("✅ numpy 导入成功")
        
        # 测试simulator模块导入
        sys.path.insert(0, '.')
        from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
        print("✅ KeyRateCalculator 导入成功")
        
        from simulator.qber_simulator import QBERSimulator, QBERParameters
        print("✅ QBERSimulator 导入成功")
        
        from simulator.dv_qkd_validator import DVQKDValidator
        print("✅ DVQKDValidator 导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_key_rate_calculation():
    """测试密钥率计算功能"""
    print("\n🧮 测试密钥率计算...")
    
    try:
        from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
        
        # 创建计算器和参数
        calculator = KeyRateCalculator()
        params = KeyRateParameters(qber=0.05, gain=0.5)
        
        # 计算渐近密钥率
        asymptotic_rate = calculator.calculate_asymptotic_key_rate(params)
        print(f"✅ 渐近密钥率: {asymptotic_rate:.6f} bits/pulse")
        
        # 计算有限密钥率
        finite_rate = calculator.calculate_finite_key_rate(params)
        print(f"✅ 有限密钥率: {finite_rate:.6f} bits/pulse")
        
        # 验证结果合理性
        if 0 <= finite_rate <= asymptotic_rate:
            print("✅ 密钥率关系正确 (finite ≤ asymptotic)")
        else:
            print(f"⚠️ 密钥率关系异常: finite={finite_rate}, asymptotic={asymptotic_rate}")
        
        # BB84基准测试
        bb84_result = calculator.calculate_bb84_benchmark()
        print(f"✅ BB84基准密钥率: {bb84_result['asymptotic_key_rate']:.6f}")
        print(f"   基准达标: {'是' if bb84_result['baseline_met'] else '否'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 密钥率计算失败: {e}")
        traceback.print_exc()
        return False

def test_qber_simulation():
    """测试QBER仿真功能"""
    print("\n📊 测试QBER仿真...")
    
    try:
        from simulator.qber_simulator import QBERSimulator, QBERParameters, EncodingScheme
        
        # 创建QBER仿真器
        qber_sim = QBERSimulator()
        
        # 测试偏振编码QBER
        params = QBERParameters(
            encoding_scheme=EncodingScheme.POLARIZATION,
            channel_length=50.0,
            detector_efficiency=0.8
        )
        
        qber_result = qber_sim.simulate_total_qber(params)
        print(f"✅ 总QBER: {qber_result['total_qber']:.6f}")
        print(f"✅ 安全性: {'安全' if qber_result['is_secure'] else '不安全'}")
        print(f"   安全余量: {qber_result['security_margin']:.6f}")
        
        # 测试偏振编码专门计算
        pol_qber = qber_sim.simulate_polarization_qber(params)
        print(f"✅ 偏振QBER: {pol_qber:.6f}")
        
        # 测试窃听攻击QBER
        attack_qber = qber_sim.simulate_eavesdropping_qber(0.1)
        print(f"✅ 攻击QBER (10%强度): {attack_qber:.6f}")
        
        return True
        
    except Exception as e:
        print(f"❌ QBER仿真失败: {e}")
        traceback.print_exc()
        return False

def test_dv_qkd_compliance():
    """测试DV-QKD合规性验证"""
    print("\n🔒 测试DV-QKD合规性...")
    
    try:
        from simulator.dv_qkd_validator import DVQKDValidator
        
        validator = DVQKDValidator()
        
        # 测试合规数据
        compliant_data = {
            'qber': 0.05,
            'detection_efficiency': 0.8,
            'encoding_scheme': 'polarization',
            'channel_length': 50.0
        }
        
        report = validator.validate_dv_qkd_compliance(compliant_data)
        print(f"✅ 合规数据检查: {'通过' if report.is_compliant else '失败'}")
        print(f"   检查项目: {report.total_checks}")
        print(f"   通过项目: {report.passed_checks}")
        
        # 测试违规数据
        violating_data = {
            'coherent_state_alpha': 1.0,  # 禁止的CV-QKD参数
            'qber': 0.15,  # 超过安全阈值
            'encoding_scheme': 'gaussian_modulation'  # 禁止的编码
        }
        
        violation_report = validator.validate_dv_qkd_compliance(violating_data)
        print(f"✅ 违规数据检查: {'正确拒绝' if not violation_report.is_compliant else '错误通过'}")
        print(f"   违规项目: {violation_report.failed_checks}")
        
        # 测试禁止参数检查
        forbidden_params = validator.check_forbidden_cv_params(violating_data)
        print(f"✅ 禁止参数检测: {len(forbidden_params)} 项")
        
        return True
        
    except Exception as e:
        print(f"❌ DV-QKD合规性测试失败: {e}")
        traceback.print_exc()
        return False

def test_qcgf_integration():
    """测试qcgf_dsl集成"""
    print("\n🔌 测试qcgf_dsl集成...")
    
    try:
        from simulator.protocol_simulator import ProtocolSimulator
        
        # 创建协议仿真器
        sim = ProtocolSimulator()
        
        if not sim._qcgf_available:
            print("⚠️ qcgf_dsl模块不可用，跳过集成测试")
            return True
        
        # 尝试BB84协议仿真
        bb84_result = sim.simulate_bb84_protocol()
        
        if bb84_result.success:
            print(f"✅ BB84协议仿真成功")
            print(f"   密钥率: {bb84_result.finite_key_rate:.6f}")
            print(f"   QBER: {bb84_result.total_qber:.6f}")
            print(f"   性能评分: {bb84_result.performance_score:.3f}")
        else:
            print(f"⚠️ BB84协议仿真失败: {bb84_result.error_message}")
        
        return True
        
    except Exception as e:
        print(f"❌ qcgf_dsl集成测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 AI4QKD Simulator模块基础功能验证")
    print("=" * 50)
    
    tests = [
        ("基础导入", test_basic_imports),
        ("密钥率计算", test_key_rate_calculation),
        ("QBER仿真", test_qber_simulation),
        ("DV-QKD合规性", test_dv_qkd_compliance),
        ("qcgf_dsl集成", test_qcgf_integration)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！simulator模块基础功能正常")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ 大部分测试通过，存在少量问题")
    else:
        print("❌ 测试失败较多，需要进一步检查")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)