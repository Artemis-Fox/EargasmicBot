import discord
import asyncio
from discord.ext import commands
from discord import app_commands



class Leave(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None


    @app_commands.command()
    async def leave(self, interaction: discord.Interaction):

        # if the bot is in a channel, make it leave
        if interaction.guild.voice_client !=None:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("TTFN!")
        else:
            await interaction.response.send_message("I can't leave a place im not in!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Leave(bot))
