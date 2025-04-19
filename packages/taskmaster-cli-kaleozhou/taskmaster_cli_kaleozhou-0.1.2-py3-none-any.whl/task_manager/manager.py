import json
from typing import List, Optional, Dict, Union
from datetime import datetime
from pathlib import Path
from .models import Task, SubTask, TaskStatus, Priority
import os

class TaskManager:
    def __init__(self, tasks_file: str = None):
        if tasks_file is None:
            # 在当前目录下创建 tasks.json
            self.tasks_file = Path.cwd().absolute() / "tasks.json"
        else:
            self.tasks_file = Path(tasks_file).absolute()
            
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
        # 确保父目录存在
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump({
                'tasks': [task.model_dump() for task in self.tasks.values()]
            }, f, ensure_ascii=False, indent=2, default=str)

    def add_task(self, title: str, description: Optional[str] = None,
                priority: Priority = Priority.MEDIUM) -> Task:
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

    def _find_task_by_id(self, task_id: str) -> Union[Task, SubTask, None]:
        """根据ID查找任务或子任务"""
        if '.' not in task_id:
            return self.tasks.get(task_id)

        parts = task_id.split('.')
        if parts[0] not in self.tasks:
            return None

        current = self.tasks[parts[0]]
        if len(parts) == 1:
            return current

        # 遍历子任务层级
        for part in parts[1:]:
            found = False
            for subtask in current.subtasks:
                if subtask.id.endswith('.' + part):
                    current = subtask
                    found = True
                    break
            if not found:
                return None
        return current

    def add_subtask(self, parent_id: str, title: str, description: Optional[str] = None) -> SubTask:
        """添加子任务，支持多级嵌套"""
        parent = self._find_task_by_id(parent_id)
        if parent is None:
            raise ValueError(f"父任务 {parent_id} 不存在")

        # 生成新的子任务ID
        if isinstance(parent, Task):
            subtask_id = f"{parent.id}.{len(parent.subtasks) + 1}"
            parent_subtasks = parent.subtasks
        else:  # SubTask
            subtask_id = f"{parent.id}.{len(parent.subtasks) + 1}"
            parent_subtasks = parent.subtasks

        subtask = SubTask(
            id=subtask_id,
            title=title,
            description=description
        )
        parent_subtasks.append(subtask)
        self._save_tasks()
        return subtask

    def update_task_status(self, task_id: str, status: TaskStatus):
        """更新任务状态"""
        task = self._find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"任务 {task_id} 不存在")
        
        task.status = status
        task.updated_at = datetime.now()
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
            Priority[x.priority.upper()].value,
            x.id
        ))

    def _get_task_dict(self, task: Union[Task, SubTask]) -> Dict:
        """递归获取任务信息"""
        task_dict = {
            'id': task.id,
            'title': task.title,
            'status': task.status
        }
        if isinstance(task, Task):
            task_dict['priority'] = task.priority
        
        if task.subtasks:
            task_dict['subtasks'] = [
                self._get_task_dict(st) for st in task.subtasks
            ]
        return task_dict

    def get_task_tree(self) -> List[Dict]:
        """获取任务树状结构"""
        return [self._get_task_dict(task) for task in sorted(self.tasks.values(), key=lambda x: x.id)] 