from abc import ABC, abstractmethod
from typing import Optional

from eve_db.models import Pilot
from eve_db.selectors.pilot import pilot_by_discord_id_selector


class BaseDiscordActionService(ABC):

	_pilot: Pilot
	_discord_id: str

	@abstractmethod
	def execute(self) -> str:
		pass

	@classmethod
	def load(cls, *args, discord_id: str, **kwargs) -> str:
		try:
			service = cls(**kwargs)
			service._set_discord_id(discord_id=discord_id)
			validation_error = service._validate_pilot(discord_id=discord_id)

			if validation_error:
				return validation_error
			return service.execute()
		except Exception as e:
			return str(e)

	def _validate_pilot(self, discord_id: str) -> Optional[str]:
		pilot = pilot_by_discord_id_selector(discord_id=discord_id)
		if not pilot:
			return 'Pilot not found. Please register pilot'

		self._pilot = pilot

	def _set_discord_id(self, discord_id: str):
		self._discord_id = discord_id