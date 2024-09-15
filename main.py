import discord
import sys
import os
import asyncio
from _datetime import datetime
import platform
import logging

import config
from config import DISCORD_TOKEN ,VERSION , GUILD_ID
from pathlib import Path
import json
import requests

from discord.ext import commands, tasks

with open("config.json", mode="r") as config_file:
    config_json = json.load(config_file)
time1 = datetime.now()
time2 = time1.strftime("%d-%m-%Y-%H-%M-%S")
log = logging.getLogger('discord')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'), filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y-%S-%M-%S',
                    filename=f'./logs/log-{time2}.log')

webhook_url = "https://discord.com/api/webhooks/1195478342594478150/QUnYAl-FMGnR2MIPpT62aQvPZ313uVgo44tCxW78jNwfchfDqoFG6Kkma0Ly4bX7W_Cw"

logging.basicConfig(filename='saturnbot.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# Add the handlers to the Logger

req = requests.get(f'https://api.github.com/repos/Blue-Gamer48/herz_des_nordens/tags')
response = json.loads(req.text)
if req.status_code == 200:
    if response[0]['name'] == "1.0.0":
        print("You are currently running the latest version of Herz des Nordens!\n")
    else:
        version_listed = False
        for x in response:
            if x['name'] == VERSION:
                version_listed = True
                print("Der Bot ist auf der neuesten Version! :)\n")
        if not version_listed:
            print("Die Hier verwendete Version ist nicht Gelistet!\n")
elif req.status_code == 404:
    # 404 Not Found
    print("Es Konnte keine Lezte version Gefunden werden!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    print("Ein Fehler ist beim Suchen der version aufgetreten. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    print("Ein Fehler ist beim Suchen der version aufgetreten. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    print("Ein Fehler ist beim Suchen der Version aufgetreten. [503 Service Unavailable]\n")
else:
    print("Ein unbekannter Fehler ist beim Suchen der Version aufgetreten\n")
    print("HTML Error Code:" + str(req.status_code))


def run_check():
    version = sys.version_info
    if not int(version.major) >= 3 and int(version.minor) >= 10:
        if int(version.major) == 0:
            return
        raise SystemExit(
            f"Du brauchst eine aktuellere Python Version um das Skript auszuführen, mindestens 3.10 oder höher!"
        )
    return


prefix = "t."
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), debug_guilds=None)
# bot.remove_command("help")
check = 0
loop = asyncio.get_event_loop()


@bot.event
async def on_ready():
    print(f"""
        ----------------------------------------------------------------
        Planetbot Logs

        ----------------------------------------------------------------
        Der Bot mit dem Namen {bot.user.name} wurde erfolgreich gestartet!
        Discord.py Version: {discord.__version__}
        Python Version: {platform.python_version()}
        Operating System: {platform.system()} {platform.release()} ({os.name})
        ----------------------------------------------------------------
        """)
    log.info(f"""
    ----------------------------------------------------------------

    Saturnbot Logs

    ----------------------------------------------------------------
    Der Bot mit dem Namen "{bot.user.name}" wurde erfolgreich gestartet!
    Discord.py Version: {discord.__version__}
    Python Version: {platform.python_version()}
    Operating System: {platform.system()} {platform.release()} ({os.name})
    ----------------------------------------------------------------
    """)
    run_check()
    bot.loop.create_task(status_task())


########################################################################################################################
async def status_task():
    while True:
        game = discord.Game("ein Bot von Blue_Gamer48")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game("Version 0.0.1")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game("Bibiliotek Py-Cord")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game("Entwickelt von Blue_Gamer48")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)


cogs = [file.stem for file in Path('cogs').glob('**/*.py') if not file.name.startswith('__')]
for cog in cogs:
    bot.load_extension(f'cogs.{cog}')
    print(f'Loaded cog {cog}')
bot.run(DISCORD_TOKEN)