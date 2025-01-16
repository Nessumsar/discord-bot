import discord
import json
import os
from models import Group, Task
from typing import List

CHECKLIST_FILE = "shared_checklist.json"


def load_checklist() -> List[Group]:
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as file:
            data = json.load(file)
            groups = []
            for group_name, task_dicts in data.items():
                tasks = [Task(name=task_name, completed=completed) for task_name, completed in task_dicts[0].items()]
                groups.append(Group(name=group_name, tasks=tasks))
            return groups
    return []


def save_checklist(groups: List[Group]) -> None:
    data = {
        group.name: [{task.name: task.completed for task in group.tasks}] for group in groups
    }
    with open(CHECKLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)


async def view_checklist(interaction: discord.Interaction):
    data = load_checklist()
    if not data:
        await interaction.response.send_message("The checklist is empty!")
        return

    message_lines = ["Shared Checklist:"]
    for group_index, group in enumerate(data):
        message_lines.append(f"\n**{group_index+1}: {group.name}**:")
        for task_index, task in enumerate(group.tasks):  # Assuming only one task dictionary per group
            status = '✅' if task.completed else '❌'
            message_lines.append(f"\t{task_index+1}: {task.name} {status}")

    response = "\n".join(message_lines)
    await interaction.response.send_message(response)


async def add_group(interaction: discord.Interaction, group_name: str):
    groups = load_checklist()

    if any(group.name == group_name for group in groups):
        print(f"A group named '{group_name}' already exists.")
        await interaction.response.send_message(f"A group named '{group_name}' already exists.")
        return

    new_group = Group(name=group_name, tasks=[])
    groups.append(new_group)
    save_checklist(groups)
    print(f"Group '{group_name}' has been created successfully with no tasks.")
    await interaction.response.send_message(f"Group '{group_name}' has been created successfully with no tasks.")


async def add_task(interaction: discord.Interaction, group_index: int, task_name: str):
    group_index = group_index - 1 #Decrement by 1 to offset lists starting on 0
    data = load_checklist()

    if group_index < 0 or group_index >= len(data):
        print(f"Invalid group index provided: {group_index}")
        await interaction.response.send_message(f"Invalid group index provided: {group_index+1}")
        return

    group = data[group_index]

    if any(task.name == task_name for task in group.tasks):
        print(f"Task '{task_name}' already exists in group '{group.name}'.")
        await interaction.response.send_message(f"Task '{task_name}' already exists in group '{group.name}'.")
        return

    data[group_index].tasks.append(Task(name=task_name))
    save_checklist(data)
    print(f"Task '{task_name}' added to {group.name}.")
    await interaction.response.send_message(f"Task '{task_name}' added to {group.name}.")


async def toggle_task(interaction: discord.Interaction, group_index: int, task_index: int):
    group_index = group_index - 1
    task_index = task_index - 1 # Decrement by 1 to offset lists starting on 0
    data = load_checklist()

    if group_index < 0 or group_index >= len(data):
        print(f"Invalid group index provided: {group_index}")
        await interaction.response.send_message(f"Invalid group index provided: {group_index}")
        return

    group = data[group_index]
    if group not in data or group.get_task_by_index(task_index) is None:
        print(f"Task '{task_index+1}' not found in {group.name}.")
        await interaction.response.send_message(f"Task '{task_index+1}' not found in {group.name}.")
        return

    task = group.get_task_by_index(task_index)
    task.completed = not task.completed
    save_checklist(data)
    status = "✅" if task.completed else "❌"
    print(f"Task '{task_index+1}' in {group.name} is now {status}.")
    await interaction.response.send_message(f"Task '{task_index+1}' in {group.name} is now {status}.")


async def reset_checklist(interaction: discord.Interaction):
    save_checklist([])
    print("The checklist has been reset!")
    await interaction.response.send_message("The checklist has been reset!")