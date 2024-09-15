import discord
from discord.ext import commands
class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user = None
    @commands.Cog.listener()
    async def on_command(self, ctx):  # Log Commands
        print(f"[Command Run] {ctx.author} Used `{ctx.message.content}` in {ctx.guild}.")
    @commands.Cog.listener()
    async def on_application_command_error(context, exception):
        print(f"Exception: {exception}")
    async def on_command_error(self, ctx, error,permission = PermissionError):  # Global Command Error Handler
        if isinstance(error, commands.MissingRequiredArgument):
            msg = f'du musst das Parameter: `{error.param.name} angeben`'
        elif isinstance(error, commands.BadArgument):
            msg = error.args[0].replace('"', '`')
            msg += f'\n\n nutze `{self.prefix}help'
            await ctx.send(msg)
            await ctx.send(f'**hat nicht die Berechtigung:**\n{permission}')
        elif isinstance(error, commands.BotMissingPermissions):
            permissions = '\n'.join(f'- {p.title().replace("_", " ")}' for p in error.missing_permissions)
            await ctx.send(f'**{self.user.mention} hat nicht die Berechtigung:**\n{permissions}')
        elif isinstance(error, discord.NotFound):
            print('nfnd')
        else:
            print(error)


def setup(bot):
    bot.add_cog(errors(bot))