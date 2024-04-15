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

		await self.tree.sync(guild=self.guild_object)


	async def on_ready(self):
		INFO(f"{perf_counter()} seconds after launch", "bot is online")


	async def on_command_error(self, ctx, exception):
		if ctx.author.id in self.devops:
			await ctx.reply(
				exception,
				ephemeral=True
			)


bot = DiscordBot(
	command_prefix=conf['BotSettings']['Prefix'],
	help_command=None,
	intents=discord.Intents.all()
)



@bot.tree.command(name='cogs', description='...')
@app_commands.describe(mode='...', target='...')
@app_commands.choices(mode=[
	app_commands.Choice(name='list', value=0),
	app_commands.Choice(name='target-switch', value=1),
	app_commands.Choice(name='target-reload', value=2)
	app_commands.Choice(name='all-switch', value=3)
	app_commands.Choice(name='all-reload', value=4)
])
async def cogs_control(inter: discord.Interaction, mode: app_commands.Choice[str], target: str):
	if inter.user.id not in bot.devops:
		return

	cogs_in_folder = [i[:-3] for i in os.listdir('cogs/') if i.endswith('.py') and i[:1] != '_']

	if mode.name == 'target-switch':
		# ? exam on presence of expan and removing
		if '.' in target:
			target[:target.find('.')]

	elif mode.name == 'target-reload':
		if '.' in target:
			target[:target.find('.')]

	elif mode.name == 'all-switch':
		for file in os.listdir('cogs/'):
			if file.endswith('.py') and file[:1] not in ['_', '-']:
				try:
					if file[:-3].lower() in [i.lower() for i in bot.cogs]:
						await bot.unload_extension(f'cogs.{file[:-3]}')

					else:
						await bot.load_extension(f'cogs.{file[:-3]}')

				except Exception as e:
					print(f'\n\nИСКЛЮЧЕНИЕ: {file[:-3]}\n\n{e}')

	elif mode.name == 'all-reload':
		for file in os.listdir('cogs/'):
			if file.endswith('.py') and file[:1] not in ['_', '-']:
				try:
					if file[:-3].lower() in [i.lower() for i in bot.cogs]:
						await bot.reload_extension(f'cogs.{file[:-3]}')

					else:
						await bot.load_extension(f'cogs.{file[:-3]}')

				except Exception as e:
					print(f'\n\nИСКЛЮЧЕНИЕ: {file[:-3]}\n\n{e}')

	else:
		# ? generation of embed with cogs statuses
		embed = discord.Embed(
			title=' Cogs:',
			color=discord.Color.orange()
		)

		[embed.add_field(name=i, value='*** +'+'-'*50+'<***') for i in [f' |> {i} is Enable' if i in bot.cogs else f' |> {i} is Disable' if i not in bot.cogs else f' | !!! {i} is not correct working' for i in cogs_in_folder]]

		await inter.response.send_message(
			embed=embed,
			ephemeral=True
		)


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