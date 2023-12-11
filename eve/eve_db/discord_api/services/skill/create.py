import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.test2 import BOT

from eve_db.discord_api.choices import PilotSkill

class PilotSkillAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction, answer_ship: str):
        super().__init__(interaction)
        self.answer_ship = answer_ship
        self.skill_map = PilotSkill().skill_map
        self.ship_gun_typ_dict = PilotSkill().ship_gun_typ_dict
        self.ships_type_dict = PilotSkill().ships_type_dict
        self.gun_type = self.ship_gun_typ_dict.get(self.answer_ship.upper(), None)

    async def gun_skill_choices(self):
        gun_type = self.ship_gun_typ_dict.get(self.answer_ship.upper(), None)
        if gun_type:
            return await self.gun_skill_reg()
        else:
            return False

    async def gun_skill_reg(self):
        message = await self.followup_send_massage(
            f'Choose your level of {self.gun_type} skill (Press the number)\n'
            '1: 4-4\n'
            '2: 4-5-3\n'
            '3: 5-5-4\n'
        )
        await self.add_reactions(message=message, slice=3)
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_skill_level = self.skill_map.get(
            self.emoji_map(f'{reaction.emoji}'))
        return {
            'gun_type': self.gun_type.upper(),
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
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
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
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
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
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_engineering_level = self.skill_map.get(
            self.emoji_map(f'{reaction.emoji}'))

        result = {
            'command_skill_level': answer_command_skill_level,
            'defense_upgrade_skill_level': answer_defense_upgrade_level,
            'engineering_skill_level': answer_engineering_level,
            'ship_name': self.answer_ship,
            'ship_type': self.ships_type_dict.get(self.answer_ship.upper())
        }
        return result

    async def load(self):
        gun_skill = await self.gun_skill_choices()
        base_ship_skills = await self.base_ship_skills_reg()

        return gun_skill, base_ship_skills