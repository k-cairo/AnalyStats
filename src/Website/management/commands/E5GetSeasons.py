import contextlib
import dataclasses
import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Website.models import E5Championship, E5Season
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetSeasons:
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def get_seasons(cls, championship: E5Championship) -> None:
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(championship.url)

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Logo
                if cls.selenium_driver.status.success:
                    try:
                        championship.logo = cls.selenium_driver.driver.find_element(
                            By.CSS_SELECTOR, "img.teamlogo").get_attribute("src")
                        championship.save()
                    except NoSuchElementException:
                        logging.warning(msg=f"GetSeasons.get_seasons() - "
                                            f"Championship {championship} logo not found")
                        pass

                # Get Seasons
                seasons_table = cls.selenium_driver.driver.find_element(By.CSS_SELECTOR, "table#seasons tbody")
                seasons_trs = seasons_table.find_elements(By.CSS_SELECTOR, "tr")

                for season_tr in seasons_trs:
                    with contextlib.suppress(NoSuchElementException):
                        season: E5Season = E5Season()
                        season.championship = championship
                        season.name = season_tr.find_element(By.CSS_SELECTOR, "th.left a").text
                        season.squads = int(season_tr.find_elements(By.CSS_SELECTOR, "td.right")[0].text)
                        season.url = season_tr.find_element(By.CSS_SELECTOR, "th.left a").get_attribute("href")

                        # Check season is valid (Any blank field)
                        if not season.check_not_empty():
                            logging.warning(
                                msg=f"GetSeasons.get_seasons() - {cls.selenium_driver.status.error_context} : "
                                    f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")
                            continue

                        if not season.check_if_exists():
                            season.save()

            except Exception as ex:
                cls.selenium_driver.status.success = False
                cls.selenium_driver.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_GET_SEASONS_FAILED
                cls.selenium_driver.status.error_context = "GetSeasons.get_seasons()"
                cls.selenium_driver.status.exception = ex

    # E5
    @classmethod
    def execute(cls) -> None:
        cls.selenium_driver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : GetSeasons start -----")

        # Query Countries
        championships = E5Championship.objects.all()

        # Loop Through Championships
        for championship in championships:
            if not championship.country.parse_country:
                continue

            # Init driver
            if cls.selenium_driver.status.success:
                cls.selenium_driver.init()
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetSeasons.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Get Seasons
            if cls.selenium_driver.status.success:
                cls.get_seasons(championship=championship)
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetSeasons.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Close driver
            cls.selenium_driver.quit()
            if not cls.selenium_driver.status.success:
                logging.warning(
                    msg=f"GetSeasons.execute() - {cls.selenium_driver.status.error_context} : "
                        f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetSeasons end -----")


# E5
class Command(BaseCommand):
    help = "Get all seasons"

    def handle(self, *args, **options):
        # GET SEASONS
        E5GetSeasons.execute()

        self.stdout.write('Seasons Updated Successfully')
