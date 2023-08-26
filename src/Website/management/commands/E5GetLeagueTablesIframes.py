import logging
from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_league_tables import E5GetLeagueTables

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "GetActiveSeasonsLeagueTableIframes"
    help = "Get Active Season's League Table Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetLeagueTables = E5GetLeagueTables()

        # Logging
        logging.info(msg=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : "
                                f"{scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Active Seasons League Table
        if scraper.status.success:
            scraper.get_iframes()
            if not scraper.status.success:
                logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : "
                                    f"{scraper.status.error_type} : "
                                    f"{scraper.status.exception}")

        # Close driver
        scraper.quit()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : "
                                f"{scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : {self.CONTEXT} end -----")

        self.stdout.write("Active Season's League Tables Iframes Updated Successfully")
