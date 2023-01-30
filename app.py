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
    try:
        if message.content.startswith("!financebot help"):
            msg = "Welcome to finance bot!\n!financebot mortgage help\n!financebot mortgage <price> <down> <length> <interest>\n!financebot bondask help\nfinancebot bondask <coupon> <interest> <numPeriods> <bondValue>\n"
            await message.channel.send(msg)
        elif message.content.startswith("!financebot mortgage help"):
            msg = "Calculate a mortgage payment by using the following command\n!mortgage <price> <down> <length> <interest>"
            await message.channel.send(msg)
        # of form !mortgage <price> <down> <length> <interest>
        elif message.content.startswith("!financebot mortgage"):
            split = message.content.split()

            price = float(split[2])
            down = float(split[3])
            length = float(split[4]) * 12
            interest = (float(split[5]) / 12) / 100

            monthly_payment = (price - down) * interest * ((math.pow((1+interest), length))/((math.pow((1+interest), length))-1))

            await message.channel.send("Monthly payment: $" + str(round(monthly_payment, 2)))
        elif message.content.startswith("!financebot bondask help"):
            msg = "Calculate bond ask by using the following command\n!bondask <coupon> <interest> <numPeriods> <bondValue>"
            await message.channel.send(msg)
        elif message.content.startswith("!financebot bondask"):
            split = message.content.split()
            # ((coupon / 2) / (interest rate / 2)) * 1 - (1 / ((1 + (interest / 2))^(numPeriods-1)))

            coupon = float(split[2])
            interest = float(split[3]) / 100
            num_periods = float(split[4])
            bond_value = float(split[5])

            p1 = float((coupon / 2) / (interest / 2))
            p2 = (1 / math.pow(1 + float(interest / 2), num_periods - 1))
            p3 = bond_value + (coupon / 2)
            p4 = math.pow((1 + (interest / 2)), num_periods)

            bond_ask = (p1 * (1 - p2)) + (p3 / p4)
            await message.channel.send("Bond ask: $" + str(round(bond_ask, 2)))
        elif message.content == "!financebot":
            msg = "Incomplete financebot command. Valid commands are:\n!financebot mortgage help\n!financebot mortgage <price> <down> <length> <interest>\n!financebot bondask help\nfinancebot bondask <coupon> <interest> <numPeriods> <bondValue>\n"
            await message.channel.send(msg)
    except:
        msg = "Invalid financebot command. Valid commands are:\n!financebot mortgage help\n!financebot mortgage <price> <down> <length> <interest>\n!financebot bondask help\nfinancebot bondask <coupon> <interest> <numPeriods> <bondValue>\n"
        await message.channel.send(msg)

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
