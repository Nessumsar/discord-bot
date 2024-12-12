import discord
from datetime import datetime
import asyncio
import pytz

local_tz = pytz.timezone('Europe/Stockholm')
woken_up_users = set()

async def welcome_member_waking_up(before, after, bot):
    channel = bot.get_channel(1315675558163648562)
    for member in channel.members:
        if after == member:
            if before.status != after.status and after.status == discord.Status.online:
                current_time = datetime.now(local_tz)
                if (4 <= current_time.hour < 16) and (after.id not in woken_up_users):
                    # Send a message in the specific channel
                    print(f'{member} woke up at {current_time}')
                    await channel.send(f"Good morning <@{after.id}>!")
                    woken_up_users.add(after.id)


async def reset_woken_up_users():
    # Reset the woken_up_users set if the time is between 16:00 PM and 04:00 AM
    while True:
        now = datetime.now(local_tz)
        print(f"Checking if the list should be reset: {now}")

        # Check if it's after 16:00 PM and before 04:00 AM
        if now.hour >= 16 or now.hour < 4:
            print("Resetting the list of users who woke up today.")
            woken_up_users.clear()

        # Sleep for an hour and check again
        await asyncio.sleep(3600)