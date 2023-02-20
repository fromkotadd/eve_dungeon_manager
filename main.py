import sqlite3


class Person:
	def __init__(self):
		# Представление карточки пилота для юзера
		self.pilot_name = None
		self.ship_type = None
		self.first_skill = None
		self.second_skill = None
		self.implant_lvl = None
		self.fit_class = None
		self.pilot_rating = None
		# данные для БД
		self.count_entry = None
		self.id = None

	def pilot_card_builder(self):
		return {
			'pilot_name': self.pilot_name,
			'ship_type': self.ship_type,
			'first_skill': self.first_skill,
			'second_skill': self.second_skill,
			'implant_lvl': self.implant_lvl,
			'fit_class': self.fit_class,
			'pilot_rating': self.pilot_rating,
			'count_entry': self.count_entry,
			'id': self.id,
		}
	def __str__(self):
		return f"pilot name: {self.pilot_name}, ship type: {self.ship_type}, first skill: {self.first_skill}," \
				f" second skill: {self.second_skill}, implant lvl: {self.implant_lvl},fit class: {self.fit_class}," \
				f" pilot rating: {self.pilot_rating}, count entry: {self.count_entry}, id: {self.id},"


class PersonBuilder:
	def __init__(self, person=Person()):
		self.person = person

	@property
	def for_initialization(self):
		return PersonBuilderForInitialization(self.person)

	@property
	def for_download_to_database(self):
		return PersonBuilderFromDb(self.person)

	def build(self):
		return self.person


class PersonBuilderForInitialization(PersonBuilder):
	def __init__(self, person=Person()):
		super().__init__(person)

	def pilot_name(self, pilot_name):
		self.person.pilot_name = pilot_name
		return self

	def ship_type(self, ship_type):
		self.person.ship_type = ship_type
		return self

	def first_skill(self, first_skill):
		self.person.first_skill = first_skill
		return self

	def second_skill(self, second_skill):
		self.person.second_skill = second_skill
		return self

	def implant_lvl(self, implant_lvl):
		self.person.implant_lvl = implant_lvl
		return self

	def fit_class(self, fit_class):
		self.person.fit_class = fit_class
		return self

	def pilot_rating(self, pilot_rating):
		self.person.pilot_rating = pilot_rating
		return self


class PersonBuilderFromDb(PersonBuilder):
	def __init__(self, person):
		super().__init__(person)

	def count_entry(self, count_entry):
		self.person.count_entry = count_entry
		return self

	def id(self, id):
		self.person.id = id
		return self


class DownloadAdaptor:
	def __init__(self, pilot_card_dist):
		self.pilot_card_dist = pilot_card_dist
		self.table_cell_name = []
		self.cell_content = []

	def adaptor(self):
		for key, value in self.pilot_card_dist.items():
			self.table_cell_name.append(key)
			self.cell_content.append(value)
		return self.table_cell_name[:-1], self.cell_content[:-1]

	def __str__(self):
		return self.pilot_card_dist


class DbManager:

	@staticmethod
	def db_connect(db_name='pilot.db'):
		sqlite_connection = sqlite3.connect(db_name)
		cursor = sqlite_connection.cursor()
		return sqlite_connection, cursor

	@staticmethod
	def damp_to_db(adaptor_lst, db_name):
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
	def load_from_db(pilot_id, db_name):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sqlite_select_query = """SELECT * from pilot_card where id = ?"""
		cursor.execute(sqlite_select_query, (pilot_id,))
		print("Чтение одной строки \n")
		record = cursor.fetchone()
		cursor.close()
		return record

	@staticmethod
	def table_update(table_name, pilot_id, changes, db_name):
		sqlite_connection, cursor = DbManager.db_connect(db_name)
		sql_update_query = f"""Update pilot_card set {table_name} = ? where id = ?"""
		cursor.execute(sql_update_query, (changes, pilot_id))
		sqlite_connection.commit()
		print("Запись успешно обновлена")
		cursor.close()


if __name__ == "__main__":
	pb = PersonBuilder()
	person = pb.for_initialization.pilot_name('Riva25 Wilson').ship_type('bk').first_skill('553').second_skill('553')\
		.implant_lvl('10').fit_class('c').pilot_rating('mid').for_download_to_database.count_entry('10').build()
	card = person.pilot_card_builder()
	pilot_card_to_dump = DownloadAdaptor(card).adaptor()
	DbManager().damp_to_db(pilot_card_to_dump, 'pilot.db')

