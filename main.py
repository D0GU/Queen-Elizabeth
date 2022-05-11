# D0GU#5777

import discord
from discord.ext import commands
from utility import Utility
from utility import *


if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=config["prefix"],intents=intents)
    bot.add_cog(Utility(bot))
    bot.run(config["token"])
    