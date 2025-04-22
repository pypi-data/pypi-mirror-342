import asyncio
from pyhunt import trace
from manager import TaskManager


@trace
async def main():
    manager = TaskManager()
    await manager.add_task("Write documentation")
    await manager.add_task("Implement feature X")
    await manager.complete_task("Write documentation")
    await manager.complete_task("Nonexistent task")


if __name__ == "__main__":
    asyncio.run(main())
