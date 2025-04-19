import json
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
from .models import Task, SubTask, TaskStatus, TaskPriority
import os

class TaskManager:
    def __init__(self, tasks_file: str = None):
        if tasks_file is None:
            # 在用户主目录下创建 .taskmaster 目录
            home_dir = Path.home()
            taskmaster_dir = home_dir / '.taskmaster'
            taskmaster_dir.mkdir(exist_ok=True)
            
            # 使用当前目录名作为项目名
            current_dir = Path.cwd().name
            self.tasks_file = taskmaster_dir / f"{current_dir}_tasks.json"
        else:
            self.tasks_file = Path(tasks_file)
            
        self.tasks: Dict[str, Task] = {}
        self._load_tasks()

    def _load_tasks(self):
        """从文件加载任务"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for task_data in data.get('tasks', []):
                    task = Task(**task_data)
                    self.tasks[task.id] = task

    def _save_tasks(self):
        """保存任务到文件"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump({
                'tasks': [task.model_dump() for task in self.tasks.values()]
            }, f, ensure_ascii=False, indent=2, default=str)

    def add_task(self, title: str, description: Optional[str] = None,
                priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """添加新任务"""
        task_id = str(len(self.tasks) + 1)
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority
        )
        self.tasks[task_id] = task
        self._save_tasks()
        return task

    def add_subtask(self, parent_id: str, title: str, description: Optional[str] = None) -> SubTask:
        """添加子任务"""
        if parent_id not in self.tasks:
            raise ValueError(f"父任务 {parent_id} 不存在")
        
        parent_task = self.tasks[parent_id]
        subtask_id = f"{parent_id}.{len(parent_task.subtasks) + 1}"
        subtask = SubTask(
            id=subtask_id,
            title=title,
            description=description
        )
        parent_task.subtasks.append(subtask)
        self._save_tasks()
        return subtask

    def update_task_status(self, task_id: str, status: TaskStatus):
        """更新任务状态"""
        if '.' in task_id:  # 子任务
            parent_id, subtask_num = task_id.split('.')
            if parent_id not in self.tasks:
                raise ValueError(f"父任务 {parent_id} 不存在")
            parent_task = self.tasks[parent_id]
            for subtask in parent_task.subtasks:
                if subtask.id == task_id:
                    subtask.status = status
                    subtask.updated_at = datetime.now()
                    break
        else:  # 主任务
            if task_id not in self.tasks:
                raise ValueError(f"任务 {task_id} 不存在")
            self.tasks[task_id].status = status
            self.tasks[task_id].updated_at = datetime.now()
        
        self._save_tasks()

    def add_dependency(self, task_id: str, depends_on: str):
        """添加任务依赖"""
        if task_id not in self.tasks or depends_on not in self.tasks:
            raise ValueError("任务不存在")
        if depends_on not in self.tasks[task_id].dependencies:
            self.tasks[task_id].dependencies.append(depends_on)
            self._save_tasks()

    def get_next_tasks(self) -> List[Task]:
        """获取下一个可以开始的任务"""
        next_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                dependencies_met = all(
                    self.tasks[dep].status == TaskStatus.DONE
                    for dep in task.dependencies
                )
                if dependencies_met:
                    next_tasks.append(task)
        return sorted(next_tasks, key=lambda x: (
            TaskPriority[x.priority.upper()].value,
            x.id
        ))

    def get_task_tree(self) -> List[Dict]:
        """获取任务树状结构"""
        tree = []
        for task in sorted(self.tasks.values(), key=lambda x: x.id):
            task_dict = {
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'priority': task.priority,
                'subtasks': [
                    {
                        'id': st.id,
                        'title': st.title,
                        'status': st.status
                    } for st in task.subtasks
                ]
            }
            tree.append(task_dict)
        return tree 