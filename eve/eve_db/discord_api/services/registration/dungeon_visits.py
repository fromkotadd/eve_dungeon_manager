from typing import List

import discord

from eve_db.representors.representors import pilot_exists
from eve_db.representors.representors import dungeon_visit_add

class DungeonVisits:
	def __init__(self, dungeon: str, interaction: discord.Interaction):
		self.interaction = interaction
		self.dungeon = dungeon
		self.discord_id = self.interaction.user.id
		self.discord_name = self.interaction.user.name
	async def write_visits(self):
		pilot_exist = await pilot_exists(discord_id=self.discord_id)
		if not pilot_exist:
			return f'Пользователь {self.discord_name} не зарегистрирован'
		for i in range(10):
			result = await dungeon_visit_add(self.discord_id, self.dungeon)
		return result
