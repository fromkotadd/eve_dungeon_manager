import asyncio

import discord

from eve_db.discord_api import config
from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd
from eve_db.discord_api.test2 import BOT

class Registration:

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction
        self.user_name = interaction.user.name

    async def start(self):
        channel = await (self.interaction.guild.create_text_channel(
            name=self.user_name,
            category=self.interaction.channel.category))
        await channel.send(f'<@{str(self.interaction.user.id)}>')


        # pilot_card_reg = await PilotCardAdd(self.interaction, channel).pilot_card_add()
        dungeon_choice = await DungeonChoice(self.interaction, channel).dungeon_choice()
        answers_ship = await PilotShipAdd(self.interaction, channel).load(dungeon_choice)
        answer_gun_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).gun_skill_reg()
        answer_ship_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).base_ship_skills_reg()
        answer_implant = await PilotImplantAdd(self.interaction, channel).implant(answer_gun_skill['gun_type'])
        await channel.send(
            # f'pilot_card_reg: {pilot_card_reg}\n'
            f'dungeon_choice: {dungeon_choice}\n'
            f'answers_ship: {answers_ship}\n'
            f'answer_gun_skill: {answer_gun_skill}\n'
            f'answer_ship_skill: {answer_ship_skill}\n'
            f'answer_implant: {answer_implant}'
        )
        await channel.send('Registration completed!')
        await asyncio.sleep(60)
        await channel.delete()

    async def write_to_db(self):
        pass

