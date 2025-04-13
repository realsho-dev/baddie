# ai.py
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

        chat_history.append(f"{message.author.name}: {message.content}")
        if len(chat_history) > 10:
            chat_history.pop(0)

        if message.content.startswith(bot.command_prefix):
            await bot.process_commands(message)
            return

        if ai_channel and message.channel.id == ai_channel:
            prompt = f"{message.author.name}: {message.content}\nAnswer concisely:"
            response = get_ai_response(prompt)
            await message.reply(response)

    @bot.hybrid_command(name="ask")
    async def ask(ctx: commands.Context, *, question: str = None):
        if not question:
            await ctx.send(embed=discord.Embed(title="Error", description=f"Use `{bot.command_prefix}ask <question>`", color=0xCD5C5C))
        prompt = f"{ctx.author.name}: {question}\nAnswer concisely:"
        response = get_ai_response(prompt)
        await ctx.send(response)

    @bot.hybrid_command(name="aichannel")
    @commands.has_permissions(manage_channels=True)
    async def set_ai_channel(ctx: commands.Context, channel: discord.TextChannel = None):
        global ai_channel
        if channel:
            if ai_channel == channel.id:
                ai_channel = None
                embed = discord.Embed(title="AI Channel Removed", description=f"AI disabled in {channel.mention}", color=0x9ACD32)
            else:
                ai_channel = channel.id
                embed = discord.Embed(title="AI Channel Set", description=f"AI enabled in {channel.mention}", color=0x9ACD32)
        else:
            ai_channel = ctx.channel.id
            embed = discord.Embed(title="AI Channel Set", description=f"AI enabled in {ctx.channel.mention}", color=0x9ACD32)
        embed.set_footer(text="Created by Ayanokouji")
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="clearhistory")
    async def clearhistory(ctx: commands.Context):
        global chat_history
        chat_history = []
        await ctx.send(embed=discord.Embed(title="History Cleared", description="AI chat history reset", color=0x9ACD32))