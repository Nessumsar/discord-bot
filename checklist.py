import discord
from discord.ext import commands
import json
import os

CHECKLIST_FILE = "shared_checklist.json"

def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as file:
            return json.load(file)
    return {}

def save_checklist(data):
    with open(CHECKLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)


async def view_checklist(interaction: discord.Interaction):
    data = load_checklist()
    if not data:
        await interaction.response.send_message(content="The checklist is empty!")
        return

    response = "Shared Checklist:\n"
    for village, tasks in data.items():
        response += f"\n**{village}**:\n"
        for task in tasks[0]:  # Assuming only one task dictionary per village
            status = '✅' if tasks[0][task] else '❌'
            response += f"- {task}: {status}\n"

    await interaction.response.send_message(content=response)


async def add_task(interaction: discord.Interaction, village: str, task: str):
    async def add_task(interaction: discord.Interaction, village: str, task: str):
        data = load_checklist()
        if village not in data:
            data[village] = [{}]  # Initialize a new village with an empty task list

        # Add the task to the village (set to False by default)
        if task not in data[village][0]:
            data[village][0][task] = False
            save_checklist(data)
            await interaction.response.send_message(content=f"Task '{task}' added to {village}.")
        else:
            await interaction.response.send_message(content=f"Task '{task}' already exists in {village}.")

async def toggle_task(interaction: discord.Interaction, village: str, task: str):
    data = load_checklist()
    if village not in data or task not in data[village][0]:
        await interaction.response.send_message(content=f"Task '{task}' not found in {village}.")
        return

    data[village][0][task] = not data[village][0][task]
    save_checklist(data)
    status = "✅" if data[village][0][task] else "❌"
    await interaction.response.send_message(content=f"Task '{task}' in {village} is now {status}.")

async def reset_checklist(interaction: discord.Interaction):
    save_checklist({})
    await interaction.response.send_message(content="The checklist has been reset!")