import contextlib
import dataclasses
import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Website.models import E5Championship, E5Team
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetTeams:
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def get_teams(cls, championship: E5Championship) -> None:
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(championship.url)

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Teams
                teams_table = cls.selenium_driver.driver.find_element(
                    By.CSS_SELECTOR, "table.stats_table.sortable.min_width.force_mobilize.now_sortable")
                teams_trs = teams_table.find_elements(By.CSS_SELECTOR, "tbody tr")

                for teams_tr in teams_trs:
                    with contextlib.suppress(NoSuchElementException):
                        team: E5Team = E5Team()
                        team.name = teams_tr.find_element(
                            By.CSS_SELECTOR, "td.left a").text.replace('"', "").replace("'", "")
                        team.championship = championship
                        team.gender = championship.gender
                        team.url = teams_tr.find_element(By.CSS_SELECTOR, "td.left a").get_attribute("href")

                        # Check team is valid (Any blank field)
                        if not team.check_not_empty():
                            logging.warning(
                                msg=f"GetTeams.execute() - {cls.selenium_driver.status.error_context} : "
                                    f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")
                            continue

                        if not team.check_if_exists():
                            team.save()

            except Exception as ex:
                cls.selenium_driver.status.success = False
                cls.selenium_driver.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_GET_CHAMPIONSHIPS_FAILED
                cls.selenium_driver.status.error_context = "GetChampionships.get_championships()"
                cls.selenium_driver.status.exception = ex

    # E5
    @classmethod
    def execute(cls) -> None:
        cls.selenium_driver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : GetTeams start -----")

        # Query Countries
        championships = E5Championship.objects.all()

        # Loop Through Championships
        for championship in championships:
            # Init driver
            if cls.selenium_driver.status.success:
                cls.selenium_driver.init()
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetTeams.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Get Teams
            if cls.selenium_driver.status.success:
                cls.get_teams(championship=championship)
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetTeams.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Close driver
            cls.selenium_driver.quit()
            if not cls.selenium_driver.status.success:
                logging.warning(
                    msg=f"GetTeams.execute() - {cls.selenium_driver.status.error_context} : "
                        f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetTeams end -----")


# E5
class Command(BaseCommand):
    help = "Get all teams"

    def handle(self, *args, **options):
        # GET TEAMS
        E5GetTeams.execute()

        self.stdout.write('Teams Updated Successfully')
