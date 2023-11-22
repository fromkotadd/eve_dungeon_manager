import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands.context import Context

from eve_db.discord_api import config
from eve_db.representors.representors import first,\
	pilot_card_add, pilot_ship_add, pilot_implant_add, pilot_skill_add

from discord.ext import commands
import discord

from eve_db.discord_api.services.base import BaseDiscordActionService

class PersistentViewForRegister(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Register', style=discord.ButtonStyle.green, custom_id='Register')
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Welcome to registration!', ephemeral=False)
        s = interaction.user.id
        await interaction.followup.send(f'User: {s}')
        await DungeonChoice(interaction).dungeon_choice()
        b = await PilotCardAdd(interaction).pilot_card_add()
        await interaction.followup.send(f'PilotCardAdd: {b}')
        c = await PilotShipAdd(interaction).load(required_ships)
        await interaction.followup.send(f'PilotShipAdd: {c}')
        d = await PilotImplantAdd(interaction).implant('LARGE RAILGUN')
        await interaction.followup.send(f'PilotImplantAdd: {d}')


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentViewForRegister())


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


class DungeonChoice(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)

    async def dungeon_choice(self):
        message = await self.followup_send_massage('Choose a dungeon'
                                                   ' for registration '
                                                   '(Press the number)')

        await self.add_reactions(slice=4, message=message)
        answer = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)

        answer_dungeon = self.emoji_map(f'{answer.emoji}')
        await self.followup_send_massage(
            f'Your dungeon chose is {int(answer_dungeon)}')

        return answer_dungeon

class PilotCardAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)

    async def pilot_card_add(self):
        await self.followup_send_massage('Input your in game nick-name'
                                                ' Warning! This nick-'
                                                'name will be used in the base')
        answer_name = await bot.wait_for('message', check=lambda
			message: message.author == self.interaction.user)

        await self.followup_send_massage('Input your in game corporation'
                                        ' teg (STEP, WGS, EVE, etc)')
        answer_corporation = await bot.wait_for('message', check=lambda
			message: message.author == self.interaction.user)

        message = await self.followup_send_massage(
            'Select your in game tech level'
            ' (Press the number)')
        await self.add_reactions(message=message, slice=10)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_tech_level = self.emoji_map(f'{reaction.emoji}')

        # discord_id = str(self.interaction.user.id)
        return {'discord_id': self.discord_id,
                'name': answer_name.content,
                'corporation': answer_corporation.content.upper(),
                'tech_level': answer_tech_level,
                'interaction': self.interaction
                }

class PilotShipAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)
        self.required_core_colors = {
            1: 'GREEN',
            2: 'BLUE',
            3: 'VIOLET',
            4: 'GOLD',
            5: 'NONE',
        }
        self.required_fit_grade = {
            1: 'C',
            2: 'B',
            3: 'A',
            4: 'X',
        }

    async def core_color(self):
        message = await self.followup_send_massage('Select your core color'
                                                  '(Press the number)\n'
                                                  '1: Green\n'
                                                  '2: Blue\n'
                                                  '3: Violet\n'
                                                  '4: Gold\n'
                                                  '5: None\n')

        await self.add_reactions(message=message, slice=5)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_color = self.emoji_map(f'{reaction.emoji}')

        await self.followup_send_massage(
            f'Selected core_color color is {self.required_core_colors[int(answer_core_color)]}'
        )
        return self.required_core_colors[int(answer_core_color)]

    async def core_level(self):
        message = await self.followup_send_massage('Select your core level'
                                                  '(Press the number)')
        await self.add_reactions(message=message, slice=7)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_lvl = self.emoji_map(f'{reaction.emoji}')
        await self.followup_send_massage(
            f'Selected core level is {int(answer_core_lvl)}'
        )
        return answer_core_lvl

    async def fit_grade(self):

        message = await self.followup_send_massage('Select your fit grade'
                                                  '(Press the number)'
                                                  '\n1: C-grade\n'
                                                  '2: B-grade\n'
                                                  '3: A-grade\n'
                                                  '4: X-grade\n')
        await self.add_reactions(message=message, slice=4)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_fit_grade = self.emoji_map(f'{reaction.emoji}')
        await self.interaction.followup.send(
            f'Selected fit grade is {self.required_fit_grade[int(answer_fit_grade)]}'
        )
        return self.required_fit_grade[int(answer_fit_grade)]


    async def load(self, required_ships_dict):

        message = await self.followup_send_massage(
            f'Choose your ship for registration\n'
            f'{[(x, y) for x, y in required_ships_dict.items()]}'
        )

        await self.add_reactions(message=message, slice=len(required_ships_dict))
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_ship_choice = self.emoji_map(f'{reaction.emoji}')

        ship_name = required_ships_dict[int(answer_ship_choice)]
        await self.followup_send_massage(
            f'Selected ship: {ship_name}')

        core_color_ = await self.core_color()
        core_lvl_ = await self.core_level()
        fit_grade_ = await self.fit_grade()
        await self.followup_send_massage(
            f'Selected ship: {ship_name}\n'
            f'Selected core color: {core_color_}\n'
            f'Selected core level: {core_lvl_}\n'
            f'Selected fit grade: {fit_grade_}'
        )
        return {'ship_name': ship_name.lower(), 'core_color': core_color_,
                'core_lvl': core_lvl_, 'fit_grade': fit_grade_}
class PilotImplantAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)

    async def implant(self, gun_type: str):
        implant_map = {
            'LARGE RAILGUN': 'HIGH POWER COIL',
            'CAPITAL RAILGUN': 'HIGH POWER COIL',
            'LARGE LASER': 'FOCUSED CRYSTAL',
            'CAPITAL LASER': 'FOCUSED CRYSTAL',
            'LARGE CANNON': 'BARRAGE REPRESSION',
            'CAPITAL CANNON': 'BARRAGE REPRESSION',
            'LARGE MISSILE': 'WARHEAD CHARGE',
            'CAPITAL MISSILE': 'WARHEAD CHARGE',
        }
        implant = implant_map.get(gun_type)
        await self.followup_send_massage(f'Input yor {implant} implant level'
                                        '\n integer range 1-45')
        answer_implant_level = await bot.wait_for('message', check=lambda
            message: message.author == self.interaction.user)
        await self.followup_send_massage(
            f'Your {implant} implant level is {answer_implant_level.content}')
        return {'implant_name': implant,
                'implant_level': answer_implant_level.content}

class PilotSkillAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction, answer_ship: str):
        super().__init__(interaction)
        self.answer_ship = answer_ship
        self.skill_map = {
            '1': '4-4',
            '2': '4-5-3',
            '3': '5-5-4',
        }
        self.ship_gun_typ_dict = {
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

    async def gun_skill_reg(self, gun_type: str, skill_map: dict):
        message = await self.followup_send_massage(
            f'Choose your level of {gun_type} skill (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_skill_level = skill_map.get(self.emoji_map(f'{reaction.emoji}'))
        await self.followup_send_massage(
            f'Selected skill level: {answer_skill_level}'
        )
        return answer_skill_level, gun_type

        gun_typ = self.ship_gun_typ_dict.get(self.answer_ship.upper())
        if gun_typ == 'LARGE LASER':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)
        if gun_typ == 'LARGE RAILGUN':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)
        if gun_typ == 'CAPITAL MISSILE':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)
        if gun_typ == 'CAPITAL CANNON':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)
        if gun_typ == 'CAPITAL RAILGUN':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)
        if gun_typ == 'FIGHTER':
            return await gun_skill_fun_body(interaction, gun_typ, skill_map)

bot = PersistentViewBot()

required_ships = {
			1: 'APOCALYPSE STRIKER',
			2: 'APOCALYPSE NAVY ISSUE',
			3: 'NIGHTMARE',
			4: 'MEGATHRON STRIKER',
			5: 'MEGATHRON NAVY ISSUE',
		}
@bot.command()
@commands.is_owner()
async def prepare(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("Регистрация", view=PersistentViewForRegister())
    # The stored view can now be reused later on.

def run():
    bot.run(config.config['TOKEN'])