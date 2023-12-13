import asyncio

import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands.context import Context
from discord.utils import get

from eve_db.discord_api import config
from eve_db.representors.representors import first,\
	pilot_card_add, pilot_ship_add, pilot_implant_add, pilot_skill_add

from discord.ext import commands
import discord

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentViewForRegister())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

BOT = PersistentViewBot()

class PersistentViewForRegister(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Register', style=discord.ButtonStyle.green, custom_id='Register')
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        from eve_db.discord_api.services.registration.registration import \
            Registration

        # channel = await interaction.guild.create_text_channel("registration", category=interaction.channel.category)
        registration = Registration(interaction=interaction)
        await registration.start()

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