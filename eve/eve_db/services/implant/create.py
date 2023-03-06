from eve_db.forms.implant import ImplantForm
from eve_db.selectors.implant import implant_by_name_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import ImplantNames

class CreateImplantService(BaseDiscordActionService):

	def __init__(self, implant_name: str, implant_level: str):
		self._implant_name = ImplantNames(implant_name)
		self._implant_level = implant_level



	def execute(self) -> str:
		implant = implant_by_name_selector(pilot=self._pilot, name=self._implant_name).first()
		if implant:
			return f'You already added implant {self._implant_name}.'

		form = ImplantForm({
			'pilot': self._pilot,
			'implant_name': self._implant_name,
			'implant_level': self._implant_level

		})
		if not form.is_valid():
			return form.errors

		form.save()
		return f'Implant {self._implant_name} added'


