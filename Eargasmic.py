import discord, os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = discord.Object(id=620016163229007885)


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        self.coglist = ["cogs.Play", "cogs.Leave"]
        intents.voice_states = True
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)

    async def setup_hook(self):
        for ext in self.coglist:
            await self.load_extension(ext)
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)



bot = MyBot()

@bot.event
async def on_ready():
    print(f'Hey Suger cube! {bot.user} is Logged in!')
    print('------')



bot.run(TOKEN)
