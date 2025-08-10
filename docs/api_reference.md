# API参考文档

> 本文档汇总AI4QKD系统各核心模块的主要类、函数与配置项，便于开发者查阅与调用。

---

## 1. qcgf_dsl（量子-经典图流DSL）

### 主要类与接口

| 类/函数 | 参数 | 返回值 | 用途 |
| ------- | ---- | ------ | ---- |
| `ProtocolGraph` | name: str | ProtocolGraph实例 | 协议图核心数据结构 |
| `Node` | node_id, node_type, params, party, position | Node实例 | 协议节点封装 |
| `Edge` | source_id, target_id, edge_type, params | Edge实例 | 协议图中的边 |
| `NodeType` | 无参数 | Enum | 节点类型枚举 |
| `EdgeType` | 无参数 | Enum | 边类型枚举 |
| `Party` | 无参数 | Enum | 协议参与方枚举 |
| `QCGFCompiler` | 无参数 | QCGFCompiler实例 | 协议图编译器 |
| `QCGFParser` | 无参数 | QCGFParser实例 | DSL解析器 |
| `ProtocolVisualizer` | 无参数 | ProtocolVisualizer实例 | 协议图可视化工具 |

### 主要方法

| 方法 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `ProtocolGraph.add_node` | node_type, params, party, position, node_id | node_id | 添加节点到协议图 |
| `ProtocolGraph.add_edge` | source_id, target_id, edge_type, params | edge_id | 添加边到协议图 |
| `ProtocolGraph.to_dict` | 无参数 | dict | 协议图序列化为字典 |
| `ProtocolGraph.from_dict` | data: dict | ProtocolGraph | 字典反序列化为协议图 |
| `QCGFCompiler.compile_protocol` | protocol_graph, target_language | str | 编译协议图为代码 |
| `ProtocolVisualizer.visualize` | graph, ax | None | 可视化协议图 |

---

## 2. simulator（量子仿真器）

### 主要类与接口

| 类/函数 | 参数 | 返回值 | 用途 |
| ------- | ---- | ------ | ---- |
| `QuantumSimulator` | max_photon_number, pulse_rate, num_measurements | QuantumSimulator实例 | 主量子仿真器 |
| `RealQuantumSimulator` | protocol_graph | RealQuantumSimulator实例 | 物理精确仿真器 |
| `ChannelModel` | loss, noise, fiber_length, max_photon_number | ChannelModel实例 | 量子信道建模 |
| `Measurement` | max_photon_number | Measurement实例 | 量子测量仿真 |
| `StatePreparation` | mu, decoy_mu, max_photon_number | StatePreparation实例 | 量子态制备仿真 |
| `PerformanceMetrics` | 无参数 | PerformanceMetrics实例 | 性能指标计算 |
| `NoiseModel` | dephasing_rate, amplitude_damping_rate, phase_noise_std | NoiseModel实例 | 噪声模型 |

### 主要方法

| 方法 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `QuantumSimulator.simulate_protocol_graph` | protocol_graph, simulation_params | dict | 仿真协议图 |
| `QuantumSimulator.simulate_mdi_qkd_protocol` | alice_mean_photon, bob_mean_photon, channel_loss, charlie_efficiency | dict | 仿真MDI-QKD协议 |
| `RealQuantumSimulator.run` | 无参数 | dict | 运行完整协议仿真 |
| `ChannelModel.apply_loss_channel` | input_state, loss_rate | dict | 应用损耗信道 |
| `Measurement.projective_measurement` | input_state, basis | dict | 投影测量仿真 |
| `StatePreparation.prepare_wcp_state` | mu | dict | 制备弱相干脉冲态 |
| `PerformanceMetrics.calculate_qber` | alice_bits, bob_bits | float | 计算QBER |
| `NoiseModel.apply_dephasing` | state | ndarray | 施加退相干噪声 |

---

## 3. ai_agent（AI智能体）

### 主要类与接口

| 类/函数 | 参数 | 返回值 | 用途 |
| ------- | ---- | ------ | ---- |
| `HybridAgent` | config | HybridAgent实例 | 混合智能体 |
| `SACAgent` | state_dim, action_dim, num_node_targets, param_dim | SACAgent实例 | SAC智能体 |
| `PPOAgent` | state_dim, action_dim, num_node_targets, param_dim | PPOAgent实例 | PPO智能体 |
| `GeneticAlgorithm` | population_size, crossover_rate, mutation_rate, fitness_fn | GeneticAlgorithm实例 | 遗传算法优化器 |
| `EvolutionStrategy` | mean_vector, stdev_vector, population_size, learning_rate | EvolutionStrategy实例 | 演化策略优化器 |
| `Population` | population_size, initialization_fn, fitness_fn | Population实例 | 种群管理 |
| `PolicyNetwork` | input_dim, num_actions, num_node_targets, param_dim | PolicyNetwork实例 | 策略网络 |
| `ValueNetwork` | input_dim | ValueNetwork实例 | 价值网络 |
| `ReplayBuffer` | capacity | ReplayBuffer实例 | 经验回放缓冲区 |

### 主要方法

| 方法 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `HybridAgent.optimize` | initial_protocol | (ProtocolGraph, List[str]) | 优化协议 |
| `SACAgent.select_action` | state | ndarray | 选择动作 |
| `SACAgent.train` | replay_buffer, batch_size | None | 训练SAC智能体 |
| `PPOAgent.select_action` | state | tuple | 选择动作及概率 |
| `PPOAgent.update` | memory | None | 更新PPO策略 |
| `GeneticAlgorithm.evolve` | generations | ProtocolGraph | 进化优化 |
| `Population.get_best_individual` | 无参数 | Any | 获取最优个体 |

---

## 4. security_evaluator（安全评估）

### 主要类与接口

| 类/函数 | 参数 | 返回值 | 用途 |
| ------- | ---- | ------ | ---- |
| `KeyRateCalculator` | qber, gain, protocol_type, params, config | KeyRateCalculator实例 | 密钥率计算器 |
| `EntropyEstimator` | config | EntropyEstimator实例 | 熵估计器 |
| `FiniteKeyAnalyzer` | config | FiniteKeyAnalyzer实例 | 有限密钥分析 |
| `ComposableSecurityAnalyzer` | config | ComposableSecurityAnalyzer实例 | 可组合安全性分析 |
| `SecurityParameters` | epsilon_sec, epsilon_cor, epsilon_pa | SecurityParameters实例 | 安全参数集合 |

### 主要方法

| 方法 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `KeyRateCalculator.calculate_key_rate` | 无参数 | float | 计算最终密钥率 |
| `KeyRateCalculator.compute` | qber, gain, n_pulses, protocol_type | KeyRateResult | 详细密钥率计算 |
| `EntropyEstimator.calculate_min_entropy` | qber, protocol_type | EntropyResult | 计算最小熵 |
| `FiniteKeyAnalyzer.analyze_finite_key_effects` | n_raw, qber, protocol_type | FiniteKeyResult | 有限密钥效应分析 |
| `ComposableSecurityAnalyzer.analyze_composable_security` | n_protocols, protocol_epsilon | ComposableSecurityResult | 可组合安全性分析 |

---

## 5. formal_verification（形式化验证）

### 主要类与接口

| 类/函数 | 参数 | 返回值 | 用途 |
| ------- | ---- | ------ | ---- |
| `ProtocolVerifier` | 无参数 | ProtocolVerifier实例 | 协议结构验证器 |
| `VerificationReport` | is_valid, errors, warnings, metadata | VerificationReport实例 | 验证报告 |
| `SecurityProof` | 无参数 | SecurityProof实例 | 安全性证明生成 |
| `ModelChecker` | 无参数 | ModelChecker实例 | 协议模型检查器 |
| `TheoremProver` | 无参数 | TheoremProver实例 | 定理证明器 |

### 主要方法

| 方法 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `ProtocolVerifier.verify` | graph | VerificationReport | 验证协议图结构 |
| `SecurityProof.generate` | graph, qber, gain | str | 生成LaTeX安全性证明 |
| `ModelChecker.run_model_check` | spec, graph | bool | 运行CTL/LTL模型检查 |
| `TheoremProver.prove_no_cloning` | 无参数 | CheckSatResult | 证明不可克隆定理 |

---

## 6. utils（工具函数）

### 主要函数

| 函数 | 参数 | 返回值 | 用途 |
| ---- | ---- | ------ | ---- |
| `setup_logger` | name, log_level, log_file | Logger | 设置日志记录器 |
| `compute_key_rate_metrics` | results | dict | 统计密钥率指标 |
| `track_drl_learning_curve` | rewards, window_size | dict | 跟踪DRL学习曲线 |
| `normalize_results` | df, columns | DataFrame | Min-Max归一化 |
| `graph_to_dict` | graph | dict | 协议图序列化 |
| `dict_to_graph` | graph_dict | ProtocolGraph | 协议图反序列化 |
| `compare_graphs` | g1, g2 | float | 协议图相似度 |
| `plot_learning_curve` | rewards, title, save_path | None | 绘制DRL学习曲线 |
| `plot_qber_gain_evolution` | history, title, save_path | None | 绘制QBER/Gain演化 |
| `plot_performance_comparison` | original_metrics, optimized_metrics, title, save_path | None | 性能对比条形图 |

---

## 详细参数说明

### qcgf_dsl 模块详细说明

#### ProtocolGraph 类
- **初始化参数**：
  - `name`: 协议图名称，默认为 "QKD_Protocol"
- **主要方法**：
  - `add_node()`: 添加节点，返回节点ID
  - `add_edge()`: 添加边，返回边ID
  - `get_node_count()`: 获取节点数量
  - `get_edge_count()`: 获取边数量
  - `is_dag()`: 检查是否为有向无环图

#### Node 类
- **初始化参数**：
  - `node_id`: 节点唯一标识符
  - `node_type`: 节点类型（NodeType枚举）
  - `params`: 节点参数字典
  - `party`: 参与方（Party枚举）
  - `position`: 节点位置坐标

### simulator 模块详细说明

#### QuantumSimulator 类
- **初始化参数**：
  - `max_photon_number`: 最大光子数，默认10
  - `pulse_rate`: 脉冲率（Hz），默认1e9
  - `num_measurements`: 测量次数，默认1000

#### StatePreparation 类
- **主要方法**：
  - `prepare_vacuum_state()`: 制备真空态
  - `prepare_single_photon_state()`: 制备单光子态
  - `prepare_wcp_state(mu)`: 制备弱相干脉冲态

### ai_agent 模块详细说明

#### HybridAgent 类
- **配置参数**：
  - `graph_encoder`: 图编码器配置
  - `drl_agent`: DRL智能体配置
  - `ea_agent`: 演化算法配置

#### SACAgent 类
- **初始化参数**：
  - `state_dim`: 状态维度
  - `action_dim`: 动作维度
  - `lr`: 学习率，默认3e-4
  - `gamma`: 折扣因子，默认0.99

### security_evaluator 模块详细说明

#### KeyRateCalculator 类
- **支持协议**：BB84、Decoy-BB84、MDI-QKD
- **主要参数**：
  - `qber`: 量子比特错误率
  - `gain`: 信道增益
  - `protocol_type`: 协议类型

#### EntropyEstimator 类
- **支持熵类型**：
  - 最小熵 H_min(X|E)
  - 条件熵 H(X|E)
  - 冯·诺依曼熵
  - 相对熵

---

> 如需更多详细信息，请查阅各模块源码及注释。 