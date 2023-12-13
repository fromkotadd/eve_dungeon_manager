import asyncio

import discord

from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd

from eve_db.representors.representors import \
	pilot_card_add, pilot_ship_add, pilot_implant_add, pilot_skill_add
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


        pilot_card = await PilotCardAdd(self.interaction, channel).pilot_card_add()
        dungeon_choice = await DungeonChoice(self.interaction, channel).dungeon_choice()
        answers_ship = await PilotShipAdd(self.interaction, channel).load(dungeon_choice)
        answer_gun_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).gun_skill_reg()
        answer_ship_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).base_ship_skills_reg()
        answer_implant = await PilotImplantAdd(self.interaction, channel).implant(answer_gun_skill['gun_type'])
        await channel.send(
            f'pilot_card_reg: {pilot_card}\n'
            f'dungeon_choice: {dungeon_choice}\n'
            f'answers_ship: {answers_ship}\n'
            f'answer_gun_skill: {answer_gun_skill}\n'
            f'answer_ship_skill: {answer_ship_skill}\n'
            f'answer_implant: {answer_implant}'
        )
        await channel.send('Registration completed!')
        s = await self.django_app_write(pilot_card, answers_ship, answer_gun_skill, answer_ship_skill, answer_implant)
        await channel.send('Django app write completed!')
        await channel.send(s)
        await asyncio.sleep(60)
        await channel.delete()

    async def django_app_write(self,  pilot_card, answers_ship, answer_gun_skill, answer_ship_skill, answer_implant):
        pilot_card_res = await pilot_card_add(
            discord_id=pilot_card['discord_id'],
            name=pilot_card['name'],
            corporation=pilot_card['corporation'].upper(),
            tech_level=pilot_card['tech_level'],
        )
        pilot_ship_reg = await pilot_ship_add(
            discord_id=pilot_card['discord_id'],
            ship_name=answers_ship['ship_name'].lower(),
            core_color=answers_ship['core_color'].lower(),
            core_lvl=answers_ship['core_lvl'],
            fit_grade=answers_ship['fit_grade'].title()
        )
        pilot_gun_skill_reg = await pilot_skill_add(
            discord_id=pilot_card['discord_id'],
            name=answer_gun_skill['gun_type'].lower(),
            level=answer_gun_skill['skill_level'],
            )
        command_skill_reg = await pilot_skill_add(
            discord_id=pilot_card['discord_id'],
            name=f"{answer_ship_skill['ship_type']} command",
            level=answer_ship_skill['command_skill_level'],
            )
        defense_upgrade_skill_reg = await pilot_skill_add(
            discord_id=pilot_card['discord_id'],
            name=f"{answer_ship_skill['ship_type']} defense upgrade",
            level=answer_ship_skill['defense_upgrade_skill_level'],
            )
        engineering_skill_reg = await pilot_skill_add(
            discord_id=pilot_card['discord_id'],
            name=f"{answer_ship_skill['ship_type']} engineering",
            level=answer_ship_skill['engineering_skill_level'],
            )
        implant_reg = await pilot_implant_add(
            discord_id=pilot_card['discord_id'],
            implant_name=answer_implant['implant_name'].lower(),
            implant_level=answer_implant['implant_level'],
            )

        return {
            'pilot_card_res': pilot_card_res,
            'pilot_ship_reg': pilot_ship_reg,
            'pilot_gun_skill_reg': pilot_gun_skill_reg,
            'command_skill_reg': command_skill_reg,
            'defense_upgrade_skill_reg': defense_upgrade_skill_reg,
            'engineering_skill_reg': engineering_skill_reg,
            'implant_reg': implant_reg,
        }

