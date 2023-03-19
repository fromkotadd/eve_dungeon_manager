from django.forms import ModelForm
from eve_db.models import Implant


class ImplantForm(ModelForm):
	class Meta:
		model = Implant
		fields = ['pilot', 'implant_name', 'implant_level']
