from typing import Dict, Any

def calculate_reward(security_results: Dict[str, Any], protocol_complexity: float) -> float:
    """
    计算给定安全评估结果和协议复杂度的奖励值。

    一个好的奖励函数是AI训练成功的关键。
    它可以是多目标的，例如：
    - 最大化密钥率
    - 惩罚过高的QBER
    - 惩罚过于复杂的协议结构

    Args:
        security_results (Dict[str, Any]): 来自KeyRateCalculator的评估结果。
                                           期望包含 'final_key_rate', 'qber' 等。
        protocol_complexity (float): 一个衡量协议图复杂度的指标（例如，节点数）。

    Returns:
        float: 计算出的奖励值。
    """
    # 初始版本：奖励直接等于最终的安全密钥率
    # security_results 是一个 KeyRateResult 对象，不是字典
    key_rate = security_results.final_key_rate
    qber = security_results.parameters.qber

    reward = key_rate

    # 示例：可以引入对高QBER的惩罚
    if qber > 0.1:  # QBER阈值
        reward -= (qber - 0.1) * 10  # QBER越高，惩罚越大

    # 示例：可以引入对复杂度的惩罚
    # reward -= protocol_complexity * 0.001

    # 确保奖励不会是负无穷大或NaN
    if not isinstance(reward, (int, float)) or not -float('inf') < reward < float('inf'):
        return 0.0

    return reward 