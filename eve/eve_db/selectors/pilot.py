from typing import Optional
from itertools import chain

from django.db.models import QuerySet, Count, Q, Avg

from eve_db.models import Pilot
from eve_db.choices import SkillNames, Dungeons, ShipNames, ImplantNames
from eve_db.utils import get_week_beginning


def pilot_by_discord_id_selector(discord_id: str) -> Optional[Pilot]:
	return Pilot.objects \
		.filter(discord_id=discord_id) \
		.first()


def pilot_by_discord_id_exists_selector(discord_id: str) -> bool:
	return Pilot.objects \
		.filter(discord_id=discord_id) \
		.exists()

def _pilot_card_delete(pilot_id: str):
	Pilot.objects.filter(discord_id=pilot_id).delete()


def pilots_for_first_dungeon(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
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
		required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills), distinct=True),
		skills_rating=Avg(
			'skills__level',
			filter=Q(skills__name__in=required_skills)
		),
	) \
			   .filter(
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL]),
			Q(pilot_ships__ship_name__in=[ShipNames.VINDICATOR]),
			Q(skills__name__in=[SkillNames.LARGE_RAILGUN], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.BHAALGORN]),
			Q(skills__name__in=[SkillNames.LARGE_LASER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(pilot_ships__ship_name__in=[ShipNames.NIGHTMARE]),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
	) \
			   .order_by('-skills_rating').distinct()[:pilots_amount]


def pilots_for_second_dungeon(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.II
	required_skills = [
		SkillNames.BATTLESHIP_COMMAND,
		SkillNames.BATTLESHIP_DEFENSE_UPGRADE,
		SkillNames.BATTLESHIP_ENGINEERING
	]
	return Pilot.objects \
			   .annotate(
		dungeon_visits_amount=Count(
			'visits',
			filter=Q(
				visits__date_created__gte=week_beginning,
				visits__dungeon__dungeon_name=dungeon_name
			),
			distinct=True
		),
		required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills), distinct=True),
		skills_rating=Avg(
			'skills__level',
			filter=Q(skills__name__in=required_skills)
		),
	) \
			   .filter(
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.APOCALYPSE_STRIKER]),
			Q(skills__name__in=[SkillNames.LARGE_LASER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.APOCALYPSE_NAVY_ISSUE]),
			Q(skills__name__in=[SkillNames.LARGE_LASER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(pilot_ships__ship_name__in=[ShipNames.NIGHTMARE]),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL]),
			Q(pilot_ships__ship_name__in=[ShipNames.MEGATHRON_STRIKER]),
			Q(skills__name__in=[SkillNames.LARGE_RAILGUN], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL]),
			Q(pilot_ships__ship_name__in=[ShipNames.MEGATHRON_NAVY_ISSUE]),
			Q(skills__name__in=[SkillNames.LARGE_RAILGUN], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
	) \
			.order_by('-skills_rating').distinct()[:pilots_amount]

def pilots_for_third_dungeon(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
	a = pilots_for_third_dungeon_dread(pilots_amount, implant_level, skills_rating, gun_rating)
	b = pilots_for_third_dungeon_carrier(pilots_amount, implant_level, skills_rating, gun_rating)
	result_list = list(chain(a.values(), b.values()))
	id_by_dict = {i['id']: i for i in result_list}
	clear_result_list = list(id_by_dict.values())

	return clear_result_list[:pilots_amount]

def pilots_for_third_dungeon_dread(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.III
	required_skills_dread = [
		SkillNames.DREADNOUGHT_COMMAND,
		SkillNames.DREADNOUGHT_DEFENSE_UPGRADE,
		SkillNames.DREADNOUGHT_ENGINEERING
	]
	return Pilot.objects \
			   .annotate(
		dungeon_visits_amount=Count(
			'visits',
			filter=Q(
				visits__date_created__gte=week_beginning,
				visits__dungeon__dungeon_name=dungeon_name
			),
			distinct=True
		),
		required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills_dread), distinct=True),
		skills_rating=Avg(
			'skills__level',
			filter=Q(skills__name__in=required_skills_dread)
		),
	) \
			   .filter(
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.REVELATION]),
			Q(skills__name__in=[SkillNames.CAPITAL_LASER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL]),
			Q(pilot_ships__ship_name__in=[ShipNames.MOROS]),
			Q(skills__name__in=[SkillNames.CAPITAL_RAILGUN], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.BARRAGE_REPRESSION]),
			Q(pilot_ships__ship_name__in=[ShipNames.NAGLFAR]),
			Q(skills__name__in=[SkillNames.CAPITAL_CANNON], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.WARHEAD_CHARGE]),
			Q(pilot_ships__ship_name__in=[ShipNames.PHOENIX]),
			Q(skills__name__in=[SkillNames.CAPITAL_MISSILE], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
	) \
			   .order_by('-skills_rating').distinct()[:pilots_amount]


def pilots_for_third_dungeon_carrier(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.III
	required_skills_carrier = [
		SkillNames.CARRIER_COMMAND,
		SkillNames.CARRIER_DEFENSE_UPGRADE,
		SkillNames.CARRIER_ENGINEERING
	]
	return Pilot.objects \
			   .annotate(
		dungeon_visits_amount=Count(
			'visits',
			filter=Q(
				visits__date_created__gte=week_beginning,
				visits__dungeon__dungeon_name=dungeon_name
			),
			distinct=True
		),
		required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills_carrier), distinct=True),
		skills_rating=Avg(
			'skills__level',
			filter=Q(skills__name__in=required_skills_carrier)
		),
	) \
			   .filter(
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.BOMBARD_TACTICS]),
			Q(pilot_ships__ship_name__in=[
				ShipNames.NIDHOUGGUR,
				ShipNames.CHIMERA,
				ShipNames.ARCHON,
				ShipNames.THANATOS
			]),
			Q(skills__name__in=[SkillNames.FIGHTER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_carrier),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
	) \
			   .order_by('-skills_rating').distinct()[:pilots_amount]


def pilots_for_fourth_dungeon(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> QuerySet[Pilot]:
	week_visits_limit = 10
	week_beginning = get_week_beginning()
	dungeon_name = Dungeons.IV
	required_skills_dread = [
		SkillNames.DREADNOUGHT_COMMAND,
		SkillNames.DREADNOUGHT_DEFENSE_UPGRADE,
		SkillNames.DREADNOUGHT_ENGINEERING
	]
	return Pilot.objects \
			   .annotate(
		dungeon_visits_amount=Count(
			'visits',
			filter=Q(
				visits__date_created__gte=week_beginning,
				visits__dungeon__dungeon_name=dungeon_name
			),
			distinct=True
		),
		required_skills_amount=Count('skills', filter=Q(skills__name__in=required_skills_dread), distinct=True),
		skills_rating=Avg(
			'skills__level',
			filter=Q(skills__name__in=required_skills_dread)
		),
	) \
			   .filter(
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.FOCUSED_CRYSTAL]),
			Q(pilot_ships__ship_name__in=[ShipNames.REVELATION]),
			Q(skills__name__in=[SkillNames.CAPITAL_LASER], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.HIGH_POWER_COIL]),
			Q(pilot_ships__ship_name__in=[ShipNames.MOROS]),
			Q(skills__name__in=[SkillNames.CAPITAL_RAILGUN], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.BARRAGE_REPRESSION]),
			Q(pilot_ships__ship_name__in=[ShipNames.NAGLFAR]),
			Q(skills__name__in=[SkillNames.CAPITAL_CANNON], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
		|
		Q(
			Q(implants__implant_level__gte=implant_level),
			Q(implants__implant_name__in=[ImplantNames.WARHEAD_CHARGE]),
			Q(pilot_ships__ship_name__in=[ShipNames.PHOENIX]),
			Q(skills__name__in=[SkillNames.CAPITAL_MISSILE], skills__level__gte=gun_rating),
			required_skills_amount=len(required_skills_dread),
			dungeon_visits_amount__lt=week_visits_limit,
			skills_rating__gte=skills_rating
		)
	) \
			   .order_by('-skills_rating').distinct()[:pilots_amount]
