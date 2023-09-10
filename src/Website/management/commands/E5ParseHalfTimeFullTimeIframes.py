from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_half_time_full_time import E5GetHalfTimeFullTime


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5ParseHalfTimeFullTimeIframes"
    help = "Parse Half Time Full Time Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetHalfTimeFullTime = E5GetHalfTimeFullTime()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Parse Half Time Full Time Iframes
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

        self.stdout.write("Half Time Full Time Iframes Parsed Successfully")
