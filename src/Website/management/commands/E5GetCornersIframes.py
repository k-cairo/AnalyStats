import logging
from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver
from e5toolbox.scrapper.stats.get_corners import E5GetCorners

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "GetCornersIframes"
    help = "Get Active Season's Corners Iframes"

    def handle(self, *args, **options):
        # Instance selenium_webdriver
        scraper: E5GetCorners = E5GetCorners()

        # Logging
        logging.info(msg=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            logging.warning(msg=f"{self.CONTEXT} - {scraper.status.error_context} : "
                                f"{scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Active Seasons Teams
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

        self.stdout.write("Active Season's Corners Iframes Updated Successfully")
