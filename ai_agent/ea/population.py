from typing import List, Callable, Any, Optional
import random

class Population:
    """
    种群管理类，用于演化算法。
    """
    def __init__(self,
                 population_size: int,
                 initialization_fn: Callable[[int], List[Any]],
                 fitness_fn: Callable[[Any], float]):
        """
        初始化种群。

        Args:
            population_size (int): 种群大小。
            initialization_fn (Callable): 用于创建初始种群的函数。
            fitness_fn (Callable): 评估单个个体适应度的函数。
        """
        self.population_size = population_size
        self.initialization_fn = initialization_fn
        self.fitness_fn = fitness_fn
        self.individuals = self.initialization_fn(self.population_size)
        self.fitness_scores = [self.fitness_fn(ind) for ind in self.individuals]

    def evaluate_fitness(self):
        """重新评估整个种群的适应度。"""
        self.fitness_scores = [self.fitness_fn(ind) for ind in self.individuals]

    def get_best_individual(self) -> Any:
        """返回当前种群中适应度最高的个体。"""
        best_index = self.fitness_scores.index(max(self.fitness_scores))
        return self.individuals[best_index]

    def get_fitness_statistics(self) -> dict:
        """返回适应度的统计信息。"""
        return {
            "max": max(self.fitness_scores),
            "min": min(self.fitness_scores),
            "avg": sum(self.fitness_scores) / len(self.fitness_scores)
        }

    def replacement(self,
                    new_individuals: List[Any],
                    strategy: str = "elitism"):
        """
        用新个体替换旧种群。

        Args:
            new_individuals (List[Any]): 用于替换的新个体列表。
            strategy (str, optional): 替换策略。
                                      "elitism": 保留上一代最优个体。
                                      "full": 完全替换。
                                      Defaults to "elitism".
        """
        if strategy == "elitism":
            best_old_individual = self.get_best_individual()
            self.individuals = new_individuals
            self.evaluate_fitness()
            # 寻找新种群中最差个体并用旧种群的最优个体替换
            worst_new_index = self.fitness_scores.index(min(self.fitness_scores))
            self.individuals[worst_new_index] = best_old_individual
            self.evaluate_fitness()
        elif strategy == "full":
            self.individuals = new_individuals
            self.evaluate_fitness()
        else:
            raise ValueError(f"未知的替换策略: {strategy}")
            
    def tournament_selection(self, k: int = 3) -> List[Any]:
        """
        锦标赛选择。

        Args:
            k (int): 锦标赛的大小。

        Returns:
            List[Any]: 被选中的父代列表。
        """
        parents = []
        for _ in range(self.population_size):
            tournament = random.sample(list(zip(self.individuals, self.fitness_scores)), k)
            # 按适应度排序，选择最优者
            winner = max(tournament, key=lambda item: item[1])[0]
            parents.append(winner)
        return parents 