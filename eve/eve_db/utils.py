from datetime import datetime

from asgiref.sync import sync_to_async
from django.utils import timezone
from table2ascii import table2ascii, PresetStyle, Alignment


def get_week_beginning() -> datetime:
	now = timezone.now()
	return now - timezone.timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second)


@sync_to_async()
def table_create(pilots_cards, pilot_ships_func):
	body = []
	for pilots_card in pilots_cards:
		pilot_ships = pilot_ships_func(discord_id=int(pilots_card['discord_id']))
		ship_name = []
		core_color = []
		core_lvl = []
		fit_grade = []
		for ships in pilot_ships:
			ship_name.append(ships['ship_name'])
			core_color.append(ships['core_color'])
			core_lvl.append(ships['core_lvl'])
			fit_grade.append(ships['fit_grade'])
		value = [
				pilots_card['name'],
				pilots_card['corporation'],
				pilots_card['tech_level'],
				pilots_card['dungeon_visits_amount'],
				',\n'.join(ship_name),
				',\n'.join(core_color),
				',\n'.join([f'{x}' for x in core_lvl]),
				',\n'.join(fit_grade)
			]
		body.append(value)
	output = table2ascii(
			header=[
				'ИМЯ',
				'ТЕГ',
				'УР.',
				'ПРОЙДЕНО.РАЗ',
				'КОРАБЛИ',
				'ЦВ.ЯДР',
				'УР.ЯДР',
				'ФИТ'
					],
			body=body,
			style=PresetStyle.ascii,
			alignments=Alignment.LEFT
		)
	return output


@sync_to_async()
def table_create_(pilots_cards, pilot_ships_func):
	body = []
	for pilots_card in pilots_cards:
		pilot_ships = pilot_ships_func(discord_id=int(pilots_card['discord_id']))
		ship_name = []
		core_color = []
		core_lvl = []
		fit_grade = []
		for ships in pilot_ships:
			ship_name.append(ships['ship_name'])
			core_color.append(ships['core_color'])
			core_lvl.append(ships['core_lvl'])
			fit_grade.append(ships['fit_grade'])
		value = [
				pilots_card['name'],
				pilots_card['corporation'],
				pilots_card['tech_level'],
				pilots_card['dungeon_visits_amount'],
				',\n'.join(ship_name),
				',\n'.join(core_color),
				',\n'.join([f'{x}' for x in core_lvl]),
				',\n'.join(fit_grade)
			]
		body.append(value)
	output = table2ascii(
			header=[
				'ИМЯ',
				'ТЕГ',
				'УР.',
				'ПРОЙДЕНО.РАЗ',
				'КОРАБЛИ',
				'ЦВ.ЯДР',
				'УР.ЯДР',
				'ФИТ'
					],
			body=body,
			style=PresetStyle.ascii,
			alignments=Alignment.LEFT
		)
	return output
