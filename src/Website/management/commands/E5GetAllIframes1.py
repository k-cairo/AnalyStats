from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 1"

    # E5
    def handle(self, *args, **options):
        # Parse League Table Iframes
        call_command(command_name="E5ParseLeagueTableIframes")

        # Get BTTS Iframes
        call_command(command_name="E5Parser", str_endpoint="btts/", str_error_context="Get BTTS Iframes",
                     int_iframe_length=5, str_save_message="BTTS Iframe", str_class="E5BttsIframes")

        # Parse BTTS Iframes
        call_command(command_name="E5ParseBttsIframes")

        # Get Over 0.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-0-5-goals/",
                     str_error_context="Get Over 0.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 0.5 Goals Iframe", str_class="E5Over05GoalsIframe")

        # Parse Over 0.5 Goals Iframes
        call_command(command_name="E5ParseOver05GoalsIframes")

        # Get Over 1.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-1-5-goals/",
                     str_error_context="Get Over 1.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 1.5 Goals Iframe", str_class="E5Over15GoalsIframe")

        # Parse Over 1.5 Goals Iframes
        call_command(command_name="E5ParseOver15GoalsIframes")
