import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot("!", intents=intents)

message = 'Hello! Question of the day From Thor: '


@bot.event
async def on_ready():
    print("Logged in")
    with open('links.txt') as f:
        lines = f.readlines()
        urls = [line.strip() for line in lines]
    print(urls)
    send_message.start(urls)


@tasks.loop(hours=24)
async def send_message(urls):
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    print(f"Channel is: {channel}")
    while len(urls) > 0:
        url = urls.pop()
        await channel.send(message + url)
        print(f"Sent message: {message + url}")
        await asyncio.sleep(86400)  # wait 1 day


@send_message.before_loop
async def before():
    await bot.wait_until_ready()
    print(f"Finished waiting")


# @client.event
# async def on_ready():
#     await client.get_channel(target_channel_id).send('Hello! I am thor')
#     await asyncio.sleep(2)


if __name__ == '__main__':
    # client.run(TOKEN)
    bot.run(TOKEN)


