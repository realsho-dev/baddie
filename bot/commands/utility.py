# utility.py
from discord.ext import commands
import discord
import requests
import time

start_time = time.time()

def setup_utility(bot):
    @bot.hybrid_command(name="addemoji")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(ctx: commands.Context, name: str = None, *, source: str = None):
        if not name or not source:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}addemoji <name> <url>`", color=0xCD5C5C))
            return
        if source.startswith("http"):
            response = requests.get(source)
            image = response.content
            emoji = await ctx.guild.create_custom_emoji(name=name, image=image)
            embed = discord.Embed(
                title="Emoji Added",
                description=f"Emoji: {emoji}\nName: {name}",
                color=0x9ACD32
            )
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title="Error", description="Invalid URL", color=0xCD5C5C))

    @bot.hybrid_command(name="addrole")
    @commands.has_permissions(manage_roles=True)
    async def addrole(ctx: commands.Context, member: discord.Member = None, role: discord.Role = None):
        if not member or not role:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}addrole @user @role`", color=0xCD5C5C))
            return
        await member.add_roles(role)
        embed = discord.Embed(
            title="Role Added",
            description=f"Target: {member.name}\nRole: {role.name}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="afk")
    async def afk(ctx: commands.Context, *, message: str = "Away"):
        embed = discord.Embed(
            title="AFK Set",
            description=f"User: {ctx.author.name}\nMessage: {message}",
            color=0x4682B4
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="avatar")
    async def avatar(ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title="Avatar",
            description=f"User: {member.name}",
            color=0x4682B4
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="botinfo")
    async def botinfo(ctx: commands.Context):
        uptime = int(time.time() - start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        embed = discord.Embed(
            title="Bot Details",
            description="Bot statistics",
            color=0x4682B4
        )
        embed.add_field(name="Name", value=f"{bot.user.name}#{bot.user.discriminator}", inline=True)
        embed.add_field(name="ID", value=str(bot.user.id), inline=True)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(g.member_count for g in bot.guilds), inline=True)
        embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Creator", value="Ayanokouji", inline=True)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="channelinfo")
    async def channelinfo(ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(
            title="Channel Info",
            description=f"Name: {channel.name}",
            color=0x4682B4
        )
        embed.add_field(name="ID", value=str(channel.id), inline=True)
        embed.add_field(name="Type", value=str(channel.type).capitalize(), inline=True)
        embed.add_field(name="Created", value=channel.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="Position", value=channel.position, inline=True)
        embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
        embed.add_field(name="Slowmode", value=f"{channel.slowmode_delay}s" if channel.slowmode_delay else "Off", inline=True)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="clearafk")
    async def clearafk(ctx: commands.Context):
        embed = discord.Embed(
            title="AFK Cleared",
            description=f"User: {ctx.author.name}",
            color=0x4682B4
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="createrole")
    @commands.has_permissions(manage_roles=True)
    async def createrole(ctx: commands.Context, *, name: str = None):
        if not name:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}createrole <name>`", color=0xCD5C5C))
            return
        role = await ctx.guild.create_role(name=name)
        embed = discord.Embed(
            title="Role Created",
            description=f"Role: {role.name}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="deleteemoji")
    @commands.has_permissions(manage_emojis=True)
    async def deleteemoji(ctx: commands.Context, name: str = None):
        if not name:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}deleteemoji <name>`", color=0xCD5C5C))
            return
        emoji = discord.utils.get(ctx.guild.emojis, name=name)
        if emoji:
            await emoji.delete()
            embed = discord.Embed(
                title="Emoji Deleted",
                description=f"Name: {name}",
                color=0xCD5C5C
            )
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Name: {name} not found", color=0xCD5C5C))

    @bot.hybrid_command(name="deleterole")
    @commands.has_permissions(manage_roles=True)
    async def deleterole(ctx: commands.Context, role: discord.Role = None):
        if not role:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}deleterole @role`", color=0xCD5C5C))
            return
        await role.delete()
        embed = discord.Embed(
            title="Role Deleted",
            description=f"Role: {role.name}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="editnickname")
    @commands.has_permissions(manage_nicknames=True)
    async def editnickname(ctx: commands.Context, member: discord.Member = None, *, nickname: str = None):
        if not member or not nickname:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}editnickname @user <nickname>`", color=0xCD5C5C))
            return
        old_nick = member.nick or member.name
        await member.edit(nick=nickname)
        embed = discord.Embed(
            title="Nickname Updated",
            description=f"Old: {old_nick}\nNew: {nickname}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="emotes")
    async def emotes(ctx: commands.Context):
        emotes = " ".join([str(e) for e in ctx.guild.emojis]) or "None"
        embed = discord.Embed(
            title="Server Emojis",
            description=f"Emojis: {emotes}",
            color=0x4682B4
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="listroles")
    async def listroles(ctx: commands.Context):
        roles = ", ".join([r.name for r in ctx.guild.roles])
        embed = discord.Embed(
            title="Server Roles",
            description=f"Roles: {roles}",
            color=0x4682B4
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="ping")
    async def ping(ctx: commands.Context):
        embed = discord.Embed(
            title="Ping",
            description=f"Latency: {round(bot.latency * 1000)}ms",
            color=0x4682B4
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def removerole(ctx: commands.Context, member: discord.Member = None, role: discord.Role = None):
        if not member or not role:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}removerole @user @role`", color=0xCD5C5C))
            return
        await member.remove_roles(role)
        embed = discord.Embed(
            title="Role Removed",
            description=f"Target: {member.name}\nRole: {role.name}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="roleinfo")
    async def roleinfo(ctx: commands.Context, role: discord.Role = None):
        if not role:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}roleinfo @role`", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Role Info",
            description=f"Name: {role.name}",
            color=0x4682B4
        )
        embed.add_field(name="ID", value=str(role.id), inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Permissions", value=", ".join([p[0].replace("_", " ").title() for p in role.permissions if p[1]]) or "None", inline=False)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="servericon")
    async def servericon(ctx: commands.Context):
        if not ctx.guild.icon:
            await ctx.send(embed=discord.Embed(title="Error", description="No server icon", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Server Icon",
            description="Server image",
            color=0x4682B4
        )
        embed.set_image(url=ctx.guild.icon.url)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="serverinfo")
    async def serverinfo(ctx: commands.Context):
        guild = ctx.guild
        embed = discord.Embed(
            title="Server Info",
            description=f"Name: {guild.name}",
            color=0x4682B4
        )
        embed.add_field(name="ID", value=str(guild.id), inline=True)
        embed.add_field(name="Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}", inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        embed.add_field(name="Max Members", value=guild.max_members, inline=True)
        embed.add_field(name="Verification", value=str(guild.verification_level).capitalize(), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="userinfo")
    async def userinfo(ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title="User Info",
            description=f"Name: {member.name}",
            color=0x4682B4
        )
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="Status", value=str(member.status).capitalize(), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.name, inline=True)
        embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles[1:]]), inline=False)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)