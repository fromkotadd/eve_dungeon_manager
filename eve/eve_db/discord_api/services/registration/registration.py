import asyncio

import discord

from eve_db.discord_api.config import config
from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd
from eve_db.representors.representors import pilot_exists
from eve_db.representors.representors import \
	pilot_card_add, pilot_ship_add, pilot_implant_add, pilot_skill_add
class Registration:

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction
        self.user = self.interaction.user
        self.discord_id = self.interaction.user.id
        self.role = self.interaction.guild.get_role(config['DORMANT_ROLE'])
        self.faq_channel = 1184803402115457054

    async def start(self):
        channel = await (self.interaction.guild.create_text_channel(
            name=self.interaction.user.name,
            category=self.interaction.channel.category))

        async def normal_thread():
            await channel.send(f'<@{str(self.interaction.user.id)}>')
            await self.interaction.response.send_message(
                f'Для регистрации перейди в канал - <#{channel.id}>',
                ephemeral=True)

            pilot_exist = await pilot_exists(discord_id=self.discord_id)
            if not pilot_exist:
                pilot_card = await PilotCardAdd(self.interaction, channel).pilot_card_add()
            else:
                pilot_card = None
            dungeon_choice = await DungeonChoice(self.interaction, channel).dungeon_choice()
            answers_ship = await PilotShipAdd(self.interaction, channel).load(dungeon_choice)
            answer_gun_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).gun_skill_reg()
            answer_ship_skill = await PilotSkillAdd(self.interaction, channel, answers_ship['ship_name']).base_ship_skills_reg()
            answer_implant = await PilotImplantAdd(self.interaction, channel).implant(answer_gun_skill['gun_type'])
            await channel.send('Registration completed!')
            if not pilot_exist:
                write = await self.django_app_write(answers_ship, answer_gun_skill, answer_ship_skill, answer_implant, pilot_card=pilot_card)
            else:
                write = await self.django_app_write(answers_ship, answer_gun_skill, answer_ship_skill, answer_implant, None)
            await channel.send(f'Ознакомится с функционалом бота можно в канале <#{self.faq_channel}>')
            # await channel.send(write)
            try:
                if self.role not in self.user.roles:
                    await self.user.add_roles(self.role)
            except Exception as e:
                print(e)
                await channel.send('Не удалось добавить роль')
                await channel.send(f'Ошибка- {e}')
                await channel.send('Отправь пожалуйста скрин в канал bug-report')
                await asyncio.sleep(60)
                await channel.delete()

            await asyncio.sleep(60)
            await self.interaction.delete_original_response()
            await channel.delete()
        async def kill_thread():
            await asyncio.sleep(600)
            await self.interaction.delete_original_response()
            await channel.delete()

        asyncio.create_task(normal_thread())
        asyncio.create_task(kill_thread())


    async def django_app_write(self, answers_ship, answer_gun_skill, answer_ship_skill, answer_implant, pilot_card=None):
        if pilot_card is not None:
            pilot_card_res = await pilot_card_add(
                discord_id=self.discord_id,
                name=pilot_card['name'],
                corporation=pilot_card['corporation'].upper(),
                tech_level=pilot_card['tech_level'],
            )
        pilot_ship_reg = await pilot_ship_add(
            discord_id=self.discord_id,
            ship_name=answers_ship['ship_name'].lower(),
            core_color=answers_ship['core_color'].lower(),
            core_lvl=answers_ship['core_lvl'],
            fit_grade=answers_ship['fit_grade'].title()
        )
        pilot_gun_skill_reg = await pilot_skill_add(
            discord_id=self.discord_id,
            name=answer_gun_skill['gun_type'].lower(),
            level=answer_gun_skill['skill_level'],
            )
        command_skill_reg = await pilot_skill_add(
            discord_id=self.discord_id,
            name=f"{answer_ship_skill['ship_type']} command",
            level=answer_ship_skill['command_skill_level'],
            )
        defense_upgrade_skill_reg = await pilot_skill_add(
            discord_id=self.discord_id,
            name=f"{answer_ship_skill['ship_type']} defense upgrade",
            level=answer_ship_skill['defense_upgrade_skill_level'],
            )
        engineering_skill_reg = await pilot_skill_add(
            discord_id=self.discord_id,
            name=f"{answer_ship_skill['ship_type']} engineering",
            level=answer_ship_skill['engineering_skill_level'],
            )
        implant_reg = await pilot_implant_add(
            discord_id=self.discord_id,
            implant_name=answer_implant['implant_name'].lower(),
            implant_level=answer_implant['implant_level'],
            )
        if pilot_card is not None:
            return {
                'pilot_card_res': pilot_card_res,
                'pilot_ship_reg': pilot_ship_reg,
                'pilot_gun_skill_reg': pilot_gun_skill_reg,
                'command_skill_reg': command_skill_reg,
                'defense_upgrade_skill_reg': defense_upgrade_skill_reg,
                'engineering_skill_reg': engineering_skill_reg,
                'implant_reg': implant_reg,
            }
        else:
            return {
                'pilot_ship_reg': pilot_ship_reg,
                'pilot_gun_skill_reg': pilot_gun_skill_reg,
                'command_skill_reg': command_skill_reg,
                'defense_upgrade_skill_reg': defense_upgrade_skill_reg,
                'engineering_skill_reg': engineering_skill_reg,
                'implant_reg': implant_reg,
            }

