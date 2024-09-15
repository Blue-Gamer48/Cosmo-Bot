import discord
from discord.commands import slash_command, permissions, Option
from discord.ext import commands
from discord.ui import modal
from utils.database import connect

class serversettings(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
def setup(bot):
    bot.add_cog(serversettings(bot))