from django.db.models import QuerySet

from eve_db.models import Implant, Pilot
from eve_db.choices import ImplantNames


def implant_by_name_selector(pilot: Pilot, name: ImplantNames) -> QuerySet[Implant]:
	return pilot.implants.filter(implant_name=name)
