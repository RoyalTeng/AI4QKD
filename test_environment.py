#!/usr/bin/env python3
"""
AI4QKD环境测试脚本
验证所有依赖包是否正确安装
"""

import sys
import os

def test_environment():
    """测试AI4QKD环境"""
    print("=== AI4QKD 环境测试 ===")
    
    # 检查Python环境
    print(f"✅ Python版本: {sys.version}")
    print(f"✅ Python路径: {sys.executable}")
    
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'base')
    print(f"✅ 当前conda环境: {conda_env}")
    
    # 测试核心包
    packages_to_test = [
        ('torch', 'PyTorch'),
        ('numpy', 'NumPy'),
        ('scipy', 'SciPy'),
        ('pandas', 'Pandas'),
        ('networkx', 'NetworkX'),
        ('matplotlib', 'Matplotlib'),
        ('qiskit', 'Qiskit'),
        ('gymnasium', 'Gymnasium'),
        ('stable_baselines3', 'Stable-Baselines3'),
        ('plotly', 'Plotly'),
        ('cryptography', 'Cryptography'),
        ('sympy', 'SymPy'),
        ('z3', 'Z3-Solver'),
        ('tqdm', 'TQDM'),
        ('yaml', 'PyYAML'),
        ('click', 'Click'),
        ('jupyter', 'Jupyter'),
        ('ipython', 'IPython')
    ]
    
    failed_packages = []
    
    for module_name, display_name in packages_to_test:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name}版本: {version}")
        except ImportError:
            print(f"❌ {display_name}导入失败")
            failed_packages.append(display_name)
    
    # 测试PyTorch CUDA
    try:
        import torch
        print(f"✅ CUDA可用: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✅ CUDA设备: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA版本: {torch.version.cuda}")
    except Exception as e:
        print(f"❌ PyTorch CUDA测试失败: {e}")
    
    # 测试量子计算包
    try:
        import qiskit
        print(f"✅ Qiskit版本: {qiskit.__version__}")
        
        # 测试Qiskit Aer
        from qiskit_aer import Aer
        backend = Aer.get_backend('qasm_simulator')
        print("✅ Qiskit Aer可用")
    except Exception as e:
        print(f"❌ Qiskit测试失败: {e}")
    
    # 测试强化学习环境
    try:
        import gymnasium as gym
        env = gym.make('CartPole-v1')
        print("✅ Gymnasium环境创建成功")
        env.close()
    except Exception as e:
        print(f"❌ Gymnasium测试失败: {e}")
    
    # 测试项目模块
    project_modules = [
        'qcgf_dsl',
        'simulator',
        'security_evaluator',
        'ai_agent',
        'formal_verification',
        'utils'
    ]
    
    print("\n=== 项目模块测试 ===")
    for module_name in project_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}模块导入成功")
        except ImportError as e:
            print(f"❌ {module_name}模块导入失败: {e}")
    
    # 总结
    print("\n=== 测试总结 ===")
    if failed_packages:
        print(f"❌ 失败的包: {', '.join(failed_packages)}")
        print("请检查这些包的安装")
    else:
        print("✅ 所有包测试通过！")
    
    print(f"\n🎉 AI4QKD环境配置{'成功' if not failed_packages else '部分成功'}！")

if __name__ == "__main__":
    test_environment()
