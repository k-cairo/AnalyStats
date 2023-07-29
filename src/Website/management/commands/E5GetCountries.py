import dataclasses
import logging
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from E5AppConf import E5AppConf
from Website.models import E5Country
from e5toolbox.base.E5File import E5File
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetCountries:
    conf: E5AppConf
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def get_countries(cls):
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(cls.conf.get_countries_url)

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Countries
                if cls.selenium_driver.status.success:
                    tr_countries = cls.selenium_driver.driver.find_elements(By.CSS_SELECTOR, "table#countries tbody tr")
                    for tr_country in tr_countries:
                        country: E5Country = E5Country()
                        try:
                            country.name = tr_country.find_element(By.CSS_SELECTOR, "th a").text.replace("'", "")
                            country.organisation = tr_country.find_element(
                                By.CSS_SELECTOR, "td.left.poptip").text.replace("'", "")
                            country.url = tr_country.find_element(By.CSS_SELECTOR, "th a").get_attribute("href")
                        except NoSuchElementException:
                            continue

                        # Check if country is valid (Any blank field)
                        if not country.check_not_empty():
                            logging.warning(msg=f"GetCountries.get_countries() - Country not valid : {country}")
                            continue

                        if not country.check_if_exists():
                            country.save()

            except Exception as ex:
                cls.selenium_driver.status.success = False
                cls.selenium_driver.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_GET_COUNTRY_FAILED
                cls.selenium_driver.status.error_context = "GetCountries.get_countries()"
                cls.selenium_driver.status.exception = ex

    # E5
    @classmethod
    def execute(cls) -> None:
        success: bool = True
        message: str
        cls.conf = E5AppConf()
        cls.selenium_driver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : GetCountries start -----")

        # Check environment variable
        appconf_path = os.environ.get("jsonconf")
        if appconf_path is None:
            success = False
            logging.warning(msg="GetCountries.execute() - jsonconf environment variable not found")

        # Load conf
        if success and E5File.is_valid_path(isdir=False, path=appconf_path):
            success, message = cls.conf.load(pathfile=appconf_path)
            if not success:
                logging.warning(msg=f"GetCountries.execute() - {message}")
        else:
            success = False
            logging.warning(msg=f"GetCountries.execute() - Invalid json file path : {appconf_path}")

        # Init driver
        if success:
            cls.selenium_driver.init()
            if not cls.selenium_driver.status.success:
                logging.warning(
                    msg=f"GetCountries.execute() - {cls.selenium_driver.status.error_context} : "
                        f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Get Countries
        if cls.selenium_driver.status.success:
            cls.get_countries()
            if not cls.selenium_driver.status.success:
                logging.warning(
                    msg=f"GetCountries.execute() - {cls.selenium_driver.status.error_context} : "
                        f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Close driver
        cls.selenium_driver.quit()
        if not cls.selenium_driver.status.success:
            logging.warning(
                msg=f"GetCountries.execute() - {cls.selenium_driver.status.error_context} : "
                    f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetCountries end -----")


# E5
class Command(BaseCommand):
    help = "Get all countries"

    def handle(self, *args, **options):
        # GET COUNTRIES
        E5GetCountries.execute()

        self.stdout.write('Countries Updated Successfully')
