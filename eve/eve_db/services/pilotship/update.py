from eve_db.forms.pilotship import ShipForm
from eve_db.selectors.pilot import pilot_by_discord_id_selector
from eve_db.selectors.pilotship import pilot_ship_by_name_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import ShipNames, CoreColors, FitGrade


class UpdatePilotShipService(BaseDiscordActionService):

	def __init__(self, discord_id: str, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
		self._discord_id = discord_id
		self._pilot = pilot_by_discord_id_selector(discord_id)
		self._ship_name = ShipNames(ship_name)
		self._core_color = CoreColors(core_color)
		self._core_lvl = core_lvl
		self._fit_grade = FitGrade(fit_grade)

	def execute(self) -> str:
		ship = pilot_ship_by_name_selector(pilot=self._pilot, name=self._ship_name).first()
		if not ship:
			return f'You not added ship {self._ship_name}.'
		form = ShipForm({
			'pilot': self._pilot,
			'ship_name': self._ship_name,
			'core_color': self._core_color,
			'core_lvl': self._core_lvl,
			'fit_grade': self._fit_grade,
		})
		if not form.is_valid():
			return form.errors

		self._pilot.pilot_ships\
			.filter(
				ship_name=self._ship_name
			)\
			.update(
				core_color=self._core_color,
				core_lvl=self._core_lvl,
				fit_grade=self._fit_grade
			)
		return f'Ship {self._ship_name} update'
