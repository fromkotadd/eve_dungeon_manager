import re
from typing import Optional, Literal
import discord

from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands.context import Context
from discord.ext.commands import Greedy


from eve_db.discord_api import config
import eve_db.discord_api.discord_bot
from eve_db.representors.representors import first, pilot_card_add, pilot_ship_add, \
	pilot_implant_add, pilot_skill_add, dungeon_visit_add, pilot_card_upd, pilot_ship_upd, \
	pilot_implant_upd, pilot_skill_upd, second, third, fourth
from eve_db.selectors.pilotship import ships_for_first_dungeon, ships_for_second_dungeon, ships_for_third_dungeon, \
	ships_for_fourth_dungeon
from eve_db.utils import table_create, table_create_

from sympy.abc import y

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, owner_id=config.config['OWNER_ID'])
ID_CHANNEL = config.config['ID_CHANNEL']
guild = discord.Object(id=config.config['GUILD_ID'])

def emoji_map(emoji):
	emoji_num_dict = {
		'1️⃣': '1', '2️⃣': '2', '3️⃣': '3', '4️⃣': '4', '5️⃣': '5',
		'6️⃣': '6', '7️⃣': '7', '8️⃣':  '8', '9️⃣': '9', '🔟': '10'
	}
	return emoji_num_dict.get(emoji, 'хуй пизда')

emoji_list = [
		'1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣',
		'6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'
		]

class BaseButton(Button):
	def __init__(self, label, custom_id, style, row=None):
		super().__init__(label=label, custom_id=custom_id, style=style, row=row)

	async def callback(self, interaction: discord.Interaction):
		if self.custom_id == 'register':
			await pilot_card_reg(interaction)
		# await interaction.followup.send('You pressed the button!', ephemeral=True)

class BaseView(View):
	def __init__(self, ctx: Context = None, timeout: int = 1800, *args, **kwargs):
		self.ctx = ctx
		super().__init__(timeout=timeout, *args, **kwargs)

	async def interaction_check(self, interaction: discord.Interaction):
		return interaction.user == self.ctx.author

async def pilot_card_reg(interaction: discord.Interaction):

	await interaction.response.send_message('Input your in game nick-name'
											' Warning! This nick-'
											'name will be used in the base')
	answer_name = await bot.wait_for('message', check=lambda
		message: message.author == interaction.user)

	await interaction.followup.send('Input your in game corporation'
									' teg (STEP, WGS, EVE, etc)')
	answer_corporation = await bot.wait_for('message', check=lambda
		message: message.author == interaction.user)

	message = await interaction.followup.send('Select your in game tech level'
											  ' (Press the number)')
	for emoji in range(10):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_tech_level = emoji_map(f'{reaction.emoji}')

	discord_id = str(interaction.user.id)

	pilot_card_reg = await pilot_card_add(
		discord_id=discord_id,
		name=answer_name.content,
		corporation=answer_corporation.content.upper(),
		tech_level=answer_tech_level,
	)
	await interaction.followup.send(pilot_card_reg)
	if pilot_card_reg == 'Pilot registered':
	# if 1==1:
		answers_ship = await dungeon_registration_choice(interaction)
		answer_ship_name = answers_ship[0]['ship_name'].upper()
		pilot_ship_reg = await pilot_ship_add(discord_id=discord_id,
								   ship_name=answer_ship_name.lower(),
								   core_color=answers_ship[0]['core_color'].lower(),
								   core_lvl=answers_ship[0]['core_lvl'],
								   fit_grade=answers_ship[0]['fit_grade'].title())
		await interaction.followup.send(pilot_ship_reg)
	if pilot_ship_reg.endswith('added'):
	# if 1 == 1:
		answer_skill_level, answer_skill_name = await gun_skill_reg(interaction, answer_ship_name)
		pilot_gun_skill_reg = await pilot_skill_add(discord_id=discord_id,
												name=answer_skill_name.lower(),
												level=answer_skill_level,
												)
		await interaction.followup.send(pilot_gun_skill_reg)
	if pilot_gun_skill_reg.endswith('added'):
	# if 1 == 1:

		result = await ship_skills_reg(interaction, answer_ship_name)
	answer_command_skill_reg = await pilot_skill_add(discord_id=discord_id,
													 name=f"{result['ship_type']} command",
													 level=result['command_skill_level'],
													 )
	await interaction.followup.send(answer_command_skill_reg)
	answer_defense_upgrade_reg = await pilot_skill_add(discord_id=discord_id,
													  name=f"{result['ship_type']} defense upgrade",
													  level=result['defense_upgrade_skill_level'],
													  )
	await interaction.followup.send(answer_defense_upgrade_reg)
	answer_engineering_reg = await pilot_skill_add(discord_id=discord_id,
												   name=f"{result['ship_type']} engineering",
												   level=result['engineering_skill_level'],
												   )
	await interaction.followup.send(answer_engineering_reg)

	if answer_command_skill_reg.endswith('added')\
			and answer_defense_upgrade_reg.endswith('added')\
			and answer_engineering_reg.endswith('added'):
		pass

async def core_color(interaction: discord.Interaction):
	required_core_colors = {
		1: 'GREEN',
		2: 'BLUE',
		3: 'VIOLET',
		4: 'GOLD',
		5: 'NONE',
	}
	message = await interaction.followup.send('Select your core color'
											  '(Press the number)\n'
											  '1: Green\n'
											  '2: Blue\n'
											  '3: Violet\n'
											  '4: Gold\n'
											  '5: None\n')
	for emoji in range(5):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_core_color = emoji_map(f'{reaction.emoji}')
	await interaction.followup.send(
		f'Selected core_color color is {required_core_colors[int(answer_core_color)]}'
	)
	return required_core_colors[int(answer_core_color)]

async def core_level(interaction: discord.Interaction):
	message = await interaction.followup.send('Select your core level'
											  '(Press the number)')
	for emoji in range(7):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_core_lvl = emoji_map(f'{reaction.emoji}')
	await interaction.followup.send(
		f'Selected core level is {int(answer_core_lvl)}'
	)
	return answer_core_lvl

async def fit_grade(interaction: discord.Interaction):
	required_fit_grade = {
		1: 'C',
		2: 'B',
		3: 'A',
		4: 'X',
	}
	message = await interaction.followup.send('Select your fit grade'
											  '(Press the number)'
											  '\n1: C-grade\n'
											  '2: B-grade\n'
											  '3: A-grade\n'
											  '4: X-grade\n')
	for emoji in range(4):
		await message.add_reaction(emoji_list[emoji])

	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_fit_grade = emoji_map(f'{reaction.emoji}')
	await interaction.followup.send(
		f'Selected fit grade is {required_fit_grade[int(answer_fit_grade)]}'
	)
	return required_fit_grade[int(answer_fit_grade)]

async def ship_registration_function_body(interaction: discord.Interaction,
										  required_ships: dict):
	message = await interaction.followup.send(
		f'Choose your ship for registration on first dungeon\n'
		f'{[(x, y) for x, y in required_ships.items()]}'
	)

	for emoji in range(len(required_ships.keys())):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_ship_choice = emoji_map(f'{reaction.emoji}')

	ship_name = required_ships[int(answer_ship_choice)]
	await interaction.followup.send(
		f'Selected ship: {ship_name}')

	core_color_ = await core_color(interaction)
	core_lvl_ = await core_level(interaction)
	fit_grade_ = await fit_grade(interaction)
	await interaction.followup.send(
		f'Selected ship: {ship_name}\n'
		f'Selected core color: {core_color_}\n'
		f'Selected core level: {core_lvl_}\n'
		f'Selected fit grade: {fit_grade_}'
	)
	return {'ship_name': ship_name.lower(), 'core_color': core_color_,
			'core_lvl': core_lvl_, 'fit_grade': fit_grade_}


async def gun_skill_reg(interaction: discord.Interaction,
						answer_ship: str):
	skill_map = {
		'1': '4-4',
		'2': '4-5-3',
		'3': '5-5-4',
		}
	ship_gun_typ_dict = {
		'BHAAlGORN': 'LARGE LASER',
		'NIGHTMARE': 'LARGE LASER',
		'APOCALYPSE NAVY ISSUE': 'LARGE LASER',
		'APOCALYPSE STRIKER': 'LARGE LASER',
		'MEGATHRON NAVY ISSUE': 'LARGE RAILGUN',
		'MEGATHRON STRIKER': 'LARGE RAILGUN',
		'VINDICATOR': 'LARGE RAILGUN',
		'PHOENIX': 'CAPITAL MISSILE',
		'NAGLFAR': 'CAPITAL CANNON',
		'MOROS': 'CAPITAL RAILGUN',
		'REVELATION': 'CAPITAL LASER',
		'THANATOS': 'FIGHTER',
		'ARCHON': 'FIGHTER',
		'CHIMERA': 'FIGHTER',
		'NIDHOUGGUR': 'FIGHTER',
	}

	async def gun_skill_fun_body(interaction: discord.Interaction,
				  gun_type: str,
				  skill_map: dict):
		message = await interaction.followup.send(
			f'Choose your level of {gun_type} skill (Press the number)\n'
			'1: 4-4\n'
			'2: 4-5-3\n'
			'3: 5-5-4\n'
		)
		for emoji in range(3):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add', check=lambda
			payload: payload.user_id == interaction.user.id)
		answer_skill_level = skill_map.get(emoji_map(f'{reaction.emoji}'))
		await interaction.followup.send(
			f'Selected skill level: {answer_skill_level}'
		)
		return answer_skill_level, gun_type

	gun_typ = ship_gun_typ_dict.get(answer_ship.upper())
	if gun_typ == 'LARGE LASER':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)
	if gun_typ == 'LARGE RAILGUN':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)
	if gun_typ == 'CAPITAL MISSILE':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)
	if  gun_typ == 'CAPITAL CANNON':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)
	if  gun_typ == 'CAPITAL RAILGUN':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)
	if  gun_typ == 'FIGHTER':
		return await gun_skill_fun_body(interaction, gun_typ, skill_map)

async def ship_skills_reg_fun_body(interaction: discord.Interaction,
								   answer_ship: str,
								   ship_type_dict: dict,
								   skill_map: dict,
								   ):
	message = await interaction.followup.send(
		f'Select your command skill level for {answer_ship} (Press the number)\n'
		'1: 4-4\n'
		'2: 4-5-3\n'
		'3: 5-5-4\n'
	)
	for emoji in range(3):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_command_skill_level = skill_map.get(
		emoji_map(f'{reaction.emoji}'))

	message = await interaction.followup.send(
		f'Select your defense upgrade skill level for {answer_ship} (Press the number)\n'
		'1: 4-4\n'
		'2: 4-5-3\n'
		'3: 5-5-4\n'
	)
	for emoji in range(3):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_defense_upgrade_level = skill_map.get(
		emoji_map(f'{reaction.emoji}'))

	message = await interaction.followup.send(
		f'Select your engineering skill level for {answer_ship} (Press the number)\n'
		'1: 4-4\n'
		'2: 4-5-3\n'
		'3: 5-5-4\n'
	)
	for emoji in range(3):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_engineering_level = skill_map.get(emoji_map(f'{reaction.emoji}'))

	await interaction.followup.send(
		f'Your base ship skills are '
		f'\n command skill level:{answer_command_skill_level},'
		f'\n defense upgrade level: {answer_defense_upgrade_level},'
		f'\n engineering_level: {answer_engineering_level}'
		f'\n for {answer_ship}, '
		f' and your ship type is {ship_type_dict.get(answer_ship)}'
	)
	result = {
		'command_skill_level': answer_command_skill_level,
		'defense_upgrade_skill_level': answer_defense_upgrade_level,
		'engineering_skill_level': answer_engineering_level,
		'ship_name': answer_ship,
		'ship_type': ship_type_dict.get(answer_ship)
	}
	print(result)
	return result
async def ship_skills_reg(interaction: discord.Interaction, answer_ship: str):
	skill_map = {
		'1': '4-4',
		'2': '4-5-3',
		'3': '5-5-4',
	}
	ships_type_dict = {
		'APOCALYPSE STRIKER': 'battleship',
		'APOCALYPSE NAVY ISSUE': 'battleship',
		'MEGATHRON STRIKER': 'battleship',
		'MEGATHRON NAVY ISSUE': 'battleship',
		'VINDICATOR': 'battleship',
		'BHAAlGORN': 'battleship',
		'NIGHTMARE': 'battleship',
		'PHOENIX': 'dreadnought',
		'NAGLFAR': 'dreadnought',
		'MOROS': 'dreadnought',
		'REVELATION': 'dreadnought',
		'THANATOS': 'carrier',
		'ARCHON': 'carrier',
		'CHIMERA': 'carrier',
		'NIDHOUGGUR': 'carrier',
	}
	ship_type = ships_type_dict.get(answer_ship)



	if ship_type == 'battleship':
		return await ship_skills_reg_fun_body(interaction, answer_ship, ships_type_dict, skill_map)
	if ship_type == 'dreadnought':
		return await ship_skills_reg_fun_body(interaction, answer_ship, ships_type_dict, skill_map)
	if ship_type == 'carrier':
		return await ship_skills_reg_fun_body(interaction, answer_ship, ships_type_dict, skill_map)

async def Implant(interaction: discord.Interaction, gun_type: str):
	implant_map = {
		'LARGE RAILGUN': 'HIGH POWER COIL',
		'CAPITAL RAILGUN':  ('HIGH POWER COIL', 'THERMAL CIRCULATION'),
		'LARGE LASER': 'FOCUSED CRYSTAL',
		'CAPITAL LASER': 'FOCUSED CRYSTAL',
		'LARGE CANNON': ('BARRAGE REPRESSION', 'SNIPING TECHNOLOGY'),
		'CAPITAL CANNON': ('BARRAGE REPRESSION', 'SNIPING TECHNOLOGY'),

		}
	if gun_type == 'LARGE RAILGUN':
		await interaction.followup.send('Input yor HIGH POWER COIL implant level'
										'\n integer range 1-45')
		answer_implant_level = await bot.wait_for('message', check=lambda
			message: message.author == interaction.user)

async def dungeon_registration_choice(interaction: discord.Interaction):
	message = await interaction.followup.send('Choose a dungeon'
											  ' for registration '
											  '(Press the number)')
	for emoji in range(4):
		await message.add_reaction(emoji_list[emoji])
	reaction = await bot.wait_for('raw_reaction_add', check=lambda
		payload: payload.user_id == interaction.user.id)
	answer_dungeon = emoji_map(f'{reaction.emoji}')
	await interaction.followup.send(
		f'Your dungeon chose is {int(answer_dungeon)}')

	if answer_dungeon == '1':
		required_ships = {
			1: 'VINDICATOR',
			2: 'BHAAlGORN',
			3: 'NIGHTMARE',
		}
		return await ship_registration_function_body(interaction, required_ships), answer_dungeon


	if answer_dungeon == '2':
		required_ships = {
			1: 'APOCALYPSE STRIKER',
			2: 'APOCALYPSE NAVY ISSUE',
			3: 'NIGHTMARE',
			4: 'MEGATHRON STRIKER',
			5: 'MEGATHRON NAVY ISSUE',
		}
		return await ship_registration_function_body(interaction, required_ships), answer_dungeon


	if answer_dungeon == '3':
		required_ships = {
			1: 'NAGLFAR',
			2: 'PHOENIX',
			3: 'MOROS',
			4: 'REVELATION',
			5: 'THANATOS',
			6: 'ARCHON',
			7: 'CHIMERA',
			8: 'NIDHOUGGUR',
		}
		return await ship_registration_function_body(interaction, required_ships), answer_dungeon


	if answer_dungeon == '4':
		required_ships = {
			1: 'NAGLFAR',
			2: 'PHOENIX',
			3: 'MOROS',
			4: 'REVELATION',
		}
		return await ship_registration_function_body(interaction, required_ships), answer_dungeon

@bot.command()
async def reg(ctx: Context):
	register_button = BaseButton(label='Register', custom_id='register', style=discord.ButtonStyle.primary)
	view = BaseView(ctx=ctx)
	view.add_item(register_button)
	await ctx.send('Welcome to registration!', view=view)

def run():
	bot.run(config.config['TOKEN'])