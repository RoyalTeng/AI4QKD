# BB84协议基准记录

## 测试时间
- 执行时间: 2025-07-14 23:xx:xx
- 测试脚本: `bb84_benchmark.py`

## 基准性能指标
- **BB84安全密钥率: 0.480900 bits/pulse** ⭐ **这是我们要超越的目标**
- 增益 (Gain): 0.7200
- 量子比特错误率 (QBER): 0.0222

## 固定物理参数 (来自 config/qkd_protocols.py)

### 量子态制备 (QSP) 参数
```python
'qsp': {
    'num_states': 100000,
    'basis_choice': ['Z', 'X'],
}
```

### 量子信道 (QC) 参数
```python
'qc': {
    'loss': 0.1,        # 10% 信道损耗
    'error_rate': 0.02, # 2% 信道错误率 (退偏振)
}
```

### 量子测量 (QM) 参数  
```python
'qm': {
    'basis_choice': ['Z', 'X'],
    'efficiency': 0.8, # 80% 探测效率
}
```

### 安全性评估参数
```python
'security': {
    'protocol_type': 'BB84',
    'params': {'p_signal': 1.0, 'leakage': 0.01}
}
```

## 计算得出的中间指标
- 信道损耗: 0.1000 (10%)
- 探测器效率: 0.8000 (80%) 
- 信道错误率: 0.0200 (2%)

## 协议图结构
- 协议名称: 'BB84_Benchmark'
- 节点数: 3 (Alice_QSP, QuantumChannel, Bob_QM)
- 边数: 2 (Alice_QSP -> QuantumChannel -> Bob_QM)
- 拓扑结构: 线性DAG (有向无环图)

## 性能标杆 (Benchmark Target)
**任何新协议必须在相同物理参数下实现：**
**KeyRate(P_new) > 0.480900 bits/pulse**

## 备注
- 使用了简化的密钥率计算方法（由于某些依赖包尚未完全安装）
- 基本的二元熵函数计算工作正常
- 协议图创建和基本仿真功能验证成功