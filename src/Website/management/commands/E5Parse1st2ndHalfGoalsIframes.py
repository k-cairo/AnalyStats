from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_1st_2nd_half_goals import E5Get1st2ndHalfGoals


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5Parse1st2ndHalfGoalsIframes"
    help = "Parse 1st 2nd Half Goals Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5Get1st2ndHalfGoals = E5Get1st2ndHalfGoals()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Parse 1st 2nd Half Goals Iframes
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

        self.stdout.write("1st 2nd Half Goals Iframes Parsed Successfully")
