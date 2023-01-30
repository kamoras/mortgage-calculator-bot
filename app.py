#!/usr/bin/python3
import os
import discord
import math
#import time

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    """Listens for specific user messages."""
    # Current time (Used for cache busting character thumbnails).
    # epoch_time = int(time.time())

    # If the author is the bot do nothing.
    if message.author == client.user:
        return

    if message.content.startswith("!mortgage help"):
        msg = "Calculate a mortgage payment by using the following command\n!mortgage <price> <down> <length> <interest>"
        await message.channel.send(msg)
    # of form !mortgage <price> <down> <length> <interest>
    elif message.content.startswith("!mortgage"):
        split = message.content.split()

        price = float(split[1])
        down = float(split[2])
        length = float(split[3]) * 12
        interest = (float(split[4]) / 12) / 100

        monthly_payment = (price - down) * interest * ((math.pow((1+interest), length))/((math.pow((1+interest), length))-1))

        await message.channel.send("Monthly payment: $" + str(round(monthly_payment, 2)))
    


@client.event
async def on_ready():
    print("Launch Succesful! The bot is now listening for commands...")

# Discord API Settings
DISCORD_BOT_TOKEN = str(os.environ.get("DISCORD_BOT_TOKEN"))
if DISCORD_BOT_TOKEN is None or DISCORD_BOT_TOKEN == "":
    print(
        "Missing Discord bot token. Please refer to https://github.com/JamesIves/discord-wow-armory-bot#configuration for more details"
    )
    quit()

else:
    client.run(DISCORD_BOT_TOKEN)
