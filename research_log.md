# AI4QKD研究日志

## 实验记录模板

### 实验基本信息
- **实验编号**: 
- **实验日期**: 2026-03-30
- **实验目的**: 
- **实验人员**: 滕俊

### 实验设置
```python
# 协议设置
协议类型: BB84
协议参数: {}

# 仿真设置
仿真器: QuantumSimulator
脉冲数: 10000
噪声参数:
  - 信道损耗: 0.1
  - 探测器效率: 0.9
  - 暗计数率: 1e-6

# AI设置
智能体: HybridAgent
迭代次数: 50
种群大小: 10
```

### 实验结果
#### 1. 基础性能
```
QBER: 
Gain: 
原始密钥率: 
仿真时间: 
```

#### 2. AI设计结果
```
最佳适应度: 
协议名称: 
节点统计: {}
```

#### 3. 关键发现
1. 
2. 
3. 

### 数据分析
#### 性能趋势
- QBER随信道损耗的变化:
- Gain随探测器效率的变化:

#### 协议比较
| 协议类型 | QBER | Gain | 密钥率 | 备注 |
|---------|------|------|--------|------|
| BB84 | | | | |
| AI设计 | | | | |

### 结论与建议
#### 主要结论
1. 
2. 
3. 

#### 后续研究方向
1. 
2. 
3. 

### 附件
- 协议文件: `results/xxx_protocol.json`
- 结果文件: `results/xxx_result.json`
- 可视化图: `results/xxx_visualization.png`

---

## 快速实验命令

### 1. 运行基础实验
```bash
python3 examples/bb84_example.py
```

### 2. 运行AI设计实验
```bash
python3 -c "
from ai_agent import HybridAgent
agent = HybridAgent()
result = agent.train(iterations=30)
print(f'最佳适应度: {result[\"best_fitness\"]:.4f}')
"
```

### 3. 参数扫描实验
```bash
python3 -c "
import numpy as np
from qcgf_dsl import ProtocolGraph
from simulator import QuantumSimulator

loss_values = np.linspace(0.05, 0.3, 6)
for loss in loss_values:
    protocol = ProtocolGraph.create_bb84()
    simulator = QuantumSimulator(channel_loss=loss)
    result = simulator.simulate(protocol, 5000)
    print(f'损耗={loss:.2f}: QBER={result.qber:.4f}, Gain={result.gain:.4f}')
"
```

## 研究计划

### 本周目标
- [ ] 完成BB84协议性能分析
- [ ] 实现E91协议
- [ ] 完成AI协议设计实验
- [ ] 撰写初步研究报告

### 本月目标
- [ ] 开发协议可视化工具
- [ ] 实现深度强化学习智能体
- [ ] 完成安全性分析模块
- [ ] 发表研究论文初稿

## 重要发现记录

### 2026-03-30
- 项目成功创建并运行
- BB84协议基础仿真正常
- AI智能体基本功能正常
- 结果保存系统工作正常