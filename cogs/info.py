import speedtest
from discord.ext import commands
from discord import slash_command ,InteractionContextType, IntegrationType
from datetime import datetime
import discord

from cogs.Botverwaltung import BotVerwaltung
from config import STEAM_API_KEY
from utils.dropdownmenu import Help_View
from utils.embeds import botinfo_embed, help_embed_default, help_allgemein_embed, blacklist_error_embed
from discord.ext.pages import Paginator, Page
import pytz
import os
from steam_web_api import  Steam
steam= Steam(STEAM_API_KEY)
class info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @slash_command(name="entwickler",description="gibt Infos zum Entwickler des Bots",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def entwickler(self,ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed)
            return
        member = ctx.author
        embed = discord.Embed(title=f"Sourcecode Entwickler", description="Der Bot wird alleine von `Blue_Gamer48#3565` Entwickelt", color=0x03465c)
        embed.set_footer(text=f'Gesendet von: {ctx.author.name} • {ctx.author.id}',icon_url=ctx.author.avatar_url)
        await ctx.respond(embed=embed)
    @slash_command(name="userinfo",description="Gibt Infos zu Einem User",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild})
    async def userinfo(self, ctx,member: discord.Member=None):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        if member == None:
            member = ctx.author
        de = pytz.timezone("Europe/Berlin")
        self.embed = discord.Embed(title=f"Userinfo für {member.name}", description="", color=0x03465c,
                              timestamp=datetime.now().astimezone(tz=de))
        self.embed.add_field(name="Name", value=f"```{member.name}```", inline=False),
        self.embed.add_field(name='Bot', value=f'```{("Ja" if member.bot else "Nein")}```', inline=False)
        self.embed.add_field(name='Nickname', value=f'```{(member.nick if member.nick else "Nicht gesetzt")}```',
                        inline=True)
        self.embed.add_field(name='Server beigetreten', value=f'```{member.joined_at.date()}```', inline=False)
        self.embed.add_field(name='Discord beigetreten', value=f'```{member.created_at.date()}```', inline=False)
        self.embed.add_field(name='Rollen', value=f'```{len(member.roles)}```', inline=False)
        self.embed.add_field(name='Farbe', value=f'```{member.color}```', inline=False)
        self.embed.add_field(name='Booster', value=f'```{("Ja" if member.premium_since else "Nein")}```', inline=False)
        self.embed.add_field(name="Deine Rollen:", value=", ".join([role.mention for role in member.roles if not role.is_default()])),
        self.embed.set_footer(text=f'Gesendet von: {ctx.author.name} • {ctx.author.id}')
        self.embed.set_thumbnail(url=member.avatar)
        await ctx.respond(embed=self.embed)
    @slash_command(name="botinfo",description="Infos zum Bot",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def botinfo(self,ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        await ctx.respond(embed=botinfo_embed,ephemeral=True)

    @slash_command(name="avatar",description="Gibt das profielbid eines Users aus",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def avatar(self, ctx, member: discord.Member=None):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        if member is None:
            embed = discord.Embed(title=f"Avatar von {ctx.author}", color=discord.Colour.blue())
            embed.set_image(url=ctx.author.avatar)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f"Avatar von {member}", color=discord.Colour.blue())
            embed.set_image(url=member.avatar)
            await ctx.respond(embed=embed)
    @slash_command(name="serverinfo",description="gibt infos zum Server aus",
                   integration_types={IntegrationType.guild_install},
                   contexts={InteractionContextType.guild})
    async def serverinfo(self,ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        member = ctx.author
        embed = discord.Embed(title=f"Serverinfo {ctx.guild.name}", description="Informationzu Diesem Server",
                              color=discord.Colour.blue())
        embed.add_field(name='👑Inhaber:', value=f"{ctx.guild.owner}")
        embed.add_field(name='🆔Server ID:', value=f"{ctx.guild.id}",inline=False)
        embed.add_field(name='📆Erstellt am:', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=False)
        embed.add_field(name='👥User:', value=f'{ctx.guild.member_count} Members',inline=False)
        embed.add_field(name='💬Kanäle: ',value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Sprachkanäle',inline=False)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="⭐ • Erstellt von Blue_Gamer48",icon_url=member.avatar)
        await ctx.respond(embed=embed)
    @slash_command(name="servericon",description="Gibt das Icon vom Server aus",
                   integration_types={IntegrationType.guild_install},
                   contexts={InteractionContextType.guild})
    async def servericon(self,ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        embed = discord.Embed(title=f"Avatar vom Server {ctx.guild}", color=discord.Colour.blue())
        embed.set_image(url=ctx.guild.icon)
        await ctx.respond(embed=embed)
    @slash_command(name="speedtest",description="Gibt infos zur Geschwindigkeit des Bots",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def speedtest(self, ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        await ctx.defer()
        s = speedtest.Speedtest(secure=True)
        print("assigned")
        s.get_best_server()
        print("got server")
        s.download()
        print("calculated download")
        s.upload()
        print("calculated upload")
        s = s.results.dict()
        print("made dictionary")
        embed=discord.Embed(title=f"Geschwindigkeits Ttest von: {self.bot.user.name}",color=0x1a36a7)
        embed.add_field(name="Ping:",value=f"{s['ping']}ms")
        embed.add_field(name="Download:",value=f"{round(s['download']/10**6, 3)} Mbits/s")
        embed.add_field(name="Upload:", value=f"{round(s['upload']/10**6, 3)} Mbits/s")
        embed.add_field(name="Server:", value=f"{s['server']['sponsor']}, {s['server']['name']}, {s['server']['country']}")
        embed.add_field(name="Bot:", value=f"{s['client']['isp']} {s['client']['country']}{s['client']['isprating']}")
        del_bot= discord.Embed(title="Bot Abschaltung",
                               description="")
        await ctx.respond(embed=embed)
    @slash_command(name="roles",description="GZeigt dir eine Listedeiner Rollen",
                   integration_types={IntegrationType.guild_install},
                   contexts={InteractionContextType.guild})
    async def roles(self, ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed, ephemeral=True)
            return
        embed = discord.Embed(title=f"Serverrollen von {ctx.guild}",
                              description="\n".join([r.mention for r in ctx.guild.roles if not r.is_default()]),
                              color=0x00ff00)
        embed.set_footer(text="ein Bot von Blue_Gamer48")
        await ctx.respond(embed=embed)
    @slash_command(name="help", description="Gibt das Hilfe Menü aus",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def help(self,ctx):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        await ctx.respond(embed=help_embed_default, view=Help_View(), ephemeral=True)
    @slash_command(name="steam_user_info", description="Gibt Infos zu einem Steam User aus",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def steam_user_info(self,ctx: discord.ApplicationContext,user_id: discord.Option(str,"17 Stelllige Steam ID")):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        if len(user_id) == 17 and user_id.isdigit():
            level = user = steam.users.get_user_steam_level(user_id)
            await ctx.respond(f"Der User ist Level: {level}")
        else:
            await ctx.respond(f"Ungültige ID. Bitte stelle sicher, dass die ID aus genau 16 Ziffern besteht.")
def setup(bot):
    bot.add_cog(info(bot))