import discord
from discord.ext import commands
import time

class StaffLogsCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Staff Logs cog healthy.")

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message : discord.Message):
        public_categories = {427010162176425985,607011650783936547,605182353458987018,427013550137933824}
        if str(message.channel.type) == 'text' and message.channel.category_id not in public_categories and message.guild != None and message.guild.id == 427007974947553280 and message.author.bot == False and message.content.lower().startswith("r.") == False and len(message.content) <= 2030:
            guild = self.client.get_guild(427007974947553280)
            log_channel = guild.get_channel(782261834530553867)
            embed = discord.Embed(description = f"**Message sent by {message.author.mention} deleted in {message.channel}:**\n\n{message.content}\n\n> Originally sent on <t:{round((message.created_at).timestamp())}:F>", color = 0xf04747, timestamp = discord.utils.utcnow())
            embed.set_author(name=message.author, icon_url=message.author.avatar)
            embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")
            await log_channel.send(embed=embed)          

    @commands.Cog.listener('on_message_edit')
    async def on_message_edit(self, before : discord.Message, after: discord.Message):
        public_categories = {427010162176425985,607011650783936547,605182353458987018,427013550137933824}
        if str(before.channel.type) == 'text' and before.channel.category_id not in public_categories and before.guild != None and before.guild.id == 427007974947553280 and before.author.bot == False and before.content!=after.content and before.content.lower().startswith("r.") == False and len(before.content) <= 950 and len(after.content) <= 950:
            guild = self.client.get_guild(427007974947553280)
            log_channel = guild.get_channel(782261834530553867)
            ogtime = f'<t:{round((before.created_at).timestamp())}:F>'
            now = f'<t:{round(time.time())}:F>'
            embed = discord.Embed(description = f"**Message sent by {after.author.mention} edited in {after.channel}: [Jump to Message]({after.jump_url})**", color = 0xffea61, timestamp = discord.utils.utcnow())
            embed.add_field(name="Before",value=f"{str(before.content)}\n\n> {ogtime}")
            embed.add_field(name="After",value=f"{str(after.content)}\n\n> {now}")
            embed.set_author(name=after.author, icon_url=after.author.avatar)
            embed.set_footer(text=f"Author ID: {after.author.id} | Message ID: {after.id}")
            await log_channel.send(embed=embed)

async def setup(client):
    await client.add_cog(StaffLogsCog(client))