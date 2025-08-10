import numpy as np
import pytest
from simulator import (
    QuantumSimulator, StatePreparation, ChannelModel, Measurement,
    PerformanceMetrics, NoiseModel, QiskitInterface
)
from qiskit import QuantumCircuit


def test_state_preparation():
    sp = StatePreparation()
    wcp = sp.prepare_wcp_state()
    assert isinstance(wcp, dict)
    decoy = sp.prepare_decoy_state()
    assert isinstance(decoy, dict)
    stats = sp.get_photon_statistics(wcp)
    assert 'mean_photon_number' in stats
    state1 = {'state_vector': np.array([1, 0])}
    state2 = {'state_vector': np.array([1, 0])}
    fid = sp.calculate_fidelity(state1, state2)
    assert np.isclose(fid, 1.0)

def test_channel_model():
    cm = ChannelModel(fiber_length=10)
    state_dict = {'density_matrix': np.eye(2)}
    channel_params = {'attenuation_coefficient': 0.2}
    out = cm.simulate_channel_transmission(state_dict, channel_params)
    assert isinstance(out, dict)

def test_measurement():
    meas = Measurement()
    state_dm = np.array([[1, 0], [0, 0]])
    meas._measurement_bases['Z'] = {
        '0': np.outer(np.array([1,0]), np.array([1,0])), 
        '1': np.outer(np.array([0,1]), np.array([0,1]))
    }
    res = meas.projective_measurement(state_dm, basis='Z')
    assert isinstance(res, dict)
    assert 'outcome' in res
    measurement_list = [{'outcome': 0}, {'outcome': 1}, {'outcome': 0}, {'outcome': 1}]
    stats = meas.calculate_measurement_statistics(measurement_list)
    assert 'outcome_distribution' in stats
    assert 0 in stats['outcome_distribution']
    assert 1 in stats['outcome_distribution']
    qber = meas.calculate_quantum_bit_error_rate([0, 1, 0, 1], [0, 0, 1, 1])
    assert 0 <= qber <= 1

def test_performance_metrics():
    pm = PerformanceMetrics()
    qber_val = 0.05
    gain_val = 0.9
    key_rate_val = pm.calculate_secret_key_rate(qber=qber_val, gain=gain_val)
    assert key_rate_val >= 0
    perf_data = {"qber": qber_val, "gain": gain_val, "key_rate": key_rate_val}
    report = pm.generate_performance_report(perf_data)
    assert isinstance(report, str)

def test_noise_model():
    nm = NoiseModel(dephasing_rate=0.1, amplitude_damping_rate=0.05, phase_noise_std=0.01)
    state = np.eye(2)
    out = nm.apply_all(state)
    assert isinstance(out, np.ndarray)

def test_qiskit_interface():
    qi = QiskitInterface()
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    counts = qi.run_circuit(qc, shots=100)
    assert isinstance(counts, dict)

def test_quantum_simulator_basic():
    sim = QuantumSimulator()
    assert hasattr(sim, 'simulate_protocol_graph')
    assert hasattr(sim, 'get_performance_report') 