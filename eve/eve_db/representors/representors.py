from asgiref.sync import sync_to_async

from eve_db.selectors.pilot import pilots_for_first_dungeon
from eve_db.services.pilot.create import CreatePilotService


@sync_to_async()
def pilot_info_table_queryset(pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2) -> list:
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

@sync_to_async()
def registration_pilot(discord_id: str,  name: str, corporation: str, tech_level: str, pilot_rating: str):
		return str(CreatePilotService.load(
		discord_id=str(discord_id),
		name=str(name),
		corporation=str(corporation),
		tech_level=int(tech_level),
		pilot_rating=str(pilot_rating)
		))