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

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SubTask(BaseModel):
    id: str  # 格式: "父任务ID.序号" 例如 "1.1" 或 "1.1.2"
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List['SubTask'] = []  # 递归支持子任务
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    dependencies: List[str] = []
    subtasks: List[SubTask] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    details: Optional[str] = None
    test_strategy: Optional[str] = None

# 添加这行来解决 SubTask 的前向引用
SubTask.model_rebuild() 