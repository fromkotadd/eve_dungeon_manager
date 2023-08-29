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


intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='~', intents=intents, owner_id=config.config['OWNER_ID'])
ID_CHANNEL = config.config['ID_CHANNEL']
guild = discord.Object(id=config.config['GUILD_ID'])

def emoji_map(emoji):
	if emoji == '1️⃣':
		return '1'
	elif emoji == '2️⃣':
		return '2'
	elif emoji == '3️':
		return '3'
	elif emoji == '4️⃣':
		return '4'
	elif emoji == '5️':
		return '5'
	elif emoji == '6️':
		return '6'
	elif emoji == '7️':
		return '7'
	elif emoji == '8️':
		return '8'
	elif emoji == '9️':
		return '9'
	elif emoji == '🔟':
		return '10'
	else:
		return 'хуй пизда'

class BaseButton(Button):
	def __init__(self, label, custom_id, style, row=None):
		super().__init__(label=label, custom_id=custom_id, style=style, row=row)

	async def callback(self, interaction: discord.Interaction):
		if self.custom_id == 'register':
			await registration(interaction)
		#
		# await interaction.response.send_message('You pressed the button!', ephemeral=True)

class BaseView(View):
	def __init__(self, ctx: Context = None, timeout: int = 1800, *args, **kwargs):
		self.ctx = ctx
		super().__init__(timeout=timeout, *args, **kwargs)

	async def interaction_check(self, interaction: discord.Interaction):
		return interaction.user == self.ctx.author

async def registration(interaction: discord.Interaction):

	await interaction.response.send_message('Input your in game nick-name')
	answer_name = await bot.wait_for('message', check=lambda
		message: message.author == interaction.user)

	await interaction.followup.send('Input your in game corporation teg (STEP, WGS, EVE, etc)')
	answer_corporation = await bot.wait_for('message', check=lambda
		message: message.author == interaction.user)

	message = await interaction.followup.send('Select your in game tech level')

	await message.add_reaction('1️⃣')
	await message.add_reaction('2️⃣')
	await message.add_reaction('3️⃣')
	await message.add_reaction('4️⃣')
	await message.add_reaction('5️⃣')
	await message.add_reaction('6️⃣')
	await message.add_reaction('7️⃣')
	await message.add_reaction('8️⃣')
	await message.add_reaction('9️⃣')
	await message.add_reaction('🔟')


	reaction = await bot.wait_for('raw_reaction_add')
	answer_tech_level = emoji_map(f'{reaction.emoji}')

	result =  await pilot_card_add(discord_id=str(interaction.user.id),
						 name=answer_name.content,
						 corporation=answer_corporation.content.upper(),
						 tech_level= answer_tech_level)

	await interaction.followup.send(result)




@bot.command()
async def reg(ctx: Context):
	register_button = BaseButton(label='Register', custom_id='register', style=discord.ButtonStyle.primary)
	view = BaseView(ctx=ctx)
	view.add_item(register_button)
	await ctx.send('Welcome!', view=view)

def run():
	bot.run(config.config['TOKEN'])