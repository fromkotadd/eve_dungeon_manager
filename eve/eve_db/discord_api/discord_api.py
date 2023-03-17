import discord
from discord.ext import commands
from table2ascii import table2ascii, PresetStyle
from discord.ext.commands.context import Context

from eve_db.discord_api import config
from eve_db.representors.representors import pilot_info_table_queryset
from eve_db.representors.representors import registration_pilot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)  # инициализируем бота с префиксом '~'
ID_CHANNEL = config.config['ID_CHANNEL']


@bot.command()
async def ida(ctx):
	author = ctx.message.author
	print(type(ctx))
	await ctx.send(author.id)  # выводит в чат id автора сообщения
	await ctx.send(author.mention)  # выводит в чат имя автора сообщения


@bot.command()
async def pilot_add(ctx: Context,  name: str, corporation: str, tech_level: str, pilot_rating: str):
	try:
		discord_id = ctx.message.author.id
		reg = await registration_pilot(
				discord_id=discord_id,
				name=name,
				corporation=corporation,
				tech_level=tech_level,
				pilot_rating=pilot_rating
			)
		await ctx.send(reg)
	except Exception as EX:
		await ctx.send('Неверный формат ввода данных', EX)


@bot.command()
async def ship_add(ctx: Context,  name: str, corporation: str, tech_level: str, pilot_rating: str):
	try:
		discord_id = ctx.message.author.id
		reg = await registration_pilot(
				discord_id=discord_id,
				name=name,
				corporation=corporation,
				tech_level=tech_level,
				pilot_rating=pilot_rating
			)
		await ctx.send(reg)
	except Exception as EX:
		await ctx.send('Неверный формат ввода данных', EX)


@bot.command()
async def I(ctx, pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2):
	pilots_cards = await pilot_info_table_queryset(pilots_amount, implant_level, skills_rating, gun_rating)
	for pilots_card in pilots_cards:
		output = table2ascii(
			header=['ИМЯ', 'КОРПА', 'ТЕХ.УР.', 'РЕЙТИНГ', 'ПРОХОДКИ', 'СРЕДНИЙ.УР.СКИЛЛОВ'],
			body=[
				[
					pilots_card['name'],
					pilots_card['corporation'],
					pilots_card['tech_level'],
					pilots_card['pilot_rating'],
					pilots_card['dungeon_visits_amount'],
					pilots_card['skills_rating']
				]
			],
			style=PresetStyle.plain
		)
		await ctx.channel.send(f"```\n{output}\n```")


def run():
	bot.run(config.config['TOKEN'])
