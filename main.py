# main.py
import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from bot.commands.moderation import setup_moderation
from bot.commands.utility import setup_utility
from bot.commands.ai import setup_ai
from bot.commands.help import setup_help
from bot.utils.status import update_status

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", ".")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def setup_bot():
    bot.remove_command("help")
    setup_moderation(bot)
    setup_utility(bot)
    setup_ai(bot)
    setup_help(bot)

    @bot.event
    async def on_ready():
        print(f"Bot online as {bot.user}")
        await bot.tree.sync()
        print("Slash commands synced")
        bot.loop.create_task(update_status(bot))

    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(setup_bot())