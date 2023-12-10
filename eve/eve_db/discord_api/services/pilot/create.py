import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.test2 import bot


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

        return {'discord_id': self.discord_id,
                'name': answer_name.content,
                'corporation': answer_corporation.content.upper(),
                'tech_level': answer_tech_level,
                'interaction': self.interaction
                }