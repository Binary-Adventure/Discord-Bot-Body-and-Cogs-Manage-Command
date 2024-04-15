import discord
from discord import app_commands
from discord.ext import commands

import asyncio
import json
import os
from time import perf_counter
from logsfuncs import INFO, ERROR, WARNING



configFile = 'config.json'

if os.path.exists(configFile):
	with open(configFile, encoding='utf-8') as file:
		conf = json.load(file)

else:
	ERROR('Config File is Not Found')



class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.bot_info = {
			'devops': conf['DevelopersID'],
			'guild_id': conf['GuildID'],
			'guild_object': discord.Object(id=conf['GuildID'])
		}


	async def setup_hook(self):
		for cog in os.listdir('cogs/'):
			if cog.endswith('.py') and cog[:1] != '_':
				try:
					await self.load_extension(f'cogs.{cog[:-3]}')

				except Exception as e:
					WARNING(f'{cog[:-3]}', f'{e}')

		await self.tree.sync(guild=self.bot_info['guild_object'])


	async def on_ready(self):
		INFO(f"{perf_counter()} seconds after launch", "bot is online")

		self.cogs_channel = discord.utils.get(self.get_guild(self.bot_info['guild_id']).channels, name='cogs')
		await self.cogs_channel.purge()
		self.message_cogs = await self.cogs_channel.send(embed=await self.cogs_embed)


	async def edit_cogs_embed(self):
		await self.message_cogs.edit(embed=await self.cogs_embed)

	
	@property
	async def cogs_embed(self):
		embed = discord.Embed(
			title=' Cogs:',
			color=discord.Colour.dark_purple()
		)

		[embed.add_field(name=i, value='*** +'+'-'*80+'<***', inline=False) for i in [f' |> {i} is Enable' if i in self.cogs else f' |> {i} is Disable' if i not in self.cogs else f' | !!! {i} is not correct working' for i in [i[:-3] for i in os.listdir('cogs/') if i.endswith('.py') and i[:1] != '_']]]
		return embed


	async def on_command_error(self, ctx, exception):
		if ctx.author.id in self.bot_info['devops']:
			await ctx.author.send(exception)


bot = DiscordBot(
	command_prefix=conf['BotSettings']['Prefix'],
	help_command=None,
	intents=discord.Intents.all()
)


@bot.command()
async def test(ctx):
	await bot.edit_cogs_embed()



@bot.tree.command(name='cogs', description='...', guild=bot.bot_info['guild_object'])
@app_commands.describe(mode='...', target='...')
@app_commands.choices(mode=[
	app_commands.Choice(name='list', value='0'),
	app_commands.Choice(name='target-switch', value='1'),
	app_commands.Choice(name='target-reload', value='2'),
	app_commands.Choice(name='all-switch', value='3'),
	app_commands.Choice(name='all-reload', value='4')
])
async def cogs_control(inter: discord.Interaction, mode: app_commands.Choice[str], target: str=None):
	if inter.user.id not in bot.bot_info['devops']:
		return

	cogs_in_folder = [i[:-3] for i in os.listdir('cogs/') if i.endswith('.py') and i[:1] != '_']

	if mode.name == 'target-switch':
		if '.' in target:
			target[:target.find('.')]

		if target in bot.cogs and target in cogs_in_folder:
			await bot.unload_extension(f'cogs.{target}')

		elif target not in bot.cogs and target in cogs_in_folder:
			await bot.load_extension(f'cogs.{target}')

		else:
			pass


	elif mode.name == 'target-reload':
		if '.' in target:
			target[:target.find('.')]

		if target in bot.cogs and target in cogs_in_folder:
			await bot.reload_extension(f'cogs.{target}')

		elif target not in bot.cogs and target in cogs_in_folder:
			await bot.load_extension(f'cogs.{target}')

		else:
			# ! message Error
			pass


	elif mode.name == 'all-switch':
		pass
		# for file in os.listdir('cogs/'):
		# 	if file.endswith('.py') and file[:1] not in ['_', '-']:
		# 		try:
		# 			if file[:-3].lower() in [i.lower() for i in bot.cogs]:
		# 				await bot.unload_extension(f'cogs.{file[:-3]}')

		# 			else:
		# 				await bot.load_extension(f'cogs.{file[:-3]}')

		# 		except Exception as e:
		# 			WARNING(f'{file[:-3]}', f'{e}')


	elif mode.name == 'all-reload':
		pass
		# for file in os.listdir('cogs/'):
		# 	if file.endswith('.py') and file[:1] not in ['_', '-']:
		# 		try:
		# 			if file[:-3].lower() in [i.lower() for i in bot.cogs]:
		# 				await bot.reload_extension(f'cogs.{file[:-3]}')

		# 			else:
		# 				await bot.load_extension(f'cogs.{file[:-3]}')

		# 		except Exception as e:
		# 			WARNING(f'{file[:-3]}', f'{e}')


	else:
		await inter.response.send_message(
			embed=await bot.cogs_embed,
			ephemeral=True
		)



async def main():
	if not conf['BotSettings']['Token']:
		ERROR('Token Not Found')

	elif not conf['BotSettings']['Prefix']:
		ERROR('Prefix Not Found')

	else:
		try:
			async with bot:
				await bot.start(conf['BotSettings']['Token'])

		except discord.errors.LoginFailure:
			ERROR(' Invalid Token')


if __name__ == '__main__':
	try:
		asyncio.run(main())

	except KeyboardInterrupt:
		WARNING('key exit is pressed')