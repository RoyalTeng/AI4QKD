# TF-QKD协议发现研究计划

## 🎯 研究目标
使用AI4QKD框架发现TF-QKD（双场量子密钥分发）协议

## 🔬 TF-QKD核心特征

### 1. 结构特征
- **两个远程发送方**：Alice和Bob在两端
- **中间测量节点**：Charlie在中间进行干涉测量
- **相位编码**：基于激光相位差编码信息
- **时间同步**：精确的时间对齐要求

### 2. 物理特征
- **相干态光源**：弱相干脉冲
- **相位调制**：随机相位调制
- **干涉测量**：马赫-曾德尔干涉仪
- **单光子探测**：高灵敏度探测器

### 3. 性能特征
- **突破线性限制**：密钥率随距离呈平方根衰减
- **抗信道损耗**：适合超长距离通信
- **实际安全性**：抵御多种实际攻击

## 🧪 实验设计

### 阶段1：TF-QKD特征定义和编码

#### 1.1 定义TF特征评分系统
```python
TF_FEATURES = {
    "twin_field": {  # 双场特征
        "weight": 0.3,
        "indicators": [
            "has_two_remote_senders",
            "has_interference_measurement", 
            "has_phase_encoding"
        ]
    },
    "interference": {  # 干涉特征
        "weight": 0.25,
        "indicators": [
            "has_mach_zehnder_interferometer",
            "has_phase_stabilization",
            "has_time_synchronization"
        ]
    },
    "performance": {  # 性能特征
        "weight": 0.25,
        "indicators": [
            "has_sqrt_distance_scaling",
            "has_long_distance_capability",
            "has_phase_error_tolerance"
        ]
    },
    "security": {  # 安全特征
        "weight": 0.2,
        "indicators": [
            "has_phase_randomization",
            "has_decoy_state",
            "has_phase_error_correction"
        ]
    }
}
```

#### 1.2 创建TF-QKD协议模板
```python
def create_tf_qkd_template():
    """创建TF-QKD协议模板"""
    protocol = ProtocolGraph(name="TF-QKD Template")
    
    # 两个远程发送方
    alice_source = protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': 'coherent', 'intensity': 0.5, 'phase': 'random'},
        party=Party.ALICE
    )
    
    bob_source = protocol.add_node(
        node_type=NodeType.QSP,
        params={'state': 'coherent', 'intensity': 0.5, 'phase': 'random'},
        party=Party.BOB
    )
    
    # 相位调制器
    alice_phase_mod = protocol.add_node(
        node_type=NodeType.QG,
        params={'gate_type': 'phase_modulator', 'phase_range': '0,π'},
        party=Party.ALICE
    )
    
    bob_phase_mod = protocol.add_node(
        node_type=NodeType.QG,
        params={'gate_type': 'phase_modulator', 'phase_range': '0,π'},
        party=Party.BOB
    )
    
    # 长距离量子信道
    channel_alice = protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.3, 'distance': 300, 'type': 'optical_fiber'},
        party=None
    )
    
    channel_bob = protocol.add_node(
        node_type=NodeType.QC,
        params={'loss': 0.3, 'distance': 300, 'type': 'optical_fiber'},
        party=None
    )
    
    # 马赫-曾德尔干涉仪（中间节点）
    interferometer = protocol.add_node(
        node_type=NodeType.QG,
        params={'gate_type': 'beam_splitter', 'configuration': 'mach_zehnder'},
        party=Party.CHARLIE
    )
    
    # 相位稳定器
    phase_stabilizer = protocol.add_node(
        node_type=NodeType.QG,
        params={'gate_type': 'phase_stabilizer', 'accuracy': 0.01},
        party=Party.CHARLIE
    )
    
    # 单光子探测器
    detector = protocol.add_node(
        node_type=NodeType.QD,
        params={'type': 'single_photon', 'efficiency': 0.7, 'dark_count': 1e-6},
        party=Party.CHARLIE
    )
    
    # 时间同步模块
    time_sync = protocol.add_node(
        node_type=NodeType.CP,
        params={'operation': 'time_synchronization', 'accuracy': '10ps'},
        party=None
    )
    
    # 相位后处理
    phase_processing = protocol.add_node(
        node_type=NodeType.CP,
        params={'operation': 'phase_error_correction+key_sifting'},
        party=Party.BOTH
    )
    
    # 添加边（连接所有组件）
    # ...（详细的连接关系）
    
    return protocol
```

### 阶段2：引导式适应度函数设计

#### 2.1 TF-specific适应度函数
```python
def tf_enhanced_fitness(protocol):
    """TF-QKD增强适应度函数"""
    base_fitness = evaluate_base_fitness(protocol)
    
    # TF特征奖励
    tf_bonus = 0.0
    
    # 1. 双场特征奖励
    if has_two_remote_senders(protocol):
        tf_bonus += 0.15
    
    if has_interference_measurement(protocol):
        tf_bonus += 0.10
    
    if has_phase_encoding(protocol):
        tf_bonus += 0.05
    
    # 2. 干涉特征奖励
    if has_mach_zehnder_interferometer(protocol):
        tf_bonus += 0.10
    
    if has_phase_stabilization(protocol):
        tf_bonus += 0.08
    
    if has_time_synchronization(protocol):
        tf_bonus += 0.07
    
    # 3. 长距离性能奖励
    if has_long_distance_capability(protocol):
        tf_bonus += 0.10
    
    # 4. 安全性奖励
    if has_phase_randomization(protocol):
        tf_bonus += 0.05
    
    if has_decoy_state(protocol):
        tf_bonus += 0.05
    
    total_fitness = base_fitness + tf_bonus
    return min(total_fitness, 1.0)
```

#### 2.2 TF特征检测函数
```python
def detect_tf_features(protocol):
    """检测TF-QKD特征"""
    features = {
        "structural": {
            "two_remote_senders": False,
            "interference_node": False,
            "phase_encoding": False
        },
        "interference": {
            "mach_zehnder": False,
            "phase_stabilizer": False,
            "time_sync": False
        },
        "performance": {
            "long_distance": False,
            "sqrt_scaling": False
        },
        "security": {
            "phase_randomization": False,
            "decoy_state": False
        }
    }
    
    # 分析协议结构
    for node_id in protocol.graph.nodes():
        node = protocol.graph.nodes[node_id]['node']
        
        # 检查双场特征
        if node.node_type == NodeType.QSP:
            if node.params.get('state') == 'coherent':
                features["structural"]["phase_encoding"] = True
        
        # 检查干涉特征
        if node.node_type == NodeType.QG:
            if node.params.get('gate_type') == 'beam_splitter':
                if node.params.get('configuration') == 'mach_zehnder':
                    features["interference"]["mach_zehnder"] = True
            elif node.params.get('gate_type') == 'phase_stabilizer':
                features["interference"]["phase_stabilizer"] = True
        
        # 检查时间同步
        if node.node_type == NodeType.CP:
            if 'time_synchronization' in str(node.params.get('operation', '')):
                features["interference"]["time_sync"] = True
    
    # 计算TF分数
    tf_score = calculate_tf_score(features)
    features["tf_score"] = tf_score
    features["is_tf_like"] = tf_score >= 0.7
    
    return features
```

### 阶段3：实验执行计划

#### 3.1 实验参数
```python
EXPERIMENT_CONFIG = {
    "name": "TF-QKD Protocol Discovery",
    "iterations": 200,
    "population_size": 20,
    "elite_size": 3,
    "mutation_rate": 0.35,
    "crossover_rate": 0.25,
    "tf_template_in_population": True,
    "guided_mutation_probability": 0.7
}
```

#### 3.2 实验步骤
1. **初始化**：创建包含TF模板的初始种群
2. **训练**：使用TF增强适应度函数进行演化
3. **监控**：跟踪TF特征演化过程
4. **分析**：评估发现的协议质量
5. **验证**：在扩展仿真模型中测试性能

#### 3.3 成功标准
- **主要标准**：发现TF-like协议（TF分数 ≥ 0.7）
- **次要标准**：适应度超过基准协议（BB84/MDI）
- **高级标准**：发现新颖的TF变体协议

### 阶段4：对比实验设计

#### 4.1 对比组设置
```python
COMPARISON_GROUPS = {
    "group_a": {
        "name": "Standard AI (no TF guidance)",
        "fitness_function": "base_fitness",
        "template_in_population": False
    },
    "group_b": {
        "name": "TF-guided AI",
        "fitness_function": "tf_enhanced_fitness",
        "template_in_population": True
    },
    "group_c": {
        "name": "TF-guided with specialized mutation",
        "fitness_function": "tf_enhanced_fitness",
        "template_in_population": True,
        "guided_mutation": True
    }
}
```

#### 4.2 评估指标
1. **TF特征得分**：0-1评分
2. **适应度提升**：相对于基准的改进
3. **收敛速度**：达到最佳适应度的代数
4. **协议复杂性**：节点和边数量
5. **新颖性**：与已知TF协议的差异度

### 阶段5：结果分析和论文准备

#### 5.1 预期成果
1. **TF-like协议发现**：至少一个TF分数 ≥ 0.7的协议
2. **性能分析**：与现有协议的对比
3. **方法验证**：引导式设计的有效性证明
4. **新颖发现**：可能的TF协议变体

#### 5.2 论文贡献
- **新方法**：TF-QKD协议的AI发现方法
- **新结果**：AI发现的TF-like协议
- **新见解**：TF协议设计的原则和模式
- **新工具**：TF协议分析和评估框架

#### 5.3 时间安排
- **Day 1**：特征定义和模板创建
- **Day 2**：实验实现和初步测试
- **Day 3**：完整实验运行和数据分析
- **Day 4**：结果验证和论文撰写
- **Day 5**：论文完善和投稿准备

## 🚀 立即行动步骤

### 第一步：创建TF-QKD实验脚本
```bash
cd ~/Desktop/AI4QKD
python3 create_tf_experiment.py
```

### 第二步：运行初步实验
```bash
python3 experiment_tf_qkd.py --mode quick --iterations 50
```

### 第三步：分析初步结果
```bash
python3 analyze_tf_results.py --file results/tf_*.json
```

### 第四步：运行完整实验
```bash
python3 experiment_tf_qkd.py --mode full --iterations 200
```

## 📊 成功概率评估

基于MDI-QKD实验的成功经验：
- **技术可行性**：高（已有成功案例）
- **方法成熟度**：中高（需要调整特征定义）
- **预期成果**：很可能发现TF-like协议
- **创新价值**：高（TF-QKD是前沿方向）

## 💡 风险与应对

### 风险1：TF特征过于复杂
- **应对**：简化特征定义，分阶段实现

### 风险2：收敛到局部最优
- **应对**：增加种群多样性，使用多种变异策略

### 风险3：计算资源需求高
- **应对**：优化代码，使用增量训练

## 🎯 研究意义

### 学术意义
- 推动TF-QKD协议设计自动化
- 探索AI在复杂量子系统设计中的应用
- 为其他量子协议发现提供方法论

### 实际意义
- 加速TF-QKD技术发展和优化
- 降低协议设计门槛
- 促进量子通信实际应用

---

**开始时间**：立即开始  
**预计完成**：3-5天  
**预期影响**：高水平论文发表