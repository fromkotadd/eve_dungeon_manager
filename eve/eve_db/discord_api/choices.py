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