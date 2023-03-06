from django.forms import ModelForm
from eve_db.models import Dungeon


class DungeonForm(ModelForm):
	class Meta:
		model = Dungeon
		fields = ['dungeon_name',]