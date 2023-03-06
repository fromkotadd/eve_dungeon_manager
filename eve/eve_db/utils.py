from datetime import datetime
from django.utils import timezone


def get_week_beginning() -> datetime:
	now = timezone.now()
	return now - timezone.timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second)
