from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.stats.get_scored_both_halves import E5GetScoredBothHalves


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "E5ParseScoredBothHalvesIframes"
    help = "Parse Scored Both Halves Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5GetScoredBothHalves = E5GetScoredBothHalves()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Parse Scored Both Halves Iframes
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

        self.stdout.write("Scored Both Halves Iframes Parsed Successfully")
