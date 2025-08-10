from typing import List, Dict, Any
import numpy as np
import pandas as pd

def compute_key_rate_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    计算与密钥率相关的性能指标。

    Args:
        results (List[Dict[str, Any]]): 包含多次实验结果的列表，
                                       每个字典应包含 'key_rate', 'qber' 等键。

    Returns:
        Dict[str, float]: 包含平均值、标准差等统计指标的字典。
    """
    if not results:
        return {}
        
    df = pd.DataFrame(results)
    
    metrics = {
        "average_key_rate": df["key_rate"].mean(),
        "std_dev_key_rate": df["key_rate"].std(),
        "max_key_rate": df["key_rate"].max(),
        "min_key_rate": df["key_rate"].min(),
        "average_qber": df["qber"].mean(),
    }
    return metrics

def track_drl_learning_curve(rewards: List[float], window_size: int = 100) -> Dict[str, Any]:
    """
    跟踪并计算DRL智能体的学习曲线指标。

    Args:
        rewards (List[float]): DRL训练过程中每一步的奖励列表。
        window_size (int, optional): 用于计算移动平均的窗口大小. Defaults to 100.

    Returns:
        Dict[str, Any]: 包含总奖励、移动平均奖励等信息的字典。
    """
    if not rewards:
        return {}
        
    rewards_series = pd.Series(rewards)
    moving_average = rewards_series.rolling(window=window_size, min_periods=1).mean().tolist()
    
    return {
        "total_episodes": len(rewards),
        "total_reward": sum(rewards),
        "average_reward": np.mean(rewards),
        "moving_average_reward": moving_average
    }

def calculate_protocol_complexity(graph) -> int:
    """
    计算协议的复杂度，一个简单的示例是节点和边的总数。

    Args:
        graph: qcgf_dsl.protocol_graph.ProtocolGraph 对象。

    Returns:
        int: 协议的复杂度得分。
    """
    return graph.get_node_count() + graph.get_edge_count() 