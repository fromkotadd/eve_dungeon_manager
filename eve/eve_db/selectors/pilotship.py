from django.db.models import QuerySet

from eve_db.models import PilotShip, Pilot
from eve_db.choices import ShipNames
from eve_db.selectors.pilot import pilots_for_first_dungeon


def pilot_ship_by_name_selector(pilot: Pilot, name: ShipNames) -> QuerySet[PilotShip]:
	return pilot.pilot_ships.filter(ship_name=name)


def ships_for_first_dungeon() -> QuerySet:
	pilot_cards = pilots_for_first_dungeon()
	for pilot_card in pilot_cards:
		# print(pilot_card.pilot_ships.filter().values("ship_name", 'core_color', 'core_lvl', 'fit_grade'))
		yield pilot_card.pilot_ships.filter().values("ship_name", 'core_color', 'core_lvl', 'fit_grade')
