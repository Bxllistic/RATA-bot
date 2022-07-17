import discord
from discord.ext import commands
from bot_utils.utilFunctions import *
import traceback
import sys
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import os.path
import asyncio
from datetime import datetime, timedelta
import time
import aiosqlite

#-------------------------------------------------------------
load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix = ['r.','R.', 'r. ', 'R. '], intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="over RATA"), case_insensitive=True)
starttime = time.perf_counter()
#-----------------------------------------------------------

async def get_traceback(error):
    etype = type(error)
    trace = error.__traceback__
    verbosity = 10
    lines = traceback.format_exception(etype, error, trace, verbosity)
    txt = '\n'.join(lines)
    return txt

#-------------------------------------------------------------

client.remove_command("help")

@client.event
async def on_message(message):
    if str(message.channel.type) == "group" or str(message.channel.type) == "private":
        if message.author.bot == False:
            dmlogs = client.get_channel(819640463141109800)
            attachmentStr = ""
            if len(message.attachments) >= 1:
                for att in message.attachments:
                    attachmentStr += f"`Attachment:` {att.url}\n"
            embed = discord.Embed(description = f"**Message sent in {message.channel}:**\n\n{message.content}\n{attachmentStr}\n```Originally sent on {message.created_at} UTC```", color = 0xf04747, timestamp = discord.utils.utcnow())
            embed.set_author(name=message.author, icon_url=message.author.avatar)
            embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")
            await dmlogs.send(embed=embed)
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        commands = client.commands
        og_msg = ctx.message.content
        og_words = og_msg.split()
        check=False
        recommended = {'priority':[], 'mid':[], 'low':[]}
        for command in commands:
            if fuzz.ratio(command.name, og_words[0][2:]) > 85 and len(recommended["priority"]) < 4:
                recommended["priority"].append(f"\n> r.{command.name}")
                check=True
            elif fuzz.ratio(command.name, og_words[0][2:]) > 70 and len(recommended["mid"]) < 4:
                recommended["mid"].append(f"\n> r.{command.name}")
                check=True
            elif fuzz.ratio(command.name, og_words[0][2:]) > 50 and len(recommended["low"]) < 4:
                recommended["low"].append(f"\n> r.{command.name}")
                check=True
        recommendList = ''.join(recommended["priority"])
        if recommendList.count('>') < 4:
            recommendList += ''.join(recommended["mid"][:4-recommendList.count('>')])
            if recommendList.count('>') < 4:
                recommendList += ''.join(recommended["low"][:4-recommendList.count('>')])
        if check==False:
            embed = discord.Embed (title=f"Oops.", description="This command doesn't match anything in our bot")
            embed.set_thumbnail (url="https://media.discordapp.net/attachments/733993878511812778/788054592495288360/image0.gif")
            embed.set_footer(text=f"Command ran by {ctx.author.name}")
            await ctx.reply(embed=embed)
        elif check==True:
            embed = discord.Embed (title=f"Oops.", description="This command doesn't match anything in our bot"+"\n\nDid you mean: "+recommendList)
            embed.set_thumbnail (url="https://media.discordapp.net/attachments/733993878511812778/788054592495288360/image0.gif")
            embed.set_footer(text=f"Command ran by {ctx.author.name}")
            await ctx.reply(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        if ctx.message.content == "r.feedback":
            embed = discord.Embed(title = "⚠️ Command on Cooldown", description="You need to wait **`{:.2f}`**s to prevent clogging.".format(error.retry_after), colour = 0xcc1b1b)
            await ctx.reply(embed=embed)
        elif ctx.message.content in ["r.specpass","r.specfail"]:
            embed = discord.Embed(title = "⚠️ Command on Cooldown", description="Duplicate result prevention system triggered! Please wait for **`{:.2f}`**s and then use the command again.".format(error.retry_after), colour = 0xcc1b1b)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title = "⚠️ Command on Cooldown", description="You need to wait **`{:.2f}`**s to prevent API congestion.".format(error.retry_after), colour = 0xcc1b1b)
            await ctx.reply(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MissingAnyRole):
        return await ctx.message.add_reaction('<:missingroles:876142198415052831>')
    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        return await ctx.reply(embed=discord.Embed(description=f'<:missingroles:876142198415052831> You are missing the <@&{error.missing_role}> role.', color=discord.Color.red()))
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        print(f'{currentTimeErrorDXB()} Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        print('-'*20)
        return
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.reply("<:RO_error:773206804758790184> You cannot use this command in DMs, please use it in the appropriate channel in RATA.")
        return
    elif isinstance(error, discord.ext.commands.errors.PrivateMessageOnly):
        await ctx.reply("<:RO_error:773206804758790184> You cannot use this command here, please use it in DMs.")
        return
    else:
        print(f'{currentTimeErrorDXB()} Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        print('-'*20)
        errortraceback = await get_traceback(error)
        if len(errortraceback) > 2022:
            direc = f"/home/container/error_logs/log-{datetime.now().timestamp()}.txt"
            with open(direc, 'w') as file:
                file.write(errortraceback)
            file = discord.File(direc, filename="Error Log.txt")
            embed=discord.Embed(title=f'⚠️ An error has occured in {ctx.command}',description = f"**Full Traceback**\n`Too large to display, check attached file`.", color = 0xFF0000, timestamp = discord.utils.utcnow())   
            embed.add_field(name="Condensed Error",value=f'```fix\n{error}\n```',inline=False)
            msg = ctx.message.content[::25] + "..." if len(ctx.message.content) > 20 else ctx.message.content
            embed.set_author(name=f"Input: {msg}")
            embed.set_footer(text=f"Invoked by {ctx.author} [{ctx.author.id}]", icon_url=ctx.author.avatar)
            await client.get_channel(858327267071361064).send(embed = embed, file = file)
        else:
            embed=discord.Embed(title=f'⚠️ An error has occured in {ctx.command}',description = f"**Full Traceback**```py\n{errortraceback[:2022]}\n```", color = 0xFF0000, timestamp = discord.utils.utcnow())
            embed.add_field(name="Condensed Error",value=f'```fix\n{error}\n```',inline=False)
            msg = ctx.message.content[::25] + "..." if len(ctx.message.content) > 20 else ctx.message.content
            embed.set_author(name=f"Input: {msg}")
            embed.set_footer(text=f"Invoked by {ctx.author} [{ctx.author.id}]", icon_url=ctx.author.avatar)
            await client.get_channel(858327267071361064).send(embed = embed)


@client.event 
async def on_ready():
    end = time.perf_counter() - starttime
    print(f"{currentTimeSuccessDXB()} RATA Bot is now online!")
    print(f'{currentTimeSuccessDXB()} Startup time : {round(end,2)}s')

#----------------------------------------------------------------------------------------

async def main():
    async def connect_db():
        try:
            connection = await aiosqlite.connect("/home/container/cogs/moderation.db")
            client.db = connection
        except Exception as e:
            sys.exit(f"{currentTimeErrorDXB(crit=True)} Database Connection failed due to {e}")
    await connect_db()

    client.activityDB = {}
    async def init_db():
        # MODERATOR ACTIVITY CHECKER
        try:
            async with client.db.execute("SELECT id FROM patrol WHERE status=True") as cursor:
                data = await cursor.fetchall()
                for id in data:
                    client.activityDB[id[0]] = time.time()
        except Exception as e:
            sys.exit(f"{currentTimeErrorDXB(crit=True)} Moderator Activity DB Initializer failed due to {e}")
    await init_db()

    async def remove_old_errlogs():
        try:
            for filename in os.listdir('./error_logs'):
                if filename.startswith('log-'):
                    file_createdAt = filename.strip('log-').strip('.txt')
                    if datetime.now() - datetime.fromtimestamp(float(file_createdAt)) > timedelta(days=30):
                        os.remove('./error_logs/' + filename)
        except Exception as e:
            print(f"{currentTimeErrorDXB()} Old error logs remover failed due to {e}")
    await remove_old_errlogs()

    # start the client
    async with client:
        print(f"{currentTimeSuccessDXB()} GitHub repository clone executed!")
        cogCount = 0
        cogSuccess = 0
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogCount += 1
                try:
                    await client.load_extension(f"cogs.{filename[:-3]}")
                    cogSuccess += 1
                except Exception:
                    print(f'{currentTimeErrorDXB()} Failed to load extension {filename}.', file=sys.stderr)
                    traceback.print_exc()
        print(f"{currentTimeSuccessDXB()} {cogSuccess} out of {cogCount} cogs were successfully loaded")
        await client.load_extension('jishaku')
        TOKEN = os.getenv('TOKEN')
        await client.start(f"{TOKEN}")

asyncio.run(main())