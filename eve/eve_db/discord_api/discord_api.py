import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from table2ascii import table2ascii, PresetStyle

from eve_db.discord_api import config
from eve_db.representors.representors import first, pilot_card_add, pilot_ship_add, \
	pilot_implant_add, pilot_skill_add, dungeon_visit_add, pilot_card_upd, pilot_ship_upd, \
	pilot_implant_upd, pilot_skill_upd, second
from eve_db.selectors.pilotship import ships_for_first_dungeon, ships_for_second_dungeon

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)  # инициализируем бота с префиксом '~'
ID_CHANNEL = config.config['ID_CHANNEL']


@bot.command()
async def ida(ctx: Context):
	author = ctx.message.author
	await ctx.send(author.id)  # выводит в чат id автора сообщения
	await ctx.send(author.mention)  # выводит в чат имя автора сообщения


@bot.command()
async def pilot_add(ctx: Context, name: str, corporation: str, tech_level: str, pilot_rating: str):
	try:
		discord_id = str(ctx.message.author.id)
		reg = await pilot_card_add(
			discord_id=discord_id,
			name=name.lower(),
			corporation=corporation,
			tech_level=tech_level,
			pilot_rating=pilot_rating.lower()
		)
		await ctx.send(reg)
	except Exception as EX:
		await ctx.send(f'Неверный формат ввода данных: {EX}')


@bot.command()
async def pilot_upd(ctx: Context, name: str, corporation: str, tech_level: str, pilot_rating: str):
	try:
		discord_id = str(ctx.message.author.id)
		upd = await pilot_card_upd(
			discord_id=discord_id,
			name=name.lower(),
			corporation=corporation,
			tech_level=tech_level,
			pilot_rating=pilot_rating.lower()
		)
		await ctx.send(upd)
	except Exception as EX:
		await ctx.send(f'Неверный формат ввода данных: {EX}')


@bot.command()
async def ship_add(ctx: Context, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	try:
		discord_id = str(ctx.message.author.id)
		add = await pilot_ship_add(
			discord_id=discord_id,
			ship_name=ship_name.lower(),
			core_color=core_color.lower(),
			core_lvl=core_lvl,
			fit_grade=fit_grade.title()
		)
		await ctx.send(add)
	except Exception as ex:
		await ctx.send(f'Неверный формат ввода данных: {ex}')


@bot.command()
async def ship_upd(ctx: Context, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	try:
		discord_id = str(ctx.message.author.id)
		upd = await pilot_ship_upd(
			discord_id=discord_id,
			ship_name=ship_name.lower(),
			core_color=core_color.lower(),
			core_lvl=core_lvl,
			fit_grade=fit_grade.title()
		)
		await ctx.send(upd)
	except Exception as EX:
		await ctx.send(f'Неверный формат ввода данных: {EX}')


@bot.command()
async def implant_add(ctx: Context, implant_name: str, implant_level: str):
	try:
		discord_id = str(ctx.message.author.id)
		add = await pilot_implant_add(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await ctx.send(add)
	except Exception as ex:
		await ctx.send(f'Неверный формат ввода данных: {ex}')


@bot.command()
async def implant_upd(ctx: Context, implant_name: str, implant_level: str):
	try:
		discord_id = str(ctx.message.author.id)
		upd = await pilot_implant_upd(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await ctx.send(upd)
	except Exception as EX:
		await ctx.send(f'Неверный формат ввода данных: {EX}')


@bot.command()
async def skill_add(ctx: Context, name: str, level: str):
	try:
		discord_id = str(ctx.message.author.id)
		add = await pilot_skill_add(
			discord_id=discord_id,
			name=name.lower(),
			level=level
		)
		await ctx.send(add)
	except Exception as ex:
		await ctx.send(f'Неверный формат ввода данных: {ex}')


@bot.command()
async def skill_upd(ctx: Context, name: str, level: str):
	try:
		discord_id = str(ctx.message.author.id)
		upd = await pilot_skill_upd(
			discord_id=discord_id,
			name=name.lower(),
			level=level
		)
		await ctx.send(upd)
	except Exception as EX:
		await ctx.send(f'Неверный формат ввода данных: {EX}')


@bot.command()
async def v(ctx: Context, dungeon_name: str, visit_count: str):
	try:
		discord_id = str(ctx.message.author.id)

		for i in range(int(visit_count)):
			add = await dungeon_visit_add(
				discord_id=discord_id,
				dungeon_name=dungeon_name
			)
			await ctx.send(add)
	except Exception as ex:
		await ctx.send(f'Неверный формат ввода данных: {ex}')


@bot.command()
async def I(ctx: Context, pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2):
	pilots_cards = await first(pilots_amount, implant_level, skills_rating, gun_rating)
	for pilots_card in pilots_cards:
		pilot_ships = await ships_for_first_dungeon(pilots_card['discord_id'])
		ship_name = []
		core_color = []
		core_lvl = []
		fit_grade = []
		for ships in pilot_ships:
			ship_name.append(ships['ship_name'])
			core_color.append(ships['core_color'])
			core_lvl.append(ships['core_lvl'])
			fit_grade.append(ships['fit_grade'])
		output = table2ascii(
			header=['ИМЯ',
					'ТАГ',
					'TEХ.УР.',
					'РЕЙТ',
					'ПРО-КИ',
					'СР.УР.НА-ОВ',
					'НАЗ.КОР-ЛЯ',
					'ЦВ.ЯДРА',
					'УР.ЯДРА',
					'ФИТ.ГР.'
					],
			body=[
				[
					pilots_card['name'],
					pilots_card['corporation'],
					pilots_card['tech_level'],
					pilots_card['pilot_rating'],
					pilots_card['dungeon_visits_amount'],
					pilots_card['skills_rating'],
					',\n'.join(ship_name),
					',\n'.join(core_color),
					',\n'.join([f'{x}' for x in core_lvl]),
					',\n'.join(fit_grade)
				]
			],
			style=PresetStyle.plain
		)
		await ctx.channel.send(f"```\n{output}\n```")


@bot.command()
async def II(ctx: Context, pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2):
	pilots_cards = await second(pilots_amount, implant_level, skills_rating, gun_rating)
	for pilots_card in pilots_cards:
		pilot_ships = await ships_for_second_dungeon(pilots_card['discord_id'])
		ship_name = []
		core_color = []
		core_lvl = []
		fit_grade = []
		for ships in pilot_ships:
			ship_name.append(ships['ship_name'])
			core_color.append(ships['core_color'])
			core_lvl.append(ships['core_lvl'])
			fit_grade.append(ships['fit_grade'])
		output = table2ascii(
			header=['ИМЯ',
					'ТАГ',
					'TEХ.УР.',
					'РЕЙТ',
					'ПРО-КИ',
					'СР.УР.НА-ОВ',
					'НАЗ.КОР-ЛЯ',
					'ЦВ.ЯДРА',
					'УР.ЯДРА',
					'ФИТ.ГР.'
					],
			body=[
				[
					pilots_card['name'],
					pilots_card['corporation'],
					pilots_card['tech_level'],
					pilots_card['pilot_rating'],
					pilots_card['dungeon_visits_amount'],
					pilots_card['skills_rating'],
					',\n'.join(ship_name),
					',\n'.join(core_color),
					',\n'.join([f'{x}' for x in core_lvl]),
					',\n'.join(fit_grade)
				]
			],
			style=PresetStyle.plain
		)
		await ctx.channel.send(f"```\n{output}\n```")


def run():
	bot.run(config.config['TOKEN'])
