import asyncio

import discord
from discord.ui import Button
from eve_db.discord_api import config
from discord.ext import commands

from eve_db.discord_api.discord_bot import status_check
from eve_db.representors.representors import first, second, third, fourth
from eve_db.selectors.pilotship import ships_for_first_dungeon, \
    ships_for_second_dungeon, ships_for_third_dungeon, ships_for_fourth_dungeon
from eve_db.utils import table_create


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentViewForRegister())
        self.add_view(PersistentViewForRegisterDungeonVisits())
        self.add_view(PersistentViewForPilotFilter())

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

        registration = Registration(interaction=interaction)
        await registration.start()

class PersistentViewForRegisterDungeonVisits(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I', style=discord.ButtonStyle.green, custom_id='I')
    async def visit_registration_I(self, interaction: discord.Interaction, button: discord.ui.Button):
        from eve_db.discord_api.services.registration.dungeon_visits import \
            DungeonVisits
        dungeon_name = '1'
        dungeon_visits = DungeonVisits(dungeon_name, interaction)
        answer = await dungeon_visits.write_visits()
        await interaction.response.send_message(answer, ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

    @discord.ui.button(label='II', style=discord.ButtonStyle.green,
                       custom_id='II')
    async def visit_registration_II(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
        from eve_db.discord_api.services.registration.dungeon_visits import \
            DungeonVisits
        dungeon_name = '2'
        dungeon_visits = DungeonVisits(dungeon_name, interaction)
        answer = await dungeon_visits.write_visits()
        await interaction.response.send_message(answer, ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

    @discord.ui.button(label='III', style=discord.ButtonStyle.green,
                       custom_id='III')
    async def visit_registration_III(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
        from eve_db.discord_api.services.registration.dungeon_visits import \
            DungeonVisits
        dungeon_name = '3'
        dungeon_visits = DungeonVisits(dungeon_name, interaction)
        answer = await dungeon_visits.write_visits()
        await interaction.response.send_message(answer, ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

    @discord.ui.button(label='IV', style=discord.ButtonStyle.green,
                       custom_id='IV')
    async def visit_registration_IV(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
        from eve_db.discord_api.services.registration.dungeon_visits import \
            DungeonVisits
        dungeon_name = '4'
        dungeon_visits = DungeonVisits(dungeon_name, interaction)
        answer = await dungeon_visits.write_visits()
        await interaction.response.send_message(answer, ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

    @discord.ui.button(label='ALL', style=discord.ButtonStyle.red,
                       custom_id='ALL')
    async def visit_registration_ALL(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
        from eve_db.discord_api.services.registration.dungeon_visits import \
            DungeonVisits
        dungeon_name = ['1', '2', '3', '4']
        for i in range(len(dungeon_name)):
            dungeon_visits = DungeonVisits(dungeon_name[i], interaction)
            answer = await dungeon_visits.write_visits()
        await interaction.response.send_message('До следующего понедельника все дорманты отмечены как посещенные', ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

class PersistentViewForPilotFilter(discord.ui.View, Button):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I', style=discord.ButtonStyle.green, custom_id='First')
    async def I(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            pilots_amount: str = '20',
            implant_level: str = '15',
            skills_rating: str = '4-5-3',
            gun_rating: str = '4-5-3',
            status: str = 'online',):
        pilots_cards = await first(int(pilots_amount), int(implant_level),
                                   skills_rating, gun_rating)
        result = status_check(pilots_cards, interaction, status)
        output = await table_create(pilots_cards=result,
                                    pilot_ships_func=ships_for_first_dungeon)

        await interaction.response.send_message(f"```\nПЕРВЫЙ ДОРМАНТ\n"
                                                f"Статус пилотов: {status}\n"
                                                f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
                                                f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
                                                f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
                                                f"\n{output}\n```", ephemeral=True)
        await asyncio.sleep(600)
        await interaction.delete_original_response()

    @discord.ui.button(label='II', style=discord.ButtonStyle.green,
                       custom_id='Second')
    async def II(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            pilots_amount: str = '20',
            implant_level: str = '15',
            skills_rating: str = '4-5-3',
            gun_rating: str = '4-5-3',
            status: str = 'online'):
        pilots_cards = await second(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
        result = status_check(pilots_cards, interaction, status)
        output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_second_dungeon)

        await interaction.response.send_message(f"```\nВТОРОЙ ДОРМАНТ\n"
                                                f"Статус пилотов: {status}\n"
                                                f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
                                                f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
                                                f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
                                                f"\n{output}\n```", ephemeral=True)
        await asyncio.sleep(600)
        await interaction.delete_original_response()

    @discord.ui.button(label='III', style=discord.ButtonStyle.green,
                       custom_id='Third')
    async def III(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            pilots_amount: str = '20',
            implant_level: str = '15',
            skills_rating: str = '4-5-3',
            gun_rating: str = '4-5-3',
            status: str = 'online'):
        pilots_cards = await third(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
        result = status_check(pilots_cards, interaction, status)
        output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_third_dungeon)

        await interaction.response.send_message(f"```\nТРЕТИЙ ДОРМАНТ\n"
                                                f"Статус пилотов: {status}\n"
                                                f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
                                                f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
                                                f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
                                                f"\n{output}\n```", ephemeral=True)
        await asyncio.sleep(600)
        await interaction.delete_original_response()

    @discord.ui.button(label='IV', style=discord.ButtonStyle.green,
                       custom_id='Fourth')
    async def IV(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
            pilots_amount: str = '20',
            implant_level: str = '15',
            skills_rating: str = '4-5-3',
            gun_rating: str = '4-5-3',
            status: str = 'online'):
        pilots_cards = await fourth(int(pilots_amount), int(implant_level), skills_rating, gun_rating)
        result = status_check(pilots_cards, interaction, status)
        output = await table_create(pilots_cards=result, pilot_ships_func=ships_for_fourth_dungeon)
        await interaction.response.send_message(f"```\nЧЕТВЕРТЫЙ ДОРМАНТ\n"
                                                f"Статус пилотов: {status}\n"
                                                f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
                                                f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
                                                f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
                                                f"\n{output}\n```", ephemeral=True)
        await asyncio.sleep(600)
        await interaction.delete_original_response()

@BOT.command()
@commands.is_owner()
async def visits(ctx: commands.Context): #prepare
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("Посещение дорманта",
                   view=PersistentViewForRegisterDungeonVisits())
    # The stored view can now be reused later on.
@BOT.command()
@commands.is_owner()
async def register(ctx: commands.Context): #prepare
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("Регистрация в системе",
                   view=PersistentViewForRegister())
    # The stored view can now be reused later on.

@BOT.command()
@commands.is_owner()
async def filter(ctx: commands.Context): #prepare
    await ctx.send("Поиск пилотов",
                   view=PersistentViewForPilotFilter())
    # The stored view can now be reused later on.
def run():
    BOT.run(config.config['TOKEN'])