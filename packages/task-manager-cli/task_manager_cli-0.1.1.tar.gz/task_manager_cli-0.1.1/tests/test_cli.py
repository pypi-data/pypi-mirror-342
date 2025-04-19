import unittest
from click.testing import CliRunner
from task_manager.cli import cli
import tempfile
import os
from pathlib import Path

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        # 恢复原始工作目录
        os.chdir(self.old_cwd)
        # 清理临时目录
        for file in Path(self.temp_dir).glob('*'):
            file.unlink()
        Path(self.temp_dir).rmdir()

    def test_add_task(self):
        """测试添加任务命令"""
        result = self.runner.invoke(cli, ['add', '测试任务', '-d', '这是一个测试任务', '-p', 'high'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加任务', result.output)

    def test_add_subtask(self):
        """测试添加子任务命令"""
        # 先添加父任务
        self.runner.invoke(cli, ['add', '父任务'])
        # 添加子任务
        result = self.runner.invoke(cli, ['add-subtask', '1', '子任务', '-d', '这是一个子任务'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加子任务', result.output)

    def test_update_status(self):
        """测试更新任务状态命令"""
        # 先添加任务
        self.runner.invoke(cli, ['add', '状态测试任务'])
        # 更新状态
        result = self.runner.invoke(cli, ['status', '1', 'in_progress'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已更新任务', result.output)

    def test_update_subtask_status(self):
        """测试更新子任务状态"""
        # 添加父任务和子任务
        self.runner.invoke(cli, ['add', '父任务'])
        self.runner.invoke(cli, ['add-subtask', '1', '子任务'])
        # 更新子任务状态
        result = self.runner.invoke(cli, ['status', '1.1', 'done'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已更新任务', result.output)

    def test_add_dependency(self):
        """测试添加任务依赖命令"""
        # 添加两个任务
        self.runner.invoke(cli, ['add', '任务1'])
        self.runner.invoke(cli, ['add', '任务2'])
        # 添加依赖
        result = self.runner.invoke(cli, ['depend', '2', '1'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加依赖', result.output)

    def test_list_tasks(self):
        """测试列出任务命令"""
        # 添加一些任务
        self.runner.invoke(cli, ['add', '任务1'])
        self.runner.invoke(cli, ['add', '任务2'])
        # 列出任务
        result = self.runner.invoke(cli, ['list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('任务1', result.output)
        self.assertIn('任务2', result.output)

    def test_list_empty_tasks(self):
        """测试列出空任务列表"""
        result = self.runner.invoke(cli, ['list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('没有任务', result.output)

    def test_next_tasks(self):
        """测试显示下一个任务命令"""
        # 添加任务并设置依赖
        self.runner.invoke(cli, ['add', '任务1'])
        self.runner.invoke(cli, ['add', '任务2'])
        self.runner.invoke(cli, ['depend', '2', '1'])
        # 获取下一个任务
        result = self.runner.invoke(cli, ['next'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('任务1', result.output)

    def test_next_empty_tasks(self):
        """测试没有可执行任务时的显示"""
        result = self.runner.invoke(cli, ['next'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('没有可执行的任务', result.output)

    def test_invalid_commands(self):
        """测试无效的命令参数"""
        # 测试无效的任务ID
        result = self.runner.invoke(cli, ['status', '999', 'done'])
        self.assertNotEqual(result.exit_code, 0)
        
        # 测试无效的状态值
        result = self.runner.invoke(cli, ['status', '1', 'invalid_status'])
        self.assertNotEqual(result.exit_code, 0)

    def test_invalid_subtask_operations(self):
        """测试无效的子任务操作"""
        # 测试更新不存在的子任务状态
        result = self.runner.invoke(cli, ['status', '999.1', 'done'])
        self.assertNotEqual(result.exit_code, 0)

        # 测试添加子任务到不存在的父任务
        result = self.runner.invoke(cli, ['add-subtask', '999', '子任务'])
        self.assertNotEqual(result.exit_code, 0) 