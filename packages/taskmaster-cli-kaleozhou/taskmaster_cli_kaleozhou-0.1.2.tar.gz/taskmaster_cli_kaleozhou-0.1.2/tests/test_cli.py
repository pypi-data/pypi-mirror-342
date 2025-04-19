import unittest
from unittest.mock import patch
from click.testing import CliRunner
from pathlib import Path
import tempfile
import json
from task_manager.cli import cli
from task_manager.models import TaskStatus, Priority

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_file = Path(self.temp_dir) / "tasks.json"
        # 设置环境变量，指定任务文件路径
        self.env = {"TASK_FILE": str(self.tasks_file)}

    def test_add_task(self):
        """测试添加任务命令"""
        # 测试基本添加
        result = self.runner.invoke(cli, ['add', '测试任务'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加任务', result.output)

        # 测试带描述和优先级的添加
        result = self.runner.invoke(cli, [
            'add', 
            '重要任务', 
            '-d', '这是一个重要任务',
            '-p', 'high'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加任务', result.output)

    def test_add_subtask(self):
        """测试添加子任务命令"""
        # 先添加主任务
        self.runner.invoke(cli, ['add', '主任务'])
        
        # 添加一级子任务
        result = self.runner.invoke(cli, [
            'add-subtask',
            '1',
            '一级子任务',
            '-d', '这是一级子任务'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加子任务', result.output)

        # 添加二级子任务
        result = self.runner.invoke(cli, [
            'add-subtask',
            '1.1',
            '二级子任务'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加子任务', result.output)

    def test_update_status(self):
        """测试更新任务状态命令"""
        # 先添加任务
        self.runner.invoke(cli, ['add', '状态测试任务'])
        
        # 更新状态
        result = self.runner.invoke(cli, [
            'status',
            '1',
            'in_progress'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已更新任务', result.output)

        # 更新子任务状态
        self.runner.invoke(cli, ['add-subtask', '1', '子任务'])
        result = self.runner.invoke(cli, [
            'status',
            '1.1',
            'done'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已更新任务', result.output)

    def test_add_dependency(self):
        """测试添加任务依赖命令"""
        # 添加两个任务
        self.runner.invoke(cli, ['add', '任务1'])
        self.runner.invoke(cli, ['add', '任务2'])
        
        # 添加依赖
        result = self.runner.invoke(cli, [
            'depend',
            '2',
            '1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('已添加依赖', result.output)

    def test_next_tasks(self):
        """测试显示下一个任务命令"""
        # 添加测试任务
        self.runner.invoke(cli, ['add', '普通任务', '-p', 'low'])
        self.runner.invoke(cli, ['add', '紧急任务', '-p', 'high'])
        
        # 测试 next 命令
        result = self.runner.invoke(cli, ['next'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('紧急任务', result.output)  # 高优先级任务应该先显示

    def test_list_tasks(self):
        """测试列出所有任务命令"""
        # 创建任务树
        self.runner.invoke(cli, ['add', '主任务'])
        self.runner.invoke(cli, ['add-subtask', '1', '子任务A'])
        self.runner.invoke(cli, ['add-subtask', '1', '子任务B'])
        self.runner.invoke(cli, ['add-subtask', '1.1', '子子任务'])
        
        # 测试 list 命令
        result = self.runner.invoke(cli, ['list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('主任务', result.output)
        self.assertIn('子任务A', result.output)
        self.assertIn('子任务B', result.output)
        self.assertIn('子子任务', result.output)

    def test_invalid_commands(self):
        """测试无效命令处理"""
        # 测试更新不存在的任务状态
        result = self.runner.invoke(cli, ['status', '999', 'done'])
        self.assertNotEqual(result.exit_code, 0)
        
        # 测试添加到不存在的父任务
        result = self.runner.invoke(cli, ['add-subtask', '999', '无效子任务'])
        self.assertNotEqual(result.exit_code, 0)
        
        # 测试添加无效的依赖
        result = self.runner.invoke(cli, ['depend', '999', '888'])
        self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main() 