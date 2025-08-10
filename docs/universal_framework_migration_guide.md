# AI4QKD 通用框架迁移指南

## 概述

AI4QKD v2.0 引入了全新的通用抽象密码学框架，基于现代量子信息论提供更强大、更灵活的协议分析能力。本指南将帮助您从传统的硬编码协议类型迁移到新的通用框架。

## 主要变化

### 1. 从硬编码协议类型到通用协议特征

**旧方式**：
```python
from security_evaluator.ac_framework import ProtocolType
protocol_type = ProtocolType.BB84
```

**新方式**：
```python
from security_evaluator.universal_framework import create_bb84_protocol
protocol_features = create_bb84_protocol()
```

### 2. 从基础安全参数到通用安全参数

**旧方式**：
```python
from security_evaluator.ac_framework import SecurityParameters
params = SecurityParameters(epsilon_sec=1e-10)
```

**新方式**：
```python
from security_evaluator.universal_framework import UniversalSecurityParameters
params = UniversalSecurityParameters(
    epsilon_sec=1e-10,
    entropy_smoothing_param=1e-8,
    composability_param=1e-7
)
```

### 3. 从特定协议分析到通用安全框架

**旧方式**：
```python
# 需要针对每种协议编写特定代码
if protocol_type == ProtocolType.BB84:
    # BB84 特定逻辑
elif protocol_type == ProtocolType.MDI_QKD:
    # MDI-QKD 特定逻辑
```

**新方式**：
```python
from security_evaluator.universal_framework import UniversalSecurityFramework

framework = UniversalSecurityFramework()
result = framework.analyze_protocol_security(
    protocol_features=any_protocol,
    experimental_data=data
)
```

## 详细迁移步骤

### 步骤 1: 更新导入语句

```python
# 旧的导入（仍然可用，但会显示弃用警告）
from security_evaluator.ac_framework import ProtocolType, SecurityParameters

# 新的导入（推荐）
from security_evaluator.universal_framework import (
    UniversalSecurityParameters,
    UniversalSecurityFramework,
    ProtocolFeatures,
    QuantumOperation,
    create_bb84_protocol,
    create_mdi_qkd_protocol,
    create_decoy_bb84_protocol
)
```

### 步骤 2: 迁移协议定义

#### BB84 协议

**旧方式**：
```python
protocol_type = ProtocolType.BB84
```

**新方式**：
```python
protocol_features = create_bb84_protocol()
# 或者自定义
protocol_features = ProtocolFeatures(
    name="Custom_BB84",
    operations=[
        QuantumOperation("state_prep", "preparation"),
        QuantumOperation("quantum_channel", "channel"),
        QuantumOperation("measurement", "measurement")
    ],
    parties=['Alice', 'Bob'],
    measurement_bases=2
)
```

#### MDI-QKD 协议

**旧方式**：
```python
protocol_type = ProtocolType.MDI_QKD
```

**新方式**：
```python
protocol_features = create_mdi_qkd_protocol()
# 访问协议特征
print(f"Trusted parties: {protocol_features.trusted_parties}")
print(f"Untrusted parties: {protocol_features.untrusted_parties}")
```

#### 诱骗态协议

**旧方式**：
```python
protocol_type = ProtocolType.DECOY_BB84
```

**新方式**：
```python
protocol_features = create_decoy_bb84_protocol()
# 检查协议特征
features = protocol_features.calculate_information_theoretic_features()
print(f"Uses decoy states: {features['uses_decoy_states']}")
```

### 步骤 3: 迁移安全参数

**旧方式**：
```python
params = SecurityParameters(
    epsilon_sec=1e-9,
    epsilon_cor=1e-15,
    epsilon_rob=1e-9
)
```

**新方式**：
```python
params = UniversalSecurityParameters(
    # 保持向后兼容的参数
    epsilon_sec=1e-9,
    epsilon_cor=1e-15,
    epsilon_rob=1e-9,
    # 新的通用参数
    entropy_smoothing_param=1e-8,
    composability_param=1e-7,
    device_independence_param=1e-6
)

# 计算信息论界限
bounds = params.calculate_information_theoretic_bounds(
    min_entropy=0.5,
    mutual_information=0.3,
    protocol_rounds=100
)
```

### 步骤 4: 迁移安全性分析

**旧方式**：
```python
from security_evaluator.key_rate_calculator import KeyRateCalculator

calculator = KeyRateCalculator()
result = calculator.compute(
    qber=0.05,
    gain=0.1,
    n_pulses=100000,
    protocol_type=ProtocolType.BB84
)
```

**新方式**：
```python
framework = UniversalSecurityFramework()

experimental_data = {
    'qber': 0.05,
    'gain': 0.1,
    'n_pulses': 100000
}

security_result = framework.analyze_protocol_security(
    protocol_features=protocol_features,
    experimental_data=experimental_data,
    security_params=params
)

print(f"Key rate: {security_result['key_rate']}")
print(f"Security parameter: {security_result['security_parameter']}")
```

## 新功能特性

### 1. 熵累积分析

```python
# 多轮协议数据
rounds_data = [
    {'round': i, 'qber': 0.02 + 0.001*i, 'measurements': data_i}
    for i in range(10)
]

entropy_result = framework.apply_entropy_accumulation(rounds_data)
print(f"Accumulated entropy: {entropy_result['accumulated_entropy']}")
```

### 2. 可组合安全性分析

```python
protocol_instances = [
    {'protocol_id': 'instance_1', 'epsilon': 1e-10},
    {'protocol_id': 'instance_2', 'epsilon': 1e-11},
]

composability_result = framework.analyze_composable_security(protocol_instances)
print(f"Is composable secure: {composability_result['is_composable_secure']}")
```

### 3. 设备无关安全性

```python
di_data = {
    'bell_violation': 2.4,
    'detection_efficiency': 0.8,
    'measurement_statistics': {'00': 0.25, '01': 0.25, '10': 0.25, '11': 0.25}
}

di_result = framework.analyze_device_independent_security(di_data)
print(f"Device independence certified: {di_result['device_independence_certified']}")
```

### 4. 自定义协议分析

```python
# 创建自定义协议
custom_protocol = ProtocolFeatures(
    name="Novel_QKD_Protocol",
    operations=[
        QuantumOperation("custom_preparation", "preparation"),
        QuantumOperation("novel_channel", "channel"),
        QuantumOperation("advanced_measurement", "measurement")
    ],
    parties=['Alice', 'Bob', 'Eve'],
    communication_rounds=3,
    measurement_bases=4,
    device_independence=True
)

# 分析自定义协议
custom_features = custom_protocol.calculate_information_theoretic_features()
custom_result = framework.analyze_protocol_security(custom_protocol, experimental_data)
```

## 向后兼容性

### 自动迁移

如果您需要继续使用旧的代码，框架提供了自动迁移功能：

```python
# 旧代码仍然可用
from security_evaluator.ac_framework import ProtocolType, SecurityParameters

old_protocol = ProtocolType.BB84  # 会显示弃用警告
old_params = SecurityParameters()

# 自动转换到新格式
new_protocol = old_protocol.to_protocol_features()
new_params = old_params.to_universal_parameters()
```

### 渐进式迁移

您可以渐进式迁移：

```python
# 第一步：使用新的安全参数，保持旧的协议类型
from security_evaluator.ac_framework import ProtocolType
from security_evaluator.universal_framework import UniversalSecurityParameters

protocol_type = ProtocolType.BB84
params = UniversalSecurityParameters()

# 第二步：完全迁移到新框架
protocol_features = create_bb84_protocol()
framework = UniversalSecurityFramework()
```

## 性能优势

### 1. 更快的协议分析

新框架避免了硬编码的 if-else 逻辑，使用统一的分析管道：

```python
# 旧方式：需要为每种协议编写特定代码
def analyze_protocol(protocol_type, data):
    if protocol_type == ProtocolType.BB84:
        return analyze_bb84(data)
    elif protocol_type == ProtocolType.MDI_QKD:
        return analyze_mdi_qkd(data)
    # ...

# 新方式：统一的分析管道
result = framework.analyze_protocol_security(any_protocol, data)
```

### 2. 更准确的安全性评估

基于现代量子信息论的精确计算：

- 熵累积定理应用
- 平滑最小熵计算
- 有限密钥精确分析
- 可组合安全性保证

### 3. 更好的扩展性

添加新协议无需修改现有代码：

```python
# 定义新协议
def create_novel_protocol():
    return ProtocolFeatures(
        name="Novel_Protocol",
        operations=[...],
        parties=[...],
        # 新的协议特性
        novel_feature=True
    )

# 立即可用于分析
novel_protocol = create_novel_protocol()
result = framework.analyze_protocol_security(novel_protocol, data)
```

## 故障排除

### 常见问题

1. **ImportError: No module named 'universal_framework'**
   
   确保您正在使用最新版本的 AI4QKD：
   ```bash
   git pull origin main
   pip install -e .
   ```

2. **DeprecationWarning: ProtocolType is deprecated**
   
   这是正常的迁移警告。更新您的代码以使用 `ProtocolFeatures`。

3. **TypeError: unexpected keyword argument**
   
   检查您是否混用了旧和新的参数名称。参考迁移示例更新代码。

### 获得帮助

- 查看 `tests/test_universal_ac_framework.py` 中的示例用法
- 阅读 `security_evaluator/universal_framework.py` 中的文档字符串
- 运行 `pytest tests/test_universal_ac_framework.py -v` 验证安装

## 迁移检查清单

- [ ] 更新导入语句
- [ ] 将 `ProtocolType` 替换为 `ProtocolFeatures`
- [ ] 将 `SecurityParameters` 升级为 `UniversalSecurityParameters`
- [ ] 使用 `UniversalSecurityFramework` 进行安全性分析
- [ ] 测试新功能（熵累积、可组合安全性等）
- [ ] 更新测试用例
- [ ] 验证结果一致性

## 总结

新的通用框架提供了：

✅ **协议无关性**: 统一处理任意协议结构  
✅ **现代理论**: 基于最新量子密码学研究  
✅ **向后兼容**: 现有代码继续工作  
✅ **扩展性**: 轻松添加新协议和安全分析  
✅ **精确性**: 更准确的安全性评估  

通过逐步迁移，您将获得更强大、更灵活的量子密码协议分析能力，同时保持代码的稳定性和可维护性。