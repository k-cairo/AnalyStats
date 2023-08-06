import dataclasses
import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from Website.models import E5Team, E5Season, E5Match
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# E5
@dataclasses.dataclass
class E5GetMatchsStats:
    selenium_driver: E5SeleniumWebDriver

    # E5
    @classmethod
    def get_matchs_stats(cls, team: E5Team) -> None:
        # Check connection
        cls.selenium_driver.check_is_connected()

        if cls.selenium_driver.status.success:
            try:
                # Get Url
                cls.selenium_driver.driver.get(team.url)

                # Accept Cookies
                cls.selenium_driver.accept_cookies()

                # Get Logo
                if cls.selenium_driver.status.success:
                    try:
                        team.logo = cls.selenium_driver.driver.find_element(
                            By.CSS_SELECTOR, "img.teamlogo").get_attribute("src")
                        team.save()
                    except NoSuchElementException:
                        logging.warning(msg=f"GetMatchsStats.get_matchs_stats() - "
                                            f"Team {team} logo not found")

                # Get Matchs Stats
                if cls.selenium_driver.status.success:
                    matchs_table_trs: list[WebElement] = cls.selenium_driver.driver.find_elements(
                        By.CSS_SELECTOR, "div#div_matchlogs_for tbody tr")

                    for matchs_table_tr in matchs_table_trs:
                        venue: str = matchs_table_tr.find_element(By.CSS_SELECTOR, "td[data-stat='venue']").text
                        opponent_url: str = matchs_table_tr.find_element(By.CSS_SELECTOR, "td[data-stat='opponent'] a").get_attribute("href")
                        opponent: E5Team = E5Team.objects.get(season=team.season, url=opponent_url)

                        match: E5Match = E5Match()
                        match.championship = team.season.championship
                        match.season = team.season
                        match.date = matchs_table_tr.find_element(By.CSS_SELECTOR, "th a").text

                        if venue.lower() == "home":
                            match.home_team = team
                            match.away_team = opponent
                        elif venue.lower() == "away":
                            match.home_team = opponent
                            match.away_team = team
                        else:
                            logging.warning(msg=f"GetMatchsStats.get_matchs_stats() - "
                                                f"match : {opponent.name} - {team.name} : match venue not found")
                            continue

                        # Check match is valid
                        if not match.check_not_empty():
                            logging.warning(msg=f"GetMatchsStats.get_matchs_stats() - "
                                                f"match : {opponent.name} - {team.name} : match not valid")
                            continue

                        if not match.check_if_exists():
                            match.save()

            except Exception as ex:
                cls.selenium_driver.status.success = False
                cls.selenium_driver.status.error_context = "GetMatchsStats.get_matchs_stats()"
                cls.selenium_driver.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_GET_MATCHS_FAILED
                cls.selenium_driver.status.exception = ex




    # E5
    @classmethod
    def execute(cls) -> None:
        success: bool = True
        message: str
        cls.selenium_driver = E5SeleniumWebDriver()

        # Logging
        logging.info(msg=f"{datetime.now()} : E5GetMatchsStats start -----")

        # Query Active Seasons
        seasons = E5Season.objects.filter(active=True)

        for season in seasons:
            # Query Season Teams
            teams: QuerySet(E5Team) = E5Team.objects.filter(season=season)

            for team in teams:
                # Init driver
                if cls.selenium_driver.status.success:
                    cls.selenium_driver.init()
                    if not cls.selenium_driver.status.success:
                        logging.warning(
                            msg=f"E5GetMatchsStats.execute() - {cls.selenium_driver.status.error_context} : "
                                f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

                # Get Matchs Stats
                if cls.selenium_driver.status.success:
                    cls.get_matchs_stats(team=team)
                    if not cls.selenium_driver.status.success:
                        logging.warning(
                            msg=f"E5GetMatchsStats.execute() - {cls.selenium_driver.status.error_context} : "
                                f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

                # Close driver
                cls.selenium_driver.quit()
                if not cls.selenium_driver.status.success:
                    logging.warning(
                        msg=f"E5GetMatchsStats.execute() - {cls.selenium_driver.status.error_context} : "
                            f"{cls.selenium_driver.status.error_type} : {cls.selenium_driver.status.exception}")

        # Logging
        logging.info(msg=f"{datetime.now()} : E5GetMatchsStats end -----")


# E5
class Command(BaseCommand):
    help = "Get all matchs stats"

    def handle(self, *args, **options):
        # GET UPCOMING MATCHS
        E5GetMatchsStats.execute()

        self.stdout.write('Matchs Stats Updated Successfully')
