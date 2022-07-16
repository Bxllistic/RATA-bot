import discord	
from discord.ext import commands
from discord.ext import menus
import time	
import re
from bot_utils.roleId import Roles


def display_time(seconds, granularity=2):	
    result = []	
    for name, count in intervals:	
        value = int(seconds // count)	
        if value:
            seconds -= value * count	
            if value == 1:	
                name = name.rstrip('s')	
            result.append("{} {}".format(value, name))
    if len(result[:granularity])==0:
        return 'less than a second'
    else:
        return ', '.join(result[:granularity])



class MenuSource(menus.ListPageSource):

    def __init__(self, data, client):	
        self.client = client	
        super().__init__(data, per_page=1)

    async def format_page(self, menu, data):	
        if len(data) == 3:	
            # For edits	
            before = data[0]	
            after = data[1]	
            giventime = float(data[2])	
            curtime = time.time()	
            secs = curtime - giventime	
            saved_time = display_time(secs)	
				
            for m in re.finditer("<@![^> ]*>", before.content):	
                beforeCont = before.content	
                ping = re.sub('<@!','',m.group())	
                ping = re.sub('>','',ping)	
                guild = self.client.get_guild(before.guild.id)	
                user = guild.get_member(int(ping))	
                before.content = beforeCont[0:m.start():] + f"@{user}" + beforeCont[m.end()::]	
            if len(before.content)>1016:
                before.content = before.content[:1013] + "..."

            for m in re.finditer("<@![^> ]*>", after.content):	
                afterCont = after.content	
                ping = re.sub('<@!','',m.group())	
                ping = re.sub('>','',ping)	
                guild = self.client.get_guild(after.guild.id)	
                user = guild.get_member(int(ping))	
                after.content = afterCont[0:m.start():] + f"@{user}" + afterCont[m.end()::]
            if len(after.content)>1016:
                after.content = after.content[:1013] + "..."
                        	
            embed=discord.Embed(color=before.author.color).set_author(name=f"Message from {str(before.author)} edited", icon_url=str(before.author.avatar)).set_footer(text=f"{menu.current_page+1}/{self.get_max_pages()} | edited {str(saved_time)} ago").add_field(name="Before",value=f"```\n{before.content.replace('```','')}\n```").add_field(name="After",value=f"```\n{after.content.replace('```','')}\n```")	
            return embed

        else: 	
            # For deletes	
            msg = data[0]	
            giventime = float(data[1])	
            curtime = time.time()	
            secs = curtime - giventime	
            saved_time = display_time(secs)	
				
            for m in re.finditer("<@![^> ]*>", msg.content):	
                msgCont = msg.content	
                ping = re.sub('<@!','',m.group())	
                ping = re.sub('>','',ping)	
                guild = self.client.get_guild(msg.guild.id)	
                user = guild.get_member(int(ping))	
                msg.content = msgCont[0:m.start():] + f"@{user}" + msgCont[m.end()::]
            if len(msg.content)>2040:
                msg.content = msg.content[:2037]+"..."

            	
            urls = msg.attachments	
            if len(urls) == 0 :	
                embed=discord.Embed(description=f"```\n{msg.content.replace('```','')}\n```",color=msg.author.color).set_author(name=f"Message from {str(msg.author)} deleted", icon_url=str(msg.author.avatar)).set_footer(text=f"{menu.current_page+1}/{self.get_max_pages()} | deleted {str(saved_time)} ago")	
            else:	
                image = urls[0]	
                if msg.content == "":	
                    embed=discord.Embed(color=msg.author.color).set_author(name=f"Message from {str(msg.author)} deleted", icon_url=str(msg.author.avatar)).set_footer(text=f"{menu.current_page+1}/{self.get_max_pages()} | deleted {str(saved_time)} ago").set_image(url=image.proxy_url)	
                else:	
                    embed=discord.Embed(description=f"```\n{msg.content.replace('```','')}\n```",color=msg.author.color).set_author(name=f"Message from {str(msg.author)} deleted", icon_url=str(msg.author.avatar)).set_footer(text=f"{menu.current_page+1}/{self.get_max_pages()} | deleted {str(saved_time)} ago").set_image(url=image.proxy_url)	
            return embed


bot_snipes = {}	
intervals = (	
    ('weeks', 604800),  # 60 * 60 * 24 * 7	
    ('days', 86400),    # 60 * 60 * 24	
    ('hours', 3600),    # 60 * 60	
    ('minutes', 60),	
    ('seconds', 1),	
    )	

class SniperCog(commands.Cog):	
    
    def __init__(self, client, snipe_limit):	
        self.client = client	
        self.snipe_limit = snipe_limit	
    
    @commands.Cog.listener()	
    async def on_ready(self):	
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Sniper cog healthy.")	
    
    @commands.Cog.listener('on_message_delete')	
    async def sniper_on_message_delete(self, message : discord.Message):	
        global bot_snipes	
        if message.author.bot == False and message.guild != None and message.content.lower().startswith("r.") == False:	
            try:
                if self.snipe_limit != None:
                    if len(bot_snipes[message.channel.id]) == self.snipe_limit:	
                        del bot_snipes[message.channel.id][-1]	
                    bot_snipes[message.channel.id].insert(0,[message,time.time()])	
                else:	
                    bot_snipes[message.channel.id].insert(0,[message,time.time()])	
            except KeyError:	
                bot_snipes[message.channel.id] = [[message,time.time()]]	
    
    @commands.Cog.listener('on_message_edit')	
    async def sniper_on_message_edit(self, before : discord.Message, after: discord.Message):	
        global bot_snipes	
        if before.author.bot == False and before.guild != None and before.content != after.content and before.content.lower().startswith("r.") == False:	
            try:
                if self.snipe_limit != None:
                    if len(bot_snipes[before.channel.id]) == self.snipe_limit:	
                        del bot_snipes[before.channel.id][-1]	
                    bot_snipes[before.channel.id].insert(0,[before,after,time.time()])	
                else:	
                    bot_snipes[before.channel.id].insert(0,[before,after,time.time()])	
            except KeyError:	
                bot_snipes[before.channel.id] = [[before,after,time.time()]]	
    
    @commands.command() 
    @commands.has_any_role(Roles.owner_chairman, Roles.department_overseer, Roles.director, Roles.assistant_director, Roles.advisor, Roles.board_of_directors, Roles.head_instructor, Roles.lead_moderator)
    @commands.guild_only()
    async def snipe(self, ctx, channel : discord.TextChannel = None):	
        channel = channel or ctx.channel	
        try:	
            channelLogList = bot_snipes[channel.id]	
            infoPageHandler = menus.MenuPages(source=MenuSource(channelLogList, self.client), clear_reactions_after=True, delete_message_after=False, timeout=120.0)	
            await infoPageHandler.start(ctx)	
        except KeyError:	
            await ctx.send('<:RO_error:773206804758790184> Nothing to snipe!')	


async def setup(client):	
    await client.add_cog(SniperCog(client, 10))