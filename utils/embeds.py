import discord
import psutil
import platform
import psutil
import speedtest
import  os
import aiohttp
#s = speedtest.Speedtest()
#s = s.results.dict()
botinfo_embed = discord.Embed(title=f"Botinfo von Planetbot")
botinfo_embed.add_field(name="Name:", value=f"```Planetbot```",inline=False)
botinfo_embed.add_field(name="Botinhaber",value="```Blue_Gamer48```")
botinfo_embed.add_field(name="Bot Version",value="```2.0.0-Dev```",inline=False)
botinfo_embed.add_field(name="Programmiersprache",value=f"```Python```",inline=False)
botinfo_embed.add_field(name="RAM:",value=f"```{psutil.virtual_memory()[2]}```")
botinfo_embed.add_field(name="Prozessorkerne:",value=f"```{psutil.cpu_count()}```",inline=False)
botinfo_embed.add_field(name="Programmiersprachen Version",value=f"```{platform.python_version()}```",inline=False)
botinfo_embed.add_field(name="Bibiliotek und Version",value=f"```{discord.__title__} {discord.__version__}```",inline=False)
botinfo_embed.add_field(name="Betriebsysystem und Version",value=f"```{platform.system()} {platform.release()} ({os.name}```",inline=False)
#botinfo_embed.add_field(name="Bot:",value=f"```{s['client']['isp']}() {s['client']['country']} {s['client']['isprating']}```")
botinfo_embed.set_footer(text=f"Ein Bot von Blue_Gamer48 ©️2024 Planetbot")

help_embed_default = discord.Embed(title="Hilfe für Planetbot", description="Wilkommen im Hilfemenü  von Planetbot")
help_embed_default.set_thumbnail(url="https://cdn.discordapp.com/attachments/1057042955711557743/1212507577972293673/Planetbot_Logo.jpg?ex=65f216ad&is=65dfa1ad&hm=bf34e1a25c7a8294664caecb68483b868737e7a6827fb1e925c28cab3d56e5b2&")
help_embed_default.set_footer(text=f"Ein Bot von Blue_Gamer48 ©️2024 Planetbot")

help_allgemein_embed = discord.Embed(title="Allgemein",description="Alle Spaß Befehle von Planetbot",color=0x5fffd4)
help_allgemein_embed.add_field(name="/gutenmorgen",value="Wünsche allen Usern einen Guten Morgen",inline=False)
help_allgemein_embed.add_field(name="/gutenacht",value="Wünsche allen Usern eine Gute Nacht",inline=False)
help_allgemein_embed.add_field(name="/hallo",value="Begrüße die User",inline=False)
help_allgemein_embed.set_thumbnail(url="https://logos.flamingtext.com/Word-Logos/allgemein-design-beauty-name.png")
help_allgemein_embed.set_footer(text=f"Ein Bot von Blue_Gamer48 ©️2024 Planetbot")

help_info_embed = discord.Embed(title="Informations Befehle",description="Alle Info Befehle von Planetbot",color=0x195080)
help_info_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Info_Simple.svg/768px-Info_Simple.svg.png")
help_info_embed.add_field(name="/userinfo",value="gibt infos zum User",inline=False)
help_info_embed.add_field(name="/serverinfo",value="gibt Infos zum Server",inline=False)
help_info_embed.add_field(name="/botinfo",value="gibt Infos zum Bot",inline=False)
help_info_embed.add_field(name="/entwickler",value="git aus wer den Bot Entwickelt",inline=False)
help_info_embed.add_field(name="/botlinks",value="bit die wichtigsten Links zum Bot",inline=False)
help_info_embed.add_field(name="/entwickler",value="gibt an wer am Bot Arbeitetet",inline=False)
help_info_embed.add_field(name="/avatar",value="Schickt das Avatar Bild vom ausgewählten User oder vom ausführendem User",inline=False)
help_info_embed.add_field(name="/servericon",value="Schickt das Icon vom Server",inline=False)
help_info_embed.add_field(name="/speedtest",value="Damit kannst du prüfen wie Schnell der Bot Reagiert",inline=False)
help_info_embed.add_field(name="/roles",value="Zeigt dir an was es für Rolllen auf dem Server gibt",inline=False)
help_info_embed.set_footer(text=f"Ein Bot von Blue_Gamer48 ©️2024 Planetbot")

help_fun_embed = discord.Embed(title="Spaß Befehle",description="Alle Spaß Befehle von Planetbot",color=0x5fffd4)
help_fun_embed.add_field(name="/countdown",value="Zählt einen Countdown von 10 runter",inline=False)
help_fun_embed.add_field(name="/coinflip",value="Wirft eine Münze",inline=False)
help_fun_embed.add_field(name="/roll",value="wirft einen Würfel",inline=False)
help_fun_embed.add_field(name="/hype",value="Zeige mit einem Bild das du gehypet bist",inline=False)
help_fun_embed.add_field(name="/coinflip",value="wirft ne Münze",inline=False)
help_fun_embed.add_field(name="/say",value="lässt den Bot etwas Sagen",inline=False)
help_fun_embed.add_field(name="/everyone",value="Gibt ein Bild aus wenn dich ein Everyone Ping Stört",inline=False)
help_fun_embed.add_field(name="/i_love_trains",value="Zeigt das du Züge magst (ASFD Movie)",inline=False)
help_fun_embed.add_field(name="/iq",value="Zeigt an wie Schlau oder doof ein User oder du bist",inline=False)
help_fun_embed.add_field(name="/hack",value="Hacke einen User",inline=False)
help_fun_embed.add_field(name="/eightball",value="Befrage den Magischen 8Ball",inline=False)
help_fun_embed.add_field(name="/bob",value="Lasse Bob im Chat erscheinen",inline=False)
help_fun_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Twemoji_1f61c.svg/512px-Twemoji_1f61c.svg.png")
help_fun_embed.set_footer(text=f"Ein Bot von Blue_Gamer48 ©️2024 Planetbot")


blacklist_error_embed =discord.Embed(title="Du Kannst dies nicht nutzen ⛔",
                                    description="Hallo du bist auf der Bot Blacklist weil du gegen die [Nutzungsbedingungen](https://blue-hamer48.de/planetbot/nutzungsbedingung) Verstoßen hast, schaue bitte per blacklist-info wie lange deine Sperre gültig ist und melde dich wenn du die Sperre für Ungerechtfertigt hälst.")