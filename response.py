import discord
from discord import app_commands
from discord.ext import commands
import datetime

from users import UserDatabase

async def addbirthday(interaction : discord.Interaction, birthday_month : str, birthday_day : str, birthday_year : str, users : UserDatabase):
    if users.user_exists(interaction.user.id):
        result_title = f'**User Already Created**'
        result_description = f'User already created for **{interaction.user.mention}**'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/addbirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=False)
    else:
        month_mapping = {
            "january": 1, 
            "february": 2, 
            "march": 3, 
            "april": 4, 
            "may": 5, 
            "june": 6, 
            "july": 7, 
            "august": 8, 
            "september": 9, 
            "october": 10, 
            "november": 11, 
            "december": 12
        }

        users.insert_user(int(interaction.user.id), month_mapping.get(birthday_month.lower()), int(birthday_day), int(birthday_year))
        result_title = f'**User Created**'
        result_description = f'User created for **{interaction.user.mention}**'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/addbirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=False)