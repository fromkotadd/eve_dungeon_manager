from asgiref.sync import sync_to_async

from eve_db.selectors.pilot import pilots_for_first_dungeon, pilots_for_second_dungeon, pilots_for_third_dungeon_dread,\
	pilots_for_fourth_dungeon, pilots_for_third_dungeon_carrier
from eve_db.services.implant.update import UpdateImplantService
from eve_db.services.pilot.create import CreatePilotService
from eve_db.services.pilot.update import UpdatePilotService
from eve_db.services.pilotship.create import CreatePilotShipService
from eve_db.services.implant.create import CreateImplantService
from eve_db.services.pilotship.update import UpdatePilotShipService
from eve_db.services.skill.create import CreateSkillService
from eve_db.services.dungeon_pilot_visit.create import CreateDungeonVisitService
from eve_db.services.skill.update import UpdateSkillService


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
	return UpdatePilotService(
			discord_id=discord_id,
			name=name,
			corporation=corporation,
			tech_level=tech_level,
			pilot_rating=pilot_rating
		)\
			.execute()


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
	return UpdatePilotShipService(
		discord_id=discord_id,
		ship_name=ship_name,
		core_color=core_color,
		core_lvl=core_lvl,
		fit_grade=fit_grade
	)\
		.execute()


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
def pilot_implant_upd(discord_id: str, implant_name: str, implant_level: str):
	return UpdateImplantService(
		discord_id=discord_id,
		implant_name=implant_name,
		implant_level=implant_level
	)\
		.execute()


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
def pilot_skill_upd(discord_id: str, name: str, level: str):
	return UpdateSkillService(
		discord_id=discord_id,
		name=name,
		level=level
	)\
		.execute()


@sync_to_async()
def dungeon_visit_add(discord_id: str, dungeon_name: str):
	return str(
		CreateDungeonVisitService.load(
			discord_id=discord_id,
			dungeon_name=int(dungeon_name)
		)
	)


@sync_to_async()
def first(pilots_amount: int=20, implant_level: int=15, skills_rating: str='4-5-3', gun_rating: str='4-5-3') -> list:
	skills_ratings = skill_level_map(skills_rating)
	gun_ratings = gun_level_map(gun_rating)
	sample_of_pilots = pilots_for_first_dungeon(pilots_amount, implant_level, skills_ratings, gun_ratings) \
		.values(
		'discord_id',
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	return list(sample_of_pilots)


@sync_to_async()
def second(pilots_amount: int=20, implant_level: int=15, skills_rating: str='4-5-3', gun_rating: str='4-5-3') -> list:
	skills_ratings = skill_level_map(skills_rating)
	gun_ratings = gun_level_map(gun_rating)
	sample_of_pilots = pilots_for_second_dungeon(pilots_amount, implant_level, skills_ratings, gun_ratings) \
		.values(
		'discord_id',
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	return list(sample_of_pilots)


@sync_to_async()
def third(pilots_amount: int=20, implant_level: int=15, skills_rating: str='4-5-3', gun_rating: str='4-5-3') -> list:
	skills_ratings = skill_level_map(skills_rating)
	gun_ratings = gun_level_map(gun_rating)
	sample_of_pilots_dread = pilots_for_third_dungeon_dread(pilots_amount, implant_level, skills_ratings, gun_ratings).\
		values(
			'discord_id',
			'name',
			'corporation',
			'tech_level',
			'pilot_rating',
			'dungeon_visits_amount',
			'skills_rating'
		)
	sample_of_pilots_carrier = pilots_for_third_dungeon_carrier(pilots_amount, implant_level, skills_ratings, gun_ratings).\
		values(
			'discord_id',
			'name',
			'corporation',
			'tech_level',
			'pilot_rating',
			'dungeon_visits_amount',
			'skills_rating'
		)
	return list(sample_of_pilots_dread), list(sample_of_pilots_carrier)


@sync_to_async()
def fourth(pilots_amount: int=20, implant_level: int=15, skills_rating: str='4-5-3', gun_rating: str='4-5-3') -> list:
	skills_ratings = skill_level_map(skills_rating)
	gun_ratings = gun_level_map(gun_rating)
	sample_of_pilots = pilots_for_fourth_dungeon(pilots_amount, implant_level, skills_ratings, gun_ratings) \
		.values(
		'discord_id',
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	return list(sample_of_pilots)


def skill_level_map(abs_skill_level: str) -> int:
	SKILL_LEVEL_MAP = {
			'4-4': 1,
			'4-5-3': 2,
			'5-5-4': 3,
		}
	return SKILL_LEVEL_MAP.get(abs_skill_level, "Invalid skill level")

def gun_level_map(abs_gun_level: str) -> int:
	GUN_LEVEL_MAP = {
			'4-4': 1,
			'4-5-3': 2,
			'5-5-4': 3,
		}
	return GUN_LEVEL_MAP.get(abs_gun_level, "Invalid gun level")