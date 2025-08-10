#!/usr/bin/env python3
"""
AI辅助QKD协议设计系统主程序
"""

from config import settings
# from qcgf_dsl.protocol_graph import ProtocolGraph  # 已在env中，此处可不直接使用
# from simulator.quantum_simulator import QuantumSimulator
# from security_evaluator.key_rate_calculator import KeyRateCalculator
from ai_agent.hybrid_agent import HybridAgent
# from formal_verification.protocol_verifier import ProtocolVerifier
from utils.logger import setup_logger
from utils.training_logger import TrainingLogger # 导入新的日志记录器
from ai_agent.environment import QKDSimEnv
import logging
import json
import os
import argparse # 导入argparse
from pathlib import Path
import csv
from typing import Dict, Optional # 重新导入 Dict
import torch
from datetime import datetime

# import pandas as pd # 不再需要pandas来保存CSV

# 猴子补丁：为 qiskit 库中可能存在的旧版日志调用提供兼容性
# Qiskit 的某些旧代码或依赖可能仍在调用 .warn() 而不是 .warning()
if not hasattr(logging.Logger, 'warn'):
    logging.Logger.warn = logging.Logger.warning

# --- 路径定义 (由TrainingLogger管理) ---
# CHECKPOINT_DIR = "checkpoints"
# RESULTS_FILE = "training_results.csv"

def get_config_dict(settings_module):
    """从settings模块中提取所有大写变量，转换为配置字典。"""
    return {key: getattr(settings_module, key) for key in dir(settings_module) if key.isupper()}

# 以下旧的保存/加载函数将被TrainingLogger的功能所取代
# def save_checkpoint(...):
# def load_checkpoint(...):
# def save_results(...):

def load_initial_state(resume_id: str, agent: HybridAgent, episode_num: Optional[int] = None) -> int:
    """
    从指定的运行ID加载模型状态，并确定起始回合数。
    此函数只负责加载状态，不创建新的logger。

    Args:
        resume_id: 要从中恢复的运行ID。
        agent: 要加载权重的Agent实例。
        episode_num: 要加载模型的指定回合数 (可选)。

    Returns:
        起始回合数。
    """
    logger = logging.getLogger(__name__)
    logger.info(f"正在从 run_id '{resume_id}' 恢复训练")
    
    results_dir = Path("results") / resume_id
    if not results_dir.exists():
        logger.error(f"错误: 无法找到指定的恢复目录！\n路径 '{results_dir}' 不存在。\n请检查您的 --resume_id 是否正确。")
        return 0

    model_path_to_load = None
    if episode_num is not None:
        # 优先加载指定回合的模型
        model_path = results_dir / "episodes" / f"episode_{episode_num:04d}" / "model.pt"
        if model_path.exists():
            model_path_to_load = model_path
        else:
            logger.error(f"错误: 在 {model_path} 未找到指定的模型文件！请检查回合号是否正确。")
            raise FileNotFoundError(f"Model for episode {episode_num} not found.")
    else:
        # 否则，加载 'best' 或 'latest' 模型
        best_model_path = results_dir / "best" / "model.pt"
        latest_model_path = results_dir / "latest" / "model.pt"
        if best_model_path.exists():
            model_path_to_load = best_model_path
            logger.info(f"找到并使用最佳模型文件: {best_model_path}")
        elif latest_model_path.exists():
            model_path_to_load = latest_model_path
            logger.info(f"找到并使用最新模型文件: {latest_model_path}")

    if model_path_to_load:
        agent.load_models(str(model_path_to_load))
        logger.info(f"✅ 成功加载模型: {model_path_to_load}")
    else:
        logger.warning(f"❌ 未找到任何可加载的模型文件，将使用随机初始化的新模型。")

    # 通过日志文件确定下一个回合的编号
    action_log_path = Path("logs") / "ai_training" / resume_id / "action_log.csv"
    if not action_log_path.exists():
        logger.warning(f"在 {action_log_path} 未找到日志文件，将从第0回合开始。")
        return 0
    
    try:
        # 读取CSV以确定最后一个记录的step
        import pandas as pd
        df = pd.read_csv(action_log_path)
        if not df.empty:
            last_step = df['step'].max()
            # 从配置中获取每回合的步数
            config = get_config_dict(settings)
            max_steps = config.get("MAX_STEPS_PER_EPISODE", 20) # 使用默认值以防万一
            start_episode = (last_step // max_steps) + 1
            logger.info(f"从日志中恢复进度：最后完成的步骤是 {last_step}，将从第 {start_episode} 回合继续。")
            return int(start_episode)
    except Exception as e:
        logger.error(f"读取日志恢复进度时出错: {e}。将从第0回合开始。")
    
    return 0

def convert_to_dict(obj, max_depth=10, seen=None):
    """
    递归地将对象转换为字典，包含循环引用检测和深度限制
    
    Args:
        obj: 要转换的对象
        max_depth: 最大递归深度
        seen: 已访问对象的集合，用于循环引用检测
    """
    if seen is None:
        seen = set()
    
    if max_depth <= 0:
        return f"<MAX_DEPTH_REACHED: {type(obj).__name__}>"
    
    # 避免循环引用
    if id(obj) in seen:
        return f"<CIRCULAR_REFERENCE: {type(obj).__name__}>"
    
    # 基本类型直接返回
    if obj is None or isinstance(obj, (int, float, str, bool)):
        return obj
    
    # 处理numpy类型
    if hasattr(obj, 'dtype') and hasattr(obj, 'tolist'):
        try:
            return obj.tolist()
        except:
            return str(obj)
    
    # 处理枚举类型
    if hasattr(obj, 'value'):
        return obj.value
    
    # 处理数组/列表
    if isinstance(obj, (list, tuple)):
        return [convert_to_dict(item, max_depth-1, seen) for item in obj]
    
    # 处理字典
    if isinstance(obj, dict):
        return {key: convert_to_dict(value, max_depth-1, seen) for key, value in obj.items()}
    
    # 处理复杂对象
    if hasattr(obj, '__dict__'):
        seen.add(id(obj))
        try:
            result = {}
            for key, value in obj.__dict__.items():
                # 跳过私有属性和方法
                if key.startswith('_'):
                    continue
                try:
                    result[key] = convert_to_dict(value, max_depth-1, seen)
                except Exception as e:
                    result[key] = f"<ERROR_CONVERTING: {type(value).__name__}: {str(e)[:100]}>"
            return result
        finally:
            seen.remove(id(obj))
    
    # 其他类型转换为字符串
    return str(obj)

def main(args):
    """主函数：运行AI训练流程"""
    # --- 1. 初始化 ---
    setup_logger(__name__, settings.LOG_LEVEL, settings.LOG_FILE)
    logger = logging.getLogger(__name__)
    config = get_config_dict(settings)
    
    env = QKDSimEnv(config)
    agent = HybridAgent(config)

    start_episode = 0
    origin_run_id = None
    if args.resume_id:
        origin_run_id = args.resume_id
        start_episode = load_initial_state(args.resume_id, agent, args.episode)

    # --- 2. 初始化新的 TrainingLogger ---
    training_logger = TrainingLogger(
        run_id=args.run_id,  # 允许通过命令行指定新run_id
        config=config,
        flush_interval=config.get("FLUSH_INTERVAL", 50),
        save_episode_interval=config.get("SAVE_EPISODE_INTERVAL", settings.SAVE_EPISODE_INTERVAL),
        save_only_if_keyrate_improves=config.get("SAVE_ONLY_IF_KEYRATE_IMPROVES", settings.SAVE_ONLY_IF_KEYRATE_IMPROVES),
        base_model_path=str(agent.model_path) if hasattr(agent, 'model_path') else None,
        origin_run_id=origin_run_id
    )
    
    logger.info("开始AI训练")
    logger.info(f"Run ID: {training_logger.run_id}")
    logger.info(f"计划训练回合数: {config['NUM_EPISODES']}")
    logger.info(f"起始回合: {start_episode}")

    total_steps = 0
    start_time = datetime.now()

    # --- 3. 训练循环 ---
    num_episodes_to_run = config["NUM_EPISODES"]
    max_steps_per_episode = config["MAX_STEPS_PER_EPISODE"]

    logger.info(f"🔄 开始训练循环，总共需要运行 {num_episodes_to_run} 个回合")
    
    for i in range(num_episodes_to_run):
        current_episode = start_episode + i
        logger.info(f"🎯 开始第 {i+1}/{num_episodes_to_run} 个回合 (回合ID: {current_episode})")
        
        obs, info = env.reset()
        done = False
        total_reward = 0
        step_count = 0
        
        while not done:
            # 1. Agent选择动作
            action = env.action_space.sample()  # 暂时使用随机动作

            # 2. 环境执行动作
            next_obs, reward, done, truncated, info = env.step(action)
            
            # 3. Agent学习
            # agent.drl_agent.remember(...)
            # loss = agent.drl_agent.train()
            loss = 1.0 / (step_count + 1)  # 伪造的loss数据
            
            # 4. 记录每一步的详细信息
            security_results = info.get('security_results', {})
            if isinstance(security_results, dict):
                key_rate = security_results.get('final_key_rate', 0.0)
                entropy = security_results.get('h_min', 0.0)
            else:
                # 如果是 KeyRateResult 对象
                key_rate = getattr(security_results, 'final_key_rate', 0.0)
                entropy = getattr(security_results, 'h_min', 0.0)

            training_logger.step(
                step=total_steps,
                loss=loss,
                reward=reward,
                key_rate=key_rate,
                entropy=entropy,
                actions=action
            )

            obs = next_obs
            total_reward += reward
            step_count += 1
            total_steps += 1
            
            if step_count >= max_steps_per_episode:
                done = True

        # --- 4. 回合结束处理 ---
        logger.info(f"回合 {current_episode} 完成 | 总奖励: {total_reward:.4f}")
        
        try:
            logger.info(f"🔄 开始保存回合 {current_episode} 的结果...")
            
            # 获取最新的协议和评估结果以供保存
            logger.info("正在获取协议图...")
            protocol_dict = env.protocol_graph.to_dict()
            logger.info(f"✅ 协议图获取成功，包含 {len(protocol_dict)} 项")
            
            # 从最后一步的info中获取密钥率结果
            logger.info("正在获取密钥率结果...")
            keyrate_dict = info.get('security_results', {})
            keyrate_dict = convert_to_dict(keyrate_dict)
            logger.info(f"✅ 密钥率结果获取成功，包含 {len(keyrate_dict)} 项")
            
            logger.info("正在调用 training_logger.save_episode_result...")
            training_logger.save_episode_result(
                episode_id=current_episode,
                model=agent,
                protocol_dict=protocol_dict,
                keyrate_dict=keyrate_dict
            )
            logger.info(f"✅ 回合 {current_episode} 结果已保存")
        except Exception as e:
            logger.error(f"❌ 保存回合 {current_episode} 结果时出错: {e}")
            logger.error(f"错误类型: {type(e).__name__}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            # 不要因为保存失败而停止训练
            pass
        
        logger.info(f"🏁 第 {i+1}/{num_episodes_to_run} 个回合 (回合ID: {current_episode}) 处理完成")

    # --- 5. 训练结束 ---
    logger.info("🎉 所有训练回合完成")
    logger.info("训练完成")
    
    training_duration = (datetime.now() - start_time).total_seconds()
    
    # 获取最终产物
    final_protocol = env.protocol_graph.to_dict()
    final_keyrate = info.get('security_results', {})
    final_keyrate = convert_to_dict(final_keyrate)

    training_logger.save_all(
        agent_name=agent.name if hasattr(agent, 'name') else "HybridAgent",
        total_steps=total_steps,
        total_episodes=start_episode + num_episodes_to_run,
        training_duration_sec=training_duration,
        model=agent,
        protocol_dict=final_protocol,
        keyrate_dict=final_keyrate
    )
    
    logger.info(f"训练总结和图表已保存到: {training_logger.results_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-assisted QKD Protocol Design System")
    parser.add_argument(
        '--run_id', 
        type=str, 
        default=None, 
        help="Specify a custom run ID for the new training run."
    )
    parser.add_argument(
        '--resume_id', 
        type=str, 
        default=None, 
        help="Provide the run_id of a previous run to resume from."
    )
    parser.add_argument(
        '--episode',
        type=int,
        default=None,
        help="Specify which episode's model to load when resuming. Defaults to the best/latest model."
    )
    args = parser.parse_args()
    
    # 不再需要手动创建目录，Logger会处理
    # os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    
    try:
        main(args)
    except Exception as e:
        print(f"❌ 程序运行时发生未捕获的异常: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        raise 