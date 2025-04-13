# help.py
from discord.ext import commands
import discord
from discord import SelectOption, ui

CATEGORIES = {
    "moderation": {"label": "Moderation", "description": "Server management tools"},
    "utility": {"label": "Utility", "description": "Handy server utilities"},
    "ai": {"label": "AI", "description": "Interact with AI assistant"}
}

COMMANDS = {
    "moderation": [
        {"name": "ban", "syntax": "{prefix}ban @user [reason]", "example": "{prefix}ban @User Spamming", "description": "Ban a user permanently"},
        {"name": "clearwarnings", "syntax": "{prefix}clearwarnings @user", "example": "{prefix}clearwarnings @User", "description": "Clear a user's warnings"},
        {"name": "clearslowmode", "syntax": "{prefix}clearslowmode", "example": "{prefix}clearslowmode", "description": "Disable slowmode"},
        {"name": "kick", "syntax": "{prefix}kick @user [reason]", "example": "{prefix}kick @User Disruptive", "description": "Kick a user out"},
        {"name": "lock", "syntax": "{prefix}lock", "example": "{prefix}lock", "description": "Restrict channel messaging"},
        {"name": "mute", "syntax": "{prefix}mute @user <time>", "example": "{prefix}mute @User 10m", "description": "Mute a user temporarily"},
        {"name": "purge", "syntax": "{prefix}purge <number>", "example": "{prefix}purge 50", "description": "Delete multiple messages"},
        {"name": "setlogchannel", "syntax": "{prefix}setlogchannel #channel", "example": "{prefix}setlogchannel #logs", "description": "Set logging channel"},
        {"name": "slowmode", "syntax": "{prefix}slowmode <seconds>", "example": "{prefix}slowmode 10", "description": "Set message delay"},
        {"name": "unban", "syntax": "{prefix}unban user_id", "example": "{prefix}unban 1234567890", "description": "Unban a user"},
        {"name": "unlock", "syntax": "{prefix}unlock", "example": "{prefix}unlock", "description": "Unrestrict channel messaging"},
        {"name": "unmute", "syntax": "{prefix}unmute @user", "example": "{prefix}unmute @User", "description": "Unmute a user"},
        {"name": "warn", "syntax": "{prefix}warn @user [reason]", "example": "{prefix}warn @User Off-topic", "description": "Warn a user"},
        {"name": "warnings", "syntax": "{prefix}warnings @user", "example": "{prefix}warnings @User", "description": "View user warnings"}
    ],
    "utility": [
        {"name": "addemoji", "syntax": "{prefix}addemoji <name> <url>", "example": "{prefix}addemoji smile https://link.com/smile.png", "description": "Add custom emoji"},
        {"name": "addrole", "syntax": "{prefix}addrole @user @role", "example": "{prefix}addrole @User @Member", "description": "Assign a role"},
        {"name": "afk", "syntax": "{prefix}afk [message]", "example": "{prefix}afk Away", "description": "Set AFK status"},
        {"name": "avatar", "syntax": "{prefix}avatar [@user]", "example": "{prefix}avatar @User", "description": "Show user avatar"},
        {"name": "botinfo", "syntax": "{prefix}botinfo", "example": "{prefix}botinfo", "description": "View bot details"},
        {"name": "channelinfo", "syntax": "{prefix}channelinfo [#channel]", "example": "{prefix}channelinfo #general", "description": "Channel details"},
        {"name": "clearafk", "syntax": "{prefix}clearafk", "example": "{prefix}clearafk", "description": "Clear AFK status"},
        {"name": "createrole", "syntax": "{prefix}createrole <name>", "example": "{prefix}createrole VIP", "description": "Create a role"},
        {"name": "deleteemoji", "syntax": "{prefix}deleteemoji <name>", "example": "{prefix}deleteemoji smile", "description": "Remove custom emoji"},
        {"name": "deleterole", "syntax": "{prefix}deleterole @role", "example": "{prefix}deleterole @VIP", "description": "Delete a role"},
        {"name": "editnickname", "syntax": "{prefix}editnickname @user <nickname>", "example": "{prefix}editnickname @User CoolUser", "description": "Change nickname"},
        {"name": "emotes", "syntax": "{prefix}emotes", "example": "{prefix}emotes", "description": "List server emojis"},
        {"name": "listroles", "syntax": "{prefix}listroles", "example": "{prefix}listroles", "description": "List server roles"},
        {"name": "ping", "syntax": "{prefix}ping", "example": "{prefix}ping", "description": "Check bot latency"},
        {"name": "removerole", "syntax": "{prefix}removerole @user @role", "example": "{prefix}removerole @User @Member", "description": "Remove a role"},
        {"name": "roleinfo", "syntax": "{prefix}roleinfo @role", "example": "{prefix}roleinfo @Admin", "description": "Role details"},
        {"name": "servericon", "syntax": "{prefix}servericon", "example": "{prefix}servericon", "description": "Show server icon"},
        {"name": "serverinfo", "syntax": "{prefix}serverinfo", "example": "{prefix}serverinfo", "description": "Server details"},
        {"name": "userinfo", "syntax": "{prefix}userinfo [@user]", "example": "{prefix}userinfo @User", "description": "User details"}
    ],
    "ai": [
        {"name": "aichannel", "syntax": "{prefix}aichannel #channel", "example": "{prefix}aichannel #ai-chat", "description": "Set AI channel"},
        {"name": "ask", "syntax": "{prefix}ask <question>", "example": "{prefix}ask What's the weather?", "description": "Ask AI a question"},
        {"name": "clearhistory", "syntax": "{prefix}clearhistory", "example": "{prefix}clearhistory", "description": "Clear AI history"}
    ]
}

def setup_help(bot):
    class HelpSelect(ui.Select):
        def __init__(self):
            options = [SelectOption(label=cat["label"], value=key, description=cat["description"]) for key, cat in CATEGORIES.items()]
            super().__init__(placeholder="Select a Category", options=options)

        async def callback(self, interaction: discord.Interaction):
            category = self.values[0]
            embed = discord.Embed(
                title=f"{CATEGORIES[category]['label']} Commands",
                description=f"Category: {CATEGORIES[category]['description']}",
                color=0x4682B4
            )
            commands_text = "\n".join([f"`{cmd['name']}` - {cmd['description']}" for cmd in COMMANDS[category]])
            embed.add_field(name="Commands", value=commands_text or "No commands", inline=False)
            embed.set_footer(text="Created by Ayanokouji")
            await interaction.response.edit_message(embed=embed, view=self.view)

    class HelpView(ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(HelpSelect())

    @bot.hybrid_command(name="help")
    async def help_command(ctx: commands.Context, arg: str = None):
        if not arg:
            embed = discord.Embed(
                title="Command Overview",
                description="A versatile bot for server management and AI interaction.\nCrafted by Ayanokouji for seamless Discord control.",
                color=0x4682B4
            )
            embed.add_field(name="Instructions", value=f"Explore commands by category or specify `{bot.command_prefix}help <command>`", inline=False)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text="Created by Ayanokouji")
            view = HelpView()
            await ctx.send(embed=embed, view=view)
        else:
            cmd_name = arg.lower()
            for category in COMMANDS:
                for cmd in COMMANDS[category]:
                    if cmd["name"] == cmd_name:
                        embed = discord.Embed(
                            title=f"Command: {bot.command_prefix}{cmd['name']}",
                            description=cmd['description'],
                            color=0x9ACD32
                        )
                        embed.add_field(name="Syntax", value=f"`{cmd['syntax'].format(prefix=bot.command_prefix)}`", inline=False)
                        embed.add_field(name="Example", value=f"`{cmd['example'].format(prefix=bot.command_prefix)}`", inline=False)
                        embed.set_footer(text="Created by Ayanokouji")
                        await ctx.send(embed=embed)
                        return
            await ctx.send(embed=discord.Embed(title="Error", description="Command not found", color=0xCD5C5C))