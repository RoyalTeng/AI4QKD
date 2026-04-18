@echo off
echo ========================================
echo AI4QKD Miniconda 自动化配置脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 开始自动化配置...
echo 1. 下载Miniconda
echo 2. 安装Miniconda
echo 3. 配置conda环境
echo 4. 创建AI4QKD环境
echo 5. 安装所有依赖包
echo.

python setup_miniconda_automated.py

if errorlevel 1 (
    echo.
    echo ❌ 配置失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 🎉 配置完成！
echo.
echo 使用说明：
echo 1. 双击运行 activate_ai4qkd.bat 激活环境
echo 2. 运行 python test_environment.py 验证环境
echo 3. 运行 python examples/bb84_example.py 测试项目
echo.
pause
