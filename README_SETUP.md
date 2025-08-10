# AI4QKD Miniconda 自动化配置指南

## 🚀 一键配置（推荐）

### Windows用户
1. 确保已安装Python 3.8+
2. 双击运行 `quick_setup.bat`
3. 等待自动配置完成

### Linux/macOS用户
1. 确保已安装Python 3.8+
2. 运行 `./quick_setup.sh`
3. 等待自动配置完成

## 📋 配置内容

自动化脚本将完成以下操作：

1. **下载Miniconda** - 自动下载适合您系统的Miniconda安装程序
2. **安装Miniconda** - 静默安装到默认位置
3. **配置conda环境** - 初始化conda并配置源
4. **创建AI4QKD环境** - 创建专用的conda环境
5. **安装所有依赖** - 自动安装所有必需的包
6. **创建项目目录** - 设置必要的目录结构
7. **生成激活脚本** - 创建便捷的环境激活脚本

## 🎯 安装的包

### 深度学习框架
- PyTorch 2.5.1 (CUDA 12.1)
- PyTorch Geometric 2.6.1
- Transformers 4.30.0+

### 强化学习
- Stable-Baselines3 2.0.0+
- Gymnasium 1.1.1

### 量子计算
- Qiskit 2.1.0
- Qiskit Aer 0.17.1
- QuTiP 5.0.4
- Cirq 1.2.0+

### 科学计算
- NumPy 1.23.5
- SciPy 1.13.1
- Pandas 2.2.3
- NetworkX 3.2.1

### 可视化
- Matplotlib 3.9.4
- Plotly 5.15.0+

### 工具库
- TQDM 4.67.1
- PyYAML 6.0.2
- Click 8.1.0+
- Cryptography 41.0.0+
- SymPy 1.13.1
- Z3-Solver 4.15.1.0

## 🔧 使用说明

### 激活环境

**Windows:**
```bash
# 双击运行
activate_ai4qkd.bat

# 或命令行运行
C:\Miniconda3\Scripts\activate.bat ai4qkd
```

**Linux/macOS:**
```bash
# 运行脚本
./activate_ai4qkd.sh

# 或直接激活
source ~/miniconda3/bin/activate ai4qkd
```

### 验证环境
```bash
python test_environment.py
```

### 运行示例
```bash
# BB84协议示例
python examples/bb84_example.py

# AI训练示例
python main.py --mode design
```

## 🛠️ 故障排除

### 常见问题

1. **Python未找到**
   - 确保已安装Python 3.8+
   - 检查PATH环境变量

2. **下载失败**
   - 检查网络连接
   - 尝试使用VPN或代理

3. **安装失败**
   - 检查磁盘空间
   - 以管理员权限运行

4. **CUDA问题**
   - 检查NVIDIA驱动
   - 验证CUDA版本兼容性

### 手动安装

如果自动安装失败，可以手动执行：

```bash
# 1. 下载Miniconda
# 访问 https://anaconda.com/download

# 2. 安装Miniconda
# 运行下载的安装程序

# 3. 创建环境
conda create -n ai4qkd python=3.10 -y

# 4. 激活环境
conda activate ai4qkd

# 5. 安装包
conda install pytorch=2.5.1 torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install torch-geometric==2.6.1 transformers>=4.30.0 stable-baselines3>=2.0.0
conda install -c conda-forge qiskit=2.1.0 gymnasium=1.1.1 -y
# ... 其他包
```

## 📞 技术支持

如果遇到问题，请：

1. 检查错误日志
2. 运行 `python test_environment.py` 查看详细状态
3. 查看项目文档
4. 提交Issue到项目仓库

## 🎉 完成配置

配置完成后，您就可以开始使用AI4QKD项目进行量子AI协议的研究了！

- 阅读项目README.md了解项目架构
- 运行示例代码熟悉使用方法
- 开始您的量子AI研究之旅
