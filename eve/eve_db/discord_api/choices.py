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