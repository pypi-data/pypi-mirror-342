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

## 使用方法

### 创建新任务

```bash
task add "完成项目文档" -d "编写项目的README和API文档" -p high
```

### 添加子任务

```bash
task add-subtask 1 "编写README.md" -d "包含项目说明和使用示例"
```

### 更新任务状态

```bash
task status 1 in_progress
```

### 添加任务依赖

```bash
task depend 2 1  # 任务2依赖于任务1
```

### 查看所有任务

```bash
task list
```

### 查看下一个待处理任务

```bash
task next
```

## 配置

任务数据默认保存在用户主目录的 `.taskmaster` 文件夹下，每个项目会创建独立的任务文件。

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