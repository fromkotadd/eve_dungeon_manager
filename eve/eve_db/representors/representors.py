from typing import Optional

from django.db.models import QuerySet

from eve_db.selectors.pilot import pilots_for_first_dungeon
from eve_db.models import Skill, PilotShip, Implant, Pilot


def foo() -> Optional[str]:
	sample_of_pilots = pilots_for_first_dungeon().values()

	# # print(sample_of_pilots[0])
	# print(sample_of_pilots[0]['discord_id'])
	# p = Pilot.objects.get(discord_id=sample_of_pilots[0]['discord_id'])
	# print(p.implants.filter().values())
	# print(p)
	pilot = Pilot.objects.get(discord_id=sample_of_pilots[0]['discord_id'])
	pilot_ships = pilot.pilot_ships.filter().values()
	pilot_skills = pilot.skills.filter().values()


