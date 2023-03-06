from django.db.models import QuerySet

from eve_db.models import PilotShip, Pilot
from eve_db.choices import ShipNames


def pilot_ship_by_name_selector(pilot: Pilot, name: ShipNames) -> QuerySet[PilotShip]:
	return pilot.pilot_ships.filter(ship_name=name)
