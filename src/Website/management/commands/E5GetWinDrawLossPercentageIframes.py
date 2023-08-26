from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from Website.models import E5WinDrawLossPercentageIframe
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "GetWinDrawLossPercentageIframes"
    help = "Get Win Draw Loss Percentage Iframes"

    def handle(self, *args, **options):
        # Instantiate Scraper
        scraper: E5SeleniumWebDriver = E5SeleniumWebDriver()

        # Logging
        scraper.log_info(message=f"{datetime.now()} : {self.CONTEXT} start -----")

        # Init driver
        scraper.init()
        if not scraper.status.success:
            scraper.log_warning(f"{self.CONTEXT} - {scraper.status.error_context} : {scraper.status.error_type} : "
                                f"{scraper.status.exception}")

        # Get Win Draw Loss Percentage Iframes
        if scraper.status.success:
            scraper.get_iframe(endpoint="wdl/", error_context=self.CONTEXT,
                               save_message="Win Draw Loss Percentage Iframes", class_=E5WinDrawLossPercentageIframe)
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

        self.stdout.write("Win Draw Loss Percentage Iframes Updated Successfully")
