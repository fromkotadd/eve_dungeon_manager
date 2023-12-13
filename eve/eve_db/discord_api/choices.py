class CoreColorsChoices:

	def __init__(self):
		self.core_colors = {
			1: 'GREEN',
			2: 'BLUE',
			3: 'VIOLET',
			4: 'GOLD',
			5: 'NONE',
		}

	def get_core_colors(self):
		return self.core_colors

	def __str__(self):
		return self.core_colors

class FitGradeChoices:

	def __init__(self):
		self.fit_grade = {
			1: 'C',
			2: 'B',
			3: 'A',
			4: 'X',
		}

	def get_fit_graded(self):
		return self.fit_grade

class ImplantChoices:

	def __init__(self):
		self.implant = {
			'LARGE RAILGUN': 'HIGH POWER COIL',
			'CAPITAL RAILGUN': 'HIGH POWER COIL',
			'LARGE LASER': 'FOCUSED CRYSTAL',
			'CAPITAL LASER': 'FOCUSED CRYSTAL',
			'LARGE CANNON': 'BARRAGE REPRESSION',
			'CAPITAL CANNON': 'BARRAGE REPRESSION',
			'LARGE MISSILE': 'WARHEAD CHARGE',
			'CAPITAL MISSILE': 'WARHEAD CHARGE',
			'FIGHTER' : 'BOMBARD TACTICS'
		}

	def get_impant(self):
		return self.implant

class GunType:
	def __init__(self):
		self.ship_gun_typ_dict = {
			'BHAAlGORN': 'LARGE LASER',
			'NIGHTMARE': 'LARGE LASER',
			'APOCALYPSE NAVY ISSUE': 'LARGE LASER',
			'APOCALYPSE STRIKER': 'LARGE LASER',
			'MEGATHRON NAVY ISSUE': 'LARGE RAILGUN',
			'MEGATHRON STRIKER': 'LARGE RAILGUN',
			'VINDICATOR': 'LARGE RAILGUN',
			'PHOENIX': 'CAPITAL MISSILE',
			'NAGLFAR': 'CAPITAL CANNON',
			'MOROS': 'CAPITAL RAILGUN',
			'REVELATION': 'CAPITAL LASER',
			'THANATOS': 'FIGHTER',
			'ARCHON': 'FIGHTER',
			'CHIMERA': 'FIGHTER',
			'NIDHOUGGUR': 'FIGHTER',
		}

class ShipForDungeonChoices:
	def __init__(self):
		self.ship_for_dungeon = {
			'1': {
				1: 'VINDICATOR',
				2: 'BHAAlGORN',
				3: 'NIGHTMARE',
			},
			'2': {
				1: 'APOCALYPSE STRIKER',
				2: 'APOCALYPSE NAVY ISSUE',
				3: 'NIGHTMARE',
				4: 'MEGATHRON STRIKER',
				5: 'MEGATHRON NAVY ISSUE',
			},
			'3': {
				1: 'NAGLFAR',
				2: 'PHOENIX',
				3: 'MOROS',
				4: 'REVELATION',
				5: 'THANATOS',
				6: 'ARCHON',
				7: 'CHIMERA',
				8: 'NIDHOUGGUR',
			},
			'4': {
				1: 'NAGLFAR',
				2: 'PHOENIX',
				3: 'MOROS',
				4: 'REVELATION',
			}
		}

	def get_ship_for_dungeon(self):
		return self.ship_for_dungeon

class PilotSkill:
	def __init__(self):
		self.skill_map = {
			'1': '4-4',
			'2': '4-5-3',
			'3': '5-5-4',
			}
		self.ship_gun_typ_dict = {
			'BHAALGORN': 'LARGE LASER',
			'NIGHTMARE': 'LARGE LASER',
			'APOCALYPSE NAVY ISSUE': 'LARGE LASER',
			'APOCALYPSE STRIKER': 'LARGE LASER',
			'MEGATHRON NAVY ISSUE': 'LARGE RAILGUN',
			'MEGATHRON STRIKER': 'LARGE RAILGUN',
			'VINDICATOR': 'LARGE RAILGUN',
			'PHOENIX': 'CAPITAL MISSILE',
			'NAGLFAR': 'CAPITAL CANNON',
			'MOROS': 'CAPITAL RAILGUN',
			'REVELATION': 'CAPITAL LASER',
			'THANATOS': 'FIGHTER',
			'ARCHON': 'FIGHTER',
			'CHIMERA': 'FIGHTER',
			'NIDHOUGGUR': 'FIGHTER',
		}
		self.ships_type_dict = {
			'APOCALYPSE STRIKER': 'battleship',
			'APOCALYPSE NAVY ISSUE': 'battleship',
			'MEGATHRON STRIKER': 'battleship',
			'MEGATHRON NAVY ISSUE': 'battleship',
			'VINDICATOR': 'battleship',
			'BHAAlGORN': 'battleship',
			'NIGHTMARE': 'battleship',
			'PHOENIX': 'dreadnought',
			'NAGLFAR': 'dreadnought',
			'MOROS': 'dreadnought',
			'REVELATION': 'dreadnought',
			'THANATOS': 'carrier',
			'ARCHON': 'carrier',
			'CHIMERA': 'carrier',
			'NIDHOUGGUR': 'carrier',
		}

	def get_skill_map(self):
		return self.skill_map

	def get_ship_gun_typ_dict(self):
		return self.ship_gun_typ_dict

	def get_ships_type_dict(self):
		return self.ships_type_dict

