from discord.ext import commands
from discord import ui
import discord

from discord.ext.pages import Paginator, Page
from utils.embeds import *
class Help_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(  # the decorator that lets you specify the properties of the select menu
        placeholder="Wähle wofür du Hilfe Brauchst",  # the placeholder text that will be displayed if nothing is selected
        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=1,  # the maximum number of values that can be selected by the users
        options=[  # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Startseite",
                description="Hauptseite des Menüs"
            ),
            discord.SelectOption(
                label="Allgemein",
                description="Allgemeine Befehle"
            ),
            discord.SelectOption(
                label="Spaß",
                description="Spaßbefehle"
            ),
            discord.SelectOption(
                label="Info",
                description="Informations Befehle"

            )
        ]
    )
    async def select_callback(self, select, interaction):  # the function called when the user is done selecting options
        if select.values[0] == "Startseite":
            await interaction.edit(embed=help_embed_default)
        elif select.values[0] == "Allgemein":
            await interaction.edit(embed=help_allgemein_embed)
        elif select.values[0] == "Info":
            await interaction.edit(embed=help_info_embed)
        elif select.values[0] == "Spaß":
            await interaction.edit(embed=help_fun_embed)


