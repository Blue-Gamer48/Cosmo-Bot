import random
import discord
from discord import option
from discord.ext import commands
from discord.commands import slash_command

from cogs.Botverwaltung import BotVerwaltung
from utils.database import connect
from config import DB_ECO_NAME , DB_ECO_GUILD_SHOP_USER
from utils.embeds import blacklist_error_embed
import ezcord
class ConfirmJobView(discord.ui.View):
    def __init__(self, job, user_id, cur, con):
        super().__init__(timeout=30)  # Timeout auf 30 Sekunden setzen
        self.job = job
        self.user_id = user_id
        self.cur = cur
        self.con = con
        self.value = None
        self.message = None

    @discord.ui.button(label="Ja", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.cur.execute(f"UPDATE {DB_ECO_NAME} SET job = %s WHERE user_id = %s", (self.job, self.user_id))
        await self.con.commit()
        await interaction.response.send_message(f"Der Job wurde zu {self.job} geändert.", ephemeral=True)
        self.value = True
        self.disable_all_items()
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.errors.NotFound:
                pass  # Nachricht existiert nicht mehr
        self.stop()

    @discord.ui.button(label="Nein", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Der Job wurde nicht geändert.", ephemeral=True)
        self.value = False
        self.disable_all_items()
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.errors.NotFound:
                pass  # Nachricht existiert nicht mehr
        self.stop()

    async def on_timeout(self):
        self.disable_all_items()
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.errors.NotFound:
                pass  # Nachricht existiert nicht mehr


class ConfirmDeleteButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)  # Timeout auf 30 Sekunden gesetzt
        self.value = None

    @discord.ui.button(label="Bestätigen", style=discord.ButtonStyle.danger)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.secondary)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(content="Zeitüberschreitung. Dein Account wurde nicht gelöscht.", view=self)


class Economysystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(name="money", description="Zeigt deinen Geldstand an")
    async def money(self, ctx: discord.ApplicationContext):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        async with connect() as (con, cur):
            await cur.execute(f"SELECT money FROM `{DB_ECO_NAME}` WHERE user_id = %s", (ctx.author.id,))
            money = await cur.fetchone()
            if money is not None:
                money_amount = money[0]  # Das erste Element des Tupels auswählen
                await ctx.respond(f"Du hast {money_amount} Coins")
            else:
                await ctx.respond("Du hast noch keinen Account. Bitte erstelle einen mit `/create_account`.")

    @slash_command(name="add_money", description="Füge Geld hinzu")
    @commands.is_owner()
    async def add_money(self, ctx: discord.ApplicationContext, user: discord.Member, amount: int):
        if user.bot:
            await ctx.respond("Bots können kein Geld erhalten.")
            return
        async with connect() as (con, cur):

            await cur.execute(f"SELECT money FROM `{DB_ECO_NAME}` WHERE user_id = %s", user.id)
            result = await cur.fetchone()

            if result is None:
                await ctx.respond("User has no money record.")
                return

            old_money = result[0]

            new_money = old_money + amount
            await cur.execute(f"UPDATE `{DB_ECO_NAME}` SET money = %s WHERE user_id = %s", (new_money, user.id))
            await con.commit()

            await ctx.respond(f"Der alte Geldstand war {old_money} Coins. Der neue Geldstand ist {new_money} Coins.")

    @slash_command(name="del_account", description="Lösche deinen Datenbank Account")
    async def delete_account(self, ctx: discord.ApplicationContext):
        async with connect() as (con, cur):
            await cur.execute(f"SELECT user_id FROM `{DB_ECO_NAME}` WHERE user_id = %s", (ctx.author.id,))
            result = await cur.fetchone()
            if result is None:
                await ctx.respond("Du hast keinen Account.")
                return

        view = ConfirmDeleteButton()
        message = await ctx.respond("Bist du sicher, dass du deinen Account löschen möchtest?", view=view)

        # Speichere die Nachricht in der Ansicht, damit sie bei einem Timeout aktualisiert werden kann
        view.message = await message.original_response()

        # Warte auf die Interaktion mit der Schaltfläche
        await view.wait()

        if view.value is None:
            await view.message.edit(content="Zeitüberschreitung. Dein Account wurde nicht gelöscht.", view=view)
        elif view.value:
            async with connect() as (con, cur):
                await cur.execute(f"DELETE FROM `{DB_ECO_NAME}` WHERE user_id = %s", (ctx.author.id,))
                await con.commit()
                await view.message.edit(content="Dein Account wurde gelöscht.", view=view)
        else:
            await view.message.edit(content="Dein Account wurde nicht gelöscht.", view=view)


    @slash_command()
    async def create_account(self, ctx: discord.ApplicationContext):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        async with connect() as (conn, cur):
            # Check if User Exists
            await cur.execute(f"SELECT user_id FROM `{DB_ECO_NAME}` WHERE user_id = %s", (ctx.author.id,))
            check_user = await cur.fetchone()
            if check_user is None:
                # When User not Exists add to DB
                await cur.execute(f"INSERT INTO `{DB_ECO_NAME}` (`user_id`, `money`, `job`) VALUES (%s, %s, %s)", (ctx.author.id, 0, None))
                await ctx.respond("Ich habe dir einen Account Erstellt du kannst nun das Economysystem nutzen")
            else:
                print("User is in DB")
                await ctx.respond("User ist schohn in der db")
    @slash_command(name="pay", description="Zahle einem anderen Benutzer Geld")
    async def pay(self, ctx: discord.ApplicationContext, user: discord.Member, amount: int):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        sender = ctx.author
        if sender.bot or user.bot:
            await ctx.respond("Bots können kein Geld erhalten.")
            return
        if sender.id == user.id:
            await ctx.respond("Du kannst dir selbst kein Geld zahlen, das macht keinen Sinn.")
            return

        async with connect() as (con, cur):
            # Geld vom Sender abziehen
            await cur.execute(f"SELECT money FROM `{DB_ECO_NAME}` WHERE user_id = %s", (sender.id,))
            result1 = await cur.fetchone()
            if result1 is None:
                await ctx.respond(f"User {sender.name} has no money record.")
                return

            old_money_sender = result1[0]
            if old_money_sender < amount:
                await ctx.respond("Du hast nicht genug Geld.")
                return

            new_money_sender = old_money_sender - amount
            await cur.execute(f"UPDATE `{DB_ECO_NAME}` SET money = %s WHERE user_id = %s", (new_money_sender, sender.id))
            await con.commit()

            # Geld dem Empfänger hinzufügen
            await cur.execute(f"SELECT money FROM `{DB_ECO_NAME}` WHERE user_id = %s", (user.id,))
            result2 = await cur.fetchone()
            if result2 is None:
                await ctx.respond(f"User {user.name} has no money record.")
                return

            old_money_receiver = result2[0]
            new_money_receiver = old_money_receiver + amount
            await cur.execute(f"UPDATE `{DB_ECO_NAME}` SET money = %s WHERE user_id = %s", (new_money_receiver, user.id))
            await con.commit()

            await ctx.respond(f"Der User {user.name} hat {amount} Coins von {sender.name} erhalten.")
    @slash_command(name="work", description="Gehe Arbeiten um Geld zu verdienen")
    async def work(self, ctx: discord.ApplicationContext):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        user = ctx.author
        async with connect() as (con, cur):

            await cur.execute(f"SELECT money FROM `{DB_ECO_NAME}` WHERE user_id = %s", user.id)
            result = await cur.fetchone()

            if result is None:
                await ctx.respond("User has no money record.")
                return
            smallest = 1
            largest = 1000
            old_money = result[0]
            amount = random.randint(smallest, largest - 1)
            new_money = old_money + amount
            await cur.execute(f"UPDATE `{DB_ECO_NAME}` SET money = %s WHERE user_id = %s", (new_money, user.id))
            await con.commit()
            await ctx.respond(f"Du warst Arbeiten und hast Geld Verdient du hattest Voher: {old_money} Coins. Du hast nun {new_money} Coins weil dein Chef dir {amount} Coins überwiesen hat.")

    @commands.slash_command(name="add_job", description="Weise einem Benutzer einen Job zu")
    async def add_job(self, ctx: discord.ApplicationContext, user: discord.Member, job: str):
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed,ephemeral=True)
            return
        if await BotVerwaltung.is_blacklist(ctx):
            await ctx.respond(embed=blacklist_error_embed)
            return
        if user.bot:
            await ctx.respond("Bots können keinen Job haben.")
            return

        async with connect() as (con, cur):
            # Debugging: print user id
            print(f"User ID: {user.id}")

            # Überprüfen, ob der Benutzer bereits in der Datenbank ist
            await cur.execute(f"SELECT job FROM {DB_ECO_NAME} WHERE user_id = %s", (user.id,))
            result = await cur.fetchone()

            if result is None:
                await cur.execute(f"INSERT INTO {DB_ECO_NAME} (user_id, money, job) VALUES (%s, %s, %s)", (user.id, 0, job))
                await con.commit()
                await ctx.respond(f"Dem Benutzer {user.display_name} wurde der Job {job} zugewiesen.")
                return

            current_job = result[0]

            if current_job is None:
                await cur.execute(f"UPDATE {DB_ECO_NAME} SET job = %s WHERE user_id = %s", (job, user.id))
                await con.commit()
                await ctx.respond(f"Dem Benutzer {user.display_name} wurde der Job {job} zugewiesen.")
            else:
                view = ConfirmJobView(job, user.id, cur, con)
                response = await ctx.respond(
                    f"Du hast bereits den Job {current_job}. Möchtest du zum Job {job} wechseln?", view=view,
                    ephemeral=True)
                view.message = await response.original_response()
                await view.wait()

    @slash_command(name="add_guild_item")
    @option("item", description="The name of the item to add")
    @option("price", description="The price of the item (use comma for decimal)")
    @option("set_role", description="Soll die Rolle gesetzt werden?", choices=["Ja", "Nein"], default="Nein",required=True)
    async def add_guild_item_two(self, ctx, item: str, price: str,set_role: str):
        Ja = "Ja"
        Nein = "Nein"
        if set_role == Ja:
            await ctx.respond("Später")
            return
        else:
            guild = ctx.guild
            try:
                price = float(price.replace(',', '.'))

                # Ensure the price is within the valid range for DECIMAL(10, 2)
                if price < 0 or price >= 1000000000:
                    await ctx.respond('Invalid price. Please enter a price between 0 and 1000000000')
                    return
            except ValueError:
                await ctx.respond('Invalid price format. Please use a number with a comma for decimal.')
                return

            try:
                async with connect() as (con, cur):
                    if ctx.author.id == guild.owner_id:
                        # Check if the item already exists for this guild
                        await cur.execute(f"SELECT item FROM {DB_ECO_GUILD_SHOP_USER} WHERE guild_id = %s AND item = %s",
                                          (guild.id, item))
                        result = await cur.fetchone()

                        if result is None:
                            query = f"INSERT INTO {DB_ECO_GUILD_SHOP_USER} (guild_id, item, price) VALUES (%s, %s, %s)"
                            await cur.execute(query, (guild.id, item, price))
                            await con.commit()
                            await ctx.respond(f'Item {item} wurde erfolgreich mit dem Preis {price} hinzugefügt.')
                        else:
                            await ctx.respond('Das Item gibt es schon.')
                    else:
                        await ctx.respond('You are not the owner of this guild.')
            except Exception as e:
                await ctx.respond(f'Ein Fehler ist aufgetreten: {e}')
                print(f'Error: {e}')
                return

# Setup Cog
def setup(bot):
    bot.add_cog(Economysystem(bot))
