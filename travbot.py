import discord
import os
from dotenv import load_dotenv
import presence

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = None

def runBot():
    global client
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            print(
                f'{client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
        client.loop.create_task(presence.reset_woken_up_users())


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message)

    @client.event
    async def on_presence_update(before, after):
        await presence.welcome_member_waking_up(before, after, client)

    client.run(TOKEN)


async def processMessage(message):
    try:
        botfeedback = handle_user_messages(message)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)


def handle_user_messages(message) ->str:
    content = message.content.lower()
    for mentioned_user in message.mentions:
        if mentioned_user.id not in presence.woken_up_users:
            return f"{mentioned_user.name}, haven't woken up yet!"
    
    if(content.startswith("/")):
        return handle_commands(message)
    else:
        return ''


def handle_commands(message):
    if (message == "/status"):
        return "Status x work in progress"
