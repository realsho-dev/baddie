# moderation.py
from discord.ext import commands
import discord
import asyncio

log_channel = None

def setup_moderation(bot):
    async def log_action(action, target, reason, moderator):
        if log_channel:
            channel = bot.get_channel(log_channel)
            if channel:
                await channel.send(embed=discord.Embed(
                    title=f"Log: {action}",
                    description=f"Target: {target}\nReason: {reason or 'None'}\nBy: {moderator}",
                    color=0x708090
                ))

    @bot.hybrid_command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}ban @user [reason]`", color=0xCD5C5C))
            return
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Ban Enforced",
            description=f"Target: {member.name}\nReason: {reason or 'None'}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Ban", member.name, reason, ctx.author)

    @bot.hybrid_command(name="clearwarnings")
    @commands.has_permissions(manage_messages=True)
    async def clearwarnings(ctx: commands.Context, member: discord.Member = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}clearwarnings @user`", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Warnings Cleared",
            description=f"Target: {member.name}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Clear Warnings", member.name, None, ctx.author)

    @bot.hybrid_command(name="clearslowmode")
    @commands.has_permissions(manage_channels=True)
    async def clearslowmode(ctx: commands.Context):
        await ctx.channel.edit(slowmode_delay=0)
        embed = discord.Embed(
            title="Slowmode Off",
            description="Channel: This channel",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Clear Slowmode", ctx.channel.name, None, ctx.author)

    @bot.hybrid_command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}kick @user [reason]`", color=0xCD5C5C))
            return
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Kick Enforced",
            description=f"Target: {member.name}\nReason: {reason or 'None'}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Kick", member.name, reason, ctx.author)

    @bot.hybrid_command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(ctx: commands.Context):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(
            title="Channel Locked",
            description="Channel: This channel",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Lock", ctx.channel.name, None, ctx.author)

    @bot.hybrid_command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(ctx: commands.Context, member: discord.Member = None, time: str = None):
        if not member or not time:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}mute @user <time>`", color=0xCD5C5C))
            return
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted") or await ctx.guild.create_role(name="Muted")
        await member.add_roles(muted_role)
        embed = discord.Embed(
            title="Mute Enforced",
            description=f"Target: {member.name}\nDuration: {time}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Mute", member.name, f"Duration: {time}", ctx.author)
        await asyncio.sleep(int(time[:-1]) * 60 if time.endswith('m') else int(time))
        await member.remove_roles(muted_role)

    @bot.hybrid_command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx: commands.Context, amount: int = None):
        if not amount:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}purge <number>`", color=0xCD5C5C))
            return
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Messages Purged",
            description=f"Count: {amount}",
            color=0xCD5C5C
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed, delete_after=5)
        await log_action("Purge", f"{amount} messages", None, ctx.author)

    @bot.hybrid_command(name="setlogchannel")
    @commands.has_permissions(manage_channels=True)
    async def setlogchannel(ctx: commands.Context, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}setlogchannel #channel`", color=0xCD5C5C))
            return
        global log_channel
        log_channel = channel.id
        embed = discord.Embed(
            title="Log Channel Set",
            description=f"Channel: {channel.mention}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(ctx: commands.Context, seconds: int = None):
        if seconds is None:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}slowmode <seconds>`", color=0xCD5C5C))
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(
            title="Slowmode On",
            description=f"Delay: {seconds} seconds",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Slowmode", f"{seconds}s in {ctx.channel.name}", None, ctx.author)

    @bot.hybrid_command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(ctx: commands.Context, user_id: int = None):
        if not user_id:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}unban user_id`", color=0xCD5C5C))
            return
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="Unban Enforced",
            description=f"Target: {user.name}",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Unban", user.name, None, ctx.author)

    @bot.hybrid_command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(ctx: commands.Context):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(
            title="Channel Unlocked",
            description="Channel: This channel",
            color=0x9ACD32
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Unlock", ctx.channel.name, None, ctx.author)

    @bot.hybrid_command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(ctx: commands.Context, member: discord.Member = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}unmute @user`", color=0xCD5C5C))
            return
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            embed = discord.Embed(
                title="Unmute Enforced",
                description=f"Target: {member.name}",
                color=0x9ACD32
            )
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
            await log_action("Unmute", member.name, None, ctx.author)
        else:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Target: {member.name} not muted", color=0xCD5C5C))

    @bot.hybrid_command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}warn @user [reason]`", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Warning Issued",
            description=f"Target: {member.name}\nReason: {reason or 'None'}",
            color=0xDAA520
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await log_action("Warn", member.name, reason, ctx.author)

    @bot.hybrid_command(name="warnings")
    async def warnings(ctx: commands.Context, member: discord.Member = None):
        if not member:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}warnings @user`", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Warnings",
            description=f"Target: {member.name}\nStatus: Not implemented",
            color=0xDAA520
        )
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)