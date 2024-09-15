from discord import Forbidden
import asyncio
import random
from discord import Forbidden
from discord import slash_command ,InteractionContextType, IntegrationType
from discord.ext import commands

from utils.embeds import *

cache_counter = 0
async def cat_pic():
    random_param = random.randint(1, 1000000)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://cataas.com/cat?cache={random_param}') as response:
            if response.status == 200:
                image_url = str(response.url)
                return image_url
            else:
                return None
class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user = None
    @slash_command(name="countdown",
                   description="Lass den bot von 10 Runterzählen",
                   integration_types={IntegrationType.guild_install,IntegrationType.user_install},
                   contexts={InteractionContextType.guild,InteractionContextType.bot_dm,InteractionContextType.private_channel})
    async def countdown(self, ctx):
        msg = await ctx.respond(f"Der Countdown Läuft")
        await asyncio.sleep(2)
        await msg.edit(content='**:keycap_ten:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:nine:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:eight:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:seven:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:six:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:five:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:four:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:three:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:two:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:one:**')
        await asyncio.sleep(1)
        await msg.edit(content='**:ok:** DING DING DING')

    @slash_command(name="cat",description="sendet ein zufälliges Katzen Bild",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def cat(self, ctx):
        cat_picture = await cat_pic()
        if cat_picture:
            embed = discord.Embed(title="Random Cat", color=discord.Color.blue())
            embed.set_image(url=cat_picture)
            await ctx.respond(embed=embed)
        else:
            ctx.respond("Konnte mir leider kein Bild Holen")

    @slash_command(name="hype",description="Schickt einen Hype Train los",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.private_channel})
    async def hype(self, ctx):
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.respond(msg)
    @slash_command(name="roll",description="wirf einen Würfel",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def roll(self,ctx):
        dice=[1,2,3,4,5,6]
        randice=random.choice(dice)
        self.embed = discord.Embed(title=f'🎲 Würfelwurf',description=(f"du hast eine {randice} gewürfelt"), color=0xf8f8f9)
        self.embed.set_footer(text=f"der Command wurde von {ctx.author.name} {ctx.author.id} ausgeführt")
        await ctx.respond(embed=self.embed)
    @slash_command(name="coinfip",description="Wirf eine Münze",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def coinflip(self, ctx):
        coin = ["Kopf", "Zahl", "Die Münze ist Runtergefallen, bitte Versuche es Nochmal"]
        rancoin = random.choice(coin)
        embed = discord.Embed(title=f"Münzwurf     :coin:",
                              description=rancoin,
                              color=0x00ff00)
        embed.set_footer(text="ein Bot von Blue_Gamer48")
        await ctx.respond(embed=embed)
    @slash_command(name="iq",description="lass dir den IQ eines Users anzeigen",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild,InteractionContextType.private_channel})
    async def iq(self,ctx,member: discord.Member):
        if member == None:
            member = ctx.author
        smallest = 0
        largest = 100
        youriq = random.randint(smallest, largest - 1)
        await ctx.respond(f"Der IQ von {member} ist: {youriq}.")

    @slash_command(name="say",description="Lasse de bot etwas sagen",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def say(self,ctx, message):
        self.embed = discord.Embed(title='', description=(message),color=0xf8f8f9)
        self.embed.set_footer(text=f"Geschrieben von: {ctx.author.name} {ctx.author.id}")
        await ctx.respond(embed=self.embed )
    @slash_command(name="everyone",description="Gebe eine naricht gegen Everyone Pings aus",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.private_channel})
    async def everyone(self, ctx):
        member = ctx.author
        file = discord.File("./images/everyone/" + random.choice(os.listdir("./images/everyone/")))
        self.embed = discord.Embed(title='😡 everyone', description=("Hör auf everyone zu Spammen das kann nicht so wichtig sein!!!"), color=0xf8f8f9)
        self.embed.set_footer(text=f"der Command wurde von {ctx.author.name} {ctx.author.id} ausgeführt")
        self.embed.set_image(url="attachment://./images/everyone/" + random.choice(os.listdir("./images/everyone/")))
        await ctx.respond(embed=self.embed)
    @slash_command(name="i_love_trains",description="Ich mag Züge",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def i_love_trains(self,ctx):
        embed = discord.Embed(title='        Ich mag Züge        ', description=(""), color=0xf8f8f9)
        await ctx.respond(embed=embed)
        await ctx.respond("https://thumbs.gfycat.com/AjarPersonalImpala-mobile.mp4")

    @slash_command(name="hack",description="Hacke einen User",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild,InteractionContextType.private_channel})
    async def hack(self, ctx, user: discord.Member):
        """Hack someone's account! Try it!"""
        msg = await ctx.respond(f"Hacking! Target: {user}")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓    ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓   ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓▓▓ ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files COMPLETE! [▓▓▓▓▓▓]")
        await asyncio.sleep(2)
        await msg.edit(content="Retrieving Login Info... [▓▓▓    ]")
        await asyncio.sleep(3)
        await msg.edit(content="Retrieving Login Info... [▓▓▓▓▓ ]")
        await asyncio.sleep(3)
        await msg.edit(content="Retrieving Login Info... [▓▓▓▓▓▓ ]")
        await asyncio.sleep(4)
        await msg.edit(content=f"An error has occurred hacking {user}'s account. Please try again later. ❌")

    @slash_command(name="eightball",description="Der magische Eightball beantwortet Fragen für dich.",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def eightball(self, ctx, *, message:str):
        """Really desperate? Ask the 8ball for advice. Only yes/no questions!"""
        try:
            choices = [' Ja :white_check_mark:',"Nein :x:","Vieleicht :question:"]
            color = discord.Color(value=0x00ff00)
            em = discord.Embed(color=color, title=f"{message}")
            em.description = random.choice(choices)
            em.set_author(name="Der Magische 8 Ball", icon_url="https://vignette.wikia.nocookie.net/battlefordreamislandfanfiction/images/5/53/8-ball_my_friend.png/revision/latest?cb=20161109021012")
            em.set_footer(text=f"der Command wurde von {ctx.author.name} {ctx.author.id} ausgeführt")
            await ctx.respond(embed=em)
        except Forbidden:
            color = discord.Color(value=0xf44242)
            em = discord.Embed(color=color, title='Error ')
            em.description = 'Error code **{e.code}**: {e.error}'
            return await ctx.respond(embed=em)

    @slash_command(name="bob",description="Das ist Bob",
                   integration_types={IntegrationType.guild_install, IntegrationType.user_install},
                   contexts={InteractionContextType.guild, InteractionContextType.bot_dm,
                             InteractionContextType.private_channel})
    async def bob(self,ctx):
        await ctx.respond("░░░░░▐▀█▀▌░░░░▀█▄░░░\n"
                       "░░░░░▐█▄█▌░░░░░░▀█▄░░\n"
                       "░░░░░░▀▄▀░░░▄▄▄▄▄▀▀░░\n"
                       "░░░░▄▄▄██▀▀▀▀░░░░░░░\n"
                       "░░░█▀▄▄▄█░▀▀░░ \n"
                       "░░░▌░▄▄▄▐▌▀▀▀░░ This is Bob\n"
                       "▄░▐░░░▄▄░█░▀▀ ░░ Copy And Paste Him In \n"
                       "▀█▌░░░▄░▀█▀░▀ ░░ Every Discord Server, \n"
                       "░░░░░░░▄▄▐▌▄▄░░░ So, He Can Take \n"
                       "░░░░░░░▀███▀█░▄░░ Over Discord\n"
                       "░░░░░░▐▌▀▄▀▄▀▐▄░░  (dont spam him tho) \n"
                       "░░░░░░▐▀░░░░░░▐▌░░\n"
                       "░░░░░░█░░░░░░░░█░░░░░░░\n"
                       "░░░░░░█░░░░░░░░█░░░░░░░\n"
                       "░░░░░░█░░░░░░░░█░░░░░░░\n"
                       "░░░░▄██▄░░░░░▄██▄░░░░░░\n")


def setup(bot):
    bot.add_cog(fun(bot))