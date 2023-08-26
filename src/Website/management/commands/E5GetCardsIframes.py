from datetime import datetime
from typing import ClassVar

from django.core.management.base import BaseCommand

from Website.models import E5CardsIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver


# E5
class Command(BaseCommand):
    CONTEXT: ClassVar[str] = "GetCardsIframes"
    help = "Get Cards Iframes"

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

        # Get Cards Iframes
        if scraper.status.success:
            scraper.get_iframes(endpoint='cards/', error_context=self.CONTEXT, iframe_length=4,
                                save_message="Cards Iframes", class_=E5CardsIframes)
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

        self.stdout.write("Cards Iframes Updated Successfully")
