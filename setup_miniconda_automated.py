#!/usr/bin/env python3
"""
AI4QKD Miniconda自动化配置脚本
自动下载、安装和配置Miniconda环境
"""

import os
import sys
import subprocess
import platform
import urllib.request
import hashlib
import zipfile
import tarfile
from pathlib import Path

class MinicondaAutoSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.python_version = "3.10"
        self.miniconda_version = "latest"
        self.install_dir = None
        
    def get_download_url(self):
        """获取Miniconda下载URL"""
        base_url = "https://repo.anaconda.com/miniconda"
        
        if self.system == "windows":
            if "64" in self.machine or "x86_64" in self.machine:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-Windows-x86_64.exe"
            else:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-Windows-x86.exe"
        elif self.system == "linux":
            if "64" in self.machine or "x86_64" in self.machine:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-Linux-x86_64.sh"
            else:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-Linux-x86.sh"
        elif self.system == "darwin":  # macOS
            if "arm" in self.machine or "aarch64" in self.machine:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-MacOSX-arm64.sh"
            else:
                return f"{base_url}/Miniconda3-{self.miniconda_version}-MacOSX-x86_64.sh"
        else:
            raise ValueError(f"不支持的操作系统: {self.system}")
    
    def download_miniconda(self):
        """下载Miniconda安装程序"""
        url = self.get_download_url()
        filename = url.split('/')[-1]
        
        print(f"正在下载Miniconda: {url}")
        print(f"文件名: {filename}")
        
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"✅ 下载完成: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None
    
    def install_miniconda(self, installer_path):
        """安装Miniconda"""
        print(f"正在安装Miniconda: {installer_path}")
        
        if self.system == "windows":
            # Windows静默安装
            cmd = [installer_path, "/S", "/D=C:\\Miniconda3"]
            self.install_dir = "C:\\Miniconda3"
        else:
            # Linux/macOS安装
            cmd = ["bash", installer_path, "-b", "-p", f"{os.path.expanduser('~')}/miniconda3"]
            self.install_dir = f"{os.path.expanduser('~')}/miniconda3"
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Miniconda安装完成: {self.install_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装失败: {e}")
            return False
    
    def setup_conda_environment(self):
        """设置conda环境"""
        # 添加conda到PATH
        if self.system == "windows":
            conda_path = f"{self.install_dir}\\Scripts\\conda.exe"
        else:
            conda_path = f"{self.install_dir}/bin/conda"
        
        # 初始化conda
        try:
            subprocess.run([conda_path, "init"], check=True)
            print("✅ Conda初始化完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ Conda初始化失败: {e}")
            return False
        
        return True
    
    def create_ai4qkd_environment(self):
        """创建AI4QKD环境"""
        print("正在创建AI4QKD环境...")
        
        # 创建环境文件
        env_content = """name: ai4qkd
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - numpy=1.23.5
  - scipy=1.13.1
  - pandas=2.2.3
  - matplotlib=3.9.4
  - networkx=3.2.1
  - jupyter
  - ipython=8.12.0
  - tqdm=4.67.1
  - pyyaml=6.0.2
  - click
  - pytorch=2.5.1
  - torchvision
  - torchaudio
  - pytorch-cuda=12.1
  - gymnasium=1.1.1
  - qiskit=2.1.0
  - qiskit-aer=0.17.1
  - qutip=5.0.4
  - cryptography
  - pycryptodome
  - z3-solver=4.15.1.0
  - sympy=1.13.1
  - plotly
  - pip
  - pip:
    - torch-geometric==2.6.1
    - transformers>=4.30.0
    - stable-baselines3>=2.0.0
    - cirq>=1.2.0
"""
        
        with open("ai4qkd_environment.yml", "w") as f:
            f.write(env_content)
        
        print("✅ 环境文件创建完成")
        
        # 创建环境
        try:
            if self.system == "windows":
                conda_cmd = f"{self.install_dir}\\Scripts\\conda.exe"
            else:
                conda_cmd = f"{self.install_dir}/bin/conda"
            
            subprocess.run([conda_cmd, "env", "create", "-f", "ai4qkd_environment.yml"], check=True)
            print("✅ AI4QKD环境创建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 环境创建失败: {e}")
            return False
    
    def setup_project_directories(self):
        """设置项目目录"""
        directories = [
            "logs/ai_training",
            "checkpoints",
            "results",
            "docs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ 项目目录创建完成")
    
    def create_activation_script(self):
        """创建激活脚本"""
        if self.system == "windows":
            script_content = f"""@echo off
echo 正在激活AI4QKD环境...
call "{self.install_dir}\\Scripts\\activate.bat" ai4qkd
echo 环境激活完成！
echo 当前Python路径: %CONDA_PREFIX%\\python.exe
cmd /k
"""
            with open("activate_ai4qkd.bat", "w") as f:
                f.write(script_content)
        else:
            script_content = f"""#!/bin/bash
echo "正在激活AI4QKD环境..."
source "{self.install_dir}/bin/activate" ai4qkd
echo "环境激活完成！"
echo "当前Python路径: $CONDA_PREFIX/bin/python"
exec bash
"""
            with open("activate_ai4qkd.sh", "w") as f:
                f.write(script_content)
            os.chmod("activate_ai4qkd.sh", 0o755)
        
        print("✅ 激活脚本创建完成")
    
    def run(self):
        """运行完整的自动化配置"""
        print("🚀 开始AI4QKD Miniconda自动化配置...")
        print(f"操作系统: {self.system}")
        print(f"架构: {self.machine}")
        
        # 1. 下载Miniconda
        installer = self.download_miniconda()
        if not installer:
            return False
        
        # 2. 安装Miniconda
        if not self.install_miniconda(installer):
            return False
        
        # 3. 设置conda环境
        if not self.setup_conda_environment():
            return False
        
        # 4. 创建AI4QKD环境
        if not self.create_ai4qkd_environment():
            return False
        
        # 5. 设置项目目录
        self.setup_project_directories()
        
        # 6. 创建激活脚本
        self.create_activation_script()
        
        print("\n🎉 AI4QKD Miniconda配置完成！")
        print("\n📋 使用说明:")
        if self.system == "windows":
            print("1. 双击运行: activate_ai4qkd.bat")
        else:
            print("1. 运行: ./activate_ai4qkd.sh")
        print("2. 验证环境: python test_environment.py")
        print("3. 运行示例: python examples/bb84_example.py")
        
        return True

def main():
    """主函数"""
    setup = MinicondaAutoSetup()
    success = setup.run()
    
    if success:
        print("\n✅ 配置成功完成！")
        sys.exit(0)
    else:
        print("\n❌ 配置失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
