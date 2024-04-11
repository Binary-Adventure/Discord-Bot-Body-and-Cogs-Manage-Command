import discord
from discord import app_commands
from discord.ext import commands

import asyncio
import json
import os
import logsfuncs
from time import perf_counter



configFile = 'config.json'

if os.path.exists(configFile):
	with open(configFile, encoding='utf-8') as file:
		conf = json.load(file)

else:
	raise NameError('Config File is Not Found')



class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.devops = conf['DevelopersID']
		self.guild_object = discord.Object(id=conf['GuildID'])


	async def setup_hook(self):
		for cog in os.listdir('cogs/'):
			if cog.endswith('.py') and cog[:1] != '_':
				try:
					await self.load_extension(f'cogs.{cog[:-3]}')

				except Exception as e:
					print(f'\n\nEXCEPTION: {cog[:-3]}\n\n{e}')

		# await self.tree.sync(guild=self.guild_object)


	async def on_ready(self):
		INFO(f"{perf_counter()} seconds after launch", "bot is online")
		#print(f'\n [ bot is online ] {perf_counter()} seconds after launch')


	async def on_command_error(self, ctx, exception):
		if ctx.author.id in self.devops:
			await ctx.reply(
				exception,
				ephemeral=True
			)


# class HelpCommand(commands.MinimalHelpCommand):



bot = DiscordBot(
	command_prefix=conf['BotSettings']['Prefix'],
	help_command=None,
	intents=discord.Intents.all()
)



@bot.command()
async def cogs(ctx, mode=None, target=None):
	try:
		if ctx.author.id not in bot.devops:
			return

		cogs_in_folder = [i[:-3] for i in os.listdir('cogs/') if i.endswith('.py') and i[:1] != '_']

		if mode:
			if target:
				# ? exam on presence of expan and removing
				if '.' in target:
					target[:target.find('.')]

				if mode in 'switch':
					if target in bot.cogs:
						bot.unload_extension(target)

					else:
						bot.load_extension(f'cogs.{target}')

				elif mode in 'reload':
					if target in bot.cogs:
						bot.reload_extension(target)

			# else:
			# 	if mode in 'switch':
			# 		pass

			# 	elif mode in 'reload':
			# 		pass
 
		else:
			# ? generation of embed with cogs statuses
			embed = discord.Embed(
				title=' Cogs:',
				color=discord.Color.orange()
			)

			[embed.add_field(name=i, value='*** +'+'-'*50+'<***') for i in [f' |> {i} is Enable' if i in bot.cogs else f' |> {i} is Disable' if i not in bot.cogs else f' | !!! {i} is not correct working' for i in cogs_in_folder]]

			await ctx.reply(

				embed=embed,
				ephemeral=True
			)

	except Exception as e:
		pass



async def main():
	if not conf['BotSettings']['Token']:
		raise NameError('Token Not Found')

	elif not conf['BotSettings']['Prefix']:
		raise NameError('Prefix Not Found')

	else:
		try:
			async with bot:
				await bot.start(conf['BotSettings']['Token'])

		except discord.errors.LoginFailure:
			raise NameError('\n Invalid Token\n')


if __name__ == '__main__':
	try:
		asyncio.run(main())

	except KeyboardInterrupt:
		print('\n key exit is pressed')