import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import schedule
import datetime

import response
from users import UserDatabase

load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    usersDatabase = UserDatabase('users.db')
    
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

    @bot.tree.command(name = "addbirthday", description = "Adds Birthday to the Database!")
    @app_commands.describe(birthday_month = "Enter Birthday Month (e.g. January)", birthday_day = "Enter Birthday Day (e.g. 19)", birthday_year = "Enter Birthday Year (e.g. 1994)")
    async def addbirthday(interaction : discord.Interaction, birthday_month : str, birthday_day : str, birthday_year : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.addbirthday(interaction, birthday_month, birthday_day, birthday_year, usersDatabase)
        

    # wish birthday [username]

    # delete user 


    bot.run(TOKEN)
    
