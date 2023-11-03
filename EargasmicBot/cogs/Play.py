import discord
import yt_dlp
import asyncio
from discord.ext import commands
from discord import app_commands

# supress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @app_commands.command()
    @app_commands.describe(url='The Youtube Video Link')
    async def play(self, interaction: discord.Interaction, *, url: str):

        # Get the voice channel the user is in
        try:
            UserChannel = interaction.user.voice.channel
        except:
        # if user is not in voice channel, tells user to get into voice channel
            await interaction.response.send_message('You gotta be in a VC to call me!')
        # Check if user is in a voice channel and connects to VC
        if interaction.guild.voice_client == None:
            voice = await UserChannel.connect()
        # Stream the song
        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if interaction.guild.voice_client.is_playing():
                interaction.guild.voice_client.stop()
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error {e}') if e else None)
        await interaction.response.send_message(f'Now playing [*{player.title}*]!')

        



async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
