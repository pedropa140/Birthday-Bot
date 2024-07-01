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
        # user = interaction.user
        # user_guilds = [guild for guild in bot.guilds if guild.get_member(user.id)]
        # if user_guilds:
        #     await interaction.response.send_message(f'You are in the following servers: {", ".join(guild.name for guild in user_guilds)}')
        # else:
        #     await interaction.response.send_message('You are not in any of the same servers as the bot.')
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
        
    @bot.tree.command(name = "wishbirthday", description = "Wish a Someone a Happy Birthday!")
    @app_commands.describe(discord_user = "Enter Discord Username")
    async def wishbirthday(interaction : discord.Interaction, discord_user : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.wishbirthday(interaction, discord_user, usersDatabase)

    @bot.tree.command(name = "removebirthday", description = "Removes a Birthday from the Database!")
    async def removebirthday(interaction : discord.Interaction):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')
        
        await response.removebirthday(interaction, usersDatabase)

    bot.run(TOKEN)
    
