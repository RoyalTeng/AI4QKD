#!/bin/bash

echo "========================================"
echo "AI4QKD Miniconda 自动化配置脚本"
echo "========================================"
echo

echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python环境检查通过"
echo

echo "开始自动化配置..."
echo "1. 下载Miniconda"
echo "2. 安装Miniconda"
echo "3. 配置conda环境"
echo "4. 创建AI4QKD环境"
echo "5. 安装所有依赖包"
echo

python3 setup_miniconda_automated.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ 配置失败，请检查错误信息"
    exit 1
fi

echo
echo "🎉 配置完成！"
echo
echo "使用说明："
echo "1. 运行 ./activate_ai4qkd.sh 激活环境"
echo "2. 运行 python test_environment.py 验证环境"
echo "3. 运行 python examples/bb84_example.py 测试项目"
echo
