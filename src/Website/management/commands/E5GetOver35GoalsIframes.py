import logging
from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_over_35_goals import E5GetOver35Goals


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5GetOver25GoalsIframes"
    help = "Get Active Season's Overs 3.5 Goals Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetOver35Goals = E5GetOver35Goals()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : "
                                f"{scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Iframes
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
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} end -----")

        self.stdout.write("Overs 3.5 Goals Iframes Updated Successfully")
