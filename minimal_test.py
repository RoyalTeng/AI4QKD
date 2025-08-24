import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.getcwd())

print("Testing simulator module...")

try:
    print("1. Testing numpy...")
    import numpy as np
    print("   [OK] numpy imported successfully")
    
    print("2. Testing key_rate_calculator...")
    from simulator.key_rate_calculator import KeyRateCalculator, KeyRateParameters
    print("   [OK] KeyRateCalculator imported")
    
    calculator = KeyRateCalculator()
    print("   [OK] KeyRateCalculator instantiated")
    
    params = KeyRateParameters(qber=0.05, gain=0.5)
    print("   [OK] KeyRateParameters created")
    
    rate = calculator.calculate_asymptotic_key_rate(params)
    print(f"   [OK] Asymptotic key rate: {rate:.6f}")
    
    print("3. Testing qber_simulator...")
    from simulator.qber_simulator import QBERSimulator, QBERParameters
    print("   [OK] QBERSimulator imported")
    
    qber_sim = QBERSimulator()
    qber_params = QBERParameters(channel_length=50.0)
    qber_result = qber_sim.simulate_total_qber(qber_params)
    print(f"   [OK] QBER simulation: {qber_result['total_qber']:.6f}")
    
    print("4. Testing dv_qkd_validator...")
    from simulator.dv_qkd_validator import DVQKDValidator
    validator = DVQKDValidator()
    test_data = {'qber': 0.05}
    report = validator.validate_dv_qkd_compliance(test_data)
    print(f"   [OK] DV-QKD compliance: {report.is_compliant}")
    
    print("\n[SUCCESS] All tests passed!")
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()