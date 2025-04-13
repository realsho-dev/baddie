# status.py
import discord
import asyncio

custom_statuses = [
    {"type": "game", "message": "{prefix}help"},
    {"type": "watching", "message": "{guilds} servers"},
    {"type": "game", "message": "by Ayanokouji"},
    {"type": "playing", "message": "with Discord commands"},
    {"type": "watching", "message": "server chats"},
    {"type": "game", "message": "{prefix}ask for AI fun"},
    {"type": "listening", "message": "user requests"},
    {"type": "playing", "message": "bot games"},
    {"type": "watching", "message": "{users} users"},
    {"type": "game", "message": "Kuro-bot V2"},
    {"type": "listening", "message": "to Ayanokouji's code"},
    {"type": "watching", "message": "server moderation"},
    {"type": "playing", "message": "with roles"},
    {"type": "game", "message": "{prefix}ping"},
    {"type": "watching", "message": "emoji updates"},
    {"type": "listening", "message": "channel logs"},
    {"type": "playing", "message": "with AI responses"},
    {"type": "game", "message": "Llama AI"},
    {"type": "watching", "message": "server boosts"},
    {"type": "listening", "message": "to your commands"},
    {"type": "playing", "message": "in {guilds} guilds"},
    {"type": "game", "message": "{prefix}botinfo"},
    {"type": "watching", "message": "server info"},
    {"type": "listening", "message": "for {prefix}mute"},
    {"type": "playing", "message": "with embeds"},
]

async def update_status(bot):
    while True:
        for status in custom_statuses:
            message = status["message"].format(
                prefix=bot.command_prefix,
                guilds=len(bot.guilds),
                users=sum(g.member_count for g in bot.guilds)
            )
            if status["type"] == "game" or status["type"] == "playing":
                activity = discord.Game(name=message)
            elif status["type"] == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=message)
            elif status["type"] == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=message)
            else:
                continue
            await bot.change_presence(activity=activity)
            await asyncio.sleep(20)