#!/usr/bin/env python3
"""
BB84协议基准测试 - 简化版本
用于建立性能标杆，避免复杂依赖问题
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# 使用最基础的模块来避免依赖问题
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party
from config.qkd_protocols import BB84_PARAMS
from security_evaluator.key_rate_calculator import KeyRateCalculator
from security_evaluator.ac_framework import ProtocolType

def create_bb84_protocol_graph():
    """根据配置创建BB84协议图"""
    graph = ProtocolGraph(name="BB84_Benchmark")
    
    # 添加节点
    alice_qsp = graph.add_node(
        node_type=NodeType.QSP, 
        params=BB84_PARAMS['qsp'], 
        party=Party.ALICE,
        node_id="Alice_QSP"
    )
    
    qc = graph.add_node(
        node_type=NodeType.QC,
        params=BB84_PARAMS['qc'],
        node_id="QuantumChannel"
    )
    
    bob_qm = graph.add_node(
        node_type=NodeType.QM,
        params=BB84_PARAMS['qm'],
        party=Party.BOB,
        node_id="Bob_QM"
    )
    
    # 添加边
    graph.add_edge(alice_qsp, qc)
    graph.add_edge(qc, bob_qm)
    
    return graph

def simulate_bb84_simplified():
    """简化的BB84仿真，计算基础性能指标"""
    # 从配置获取物理参数
    qc_params = BB84_PARAMS['qc']
    qm_params = BB84_PARAMS['qm']
    
    # 计算基础性能指标
    channel_loss = qc_params['loss']  # 0.1 (10%)
    channel_error = qc_params['error_rate']  # 0.02 (2%)
    detector_efficiency = qm_params['efficiency']  # 0.8 (80%)
    
    # 简化的增益计算：考虑信道损耗和探测器效率
    gain = (1 - channel_loss) * detector_efficiency
    
    # 简化的QBER计算：主要来自信道错误
    qber = channel_error / (1 - channel_loss)  # 考虑信道损耗的影响
    
    return {
        'gain': gain,
        'qber': qber,
        'channel_loss': channel_loss,
        'detector_efficiency': detector_efficiency,
        'channel_error_rate': channel_error
    }

def calculate_bb84_key_rate(qber, gain):
    """计算BB84安全密钥率"""
    try:
        # 使用项目的密钥率计算器
        calculator = KeyRateCalculator(
            qber=qber,
            gain=gain,
            protocol_type=ProtocolType.BB84,
            params={'n_pulses': 100000}  # 默认脉冲数
        )
        
        key_rate = calculator.calculate_key_rate()
        return key_rate
        
    except Exception as e:
        print(f"密钥率计算出错: {e}")
        # 使用简化的安全密钥率估算
        # R ≈ Gain * [1 - h(QBER)] - f_ec * h(QBER)
        import math
        
        if qber <= 0 or qber >= 0.5:
            return 0.0
            
        # 二元熵函数
        h_qber = -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber)
        
        # 简化的密钥率公式
        f_ec = 1.16  # 纠错效率因子
        key_rate = gain * (1 - h_qber) - gain * f_ec * h_qber
        
        return max(0.0, key_rate)

def main():
    """主函数：运行BB84基准测试"""
    print("=== BB84协议基准测试 ===")
    
    # 1. 创建协议图
    protocol_graph = create_bb84_protocol_graph()
    print(f"协议图 '{protocol_graph.name}' 创建完成")
    print(f"节点数: {protocol_graph.get_node_count()}")
    print(f"边数: {protocol_graph.get_edge_count()}")
    
    # 2. 运行简化仿真
    sim_results = simulate_bb84_simplified()
    print(f"\n=== 仿真结果 ===")
    print(f"增益 (Gain): {sim_results['gain']:.4f}")
    print(f"量子比特错误率 (QBER): {sim_results['qber']:.4f}")
    print(f"信道损耗: {sim_results['channel_loss']:.4f}")
    print(f"探测器效率: {sim_results['detector_efficiency']:.4f}")
    print(f"信道错误率: {sim_results['channel_error_rate']:.4f}")
    
    # 3. 计算安全密钥率
    key_rate = calculate_bb84_key_rate(sim_results['qber'], sim_results['gain'])
    print(f"\n=== 安全性分析 ===")
    print(f"BB84安全密钥率: {key_rate:.6f} bits/pulse")
    
    # 4. 记录基准
    benchmark = {
        'protocol': 'BB84',
        'gain': sim_results['gain'],
        'qber': sim_results['qber'],
        'key_rate': key_rate,
        'physical_params': {
            'channel_loss': sim_results['channel_loss'],
            'detector_efficiency': sim_results['detector_efficiency'],
            'channel_error_rate': sim_results['channel_error_rate']
        }
    }
    
    return benchmark

if __name__ == "__main__":
    benchmark_result = main()
    print(f"\n=== 基准建立完成 ===")
    print(f"BB84基准密钥率: {benchmark_result['key_rate']:.6f} bits/pulse")