from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 0"

    # E5
    def handle(self, *args, **options):
        # Get Leagues
        call_command(command_name="E5Parser", str_error_context="Get Leagues")

        # Get Seasons
        call_command(command_name="E5Parser", str_error_context="Get Seasons")

        # Get League Table Iframes
        call_command(command_name="E5Parser", str_endpoint="/", str_error_context="Get League Table Iframes",
                     int_iframe_length=1, str_save_message="League Table Iframe", str_class="E5LeagueTableIframe")

        # Get Teams
        call_command(command_name="E5Parser", str_error_context="Get Teams")
