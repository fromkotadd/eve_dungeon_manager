import asyncio
import os
from typing import Optional, Literal

import discord
from discord.ui import Button
from eve_db.discord_api import config
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Greedy

from eve_db.representors.representors import first, second, third, fourth, \
	pilot_card_add, pilot_card_upd, pilot_ship_add, pilot_ship_upd, \
	pilot_implant_add, pilot_implant_upd, pilot_skill_add, pilot_skill_upd, \
	dungeon_visit_add
from eve_db.selectors.pilotship import ships_for_first_dungeon, \
	ships_for_second_dungeon, ships_for_third_dungeon, ships_for_fourth_dungeon
from eve_db.utils import table_create
from eve_db.discord_api.utils import prerry_table_output
from eve_db.discord_api.services.pilot.delete import PilotCardDelete

base_dir = os.path.dirname(os.path.realpath(__file__))


class PersistentViewBot(commands.Bot):
	def __init__(self):
		intents = discord.Intents.all()
		intents.message_content = True
		intents.guilds = True
		intents.members = True

		super().__init__(
			command_prefix=commands.when_mentioned_or('.'),
			intents=intents)

	async def setup_hook(self) -> None:
		self.add_view(PersistentViewForRegister())
		self.add_view(PersistentViewForRegisterDungeonVisits())
		self.add_view(PersistentViewForPilotFilterOnLine())
		self.add_view(PersistentViewForPilotFilterOffLine())
		self.add_view(PersistentViewForDelete())

	async def on_ready(self):
		print(f'Logged in as {self.user} (ID: {self.user.id})')
		print('------')


BOT = PersistentViewBot()


class PersistentViewForDelete(discord.ui.View, Button):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(
		label='Delete',
		style=discord.ButtonStyle.red,
		custom_id='Delete'
	)
	async def delete(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button):

		delete = PilotCardDelete(interaction=interaction)
		await delete.pilot_card_delete()


class PersistentViewForRegister(discord.ui.View, Button):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label='Register', style=discord.ButtonStyle.green,
                       custom_id='Register')
	async def register(self, interaction: discord.Interaction,
                       button: discord.ui.Button):
		from eve_db.discord_api.services.registration.registration import \
            Registration
		registration = Registration(interaction=interaction)

		await registration.start()


class PersistentViewForRegisterDungeonVisits(discord.ui.View, Button):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label='I', style=discord.ButtonStyle.green,
                        custom_id='I')
	async def visit_registration_I(self, interaction: discord.Interaction,
                                    button: discord.ui.Button):
		from eve_db.discord_api.services.registration.dungeon_visits import \
        DungeonVisits
		dungeon_name = '1'
		dungeon_visits = DungeonVisits(dungeon_name, interaction)
		answer = await dungeon_visits.write_visits()
		await interaction.response.send_message(answer, ephemeral=True)
		await asyncio.sleep(10)
		await interaction.delete_original_response()

	@discord.ui.button(label='II', style=discord.ButtonStyle.green,
                        custom_id='II')
	async def visit_registration_II(self, interaction: discord.Interaction,
									button: discord.ui.Button):
		from eve_db.discord_api.services.registration.dungeon_visits import \
			DungeonVisits
		dungeon_name = '2'
		dungeon_visits = DungeonVisits(dungeon_name, interaction)
		answer = await dungeon_visits.write_visits()
		await interaction.response.send_message(answer, ephemeral=True)
		await asyncio.sleep(10)
		await interaction.delete_original_response()

	@discord.ui.button(label='III', style=discord.ButtonStyle.green,
					   custom_id='III')
	async def visit_registration_III(self, interaction: discord.Interaction,
									 button: discord.ui.Button):
		from eve_db.discord_api.services.registration.dungeon_visits import \
			DungeonVisits
		dungeon_name = '3'
		dungeon_visits = DungeonVisits(dungeon_name, interaction)
		answer = await dungeon_visits.write_visits()
		await interaction.response.send_message(answer, ephemeral=True)
		await asyncio.sleep(10)
		await interaction.delete_original_response()

	@discord.ui.button(label='IV', style=discord.ButtonStyle.green,
					   custom_id='IV')
	async def visit_registration_IV(self, interaction: discord.Interaction,
									button: discord.ui.Button):
		from eve_db.discord_api.services.registration.dungeon_visits import \
			DungeonVisits
		dungeon_name = '4'
		dungeon_visits = DungeonVisits(dungeon_name, interaction)
		answer = await dungeon_visits.write_visits()
		await interaction.response.send_message(answer, ephemeral=True)
		await asyncio.sleep(10)
		await interaction.delete_original_response()

	@discord.ui.button(label='ALL', style=discord.ButtonStyle.red,
					   custom_id='ALL')
	async def visit_registration_ALL(self, interaction: discord.Interaction,
									 button: discord.ui.Button):
		from eve_db.discord_api.services.registration.dungeon_visits import \
			DungeonVisits
		dungeon_name = ['1', '2', '3', '4']
		for i in range(len(dungeon_name)):
			dungeon_visits = DungeonVisits(dungeon_name[i], interaction)
			answer = await dungeon_visits.write_visits()
		await interaction.response.send_message(
			'До следующего понедельника все дорманты отмечены как посещенные',
			ephemeral=True)
		await asyncio.sleep(10)
		await interaction.delete_original_response()


class PersistentViewForPilotFilterOnLine(discord.ui.View, Button):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label='I', style=discord.ButtonStyle.green,
					   custom_id='First')
	async def I(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'online', ):
		pilots_cards = await first(int(pilots_amount), int(implant_level),
								   skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_first_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ПЕРВЫЙ ДОРМАНТ',
			timeout=300
		)

	@discord.ui.button(label='II', style=discord.ButtonStyle.green,
					   custom_id='Second')
	async def II(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'online'):
		pilots_cards = await second(int(pilots_amount), int(implant_level),
									skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_second_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ВТОРОЙ ДОРМАНТ',
			timeout=300
		)

	@discord.ui.button(label='III', style=discord.ButtonStyle.green,
					   custom_id='Third')
	async def III(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'online'):
		pilots_cards = await third(int(pilots_amount), int(implant_level),
								   skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_third_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ТРЕТИЙ ДОРМАНТ',
			timeout=300
		)


	@discord.ui.button(label='IV', style=discord.ButtonStyle.green,
					   custom_id='Fourth')
	async def IV(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'online'):
		pilots_cards = await fourth(int(pilots_amount), int(implant_level),
									skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_fourth_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ЧЕТВЕРТЫЙ ДОРМАНТТ',
			timeout=300
		)


class PersistentViewForPilotFilterOffLine(discord.ui.View, Button):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label='I', style=discord.ButtonStyle.gray,
					   custom_id='First+')
	async def I(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'Any', ):
		pilots_cards = await first(int(pilots_amount), int(implant_level),
								   skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_first_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ПЕРВЫЙ ДОРМАНТ',
			timeout=300
		)

	@discord.ui.button(label='II', style=discord.ButtonStyle.gray,
					   custom_id='Second+')
	async def II(
            self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'Any'):

		pilots_cards = await second(int(pilots_amount), int(implant_level),
									skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)

		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_second_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ВТОРОЙ ДОРМАНТ',
			timeout=300
		)

	@discord.ui.button(label='III', style=discord.ButtonStyle.gray,
					   custom_id='Third+')
	async def III(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'Any'):
		pilots_cards = await third(int(pilots_amount), int(implant_level),
								   skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_third_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ТРЕТИЙ ДОРМАНТ',
			timeout=300
		)

	@discord.ui.button(label='IV', style=discord.ButtonStyle.gray,
					   custom_id='Fourth+')
	async def IV(
			self,
			interaction: discord.Interaction,
			button: discord.ui.Button,
			pilots_amount: str = '20',
			implant_level: str = '15',
			skills_rating: str = '4-5-3',
			gun_rating: str = '4-5-3',
			status: str = 'Any'):
		pilots_cards = await fourth(int(pilots_amount), int(implant_level),
									skills_rating, gun_rating)
		result = status_check(pilots_cards, interaction, status)
		await prerry_table_output(
			interaction=interaction,
			pilot_data=result,
			pilot_ships_func=ships_for_fourth_dungeon,
			status=status,
			implant_level=implant_level,
			skills_rating=skills_rating,
			gun_rating=gun_rating,
			dungeon_name='ЧЕТВЕРТЫЙ ДОРМАНТ',
			timeout=300
		)


@BOT.command()
@commands.is_owner()
async def delete(ctx: commands.Context):
	await ctx.send(
		file=discord.File(os.path.join(base_dir, 'content/gray_cat.jpg')))
	await ctx.send("Удаление учетных данных пилота",
				   view=PersistentViewForDelete())


@BOT.command()
@commands.is_owner()
async def visits(ctx: commands.Context):  # prepare
	await ctx.send("Отметить посещение дорманта",
				   view=PersistentViewForRegisterDungeonVisits())


@BOT.command()
@commands.is_owner()
async def register(ctx: commands.Context):  # prepare 1
	"""Starts a persistent view."""
	# In order for a persistent view to be listened to, it needs to be sent to an actual message.
	# Call this method once just to store it somewhere.
	# In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.

	await ctx.send("Регистрация в системе",
				   view=PersistentViewForRegister())
	await ctx.send(
		file=discord.File(os.path.join(base_dir, 'content/gray_cat.jpg')))
	await ctx.send("Удаление учетных данных пилота",
				   view=PersistentViewForDelete())


# The stored view can now be reused later on.


@BOT.command()
@commands.is_owner()
async def filter(ctx: commands.Context):
	await ctx.send("Поиск пилотов Онлайн",
				   view=PersistentViewForPilotFilterOnLine())
	await ctx.send(
		file=discord.File(os.path.join(base_dir, 'content/rainbow_cat.jpg')))
	await ctx.send("Поиск пилотов Офлайн",
				   view=PersistentViewForPilotFilterOffLine())


# The stored view can now be reused later on.


@BOT.event
async def on_ready():
	print(f'Logged in as {BOT.user}')  # Bot Name
	print(BOT.user.id)  # Bot ID


# ------ Sync Tree ------
@BOT.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
		ctx: Context, guilds: Greedy[discord.Object],
		spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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


@BOT.tree.command()
async def ida(interaction: discord.Interaction) -> None:
	author = interaction.user
	await interaction.response.send_message(
		(author.id, author.name))  # выводит в чат id автора сообщения


@BOT.tree.command(name="create_pilot_profile",
				  description="registration in the system")
async def pilot_add(interaction: discord.Interaction, name: str,
					corporation: str, tech_level: str):
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {EX}')


@BOT.tree.command(name='update_pilot_profile',
				  description='update pilot card data')
async def pilot_upd(interaction: discord.Interaction, name: str,
					corporation: str, tech_level: str):
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {EX}')


@BOT.tree.command(name='create_pilot_ship',
				  description='register a new dungeon ship')
async def ship_add(interaction: discord.Interaction, ship_name: str,
				   core_color: str, core_lvl: str, fit_grade: str):
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {ex}')


@BOT.tree.command(name='update_pilot_ship', description='ship profile update')
async def ship_upd(interaction: discord.Interaction, ship_name: str,
				   core_color: str, core_lvl: str, fit_grade: str):
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {EX}')


@BOT.tree.command(name='create_pilot_implant',
				  description='register a new implant')
async def implant_add(interaction: discord.Interaction, implant_name: str,
					  implant_level: str):
	try:
		discord_id = str(interaction.user.id)
		add = await pilot_implant_add(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await interaction.response.send_message(add)
	except Exception as ex:
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {ex}')


@BOT.tree.command(name='update_pilot_implant',
				  description='implant profile update')
async def implant_upd(interaction: discord.Interaction, implant_name: str,
					  implant_level: str):
	try:
		discord_id = str(interaction.user.id)
		upd = await pilot_implant_upd(
			discord_id=discord_id,
			implant_name=implant_name.lower(),
			implant_level=implant_level
		)
		await interaction.response.send_message(upd)
	except Exception as EX:
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {EX}')


@BOT.tree.command(name='create_pilot_skill', description='register a new skill')
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {ex}')


@BOT.tree.command(name='update_pilot_skill', description='skill profile update')
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
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {EX}')


@BOT.tree.command(name='visit_dungeon', description='add dungeon visit')
async def v(interaction: discord.Interaction, dungeon_name: str,
			visit_count: str):
	try:
		discord_id = str(interaction.user.id)

		for i in range(int(visit_count)):
			result = await dungeon_visit_add(
				discord_id=discord_id,
				dungeon_name=dungeon_name
			)
		await interaction.response.send_message(result)
	except Exception as ex:
		await interaction.response.send_message(
			f'Неверный формат ввода данных: {ex}')


def status_check(pilots_cards, interaction, status):
	lst = []
	for pilot in range(len(pilots_cards)):
		member = interaction.guild.get_member(
			int(pilots_cards[pilot]['discord_id']))
		if member is not None:
			if member.status != discord.Status.offline:
				lst.append(pilots_cards[pilot])

	if status == 'online':
		return lst
	else:
		return pilots_cards


@BOT.tree.command(name='first_dungeon',
				  description='find pilots for the first dungeon')
async def I(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await first(int(pilots_amount), int(implant_level),
							   skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	await prerry_table_output(
		interaction=interaction,
		pilot_data=result,
		pilot_ships_func=ships_for_first_dungeon,
		status=status,
		implant_level=implant_level,
		skills_rating=skills_rating,
		gun_rating=gun_rating,
		dungeon_name='ПЕРВЫЙ ДОРМАНТ',
		timeout=300
	)


@BOT.tree.command(name='second_dungeon',
				  description='find pilots for the second dungeon')
async def II(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await second(int(pilots_amount), int(implant_level),
								skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	await prerry_table_output(
		interaction=interaction,
		pilot_data=result,
		pilot_ships_func=ships_for_second_dungeon,
		status=status,
		implant_level=implant_level,
		skills_rating=skills_rating,
		gun_rating=gun_rating,
		dungeon_name='ВТОРОЙ ДОРМАНТ',
		timeout=300
	)


@BOT.tree.command(name='third_dungeon',
				  description='find pilots for the third dungeon')
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
	await prerry_table_output(
		interaction=interaction,
		pilot_data=result,
		pilot_ships_func=ships_for_third_dungeon,
		status=status,
		implant_level=implant_level,
		skills_rating=skills_rating,
		gun_rating=gun_rating,
		dungeon_name='ТРЕТИЙ ДОРМАНТ',
		timeout=300
	)


@BOT.tree.command(name='fourth_dungeon',
				  description='find pilots for the first dungeon')
async def IV(
		interaction: discord.Interaction,
		pilots_amount: str = '20',
		implant_level: str = '15',
		skills_rating: str = '4-5-3',
		gun_rating: str = '4-5-3',
		status: str = 'online'):
	pilots_cards = await fourth(int(pilots_amount), int(implant_level),
								skills_rating, gun_rating)
	result = status_check(pilots_cards, interaction, status)
	await prerry_table_output(
		interaction=interaction,
		pilot_data=result,
		pilot_ships_func=ships_for_fourth_dungeon,
		status=status,
		implant_level=implant_level,
		skills_rating=skills_rating,
		gun_rating=gun_rating,
		dungeon_name='ЧЕТВЕРТЫЙ ДОРМАНТ',
		timeout=300
	)


def run():
	BOT.run(config.config['TOKEN'])
