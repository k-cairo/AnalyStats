from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 3"

    # E5
    def handle(self, *args, **options):
        # Get Corners Iframes
        call_command(command_name="E5Parser", str_endpoint="corners/", str_error_context="Get Corners Iframes",
                     int_iframe_length=9, str_save_message="Corners Iframe", str_class="E5CornersIframes")

        # Parse Corners Iframes
        call_command(command_name="E5ParseCornersIframes")

        # Get Cards Iframes
        call_command(command_name="E5Parser", str_endpoint="cards/", str_error_context="Get Cards Iframes",
                     int_iframe_length=4, str_save_message="Cards Iframe", str_class="E5CardsIframes")

        # Parse Cards Iframes
        call_command(command_name="E5ParseCardsIframes")

        # Get Half Time Full Time Iframes
        call_command(command_name="E5Parser", str_endpoint="half-time-full-time/",
                     str_error_context="Get Half Time Full Time Iframes", int_iframe_length=1,
                     str_save_message="Half Time Full Time Iframe", str_class="E5HalfTimeFullTimeIframe")

        # Parse Half Time Full Time Iframes
        call_command(command_name="E5ParseHalfTimeFullTimeIframes")
