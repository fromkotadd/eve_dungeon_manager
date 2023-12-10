import discord

from eve_db.discord_api.services.base import BaseDiscordActionService
from eve_db.discord_api.test2 import bot

from eve_db.discord_api.choices import CoreColorsChoices, FitGradeChoices

class PilotShipAdd(BaseDiscordActionService):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)
        self.required_core_colors = CoreColorsChoices.get_core_colors
        self.required_fit_grade = FitGradeChoices.get_fit_grade

    async def core_color(self):
        message = await self.followup_send_massage('Select your core color'
                                                  '(Press the number)\n'
                                                  '1: Green\n'
                                                  '2: Blue\n'
                                                  '3: Violet\n'
                                                  '4: Gold\n'
                                                  '5: None\n')

        await self.add_reactions(message=message, slice=5)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_color = self.emoji_map(f'{reaction.emoji}')

        await self.followup_send_massage(
            f'Selected core_color color is {self.required_core_colors[int(answer_core_color)]}'
        )
        return self.required_core_colors[int(answer_core_color)]

    async def core_level(self):
        message = await self.followup_send_massage('Select your core level'
                                                  '(Press the number)')
        await self.add_reactions(message=message, slice=7)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_core_lvl = self.emoji_map(f'{reaction.emoji}')
        await self.followup_send_massage(
            f'Selected core level is {int(answer_core_lvl)}'
        )
        return answer_core_lvl

    async def fit_grade(self):

        message = await self.followup_send_massage('Select your fit grade'
                                                  '(Press the number)'
                                                  '\n1: C-grade\n'
                                                  '2: B-grade\n'
                                                  '3: A-grade\n'
                                                  '4: X-grade\n')
        await self.add_reactions(message=message, slice=4)
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_fit_grade = self.emoji_map(f'{reaction.emoji}')
        await self.interaction.followup.send(
            f'Selected fit grade is {self.required_fit_grade[int(answer_fit_grade)]}'
        )
        return self.required_fit_grade[int(answer_fit_grade)]


    async def load(self, required_ships_dict):

        message = await self.followup_send_massage(
            f'Choose your ship for registration\n'
            f'{[(x, y) for x, y in required_ships_dict.items()]}'
        )

        await self.add_reactions(message=message, slice=len(required_ships_dict))
        reaction = await bot.wait_for('raw_reaction_add', check=lambda
            payload: payload.user_id == self.interaction.user.id)
        answer_ship_choice = self.emoji_map(f'{reaction.emoji}')

        ship_name = required_ships_dict[int(answer_ship_choice)]
        await self.followup_send_massage(
            f'Selected ship: {ship_name}')

        core_color_ = await self.core_color()
        core_lvl_ = await self.core_level()
        fit_grade_ = await self.fit_grade()
        await self.followup_send_massage(
            f'Selected ship: {ship_name}\n'
            f'Selected core color: {core_color_}\n'
            f'Selected core level: {core_lvl_}\n'
            f'Selected fit grade: {fit_grade_}'
        )
        return {'ship_name': ship_name.lower(), 'core_color': core_color_,
                'core_lvl': core_lvl_, 'fit_grade': fit_grade_}