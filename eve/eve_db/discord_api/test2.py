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

bot = PersistentViewBot()

from eve_db.discord_api.services.dungeon.create import DungeonChoice
from eve_db.discord_api.services.implant.create import PilotImplantAdd
from eve_db.discord_api.services.pilot.create import PilotCardAdd
from eve_db.discord_api.services.pilotship.create import PilotShipAdd
from eve_db.discord_api.services.skill.create import PilotSkillAdd



class PersistentViewForRegister(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Register', style=discord.ButtonStyle.green, custom_id='Register')
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Welcome to registration!', ephemeral=False)
        a = interaction.user.id
        await interaction.followup.send(f'User: {a}')
        x = await DungeonChoice(interaction).dungeon_choice()
        await interaction.followup.send(f'DungeonChoice: {x}')
        b = await PilotCardAdd(interaction).pilot_card_add()
        await interaction.followup.send(f'PilotCardAdd: {b}')
        c = await PilotShipAdd(interaction).load(x)
        await interaction.followup.send(f'PilotShipAdd: {c}')
        d = await PilotSkillAdd(interaction, c['ship_name']).gun_skill_choices()
        await interaction.followup.send(f'PilotSkillAdd.gun_skill_choices: {d}')
        f = await PilotSkillAdd(interaction, c['ship_name']).base_ship_skills_reg()
        await interaction.followup.send(f'PilotSkillAdd.base_ship_skills_reg: {f}')
        e = await PilotImplantAdd(interaction).implant(d['gun_type'])
        await interaction.followup.send(f'PilotImplantAdd: {e}')


@bot.command()
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
    bot.run(config.config['TOKEN'])