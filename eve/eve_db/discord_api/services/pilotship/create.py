import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.test2 import BOT

from eve_db.discord_api.choices import CoreColorsChoices, FitGradeChoices

class PilotShipAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)
        self.required_core_colors = CoreColorsChoices().core_colors
        self.required_fit_grade = FitGradeChoices().fit_grade

    async def core_color(self):
        message = await self.followup_send_massage('Select your core color'
                                                  '(Press the number)\n'
                                                  '1: Green\n'
                                                  '2: Blue\n'
                                                  '3: Violet\n'
                                                  '4: Gold\n'
                                                  '5: None\n')

        await self.add_reactions(message=message, slice=5)
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_color = self.emoji_map(f'{reaction.emoji}')
        return self.required_core_colors[int(answer_core_color)]

    async def core_level(self):
        message = await self.followup_send_massage('Select your core level'
                                                  '(Press the number)')
        await self.add_reactions(message=message, slice=7)
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_lvl = self.emoji_map(f'{reaction.emoji}')

        return answer_core_lvl

    async def fit_grade(self):

        message = await self.followup_send_massage('Select your fit grade'
                                                  '(Press the number)'
                                                  '\n1: C-grade\n'
                                                  '2: B-grade\n'
                                                  '3: A-grade\n'
                                                  '4: X-grade\n')
        await self.add_reactions(message=message, slice=4)
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_fit_grade = self.emoji_map(f'{reaction.emoji}')
        return self.required_fit_grade[int(answer_fit_grade)]


    async def load(self, required_ships_dict):

        message = await self.followup_send_massage(
            f'Choose your ship for registration\n'
            f'{[(x, y) for x, y in required_ships_dict.items()]}'
        )

        await self.add_reactions(message=message, slice=len(required_ships_dict))
        reaction = await BOT.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_ship_choice = self.emoji_map(f'{reaction.emoji}')

        ship_name = required_ships_dict[int(answer_ship_choice)]
        core_color_ = await self.core_color()
        core_lvl_ = await self.core_level()
        fit_grade_ = await self.fit_grade()

        return {'ship_name': ship_name.upper(), 'core_color': core_color_,
                'core_lvl': core_lvl_, 'fit_grade': fit_grade_}