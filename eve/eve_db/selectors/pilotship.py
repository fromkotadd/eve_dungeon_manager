from django.db.models import QuerySet, Q

from eve_db.models import PilotShip, Pilot
from eve_db.choices import ShipNames


def pilot_ship_by_name_selector(pilot: Pilot, name: ShipNames) -> QuerySet[PilotShip]:
	return pilot.pilot_ships.filter(ship_name=name)


def ships_for_first_dungeon(discord_id: str) -> list:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	required_ships = [
		ShipNames.VINDICATOR,
		ShipNames.BHAALGORN,
		ShipNames.NIGHTMARE
	]
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name__in=required_ships)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)


def ships_for_second_dungeon(discord_id: str) -> list:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	required_ships = [
		ShipNames.APOCALYPSE_STRIKER,
		ShipNames.APOCALYPSE_NAVY_ISSUE,
		ShipNames.NIGHTMARE,
		ShipNames.MEGATHRON_STRIKER,
		ShipNames.MEGATHRON_NAVY_ISSUE
	]
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name__in=required_ships)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)


def ships_for_third_dungeon(discord_id: str) -> list:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	required_ships = [
		ShipNames.NAGLFAR,
		ShipNames.PHOENIX,
		ShipNames.MOROS,
		ShipNames.REVELATION,
		ShipNames.THANATOS,
		ShipNames.ARCHON,
		ShipNames.CHIMERA,
		ShipNames.NIDHOUGGUR
	]
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name__in=required_ships)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)


def ships_for_fourth_dungeon(discord_id: str) -> list:
	pilot_cards = Pilot.objects.get(discord_id=discord_id)
	required_ships = [
		ShipNames.NAGLFAR,
		ShipNames.PHOENIX,
		ShipNames.MOROS,
		ShipNames.REVELATION
	]
	pilot_ship = pilot_cards.pilot_ships.\
		filter(
			Q(ship_name__in=required_ships)
		)\
		.values(
			'ship_name',
			'core_color',
			'core_lvl',
			'fit_grade'
		)
	return list(pilot_ship)
