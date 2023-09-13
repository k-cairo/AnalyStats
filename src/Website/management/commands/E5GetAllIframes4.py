from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 4"

    # E5
    def handle(self, *args, **options):
        # Get Scored Both Halves Iframes
        call_command(command_name="E5Parser", str_endpoint="sbh/",
                     str_error_context="Get Scored Both Halves Iframes", int_iframe_length=2,
                     str_save_message="Scored Both Halves Iframe", str_class="E5ScoredBothHalfIframes")

        # Parse Scored Both Halves Iframes
        call_command(command_name="E5ParseScoredBothHalvesIframes")

        # Get Won Both Halves Iframes
        call_command(command_name="E5Parser", str_endpoint="wbh/",
                     str_error_context="Get Won Both Halves Iframes", int_iframe_length=2,
                     str_save_message="Won Both Halves Iframe", str_class="E5WonBothHalfIframes")

        # Parse Won Both Halves Iframes
        call_command(command_name="E5ParseWonBothHalvesIframes")

        # Get 1st 2nd Half Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="1st-2nd-half-goals/",
                     str_error_context="Get 1st 2nd Half Goals Iframes", int_iframe_length=3,
                     str_save_message="1st 2nd Half Goals Iframe", str_class="E51st2ndHalfGoalsIframe")

        # Parse 1st 2nd Half Goals Iframes
        call_command(command_name="E5Parse1st2ndHalfGoalsIframes")
