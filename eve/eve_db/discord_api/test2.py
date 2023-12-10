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
        a = interaction.user.id
        await interaction.followup.send(f'User: {a}')
        x = await DungeonChoice(interaction).dungeon_choice()

        b = await PilotCardAdd(interaction).pilot_card_add()
        await interaction.followup.send(f'PilotCardAdd: {b}')
        c = await PilotShipAdd(interaction).load(x)
        await interaction.followup.send(f'PilotShipAdd: {c}')
        d = await PilotSkillAdd(interaction, c['ship_name']).gun_skill_choices()
        await interaction.followup.send(f'PilotSkillAdd.gun_skill_choices: {d}')
        f = await PilotSkillAdd(interaction, c['ship_name']).base_ship_skills_reg()
        await interaction.followup.send(f'PilotSkillAdd.base_ship_skills_reg: {f}')
        e = await PilotImplantAdd(interaction).implant(d['gun_type'])
        await interaction.followup.send(f'PilotImplantAdd: {e}')




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
        self.ship_for_dungeon = {
            '1': {
                1: 'VINDICATOR',
                2: 'BHAAlGORN',
                3: 'NIGHTMARE',
		    },
            '2': {
                1: 'APOCALYPSE STRIKER',
                2: 'APOCALYPSE NAVY ISSUE',
                3: 'NIGHTMARE',
                4: 'MEGATHRON STRIKER',
                5: 'MEGATHRON NAVY ISSUE',
            },
            '3': {
                1: 'NAGLFAR',
                2: 'PHOENIX',
                3: 'MOROS',
                4: 'REVELATION',
                5: 'THANATOS',
                6: 'ARCHON',
                7: 'CHIMERA',
                8: 'NIDHOUGGUR',
            },
            '4': {
                1: 'NAGLFAR',
                2: 'PHOENIX',
                3: 'MOROS',
                4: 'REVELATION',
            }
        }


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

        return self.ship_for_dungeon.get(answer_dungeon)

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
        self.implant_map = {
            'LARGE RAILGUN': 'HIGH POWER COIL',
            'CAPITAL RAILGUN': 'HIGH POWER COIL',
            'LARGE LASER': 'FOCUSED CRYSTAL',
            'CAPITAL LASER': 'FOCUSED CRYSTAL',
            'LARGE CANNON': 'BARRAGE REPRESSION',
            'CAPITAL CANNON': 'BARRAGE REPRESSION',
            'LARGE MISSILE': 'WARHEAD CHARGE',
            'CAPITAL MISSILE': 'WARHEAD CHARGE',
        }
        print(gun_type.upper())
        implant = self.implant_map.get(gun_type.upper())
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
        self.ships_type_dict = {
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

    async def gun_skill_choices(self):
        gun_type = self.ship_gun_typ_dict.get(self.answer_ship.upper(), None)
        if gun_type:
            return await self.gun_skill_reg(gun_type)
        else:
            return False

    async def gun_skill_reg(self, gun_type: str):
        message = await self.followup_send_massage(
            f'Choose your level of {gun_type} skill (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_skill_level = self.skill_map.get(self.emoji_map(f'{reaction.emoji}'))
        await self.followup_send_massage(
            f'Selected skill level: {answer_skill_level}'
        )
        return {
            'gun_type': gun_type.upper(),
            'skill_level': answer_skill_level
        }

    async def base_ship_skills_reg(self):
        message = await self.followup_send_massage(
            f'Select your command skill level for {self.answer_ship} (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_command_skill_level = self.skill_map.get(
            self.emoji_map(f'{reaction.emoji}'))

        message = await self.followup_send_massage(
            f'Select your defense upgrade skill level for {self.answer_ship} (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_defense_upgrade_level = self.skill_map.get(
            self.emoji_map(f'{reaction.emoji}'))

        message = await self.followup_send_massage(
            f'Select your engineering skill level for {self.answer_ship} (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_engineering_level = self.skill_map.get(self.emoji_map(f'{reaction.emoji}'))

        await self.followup_send_massage(
            f'Your base ship skills are '
            f'\n command skill level:{answer_command_skill_level},'
            f'\n defense upgrade level: {answer_defense_upgrade_level},'
            f'\n engineering_level: {answer_engineering_level}'
            f'\n for {self.answer_ship}, '
            f' and your ship type is {self.ships_type_dict.get(self.answer_ship.upper())}'
        )
        result = {
            'command_skill_level': answer_command_skill_level,
            'defense_upgrade_skill_level': answer_defense_upgrade_level,
            'engineering_skill_level': answer_engineering_level,
            'ship_name': self.answer_ship,
            'ship_type': self.ships_type_dict.get(self.answer_ship.upper())
        }
        return result


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
async def a(ctx: commands.Context): #prepare
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("Регистрация", view=PersistentViewForRegister())
    # The stored view can now be reused later on.

def run():
    bot.run(config.config['TOKEN'])