import dataclasses
import logging
import os
from datetime import datetime, timedelta
from typing import ClassVar

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from E5AppConf import E5AppConf
from Website.models import E5Team, E5Season, E5Match
from e5toolbox.base.E5File import E5File
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetUpcomingMatchs:
    days: ClassVar[list[str]] = []
    conf: E5AppConf
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def build_days(cls):
        today_str: str = datetime.now().strftime("%Y-%m-%d")
        cls.days.append(today_str)
        for idx in range(6):
            date_str: str = (datetime.now() + timedelta(days=idx)).strftime("%Y-%m-%d")
            cls.days.append(date_str)

    # E5
    @classmethod
    def get_upcoming_matchs(cls, date: str) -> None:
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(f"{cls.conf.get_upcoming_matchs_url}/{date}")

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Upcoming Matchs
                if cls.selenium_driver.status.success:
                    div_championships = cls.selenium_driver.driver.find_elements(
                        By.CSS_SELECTOR, "div.table_wrapper.tabbed")
                    for div_championship in div_championships:
                        try:
                            championship_url: str = div_championship.find_element(By.CSS_SELECTOR,
                                                                                  "h2 a").get_attribute("href")
                        except NoSuchElementException:
                            logging.warning(f"GetUpcomingMatchs.get_upcoming_matchs(): No championship url found")
                            continue

                        try:
                            season: E5Season = E5Season.objects.filter(url=championship_url).get()
                        except ObjectDoesNotExist:
                            continue

                        if season is None:
                            logging.warning(f"GetUpcomingMatchs.get_upcoming_matchs(): No season found")
                            continue

                        if not season.championship.country.parse_country:
                            continue

                        upcoming_matchs_tr = div_championship.find_elements(
                            By.CSS_SELECTOR, "table.stats_table.sortable.min_width.now_sortable tbody tr")

                        # Loop Through Matchs
                        for upcoming_match_tr in upcoming_matchs_tr:
                            try:
                                home_team_str: str = upcoming_match_tr.find_element(By.CSS_SELECTOR, "td.right a").text
                                away_team_str: str = upcoming_match_tr.find_element(By.CSS_SELECTOR, "td.left a").text
                                home_team_url: str = upcoming_match_tr.find_element(By.CSS_SELECTOR,
                                                                                    "td.right a").get_attribute("href")
                                away_team_url: str = upcoming_match_tr.find_element(By.CSS_SELECTOR,
                                                                                    "td.left a").get_attribute("href")
                            except NoSuchElementException:
                                logging.warning(f"GetUpcomingMatchs.get_upcoming_matchs(): No match found")
                                continue

                            # Get E5Team - Home
                            try:
                                home_team: E5Team = E5Team.objects.filter(url=home_team_url, season=season).get()
                            except ObjectDoesNotExist:
                                logging.warning(
                                    f"GetUpcomingMatchs.get_upcoming_matchs(): No home team found - {season.championship} - {home_team_str}")
                                continue

                            # Get E5Team - Away
                            try:
                                away_team: E5Team = E5Team.objects.filter(url=away_team_url, season=season).get()
                            except ObjectDoesNotExist:
                                logging.warning(
                                    f"GetUpcomingMatchs.get_upcoming_matchs(): No away team found - {season.championship} - {away_team_str}")
                                continue

                            # Create E5Match
                            match: E5Match = E5Match()
                            match.season = season
                            match.championship = match.season.championship
                            match.date = date
                            match.home_team = home_team
                            match.away_team = away_team

                            # Check if match is not empty
                            if not match.check_not_empty():
                                logging.warning(
                                    f"GetUpcomingMatchs.get_upcoming_matchs(): Match is empty - {match}")
                                continue

                            # Check if match already exists
                            if not match.check_if_exists():
                                match.save()

            except Exception as ex:
                cls.selenium_driver.status.success = False
                cls.selenium_driver.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_GET_UPCOMING_MATCHS_FAILED
                cls.selenium_driver.status.error_context = "GetUpcomingMatchs.get_upcoming_matchs()"
                cls.selenium_driver.status.exception = ex

    # E5
    @classmethod
    def execute(cls) -> None:
        success: bool = True
        message: str
        cls.conf = E5AppConf()
        cls.selenium_driver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : GetUpcomingMatchs start -----")

        # Build days
        cls.build_days()

        # Check environment variable
        appconf_path = os.environ.get("jsonconf")
        if appconf_path is None:
            success = False
            logging.warning(msg="GetUpcomingMatchs.execute() - jsonconf environment variable not found")

        # Load conf
        if success and E5File.is_valid_path(isdir=False, path=appconf_path):
            success, message = cls.conf.load(pathfile=appconf_path)
            if not success:
                logging.warning(msg=f"GetUpcomingMatchs.execute() - {message}")
        else:
            success = False
            logging.warning(msg=f"GetUpcomingMatchs.execute() - Invalid json file path : {appconf_path}")

        # Check if Match.date already exists (next 7 days)
        if success:
            for day in cls.days:
                upcoming_matchs_queryset: QuerySet(E5Match) = E5Match.objects.filter(date=day)
                if len(upcoming_matchs_queryset) != 0:
                    continue

                # Init driver
                if success:
                    cls.selenium_driver.init()
                    if not cls.selenium_driver.status.success:
                        logging.warning(
                            msg=f"GetUpcomingMatchs.execute() - {cls.selenium_driver.status.error_context} : "
                                f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

                # Get Upcoming Matchs for the day
                if cls.selenium_driver.status.success:
                    cls.get_upcoming_matchs(date=day)
                    if not cls.selenium_driver.status.success:
                        logging.warning(
                            msg=f"GetUpcomingMatchs.execute() - {cls.selenium_driver.status.error_context} : "
                                f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

                # Close driver
                cls.selenium_driver.quit()
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"GetUpcomingMatchs.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : GetUpcomingMatchs end -----")


# E5
class Command(BaseCommand):
    help = "Get all upcoming matchs"

    def handle(self, *args, **options):
        # GET UPCOMING MATCHS
        E5GetUpcomingMatchs.execute()

        self.stdout.write('Upcoming Matchs Updated Successfully')
