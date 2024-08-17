import discord
from discord import app_commands
from discord.ext import commands

import asyncio
import json
import os
from time import perf_counter

from loggingModule import logs



configFile = 'config.json'
cogsFolder = 'cogs.'


if os.path.exists(configFile):
	with open(configFile, encoding='utf-8') as file:
		conf = json.load(file)

		# ! config example for config file with settings
		'''
		{
			"BotSettings": {
				"Token": "",
				"Prefix": "!"
			},
			"GuildID": 0,
			"DevelopersID": []
		}
		'''

else:
	logs.ERROR('Config File is Not Found')



class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.params = {
			'devops': conf['DevelopersID'],
			'guild_id': conf['GuildID'],
			'guild_object': discord.Object(id=conf['GuildID'])
		}


	async def setup_hook(self):
		# ? first setup all cogs
		for cog in os.listdir(cogsFolder):
			if cog.endswith('.py') and cog[:1] != '_':
				try:
					await self.load_extension(f'{cogsFolder}{cog[:-3]}')

				except Exception as e:
					logs.WARNING(cog[:-3], e)

		await self.tree.sync(guild=self.params['guild_object'])


	async def on_ready(self):
		# ? preparation of the channel for Cogs list
		self.cogs_channel = discord.utils.get(self.get_guild(self.params['guild_id']).channels, name='cogs')
		await self.cogs_channel.purge()
		self.message_cogs = await self.cogs_channel.send(embed=await self.cogs_embed)

		logs.INFO(f"{perf_counter()} seconds after launch", "bot is online")


	async def on_command_error(self, ctx, exception):
		if ctx.author.id in self.params['devops']:
			await ctx.author.send(exception)


	async def on_error(self, inter: discord.Interaction, error):
		if inter.user.id in self.params['devops']:
			await inter.response.send_message(error)



	@property
	async def cogs_embed(self):
		embed = discord.Embed(
			title=' Cogs:',
			color=discord.Colour.green()
		)

		[embed.add_field(name=_, value='*** +'+'-'*80+'<***', inline=False) for _ in [f' |> {_} is Enable' if _ in self.cogs else f' |> {_} is Disable' if _ not in self.cogs else f' | !!! {_} is not correct working' for _ in [_[:-3] for _ in os.listdir(cogsFolder) if _.endswith('.py') and _[:1] != '_']]]

		return embed



bot = DiscordBot(
	command_prefix=conf['BotSettings']['Prefix'],
	help_command=None,
	intents=discord.Intents.all()
)



@bot.tree.command(name='cogs', description='command for manage cogs', guild=bot.params['guild_object'])
@app_commands.describe(mode='choose mode for switch cogs (all or one)', target='enter the cog name for switch him (optional)')
@app_commands.choices(mode=[
	app_commands.Choice(name=n, value=i) for i, n in enumerate([
		'list',
		'target-switch',
		'target-reload',
		'all-switch',
		'all-reload'
	])
],
	target=[app_commands.Choice(name=n, value=i) for i, n in enumerate([i[:-3] for i in os.listdir(cogsFolder) if i.endswith('.py') and i[:1] != '_'])]
)
async def cogs_manager(inter: discord.Interaction, mode: app_commands.Choice[int], target: app_commands.Choice[int]=None):
	if inter.user.id not in bot.params['devops']:
		return

	cogs_folder = [_[:-3] for _ in os.listdir(cogsFolder) if _.endswith('.py') and _[:1] != '_']

	if mode.value == 1 or mode.value == 2:
		if target == None:
			await inter.response.send_message(
				'For surgery with cog, you need to specify the goal',
				ephemeral=True
			)
			return

		try:
			if target.name in bot.cogs and target.name in cogs_folder and mode.value == 1:
				await bot.unload_extension(f'{cogsFolder}{target.name}')

			elif target.name in bot.cogs and target.name in cogs_folder and mode.value == 2:
				await bot.reload_extension(f'{cogsFolder}{target.name}')

			elif target.name not in bot.cogs and target.name in cogs_folder:
				await bot.load_extension(f'{cogsFolder}{target.name}')

			else:
				# ! message Error
				logs.ERROR(f'It is impossible to conduct an operation with - {target.name}')

		except Exception as e:
			logs.WARNING(file[:-3], e)


	elif mode.value == 3 or mode.value == 4:
		if mode.value == 3:
			for file in os.listdir(cogsFolder): 
				if file.endswith('.py') and file[:1] not in ['_', '-']:
					try:
						if file[:-3].lower() in [i.lower() for i in bot.cogs]:
							await bot.unload_extension(f'{cogsFolder}{file[:-3]}')

						else:
							await bot.load_extension(f'{cogsFolder}{file[:-3]}')

					except Exception as e:
						logs.WARNING(file[:-3], e)

		elif mode.value == 4:
			for file in os.listdir(cogsFolder):
				if file.endswith('.py') and file[:1] not in ['_', '-']:
					try:
						if file[:-3].lower() in [i.lower() for i in bot.cogs]:
							await bot.reload_extension(f'{cogsFolder}{file[:-3]}')

						else:
							await bot.load_extension(f'{cogsFolder}{file[:-3]}')

					except Exception as e:
						logs.WARNING(file[:-3], e)

		else:
			await inter.response.send_message(
				'The operation cannot be done',
				ephemeral=True
			)
			return

	else:
		await inter.response.send_message(
			embed=await bot.cogs_embed,
			ephemeral=True
		)
		return

	await bot.message_cogs.edit(embed=await bot.cogs_embed)
	await inter.response.send_message(
		'Operation with cogs is done',
		ephemeral=True,
		delete_after=15
	)
	await bot.tree.sync(guild=bot.params['guild_object'])



async def main():
	if not conf['BotSettings']['Token']:
		logs.ERROR('Token Not Found')

	elif not conf['BotSettings']['Prefix']:
		logs.ERROR('Prefix Not Found')

	else:
		try:
			async with bot:
				await bot.start(conf['BotSettings']['Token'])

		except discord.errors.LoginFailure:
			logs.ERROR('Invalid Token')


if __name__ == '__main__':
	try:
		asyncio.run(main())

	except KeyboardInterrupt:
		logs.WARNING('key exit is pressed')