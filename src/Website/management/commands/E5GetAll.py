import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Get All"

    # E5
    def handle(self, *args, **options):
        # Get Day of today
        today = datetime.datetime.now().weekday()

        ################################################### ALL DAYS ###################################################
        # Get Leagues
        call_command(command_name="E5Parser", str_error_context="Get Leagues")

        # Get Seasons
        call_command(command_name="E5Parser", str_error_context="Get Seasons")

        # Get League Table Iframes
        call_command(command_name="E5Parser", str_endpoint="/", str_error_context="Get League Table Iframes",
                     int_iframe_length=1, str_save_message="League Table Iframe", str_class="E5LeagueTableIframe")

        # Get Teams
        call_command(command_name="E5Parser", str_error_context="Get Teams")

        #################################################### MONDAY ####################################################
        if today == 0:
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

            # Get Over 2.5 Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="over-2-5-goals/",
                         str_error_context="Get Over 2.5 Goals Iframes", int_iframe_length=4,
                         str_save_message="Over 2.5 Goals Iframe", str_class="E5Over25GoalsIframe")

            # Parse Over 2.5 Goals Iframes
            call_command(command_name="E5ParseOver25GoalsIframes")

            # Get Average Team Goal Iframes
            call_command(command_name="E5Parser", str_endpoint="amr/",
                         str_error_context="Get Average Team Goal Iframes", int_iframe_length=1,
                         str_save_message="Average Team Goal Iframe", str_class="E5AverageTeamGoalsIframe")

            # Parse Average Team Goal Iframes
            call_command(command_name="E5ParseAverageTeamGoalsIframes")

        ################################################### TUESDAY ####################################################
        elif today == 1:  # 17
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

            # Get 1st 2nd Half Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="1st-2nd-half-goals/",
                         str_error_context="Get 1st 2nd Half Goals Iframes", int_iframe_length=3,
                         str_save_message="1st 2nd Half Goals Iframe", str_class="E51st2ndHalfGoalsIframe")

            # Parse 1st 2nd Half Goals Iframes
            call_command(command_name="E5Parse1st2ndHalfGoalsIframes")

            # Get Average First Goal Time Iframes
            call_command(command_name="E5Parser", str_endpoint="agt/",
                         str_error_context="Get Average First Goal Time Iframes", int_iframe_length=1,
                         str_save_message="Average First Goal Time Iframe", str_class="E5Average1stGoalTimeIframe")

            # Parse Average First Goal Time Iframes
            call_command(command_name="E5ParseAverageFirstGoalTimeIframes")

            # Get Early Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="early/",
                         str_error_context="Get Early Goals Iframes", int_iframe_length=1,
                         str_save_message="Early Goals Iframe", str_class="E5EarlyGoalsIframe")

            # Parse Early Goals Iframes
            call_command(command_name="E5ParseEarlyGoalsIframes")

        ################################################## WEDNESDAY ###################################################
        elif today == 2:  # 10
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

            # Get Late Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="late/",
                         str_error_context="Get Late Goals Iframes", int_iframe_length=1,
                         str_save_message="Late Goals Iframe", str_class="E5LateGoalsIframe")

            # Parse Late Goals Iframes
            call_command(command_name="E5ParseLateGoalsIframes")

        ################################################### THURSDAY ###################################################
        elif today == 3:
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

            # Get Over 2.5 Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="over-2-5-goals/",
                         str_error_context="Get Over 2.5 Goals Iframes", int_iframe_length=4,
                         str_save_message="Over 2.5 Goals Iframe", str_class="E5Over25GoalsIframe")

            # Parse Over 2.5 Goals Iframes
            call_command(command_name="E5ParseOver25GoalsIframes")

            # Get Average Team Goal Iframes
            call_command(command_name="E5Parser", str_endpoint="amr/",
                         str_error_context="Get Average Team Goal Iframes", int_iframe_length=1,
                         str_save_message="Average Team Goal Iframe", str_class="E5AverageTeamGoalsIframe")

            # Parse Average Team Goal Iframes
            call_command(command_name="E5ParseAverageTeamGoalsIframes")

        #################################################### FRIDAY ####################################################
        elif today == 4:
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

            # Get 1st 2nd Half Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="1st-2nd-half-goals/",
                         str_error_context="Get 1st 2nd Half Goals Iframes", int_iframe_length=3,
                         str_save_message="1st 2nd Half Goals Iframe", str_class="E51st2ndHalfGoalsIframe")

            # Parse 1st 2nd Half Goals Iframes
            call_command(command_name="E5Parse1st2ndHalfGoalsIframes")

            # Get Average First Goal Time Iframes
            call_command(command_name="E5Parser", str_endpoint="agt/",
                         str_error_context="Get Average First Goal Time Iframes", int_iframe_length=1,
                         str_save_message="Average First Goal Time Iframe", str_class="E5Average1stGoalTimeIframe")

            # Parse Average First Goal Time Iframes
            call_command(command_name="E5ParseAverageFirstGoalTimeIframes")

            # Get Early Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="early/",
                         str_error_context="Get Early Goals Iframes", int_iframe_length=1,
                         str_save_message="Early Goals Iframe", str_class="E5EarlyGoalsIframe")

            # Parse Early Goals Iframes
            call_command(command_name="E5ParseEarlyGoalsIframes")

        ################################################### SATURDAY ###################################################
        elif today == 5:
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

            # Get Late Goals Iframes
            call_command(command_name="E5Parser", str_endpoint="late/",
                         str_error_context="Get Late Goals Iframes", int_iframe_length=1,
                         str_save_message="Late Goals Iframe", str_class="E5LateGoalsIframe")

            # Parse Late Goals Iframes
            call_command(command_name="E5ParseLateGoalsIframes")
