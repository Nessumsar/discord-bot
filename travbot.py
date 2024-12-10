import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.default()
intents.message_content = True


def runBot():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            print(
                f'{client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message)

    client.run(TOKEN)    
    

def handle_user_messages(message) ->str:
    content = message.content.lower()
    print(message)
    if(content == '/status'):
        return 'Showing status for x'
    if(content == '/update'):
        return 'Updating x'
    else:
        return 'Unknown command'

async def processMessage(message):
    try:
        botfeedback = handle_user_messages(message)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)