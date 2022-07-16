import discord
from discord.ext import commands
from discord.ext import menus
import time
from io import BytesIO
import aiohttp, asyncio
from bot_utils.roleId import Roles

def display_time(seconds, granularity=2):
    result = []
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])

class MenuSource(menus.ListPageSource):

    def __init__(self, data):
        super().__init__(data, per_page=20)

    async def format_page(self, menu, data):
        global rolename,num
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"List of members in {rolename} - {num}",description='\n'.join(f'{i+1}. {v}' for i, v in enumerate(data, start=offset))).set_footer(text=f"{menu.current_page+1}/{self.get_max_pages()}")
        return embed

class UtilCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        global bot_start_time
        bot_start_time = time.time()
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Utility commands cog healthy.")
    
    @commands.command()
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content=f':ping_pong: Pong!\n**Typing Latency:** `{round(duration,2)}ms`\n**API Websocket:** `{round(self.client.latency*1000,2)}ms`')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx, *, message = None):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def sayin(self, ctx, channel: discord.TextChannel, *, message = None):
        await channel.send(message)
        await ctx.message.add_reaction('<:RO_success:773206804850016276>')
        await ctx.message.delete(delay=5)

    @commands.command()
    @commands.has_any_role(Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director, Roles.lead_moderator, Roles.head_instructor)
    async def dm(self, ctx, user: discord.User, *, message):
        try:
            await user.send(message)
            await ctx.message.add_reaction('<:RO_success:773206804850016276>')
        except:
            await ctx.send("<a:RO_alert:773211228373647360> DM Failure - Could not DM user.")

    @dm.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.dm <userID/disc> <message>\n```")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def stats(self, ctx):
        global bot_start_time, saved_time_normal
        uptime_secs = time.time() - bot_start_time
        saved_time = display_time(uptime_secs)
        embed=discord.Embed(title="Bot Stats", color=0x2fee92)
        embed.add_field(name="Uptime",value=f"```\n{saved_time}\n```")
        embed.add_field(name="Ping",value=f"```\n{round(self.client.latency * 1000)}ms\n```")
        embed.add_field(name="burger?",value="```\nyes\n```")
        await ctx.send(embed=embed)

    @commands.command(name="inrole")
    @commands.has_permissions(manage_guild=True)
    async def inrole(self,ctx,*,role : discord.Role):
        async with ctx.typing():
            global rolename, num
            rolename = role.name
            memberlist = role.members
            if len(memberlist)==0:
                e=discord.Embed(description=f"<:RO_error:773206804758790184> No members found under `{rolename}`.")
                await ctx.send(embed=e)
            else:
                num = len(memberlist)
                infoPageHandler = menus.MenuPages(source=MenuSource(memberlist), clear_reactions_after=True, delete_message_after=False, timeout=120.0)
                await infoPageHandler.start(ctx)
        
    @inrole.error
    async def inrole_error(self, ctx, error): 
        if isinstance(error, discord.ext.commands.errors.RoleNotFound):
            await ctx.send(f"<a:RO_alert:773211228373647360> Role was not found. Please ensure you are either mentioning, typing out its exact name or role ID of the specific role.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.inrole <role_id/_name/_mention>\n```")

    @commands.command(name="screenshot",aliases=['ss'])
    @commands.has_permissions(manage_guild=True)
    async def screenshot(self,ctx,*,url):
        msg = await ctx.send("**Obtaining results...**")
        
        if url.startswith("-s "):
            url = url.replace("-s ","")
            localcheck = False
            if "-splr" in url:
                url = url.replace("-splr ","")
                localcheck = True
            urlspl = url.split()
            url = "+".join(urlspl)
            try:
                timeout = aiohttp.ClientTimeout(total=60)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(f"https://image.thum.io/get/width/1500/crop/750/noanimate/https://www.google.com/search?q={url}") as resp:
                        if resp.status != 200:
                            return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image. Ensure you are using a valid URL `(https://...)`")
                        data = BytesIO(await resp.read())
                        await msg.delete()
                        if localcheck:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'SPOILER_screenshot.png'))
                        else:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'screenshot.png'))
            except asyncio.TimeoutError:
                return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image (TimeOut).")
        
        elif url.startswith("-i "):
            url = url.replace("-i ","")
            localcheck = False
            if "-splr" in url:
                url = url.replace("-splr ","")
                localcheck = True
            urlspl = url.split()
            url = "+".join(urlspl)
            try:
                timeout = aiohttp.ClientTimeout(total=60)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(f"https://image.thum.io/get/width/1500/crop/750/noanimate/https://www.google.com/search?q={url}&client=img&hl=en&source=lnms&tbm=isch&biw=1366&bih=625") as resp:
                        if resp.status != 200:
                            return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image. Ensure you are using a valid URL `(https://...)`")
                        data = BytesIO(await resp.read())
                        await msg.delete()
                        if localcheck:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'SPOILER_screenshot.png'))
                        else:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'screenshot.png'))
            except asyncio.TimeoutError:
                return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image (TimeOut).")
        
        else:
            localcheck = False
            if "-splr" in url:
                url = url.replace("-splr ","")
                localcheck = True
            if not url.startswith('http'):
                url = 'https://'+url
            if not url.endswith('/'):
                url = url+'/'
            try:
                timeout = aiohttp.ClientTimeout(total=60)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(f"https://image.thum.io/get/width/1920/crop/1000/noanimate/{url}") as resp:
                        if resp.status != 200:
                            return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image. Ensure you are using a valid URL `(https://...)`")
                        data = BytesIO(await resp.read())
                        await msg.delete()
                        if localcheck:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'SPOILER_screenshot.png'))
                        else:
                            return await ctx.reply(f'Requested by **`{ctx.author}`**', file=discord.File(data, 'screenshot.png'))
            except asyncio.TimeoutError:
                return await msg.edit("<a:RO_alert:773211228373647360> An error occured while obtaining the image (TimeOut).")

        
    @screenshot.error
    async def screenshot_error(self, ctx, error): 
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"<a:RO_alert:773211228373647360> Missing necessary argument.\n```\n{ctx.message.content.split()[0]} <URL>\n```")


async def setup(client):
    await client.add_cog(UtilCog(client)) 