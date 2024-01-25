import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.button_bot import BOT


class PilotCardAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction, channel):
        super().__init__(interaction)
        self.channel = channel

    async def pilot_card_add(self):
        await self.channel.send(
            'Введи свой игровой ник\n'
            ' Острожно! Этот ник'
            ' будет использоваться для цитирования и поиска вас в базе данных',
        )
        answer_name = await BOT.wait_for('message', check=lambda
			message: message.author == self.interaction.user)


        await self.channel.send(
            'Введи свой корп-тег '
            '(STEP, WGS, EVE, etc)',
        )
        answer_corporation = await BOT.wait_for('message', check=lambda
			message: message.author == self.interaction.user).replace('[', '').replace(']', '')

        message = await self.channel.send(
            'Выбери свой игровой уровень'
            ' (Жмакай эмодзи)'
        )
        await self.add_reactions(message=message, slice=10)
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_tech_level = self.emoji_map(f'{reaction.emoji}')

        return {
            'discord_id': self.discord_id,
            'name': answer_name.content,
            'corporation': answer_corporation.content.upper(),
            'tech_level': answer_tech_level,
        }