from eve_db.discord_api.services.base import BaseDiscordActionService
import discord

from eve_db.discord_api.test2 import bot
from eve_db.discord_api.choices import ShipForDungeonChoices

class DungeonChoice(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)
        self.ship_for_dungeon = ShipForDungeonChoices().ship_for_dungeon

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