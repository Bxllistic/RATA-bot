import discord
from discord.ext import commands
import asyncio

class SupervisorCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Supervisor cog healthy.")

    @commands.command(name = "supervisorfree")
    async def supervisorfree(self,ctx):
        if "supervisor-request" not in ctx.channel.name:
            return
        else:
            embed = discord.Embed(title="Supervision opportunity available!",description=f"{ctx.author.mention} is open to supervise a training. React if you're available.")
            embed.set_footer(text=f"{ctx.author}",icon_url=f"{ctx.author.avatar}")
            await ctx.message.delete(delay=0) 
            msg = await ctx.send(embed = embed)
            await msg.add_reaction("<:RO_success:773206804850016276>")

            def check(reaction,user):
                return reaction.message.id == msg.id and str(reaction.emoji) == "<:RO_success:773206804850016276>" and user.bot == False
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=21600.0, check=check)
            except asyncio.TimeoutError:
                try:
                    await msg.delete(delay=0)
                    await ctx.author.send("<:RO_error:773206804758790184> Your supervision request has surpassed 6 hours without any activity and has been deleted automatically.")
                except:
                    pass
            else:
                await user.send(f"<:RO_success:773206804850016276> You have accepted `{ctx.author.display_name}`'s supervision opportunity. DM him/her to discuss training specifics.")
                await ctx.author.send(f"<:RO_success:773206804850016276> `{user.display_name}` has accepted your supervision opportunity. Expect a DM from them soon.")
                await msg.delete(delay=0)

async def setup(client):
    await client.add_cog(SupervisorCog(client))