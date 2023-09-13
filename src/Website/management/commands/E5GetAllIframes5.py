from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 5"

    # E5
    def handle(self, *args, **options):
        # Get Rescued Points Iframes
        call_command(command_name="E5Parser", str_endpoint="rescued-points/",
                     str_error_context="Get Rescued Points Iframes", int_iframe_length=1,
                     str_save_message="Rescued Points Iframe", str_class="E5RescuedPointsIframe")

        # Parse Rescued Points Iframes
        call_command(command_name="E5ParseRescuedPointsIframes")

        # Get Clean Sheet Iframes
        call_command(command_name="E5Parser", str_endpoint="clean-sheets/",
                     str_error_context="Get Clean Sheet Iframes", int_iframe_length=2,
                     str_save_message="Clean Sheet Iframe", str_class="E5CleanSheetIframe")

        # Parse Clean Sheet Iframes
        call_command(command_name="E5ParseCleanSheetsIframes")

        # Get Won To Nil Iframes
        call_command(command_name="E5Parser", str_endpoint="wtn/",
                     str_error_context="Get Won To Nil Iframes", int_iframe_length=2,
                     str_save_message="Won To Nil Iframe", str_class="E5WonToNilIframe")

        # Parse Won To Nil Iframes
        call_command(command_name="E5ParseWonToNilIframes")
