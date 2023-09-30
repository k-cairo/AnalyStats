import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get Just Upcoming Matches"

    # E5
    def handle(self, *args, **options):
        # Get Upcoming Fixtures
        call_command(command_name="E5Parser", str_error_context="Get Upcoming Matches")

