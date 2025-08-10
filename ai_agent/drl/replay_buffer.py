import random
from collections import deque
import numpy as np

class ReplayBuffer:
    """
    一个简单的先进先出（FIFO）经验回放缓冲区，用于DDPG、TD3或SAC等离策略算法。
    """
    def __init__(self, capacity: int):
        """
        初始化回放缓冲区。

        Args:
            capacity (int): 缓冲区的最大容量。
        """
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """
        将一个经验元组 (s, a, r, s', done) 添加到缓冲区。
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        """
        从缓冲区中随机采样一批经验。

        Args:
            batch_size (int): 采样的批量大小。

        Returns:
            一个包含状态、动作、奖励、下一个状态和完成标志的元组，均为NumPy数组。
        """
        # 随机抽取一批经验
        batch = random.sample(self.buffer, batch_size)
        
        # 将经验元组解压
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        
        return state, action, reward, next_state, done

    def __len__(self) -> int:
        """返回当前缓冲区中的经验数量。"""
        return len(self.buffer)

class OnPolicyBuffer:
    """
    一个用于在策略（On-Policy）算法（如PPO）的缓冲区。
    这个缓冲区在每次更新后都会清空。
    """
    def __init__(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.is_terminals = []
    
    def clear(self):
        """清空所有列表。"""
        del self.actions[:]
        del self.states[:]
        del self.logprobs[:]
        del self.rewards[:]
        del self.is_terminals[:]

    def __len__(self) -> int:
        """返回存储的经验数量。"""
        return len(self.states) 