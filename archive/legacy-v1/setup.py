#!/usr/bin/env python3
"""
AI4QKD项目设置脚本
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def check_python():
    """检查Python"""
    print_header("检查Python环境")
    
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python版本满足要求")
        return True
    else:
        print("❌ 需要Python 3.8+")
        return False


def create_venv():
    """创建虚拟环境"""
    print_header("创建虚拟环境")
    
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print(f"虚拟环境已存在: {venv_dir}")
        return True
    
    try:
        print("创建虚拟环境...")
        venv.create(venv_dir, with_pip=True)
        print("✅ 虚拟环境创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False


def install_deps():
    """安装依赖"""
    print_header("安装依赖")
    
    if sys.platform == "win32":
        pip = "venv/Scripts/pip"
    else:
        pip = "venv/bin/pip"
    
    if not os.path.exists(pip):
        print(f"❌ 找不到pip: {pip}")
        return False
    
    try:
        print("安装核心依赖...")
        subprocess.run([pip, "install", "numpy", "scipy", "networkx"], check=True)
        print("✅ 依赖安装成功")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False


def create_dirs():
    """创建目录"""
    print_header("创建项目目录")
    
    dirs = ["results", "data", "logs"]
    
    try:
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            print(f"创建目录: {d}")
        print("✅ 目录创建完成")
        return True
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False


def run_test():
    """运行测试"""
    print_header("运行测试")
    
    if sys.platform == "win32":
        python = "venv/Scripts/python"
    else:
        python = "venv/bin/python"
    
    if not os.path.exists(python):
        print("❌ 找不到Python")
        return False
    
    # 创建简单测试
    test_code = '''
import sys
sys.path.insert(0, '.')

try:
    from qcgf_dsl import ProtocolGraph
    print("✅ QCGF DSL导入成功")
    
    protocol = ProtocolGraph.create_bb84()
    print(f"✅ BB84协议创建成功: {protocol.name}")
    
    print("🎉 基础测试通过！")
    sys.exit(0)
except Exception as e:
    print(f"❌ 测试失败: {e}")
    sys.exit(1)
'''
    
    try:
        result = subprocess.run([python, "-c", test_code], 
                               capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("✅ 测试通过")
            return True
        else:
            print("❌ 测试失败")
            return False
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False


def print_instructions():
    """打印使用说明"""
    print_header("使用说明")
    
    if sys.platform == "win32":
        print("激活虚拟环境:")
        print("  venv\\Scripts\\activate")
    else:
        print("激活虚拟环境:")
        print("  source venv/bin/activate")
    
    print("\n运行示例:")
    print("  python examples/bb84_example.py")
    
    print("\n项目结构:")
    print("  ai_agent/     - AI智能体模块")
    print("  qcgf_dsl/     - 量子协议DSL")
    print("  simulator/    - 量子仿真器")
    print("  examples/     - 使用示例")
    print("  results/      - 输出结果")


def main():
    """主函数"""
    print_header("AI4QKD项目设置")
    print("版本: 1.0.0")
    print("描述: AI辅助量子密钥分发协议设计")
    
    steps = [
        ("Python检查", check_python),
        ("目录创建", create_dirs),
        ("虚拟环境", create_venv),
        ("依赖安装", install_deps),
        ("运行测试", run_test)
    ]
    
    all_ok = True
    for name, func in steps:
        if not func():
            print(f"⚠️  {name}步骤有问题")
            all_ok = False
    
    if all_ok:
        print_header("🎉 设置完成！")
        print_instructions()
        return 0
    else:
        print_header("⚠️  设置有问题")
        print("部分步骤失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n设置被中断")
        sys.exit(1)