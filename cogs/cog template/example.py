import discord
import sys
from discord.ext import commands
sys.path.append("..")
from Modules import bot_lang


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'Loaded {__name__}!')


def setup(bot):
    bot.add_cog(Example(bot))
