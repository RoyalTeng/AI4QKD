"""
项目设置
"""

import os


class Settings:
    """项目设置"""
    
    # 日志配置
    LOG_LEVEL = "INFO"
    
    # 仿真配置
    DEFAULT_PULSE_COUNT = 10000
    DEFAULT_CHANNEL_LOSS = 0.1
    
    # AI配置
    DEFAULT_POPULATION_SIZE = 20
    DEFAULT_TRAINING_ITERATIONS = 50
    
    # 文件路径
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
    
    @classmethod
    def ensure_directories(cls):
        """确保目录存在"""
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)