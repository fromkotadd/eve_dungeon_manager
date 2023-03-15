from asgiref.sync import sync_to_async

from eve_db.selectors.pilot import pilots_for_first_dungeon


@sync_to_async()
def pilot_info_table_queryset() -> list:
	sample_of_pilots = pilots_for_first_dungeon() \
		.values(
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	return list(sample_of_pilots)
