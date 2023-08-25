import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
class Command(BaseCommand):
    help = "Get Active Season's Teams Ranking"

    def handle(self, *args, **options):
        # Instance selenium_webdriver
        selenium_webdriver: E5SeleniumWebDriver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : GetActiveSeasonsTeamsRanking start -----")

        # Init driver
        selenium_webdriver.init()
        if not selenium_webdriver.status.success:
            logging.warning(msg=f"Get Active Seasons Teams Ranking - {selenium_webdriver.status.error_context} : "
                                f"{selenium_webdriver.status.error_type} : "
                                f"{selenium_webdriver.status.exception}")

        # Get Active Seasons Teams
        if selenium_webdriver.status.success:
            selenium_webdriver.get_active_seasons_teams_ranking()
            if not selenium_webdriver.status.success:
                logging.warning(msg=f"Get Active Seasons Teams Ranking - {selenium_webdriver.status.error_context} : "
                                    f"{selenium_webdriver.status.error_type} : "
                                    f"{selenium_webdriver.status.exception}")

        # Close driver
        selenium_webdriver.quit()
        if not selenium_webdriver.status.success:
            logging.warning(msg=f"Get Active Seasons Teams Ranking - {selenium_webdriver.status.error_context} : "
                                f"{selenium_webdriver.status.error_type} : "
                                f"{selenium_webdriver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetActiveSeasonsTeamsRanking end -----")

        self.stdout.write("Active Season's Teams Ranking Updated Successfully")
