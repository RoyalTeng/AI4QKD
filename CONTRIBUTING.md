# 贡献指南

感谢您对AI4QKD项目的兴趣！我们欢迎各种形式的贡献，包括代码、文档、测试、想法和反馈。

## 🎯 贡献方式

### 📝 代码贡献
- 修复bug
- 添加新功能
- 性能优化
- 代码重构

### 📚 文档贡献
- 改进文档内容
- 添加使用示例
- 翻译文档
- API文档完善

### 🧪 测试贡献
- 编写单元测试
- 集成测试
- 性能测试
- 边界情况测试

### 💡 其他贡献
- 报告bug
- 提出功能建议
- 用户体验反馈
- 设计改进建议

## 🚀 快速开始

### 1. 开发环境配置

#### 克隆仓库
```bash
# Fork项目到您的GitHub账户，然后克隆
git clone https://github.com/您的用户名/AI4QKD.git
cd AI4QKD

# 添加上游仓库
git remote add upstream https://github.com/RoyalTeng/AI4QKD.git
```

#### 环境设置
```bash
# 激活conda环境
conda activate ai4qkd_env

# 或者创建新环境
conda create -n ai4qkd_dev python=3.8
conda activate ai4qkd_dev

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果存在
```

#### 验证环境
```bash
# 运行测试确保环境正常
python -m pytest tests/ -v
python test_refactor.py
```

### 2. 开发工作流

#### 创建功能分支
```bash
# 更新主分支
git checkout clean-start-v3
git pull upstream clean-start-v3

# 创建功能分支
git checkout -b feature/您的功能名称
# 或者修复bug分支
git checkout -b fix/问题描述
```

#### 开发规范
```bash
# 确保每次开发前都激活环境
conda activate ai4qkd_env

# 遵循TDD开发模式
# 1. 编写测试
# 2. 运行测试（应该失败）
# 3. 编写最小代码使测试通过
# 4. 重构代码
# 5. 重复循环
```

## 📋 开发规范

### 代码风格

#### Python代码规范
- 遵循PEP 8标准
- 使用类型注解
- 函数和类必须有文档字符串
- 保持代码可读性

```python
# 好的代码示例
def calculate_key_rate(protocol_data: Dict[str, Any], 
                      distance: float) -> float:
    """
    计算QKD协议的安全密钥率
    
    重构思路：
    - 基于信息论公式计算
    - 考虑有限密钥效应
    - 优化计算性能
    
    参数：
        protocol_data: 协议参数字典
        distance: 传输距离(公里)
        
    返回值：
        float: 安全密钥率(bits/pulse)
        
    异常：
        ValueError: 参数无效时抛出
    """
    if distance < 0:
        raise ValueError("距离不能为负数")
    
    # 实现细节...
    return key_rate
```

#### 重构代码规范
根据项目的重构指导原则，所有代码必须包含重构思路注释：

```python
# ============================================================================
# 重构说明: 此函数基于GitHub master分支的original_function重构
# 重构日期: 2025-08-18
# 重构原因: 简化计算逻辑，提高性能
# 主要改进: 使用向量化计算，减少循环开销
# 参考文件: security_evaluator/key_rate_calculator.py
# ============================================================================

def optimized_function(self, param1, param2):
    """
    重构后的函数实现
    
    重构思路：
    - 参考原有函数的算法思路
    - 简化了复杂的嵌套逻辑
    - 优化了数值计算性能
    - 改进了错误处理机制
    """
    pass
```

### 提交规范

#### 提交信息格式
```
类型(作用域): 简短描述

详细描述（可选）

- 列出主要变更
- 说明影响和原因
- 引用相关issue

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 提交类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档修改
- `style`: 代码风格修改（不影响功能）
- `refactor`: 代码重构
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

#### 提交示例
```bash
git commit -m "feat(qcgf_dsl): 添加协议合并功能

- 实现ProtocolGraph.merge()方法
- 支持节点ID冲突自动处理
- 添加合并测试用例
- 更新API文档

Fixes #123

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 测试规范

#### 测试文件结构
```
tests/
├── conftest.py              # pytest配置
├── test_qcgf_dsl_refactor.py  # qcgf_dsl模块测试
├── test_protocol_graph.py   # ProtocolGraph类测试
├── test_node_types.py       # 节点类型测试
├── test_edge_types.py       # 边类型测试
├── integration/             # 集成测试
│   ├── test_end_to_end.py
│   └── test_performance.py
└── fixtures/                # 测试数据
    ├── bb84_protocol.json
    └── test_protocols/
```

#### 测试编写指南
```python
import pytest
from qcgf_dsl import *

class TestProtocolGraphRefactor:
    """ProtocolGraph重构测试用例"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.protocol = ProtocolGraph("测试协议")
    
    def test_add_node_basic(self):
        """测试基本节点添加功能"""
        # 测试正常情况
        node_id = self.protocol.add_node(NodeType.QSP, party=Party.ALICE)
        assert node_id is not None
        assert self.protocol.has_node(node_id)
        
        # 测试节点属性
        node = self.protocol.get_node(node_id)
        assert node.node_type == NodeType.QSP
        assert node.party == Party.ALICE
    
    def test_add_node_invalid_params(self):
        """测试无效参数的处理"""
        with pytest.raises(ValueError):
            self.protocol.add_node(
                NodeType.QM,
                params={"efficiency": 1.5}  # 无效：效率>1
            )
    
    def test_protocol_serialization(self):
        """测试协议序列化功能"""
        # 创建测试协议
        node1 = self.protocol.add_node(NodeType.QSP)
        node2 = self.protocol.add_node(NodeType.QM)
        self.protocol.add_edge(node1, node2, EdgeType.QUANTUM)
        
        # 序列化和反序列化
        data = self.protocol.to_dict()
        restored = ProtocolGraph.from_dict(data)
        
        # 验证完整性
        assert restored.get_node_count() == self.protocol.get_node_count()
        assert restored.get_edge_count() == self.protocol.get_edge_count()
    
    @pytest.mark.performance
    def test_large_protocol_performance(self):
        """测试大型协议的性能"""
        import time
        
        start_time = time.time()
        for i in range(1000):
            self.protocol.add_node(NodeType.QSP)
        end_time = time.time()
        
        # 性能要求：1000个节点添加应在1秒内完成
        assert end_time - start_time < 1.0
```

#### 运行测试
```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_protocol_graph.py -v

# 运行特定测试方法
python -m pytest tests/test_protocol_graph.py::TestProtocolGraphRefactor::test_add_node_basic -v

# 运行性能测试
python -m pytest tests/ -m performance

# 生成覆盖率报告
python -m pytest tests/ --cov=qcgf_dsl --cov-report=html
```

## 🔍 代码审查

### 审查清单

#### 功能性审查
- [ ] 代码实现了预期功能
- [ ] 所有边界情况都得到处理
- [ ] 错误处理机制完善
- [ ] 向后兼容性保持

#### 代码质量审查
- [ ] 遵循项目代码规范
- [ ] 变量和函数命名清晰
- [ ] 注释和文档完整
- [ ] 包含重构思路说明

#### 测试审查
- [ ] 测试覆盖率充分
- [ ] 测试用例包含正常和异常情况
- [ ] 性能测试通过
- [ ] 集成测试通过

#### 文档审查
- [ ] API文档更新
- [ ] 用户指南更新
- [ ] 示例代码有效
- [ ] CHANGELOG更新

### 提交PR流程

#### 1. 准备提交
```bash
# 确保代码是最新的
git fetch upstream
git rebase upstream/clean-start-v3

# 运行完整测试
python -m pytest tests/ -v
python test_refactor.py

# 检查代码质量
flake8 qcgf_dsl/ tests/
black qcgf_dsl/ tests/ --check
```

#### 2. 创建Pull Request
在GitHub上创建PR时，请包含：

```markdown
## 变更描述
简要描述本次变更的内容和目的。

## 重构思路
- 基于GitHub master分支的[具体模块]
- 主要改进：[列出改进点]
- 保持了[原有设计思路]

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新
- [ ] 性能优化

## 测试
- [ ] 添加了新的测试用例
- [ ] 所有现有测试通过
- [ ] 测试覆盖率保持或提高

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 包含重构思路注释
- [ ] 文档已更新
- [ ] 向后兼容性保持

## 相关Issue
Closes #[issue_number]
```

#### 3. 响应审查反馈
- 及时回应审查意见
- 解释设计决策的理由
- 根据反馈修改代码
- 保持友好的沟通态度

## 🐛 Bug报告

### 报告模板
使用GitHub Issues报告bug时，请包含：

```markdown
## Bug描述
清晰简洁地描述遇到的问题。

## 复现步骤
1. 执行步骤1
2. 执行步骤2
3. 观察到错误

## 预期行为
描述您期望发生的行为。

## 实际行为
描述实际发生的行为。

## 环境信息
- 操作系统: [例如 Windows 10]
- Python版本: [例如 3.8.10]
- AI4QKD版本: [例如 2.0.0]
- 相关依赖版本: [NetworkX, NumPy等]

## 错误信息
```
粘贴完整的错误信息或异常堆栈
```

## 附加信息
添加任何其他有助于诊断问题的信息。
```

### Bug修复流程
1. **确认bug**: 验证问题确实存在
2. **创建测试**: 编写重现bug的测试用例
3. **修复代码**: 实现最小修复
4. **验证修复**: 确保测试通过且不引入新问题
5. **提交PR**: 包含bug修复和测试

## 💡 功能建议

### 建议模板
```markdown
## 功能描述
简洁地描述建议的功能。

## 问题背景
这个功能要解决什么问题？

## 解决方案
描述您想要的解决方案。

## 替代方案
描述您考虑过的替代解决方案。

## 用例场景
提供具体的使用场景。

## 实现复杂度
评估实现的复杂程度。
```

## 📈 性能优化

### 性能测试
```python
import time
import memory_profiler

def benchmark_protocol_creation():
    """基准测试：协议创建性能"""
    start_time = time.time()
    
    for i in range(100):
        protocol = create_bb84_protocol()
    
    end_time = time.time()
    print(f"100次BB84创建耗时: {end_time - start_time:.3f}秒")

@memory_profiler.profile
def benchmark_memory_usage():
    """基准测试：内存使用"""
    protocols = []
    for i in range(100):
        protocol = create_bb84_protocol()
        protocols.append(protocol)
    
    return protocols
```

### 性能优化指南
1. **识别瓶颈**: 使用profiler工具
2. **优化算法**: 改进时间复杂度
3. **减少内存使用**: 优化数据结构
4. **缓存机制**: 避免重复计算
5. **验证改进**: 运行基准测试

## 📖 文档贡献

### 文档类型
- **API文档**: 函数和类的技术文档
- **用户指南**: 面向用户的使用说明
- **开发文档**: 面向开发者的技术文档
- **示例代码**: 实际使用案例

### 文档规范
- 使用Markdown格式
- 包含代码示例
- 提供清晰的截图（如适用）
- 保持内容的准确性和时效性

### 文档更新流程
1. 识别需要更新的文档
2. 修改相关文档文件
3. 验证示例代码可运行
4. 提交文档更新PR

## 🏆 认可贡献者

我们感谢所有贡献者的努力！贡献者将被列入：

### 贡献者列表
- **核心开发者**: 长期活跃的主要贡献者
- **代码贡献者**: 提交代码修改的贡献者
- **文档贡献者**: 改进文档的贡献者
- **测试贡献者**: 添加测试的贡献者
- **社区贡献者**: 参与讨论和反馈的贡献者

### 贡献统计
- 提交数量
- 代码行数
- 文档改进
- issue解决数量

## 📞 联系方式

### 项目维护者
- **主要维护者**: [姓名] <email@example.com>
- **技术负责人**: [姓名] <email@example.com>

### 沟通渠道
- **GitHub Issues**: 技术问题和bug报告
- **GitHub Discussions**: 一般讨论和问题
- **邮件**: 私人或敏感问题

### 响应时间
- **bug报告**: 24-48小时内回应
- **功能建议**: 一周内回应
- **PR审查**: 72小时内开始审查

## 📜 许可证

通过贡献代码，您同意您的贡献将在与项目相同的MIT许可证下授权。

## 🙏 致谢

感谢您考虑为AI4QKD做出贡献！每一个贡献都让这个项目变得更好。

---

**欢迎加入AI4QKD开发者社区！让我们一起推进量子密码学和人工智能的融合创新！** 🚀