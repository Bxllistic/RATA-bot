import discord
from discord.ext import commands
import asyncio
from bot_utils.roleId import Roles

class ShoutCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Shout Command cog healthy.")

    @commands.command(name = "shout")
    @commands.has_any_role(Roles.junior_instructor, Roles.instructor, Roles.junior_instructor_trainer, Roles.supervisor, Roles.head_instructor, Roles.board_of_directors, Roles.assistant_director, Roles.director, Roles.advisor)
    async def shout(self, ctx, *, tier : str):
        shout_chnl = self.client.get_channel(427008571079786507)
        ranking_chnl = self.client.get_channel(836662029128957992)
        if ("tier 1" in tier.lower() or "1" in tier.lower() or "one" in tier.lower() or "t1" in tier.lower()) and "," not in tier.lower():
            embed = discord.Embed(title="Shout Confirmation", description="You are about to shout a **tier 1**.\n\nReact below to confirm the shout.", color=0x0000ff)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
            embed.set_footer(text="Times out in 15 seconds.")
            msg1 = await ctx.reply(embed = embed)
            await msg1.add_reaction("<:RO_success:773206804850016276>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:RO_success:773206804850016276>"
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await msg1.edit(embed = discord.Embed(description="**Timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                await msg1.clear_reaction("<:RO_success:773206804850016276>")
            else:
                await shout_chnl.send(f"<@&516976454731563020> A **Tier 1** is being hosted at the facility by **{ctx.author.mention}**! Slocking in **`10`** minutes.\n\n> __Trained Spectators__ may join 2 minutes after this shout.\n\nhttps://www.roblox.com/games/3553150678/RATA-Training-Facility")
                await ranking_chnl.send("r!shout Tier 1 is being hosted at the facility! Slocking in 10 minutes.")
                await msg1.delete(delay=2.0)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await asyncio.sleep(120)
                await shout_chnl.send(f"<@&751776350691655680> may join now `(Tier 1 hosted by {ctx.author.display_name})`.")
        elif ("tier 2" in tier.lower() or "2" in tier.lower() or "two" in tier.lower() or "t2" in tier.lower()) and "," not in tier.lower():
            embed = discord.Embed(title="Shout Confirmation", description="You are about to shout a **tier 2**.\n\nReact below to confirm the shout.", color=0x0000ff)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
            embed.set_footer(text="Times out in 15 seconds.")
            msg1 = await ctx.reply(embed = embed)
            await msg1.add_reaction("<:RO_success:773206804850016276>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:RO_success:773206804850016276>"
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await msg1.edit(embed = discord.Embed(description="**Timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                await msg1.clear_reaction("<:RO_success:773206804850016276>")
            else:
                await shout_chnl.send(f"<@&516976276201013261> A **Tier 2** is being hosted at the facility by **{ctx.author.mention}**! Slocking in **`10`** minutes.\n\n> __Trained Spectators__ may join 2 minutes after this shout.\n\nhttps://www.roblox.com/games/3553150678/RATA-Training-Facility")
                await ranking_chnl.send("r!shout Tier 2 is being hosted at the facility! Slocking in 10 minutes.")
                await msg1.delete(delay=2.0)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await asyncio.sleep(120)
                await shout_chnl.send(f"<@&751776350691655680> may join now `(Tier 2 hosted by {ctx.author.display_name})`.")
        elif ("tier 3" in tier.lower() or "3" in tier.lower() or "three" in tier.lower() or "t3" in tier.lower()) and "," not in tier.lower():
            embed = discord.Embed(title="Shout Confirmation", description="You are about to shout a **tier 3**.\n\nReact below to confirm the shout.", color=0x0000ff)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
            embed.set_footer(text="Times out in 15 seconds.")
            msg1 = await ctx.reply(embed = embed)
            await msg1.add_reaction("<:RO_success:773206804850016276>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:RO_success:773206804850016276>"
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await msg1.edit(embed = discord.Embed(description="**Timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                await msg1.clear_reaction("<:RO_success:773206804850016276>")
            else:
                await shout_chnl.send(f"<@&516976069027430401> A **Tier 3** is being hosted at the facility by **{ctx.author.mention}**! Slocking in **`10`** minutes.\n\n> __Trained Spectators__ may join 2 minutes after this shout.\n\nhttps://www.roblox.com/games/3553150678/RATA-Training-Facility")
                await ranking_chnl.send("r!shout Tier 3 is being hosted at the facility! Slocking in 10 minutes.")
                await msg1.delete(delay=2.0)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await asyncio.sleep(120)
                await shout_chnl.send(f"<@&751776350691655680> may join now `(Tier 3 hosted by {ctx.author.display_name})`.")
        elif ("tier 4" in tier.lower() or "4" in tier.lower() or "four" in tier.lower() or "t4" in tier.lower()) and "," not in tier.lower():
            embed = discord.Embed(title="Shout Confirmation", description="You are about to shout a **tier 4**.\n\nReact below to confirm the shout.", color=0x0000ff)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
            embed.set_footer(text="Times out in 15 seconds.")
            msg1 = await ctx.reply(embed = embed)
            await msg1.add_reaction("<:RO_success:773206804850016276>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:RO_success:773206804850016276>"
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await msg1.edit(embed = discord.Embed(description="**Timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                await msg1.clear_reaction("<:RO_success:773206804850016276>")
            else:
                await shout_chnl.send(f"<@&516975850764238858> A **Tier 4** is being hosted at the facility by **{ctx.author.mention}**! Slocking in **`10`** minutes.\n\n> __Trained Spectators__ may join 2 minutes after this shout.\n\nhttps://www.roblox.com/games/3553150678/RATA-Training-Facility")
                await ranking_chnl.send("r!shout Tier 4 is being hosted at the facility! Slocking in 10 minutes.")
                await msg1.delete(delay=2.0)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await asyncio.sleep(120)
                await shout_chnl.send(f"<@&751776350691655680> may join now `(Tier 4 hosted by {ctx.author.display_name})`.")
        elif "," in tier.lower():
            tierslist = tier.split(",")
            finaltiers = []
            for i in tierslist:
                x = i.replace(" ","")
                if "tier 4" in x or "4" in x or "four" in x or "t4" in x:
                    finaltiers.append("Tier 4")
                elif "tier 3" in x or "3" in x or "three" in x or "t3" in x:
                    finaltiers.append("Tier 3")
                elif "tier 2" in x or "2" in x or "two" in x or "t2" in x:
                    finaltiers.append("Tier 2")
                elif "tier 1" in x or "1" in x or "one" in x or "t1" in x:
                    finaltiers.append("Tier 1")
                else:
                    await ctx.send(f"\"{i}\" not recognised.")
            tiermsg = ""
            for j in finaltiers:
                if len(tiermsg) < 2:
                    tiermsg += f"`{j}`"
                else:
                    tiermsg += ", " + f"`{j}`"
            embed = discord.Embed(title="Multi Tier Shout Confirmation", description=f"You are about to shout a multi-tier for the following tiers:\n{tiermsg}\n\nReact to confirm.", color=0x0000ff)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
            embed.set_footer(text="Times out in 15 seconds.")
            msg1 = await ctx.reply(embed = embed)
            await msg1.add_reaction("<:RO_success:773206804850016276>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:RO_success:773206804850016276>"
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await msg1.edit(embed = discord.Embed(description="**Timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                await msg1.clear_reaction("<:RO_success:773206804850016276>")
            else:
                pingmsg = ""
                for j in finaltiers:
                    if j == "Tier 1":
                            pingmsg += f" <@&516976454731563020> "
                    elif j == "Tier 2":
                            pingmsg += f" <@&516976276201013261> "
                    elif j == "Tier 3":
                            pingmsg += f" <@&516976069027430401> "
                    elif j == "Tier 4":
                            pingmsg += f" <@&516975850764238858> "
                shoutmsg = ""
                for k in finaltiers:
                    if len(shoutmsg) < 2:
                        shoutmsg += f"{k}"
                    else:
                        shoutmsg += ", " + f"`{k}`"
                await shout_chnl.send(f"{pingmsg}\n**A Multi-Tier with the tiers:**\n{tiermsg}\nis being hosted at the facility by **{ctx.author.mention}**! Slocking in **`10`** minutes.\n\n> __Trained Spectators__ may join 2 minutes after this shout.\n\nhttps://www.roblox.com/games/3553150678/RATA-Training-Facility")
                await ranking_chnl.send(f"r!shout MULTI Tier with: {shoutmsg} is being hosted at the facility! Slocking in 10 minutes.")
                await msg1.delete(delay=2.0)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await asyncio.sleep(120)
                await shout_chnl.send(f"<@&751776350691655680> may join now `(MULTI TIER ({shoutmsg}) hosted by {ctx.author.display_name})`.")
        else:
            await ctx.send("Tier not found, whatcha tryna host bro? :face_with_monocle:")

async def setup(client):
    await client.add_cog(ShoutCog(client))