import json
import random
import sys
import traceback
import discord
import os
import pytz
from discord.ext import commands
from config import (PREFIX)
from discord.ext.commands import CommandNotFound, bot
from datetime import datetime
def badword():
    with open("./banned_words.json","r") as f:
        bw = json.load(f)
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond(f"Ein unbekannter Fehler ist aufgetreten: {error}", ephemeral=True)
            print(error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed(title = f"Error: {__name__}",description = f"{error}",color = 0xEE0000)
        await ctx.send(embed=em)
        me = self.bot.get_user(792484163684532274)
        await me.send(str(ctx.channel.id), embed=em)--0
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(random.choice(guild.text_channels))
        self.embed = discord.Embed(title=f"Danke fürs Einladen des Bots",
                                   description=f"ich hoffe du wirst viel Spaß Haben mit dem bot um dir die befehle anzeigen zu lassen nutze help",
                                   color=0xc800ff)
        channel = random.choice(guild.text_channels)
        await channel.send(embed=self.embed)
        invite = await guild.text_channels[0].create_invite(reason="Save for Support", max_age=0, max_uses=0, temporary=False, unique=True)
        self.embed2 = discord.Embed(title=f"Saturn Bot Jointe auf einen Server {invite}",
                                   description=f"der Bot: {self.bot.user.name} wurde zu: {guild.name} Eingeladen",
                                   color=0xc800ff)
        channel = self.bot.get_channel(1277701796910858291)
        await channel.send(embed=self.embed2)


def setup(bot):
    bot.add_cog(Events(bot))