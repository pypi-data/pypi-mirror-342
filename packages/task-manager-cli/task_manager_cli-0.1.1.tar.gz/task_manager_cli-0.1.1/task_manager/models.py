from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
    DEFERRED = "deferred"

class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SubTask(BaseModel):
    id: str  # 格式: "父任务ID.序号" 例如 "1.1"
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = []
    subtasks: List[SubTask] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    details: Optional[str] = None
    test_strategy: Optional[str] = None 