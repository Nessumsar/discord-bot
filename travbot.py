import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import presence

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
        for guild in bot.guilds:
            print(
                f'{bot.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
        bot.loop.create_task(presence.reset_woken_up_users())

    @bot.event
    async def on_message(message):
        if message.author == bot.user or not message.mentions:
            return
        await presence.check_if_mentioned_user_is_awake(message)

    @bot.event
    async def on_presence_update(before, after):
        await presence.welcome_member_waking_up(before, after, bot)

    bot.run(TOKEN)

