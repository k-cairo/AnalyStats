from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 2"

    # E5
    def handle(self, *args, **options):
        # Get Over 2.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-2-5-goals/",
                     str_error_context="Get Over 2.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 2.5 Goals Iframe", str_class="E5Over25GoalsIframe")

        # Parse Over 2.5 Goals Iframes
        call_command(command_name="E5ParseOver25GoalsIframes")

        # Get Over 3.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-3-5-goals/",
                     str_error_context="Get Over 3.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 3.5 Goals Iframe", str_class="E5Over35GoalsIframe")

        # Parse Over 3.5 Goals Iframes
        call_command(command_name="E5ParseOver35GoalsIframes")

        # Get Win Draw Loss Percentage Iframes
        call_command(command_name="E5Parser", str_endpoint="wdl/",
                     str_error_context="Get Win Draw Loss Percentage Iframes", int_iframe_length=1,
                     str_save_message="Win Draw Loss Percentage Iframe", str_class="E5WinDrawLossPercentageIframe")

        # Parse Win Draw Loss Percentage Iframes
        call_command(command_name="E5ParseWinDrawLossPercentageIframes")
