from asgiref.sync import sync_to_async

from eve_db.selectors.pilot import pilots_for_first_dungeon
from eve_db.services.pilot.create import CreatePilotService
from eve_db.services.pilotship.create import CreatePilotShipService
from eve_db.services.implant.create import CreateImplantService
from eve_db.services.skill.create import CreateSkillService
from eve_db.services.dungeon_pilot_visit.create import CreateDungeonVisitService
from eve_db.forms.pilot import PilotForm
from eve_db.forms.pilotship import ShipForm
from eve_db.models import Pilot
from eve_db.selectors.pilot import pilot_by_discord_id_selector


@sync_to_async()
def pilot_card_add(discord_id: str, name: str, corporation: str, tech_level: str, pilot_rating: str):
	return str(
		CreatePilotService.load(
			discord_id=str(discord_id),
			name=str(name),
			corporation=str(corporation),
			tech_level=int(tech_level),
			pilot_rating=str(pilot_rating)
		)
	)


@sync_to_async()
def pilot_card_upd(discord_id: str, name: str, corporation: str, tech_level: str, pilot_rating: str):
	form = PilotForm({
		'discord_id': discord_id,
		'name': name,
		'corporation': corporation,
		'tech_level': tech_level,
		'pilot_rating': pilot_rating,
	})
	if not form.is_valid():
		return form.errors

	Pilot.objects\
		.filter(
			discord_id=discord_id
		)\
		.update(
			name=name,
			corporation=corporation,
			tech_level=tech_level,
			pilot_rating=pilot_rating
		)
	return 'Pilot card update'


@sync_to_async()
def pilot_ship_add(discord_id: str, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	return str(
		CreatePilotShipService.load(
			discord_id=discord_id,
			ship_name=ship_name,
			core_color=core_color,
			core_lvl=core_lvl,
			fit_grade=fit_grade
		)
	)


@sync_to_async()
def pilot_ship_upd(discord_id: str, ship_name: str, core_color: str, core_lvl: str, fit_grade: str):
	pilot = pilot_by_discord_id_selector(discord_id)
	if not pilot:
		return 'Pilot not found. Please register pilot'
	form = ShipForm({
			'pilot': pilot,
			'ship_name': ship_name,
			'core_color': core_color,
			'core_lvl': core_lvl,
			'fit_grade': fit_grade,
		})
	if not form.is_valid():
		return form.errors

	pilot.pilot_ships\
		.filter(
			ship_name=ship_name
		)\
		.update(
			core_color=core_color,
			core_lvl=core_lvl,
			fit_grade=fit_grade
		)
	return 'Pilot ship card update'


@sync_to_async()
def pilot_implant_add(discord_id: str, implant_name: str, implant_level: str):
	return str(
		CreateImplantService.load(
			discord_id=discord_id,
			implant_name=implant_name,
			implant_level=implant_level
		)
	)


@sync_to_async()
def pilot_skill_add(discord_id: str, name: str, level: str):
	return str(
		CreateSkillService.load(
			discord_id=discord_id,
			name=name,
			level=level
		)
	)


@sync_to_async()
def dungeon_visit_add(discord_id: str, dungeon_name: str):
	return str(
		CreateDungeonVisitService.load(
			discord_id=discord_id,
			dungeon_name=int(dungeon_name)
		)
	)


@sync_to_async()
def first(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> list:
	sample_of_pilots = pilots_for_first_dungeon(pilots_amount, implant_level, skills_rating, gun_rating) \
		.values(
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	return list(sample_of_pilots)
