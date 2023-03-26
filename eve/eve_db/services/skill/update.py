from eve_db.forms.skill import SkillForm
from eve_db.selectors.pilot import pilot_by_discord_id_selector
from eve_db.selectors.skill import pilot_skills_by_name_selector
from eve_db.services.base import BaseDiscordActionService
from eve_db.choices import SkillNames, SkillLevels


class UpdateSkillService(BaseDiscordActionService):

	SKILL_LEVEL_MAP = {
		'4-4': 1,
		'4-5-3': 2,
		'5-5-4': 3,
	}

	def __init__(self, discord_id: str, name: str, level: str):
		self._discord_id = discord_id
		self._pilot = pilot_by_discord_id_selector(discord_id)
		self._name = SkillNames(name)
		self._level = SkillLevels(level)

	def execute(self) -> str:
		existing_skill = pilot_skills_by_name_selector(pilot=self._pilot, name=self._name).first()
		if not existing_skill:
			return f'You not added skill {self._name}.'

		form = SkillForm({
			'pilot': self._pilot,
			'name': self._name,
			'level': self.SKILL_LEVEL_MAP[self._level]
		})
		if not form.is_valid():
			return form.errors

		self._pilot.skills\
			.filter(
				name=self._name
			)\
			.update(
				name=self._name,
				level=self.SKILL_LEVEL_MAP[self._level]
			)
		return f'Skill {self._name} update'
