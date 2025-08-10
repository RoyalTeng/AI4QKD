"""
全局配置文件
"""

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "logs/ai4qkd.log"

# 仿真默认参数
DEFAULT_NUM_PULSES = 100000

# AI Agent 训练超参数
# 在10小时内完成训练的推荐配置 (基于~20秒/步的估算)
NUM_EPISODES = 5           # 总训练回合数
MAX_STEPS_PER_EPISODE = 20  # 每个回合的最大步数
SAVE_CHECKPOINT_INTERVAL = 1 # 每隔多少个回合保存一次模型
INVALID_PROTOCOL_PENALTY = -100.0 # 当协议被修改为无效状态时的惩罚值

# 训练日志保存策略
SAVE_EPISODE_INTERVAL = 5  # 每隔多少个回合保存一次详细记录
SAVE_ONLY_IF_KEYRATE_IMPROVES = True  # 是否只在密钥率改进时保存回合记录

# 可视化设置
FIG_SIZE = (10, 6)
DPI = 300 