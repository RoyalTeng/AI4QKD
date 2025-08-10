import numpy as np
from typing import Callable

class EvolutionStrategy:
    """
    演化策略 (ES) 算法框架。
    适用于参数优化，特别是当梯度难以计算时。
    """
    def __init__(self,
                 mean_vector: np.ndarray,
                 stdev_vector: np.ndarray,
                 population_size: int,
                 learning_rate: float,
                 fitness_fn: Callable[[np.ndarray], float]):
        """
        初始化演化策略。

        Args:
            mean_vector (np.ndarray): 参数分布的均值向量。
            stdev_vector (np.ndarray): 参数分布的标准差向量。
            population_size (int): 种群大小（必须是偶数）。
            learning_rate (float): 均值和标准差更新的学习率。
            fitness_fn (Callable): 适应度函数。
        """
        self.mean = mean_vector
        self.stdev = stdev_vector
        self.population_size = population_size
        self.learning_rate = learning_rate
        self.fitness_fn = fitness_fn

    def step(self):
        """
        执行一步演化。
        """
        # 1. 从高斯分布中采样种群
        noise = np.random.randn(self.population_size, len(self.mean))
        population = self.mean + self.stdev * noise

        # 2. 评估适应度
        fitness_scores = np.array([self.fitness_fn(individual) for individual in population])
        
        # 3. 计算梯度近似
        # 使用适应度分数作为权重来更新均值
        # 将噪声向量按适应度加权求和
        gradient_approx = np.dot(noise.T, fitness_scores) / (self.population_size * self.stdev)

        # 4. 更新均值（梯度上升）
        self.mean += self.learning_rate * gradient_approx
        
        # 可选：也可以更新标准差，例如使用 CMA-ES

    def run(self, generations: int):
        """
        运行完整的演化过程。
        """
        for gen in range(generations):
            self.step()
            # 评估当前均值的适应度作为代表
            current_fitness = self.fitness_fn(self.mean)
            print(f"Generation {gen+1}/{generations}, Current Fitness: {current_fitness}")
        return self.mean 