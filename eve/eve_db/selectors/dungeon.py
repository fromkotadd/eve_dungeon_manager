from eve_db.models import Dungeon
from eve_db.choices import Dungeons


def dungeon_by_name_selector(dungeon_name: Dungeons) -> Dungeon:
	return Dungeon.objects.filter(dungeon_name=dungeon_name).first()
