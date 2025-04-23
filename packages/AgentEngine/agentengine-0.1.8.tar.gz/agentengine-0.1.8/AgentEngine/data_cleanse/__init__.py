"""
数据清洗模块

此模块提供使用Unstructured分区库从各种源清洗数据的功能。
它支持处理文件、URL和文本内容，并提供用于管理清洗任务的简单API。

组件:
- core: 数据清洗核心实现
- task_store: 任务存储管理
- async_task_manager: 异步任务管理
- cleanse_worker_pool: 数据清洗工作池
"""

__version__ = "0.1.0"

# 导出核心组件
from .task_store import TaskStore, TaskStatus
from .cleanse_worker_pool import CleanseWorkerPool
from .async_task_manager import AsyncTaskManager
from .core import DataCleanseCore

__all__ = [
    "TaskStore",
    "TaskStatus",
    "CleanseWorkerPool",
    "AsyncTaskManager",
    "DataCleanseCore"
] 