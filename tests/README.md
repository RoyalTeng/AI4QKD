# AI4QKD 测试目录

本目录包含AI4QKD项目的所有测试文件。

## 📋 测试文件概述

### 主要测试文件
- **test_qcgf_dsl_refactor.py** - qcgf_dsl模块的完整pytest测试套件
- **conftest.py** - pytest配置和共享fixtures

### 功能验证脚本
- **test_basic.py** - 基础功能验证脚本
- **test_refactor.py** - 重构功能验证脚本
- **test_subtypes.py** - 子类型系统测试脚本

### 专项验证脚本
- **verify_refactor.py** - DSL重构验证脚本
- **verify_quantum_memory_removal.py** - 量子存储器移除验证脚本
- **simple_test.py** - 简单的量子存储器移除测试

### 手动测试脚本
- **manual_test.py** - 手动逐步验证脚本

## 🚀 运行测试

### 使用pytest (推荐)
```bash
# 激活conda环境
conda activate ai4qkd_env

# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_qcgf_dsl_refactor.py -v

# 运行特定测试类
python -m pytest tests/test_qcgf_dsl_refactor.py::TestNodeTypesRefactor -v
```

### 直接运行验证脚本
```bash
# 基础功能验证
python tests/test_basic.py

# 简单验证
python tests/simple_test.py

# 手动验证
python tests/manual_test.py
```

## 📊 测试覆盖

当前测试覆盖了以下方面：
- ✅ 节点类型系统
- ✅ 边类型系统  
- ✅ 协议图操作
- ✅ DSL解析和序列化
- ✅ 理想化模式切换
- ✅ 参数验证系统
- ✅ 可视化功能
- ✅ 代码生成功能

## ⚠️ 注意事项

1. **环境依赖**: 确保在 `ai4qkd_env` conda环境中运行测试
2. **编码问题**: 部分测试脚本包含中文输出，在某些终端可能显示为乱码，但功能正常
3. **跳过测试**: 某些pytest测试被标记为SKIPPED，这是正常的，对应未实现的功能

## 🔧 开发指南

### 添加新测试
1. 在相应的测试文件中添加测试函数
2. 使用合适的pytest标记 (unit, integration, performance等)
3. 确保测试独立且可重复运行

### 测试命名规范
- 测试文件: `test_*.py`
- 测试类: `Test*`
- 测试函数: `test_*`

### 调试测试
```bash
# 运行失败的测试并显示详细输出
python -m pytest tests/test_file.py::test_function -v -s

# 运行测试并在第一个失败时停止
python -m pytest tests/ -x --tb=short
```