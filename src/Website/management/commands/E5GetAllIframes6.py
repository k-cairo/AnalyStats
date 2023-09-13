from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes 6"

    # E5
    def handle(self, *args, **options):
        # Get Win Loss Margin Iframes
        call_command(command_name="E5Parser", str_endpoint="winloss/",
                     str_error_context="Get Win Loss Margin Iframes", int_iframe_length=2,
                     str_save_message="Win Loss Margin Iframe", str_class="E5WinLossMarginIframe")

        # Parse Win Loss Margin Iframes
        call_command(command_name="E5ParseWinLossMarginIframes")

        # Get Scored First Iframes
        call_command(command_name="E5Parser", str_endpoint="sf/",
                     str_error_context="Get Scored First Iframes", int_iframe_length=2,
                     str_save_message="Scored First Iframe", str_class="E5ScoredFirstIframe")

        # Parse Scored First Iframes
        call_command(command_name="E5ParseScoredFirstIframes")

        # Get Average First Goal Time Iframes
        call_command(command_name="E5Parser", str_endpoint="agt/",
                     str_error_context="Get Average First Goal Time Iframes", int_iframe_length=1,
                     str_save_message="Average First Goal Time Iframe", str_class="E5Average1stGoalTimeIframe")

        # Parse Average First Goal Time Iframes
        call_command(command_name="E5ParseAverageFirstGoalTimeIframes")
