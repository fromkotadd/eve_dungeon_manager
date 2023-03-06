from django.forms import ModelForm
from eve_db.models import Skill


class SkillForm(ModelForm):
	class Meta:
		model = Skill
		fields = ['pilot', 'name', 'level']
