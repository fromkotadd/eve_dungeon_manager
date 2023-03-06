from django.forms import ModelForm
from eve_db.models import PilotShip


class ShipForm(ModelForm):
	class Meta:
		model = PilotShip
		fields = ['pilot', 'ship_name', 'core_color', 'core_lvl', 'fit_grade']
