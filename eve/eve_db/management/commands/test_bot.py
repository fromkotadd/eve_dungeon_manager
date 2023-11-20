from django.core.management.base import BaseCommand
from eve_db.discord_api.test import run


class Command(BaseCommand):
    #python manage.py bot
    help = "Run a discord bot"

    def handle(self, *args, **options):
        run()