import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Person:
	""" Person DTO. """
	pilot_name: str
	ship_type: str
	first_skill: str
	second_skill: str
	implant_lvl: str
	fit_class: str
	pilot_rating: str
	count_entry: Optional[int] = 10
	id: Optional[int] = None

	def __str__(self):
		return f"pilot name: {self.pilot_name}, ship type: {self.ship_type}, first skill: {self.first_skill}," \
			   f" second skill: {self.second_skill}, implant lvl: {self.implant_lvl}, fit class: {self.fit_class}," \
			   f" pilot rating: {self.pilot_rating}, count entry: {self.count_entry}, id: {self.id}"


class DownloadAdaptor:
	def __init__(self, pilot_card_dist):
		self.pilot_card_dist = pilot_card_dist

	def adaptor(self):
		self.pilot_card_dist.pop('id', None)
		return list(self.pilot_card_dist.keys()), list(self.pilot_card_dist.values())

	def __str__(self):
		return self.pilot_card_dist


class DbManager:

	@staticmethod
	def db_connect(db_name):
		sqlite_connection = sqlite3.connect(db_name)
		cursor = sqlite_connection.cursor()
		return sqlite_connection, cursor

	@staticmethod
	def damp_to_db(adaptor_lst, db_name='pilot.db'):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		param_names = [f"p{i}" for i in range(len(adaptor_lst[1]))]
		sqlite_insert_with_param = f"""INSERT INTO pilot_card
									({', '.join(adaptor_lst[0])})
								VALUES ({", ".join(":" + p for p in param_names)});"""

		cursor.execute(sqlite_insert_with_param, adaptor_lst[1])
		sqlite_connection.commit()
		cursor.close()

	@staticmethod
	def load_from_db(pilot_id, db_name='pilot.db'):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sqlite_select_query = """SELECT * from pilot_card where id = ?"""
		cursor.execute(sqlite_select_query, (pilot_id,))
		record = cursor.fetchone()
		cursor.close()
		return record

	@staticmethod
	def table_update(table_name, pilot_id, changes, db_name='pilot.db'):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sql_update_query = f"""Update pilot_card set {table_name} = ? where id = ?"""
		cursor.execute(sql_update_query, (changes, pilot_id))
		sqlite_connection.commit()
		cursor.close()


if __name__ == "__main__":
	# person = Person(
	# 	pilot_name='Riva25 Wilson',
	# 	ship_type='bk',
	# 	first_skill='553',
	# 	second_skill='553',
	# 	implant_lvl='10',
	# 	fit_class='c',
	# 	pilot_rating='mid'
	# )
	# pilot_card_to_dump = DownloadAdaptor(asdict(person)).adaptor()
	# DbManager().damp_to_db(pilot_card_to_dump, 'pilot.db')
	# DbManager.table_update('ship_type', '12', 'bh, bk', 'pilot.db')
	s = DbManager.load_from_db(pilot_id='12', db_name='pilot.db')
	print(s)
	person = Person(*s)
	print(person)
