import asyncio
import discord

from eve_db.discord_api.button_bot import BOT
from eve_db.representors.representors import pilot_card_delete

class PilotCardDelete():
	def __init__(self, interaction: discord.Interaction):
		self.interaction = interaction
		self.discord_id = self.interaction.user.id

	async def pilot_card_delete(self):
		result = await pilot_card_delete(
			discord_id=self.discord_id
		)
		await self.interaction.response.send_message(result, ephemeral=True)
		await asyncio.sleep(10)
		await self.interaction.delete_original_response()
