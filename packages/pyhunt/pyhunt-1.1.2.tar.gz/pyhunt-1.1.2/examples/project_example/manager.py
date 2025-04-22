from pyhunt import trace, logger
from task import Task


@trace
class TaskManager:
    def __init__(self):
        self.tasks = []

    async def add_task(self, name):
        logger.info(f"Adding task '{name}'.")
        task = Task(name)
        self.tasks.append(task)
        return task

    async def complete_task(self, name):
        for task in self.tasks:
            if task.name == name and not task.completed:
                await task.complete()
                logger.info(f"Task '{name}' completed.")
                return True

        logger.warning(f"Task '{name}' not found or already completed.")
        return False
