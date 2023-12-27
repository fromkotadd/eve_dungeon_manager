from eve_db.utils import table_create
import discord
from typing import List
import asyncio

async def prerry_table_output(interaction: discord.Interaction,
							  pilot_data: List,
							  pilot_ships_func: List,
							  implant_level: str,
							  skills_rating: str,
							  gun_rating: str,
							  status: str,
							  dungeon_name:str,
							  timeout: int):

	if pilot_data == []:
		await interaction.response.send_message('Подходящих пилотов не обнаружено', ephemeral=True)

	else:
		await interaction.response.send_message(
			f"```\n=========={dungeon_name}===========\n```",
			ephemeral=True
		)
		for i in range(0, len(pilot_data), 5):
			output = await table_create(pilots_cards=pilot_data[i:i + 5],
										pilot_ships_func=pilot_ships_func)
			await interaction.followup.send(
				f"```Статус пилотов: {status}\n"
				f"УРОВЕНЬ ИМПЛАНТА>={implant_level} "
				f" ПРОКАЧКА КОРАБЛЯ>={skills_rating} "
				f"ПРОКАЧКА ОРУДИЙ>={gun_rating}"
				f"\n{output}\n```", ephemeral=True
			)
		await interaction.followup.send('==========END==========', ephemeral=True)
		await asyncio.sleep(timeout)
		await interaction.delete_original_response()