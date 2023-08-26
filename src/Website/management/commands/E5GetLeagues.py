import logging
from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.league.get_leagues import E5GetLeagues

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "GetLeagues"
    help = "Get Leagues"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetLeagues = E5GetLeagues()

        # Logging
        logging.info(msg=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Leagues
        if scraper.status.success:
            scraper.get()
            if not scraper.status.success:
                logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                    f"{scraper.status.exception}")

        # Close driver
        scraper.quit()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : {self.CONTEXT} end -----")

        self.stdout.write('Leagues Updated Successfully')
