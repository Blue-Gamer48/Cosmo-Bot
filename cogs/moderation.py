import discord
from discord.ext import commands
from discord import slash_command ,InteractionContextType, IntegrationType
from discord.ext.commands import bot
from discord.commands import Option, OptionChoice
from discord import ui
from cogs.Botverwaltung import BotVerwaltung

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(name="unban",description="Entbannt einen User",
                   integration_types={IntegrationType.guild_install},
                   contexts={InteractionContextType.guild})
    async def unban(self, ctx, member: discord.User):
        if member == ctx.author:
            ban_error = discord.Embed(title="Fehler",
                                      description="Du Bist doch nicht Gebannt wenn du hier Schreibst Witzbold!!!",
                                      color=discord.Colour.dark_red())
            await ctx.respond(embed=ban_error)
        else:
            await ctx.guild.unban(member)
            unban_message = discord.Embed(title="User Entbannt", color=discord.Colour.dark_red())
            unban_message.add_field(name="Moderator", value=f"{ctx.author}")
            unban_message.add_field(name="User:",value=member)
            await ctx.respond(embed=unban_message)

    @slash_command(name="ban", description="Bant einen User vom Server",
                   integration_types={IntegrationType.guild_install},
                   contexts={InteractionContextType.guild})
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason="Keine Begründung Angegeben"):
        await ctx.defer()
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.respond("Ich habe keine Berechtigung, Mitglieder zu bannen.")
            return
        if member == ctx.author:
            ban_error = discord.Embed(title="Fehler",
                                      description="Du kannst dich nicht Selbst vom Server Bannen was hast du überhaupt davon?",
                                      color=discord.Colour.dark_red())
            await ctx.respond(embed=ban_error)
            return
        if ctx.guild.me.top_role <= member.top_role:
            await ctx.respond("Ich kann kein Mitglied bannen, das eine höhere oder gleiche Rolle als ich hat.")
            return

        # Überprüfen, ob der Bot dem Benutzer eine private Nachricht senden kann
        try:
            ban_message_user = discord.Embed(title="Du wurdest Gebannt", color=discord.Colour.dark_red())
            ban_message_user.add_field(name="Moderator", value=f"{ctx.author}")
            ban_message_user.add_field(name="Bangrund:", value=f"{reason}")
            await member.send(embed=ban_message_user)
        except:
            await ctx.respond(f"Ich kann {member.mention} keine private Nachricht senden, kann aber trotzdem bannen.")

        # Versuchen, das Mitglied zu bannen und eine Nachricht zu senden
        try:
            ban_message_server = discord.Embed(title="User Gebannt", color=discord.Colour.dark_red())
            ban_message_server.add_field(name="Name:", value=f"{member}")
            ban_message_server.add_field(name="ID:", value=f"{member.id}")
            ban_message_server.add_field(name="Bangrund:", value=f"{reason}")
            ban_message_server.add_field(name="Moderator", value=f"{ctx.author}")
            await member.ban(reason=reason)
            await ctx.respond(embed=ban_message_server)
        except:
            await ctx.respond(f"Es gab ein Problem beim Bannen von {member.mention}.")

def setup(bot):
    bot.add_cog(moderation(bot))