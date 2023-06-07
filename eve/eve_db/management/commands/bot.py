from django.core.management.base import BaseCommand
from eve_db.discord_api.discord_bot import run


class Command(BaseCommand):
    help = "Run a discord bot"

    def handle(self, *args, **options):
        run()