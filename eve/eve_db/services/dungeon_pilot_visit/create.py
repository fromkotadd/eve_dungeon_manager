from eve_db.forms.dungeon_pilot_visit import VisitForm
from eve_db.selectors.dungeon import dungeon_by_name_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import Dungeons

class CreateDungeonVisitService(BaseDiscordActionService):

	def __init__(self, dungeon_name: str):
		self._dungeon_name = Dungeons(dungeon_name)

	def execute(self) -> str:
		dungeon = dungeon_by_name_selector(dungeon_name=self._dungeon_name)
		if not dungeon:
			return f'Dungeon {self._dungeon_name} does not exist'

		form = VisitForm({
			'dungeon': dungeon,
			'pilot': self._pilot
		})
		if not form.is_valid():
			return form.errors

		form.save()
		return f'Your visit to dungeon {self._dungeon_name} added'


