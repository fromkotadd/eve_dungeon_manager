from prettytable import PrettyTable

from eve_db.selectors.pilot import pilots_for_first_dungeon


def pilot_info_table() -> PrettyTable:
	sample_of_pilots = pilots_for_first_dungeon()\
		.values_list(
		'name',
		'corporation',
		'tech_level',
		'pilot_rating',
		'dungeon_visits_amount',
		'skills_rating'
	)
	table = PrettyTable([
			'name',
			'corporation',
			'tech_level',
			'pilot_rating',
			'dungeon_visits_amount',
			'skills_rating'
		])
	for pilot in sample_of_pilots:
		table.add_row(
			pilot
		)
	return table