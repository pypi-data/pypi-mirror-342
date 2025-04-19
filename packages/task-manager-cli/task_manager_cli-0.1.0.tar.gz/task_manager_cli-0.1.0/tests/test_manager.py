import unittest
from pathlib import Path
import tempfile
import json
from task_manager.manager import TaskManager
from task_manager.models import TaskStatus, TaskPriority, Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # 创建临时文件用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_file = Path(self.temp_dir) / "test_tasks.json"
        self.manager = TaskManager(str(self.tasks_file))

    def test_add_task(self):
        """测试添加任务"""
        task = self.manager.add_task(
            title="测试任务",
            description="这是一个测试任务",
            priority=TaskPriority.HIGH
        )
        
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.description, "这是一个测试任务")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.id, "1")

    def test_add_subtask(self):
        """测试添加子任务"""
        parent_task = self.manager.add_task("父任务")
        subtask = self.manager.add_subtask(
            parent_id=parent_task.id,
            title="子任务",
            description="这是一个子任务"
        )
        
        self.assertEqual(subtask.title, "子任务")
        self.assertEqual(subtask.description, "这是一个子任务")
        self.assertEqual(subtask.id, "1.1")
        self.assertEqual(len(self.manager.tasks["1"].subtasks), 1)

    def test_update_task_status(self):
        """测试更新任务状态"""
        task = self.manager.add_task("测试任务")
        self.manager.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        
        self.assertEqual(self.manager.tasks[task.id].status, TaskStatus.IN_PROGRESS)

    def test_add_dependency(self):
        """测试添加任务依赖"""
        task1 = self.manager.add_task("任务1")
        task2 = self.manager.add_task("任务2")
        
        self.manager.add_dependency(task2.id, task1.id)
        self.assertIn(task1.id, self.manager.tasks[task2.id].dependencies)

    def test_get_next_tasks(self):
        """测试获取下一个可执行的任务"""
        task1 = self.manager.add_task("任务1", priority=TaskPriority.LOW)
        task2 = self.manager.add_task("任务2", priority=TaskPriority.HIGH)
        self.manager.add_dependency(task1.id, task2.id)
        
        next_tasks = self.manager.get_next_tasks()
        self.assertEqual(len(next_tasks), 1)
        self.assertEqual(next_tasks[0].id, task2.id)

    def test_task_persistence(self):
        """测试任务持久化"""
        task = self.manager.add_task("持久化测试")
        
        # 创建新的管理器实例，从文件加载数据
        new_manager = TaskManager(str(self.tasks_file))
        self.assertIn(task.id, new_manager.tasks)
        self.assertEqual(new_manager.tasks[task.id].title, "持久化测试")

    def test_invalid_task_operations(self):
        """测试无效的任务操作"""
        with self.assertRaises(ValueError):
            self.manager.add_subtask("999", "无效的子任务")
        
        with self.assertRaises(ValueError):
            self.manager.update_task_status("999", TaskStatus.DONE)
        
        with self.assertRaises(ValueError):
            self.manager.add_dependency("999", "888") 