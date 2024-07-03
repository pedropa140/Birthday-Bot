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
import time

load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    usersDatabase = UserDatabase('users.db')
    
    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')
            
            print(f'{bot.user} is now running!')
            bot.loop.create_task(happybirthday(bot, usersDatabase))
        except Exception as e:
            print(e)

    async def happybirthday(bot : commands.Bot, userDatabase : UserDatabase):
        while True:
            users_list = []
            for user in usersDatabase.retrieve_users():
                users_list.append(user[0])
            date = datetime.datetime.today()
            
            for user in users_list:
                user_info = userDatabase.get_birthday_via_id(user)
                if date.month == user_info[0] and date.day == user_info[1]:
                    random_number = random.randint(1, 15)
                    age = date.year - user_info[2]
                    def get_ordinal(n):
                        if 10 <= n % 100 <= 20:
                            suffix = 'th'
                        else:
                            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
                        return str(n) + suffix
                    age = str(get_ordinal(age))
                    title = f'Happy Birthday to You! Congrats on your {age} Birthday!'
                    embed = discord.Embed(title=title, color=0xFF5733)
                    file = discord.File(f'images/birthday_gifs/image_{random_number}.gif', filename= f'image_{random_number}.gif')
                    embed.set_image(url=f'attachment://image_{random_number}.gif')
                    embed.set_author(name="Birthday-Bot says:")
                    embed.set_footer(text="/happybirthday")

                    send_message = await bot.fetch_user(user)
                    await send_message.send(file=file, embed=embed)
                
                    user_guilds = []
                    user = int(user)

                    for guild in bot.guilds:
                        member = guild.get_member(user)
                        if guild:
                            for channel in guild.channels:
                                if channel.name.lower() == 'birthday-bot' and str(channel.type).lower() == 'text':
                                    if member:
                                        user_guilds.append([guild, guild.id, channel.id])
                    
                    if user_guilds:
                        for guild in user_guilds:
                            send_message = bot.get_guild(guild[1]).get_channel(guild[2])
                            if send_message:
                                random_number = random.randint(1, 15)
                                title = f'***Happy Birthday to <@{member.id}> !***'
                                embed = discord.Embed(description=title, color=0xFF5733)
                                file = discord.File(f'images/birthday_gifs/image_{random_number}.gif', filename= f'image_{random_number}.gif')
                                embed.set_image(url=f'attachment://image_{random_number}.gif')
                                embed.set_author(name="Birthday-Bot says:")
                                embed.set_footer(text="/happybirthday")
                                await send_message.send(file=file, embed=embed)

            await asyncio.sleep(86400)

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
    async def wishbirthday(interaction : discord.Interaction, discord_user : discord.Member):
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

    @bot.tree.command(name = "help", description = "Shows how to use Birthday-Bot and how to set it up!")
    async def help(interaction : discord.Interaction):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')
        
        await response.help(interaction)

    bot.run(TOKEN)
    
