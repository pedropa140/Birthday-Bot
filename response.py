import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random

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
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
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
        error = False

        def is_valid_date(year, month, day):
            try:
                date = datetime.datetime(int(year), month, int(day))
                return True
            except ValueError:
                return False
            
        if month_mapping.get(birthday_month.lower()) is None:
            result_title = f'**ERROR**'
            result_description = f'ERROR HAS OCCURRED. PLEASE TRY AGAIN**'
            embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Birthday-Bot says:")
            embed.set_footer(text="/addbirthday")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
            return

        if not is_valid_date(birthday_year, month_mapping.get(birthday_month.lower()), birthday_day):
            result_title = f'**ERROR**'
            result_description = f'ERROR HAS OCCURRED. PLEASE TRY AGAIN**'
            embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Birthday-Bot says:")
            embed.set_footer(text="/addbirthday")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
            return
        
        users.insert_user(int(interaction.user.id), str(interaction.user), month_mapping.get(birthday_month.lower()), int(birthday_day), int(birthday_year))
        result_title = f'**User Created**'
        result_description = f'User created for **{interaction.user.mention}**'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/addbirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

async def wishbirthday(interaction : discord.Interaction, username : str, users : UserDatabase):
    def is_today(date):
        today = datetime.datetime.today()
        return date.year == today.year and date.month == today.month and date.day == today.day
    info = users.get_birthday_via_username(username)
    print(info)
    if users.user_name_exists(username):
        if is_today(datetime.datetime(2024, info[0], info[1])):
            random_number = random.randint(1, 15)
            result_description = f'{interaction.user.mention} wished a Happy Birthday to <@{users.get_id(username, info[0], info[1])}> '
            embed = discord.Embed(description=result_description, color=0xFF5733)
            file = discord.File(f'images/birthday_gifs/image_{random_number}.gif', filename= f'image_{random_number}.gif')
            embed.set_image(url=f'attachment://image_{random_number}.gif')
            embed.set_author(name="Birthday-Bot says:")
            embed.set_footer(text="/wishbirthday")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=False)
        else:
            result_title = f'**ERROR**'
            result_description = f'USER **{username}\'s** BIRTHDAY IS NOT TODAY'
            embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Birthday-Bot says:")
            embed.set_footer(text="/wishbirthday")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    else:
        result_title = f'**ERROR**'
        result_description = f'USER **{username}** DOES NOT EXIST IN DATABASE'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/wishbirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

async def removebirthday(interaction : discord.Interaction, users : UserDatabase):
    if not users.user_exists(interaction.user.id):
        result_title = f'User Not Found'
        result_description = f'User not found for **{interaction.user.mention}**'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/removebirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
    else:
        users.remove_user(interaction.user.id)
        result_title = f'**User Deleted**'
        result_description = f'User deleted for **{interaction.user.mention}**'
        embed = discord.Embed(title=result_title, description=result_description, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/removebirthday")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

async def help(interaction : discord.Interaction):
    result_title = f'How to use Reminder-Bot'
    embed = discord.Embed(title=result_title, url = "https://github.com/pedropa140/Reminder-Bot", color=0xFF5733)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Birthday-Bot says:")
    embed.add_field(name="/addbirthday **[Month]** **[Day]** **[Year]** ", value="Adds Birthday to the Database!", inline=False)
    embed.add_field(name="/wishbirthday **[Discord User]**", value="Wish a Someone a Happy Birthday!", inline=False)
    embed.add_field(name="/removebirthday", value="Removes a Birthday from the Database!", inline=False)
    embed.set_footer(text="/help")
    await interaction.response.send_message(file=file, embed=embed, ephemeral=True)