import unittest
from pathlib import Path
import tempfile
import json
from task_manager.manager import TaskManager
from task_manager.models import TaskStatus, Priority, Task, SubTask

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
            priority=Priority.HIGH
        )
        
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.description, "这是一个测试任务")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.id, "1")

    def test_add_subtask(self):
        """测试添加一级子任务"""
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

    def test_add_nested_subtasks(self):
        """测试添加多级子任务"""
        # 创建主任务
        main_task = self.manager.add_task("主任务")
        
        # 添加一级子任务
        subtask1 = self.manager.add_subtask(main_task.id, "一级子任务")
        self.assertEqual(subtask1.id, "1.1")
        
        # 添加二级子任务
        subtask2 = self.manager.add_subtask(subtask1.id, "二级子任务")
        self.assertEqual(subtask2.id, "1.1.1")
        
        # 添加三级子任务
        subtask3 = self.manager.add_subtask(subtask2.id, "三级子任务")
        self.assertEqual(subtask3.id, "1.1.1.1")
        
        # 验证任务树结构
        task = self.manager.tasks["1"]
        self.assertEqual(len(task.subtasks), 1)
        self.assertEqual(len(task.subtasks[0].subtasks), 1)
        self.assertEqual(len(task.subtasks[0].subtasks[0].subtasks), 1)

    def test_find_nested_task(self):
        """测试查找嵌套任务"""
        # 创建任务树
        main_task = self.manager.add_task("主任务")
        subtask1 = self.manager.add_subtask(main_task.id, "一级子任务")
        subtask2 = self.manager.add_subtask(subtask1.id, "二级子任务")
        
        # 测试查找各级任务
        found_main = self.manager._find_task_by_id("1")
        found_sub1 = self.manager._find_task_by_id("1.1")
        found_sub2 = self.manager._find_task_by_id("1.1.1")
        
        self.assertIsInstance(found_main, Task)
        self.assertIsInstance(found_sub1, SubTask)
        self.assertIsInstance(found_sub2, SubTask)
        
        self.assertEqual(found_main.title, "主任务")
        self.assertEqual(found_sub1.title, "一级子任务")
        self.assertEqual(found_sub2.title, "二级子任务")

    def test_update_nested_task_status(self):
        """测试更新嵌套任务状态"""
        # 创建任务树
        main_task = self.manager.add_task("主任务")
        subtask1 = self.manager.add_subtask(main_task.id, "一级子任务")
        subtask2 = self.manager.add_subtask(subtask1.id, "二级子任务")
        
        # 更新二级子任务状态
        self.manager.update_task_status("1.1.1", TaskStatus.DONE)
        
        # 验证状态更新
        found_task = self.manager._find_task_by_id("1.1.1")
        self.assertEqual(found_task.status, TaskStatus.DONE)

    def test_invalid_task_operations(self):
        """测试无效的任务操作"""
        with self.assertRaises(ValueError):
            self.manager.add_subtask("999", "无效的子任务")
        
        with self.assertRaises(ValueError):
            self.manager.update_task_status("999", TaskStatus.DONE)
        
        with self.assertRaises(ValueError):
            self.manager.add_dependency("999", "888")
        
        # 测试无效的嵌套任务操作
        with self.assertRaises(ValueError):
            self.manager.add_subtask("1.999.1", "无效的嵌套子任务")

    def test_task_tree_structure(self):
        """测试任务树结构"""
        # 创建复杂的任务树
        main_task = self.manager.add_task("主任务")
        subtask1 = self.manager.add_subtask(main_task.id, "一级子任务A")
        subtask2 = self.manager.add_subtask(main_task.id, "一级子任务B")
        subtask1_1 = self.manager.add_subtask(subtask1.id, "二级子任务A")
        
        # 获取任务树
        tree = self.manager.get_task_tree()
        
        # 验证树结构
        self.assertEqual(len(tree), 1)  # 一个主任务
        main_task_dict = tree[0]
        self.assertEqual(len(main_task_dict['subtasks']), 2)  # 两个一级子任务
        self.assertEqual(len(main_task_dict['subtasks'][0]['subtasks']), 1)  # 第一个一级子任务有一个子任务

    def test_task_persistence(self):
        """测试任务持久化"""
        # 创建任务树
        main_task = self.manager.add_task("主任务")
        subtask1 = self.manager.add_subtask(main_task.id, "一级子任务")
        subtask2 = self.manager.add_subtask(subtask1.id, "二级子任务")
        
        # 创建新的管理器实例，从文件加载数据
        new_manager = TaskManager(str(self.tasks_file))
        
        # 验证任务树是否正确加载
        self.assertIn("1", new_manager.tasks)
        loaded_task = new_manager.tasks["1"]
        self.assertEqual(len(loaded_task.subtasks), 1)
        self.assertEqual(len(loaded_task.subtasks[0].subtasks), 1)
        self.assertEqual(loaded_task.subtasks[0].subtasks[0].title, "二级子任务")

    def test_add_dependency(self):
        """测试添加任务依赖"""
        task1 = self.manager.add_task("任务1")
        task2 = self.manager.add_task("任务2")
        
        self.manager.add_dependency(task2.id, task1.id)
        self.assertIn(task1.id, self.manager.tasks[task2.id].dependencies)

    def test_get_next_tasks(self):
        """测试获取下一个可执行的任务"""
        task1 = self.manager.add_task("任务1", priority=Priority.LOW)
        task2 = self.manager.add_task("任务2", priority=Priority.HIGH)
        self.manager.add_dependency(task1.id, task2.id)
        
        next_tasks = self.manager.get_next_tasks()
        self.assertEqual(len(next_tasks), 1)
        self.assertEqual(next_tasks[0].id, task2.id)

    def test_update_task_status(self):
        """测试更新任务状态"""
        task = self.manager.add_task("测试任务")
        self.manager.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        
        self.assertEqual(self.manager.tasks[task.id].status, TaskStatus.IN_PROGRESS)

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