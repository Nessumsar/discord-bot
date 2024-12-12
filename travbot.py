import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import presence
import checklist

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = None

def run_bot():
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is logged in as {bot.user}")
        try:
            synced = await bot.tree.sync()  # Syncs slash commands with Discord
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(f"Error syncing commands: {e}")
        bot.loop.create_task(presence.reset_woken_up_users())

    @bot.event
    async def on_message(message):
        if message.author == bot.user or not message.mentions:
            return
        await presence.check_if_mentioned_user_is_awake(message)

    @bot.event
    async def on_presence_update(before, after):
        await presence.welcome_member_waking_up(before, after, bot)

    @bot.tree.command(name="checklist", description="View the shared checklist.")
    async def view_checklist(interaction: discord.Interaction):
        await checklist.view_checklist(interaction)

    @bot.tree.command(name="add_task", description="Add a task to the shared checklist.")
    async def add_task(interaction: discord.Interaction, village: str, task: str):
        await checklist.add_task(interaction, village, task)

    @bot.tree.command(name="toggle_task", description="Toggle the status of a task in the checklist.")
    async def toggle_task(interaction: discord.Interaction, village: str, task: str):
        await checklist.toggle_task(interaction, village, task)

    @bot.tree.command(name="reset_checklist", description="Reset the shared checklist.")
    async def reset_checklist(interaction: discord.Interaction):
        await checklist.reset_checklist(interaction)

    bot.run(TOKEN)

