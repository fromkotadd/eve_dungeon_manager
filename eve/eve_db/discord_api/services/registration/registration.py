from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd

async def send_welcome(interaction):
  await interaction.response.send_message("Welcome!")

class Registration:

    def __init__(self, interaction):
        self.interaction = interaction

    async def start(self):
        await send_welcome(self.interaction)

        pilot_card_reg = await PilotCardAdd(self.interaction).pilot_card_add()
        dungeon_choice = await DungeonChoice(self.interaction).dungeon_choice()
        answers_ship = await PilotShipAdd(self.interaction).load(dungeon_choice)
        answer_gun_skill = await PilotSkillAdd(self.interaction, answers_ship['ship_name']).gun_skill_reg()
        answer_ship_skill = await PilotSkillAdd(self.interaction, answers_ship['ship_name']).base_ship_skills_reg()
        answer_implant = await PilotImplantAdd(self.interaction).implant(answer_gun_skill['gun_type'])
        await self.interaction.followup.send(
            f'pilot_card_reg: {pilot_card_reg}\n'
            f'dungeon_choice: {dungeon_choice}\n'
            f'answers_ship: {answers_ship}'
            f'answer_gun_skill: {answer_gun_skill}\n'
            f'answer_ship_skill: {answer_ship_skill}\n'
            f'answer_implant: {answer_implant}'
        )
        await self.interaction.followup.send('Registration completed!')

    async def write_to_db(self):
        pass

