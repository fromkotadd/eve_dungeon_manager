from asgiref.sync import sync_to_async
from django.db.models import QuerySet, Q

from eve_db.models import PilotShip, Pilot
from eve_db.choices import ShipNames



def pilot_ship_by_name_selector(pilot: Pilot, name: ShipNames) -> QuerySet[PilotShip]:
	return pilot.pilot_ships.filter(ship_name=name)


@sync_to_async()
def ships_for_first_dungeon(discord_id: str) -> QuerySet:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name=ShipNames.VINDICATOR) | Q(ship_name=ShipNames.BHAAlGORN) | Q(ship_name=ShipNames.NIGHTMARE)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)


@sync_to_async()
def ships_for_second_dungeon(discord_id: str) -> QuerySet:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name=ShipNames.APOCALYPSE_STRIKER) | Q(ship_name=ShipNames.NIGHTMARE)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)

