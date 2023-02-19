import sqlite3


class Person:
	def __init__(self, **kwargs):
		self.pilot_name = kwargs.get('pilot_name', 'None')
		self.ship_type = kwargs.get('ship_type', 'None')
		self.first_skill = kwargs.get('first_skill', 'None')
		self.second_skill = kwargs.get('second_skill', 'None')
		self.implant_lvl = kwargs.get('implant_lvl', 'None')
		self.count_entry = kwargs.get('count_entry', 'None')
		self.id = kwargs.get('id', 'None')
		self.fit_class = kwargs.get('fit_class', 'None')
		self.pilot_rating = kwargs.get('pilot_rating', 'None')

	def pilot_card_builder(self):
		return {
			'pilot_name': self.pilot_name,
			'ship_type': self.ship_type,
			'first_skill': self.first_skill,
			'second_skill': self.second_skill,
			'implant_lvl': self.implant_lvl,
			# 'count_entry': self.count_entry,
			# 'id': self.id,
			'fit_class': self.fit_class,
			'pilot_rating': self.pilot_rating
		}

	def __str__(self):
		return f"pilot name: {self.pilot_name}, ship type: {self.ship_type}, first skill: {self.first_skill}," \
			   f" second skill: {self.second_skill}, implant lvl: {self.implant_lvl}, count entry: {self.count_entry}," \
			   f" id: {self.id}, fit class: {self.fit_class}, pilot rating: {self.pilot_rating}"


class DownloadAdaptor:
	def __init__(self, pilot_card_dist):
		self.pilot_card_dist = pilot_card_dist
		self.table_cell_name = []
		self.cell_content = []

	def adaptor(self):
		for key, value in self.pilot_card_dist.items():
			self.table_cell_name.append(key)
			self.cell_content.append(value)
		return self.table_cell_name, self.cell_content

	def __str__(self):
		return self.pilot_card_dist


class DbManager:

	@staticmethod
	def db_connect(db_name='pilot.db'):
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
		print("Переменные Python успешно вставлены в таблицу pilot")
		cursor.close()

	@staticmethod
	def load_from_db(pilot_id, db_name='pilot.db'):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sqlite_select_query = """SELECT * from pilot_card where id = ?"""
		cursor.execute(sqlite_select_query, (pilot_id, ))
		print("Чтение одной строки \n")
		record = cursor.fetchone()
		cursor.close()
		return record

	@staticmethod
	def table_update(table_name, pilot_id, changes, db_name='pilot.db'):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sql_update_query = f"""Update pilot_card set {table_name} = ? where id = ?"""
		cursor.execute(sql_update_query, (changes, pilot_id))
		sqlite_connection.commit()
		print("Запись успешно обновлена")
		cursor.close()


if __name__ == "__main__":
	# p = Person(pilot_name='bobi', ship_type='бш', second_skill='554', first_skill='333', pilot_rating='low', implant_lvl='10',
	# 			fit_class='c')
	# card = p.pilot_card_builder()
	# print(p.pilot_card_builder())
	# print(p)
	# s = DownloadAdaptor(card).adaptor()
	# DbManager.damp_to_db(s, 'pilot.db')
	# DbManager.table_update(table_name='implant_lvl', changes=7, pilot_id=1)
	DbManager.load_from_db(32)
