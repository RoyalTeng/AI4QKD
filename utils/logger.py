import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from tqdm import tqdm

class TqdmHandler(logging.StreamHandler):
    """
    一个与tqdm进度条兼容的日志处理器。
    确保日志输出不会打乱tqdm的进度条。
    """
    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)

    def emit(self, record):
        """
        发出一条记录。
        """
        try:
            msg = self.format(record)
            # 使用tqdm.write来安全地打印消息，而不会破坏进度条
            tqdm.write(msg, file=self.stream)
            self.flush()
        except RecursionError: # See issue #1107
            raise
        except Exception:
            self.handleError(record)

def setup_logger(name: str, log_level: str = "INFO", log_file: str = "logs/ai4qkd.log"):
    """
    为指定模块设置日志记录器。

    Args:
        name (str): 日志记录器的名称 (通常是 __name__).
        log_level (str, optional): 日志级别 (e.g., "DEBUG", "INFO", "WARNING"). Defaults to "INFO".
        log_file (str, optional): 日志文件的路径. Defaults to "logs/ai4qkd.log".
    """
    # 创建logs目录
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    log_level_upper = log_level.upper()
    level = getattr(logging, log_level_upper, logging.INFO)

    # 获取指定名称的日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 如果已经有处理器，则不再重复添加，防止重复输出
    if logger.hasHandlers():
        return logger # 如果已经配置过，直接返回

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. 控制台处理器 (与tqdm兼容)
    console_handler = TqdmHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. 文件处理器 (带滚动功能)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger