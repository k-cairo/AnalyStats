from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_over_15_goals import E5GetOver15Goals


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5ParseOver15GoalsIframes"
    help = "Parse Over 1.5 Goals Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetOver15Goals = E5GetOver15Goals()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Parse Over 1.5 Goals Iframes
        if scraper.status.success:
            scraper.parse_iframes()
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

        self.stdout.write("Over 1.5 Goals Iframes Parsed Successfully")
