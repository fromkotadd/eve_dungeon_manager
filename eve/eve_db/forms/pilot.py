from django.forms import ModelForm
from eve_db.models import Pilot


class PilotForm(ModelForm):
	class Meta:
		model = Pilot
		fields = ['discord_id', 'name', 'corporation', 'tech_level', 'pilot_rating']
