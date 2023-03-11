from typing import Optional

from django.db.models import QuerySet

from eve_db.selectors.pilot import pilots_for_first_dungeon
from eve_db.models import Skill, PilotShip, Implant, Pilot


def foo() -> Optional[str]:
	sample_of_pilots = pilots_for_first_dungeon().values()

	for p in sample_of_pilots:
		pilot = Pilot.objects.get(discord_id=p['discord_id'])
		pilot_ships = pilot.pilot_ships.filter().values()
		pilot_skills = pilot.skills.filter().values()
		pilot_implant = pilot.implants.filter().values()
		print(Pilot.objects.filter(discord_id=p['discord_id']), pilot_ships, pilot_skills, pilot_implant)


