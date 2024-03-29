from typing import Optional, Literal

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Greedy

from eve_db.discord_api import config
from eve_db.representors.representors import first, pilot_card_add, pilot_ship_add, \
	pilot_implant_add, pilot_skill_add, dungeon_visit_add, pilot_card_upd, pilot_ship_upd, \
	pilot_implant_upd, pilot_skill_upd, second, third, fourth
from eve_db.selectors.pilotship import ships_for_first_dungeon, ships_for_second_dungeon, ships_for_third_dungeon, \
	ships_for_fourth_dungeon
from eve_db.utils import table_create

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='~', intents=intents, owner_id=config.config['OWNER_ID'])
# ID_CHANNEL = config.config['ID_CHANNEL']
# guild = discord.Object(id=config.config['GUILD_ID'])


@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')  # Bot Name
	print(bot.user.id)  # Bot ID


# ------ Sync Tree ------
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
		ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
	if not guilds:
		if spec == "~":
			synced = await ctx.bot.tree.sync(guild=ctx.guild)
		elif spec == "*":
			ctx.bot.tree.copy_global_to(guild=ctx.guild)
			synced = await ctx.bot.tree.sync(guild=ctx.guild)
		elif spec == "^":
			ctx.bot.tree.clear_commands(guild=ctx.guild)
			await ctx.bot.tree.sync(guild=ctx.guild)
			synced = []
		else:
			synced = await ctx.bot.tree.sync()

		await ctx.send(
			f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
		)


@bot.tree.command()
async def ida(interaction: discord.Interaction) -> None:
	author = interaction.user
	await interaction.response.send_message((author.id, author.name))  # выводит в чат id автора сообщения


@bot.tree.command(name="create_pilot_profile", description="registration in the system")
async def pilot_add(interaction: discord.Interaction, name: str, corporation: str, tech_level: str):
	try:
		discord_id = str(interaction.user.id)
		reg = await pilot_card_add(
			discord_id=discord_id,
			name=name,
			corporation=corporation.upper(),
			tech_level=tech_level,
		)
		await interaction.response.send_message(reg)
	except Exception as EX:
		await interaction.response.send_message(f'Неверный формат ввода данных: {EX}')


@bot.tree.command(name='update_pilot_profile', description='update pilot card data')
async def pilot_upd(interaction: discord.Interaction, name: str, corporation: str, tech_level: str):
	try:
		discord_id = str(interaction.user.id)
		upd = await pilot_card_upd(
			discord_id=discord_id,
			name=name,
			corporation=corporation.upper(),
			tech_level=tech_level,
		)
		await interaction.response.send_message(upd)
	except Exception as EX:
		await interaction.response.send_message(f'Неверный формат ввода данных: {EX}')


@bot.tree.command(name='create_pilot_ship', description='register a new dungeon ship')
async def ship_add(interaction: discord.Interaction, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	try:
		discord_id = str(interaction.user.id)
		add = await pilot_ship_add(
			discord_id=discord_id,
			ship_name=ship_name.lower(),
			core_color=core_color.lower(),
			core_lvl=core_lvl,
			fit_grade=fit_grade.title()
		)
		await interaction.response.send_message(add)
	except Exception as ex:
		await interaction.response.send_message(add)(f'Неверный формат ввода данных: {ex}')


@bot.tree.command(name='update_pilot_ship', description='ship profile update')
async def ship_upd(interaction: discord.Interaction, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	try:
		discord_id = str(interaction.user.id)
		upd = await pilot_ship_upd(
			discord_id=discord_id,
			ship_name=ship_name.lower(),
			core_color=core_color.lower(),
			core_lvl=core_lvl,
			fit_grade=fit_grade.title()
		)
		await interaction.response.send_message(upd)
	except Exception as EX:
		await interaction.response.send_message(f'Неверный формат ввода данных: {EX}')


@bot.tree.command(name='create_pilot_implant', description='register a new implant')
async def implant_add(interaction: discord.Interaction, implant_name: str, implant_level: str):
	try:
		discord_id = str(interaction.user.id)
		add = await pilot_implant_add(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await interaction.response.send_message(add)
	except Exception as ex:
		await interaction.response.send_message(f'Неверный формат ввода данных: {ex}')


@bot.tree.command(name='update_pilot_implant', description='implant profile update')
async def implant_upd(interaction: discord.Interaction, implant_name: str, implant_level: str):
	try:
		discord_id = str(interaction.user.id)
		upd = await pilot_implant_upd(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await interaction.response.send_message(upd)
	except Exception as EX:
		await interaction.response.send_message(f'Неверный формат ввода данных: {EX}')


@bot.tree.command(name='create_pilot_skill', description='register a new skill')
async def skill_add(interaction: discord.Interaction, name: str, level: str):
	try:
		discord_id = str(interaction.user.id)
		add = await pilot_skill_add(
			discord_id=discord_id,
			name=name.lower(),
			level=level
		)
		await interaction.response.send_message(add)
	except Exception as ex:
		await interaction.response.send_message(f'Неверный формат ввода данных: {ex}')


@bot.tree.command(name='update_pilot_skill', description='skill profile update')
async def skill_upd(interaction: discord.Interaction, name: str, level: str):
	try:
		discord_id = str(interaction.user.id)
		upd = await pilot_skill_upd(
			discord_id=discord_id,
			name=name.lower(),
			level=level
		)
		await interaction.response.send_message(upd)
	except Exception as EX:
		await interaction.response.send_message(f'Неверный формат ввода данных: {EX}')


@bot.tree.command(name='visit_dungeon', description='add dungeon visit')
async def v(interaction: discord.Interaction, dungeon_name: str, visit_count: str):
	try:
		discord_id = str(interaction.user.id)

		for i in range(int(visit_count)):
				await dungeon_visit_add(
				discord_id=discord_id,
				dungeon_name=dungeon_name
			)
		await interaction.response.send_message(f'Посещение {dungeon_name} зарегистрировано')
	except Exception as ex:
		await interaction.response.send_message(f'Неверный формат ввода данных: {ex}')


def status_check(pilots_cards, interaction, status):
	lst = []
	for pilot in range(len(pilots_cards)):
		member = interaction.guild.get_member(int(pilots_cards[pilot]['discord_id']))
		if member is not None:
			if member.status != discord.Status.offline:
				lst.append(pilots_cards[pilot])

	if status == 'online':
		return lst
	else:
		return pilots_cards


@bot.tree.command(name='first_dungeon', description='find pilots for the first dungeon')
async def I(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):

	pilots_cards = await first(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_first_dungeon)

	await interaction.response.send_message(f"```\nПЕРВЫЙ ДОРМАНТ\n"
											f"Статус пилотов: {status}\n"
											f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
											f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
											f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
											f"\n{output}\n```")


@bot.tree.command(name='second_dungeon', description='find pilots for the second dungeon')
async def II(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await second(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_second_dungeon)

	await interaction.response.send_message(f"```\nВТОРОЙ ДОРМАНТ\n"
											f"Статус пилотов: {status}\n"
											f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
											f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
											f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
											f"\n{output}\n```")


@bot.tree.command(name='third_dungeon', description='find pilots for the third dungeon')
async def III(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await third(int(pilots_amount), int(implant_level),
								 skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	output = await table_create(pilots_cards=result,
								pilot_ships_func=ships_for_third_dungeon)

	await interaction.response.send_message(f"```\nТРЕТИЙ ДОРМАНТ\n"
											f"Статус пилотов: {status}\n"
											f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
											f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
											f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
											f"\n{output}\n```", ephemeral=True)


@bot.tree.command(name='fourth_dungeon', description='find pilots for the first dungeon')
async def IV(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await fourth(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_fourth_dungeon)
	await interaction.response.send_message(f"```\nЧЕТВЕРТЫЙ ДОРМАНТ\n"
											f"Статус пилотов: {status}\n"
											f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
											f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
											f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
											f"\n{output}\n```")


def run():
	bot.run(config.config['TOKEN'])
