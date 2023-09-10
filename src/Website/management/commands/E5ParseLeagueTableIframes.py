from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_league_tables import E5GetLeagueTables


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5ParseLeagueTableIframes"
    help = "Parse League Table Iframes"

    def handle(self, *args, **options):
        # Instance scraper
        scraper: E5GetLeagueTables = E5GetLeagueTables()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Teams Ranking Iframes
        if scraper.status.success:
            scraper.get_teams_ranking()
            if not scraper.status.success:
                scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                    f"{scraper.status.exception}")

        # Close driver
        scraper.quit()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} end -----")

        self.stdout.write("Teams Ranking Updated Successfully")
