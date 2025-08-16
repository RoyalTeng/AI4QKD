# CLAUDE.md

此文件为Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

AI4QKD是一个AI辅助量子密钥分发协议设计系统，该项目目前处于**完全重构阶段**。原有的复杂代码已在`clean-start-v3`分支中完全清空，只保留了核心参考文献和研究方案。

### 项目状态
- **当前分支**: `clean-start-v3` - 全新开始的重构分支
- **代码状态**: 已清空，只保留文档和参考文献
- **重构目标**: 从20,000+行复杂代码简化为<3,000行的简洁系统

## 核心架构设计（目标）

### 计划的简化架构
```
AI4QKD/
├── core/
│   ├── protocol.py      # QKD协议表示
│   ├── simulator.py     # 量子通信仿真  
│   ├── ai_designer.py   # AI驱动协议优化
│   └── evaluator.py     # 安全和性能分析
├── examples/
│   ├── bb84_demo.py     # 经典BB84演示
│   └── ai_training.py   # AI训练示例
├── utils/
│   ├── visualizer.py    # 协议可视化工具
│   └── config.py        # 系统配置
├── main.py              # 主入口程序
├── requirements.txt     # 最小依赖
└── tests/               # 单元测试
```

## 开发命令（计划中）

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活环境 (Windows)
venv\Scripts\activate

# 激活环境 (Linux/Mac)  
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 测试命令
```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试模块
python -m pytest tests/test_protocol.py -v
python -m pytest tests/test_simulator.py -v
python -m pytest tests/test_ai_designer.py -v

# 运行测试并显示覆盖率
python -m pytest tests/ --cov=core --cov-report=html
```

### 运行示例
```bash
# 基础演示
python main.py --demo

# BB84基准测试
python examples/bb84_demo.py

# AI训练演示
python examples/ai_training.py

# 性能基准测试
python benchmark.py --protocol BB84 --iterations 1000
```

### 代码质量
```bash
# 代码格式化
black .

# 代码检查
flake8 core/ examples/ tests/

# 类型检查
mypy core/
```

## 核心设计原则

### 1. 极简主义架构
- **单一职责**: 每个模块只做一件事
- **最小依赖**: 只使用必要的库 (numpy, matplotlib, 可选qiskit)
- **清晰接口**: 简单直观的API设计

### 2. 协议表示方法
- QKD协议表示为有向图：节点（量子操作）+ 边（通信链路）
- 使用简单的Python数据结构，避免复杂的图库依赖
- 支持序列化为JSON格式用于保存和加载

### 3. AI优化策略
- 使用遗传算法而非复杂的深度学习
- 专注于协议结构优化，不涉及量子电路优化
- 快速评估适应度，支持大规模进化搜索

### 4. 安全性评估
- 基于信息论安全的数学公式计算
- 有限密钥分析用于实际场景
- 实时安全验证确保生成协议的有效性

## 已验证的研究成果

### 性能基准
- **BB84基准**: 0.480900 bits/pulse
- **AI增强协议**: 0.505332 bits/pulse
- **性能提升**: 5.08%

### 关键创新
- 自适应态制备：动态量子态优化
- 智能基选择：机器学习指导的测量
- 协议图表示：使AI优化成为可能

## 理论基础

### 核心参考文献
1. **Gisin等 (2002)** - 量子密码学基础理论
2. **Dunjko & Briegel (2018)** - AI在量子领域的应用综述  
3. **现代物理评论 (2024)** - QKD协议优化的最新进展

### 研究方法
结合三个领域：量子密码学 + 机器学习 + 形式化验证

## 重构指导原则

### 删除的复杂功能
- ❌ 多层抽象框架 (universal_framework, ac_framework)
- ❌ 复杂的深度学习实现
- ❌ 重复的仿真器类
- ❌ 过度工程化的配置系统

### 保留的核心功能  
- ✅ QKD协议图表示
- ✅ 基本量子仿真
- ✅ AI协议优化
- ✅ 安全性评估
- ✅ 结果可视化

## 开发工作流程

### 1. 核心模块开发
按以下顺序实现核心模块：
1. `protocol.py` - 协议表示和序列化
2. `simulator.py` - 快速性能仿真
3. `ai_designer.py` - 遗传算法优化
4. `evaluator.py` - 安全性评估

### 2. 测试驱动开发
- 每个模块先写测试后实现
- 使用pytest进行单元测试
- 集成测试验证端到端功能

### 3. 示例和文档
- 创建清晰的使用示例
- 保持文档与代码同步
- 提供可重现的实验结果

## 性能目标

### 代码量目标
- 总文件数: < 15个
- 总代码行数: < 3,000行
- 主要模块: 4个核心 + 工具

### 功能目标
- 保持原系统90%的核心功能
- 新用户30分钟内理解项目
- 完整示例运行时间<1分钟

## 注意事项

### 当前状态提醒
- 代码库已完全清空，需要从零开始实现
- 保留了完整的理论基础和研究文档
- 所有之前验证的研究成果都需要在新架构中重新实现

### 开发优先级
1. 首先实现最小可行产品 (MVP)
2. 验证核心功能可正常工作
3. 逐步添加高级功能
4. 最后优化性能和用户体验

这个重构项目的目标是创建一个**简洁、高效、易于理解**的AI4QKD系统，让研究人员能够快速上手并扩展功能。