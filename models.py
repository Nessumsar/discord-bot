from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    name: str
    completed: bool = False

@dataclass
class Group:
    name: str
    tasks: List[Task] = field(default_factory=list)

    def get_task_by_index(self, index: int) -> Task:
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Task index out of range.")
        return self.tasks[index]

    def get_task_index(self, task_name: str) -> int:
        for i, task in enumerate(self.tasks):
            if task.name == task_name:
                return i
        raise ValueError(f"Task '{task_name}' not found in group '{self.name}'.")

    def delete_task_by_index(self, index):
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Task index {index} is out of range.")
        self.tasks.pop(index)
