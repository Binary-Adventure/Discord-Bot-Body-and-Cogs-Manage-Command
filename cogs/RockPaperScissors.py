import discord
from discord.ext import commands

from random import choice
from asyncio import sleep



class RockPaperScissors(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command()
	async def rps(self, ctx, max_score: int=None):
		game = []
		if max_score == None or max_score <= 1:
			while True:
				sign = choice(['камень', 'ножницы', 'бумага'])
				contr_sign = 'камень' if sign == 'ножницы' else 'ножницы' if sign == 'бумага' else 'бумага'

				result_sign = await ctx.send(
					'Я выбираю...',
					ephemeral=True
				)

				game.append(result_sign)

				msg = await self.bot.wait_for(
					'message',
					check=lambda message: message.author == ctx.author and message.channel == ctx.channel
				)
				game.append(msg)

				await result_sign.edit(content=f'Я выбираю {sign.upper()}!')

				if msg.content.lower() == contr_sign:
					await ctx.send(
						'Чёрт! Ты выиграл',
						ephemeral=True,
						delete_after=10
					)
					await sleep(.5)
					await ctx.send(
						embed=discord.Embed(
							title='Давай ещё раз?',
							description='[ да / нет ]'
						),
						ephemeral=True,
						delete_after=30
					)

				elif msg.content.lower() == sign:
					await ctx.send(
						'хех, ничья',
						ephemeral=True,
						delete_after=10
					)
					await sleep(.5)
					await ctx.send(
						embed=discord.Embed(
							title='Ещё раз?',
							description='[ да / нет ]'
						),
						ephemeral=True,
						delete_after=30
					)

				else:
					await ctx.send(
						choice([
							'ахахаххааа, ты проиграл',
							'Твоих денег больше НЕТ'
						]),
						ephemeral=True,
						delete_after=10
					)
					await sleep(.5)
					await ctx.send(
						embed=discord.Embed(
							title='Реванш?',
							description='[ да / нет ]'
						),
						ephemeral=True,
						delete_after=30
					)

				msg = await self.bot.wait_for(
					'message',
					check=lambda message: message.author == ctx.author and message.channel == ctx.channel
				)
				game.append(msg)

				if 'да' in msg.content.lower():
					await ctx.send(
						choice([
							'Хорошо, продолжаем',
							'Отлично, продолжим',
							'Замечательно, ещё разок',
							'Ну ещё разочек можно'
						]),
						ephemeral=True,
						delete_after=15
					)

				else:
					await ctx.send(
						'ладно',
						ephemeral=True,
						delete_after=10
					)
					[await msg.delete() for msg in game]
					await ctx.message.delete()
					break

		elif max_score > 0:
			score_user, score_bot = 0, 0

			while True:
				sign = choice(['камень', 'ножницы', 'бумага'])
				contr_sign = 'камень' if sign == 'ножницы' else 'ножницы' if sign == 'бумага' else 'бумага'

				result_sign = await ctx.send(
					'Я выбираю...',
					ephemeral=True
				)

				game.append(result_sign)

				msg = await self.bot.wait_for(
					'message',
					check=lambda message: message.author == ctx.author and message.channel == ctx.channel
				)
				game.append(msg)

				await result_sign.edit(content=f'Я выбираю {sign.upper()}!')

				if msg.content.lower() == contr_sign:
					await ctx.send(
						'Чёрт! Ты выиграл',
						ephemeral=True,
						delete_after=10
					)
					score_user += 1
					await sleep(.5)
					await ctx.send(
						embed=discord.Embed(
							title='Счёт:',
							description=f'Мои победы: **{score_bot}**\nТвои победы: **{score_user}**'
						),
						ephemeral=True,
						delete_after=30
					)

				elif msg.content.lower() == sign:
					await ctx.send(
						'хех, ничья',
						ephemeral=True,
						delete_after=10
					)
					await sleep(.5)
					await ctx.send(
						embed=discord.Embed(
							title='Счёт:',
							description=f'Мои победы: **{score_bot}**\nТвои победы: **{score_user}**'
						),
						ephemeral=True,
						delete_after=30
					)
				
				elif 'стоп' in msg.content.lower():
					await ctx.send(
						embed=discord.Embed(
							title='Ты уверен? Если ты остановишь игру, твоя ставка сгорит...',
							description='[ да / нет ]'
						),
						ephemeral=True,
						delete_after=30
					)
					msg = await self.bot.wait_for(
						'message',
						check=lambda message: message.author == ctx.author and message.channel == ctx.channel
					)
					game.append(msg)

					if 'да' in msg.content.lower():
						await ctx.send(
							'хорошо',
							ephemeral=True,
							delete_after=10
						)
						[await msg.delete() for msg in game]
						await ctx.message.delete()
						break

					else:
						await ctx.send(
							'значит продолжаем',
							ephemeral=True,
							delete_after=10
						)

				else:
					await sleep(.5)
					score_bot += 1
					await ctx.send(
						choice([
							'ахахаххааа, ты проиграл',
							'Твоих денег больше НЕТ'
						]),
						ephemeral=True,
						delete_after=10
					)
					await ctx.send(
						embed=discord.Embed(
							title='Счёт:',
							description=f'Мои победы: **{score_bot}**\nТвои победы: **{score_user}**'
						),
						ephemeral=True,
						delete_after=30
					)

				if score_user == max_score or score_bot == max_score:
					if score_user == max_score:
						await ctx.send(
							'Ещё раз?\n[ да / нет ]',
							ephemeral=True,
							delete_after=30
						)

					elif score_bot == max_score:
						await ctx.send(
							'Реванш?\n[ да / нет ]',
							ephemeral=True,
							delete_after=30
						)

					msg = await self.bot.wait_for(
						'message',
						check=lambda message: message.author == ctx.author and message.channel == ctx.channel
					)
					game.append(msg)

					if 'да' in msg.content.lower():
						await ctx.send(
							choice([
								'Хорошо, продолжаем',
								'Отлично, продолжим',
								'Замечательно, ещё разок',
								'Ну ещё разочек можно'
							]),
							ephemeral=True,
							delete_after=10
						)
						score_user, score_bot = 0, 0

					else:
						await ctx.send(
							'ладно',
							ephemeral=True,
							delete_after=10
						)
						[await msg.delete() for msg in game]
						await ctx.message.delete()
						break



async def setup(bot):
	await bot.add_cog(RockPaperScissors(bot), guild=bot.params['guild_object'])