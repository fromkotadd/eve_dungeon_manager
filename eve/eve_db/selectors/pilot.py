from typing import Optional

from django.db.models import QuerySet, Count, Q, Avg


from eve_db.models import Pilot
from eve_db.choices import SkillNames, Dungeons, ShipNames, ImplantNames
from eve_db.utils import get_week_beginning


def pilot_by_discord_id_selector(discord_id: str) -> Optional[Pilot]:
	return Pilot.objects\
		.filter(discord_id=discord_id)\
		.first()


def pilot_by_discord_id_exists_selector(discord_id: str) -> bool:
	return Pilot.objects\
		.filter(discord_id=discord_id)\
		.exists()


def pilots_for_first_dungeon() -> QuerySet[Pilot]:
	pilots_amount = 20
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.I
	required_skills = [SkillNames.LARGE_RAILGUN, SkillNames.BATTLESHIP_COMMAND, SkillNames.SMALL_LASER]
	return Pilot.objects\
		.annotate(
			dungeon_visits_amount=Count(
				'visits',
				filter=Q(
					visits__date_created__gte=week_beginning,
					visits__dungeon__dungeon_name=dungeon_name
				),
				distinct=True
			),
			required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills)),
			skills_rating=Avg(
				'skills__level',
				filter=Q(skills__name__in=required_skills)
			)
		)\
		.filter(
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			pilot_ships__ship_name__in=[ShipNames.VINDICATOR]
		)\
		.order_by('-skills_rating')[:pilots_amount]


def foo() -> QuerySet[Pilot]:
	pilots_amount = 20
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.I
	required_skills = [
		SkillNames.BATTLESHIP_COMMAND,
		SkillNames.BATTLESHIP_DEFENSE_UPGRADE,
		SkillNames.BATTLESHIP_ENGINEERING
	]
	return Pilot.objects\
		.annotate(
			dungeon_visits_amount=Count(
				'visits',
				filter=Q(
					visits__date_created__gte=week_beginning,
					visits__dungeon__dungeon_name=dungeon_name
				),
				distinct=True
			),
			required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills)),
			skills_rating=Avg(
				'skills__level',
				filter=Q(skills__name__in=required_skills)
			),
		)\
		.filter(
			Q(implants__implant_level__gte=15),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL])
			| Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.VINDICATOR]) | Q(pilot_ships__ship_name__in=[ShipNames.BHAAlGORN]),
			Q(skills__name__in=[SkillNames.LARGE_RAILGUN]) | Q(skills__name__in=[SkillNames.LARGE_LASER]),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
		)\
		.order_by('-skills_rating')[:pilots_amount]
