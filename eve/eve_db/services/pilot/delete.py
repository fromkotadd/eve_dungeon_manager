from typing import Optional

from eve_db.selectors.pilot import pilot_by_discord_id_exists_selector
from eve_db.selectors.pilot import _pilot_card_delete

class DeletePilotService:
	def __init__(self, discord_id):
		self.discord_id = discord_id

	def delete(self) -> Optional[str]:
		if pilot_by_discord_id_exists_selector(self.discord_id):
			_pilot_card_delete(self.discord_id)
			return 'Pilot card removed from database'
		return "pilot card not found"