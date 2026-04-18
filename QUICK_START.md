# 🚀 AI4QKD快速启动指南

## 📋 项目概述

这是一个**从头开始开发**的AI4QKD项目，实现了AI辅助量子密钥分发协议设计的完整框架。

## 🎯 核心功能

### 已实现功能
1. **📊 QCGF DSL**：量子-经典图流领域特定语言
   - 协议图表示
   - 节点类型系统（12种节点）
   - 参与者系统（Alice、Bob等）
   - 预定义协议（BB84）

2. **⚛️ 量子仿真器**：基础量子物理仿真
   - QBER（量子比特错误率）计算
   - 增益计算
   - 密钥率估算
   - 可配置噪声参数

3. **🤖 AI智能体**：混合智能体
   - 演化算法基础
   - 协议适应度评估
   - 协议设计和优化
   - 简单训练框架

4. **🛠️ 完整工具链**
   - 一键设置脚本
   - 示例代码
   - 测试套件
   - 可视化工具

## 🚀 5分钟快速开始

### 步骤1：运行设置脚本
```bash
# 在AI4QKD目录中运行
python setup.py
```

脚本会自动：
- ✅ 检查Python环境
- ✅ 创建虚拟环境
- ✅ 安装核心依赖（numpy, scipy, networkx）
- ✅ 创建项目目录
- ✅ 运行基础测试

### 步骤2：运行示例
```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 运行BB84示例
python examples/bb84_example.py
```

### 步骤3：验证安装
```bash
# 运行基础测试
python test_basic.py
```

## 🎮 使用示例

### 示例1：创建和仿真BB84协议
```python
from qcgf_dsl import ProtocolGraph
from simulator import QuantumSimulator

# 1. 创建BB84协议
bb84 = ProtocolGraph.create_bb84()

# 2. 运行仿真
simulator = QuantumSimulator()
result = simulator.simulate(bb84, pulse_count=10000)

print(f"QBER: {result.qber:.6f}")
print(f"Gain: {result.gain:.6f}")
print(f"密钥率: {result.raw_key_rate:.6f}")
```

### 示例2：使用AI设计新协议
```python
from ai_agent import HybridAgent

# 1. 创建AI智能体
agent = HybridAgent()

# 2. 设计新协议（快速演示）
new_protocol = agent.design_protocol(iterations=20)

# 3. 评估协议
evaluation = agent.evaluate_protocol(new_protocol)
print(f"新协议适应度: {evaluation['fitness']:.4f}")
```

### 示例3：协议可视化
```python
from qcgf_dsl import ProtocolGraph, visualize_protocol

# 创建协议
protocol = ProtocolGraph.create_bb84()

# 可视化
visualize_protocol(protocol, save_path='results/protocol.png')

# 或打印信息
from qcgf_dsl.visualizer import print_protocol_info
print_protocol_info(protocol)
```

## 📁 项目结构

```
AI4QKD/
├── README.md              # 项目详细说明
├── QUICK_START.md         # 本快速指南
├── requirements.txt       # 项目依赖
├── setup.py              # 一键设置脚本
├── test_basic.py         # 基础测试
├── examples/             # 使用示例
│   └── bb84_example.py  # BB84完整示例
├── ai_agent/            # AI智能体模块
│   ├── __init__.py
│   └── hybrid_agent.py  # 混合智能体
├── qcgf_dsl/            # 量子协议DSL
│   ├── __init__.py
│   ├── node_types.py    # 节点类型定义
│   ├── protocol_graph.py # 协议图核心
│   └── visualizer.py    # 可视化工具
├── simulator/           # 量子仿真器
│   ├── __init__.py
│   └── quantum_simulator.py # 基础仿真器
├── config/              # 配置管理
│   ├── __init__.py
│   └── settings.py     # 项目设置
└── results/             # 输出目录（自动创建）
```

## 🔧 开发工作流

### 1. 环境管理
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装新依赖
pip install package_name

# 冻结依赖
pip freeze > requirements.txt
```

### 2. 代码开发
```bash
# 运行测试
python test_basic.py

# 运行示例
python examples/bb84_example.py

# 创建新模块
# 1. 在相应目录创建.py文件
# 2. 更新__init__.py
# 3. 添加测试
```

### 3. 结果管理
```bash
# 查看结果
ls results/

# 清理结果
rm -rf results/*

# 保存重要结果
cp results/important_file.json backup/
```

## 🎯 下一步开发建议

### 短期目标（1-2周）
1. **完善量子仿真器**
   - 添加更多噪声模型
   - 支持纠缠态仿真
   - 优化仿真性能

2. **增强AI智能体**
   - 实现深度强化学习
   - 添加图神经网络编码
   - 优化训练算法

3. **扩展协议库**
   - 添加E91、MDI-QKD等协议
   - 支持协议导入/导出
   - 添加协议模板

### 中期目标（1-2月）
1. **安全评估模块**
   - 有限密钥分析
   - 熵估计计算
   - 安全参数验证

2. **图形用户界面**
   - 协议可视化编辑器
   - 仿真参数配置界面
   - 结果展示面板

3. **性能优化**
   - GPU加速支持
   - 并行计算优化
   - 内存使用优化

## 📚 学习资源

### 量子密码学基础
- **BB84协议**：第一个QKD协议，基础中的基础
- **E91协议**：基于纠缠的QKD协议
- **MDI-QKD**：测量设备无关QKD

### AI/机器学习
- **演化算法**：遗传算法、演化策略
- **强化学习**：Q-learning、策略梯度
- **图神经网络**：GCN、GAT、Graph Transformer

### 项目相关
- 查看`examples/`目录中的代码
- 阅读模块文档字符串
- 运行测试理解功能

## 🆘 常见问题

### Q1: 设置脚本失败
**A**: 检查Python版本（需要3.8+），确保有网络连接。

### Q2: 导入模块失败
**A**: 确保在项目根目录运行，或正确设置Python路径。

### Q3: 可视化失败
**A**: 需要matplotlib：`pip install matplotlib`

### Q4: AI训练慢
**A**: 这是简化版，完整版需要PyTorch和GPU加速。

## 🎉 开始你的研究！

### 研究思路1：协议创新
- 使用AI发现新的QKD协议结构
- 优化现有协议的参数
- 设计抗特定攻击的协议

### 研究思路2：性能分析
- 分析不同噪声模型的影响
- 比较不同协议的优缺点
- 研究实际部署的可行性

### 研究思路3：AI算法改进
- 改进演化算法的选择策略
- 添加深度强化学习组件
- 优化适应度函数设计

## 📞 获取帮助

### 项目文档
- `README.md`：详细项目说明
- 代码文档字符串：模块级文档
- 示例代码：使用示例

### 开发支持
- 查看测试代码理解API
- 修改示例代码进行实验
- 添加打印语句调试

---

**🎯 现在就开始吧！运行 `python setup.py` 启动你的AI4QKD研究之旅！**