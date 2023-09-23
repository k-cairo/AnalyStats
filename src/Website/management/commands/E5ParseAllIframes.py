from django.core.management import call_command
from django.core.management.base import BaseCommand


# E5
class Command(BaseCommand):
    help = "Parse all iframes"

    # E5
    def handle(self, *args, **options):
        # Get Leagues
        call_command(command_name="E5Parser", str_error_context="Get Leagues")

        # Get Seasons
        call_command(command_name="E5Parser", str_error_context="Get Seasons")

        # Get Teams
        call_command(command_name="E5Parser", str_error_context="Get Teams")

        # Parse League Table Iframes
        call_command(command_name="E5ParseLeagueTableIframes")

        # Parse BTTS Iframes
        call_command(command_name="E5ParseBttsIframes")

        # Parse Over 0.5 Goals Iframes
        call_command(command_name="E5ParseOver05GoalsIframes")

        # Parse Over 1.5 Goals Iframes
        call_command(command_name="E5ParseOver15GoalsIframes")

        # Parse Over 2.5 Goals Iframes
        call_command(command_name="E5ParseOver25GoalsIframes")

        # Parse Over 3.5 Goals Iframes
        call_command(command_name="E5ParseOver35GoalsIframes")

        # Parse Win Draw Loss Percentage Iframes
        call_command(command_name="E5ParseWinDrawLossPercentageIframes")

        # Parse Corners Iframes
        call_command(command_name="E5ParseCornersIframes")

        # Parse Cards Iframes
        call_command(command_name="E5ParseCardsIframes")

        # Parse Half Time Full Time Iframes
        call_command(command_name="E5ParseHalfTimeFullTimeIframes")

        # Parse Scored Both Halves Iframes
        call_command(command_name="E5ParseScoredBothHalvesIframes")

        # Parse Won Both Halves Iframes
        call_command(command_name="E5ParseWonBothHalvesIframes")

        # Parse 1st 2nd Half Goals Iframes
        call_command(command_name="E5Parse1st2ndHalfGoalsIframes")

        # Parse Rescued Points Iframes
        call_command(command_name="E5ParseRescuedPointsIframes")

        # Parse Clean Sheet Iframes
        call_command(command_name="E5ParseCleanSheetsIframes")

        # Parse Won To Nil Iframes
        call_command(command_name="E5ParseWonToNilIframes")

        # Parse Win Loss Margin Iframes
        call_command(command_name="E5ParseWinLossMarginIframes")

        # Parse Scored First Iframes
        call_command(command_name="E5ParseScoredFirstIframes")

        # Parse Average First Goal Time Iframes
        call_command(command_name="E5ParseAverageFirstGoalTimeIframes")

        # Parse Average Team Goal Iframes
        call_command(command_name="E5ParseAverageTeamGoalsIframes")

        # Parse Early Goals Iframes
        call_command(command_name="E5ParseEarlyGoalsIframes")

        # Parse Late Goals Iframes
        call_command(command_name="E5ParseLateGoalsIframes")
