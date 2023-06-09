from eve_db.models import Pilot
from eve_db.forms.pilot import PilotForm
from eve_db.services.base import BaseDiscordActionService
from eve_db.selectors.pilot import pilot_by_discord_id_exists_selector


class UpdatePilotService(BaseDiscordActionService):

	def __init__(self, discord_id: str, name: str, corporation: str, tech_level: str):
		self._discord_id = discord_id
		self._name = name
		self._corporation = corporation
		self._tech_level = tech_level

	def execute(self) -> str:
		if not pilot_by_discord_id_exists_selector(discord_id=self._discord_id):
			return 'You not registered'


		form = PilotForm({
			'discord_id': self._discord_id,
			'name': self._name,
			'corporation': self._corporation,
			'tech_level': self._tech_level,
		})
		if not form.is_valid():
			return form.errors

		Pilot.objects.filter(
			discord_id=self._discord_id
		)\
			.update(
				name=self._name,
				corporation=self._corporation,
				tech_level=self._tech_level,
				)
		return 'Pilot profile update'.__str__()
