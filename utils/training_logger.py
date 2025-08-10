import atexit
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
import torch

from config import settings


class NumpyJSONEncoder(json.JSONEncoder):
    """支持 NumPy 类型的 JSON 编码器"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'value'):  # 处理枚举类型
            return obj.value
        return super().default(obj)


class TrainingLogger:
    """
    AI-assisted QKD protocol design system log saving system v3.0.

    Handles structured logging for training runs, including metrics,
    model checkpoints, protocol definitions, and results visualization.
    """

    def __init__(
        self,
        run_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        flush_interval: int = 50,
        save_episode_interval: int = settings.SAVE_EPISODE_INTERVAL,
        save_only_if_keyrate_improves: bool = settings.SAVE_ONLY_IF_KEYRATE_IMPROVES,
        base_model_path: Optional[str] = None,
        base_protocol_path: Optional[str] = None,
        origin_run_id: Optional[str] = None,
    ):
        """
        Initializes the logger and creates the required directory structure.

        Args:
            run_id: A unique identifier for the run. Defaults to current timestamp.
            config: A dictionary with agent and environment configurations.
            flush_interval: Steps after which to flush metrics to JSON.
            save_episode_interval: Episodes after which to save a checkpoint.
            save_only_if_keyrate_improves: If True, only saves episode checkpoints
                                           if the key rate improves.
            base_model_path: Path to a pre-trained model to start from.
            base_protocol_path: Path to a base protocol to start from.
            origin_run_id: The run_id of the original run if continuing.
        """
        self.run_id = run_id or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.config = config or {}
        self.flush_interval = flush_interval
        self.save_episode_interval = save_episode_interval
        self.save_only_if_keyrate_improves = save_only_if_keyrate_improves
        self.base_model_path = base_model_path
        self.base_protocol_path = base_protocol_path
        self.origin_run_id = origin_run_id
        self.start_time = datetime.now()

        # --- 1. Setup Directory Structure ---
        self.log_dir = Path("logs") / "ai_training" / self.run_id
        self.results_dir = Path("results") / self.run_id
        self.latest_dir = self.results_dir / "latest"
        self.best_dir = self.results_dir / "best"
        self.episodes_dir = self.results_dir / "episodes"
        self.init_dir = self.results_dir / "init"

        self._create_directories()

        # --- 2. Handle Base Model/Protocol ---
        if self.base_model_path or self.base_protocol_path:
            self.init_dir.mkdir(exist_ok=True)
            if self.origin_run_id:
                (self.init_dir / "origin_run_id.txt").write_text(self.origin_run_id)
            if self.base_model_path:
                shutil.copy(self.base_model_path, self.init_dir / "base_model.pt")
            if self.base_protocol_path:
                shutil.copy(
                    self.base_protocol_path, self.init_dir / "base_protocol.json"
                )

        # --- 3. Initialize Log Files and State ---
        self.action_log_path = self.log_dir / "action_log.csv"
        self.metrics_buffer_path = self.log_dir / "metrics_buffer.json"
        self._initialize_csv()

        self.logs: List[Dict[str, Any]] = []
        self.best_keyrate: float = -1.0
        self.best_keyrate_episode: int = -1
        self.step_counter: int = 0

        if self.config:
            (self.results_dir / "config.json").write_text(
                json.dumps(self.config, indent=4)
            )

        atexit.register(self.close)
        print(f"[TrainingLogger] Initialized for run: {self.run_id}")
        print(f"[TrainingLogger] Results will be saved to: {self.results_dir.resolve()}")

    def _create_directories(self):
        """Creates all necessary directories for the run."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.latest_dir.mkdir(exist_ok=True)
        self.best_dir.mkdir(exist_ok=True)
        self.episodes_dir.mkdir(exist_ok=True)

    def _initialize_csv(self):
        """Creates the action log CSV and writes the header."""
        if not self.action_log_path.exists():
            with open(self.action_log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "timestamp",
                        "step",
                        "loss",
                        "reward",
                        "key_rate",
                        "entropy",
                        "actions",
                    ]
                )

    def step(
        self,
        step: int,
        loss: float,
        reward: float,
        key_rate: float,
        entropy: float,
        actions: Dict[str, Any],
    ):
        """
        Logs the metrics for a single training step.

        Args:
            step: The global step number.
            loss: The loss value from the agent.
            reward: The reward received.
            key_rate: The calculated secure key rate.
            entropy: The policy entropy.
            actions: The actions taken by the agent.
        """
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "step": step,
            "loss": loss,
            "reward": reward,
            "key_rate": key_rate,
            "entropy": entropy,
            "actions": actions,
        }
        self.logs.append(log_entry)

        with open(self.action_log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    timestamp,
                    step,
                    loss,
                    reward,
                    key_rate,
                    entropy,
                    json.dumps(actions, cls=NumpyJSONEncoder),
                ]
            )

        self.step_counter += 1
        if self.step_counter % self.flush_interval == 0:
            self.flush_json()

    def flush_json(self):
        """Writes the buffered logs to a structured JSON file."""
        if self.logs:
            self._atomic_json_write(self.logs, self.metrics_buffer_path)

    def save_episode_result(
        self,
        episode_id: int,
        model: Any,
        protocol_dict: Dict[str, Any],
        keyrate_dict: Dict[str, Any],
    ):
        """
        Saves the results of an episode, including model and protocol.

        Args:
            episode_id: The ID of the completed episode.
            model: The trained agent model (e.g., a PyTorch nn.Module).
            protocol_dict: The generated protocol as a dictionary.
            keyrate_dict: The keyrate calculation results as a dictionary.
        """
        print(f"[TrainingLogger] 开始保存回合 {episode_id} 的结果")
        try:
            key_rate = keyrate_dict.get("final_key_rate", 0.0)
            print(f"[TrainingLogger] 提取的密钥率: {key_rate}")

            should_save_episode = False
            if episode_id % self.save_episode_interval == 0:
                should_save_episode = True
                print(f"[TrainingLogger] 根据保存间隔决定保存 (间隔={self.save_episode_interval})")
            
            if self.save_only_if_keyrate_improves and key_rate > self.best_keyrate:
                 should_save_episode = True
                 print(f"[TrainingLogger] 根据密钥率提升决定保存 (当前={key_rate}, 最佳={self.best_keyrate})")

            if should_save_episode:
                print(f"[TrainingLogger] 正在保存回合 {episode_id} 到 episodes 目录")
                episode_dir = self.episodes_dir / f"episode_{episode_id:04d}"
                episode_dir.mkdir(exist_ok=True)
                self._save_artifacts(
                    episode_dir, model, protocol_dict, keyrate_dict
                )
                print(f"[TrainingLogger] ✅ 回合 {episode_id} 保存到 episodes 目录完成")
            
            print(f"[TrainingLogger] 正在保存最新结果...")
            self.save_latest(model, protocol_dict, keyrate_dict)
            print(f"[TrainingLogger] ✅ 最新结果保存完成")
            
            print(f"[TrainingLogger] 正在更新最佳结果...")
            self.update_best_result(episode_id, key_rate, model, protocol_dict, keyrate_dict)
            print(f"[TrainingLogger] ✅ 最佳结果更新完成")
            
        except Exception as e:
            print(f"[TrainingLogger] ❌ 保存回合 {episode_id} 时出错: {e}")
            print(f"[TrainingLogger] 错误类型: {type(e).__name__}")
            import traceback
            print(f"[TrainingLogger] 详细错误: {traceback.format_exc()}")
            raise  # 重新抛出异常以便上层处理

    def _save_artifacts(
        self,
        directory: Path,
        model: Any,
        protocol_dict: Dict[str, Any],
        keyrate_dict: Dict[str, Any],
    ):
        """Helper to save model, protocol, and keyrate to a directory."""
        # 保存模型
        try:
            if hasattr(model, 'state_dict'):
                self._atomic_torch_save(model.state_dict(), directory / "model.pt")
                print(f"✅ 模型state_dict已保存至 {directory / 'model.pt'}")
            elif hasattr(model, 'save_models'):
                model.save_models(str(directory / "model.pt"))
                print(f"✅ 模型已保存至 {directory / 'model.pt'}")
            else:
                print(f"警告: 模型对象既没有 state_dict 方法也没有 save_models 方法，跳过模型保存。")
        except Exception as e:
            print(f"❌ 保存模型时出错: {e}")
            print(f"错误类型: {type(e).__name__}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
        
        # 保存协议和密钥率
        try:
            self._atomic_json_write(protocol_dict, directory / "protocol.json")
            print(f"✅ 协议已保存至 {directory / 'protocol.json'}")
        except Exception as e:
            print(f"❌ 保存协议时出错: {e}")
            
        try:
            self._atomic_json_write(keyrate_dict, directory / "keyrate.json")
            print(f"✅ 密钥率已保存至 {directory / 'keyrate.json'}")
        except Exception as e:
            print(f"❌ 保存密钥率时出错: {e}")

    def save_latest(
        self,
        model: Any,
        protocol_dict: Dict[str, Any],
        keyrate_dict: Dict[str, Any],
    ):
        """Saves the latest results to the 'latest' directory."""
        self._save_artifacts(self.latest_dir, model, protocol_dict, keyrate_dict)

    def update_best_result(
        self,
        episode_id: int,
        key_rate: float,
        model: Any,
        protocol_dict: Dict[str, Any],
        keyrate_dict: Dict[str, Any],
    ):
        """Updates the best result if the current key rate is higher."""
        if key_rate > self.best_keyrate:
            self.best_keyrate = key_rate
            self.best_keyrate_episode = episode_id
            print(f"New best key rate: {key_rate:.6f} at episode {episode_id}")
            self._save_artifacts(self.best_dir, model, protocol_dict, keyrate_dict)

    def write_summary(
        self,
        agent_name: str,
        total_steps: int,
        total_episodes: int,
        training_duration_sec: float,
    ):
        """
        Writes a final summary of the training run.
        """
        end_time = datetime.now()
        summary_content = f"""
# Training Run Summary

- **Run ID**: {self.run_id}
- **Agent**: {agent_name}

## Training Context
- **Start Time**: {self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
- **End Time**: {end_time.strftime("%Y-%m-%d %H:%M:%S")}
- **Duration**: {training_duration_sec:.2f} seconds
- **Origin Run ID**: {self.origin_run_id or 'N/A'}
- **Base Model**: {self.base_model_path or 'N/A'}
- **Base Protocol**: {self.base_protocol_path or 'N/A'}

## Training Statistics
- **Total Episodes**: {total_episodes}
- **Total Steps**: {total_steps}

## Best Result
- **Best Key Rate**: {self.best_keyrate:.6f}
- **Achieved at Episode**: {self.best_keyrate_episode}
- **Best artifacts saved in**: {self.best_dir.resolve()}

## Configuration
{json.dumps(self.config, indent=4)}
"""
        (self.results_dir / "summary.txt").write_text(summary_content)

    def plot_metrics(self):
        """
        Reads all logged metrics and generates plots for key metrics.
        """
        if not self.metrics_buffer_path.exists():
            print("Warning: metrics_buffer.json not found. Skipping plotting.")
            return

        df = pd.read_json(self.metrics_buffer_path)
        if df.empty:
            print("Warning: No data in metrics_buffer.json. Skipping plotting.")
            return
            
        plt.style.use('seaborn-v0_8-whitegrid')

        # Plot Key Rate
        plt.figure(figsize=(12, 6))
        plt.plot(df["step"], df["key_rate"], label="Secure Key Rate", color="blue", alpha=0.7)
        plt.xlabel("Step")
        plt.ylabel("Key Rate")
        plt.title("Secure Key Rate Over Training Steps")
        plt.legend()
        plt.savefig(self.results_dir / "key_rate_vs_steps.png")
        plt.close()

        # Plot Reward
        plt.figure(figsize=(12, 6))
        plt.plot(df["step"], df["reward"], label="Reward", color="green", alpha=0.7)
        rolling_avg = df["reward"].rolling(window=self.flush_interval).mean()
        plt.plot(df["step"], rolling_avg, label=f"Rolling Avg ({self.flush_interval} steps)", color="red")
        plt.xlabel("Step")
        plt.ylabel("Reward")
        plt.title("Reward Over Training Steps")
        plt.legend()
        plt.savefig(self.results_dir / "reward_vs_steps.png")
        plt.close()


    def save_all(
        self,
        agent_name: str,
        total_steps: int,
        total_episodes: int,
        training_duration_sec: float,
        model: Any,
        protocol_dict: Dict[str, Any],
        keyrate_dict: Dict[str, Any],
    ):
        """
        Convenience method to run all final save operations.
        """
        self.flush_json()
        self.save_latest(model, protocol_dict, keyrate_dict)
        self.write_summary(agent_name, total_steps, total_episodes, training_duration_sec)
        self.plot_metrics()

    def close(self):
        """
        Finalizes the logging, flushing any remaining data.
        """
        print("[TrainingLogger] Closing logger and flushing remaining data.")
        self.flush_json()
    
    def _atomic_json_write(self, data: Any, path: Path):
        """Atomically writes a dictionary to a JSON file."""
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        try:
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=4, cls=NumpyJSONEncoder)
            shutil.move(temp_path, path)
        except Exception as e:
            print(f"Error during atomic write to {path}: {e}")
            if temp_path.exists():
                temp_path.unlink()

    def _atomic_torch_save(self, data: Any, path: Path):
        """Atomically saves a torch object."""
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        try:
            torch.save(data, temp_path)
            shutil.move(temp_path, path)
        except Exception as e:
            print(f"Error during atomic torch save to {path}: {e}")
            if temp_path.exists():
                temp_path.unlink() 