import contextlib
import dataclasses
from enum import Enum

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


# E5
@dataclasses.dataclass
class E5SeleniumWebdriverError(Enum):
    ERROR_TYPE_NONE = ""

    # Failed
    ERROR_TYPE_INIT_FAILED = "init_failed"
    ERROR_TYPE_QUIT_FAILED = "quit_failed"
    ERROR_TYPE_SWITCH_TO_STATS_AGAINST_FAILED = "switch_to_stats_against_failed"
    ERROR_TYPE_GET_COUNTRY_FAILED = "get_country_failed"
    ERROR_TYPE_GET_CHAMPIONSHIPS_FAILED = "get_championships_failed"
    ERROR_TYPE_GET_SEASONS_FAILED = "get_seasons_failed"
    ERROR_TYPE_GET_TEAMS_FAILED = "get_teams_failed"
    ERROR_TYPE_GET_UPCOMING_MATCHS_FAILED = "get_upcoming_matchs_failed"
    ERROR_TYPE_GET_MATCHS_FAILED = "get_matchs_failed"

    # Not Connected
    ERROR_TYPE_NOT_CONNECTED = "not_connected"


# E5
@dataclasses.dataclass
class E5SeleniumWebdriverStatus:
    success: bool = True
    error_type: E5SeleniumWebdriverError = E5SeleniumWebdriverError.ERROR_TYPE_NONE
    error_context: str = ""
    exception: str = ""


# E5
@dataclasses.dataclass
class E5SeleniumWebDriver:
    driver: WebDriver = None
    is_connected: bool = False
    status: E5SeleniumWebdriverStatus = E5SeleniumWebdriverStatus()

    # E5
    def init(self) -> None:
        try:
            service: Service = Service()
            self.driver = webdriver.Chrome(service=service)
            self.is_connected = True
            self.status.success = True
        except Exception as ex:
            self.is_connected = False
            self.status.success = False
            self.status.error_context = "E5SeleniumWebDriver.init()"
            self.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_INIT_FAILED
            self.status.exception = ex

    # E5
    def quit(self) -> None:
        try:
            self.driver.quit()
            self.status.success = True
            self.is_connected = False
        except Exception as ex:
            self.is_connected = True
            self.status.success = False
            self.status.error_context = "E5SeleniumWebDriver.quit()"
            self.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_QUIT_FAILED
            self.status.exception = ex

    # E5
    def check_is_connected(self) -> None:
        if not self.is_connected:
            self.status.success = False
            self.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_NOT_CONNECTED

    # E5
    def accept_cookies(self) -> None:
        if self.status.success and self.is_connected:
            with contextlib.suppress(NoSuchElementException):
                self.driver.implicitly_wait(time_to_wait=10)
                self.driver.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/div/div/div/div[2]/div/button[3]").click()
                self.driver.switch_to.default_content()
                self.driver.implicitly_wait(time_to_wait=2)
