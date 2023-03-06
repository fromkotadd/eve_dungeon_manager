from django.forms import ModelForm
from eve_db.models import DungeonPilotVisit

class VisitForm(ModelForm):
	class Meta:
		model = DungeonPilotVisit
		fields = ['dungeon', 'pilot']