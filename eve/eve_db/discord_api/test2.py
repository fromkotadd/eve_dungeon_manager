import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands.context import Context

from eve_db.discord_api import config
from eve_db.representors.representors import first,\
	pilot_card_add, pilot_ship_add, pilot_implant_add, pilot_skill_add

from discord.ext import commands
import discord

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentViewForRegister())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

BOT = PersistentViewBot()

from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd

async def send_welcome(interaction):
  await interaction.response.send_message("Welcome!")

async def add_pilot_card(interaction):
  return await PilotCardAdd(interaction).pilot_card_add()

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
        await BOT.close()

class PersistentViewForRegister(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Register', style=discord.ButtonStyle.green, custom_id='Register')



    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message('Welcome to registration!', ephemeral=True)
        registration = Registration(interaction)
        await registration.start()
    #     pilot_card_reg = await PilotCardAdd(interaction).pilot_card_add()
    #     dungeon_choice = await DungeonChoice(interaction).dungeon_choice()
    #     answers_ship = await PilotShipAdd(interaction).load(dungeon_choice)
    #     answer_gun_skill, answer_ship_skill =  await PilotSkillAdd(interaction, answers_ship['ship_name']).load()
    #     answer_implant = await PilotImplantAdd(interaction).implant(answer_gun_skill['gun_type'])
    #
    #     await interaction.followup.send(
    #         f'pilot_card_reg: {pilot_card_reg}\n'
    #         f'dungeon_choice: {dungeon_choice}\n'
    #         f'answers_ship: {answers_ship}'
    #         f'answer_gun_skill: {answer_gun_skill}\n'
    #         f'answer_ship_skill: {answer_ship_skill}\n'
    #         f'answer_implant: {answer_implant}'
    #     )
    #     await interaction.followup.send('Registration completed!')
    #     await BOT.close()


@BOT.command()
@commands.is_owner()
async def a(ctx: commands.Context): #prepare
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("Регистрация", view=PersistentViewForRegister())
    # The stored view can now be reused later on.

def run():
    BOT.run(config.config['TOKEN'])