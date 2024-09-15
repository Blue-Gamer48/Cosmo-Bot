import discord
from discord.ext import commands
from googletrans import Translator
import os
from discord import slash_command ,InteractionContextType, IntegrationType
from discord.ext.commands import bot
from discord.commands import Option, OptionChoice
from discord import ui
from cogs.Botverwaltung import BotVerwaltung
from utils.embeds import blacklist_error_embed


class tools(commands.Cog):
    def __init__(self, bot):
        self.text = None
        self.bot = bot
    @slash_command(name="translate",description="Übersetze einen Text",                   integration_types={IntegrationType.guild_install,IntegrationType.user_install},
                   contexts={InteractionContextType.guild,InteractionContextType.bot_dm,InteractionContextType.private_channel})
    async def translate(self,ctx, lang, *, thing):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed)
            return
        translator = Translator()
        translation = translator.translate(thing, dest=lang)
        embed = discord.Embed(title=f"Übersetzer    :translate:",description=translation.text,color=0x00ff00)
        embed.set_footer(text="ein Bot von Blue_Gamer48")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(tools(bot))