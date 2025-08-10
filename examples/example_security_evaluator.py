"""
安全性评估器使用示例

演示如何使用security_evaluator模块进行QKD协议的安全性评估
"""

import logging
from security_evaluator.key_rate_calculator import KeyRateCalculator, ProtocolType

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    """主函数"""
    print("=== AI辅助QKD协议设计系统 - 安全性评估器示例 ===\n")
    
    # 创建密钥率计算器
    calculator = KeyRateCalculator()
    
    # 示例1: BB84协议密钥率计算
    print("示例1: BB84协议密钥率计算")
    print("-" * 40)
    
    # 参数设置
    qber = 0.02  # 量子比特错误率 2%
    gain = 0.1   # 信道增益 10%
    n_pulses = int(1e9)  # 发送脉冲数量 10^9
    
    # 计算BB84协议密钥率
    bb84_result = calculator.compute(qber, gain, n_pulses, ProtocolType.BB84)
    
    print(f"输入参数:")
    print(f"  QBER: {qber:.3f}")
    print(f"  增益: {gain:.3f}")
    print(f"  脉冲数: {n_pulses:,}")
    print()
    print(f"计算结果:")
    print(f"  最终密钥率: {bb84_result.final_key_rate:.6f} bit/pulse")
    print(f"  最终密钥长度: {bb84_result.final_key_length:,}")
    print(f"  最小熵 H_min: {bb84_result.h_min:.6f}")
    print(f"  纠错泄露: {bb84_result.leak_ec:.6f}")
    print(f"  参数估计泄露: {bb84_result.leak_pe:.6f}")
    print(f"  安全密钥泄露: {bb84_result.leak_sk:.6f}")
    print(f"  秘密密钥率: {bb84_result.secret_key_rate:.6f}")
    print()
    
    # 示例2: 诱骗态BB84协议密钥率计算
    print("示例2: 诱骗态BB84协议密钥率计算")
    print("-" * 40)
    
    # 计算诱骗态BB84协议密钥率
    decoy_result = calculator.compute(qber, gain, n_pulses, ProtocolType.DECOY_BB84)
    
    print(f"输入参数:")
    print(f"  QBER: {qber:.3f}")
    print(f"  增益: {gain:.3f}")
    print(f"  脉冲数: {n_pulses:,}")
    print(f"  信号态强度: {decoy_result.parameters.mu_signal:.3f}")
    print(f"  诱骗态1强度: {decoy_result.parameters.mu_decoy1:.3f}")
    print(f"  诱骗态2强度: {decoy_result.parameters.mu_decoy2:.3f}")
    print()
    print(f"计算结果:")
    print(f"  最终密钥率: {decoy_result.final_key_rate:.6f} bit/pulse")
    print(f"  最终密钥长度: {decoy_result.final_key_length:,}")
    print(f"  最小熵 H_min: {decoy_result.h_min:.6f}")
    print(f"  纠错泄露: {decoy_result.leak_ec:.6f}")
    print(f"  参数估计泄露: {decoy_result.leak_pe:.6f}")
    print(f"  安全密钥泄露: {decoy_result.leak_sk:.6f}")
    print(f"  秘密密钥率: {decoy_result.secret_key_rate:.6f}")
    print()
    
    # 示例3: 协议比较
    print("示例3: 协议性能比较")
    print("-" * 40)
    
    # 比较不同协议
    comparison = calculator.compare_protocols(qber, gain, n_pulses)
    
    print("协议性能比较:")
    for protocol, result in comparison.items():
        if result is not None:
            print(f"  {protocol.value}:")
            print(f"    密钥率: {result.final_key_rate:.6f} bit/pulse")
            print(f"    密钥长度: {result.final_key_length:,}")
            print(f"    效率: {result.final_key_rate/gain:.3f}")
    
    print()
    
    # 示例4: 参数敏感性分析
    print("示例4: 参数敏感性分析")
    print("-" * 40)
    
    # 分析QBER对密钥率的影响
    qber_range = [0.01, 0.02, 0.03, 0.04, 0.05]
    print("QBER对密钥率的影响:")
    print("  QBER    | BB84密钥率 | 诱骗态密钥率")
    print("  --------|------------|-------------")
    
    for qber_test in qber_range:
        try:
            bb84_rate = calculator.compute(qber_test, gain, n_pulses, ProtocolType.BB84).final_key_rate
            decoy_rate = calculator.compute(qber_test, gain, n_pulses, ProtocolType.DECOY_BB84).final_key_rate
            print(f"  {qber_test:.3f}   | {bb84_rate:.6f}    | {decoy_rate:.6f}")
        except Exception as e:
            print(f"  {qber_test:.3f}   | 计算失败     | 计算失败")
    
    print()
    
    # 示例5: 不同信道条件下的性能
    print("示例5: 不同信道条件下的性能")
    print("-" * 40)
    
    # 测试不同增益下的性能
    gain_range = [0.05, 0.1, 0.15, 0.2]
    print("增益对密钥率的影响:")
    print("  增益   | BB84密钥率 | 诱骗态密钥率")
    print("  -------|------------|-------------")
    
    for gain_test in gain_range:
        try:
            bb84_rate = calculator.compute(qber, gain_test, n_pulses, ProtocolType.BB84).final_key_rate
            decoy_rate = calculator.compute(qber, gain_test, n_pulses, ProtocolType.DECOY_BB84).final_key_rate
            print(f"  {gain_test:.3f}  | {bb84_rate:.6f}    | {decoy_rate:.6f}")
        except Exception as e:
            print(f"  {gain_test:.3f}  | 计算失败     | 计算失败")
    
    print()
    
    # 总结
    print("=== 总结 ===")
    print("1. BB84协议在低QBER条件下表现较好，密钥率较高")
    print("2. 诱骗态BB84协议提供更好的安全性，但密钥率较低")
    print("3. 信道增益直接影响最终密钥率")
    print("4. QBER是影响密钥率的关键参数")
    print("5. 有限密钥效应在短密钥长度时显著影响性能")
    
    print("\n=== 示例完成 ===")

if __name__ == "__main__":
    main() 