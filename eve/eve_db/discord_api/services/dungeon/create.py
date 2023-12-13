from eve_db.discord_api.services.base import BaseDiscordActionService
import discord

from eve_db.discord_api.test2 import BOT
from eve_db.discord_api.choices import ShipForDungeonChoices

class DungeonChoice(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction, channel):
        super().__init__(interaction)
        self.ship_for_dungeon = ShipForDungeonChoices().ship_for_dungeon
        self.channel = channel

    async def dungeon_choice(self):
        message = await self.channel.send(
            'Выбери дормант для регистрации'
            ' (Жмакай эмодзи)'
        )

        await self.add_reactions(slice=4, message=message)
        answer = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)

        answer_dungeon = self.emoji_map(f'{answer.emoji}')

        return self.ship_for_dungeon.get(answer_dungeon)