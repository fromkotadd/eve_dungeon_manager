from typing import Optional

from eve_db.forms.pilot import PilotForm
from eve_db.services.base import BaseDiscordActionService
from eve_db.selectors.pilot import pilot_by_discord_id_exists_selector

class CreatePilotService(BaseDiscordActionService):

	def __init__(self, name: str, corporation: str, tech_level: str, pilot_rating: str):
		self._name = name
		self._corporation = corporation
		self._tech_level = tech_level
		self._pilot_rating = pilot_rating

	def execute(self) -> str:
		if pilot_by_discord_id_exists_selector(discord_id=self._discord_id):
			return 'You already registered'

		form = PilotForm({
			'discord_id': self._discord_id,
			'name': self._name,
			'corporation': self._corporation,
			'tech_level': self._tech_level,
			'pilot_rating': self._pilot_rating,
		})
		if not form.is_valid():
			return form.errors

		form.save()
		return 'Pilot registered'

	def _validate_pilot(self, discord_id: str) -> Optional[str]:
		# для регистрации валидация пилота не нужна
		pass
