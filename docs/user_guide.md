# 用户指南

> 本文档旨在指导用户如何安装、配置、运行和使用AI4QKD系统。无论你是想运行一个已有协议的仿真，还是利用AI设计新协议，本文档都将提供清晰的操作步骤。

---

## 一、安装与环境配置

在开始之前，请确保你已安装 Python 3.8 或更高版本。

### 1. 克隆项目

首先，从GitHub克隆本项目到本地：

```bash
git clone <your-repository-url>
cd AI4QKD
```

### 2. 创建并激活虚拟环境

我们强烈建议在Python虚拟环境中运行本项目，以隔离依赖。

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. 安装依赖

所有必需的Python库都已在 `requirements.txt` 中列出。

```bash
pip install -r requirements.txt
```
安装过程可能需要几分钟。完成后，你的环境就准备就绪了。

---

## 二、快速运行一个示例

我们提供了一系列预置的协议示例，让你能快速上手。以经典的BB84协议为例：

### 1. 运行示例脚本

在项目根目录下，执行以下命令：

```bash
python examples/bb84_example.py
```

### 2. 查看输出

你将在终端看到类似如下的日志输出，展示了仿真和评估的关键步骤与结果：

```
INFO:__main__:--- 开始执行 BB84 协议示例 ---
INFO:__main__:步骤 1: 从配置文件构建协议图...
INFO:__main__:协议图 'BB84_from_Config' 构建完成。
INFO:__main__:步骤 2: 使用真实物理仿真器进行仿真...
INFO:__main__:仿真完成。 性能指标: QBER=0.0210, Gain=0.5000
INFO:__main__:步骤 3: 估算安全密钥率...
INFO:__main__:估算的安全密钥率: 0.123456 bits/pulse
INFO:__main__:--- BB84 协议示例执行完毕 ---
```

### 3. 可视化协议图（可选）

部分示例支持生成协议图的可视化图片。运行以下命令：

```bash
python examples/bb84_example.py --visualize
```
执行后，你会在 `examples/` 目录下找到一张名为 `bb84_protocol_structure.png` 的图片，直观展示了BB84协议的结构。

---

## 三、各子模块的用法说明

### 1. 使用 `main.py` 进行AI协议设计

`main.py` 是整个系统的核心入口，主要用于AI驱动的协议设计与优化。

```bash
python main.py
```
该命令将启动AI智能体，自动进行协议设计、仿真、评估与验证的完整闭环流程。你将看到AI不断迭代、优化协议的过程日志。

### 2. 程序化调用核心模块

除了运行主程序，你也可以在自己的Python脚本中直接调用系统的核心模块。

- **调用仿真器 (`simulator`)**：
  ```python
  from simulator.quantum_simulator import QuantumSimulator
  # 假设你已有一个 protocol_graph 对象
  simulator = QuantumSimulator(config)
  results = simulator.simulate_protocol_graph(protocol_graph)
  print(f"QBER: {results['qber']}")
  ```

- **调用安全评估器 (`security_evaluator`)**：
  ```python
  from security_evaluator.key_rate_calculator import KeyRateCalculator
  key_rate_calc = KeyRateCalculator(qber=0.02, gain=0.5, ...)
  secure_key_rate = key_rate_calc.calculate_key_rate()
  print(f"安全密钥率: {secure_key_rate}")
  ```

- **调用AI优化器 (`ai_agent`)**：
  ```python
  from ai_agent.hybrid_agent import HybridAgent
  agent = HybridAgent(config)
  optimized_protocol, suggestions = agent.optimize(initial_protocol)
  ```

---

## 四、配置文件的说明与修改方式

系统的所有可调参数都集中在 `config/` 目录下，方便用户修改与实验。

### 1. `config/settings.py` - 全局配置文件

这是最重要的配置文件，包含了仿真、信道、噪声等物理参数。

- **修改信道损耗**：
  找到 `CHANNEL_LOSS` 变量，修改其值（如 `0.2` dB/km）。
- **修改噪声水平**：
  调整 `NOISE_MODEL_PARAMS` 字典中的 `dephasing_rate` 等参数。

### 2. `config/qkd_protocols.py` - 预定义协议配置

该文件存放了BB84等经典协议的参数模板。你可以复制并修改这些模板来创建自己的协议变种。

### 3. `config/ai_agent_config.py` - AI智能体配置

这里包含了AI算法的超参数。

- **修改学习率**：
  在 `get_default_ai_agent_config()` 函数返回的字典中，修改 `learning_rate` 的值。
- **调整种群大小**：
  如果你在使用演化算法，可以修改 `population_size`。

修改这些配置文件后，无需重新编译或安装，直接再次运行脚本即可生效。