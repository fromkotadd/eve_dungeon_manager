from eve_db.forms.implant import ImplantForm
from eve_db.selectors.implant import implant_by_name_selector
from eve_db.selectors.pilot import pilot_by_discord_id_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import ImplantNames


class UpdateImplantService(BaseDiscordActionService):

	def __init__(self, discord_id: str, implant_name: str, implant_level: str):
		self._discord_id = discord_id
		self._pilot = pilot_by_discord_id_selector(discord_id)
		self._implant_name = ImplantNames(implant_name)
		self._implant_level = implant_level

	def execute(self) -> str:
		implant = implant_by_name_selector(pilot=self._pilot, name=self._implant_name).first()
		if not implant:
			return f'You not added implant {self._implant_name}.'

		form = ImplantForm({
			'pilot': self._pilot,
			'implant_name': self._implant_name,
			'implant_level': self._implant_level

		})
		if not form.is_valid():
			return form.errors

		self._pilot.implants\
			.filter(
				implant_name=self._implant_name
			)\
			.update(
				implant_name=self._implant_name,
				implant_level=self._implant_level
			)

		return f'Implant {self._implant_name} update'
