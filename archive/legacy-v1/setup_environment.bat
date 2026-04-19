@echo off
echo AI4QKD深度学习环境配置脚本
echo ================================

echo 步骤1: 检查Python安装
python --version
if %errorlevel% neq 0 (
    echo Python未安装，请先从 https://www.python.org/downloads/ 下载并安装Python
    echo 安装时请选择"Add to PATH"选项
    echo 建议安装位置：D:\Python
    pause
    exit /b
)

echo 步骤2: 创建虚拟环境（D盘）
mkdir D:\AI4QKD_env
python -m venv D:\AI4QKD_env\venv

echo 步骤3: 激活虚拟环境
call D:\AI4QKD_env\venv\Scripts\activate

echo 步骤4: 升级pip到最新版本
python -m pip install --upgrade pip

echo 步骤5: 配置pip使用D盘缓存
pip config set global.cache-dir D:\AI4QKD_env\pip_cache

echo 步骤6: 安装PyTorch (CUDA版本)
echo 检测CUDA版本...
nvidia-smi
if %errorlevel% equ 0 (
    echo 检测到NVIDIA GPU，安装CUDA版本的PyTorch
    pip install torch==2.5.1+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
) else (
    echo 未检测到NVIDIA GPU，安装CPU版本的PyTorch
    pip install torch==2.5.1+cpu torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
)

echo 步骤7: 安装项目依赖
pip install -r requirements.txt

echo 步骤8: 以开发模式安装项目
pip install -e .

echo 步骤9: 验证安装
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'GPU数量: {torch.cuda.device_count()}')"

echo 步骤10: 运行测试
pytest tests/ -v

echo ================================
echo 环境配置完成！
echo 虚拟环境位置：D:\AI4QKD_env\venv
echo 激活命令：D:\AI4QKD_env\venv\Scripts\activate
echo ================================
pause