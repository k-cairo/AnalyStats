from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get all iframes"

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

        # Get BTTS Iframes
        call_command(command_name="E5Parser", str_endpoint="btts/", str_error_context="Get BTTS Iframes",
                     int_iframe_length=5, str_save_message="BTTS Iframe", str_class="E5BttsIframes")

        # Get Over 0.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-0-5-goals/",
                     str_error_context="Get Over 0.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 0.5 Goals Iframe", str_class="E5Over05GoalsIframe")

        # Get Over 1.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-1-5-goals/",
                     str_error_context="Get Over 1.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 1.5 Goals Iframe", str_class="E5Over15GoalsIframe")

        # Get Over 2.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-2-5-goals/",
                     str_error_context="Get Over 2.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 2.5 Goals Iframe", str_class="E5Over25GoalsIframe")

        # Get Over 3.5 Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="over-3-5-goals/",
                     str_error_context="Get Over 3.5 Goals Iframes", int_iframe_length=4,
                     str_save_message="Over 3.5 Goals Iframe", str_class="E5Over35GoalsIframe")

        # Get Win Draw Loss Percentage Iframes
        call_command(command_name="E5Parser", str_endpoint="wdl/",
                     str_error_context="Get Win Draw Loss Percentage Iframes", int_iframe_length=1,
                     str_save_message="Win Draw Loss Percentage Iframe", str_class="E5WinDrawLossPercentageIframe")

        # Get Corners Iframes
        call_command(command_name="E5Parser", str_endpoint="corners/", str_error_context="Get Corners Iframes",
                     int_iframe_length=9, str_save_message="Corners Iframe", str_class="E5CornersIframes")

        # Get Cards Iframes
        call_command(command_name="E5Parser", str_endpoint="cards/", str_error_context="Get Cards Iframes",
                     int_iframe_length=4, str_save_message="Cards Iframe", str_class="E5CardsIframes")

        # Get Half Time Full Time Iframes
        call_command(command_name="E5Parser", str_endpoint="half-time-full-time/",
                     str_error_context="Get Half Time Full Time Iframes", int_iframe_length=1,
                     str_save_message="Half Time Full Time Iframe", str_class="E5HalfTimeFullTimeIframe")

        # Get Scored Both Halves Iframes
        call_command(command_name="E5Parser", str_endpoint="sbh/",
                     str_error_context="Get Scored Both Halves Iframes", int_iframe_length=2,
                     str_save_message="Scored Both Halves Iframe", str_class="E5ScoredBothHalfIframes")

        # Get Won Both Halves Iframes
        call_command(command_name="E5Parser", str_endpoint="wbh/",
                     str_error_context="Get Won Both Halves Iframes", int_iframe_length=2,
                     str_save_message="Won Both Halves Iframe", str_class="E5WonBothHalfIframes")

        # Get 1st 2nd Half Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="1st-2nd-half-goals/",
                     str_error_context="Get 1st 2nd Half Goals Iframes", int_iframe_length=3,
                     str_save_message="1st 2nd Half Goals Iframe", str_class="E51st2ndHalfGoalsIframe")

        # Get Rescued Points Iframes
        call_command(command_name="E5Parser", str_endpoint="rescued-points/",
                     str_error_context="Get Rescued Points Iframes", int_iframe_length=1,
                     str_save_message="Rescued Points Iframe", str_class="E5RescuedPointsIframe")

        # Get Clean Sheet Iframes
        call_command(command_name="E5Parser", str_endpoint="clean-sheets/",
                     str_error_context="Get Clean Sheet Iframes", int_iframe_length=2,
                     str_save_message="Clean Sheet Iframe", str_class="E5CleanSheetIframe")

        # Get Won To Nil Iframes
        call_command(command_name="E5Parser", str_endpoint="wtn/",
                     str_error_context="Get Won To Nil Iframes", int_iframe_length=2,
                     str_save_message="Won To Nil Iframe", str_class="E5WonToNilIframe")

        # Get Win Loss Margin Iframes
        call_command(command_name="E5Parser", str_endpoint="winloss/",
                     str_error_context="Get Win Loss Margin Iframes", int_iframe_length=2,
                     str_save_message="Win Loss Margin Iframe", str_class="E5WinLossMarginIframe")

        # Get Scored First Iframes
        call_command(command_name="E5Parser", str_endpoint="sf/",
                     str_error_context="Get Scored First Iframes", int_iframe_length=2,
                     str_save_message="Scored First Iframe", str_class="E5ScoredFirstIframe")

        # Get Average First Goal Time Iframes
        call_command(command_name="E5Parser", str_endpoint="agt/",
                     str_error_context="Get Average First Goal Time Iframes", int_iframe_length=1,
                     str_save_message="Average First Goal Time Iframe", str_class="E5Average1stGoalTimeIframe")

        # Get Average Team Goal Iframes
        call_command(command_name="E5Parser", str_endpoint="amr/",
                     str_error_context="Get Average Team Goal Iframes", int_iframe_length=1,
                     str_save_message="Average Team Goal Iframe", str_class="E5AverageTeamGoalsIframe")

        # Get Early Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="early/",
                     str_error_context="Get Early Goals Iframes", int_iframe_length=1,
                     str_save_message="Early Goals Iframe", str_class="E5EarlyGoalsIframe")

        # Get Late Goals Iframes
        call_command(command_name="E5Parser", str_endpoint="late/",
                     str_error_context="Get Late Goals Iframes", int_iframe_length=1,
                     str_save_message="Late Goals Iframe", str_class="E5LateGoalsIframe")
