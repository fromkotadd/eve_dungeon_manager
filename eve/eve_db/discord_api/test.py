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
bot = commands.Bot(command_prefix='~', intents=intents, owner_id=config.config['OWNER_ID'])
ID_CHANNEL = config.config['ID_CHANNEL']
guild = discord.Object(id=config.config['GUILD_ID'])

def emoji_map(emoji):
	emoji_num_dict = {
		'1️⃣': '1', '2️⃣': '2', '3️⃣': '3', '4️⃣': '4', '5️': '5',
		'6️': '6', '7️': '7', '8️':  '8', '9️': '9', '🔟': '10'
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

	await interaction.response.send_message('Input your in game nick-name - Jon '
											'Dir, Bob33 etc. Warning! This nick-'
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
	reaction = await bot.wait_for('raw_reaction_add')
	answer_tech_level = emoji_map(f'{reaction.emoji}')

	discord_id = str(interaction.user.id)

	reg = await pilot_card_add(
		discord_id=discord_id,
		name=answer_name.content,
		corporation=answer_corporation.content.upper(),
		tech_level=answer_tech_level,
	)
	await interaction.followup.send(reg)
	if reg == 'Pilot registered':
		answer_ship = await ship_registration_choice(interaction)
		core_choice = None
		core_lvl = None
		fit_grade = None


async def ship_registration_choice(interaction: discord.Interaction):
	async def dungeon_registration_choice(interaction: discord.Interaction):
		message = await interaction.followup.send('Select your dungeon'
												  '(Press the number)')
		for emoji in range(4):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_dungeon = emoji_map(f'{reaction.emoji}')
		await interaction.followup.send(
			f'Your dungeon chose is {int(answer_dungeon)}')
		return answer_dungeon

	async def core(interaction: discord.Interaction):
		message = await interaction.followup.send('Select your core'
												  '(Press the number)\n'
												  '1: Green\n'
												  '2: Blue\n'
												  '3: Violet\n'
												  '4: Gold\n'
												  '5: None\n')

		for emoji in range(5):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_core = emoji_map(f'{reaction.emoji}')
		await interaction.followup.send(
			f'Selected core color is {int(answer_core)}')
		return answer_core

	dungeon_choice = await dungeon_registration_choice(interaction)

	if dungeon_choice == '1':
		required_ships = {
			1: 'VINDICATOR',
			2: 'BHAAlGORN',
			3: 'NIGHTMARE',
		}
		message = await interaction.followup.send(
			f'Choose your ship for registration on first dungeon\n'
			f'{[(x, y) for x, y in required_ships.items()]}'
		)

		for emoji in range(len(required_ships.keys())):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_ship_choice = emoji_map(f'{reaction.emoji}')

		selected_ship = required_ships[int(answer_ship_choice)]
		await interaction.followup.send(
			f'Selected ship: {selected_ship}')

		core_choice = await core(interaction)
		return selected_ship, core_choice

	if dungeon_choice == '2':
		required_ships = {
			1: 'APOCALYPSE_STRIKER',
			2: 'APOCALYPSE_NAVY_ISSUE',
			3: 'NIGHTMARE',
			4: 'MEGATHRON_STRIKER',
			5: 'MEGATHRON_NAVY_ISSUE',
		}
		message = await interaction.followup.send(
			f'Choose your ship for registration on first dungeon\n'
			f'{[(x, y) for x, y in required_ships.items()]}'
		)

		for emoji in range(len(required_ships.keys())):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_ship_choice = emoji_map(f'{reaction.emoji}')

		selected_ship = required_ships[int(answer_ship_choice)]
		await interaction.followup.send(
			f'Selected ship: {selected_ship}')
		core_choice = await core(interaction)
		return selected_ship, core_choice

	if dungeon_choice == '3':
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
		message = await interaction.followup.send(
			f'Choose your ship for registration on first dungeon\n'
			f'{[(x, y) for x, y in required_ships.items()]}'
		)

		for emoji in range(len(required_ships.keys())):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_ship_choice = emoji_map(f'{reaction.emoji}')

		selected_ship = required_ships[int(answer_ship_choice)]
		await interaction.followup.send(
			f'Selected ship: {selected_ship}')
		core_choice = await core(interaction)
		return selected_ship, core_choice


	if dungeon_choice == '4':
		required_ships = {
			1: 'NAGLFAR',
			2: 'PHOENIX',
			3: 'MOROS',
			4: 'REVELATION',
		}
		message = await interaction.followup.send(
			f'Choose your ship for registration on first dungeon\n'
			f'{[(x, y) for x, y in required_ships.items()]}'
		)

		for emoji in range(len(required_ships.keys())):
			await message.add_reaction(emoji_list[emoji])
		reaction = await bot.wait_for('raw_reaction_add')
		answer_ship_choice = emoji_map(f'{reaction.emoji}')

		selected_ship = required_ships[int(answer_ship_choice)]
		await interaction.followup.send(
			f'Selected ship: {selected_ship}')
		core_choice = await core(interaction)
		return selected_ship, core_choice


@bot.command()
async def reg(ctx: Context):
	register_button = BaseButton(label='Register', custom_id='register', style=discord.ButtonStyle.primary)
	view = BaseView(ctx=ctx)
	view.add_item(register_button)
	await ctx.send('Welcome to registration!', view=view)


def run():
	bot.run(config.config['TOKEN'])