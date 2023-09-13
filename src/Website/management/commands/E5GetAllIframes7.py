from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 7"

    # E5
    def handle(self, *args, **options):
        # Get Average Team Goal Iframes
        call_command(command_name="E5Parser", str_endpoint="amr/",
                     str_error_context="Get Average Team Goal Iframes", int_iframe_length=1,
                     str_save_message="Average Team Goal Iframe", str_class="E5AverageTeamGoalsIframe")

        # Parse Average Team Goal Iframes
        call_command(command_name="E5ParseAverageTeamGoalsIframes")

        # Get Early Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="early/",
                     str_error_context="Get Early Goals Iframes", int_iframe_length=1,
                     str_save_message="Early Goals Iframe", str_class="E5EarlyGoalsIframe")

        # Parse Early Goals Iframes
        call_command(command_name="E5ParseEarlyGoalsIframes")

        # Get Late Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="late/",
                     str_error_context="Get Late Goals Iframes", int_iframe_length=1,
                     str_save_message="Late Goals Iframe", str_class="E5LateGoalsIframe")

        # Parse Late Goals Iframes
        call_command(command_name="E5ParseLateGoalsIframes")
