from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option
from discord import Embed
from discord.utils import format_dt
from ezcord import blacklist
from config import DB_ECO_NAME, DB_BLACKLIST_NAME, DB_ECO_GUILD_SHOP_NAME, DB_ECO_GUILD_SHOP_USER, \
    DB_ECO_GUILD_SHOP_NAME
from utils.database import connect


class BotVerwaltung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.check_blacklist_loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_blacklist_table()

    async def create_blacklist_table(self):
        query = '''CREATE TABLE IF NOT EXISTS blacklist (
                        user_id BIGINT NOT NULL,
                        reason TEXT NOT NULL,
                        moderator_id BIGINT NOT NULL,
                        expires_at DATETIME,
                        PRIMARY KEY (user_id)
                        )'''
        async with connect() as (con, cur):
            await cur.execute(query)
            await con.commit()
        print("Blacklist table created")

    def calculate_expiry(self, duration, duration_type):
        if duration_type == "Lifetime":
            return None

        now = datetime.utcnow()
        if duration_type == "Seconds":
            return now + timedelta(seconds=duration)
        elif duration_type == "Minutes":
            return now + timedelta(minutes=duration)
        elif duration_type == "Hours":
            return now + timedelta(hours=duration)
        elif duration_type == "Days":
            return now + timedelta(days=duration)
        elif duration_type == "Weeks":
            return now + timedelta(weeks=duration)
        elif duration_type == "Months":
            return now + timedelta(days=duration * 30)
        elif duration_type == "Years":
            return now + timedelta(days=duration * 365)
        else:
            return None

    @tasks.loop(minutes=1)
    async def check_blacklist_loop(self):
        async with connect() as (con, cur):
            await cur.execute('SELECT * FROM blacklist')
            rows = await cur.fetchall()
            for row in rows:
                expires_at = row[3]
                if expires_at and datetime.utcnow() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S"):
                    await cur.execute('DELETE FROM blacklist WHERE user_id = %s', (row[0],))
                    await con.commit()

    @staticmethod
    async def is_blacklist(ctx):
        async with connect() as (con, cur):
            await cur.execute("SELECT * FROM blacklist WHERE user_id = %s", (ctx.author.id,))
            result = await cur.fetchone()
        if result:
            if result[3] is not None:
                formatted_time = datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S")
                timestamp = format_dt(formatted_time, "R")
            else:
                timestamp = "Lifetime"

            embed = discord.Embed(title="You are Banned!", description=f"""
                **Oh, it looks like you got banned from the bot**
                > **Expires At:** {timestamp}
                > **Moderator:** <@{result[2]}>

                **Reason:**
                ```{result[1]}```
            """, color=discord.Color.yellow())
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(style=discord.ButtonStyle.link, label="Appeal", url="https://discord.gg/invite"))
            await ctx.respond(embed=embed, view=view)
            return True
        else:
            return False

    @commands.slash_command(name='blacklist_info')
    async def blacklist_info(self, ctx, user: discord.User):
        async with connect() as (con, cur):
            await cur.execute('SELECT user_id, reason, moderator_id, expires_at FROM blacklist WHERE user_id = %s',(user.id,))
            result = await cur.fetchone()

            if result:
                user_id, reason, moderator_id, expires_at = result
                moderator = await self.bot.fetch_user(moderator_id)

                embed = discord.Embed(title="Blacklist Information", color=discord.Color.red())
                embed.add_field(name="User ID", value=user_id, inline=True)
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.add_field(name="Moderator", value=f"{moderator.name}#{moderator.discriminator}", inline=True)
                embed.add_field(name="Expires At", value="Permanent" if expires_at is None else expires_at, inline=True)

                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"{user.name}#{user.discriminator} is not on the blacklist.")

    @commands.slash_command(name="add_blacklist", description="Add user to blacklist")
    @commands.is_owner()
    async def add_blacklist(self, ctx, user: discord.Member, duration: int, duration_type: discord.Option(str, choices=["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years", "Lifetime"]), *, reason: str):
        try:
            if user.id == ctx.author.id:
                pass
                #await ctx.respond("You can't blacklist yourself.", ephemeral=True)
                #return

            expires_at = self.calculate_expiry(duration, duration_type)
            expires_at_str = expires_at.strftime("%Y-%m-%d %H:%M:%S") if expires_at else None

            async with connect() as (con, cur):
                await cur.execute(
                    '''
                    INSERT INTO blacklist (user_id, reason, moderator_id, expires_at)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    reason = VALUES(reason), moderator_id = VALUES(moderator_id), expires_at = VALUES(expires_at)
                    ''',
                    (user.id, reason, ctx.author.id, expires_at_str)
                )
                await con.commit()
                await ctx.respond(f"Der User {user.name} wurde gesperrt", ephemeral=True)

            if expires_at:
                formatted_time = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                timestamp = format_dt(formatted_time, "R")
            else:
                timestamp = "Lifetime"

            embed = discord.Embed(title="User Blacklisted", description=f"""
            User: {user.mention}
            Moderator: {ctx.author.mention}
            Expires At: {timestamp}

            Reason: ```{reason}```
            """, color=0x00FF04)
            await ctx.channel.send(embed=embed)

        except Exception as e:
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)


        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @add_blacklist.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(name='remove-blacklist')
    @commands.is_owner()
    async def remove_blacklist(self, ctx, user: discord.User):
        try:
            async with connect() as (con, cur):
                await cur.execute(f"SELECT user_id FROM `{DB_BLACKLIST_NAME}` WHERE user_id = %s", (user.id,))
                await con.commit()
                result = await cur.fetchone()
                if result:
                    await cur.execute('DELETE FROM blacklist WHERE user_id = %s', (user.id,))
                    await con.commit()
                    await ctx.respond(f"{user.name} has been removed from the blacklist.")
                else:
                    await ctx.respond(f"{user.name} is not on the blacklist.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @commands.slash_command(name="db_eco_create", description="Erstellt die Datenbanktabelle")
    @commands.is_owner()
    async def db_eco_create(self, ctx: discord.ApplicationContext):
        async with connect() as (conn, cur):
            await cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {DB_ECO_NAME} (
                    user_id BIGINT PRIMARY KEY,
                    money BIGINT DEFAULT 0,
                    job VARCHAR(255)
                )
            """)
            await cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {DB_ECO_GUILD_SHOP_NAME} (
                    guild_id BIGINT PRIMARY KEY,
                    price BIGINT DEFAULT 0,
                    item VARCHAR(255)
                )
            """)
            await cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {DB_ECO_GUILD_SHOP_USER} (
                    guild_id BIGINT,
                    item VARCHAR(255),
                    user_id BIGINT,
                    PRIMARY KEY (guild_id, item)
                )
            """)
            await ctx.respond("Datenbanktabelle wurde erstellt.")

    @db_eco_create.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(name="herunterfahren", description="Bot herunterfahren")
    @commands.is_owner()
    async def herunterfahren(self, ctx):
        embed = Embed(
            title="Bot Herunterfahren",
            description="Der Bot wird heruntergefahren... 🛑",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        await self.bot.close()

    @herunterfahren.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(name="status", description="Ändere den Status des Bots")
    @commands.is_owner()
    async def status(self, ctx,
                     status: Option(str, "Wähle einen Status", choices=["online", "idle", "dnd", "offline"])):
        status_dict = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "offline": discord.Status.offline
        }
        await self.bot.change_presence(status=status_dict[status])
        embed = Embed(
            title="Status Geändert",
            description=f"Bot-Status geändert zu {status} 🟢" if status == "online" else f"Bot-Status geändert zu {status} 🟡" if status == "idle" else f"Bot-Status geändert zu {status} ⛔" if status == "dnd" else f"Bot-Status geändert zu {status} ⚪",
            color=discord.Color.green() if status == "online" else discord.Color.gold() if status == "idle" else discord.Color.red() if status == "dnd" else discord.Color.light_gray()
        )
        await ctx.respond(embed=embed)

    @status.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(name="aktivität", description="Ändere die Aktivität des Bots")
    @commands.is_owner()
    async def aktivität(self, ctx, aktivität_typ: Option(str, "Wähle einen Aktivitätstyp",
                                                         choices=["playing", "streaming", "listening", "watching"]),
                        aktivität_name: Option(str, "Gib den Namen der Aktivität ein")):
        aktivitäten = {
            "playing": discord.Game(name=aktivität_name),
            "streaming": discord.Streaming(name=aktivität_name, url="https://twitch.tv/dein_kanal"),
            "listening": discord.Activity(type=discord.ActivityType.listening, name=aktivität_name),
            "watching": discord.Activity(type=discord.ActivityType.watching, name=aktivität_name)
        }
        await self.bot.change_presence(activity=aktivitäten[aktivität_typ])
        embed = Embed(
            title="Aktivität Geändert",
            description=f"Bot-Aktivität geändert zu {aktivität_typ} {aktivität_name} 🎮" if aktivität_typ == "playing" else f"Bot-Aktivität geändert zu {aktivität_typ} {aktivität_name} 📺" if aktivität_typ == "watching" else f"Bot-Aktivität geändert zu {aktivität_typ} {aktivität_name} 🎧" if aktivität_typ == "listening" else f"Bot-Aktivität geändert zu {aktivität_typ} {aktivität_name} 📡",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)

    @aktivität.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Fehler",
                description="Du hast keine Berechtigung, diesen Befehl zu verwenden.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(BotVerwaltung(bot))
