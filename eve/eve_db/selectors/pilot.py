from typing import Optional

from django.db.models import QuerySet, Subquery, OuterRef, Count, Q, Avg


from eve_db.models import Pilot
from eve_db.choices import SkillNames, SkillLevels, Dungeons, ShipNames
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
	required_skills = [SkillNames.LARGE_RAILGUN]
	skills_query = Q()
	for skill in required_skills:
		skills_query &= Q(skills__name=skill)
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
			skills_rating=Avg(
				'skills__level',
				filter=Q(skills__name__in=required_skills)
			)
		)\
		.filter(
			skills_query,
			dungeon_visits_amount__lt=week_visits_limit,
			pilot_ships__ship_name__in=[ShipNames.VINDICATOR]
		)\
		.order_by('-skills_rating')[:pilots_amount]


def foo() -> QuerySet[Pilot]:
	pilots_amount = 20
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.I
	required_skills = [SkillNames.LARGE_RAILGUN]
	skills_query = Q()
	for skill in required_skills:
		skills_query &= Q(skills__name=skill)
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
			skills_rating=Avg(
				'skills__level',
				filter=Q(skills__name__in=required_skills)
			)
		)\
		.filter(
			skills_query,
			dungeon_visits_amount__lt=week_visits_limit,
			pilot_ships__ship_name__in=[ShipNames.VINDICATOR]
		)\
		.order_by('-skills_rating')[:pilots_amount]

# SkillNames.LARGE_RAILGUN,
# SkillNames.LARGE_LASER,
# SkillNames.BATTLESHIP_COMMAND,
# SkillNames.BATTLESHIP_DEFENSE_UPGRADE,
# SkillNames.BATTLESHIP_ENGINEERING