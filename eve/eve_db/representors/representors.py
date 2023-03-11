from typing import Optional

from django.db.models import QuerySet
from django.forms.models import model_to_dict


from eve_db.selectors.pilot import pilots_for_first_dungeon
from eve_db.models import Pilot


def foo() -> Optional[str]:
	sample_of_pilots = pilots_for_first_dungeon().values()

	for p in sample_of_pilots:
		pilot = Pilot.objects.get(discord_id=p['discord_id'])
		pilot_ships = pilot.pilot_ships.get()
		pilot_skills = pilot.skills.filter().values()
		pilot_implant = pilot.implants.filter().values()
		# print(Pilot.objects.filter(discord_id=p['discord_id']), pilot_ships, pilot_skills, pilot_implant)

		s = model_to_dict(pilot_ships, fields=None, exclude=None)
		print(s)
		print(type(s))

