import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from .manager import TaskManager
from .models import TaskStatus, TaskPriority

console = Console()

@click.group()
def cli():
    """任务管理器命令行工具"""
    pass

@cli.command()
@click.argument('title')
@click.option('--description', '-d', help='任务描述')
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']), default='medium', help='任务优先级')
def add(title, description, priority):
    """添加新任务"""
    manager = TaskManager()
    task = manager.add_task(
        title=title,
        description=description,
        priority=TaskPriority(priority)
    )
    console.print(f"✅ 已添加任务 [bold green]{task.id}[/bold green]: {task.title}")

@cli.command()
@click.argument('parent_id')
@click.argument('title')
@click.option('--description', '-d', help='子任务描述')
def add_subtask(parent_id, title, description):
    """添加子任务"""
    manager = TaskManager()
    subtask = manager.add_subtask(
        parent_id=parent_id,
        title=title,
        description=description
    )
    console.print(f"✅ 已添加子任务 [bold green]{subtask.id}[/bold green]: {subtask.title}")

@cli.command()
@click.argument('task_id')
@click.argument('status', type=click.Choice(['pending', 'in_progress', 'done', 'blocked', 'deferred']))
def status(task_id, status):
    """更新任务状态"""
    manager = TaskManager()
    manager.update_task_status(task_id, TaskStatus(status))
    console.print(f"✅ 已更新任务 [bold green]{task_id}[/bold green] 状态为: {status}")

@cli.command()
@click.argument('task_id')
@click.argument('depends_on')
def depend(task_id, depends_on):
    """添加任务依赖"""
    manager = TaskManager()
    manager.add_dependency(task_id, depends_on)
    console.print(f"✅ 已添加依赖: [bold green]{task_id}[/bold green] 依赖于 [bold green]{depends_on}[/bold green]")

@cli.command()
def next():
    """显示下一个可执行的任务"""
    manager = TaskManager()
    next_tasks = manager.get_next_tasks()
    
    if not next_tasks:
        console.print("📝 没有可执行的任务")
        return

    table = Table(title="📋 可执行的任务")
    table.add_column("ID", style="cyan")
    table.add_column("标题", style="green")
    table.add_column("优先级", style="yellow")
    
    for task in next_tasks:
        table.add_row(task.id, task.title, task.priority)
    
    console.print(table)

@cli.command()
def list():
    """显示所有任务"""
    manager = TaskManager()
    tasks = manager.get_task_tree()
    
    if not tasks:
        console.print("📝 没有任务")
        return

    tree = Tree("📋 任务列表")
    
    for task in tasks:
        status_color = {
            'pending': 'yellow',
            'in_progress': 'blue',
            'done': 'green',
            'blocked': 'red',
            'deferred': 'grey'
        }
        
        task_str = f"[{status_color[task['status']]}]{task['id']}: {task['title']} ({task['status']})[/{status_color[task['status']]}]"
        task_node = tree.add(task_str)
        
        for subtask in task['subtasks']:
            subtask_str = f"[{status_color[subtask['status']]}]{subtask['id']}: {subtask['title']} ({subtask['status']})[/{status_color[subtask['status']]}]"
            task_node.add(subtask_str)
    
    console.print(tree)

if __name__ == '__main__':
    cli() 