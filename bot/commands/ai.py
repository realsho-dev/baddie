from discord.ext import commands
import discord
from bot.ai.client import get_ai_response

ai_channel = None
chat_history = []

def setup_ai(bot):
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        # Don't trigger AI in DMs or without channel
        if not message.guild or not message.channel:
            return

        if ai_channel and message.channel.id == ai_channel:
            chat_history.append(f"{message.author.name}: {message.content}")
            if len(chat_history) > 10:
                chat_history.pop(0)

            prompt = f"{message.author.name}: {message.content}\nAnswer concisely:"
            response = get_ai_response(prompt)
            await message.reply(response)

        if message.content.startswith(bot.command_prefix):
            await bot.process_commands(message)

    @bot.hybrid_command(name="ask")
    async def ask(ctx: commands.Context, *, question: str = None):
        if not question:
            await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Use `{bot.command_prefix}ask <question>`",
                color=0xCD5C5C
            ))
            return

        prompt = f"{ctx.author.name}: {question}\nAnswer concisely:"
        response = get_ai_response(prompt)
        await ctx.send(response)

    @bot.hybrid_command(name="aichannel")
    @commands.has_permissions(manage_channels=True)
    async def set_ai_channel(ctx: commands.Context, channel: discord.TextChannel = None):
        global ai_channel
        target_channel = channel or ctx.channel

        if ai_channel == target_channel.id:
            ai_channel = None
            embed = discord.Embed(
                title="AI Channel Disabled",
                description=f"AI disabled in {target_channel.mention}",
                color=0xCD5C5C
            )
        else:
            ai_channel = target_channel.id
            embed = discord.Embed(
                title="AI Channel Enabled",
                description=f"AI enabled in {target_channel.mention}",
                color=0x9ACD32
            )

        await ctx.send(embed=embed)

    @bot.hybrid_command(name="clearhistory")
    async def clearhistory(ctx: commands.Context):
        global chat_history
        chat_history = []
        await ctx.send(embed=discord.Embed(
            title="History Cleared",
            description="AI chat history reset",
            color=0x9ACD32
        ))
