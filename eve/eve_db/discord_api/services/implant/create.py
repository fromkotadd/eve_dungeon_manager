import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.test2 import BOT

from eve_db.discord_api.choices import ImplantChoices

class PilotImplantAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)

    async def implant(self, gun_type: str):
        self.implant_map = ImplantChoices().implant
        implant = self.implant_map.get(gun_type.upper())
        await self.followup_send_massage(f'Input yor {implant} implant level'
                                        '\n integer range 1-45')
        answer_implant_level = await BOT.wait_for('message', check=lambda
            message: message.author == self.interaction.user)
        await self.followup_send_massage(
            f'Your {implant} implant level is {answer_implant_level.content}')
        return {'implant_name': implant,
                'implant_level': answer_implant_level.content}