# Task Manager (任务管理器)

一个简单但功能强大的命令行任务管理工具，帮助您在项目中轻松管理和追踪任务进度。

[![PyPI version](https://badge.fury.io/py/task-manager-cli.svg)](https://badge.fury.io/py/task-manager-cli)
[![GitHub](https://img.shields.io/github/license/kaleozhou/tasks-manager)](https://github.com/kaleozhou/tasks-manager)

## 特性

- 📝 任务管理：创建、更新和删除任务
- 🌲 子任务支持：将大任务分解为小任务
- 🔄 任务状态跟踪：支持多种任务状态（待处理、进行中、已完成、已阻塞、已推迟）
- ⭐ 优先级管理：高、中、低三级优先级
- 🔗 任务依赖：设置任务间的依赖关系
- 💾 本地持久化：自动保存任务数据
- 🎨 美观的终端界面：使用 Rich 提供清晰的视觉展示

## 安装

```bash
pip install task-manager-cli
```

## 详细使用说明

### 1. 添加新任务

创建一个新的主任务，可以设置标题、描述和优先级。

```bash
# 基本用法
task add "任务标题"

# 添加描述和优先级
task add "完成项目文档" -d "编写项目的README和API文档" -p high

# 优先级选项：high（高）、medium（中）、low（低）
```

### 2. 添加子任务

为主任务添加子任务，帮助分解大任务。

```bash
# 语法：task add-subtask <父任务ID> "子任务标题" [-d "描述"]
task add-subtask 1 "编写单元测试" -d "确保代码质量"
```

### 3. 更新任务状态

跟踪任务的进展状态。

```bash
# 语法：task status <任务ID> <状态>
task status 1 in_progress

# 可用状态：
# - pending（待处理）
# - in_progress（进行中）
# - done（已完成）
# - blocked（已阻塞）
# - deferred（已推迟）

# 更新子任务状态
task status 1.1 done
```

### 4. 管理任务依赖

设置任务之间的依赖关系。

```bash
# 语法：task depend <任务ID> <依赖任务ID>
task depend 2 1  # 任务2依赖于任务1

# 被依赖的任务必须完成后，依赖任务才能开始
```

### 5. 查看任务列表

以树状结构显示所有任务。

```bash
task list

# 示例输出：
# 📋 任务列表
# └── 1: 项目文档 (进行中)
#     ├── 1.1: 编写README (已完成)
#     └── 1.2: API文档 (待处理)
```

### 6. 查看下一个任务

显示所有可以开始的任务（没有未完成的依赖）。

```bash
task next

# 示例输出：
#       📋 可执行的任务       
# ┏━━━━┳━━━━━━━━━━┳━━━━━━━━┓
# ┃ ID ┃ 标题     ┃ 优先级 ┃
# ┡━━━━╇━━━━━━━━━━╇━━━━━━━━┩
# │ 1  │ 项目文档 │ high   │
# └────┴──────────┴────────┘
```

## 数据存储

任务数据保存在当前项目目录下的 `tasks.json` 文件中。这种设计使得：
- 任务数据与项目代码一起版本控制
- AI 助手可以直接读取和修改任务数据
- 便于在团队中共享任务状态
- 方便查看和编辑任务数据

## 使用场景

1. **个人项目管理**
   - 跟踪项目进度
   - 分解大任务为小任务
   - 设置任务优先级

2. **团队协作**
   - 在代码仓库中管理任务
   - 通过 Git 共享任务状态
   - 跟踪依赖关系

3. **日常工作管理**
   - 待办事项管理
   - 进度追踪
   - 任务规划

## 开发相关

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 运行测试

```bash
pytest
```

### 构建项目

```bash
python -m build
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

- Kaleo Zhou ([@kaleozhou](https://github.com/kaleozhou))
- Email: kaleovip@163.com

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 相关链接

- GitHub: https://github.com/kaleozhou/tasks-manager
- PyPI: https://pypi.org/project/task-manager-cli/
- Bug 报告: https://github.com/kaleozhou/tasks-manager/issues 