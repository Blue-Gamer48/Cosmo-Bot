import asyncio
import random
import discord
from discord.ext import commands
from discord import slash_command ,InteractionContextType, IntegrationType
from cogs.Botverwaltung import BotVerwaltung
from utils.embeds import blacklist_error_embed
class allgemein(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
    @slash_command(name="gutenmorgen",description="Wünscht allen Usern einen Guten Morgen",
    integration_types = {IntegrationType.guild_install, IntegrationType.user_install},
    contexts = {InteractionContextType.guild,InteractionContextType.private_channel})
    async def gutenmorgen(self, ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed)
            return
        embed_gm = discord.Embed(title="Einen wunderschönen guten Morgen.",description=f"der User {ctx.author.mention} wünscht euch einen Tollen Start in den Tag",color=0x00ff00)
        embed_gm.set_footer(text=f'Gesendet von: {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed_gm)
    @slash_command(name="gutenacht",description="Wünscht allen Usern eine Gute nacht",
    integration_types = {IntegrationType.guild_install, IntegrationType.user_install},
    contexts = {InteractionContextType.guild,InteractionContextType.private_channel})
    async def gutenacht(self, ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed)
            return
        embed_gn = discord.Embed(title="Gute Nacht.",description=f"der User {ctx.author.mention} wünscht euch eine gute Nacht",color=0x00ff00)
        embed_gn.set_footer(text=f'Gesendet von: {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed_gn)
    @slash_command(name="hallo",description="Sage Hallo",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild,InteractionContextType.private_channel})
    async def hello(self, ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            if await BotVerwaltung.is_blacklist(ctx):
                await ctx.respond(embed=blacklist_error_embed)
                return
        gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif']
        msg = f':wave: {random.choice(gifs)}'
        await ctx.respond(msg)
def setup(bot):
    bot.add_cog(allgemein(bot))