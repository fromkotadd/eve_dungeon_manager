from eve_db.forms.dungeon import DungeonForm
from eve_db.selectors.dungeon import dungeon_by_name_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import Dungeons


class CreateDungeonService(BaseDiscordActionService):

	def __init__(self, dungeon_name: str):
		self._dungeon_name = Dungeons(dungeon_name)

	def execute(self) -> str:
		dungeon = dungeon_by_name_selector(dungeon_name=self._dungeon_name)
		if dungeon:
			return f'You already added dungeon {self._dungeon_name}.'

		form = DungeonForm({
			'dungeon_name': self._dungeon_name
		})
		if not form.is_valid():
			return form.errors

		form.save()
		return f'Dungeon {self._dungeon_name} added'
