import unittest
import os
import json
import csv
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from datetime import datetime

# 将项目根目录添加到Python路径中，以便能够导入 `utils` 模块
# 这是一个在测试中常见的做法
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from utils.training_logger import TrainingLogger

# --- 模拟对象，用于测试 ---

class MockAgent:
    """模拟的智能体，用于测试模型保存功能。"""
    def __init__(self):
        self.name = "TestAgent"
        
    def state_dict(self):
        return {"param1": [1.0, 2.0], "param2": {"nested": True}}

class MockModel:
    """一个模拟的PyTorch模型，用于测试模型保存功能。"""
    def state_dict(self):
        # 模拟 torch.tensor 以避免对 torch 的硬依赖
        return {"param1": 1.0, "param2": 2.0}

class MockModelInvalid:
    """一个模拟的无效模型，没有 state_dict 方法。"""
    pass

class TestTrainingLogger(unittest.TestCase):
    """TrainingLogger v3.0 的TDD测试套件。"""

    def setUp(self):
        """每个测试前的环境准备。"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.run_id = "test_run_2025_01_01_12_00_00"
        self.config = {
            "FLUSH_INTERVAL": 3,
            "SAVE_EPISODE_INTERVAL": 5,
            "MAX_STEPS_PER_EPISODE": 10,
            "NUM_EPISODES": 20
        }
        self.mock_agent = MockAgent()

    def tearDown(self):
        """每个测试后的清理工作。"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_01_initialization_creates_directory_structure(self):
        """测试1：初始化时应创建正确的目录结构。"""
        logger = TrainingLogger(
            run_id=self.run_id,
            config=self.config
        )
        
        # 验证目录结构
        expected_dirs = [
            Path("logs") / "ai_training" / self.run_id,
            Path("results") / self.run_id / "latest",
            Path("results") / self.run_id / "best", 
            Path("results") / self.run_id / "episodes"
        ]
        
        for dir_path in expected_dirs:
            self.assertTrue(dir_path.exists(), f"Directory {dir_path} should exist")

    def test_02_initialization_creates_csv_with_header(self):
        """测试2：初始化时应创建带正确表头的CSV文件。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        csv_path = Path("logs") / "ai_training" / self.run_id / "action_log.csv"
        self.assertTrue(csv_path.exists())
        
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            expected_header = ["timestamp", "step", "loss", "reward", "key_rate", "entropy", "actions"]
            self.assertEqual(header, expected_header)

    def test_03_initialization_saves_config(self):
        """测试3：初始化时应保存配置文件。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        config_path = Path("results") / self.run_id / "config.json"
        self.assertTrue(config_path.exists())
        
        with open(config_path, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config, self.config)

    def test_04_initialization_with_base_model_creates_init_dir(self):
        """测试4：有基础模型时应创建init目录并保存来源信息。"""
        # 先创建一个基础模型文件
        base_model_path = self.test_dir / "base_model.pt"
        base_model_path.write_text("mock model data")
        
        logger = TrainingLogger(
            run_id=self.run_id,
            config=self.config,
            base_model_path=str(base_model_path),
            origin_run_id="original_run_123"
        )
        
        init_dir = Path("results") / self.run_id / "init"
        self.assertTrue(init_dir.exists())
        
        # 验证来源文件
        origin_file = init_dir / "origin_run_id.txt"
        self.assertTrue(origin_file.exists())
        self.assertEqual(origin_file.read_text(), "original_run_123")
        
        # 验证基础模型被复制
        copied_model = init_dir / "base_model.pt"
        self.assertTrue(copied_model.exists())

    def test_05_step_method_logs_to_csv_and_buffer(self):
        """测试5：step方法应同时记录到CSV和内存缓冲区。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config, flush_interval=10)
        
        test_actions = {"add_node": "QSP", "params": {"intensity": 0.5}}
        logger.step(
            step=1,
            loss=0.85,
            reward=12.5,
            key_rate=0.42,
            entropy=1.35,
            actions=test_actions
        )
        
        # 验证内存缓冲区
        self.assertEqual(len(logger.logs), 1)
        log_entry = logger.logs[0]
        self.assertEqual(log_entry['step'], 1)
        self.assertEqual(log_entry['loss'], 0.85)
        self.assertEqual(log_entry['reward'], 12.5)
        self.assertEqual(log_entry['key_rate'], 0.42)
        self.assertEqual(log_entry['entropy'], 1.35)
        self.assertEqual(log_entry['actions'], test_actions)
        
        # 验证CSV文件
        csv_path = Path("logs") / "ai_training" / self.run_id / "action_log.csv"
        with open(csv_path, 'r') as f:
            reader = list(csv.reader(f))
            self.assertEqual(len(reader), 2)  # header + 1 data row
            data_row = reader[1]
            self.assertEqual(data_row[1], '1')  # step
            self.assertEqual(data_row[2], '0.85')  # loss
            self.assertEqual(data_row[3], '12.5')  # reward
            self.assertEqual(data_row[4], '0.42')  # key_rate
            self.assertEqual(data_row[5], '1.35')  # entropy
            self.assertEqual(json.loads(data_row[6]), test_actions)

    def test_06_step_method_auto_flushes_at_interval(self):
        """测试6：step方法应在达到flush_interval时自动刷新。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config, flush_interval=2)
        
        # 记录两步以触发自动刷新
        logger.step(1, 0.1, 1.0, 0.1, 0.1, {})
        self.assertEqual(logger.step_counter, 1)
        
        logger.step(2, 0.2, 2.0, 0.2, 0.2, {})
        self.assertEqual(logger.step_counter, 2)
        
        # 验证JSON文件被创建
        json_path = Path("logs") / "ai_training" / self.run_id / "metrics_buffer.json"
        self.assertTrue(json_path.exists())

    def test_07_flush_json_writes_buffer_to_file(self):
        """测试7：flush_json方法应将缓冲区写入JSON文件。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        # 添加一些日志条目
        logger.step(1, 0.1, 1.0, 0.1, 0.1, {"action": "test1"})
        logger.step(2, 0.2, 2.0, 0.2, 0.2, {"action": "test2"})
        
        # 手动刷新
        logger.flush_json()
        
        json_path = Path("logs") / "ai_training" / self.run_id / "metrics_buffer.json"
        self.assertTrue(json_path.exists())
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['step'], 1)
        self.assertEqual(data[1]['step'], 2)

    @patch('utils.training_logger.torch')
    def test_08_save_episode_result_saves_at_interval(self, mock_torch):
        """测试8：save_episode_result应在指定间隔保存。"""
        mock_torch.save = MagicMock()
        
        logger = TrainingLogger(
            run_id=self.run_id, 
            config=self.config,
            save_episode_interval=3,
            save_only_if_keyrate_improves=False  # 禁用基于密钥率改进的保存
        )
        
        protocol_dict = {"nodes": {"alice": "QSP"}}
        keyrate_dict = {"final_key_rate": 0.35}
        
        # Episode 2 不应保存（不是3的倍数）
        logger.save_episode_result(2, self.mock_agent, protocol_dict, keyrate_dict)
        episode_dir = Path("results") / self.run_id / "episodes" / "episode_0002"
        self.assertFalse(episode_dir.exists())
        
        # Episode 3 应该保存
        logger.save_episode_result(3, self.mock_agent, protocol_dict, keyrate_dict)
        episode_dir = Path("results") / self.run_id / "episodes" / "episode_0003"
        self.assertTrue(episode_dir.exists())
        self.assertTrue((episode_dir / "protocol.json").exists())
        self.assertTrue((episode_dir / "keyrate.json").exists())

    @patch('utils.training_logger.torch')
    def test_09_save_latest_overwrites_latest_directory(self, mock_torch):
        """测试9：save_latest应覆盖latest目录。"""
        mock_torch.save = MagicMock()
        
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        protocol_dict = {"test": "data"}
        keyrate_dict = {"rate": 0.5}
        
        logger.save_latest(self.mock_agent, protocol_dict, keyrate_dict)
        
        latest_dir = Path("results") / self.run_id / "latest"
        self.assertTrue((latest_dir / "protocol.json").exists())
        self.assertTrue((latest_dir / "keyrate.json").exists())
        
        # 验证内容
        with open(latest_dir / "protocol.json", 'r') as f:
            self.assertEqual(json.load(f), protocol_dict)

    def test_10_update_best_result_saves_when_improved(self):
        """测试10：update_best_result应在密钥率提升时保存。"""
        with patch('utils.training_logger.torch') as mock_torch:
            mock_torch.save = MagicMock()
            
            logger = TrainingLogger(run_id=self.run_id, config=self.config)
            
            protocol_dict = {"best": "protocol"}
            keyrate_dict = {"final_key_rate": 0.6}
            
            # 第一次应该保存（0.6 > -1）
            logger.update_best_result(5, 0.6, self.mock_agent, protocol_dict, keyrate_dict)
            self.assertEqual(logger.best_keyrate, 0.6)
            self.assertEqual(logger.best_keyrate_episode, 5)
            
            best_dir = Path("results") / self.run_id / "best"
            self.assertTrue((best_dir / "protocol.json").exists())
            
            # 更低的密钥率不应保存
            logger.update_best_result(6, 0.4, self.mock_agent, protocol_dict, keyrate_dict)
            self.assertEqual(logger.best_keyrate, 0.6)  # 应该保持不变

    def test_11_write_summary_creates_readable_report(self):
        """测试11：write_summary应创建可读的训练总结。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        logger.best_keyrate = 0.75
        logger.best_keyrate_episode = 15
        
        logger.write_summary(
            agent_name="TestAgent",
            total_steps=1000,
            total_episodes=50,
            training_duration_sec=3600.5
        )
        
        summary_path = Path("results") / self.run_id / "summary.txt"
        self.assertTrue(summary_path.exists())
        
        content = summary_path.read_text()
        self.assertIn(self.run_id, content)
        self.assertIn("TestAgent", content)
        self.assertIn("1000", content)
        self.assertIn("50", content)
        self.assertIn("3600.5", content)
        self.assertIn("0.75", content)
        self.assertIn("15", content)

    @patch('utils.training_logger.plt')
    @patch('utils.training_logger.pd')
    def test_12_plot_metrics_creates_visualizations(self, mock_pd, mock_plt):
        """测试12：plot_metrics应创建可视化图表。"""
        # 模拟pandas DataFrame和Series
        mock_series = MagicMock()
        mock_rolling = MagicMock()
        mock_rolling.mean.return_value = [0.1, 0.15, 0.2]
        mock_series.rolling.return_value = mock_rolling
        
        mock_df = MagicMock()
        mock_df.empty = False
        mock_df.__getitem__.return_value = mock_series  # 返回模拟的Series
        mock_pd.read_json.return_value = mock_df
        
        # 模拟matplotlib
        mock_figure = MagicMock()
        mock_plt.figure.return_value = mock_figure
        mock_plt.plot = MagicMock()
        mock_plt.savefig = MagicMock()
        
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        # 先创建一个metrics_buffer.json文件
        json_path = Path("logs") / "ai_training" / self.run_id / "metrics_buffer.json"
        json_path.write_text('[]')  # 空JSON数组
        
        logger.plot_metrics()
        
        # 验证图表被保存
        expected_calls = [
            call(Path("results") / self.run_id / "key_rate_vs_steps.png"),
            call(Path("results") / self.run_id / "reward_vs_steps.png")
        ]
        mock_plt.savefig.assert_has_calls(expected_calls)

    @patch('utils.training_logger.torch')
    def test_13_save_all_performs_complete_finalization(self, mock_torch):
        """测试13：save_all应执行完整的最终化过程。"""
        mock_torch.save = MagicMock()
        
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        # 添加一些日志数据
        logger.step(1, 0.1, 1.0, 0.1, 0.1, {})
        
        protocol_dict = {"final": "protocol"}
        keyrate_dict = {"final_key_rate": 0.8}
        
        with patch.object(logger, 'plot_metrics') as mock_plot:
            logger.save_all(
                agent_name="FinalAgent",
                total_steps=100,
                total_episodes=10,
                training_duration_sec=1800.0,
                model=self.mock_agent,
                protocol_dict=protocol_dict,
                keyrate_dict=keyrate_dict
            )
        
        # 验证所有最终化步骤都被执行
        json_path = Path("logs") / "ai_training" / self.run_id / "metrics_buffer.json"
        self.assertTrue(json_path.exists())  # flush_json 被调用
        
        latest_dir = Path("results") / self.run_id / "latest"
        self.assertTrue((latest_dir / "protocol.json").exists())  # save_latest 被调用
        
        summary_path = Path("results") / self.run_id / "summary.txt"
        self.assertTrue(summary_path.exists())  # write_summary 被调用
        
        mock_plot.assert_called_once()  # plot_metrics 被调用

    def test_14_close_method_flushes_remaining_data(self):
        """测试14：close方法应刷新剩余数据。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        # 添加一些未刷新的数据
        logger.step(1, 0.1, 1.0, 0.1, 0.1, {})
        
        # 验证JSON文件尚未创建
        json_path = Path("logs") / "ai_training" / self.run_id / "metrics_buffer.json"
        self.assertFalse(json_path.exists())
        
        # 调用close
        logger.close()
        
        # 验证数据被刷新
        self.assertTrue(json_path.exists())

    def test_15_atomic_operations_handle_failures_gracefully(self):
        """测试15：原子操作应优雅处理失败情况。"""
        logger = TrainingLogger(run_id=self.run_id, config=self.config)
        
        # 测试_atomic_json_write的错误处理
        invalid_data = object()  # 不能JSON序列化的对象
        
        with patch('builtins.print') as mock_print:
            logger._atomic_json_write(invalid_data, Path("test.json"))
            # 应该打印错误信息而不是崩溃
            mock_print.assert_called()

    def test_16_custom_run_id_parameter(self):
        """测试16：自定义run_id参数应被正确使用。"""
        custom_run_id = "custom_test_run_xyz"
        logger = TrainingLogger(run_id=custom_run_id, config=self.config)
        
        self.assertEqual(logger.run_id, custom_run_id)
        
        # 验证目录使用了自定义ID
        expected_path = Path("results") / custom_run_id
        self.assertTrue(expected_path.exists())

    def test_17_default_run_id_generation(self):
        """测试17：未提供run_id时应生成默认ID。"""
        with patch('utils.training_logger.datetime') as mock_datetime:
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2025-01-01_12-30-45"
            mock_datetime.now.return_value = mock_now
            
            logger = TrainingLogger(config=self.config)
            
            self.assertEqual(logger.run_id, "2025-01-01_12-30-45")
            mock_datetime.now.assert_called()
            mock_now.strftime.assert_called_with("%Y-%m-%d_%H-%M-%S")


if __name__ == '__main__':
    # 按照测试编号顺序运行，确保逻辑流程正确
    unittest.main(verbosity=2) 