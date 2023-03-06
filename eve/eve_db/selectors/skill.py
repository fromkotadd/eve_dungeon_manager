from django.db.models import QuerySet

from eve_db.models import Skill, Pilot
from eve_db.choices import SkillNames


def pilot_skills_by_name_selector(pilot: Pilot, name: SkillNames) -> QuerySet[Skill]:
	return pilot.skills.filter(name=name)
