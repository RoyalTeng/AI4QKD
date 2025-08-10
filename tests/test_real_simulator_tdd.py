"""
TDD for the Real Quantum Simulator

This file will drive the development of the new, physically accurate
QuantumSimulator using Test-Driven Development (TDD).

We start with the simplest possible case and build up from there.
"""
import sys
import os
import pytest
import numpy as np

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We will import the REAL simulator, but we need to create it first.
# For now, let's assume it will exist at 'simulator.real_quantum_simulator'
# to avoid conflicts with the dummy one.
# We will create this file in the next step.

# Placeholder for now, will be replaced by the actual import
class RealQuantumSimulator:
    def __init__(self, *args, **kwargs): pass
    def simulate_single_pulse(self, *args, **kwargs): return {}

# --- Test Case 1: The Simplest Possible Scenario ---

def test_single_pulse_ideal_scenario():
    """
    TDD Test 1: Ideal Case (No loss, no noise, matching bases)

    Scenario:
    - Alice sends a '0' bit in the Z basis.
    - The channel is perfect (no noise, no loss).
    - Bob measures in the Z basis.

    Expected Outcome:
    - Bob's measurement outcome MUST be '0'.
    """
    # This test will fail initially because RealQuantumSimulator is just a placeholder.
    # Our goal is to write the code that makes this test pass.
    
    # 1. Setup
    # In a real test, we would build a protocol graph. For this first TDD step,
    # we can pass parameters directly to a dedicated method.
    from simulator.real_quantum_simulator import RealQuantumSimulator
    
    simulator = RealQuantumSimulator()
    
    alice_state = {'basis': 'Z', 'bit': 0}
    channel_params = {'loss': 0.0, 'error_rate': 0.0}
    bob_params = {'basis': 'Z'}
    
    # 2. Execution
    # We envision a method that simulates just one pulse for granular testing.
    result = simulator.simulate_single_pulse(alice_state, channel_params, bob_params)
    
    # 3. Assertion
    assert result is not None, "Simulation should return a result dictionary."
    assert result.get('outcome') == 0, "In an ideal Z-basis scenario, Bob must measure 0."
    assert result.get('detected') is True, "In a no-loss scenario, the pulse must be detected."

# --- Test Case 2: Channel with Noise ---

def test_simulation_with_channel_error():
    """
    TDD Test 2: Channel with Depolarizing Noise

    Scenario:
    - Alice and Bob always use matching Z basis.
    - The channel has a 10% depolarizing error rate and no loss.
    - We simulate many pulses.

    Expected Outcome:
    - The final QBER should be approximately 10%.
    """
    from simulator.real_quantum_simulator import RealQuantumSimulator
    simulator = RealQuantumSimulator()
    
    num_pulses = 10000
    error_rate = 0.1
    errors = 0
    
    alice_params = {'basis': 'Z', 'bit': 0} # Alice always sends '0'
    channel_params = {'loss': 0.0, 'error_rate': error_rate}
    bob_params = {'basis': 'Z'}

    for _ in range(num_pulses):
        result = simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
        if result.get('detected') and result.get('outcome') != 0:
            errors += 1
            
    qber = errors / num_pulses
    
    # 物理上，一个错误率为p的退偏振信道导致的QBER大约是 p/2。
    expected_qber = error_rate / 2
    # We assert that the measured QBER is close to the set error_rate.
    # The tolerance (atol) accounts for statistical fluctuations.
    assert np.isclose(qber, expected_qber, atol=0.01), f"Measured QBER {qber} is not close to the expected {expected_qber}"

# --- Test Case 3: Channel with Loss ---

def test_simulation_with_loss():
    """
    TDD Test 3: Channel with Loss but no Noise

    Scenario:
    - Alice and Bob always use matching Z basis.
    - The channel has a 20% loss rate and no noise.
    - We simulate many pulses.

    Expected Outcome:
    - The total detection rate should be approximately 80%.
    - The QBER for all *detected* pulses should be 0.
    """
    from simulator.real_quantum_simulator import RealQuantumSimulator
    simulator = RealQuantumSimulator()
    
    num_pulses = 10000
    loss_rate = 0.2
    
    detected_count = 0
    errors = 0
    
    alice_params = {'basis': 'Z', 'bit': 0}
    channel_params = {'loss': loss_rate, 'error_rate': 0.0}
    bob_params = {'basis': 'Z'}

    for _ in range(num_pulses):
        result = simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
        if result.get('detected'):
            detected_count += 1
            if result.get('outcome') != 0:
                errors += 1
                
    detection_rate = detected_count / num_pulses
    qber = errors / detected_count if detected_count > 0 else 0
    
    # Assert that the detection rate is close to what's expected from loss
    expected_detection_rate = 1.0 - loss_rate
    assert np.isclose(detection_rate, expected_detection_rate, atol=0.01), \
        f"Measured detection rate {detection_rate} is not close to the expected {expected_detection_rate}"
        
    # Assert that for detected bits, there are no errors
    assert qber == 0.0, f"QBER should be 0 in a no-noise scenario, but got {qber}"

# --- Test Case 4: Basis Mismatch ---

def test_basis_mismatch_qber():
    """
    TDD Test 4: Basis Mismatch leading to 50% QBER

    Scenario:
    - The channel is perfect (no noise, no loss).
    - Alice randomly sends in Z or X basis.
    - Bob *always* measures in the opposite basis.

    Expected Outcome:
    - The QBER must be approximately 0.5, as the outcomes will be random.
    """
    from simulator.real_quantum_simulator import RealQuantumSimulator
    simulator = RealQuantumSimulator()
    
    num_pulses = 20000 # More pulses for better statistics
    errors = 0
    
    channel_params = {'loss': 0.0, 'error_rate': 0.0}

    for _ in range(num_pulses):
        alice_basis = np.random.choice(['Z', 'X'])
        alice_bit = np.random.randint(0, 2)
        
        # Bob always chooses the other basis
        bob_basis = 'X' if alice_basis == 'Z' else 'Z'
        
        alice_params = {'basis': alice_basis, 'bit': alice_bit}
        bob_params = {'basis': bob_basis}
        
        result = simulator.simulate_single_pulse(alice_params, channel_params, bob_params)
        
        # We only care about detected results
        if result.get('detected'):
            bob_bit = 1 if result.get('outcome') == 1 or result.get('outcome') == '+' else 0
            if alice_bit != bob_bit:
                errors += 1
                
    # In this specific scenario, all bits are kept for QBER calculation
    qber = errors / num_pulses
    
    expected_qber = 0.5
    assert np.isclose(qber, expected_qber, atol=0.02), \
        f"Measured QBER {qber} for mismatched bases is not close to the expected {expected_qber}" 