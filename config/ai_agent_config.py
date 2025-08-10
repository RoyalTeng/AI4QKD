"""
AI智能体优化器默认超参数配置
"""

def get_default_ai_agent_config():
    """返回AI优化器默认超参数字典"""
    return {
        'learning_rate': 0.001,
        'batch_size': 64,
        'gamma': 0.99,
        'buffer_size': 100000,
        'tau': 0.005,
        'hidden_dim': 128,
        'max_episodes': 500,
        'max_steps': 200,
        'seed': 42
    } 