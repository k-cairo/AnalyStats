import dataclasses
import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Website.models import E5Country, E5Championship
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetChampionships:
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def get_championships(cls, country: E5Country) -> None:
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(country.url)

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Championships
                if cls.selenium_driver.status.success:
                    divs_table_wrapper = cls.selenium_driver.driver.find_elements(By.CSS_SELECTOR, "div.table_wrapper")
                    for div_table_wrapper in divs_table_wrapper:
                        try:
                            div_title: str = div_table_wrapper.find_element(By.CSS_SELECTOR, "h2").text
                        except NoSuchElementException:
                            continue

                        if 'Domestic Leagues' in div_title:
                            trs_league = div_table_wrapper.find_elements(
                                By.CSS_SELECTOR, "div.table_container tbody tr")
                            for tr_league in trs_league:
                                championship: E5Championship = E5Championship()
                                championship.country = country
                                championship.name = tr_league.find_element(
                                    By.CSS_SELECTOR, "th").text.replace('"', "").replace("'", "")
                                championship.gender = tr_league.find_element(By.CSS_SELECTOR, "td.center").text
                                championship.url = tr_league.find_element(
                                    By.CSS_SELECTOR, "th.left a").get_attribute("href")

                                # Check championship is valid (Any blank field)
                                if not championship.check_not_empty():
                                    logging.warning(msg=f"GetChampionships.get_championships() - "
                                                        f"Championship not valid : {championship}")
                                    continue

                                if not championship.check_if_exists():
                                    championship.save()

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
        logging.info(msg=f"{datetime.now()} : GetChampionships start -----")

        # Query Countries
        countries = E5Country.objects.all()

        # Loop Through Countries
        for country in countries:
            # Init driver
            if cls.selenium_driver.status.success:
                cls.selenium_driver.init()
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetChampionships.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Get GetChampionships
            if cls.selenium_driver.status.success:
                cls.get_championships(country=country)
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetChampionships.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

            # Close driver
            cls.selenium_driver.quit()
            if not cls.selenium_driver.status.success:
                logging.warning(
                    msg=f"GetChampionships.execute() - {cls.selenium_driver.status.error_context} : "
                        f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetChampionships end -----")


# E5
class Command(BaseCommand):
    help = "Get all championships"

    def handle(self, *args, **options):
        # GET COUNTRIES
        E5GetChampionships.execute()

        self.stdout.write('Championships Updated Successfully')
