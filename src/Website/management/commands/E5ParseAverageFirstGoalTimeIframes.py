from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_average_first_goal_time import E5GetAverageFirstGoalTime


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5ParseAverageFirstGoalTimeIframes"
    help = "Parse Average First Goal Time Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetAverageFirstGoalTime = E5GetAverageFirstGoalTime()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Parse Average First Goal Time Iframes
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

        self.stdout.write("Average First Goal Time Iframes Parsed Successfully")
