import discord
from discord.ext import commands



class CogSample(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot



async def setup(bot):
	await bot.add_cog(CogSample(bot), guild=bot.bot_info['guild_object'])