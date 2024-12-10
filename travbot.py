import discord
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

woken_up_users = set()

local_tz = pytz.timezone('Europe/Stockholm')
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
        client.loop.create_task(reset_woken_up_users())    


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message)

    @client.event
    async def on_presence_update(before, after):
        if before.status != after.status and after.status == discord.Status.online:
            current_time = datetime.now(local_tz)
            if (4 <= current_time.hour < 16) and (after.id not in woken_up_users):
                # Send a message in the specific channel
                channel = client.get_channel(1315675558163648562)
                await channel.send(f"Good morning <@{after.id}>!")
                woken_up_users.add(after.id)

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
        if mentioned_user.id not in woken_up_users:
            return f"{mentioned_user.name}, haven't woken up yet!"
    
    if(content.startsWith("/")):
        return handle_commands(message)
    else:
        return 'Unknown command'


def handle_commands(message):
    if (message == "/status"):
        return "Status x work in progress"


async def reset_woken_up_users():
    #Reset the woken_up_users set if the time is between 12:00 PM and 04:00 AM
    while True:
        now = datetime.now(local_tz)
        print(f"Checking if the list should be reset: {now}")
        
        # Check if it's after 12:00 PM and before 04:00 AM
        if now.hour >= 12 or now.hour < 4:
            print("Resetting the list of users who woke up today.")
            woken_up_users.clear()
            
        # Sleep for an hour and check again
        await asyncio.sleep(3600)
