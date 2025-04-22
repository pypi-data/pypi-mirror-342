from pyhunt import trace


@trace
class Task:
    def __init__(self, name):
        self.name = name
        self.completed = False

    async def complete(self):
        self.completed = True
