import dataclasses
import logging
from enum import Enum
from typing import Any, ClassVar

from bs4 import BeautifulSoup, ResultSet, Tag
from django.db.models import QuerySet
from django.utils.text import slugify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from Website.models import E5Season, E5CardsIframes, E5BttsIframes, E5Over05GoalsIframe, \
    E5Over15GoalsIframe, E5Over25GoalsIframe, E5Over35GoalsIframe, E5CornersIframes, E5ScoredBothHalfIframes, \
    E5WonBothHalfIframes, E5League

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


@dataclasses.dataclass
class E5SeleniumWebdriverError(Enum):
    ERROR_TYPE_NONE = ""

    # Failed
    ERROR_TYPE_INIT_FAILED = "init_failed"
    ERROR_TYPE_QUIT_FAILED = "quit_failed"
    ERROR_TYPE_GET_TEAM_FAILED = "get_team_failed"
    ERROR_TYPE_GET_LEAGUE_NAME_OR_URL_FAILED = "get_league_name_or_url_failed"
    ERROR_TYPE_GET_URL_FAILED = "get_url_failed"
    ERROR_TYPE_GET_SOUP_FAILED = "get_soup_failed"
    ERROR_TYPE_GET_IFRAME_URL_FAILED = "get_iframe_url_failed"
    ERROR_TYPE_GET_IFRAME_FAILED = "get_iframe_failed"
    ERROR_TYPE_GET_OVER_05_GOALS_IFRAME_URL_FAILED = "get_over_05_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_15_GOALS_IFRAME_URL_FAILED = "get_over_15_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_25_GOALS_IFRAME_URL_FAILED = "get_over_25_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_35_GOALS_IFRAME_URL_FAILED = "get_over_35_goals_iframe_url_failed"
    ERROR_TYPE_GET_CORNER_IFRAME_URL_FAILED = "get_corner_iframe_url_failed"
    ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED = "get_card_iframe_url_failed"
    # Empty
    ERROR_TYPE_IFRAME_EMPTY = "iframe_empty"
    # Bad Length
    ERROR_TYPE_IFRAMES_BAD_LENGTH = "iframes_bad_length"
    # Not Connected
    ERROR_TYPE_NOT_CONNECTED = "not_connected"


@dataclasses.dataclass
class E5SeleniumWebdriverStatus:
    success: bool = True
    error_type: E5SeleniumWebdriverError = E5SeleniumWebdriverError.ERROR_TYPE_NONE
    error_context: str = ""
    exception: str = ""


# E5
@dataclasses.dataclass
class E5SeleniumWebDriver:
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    soup: BeautifulSoup = None
    driver: WebDriver = None
    is_connected: bool = False
    status: E5SeleniumWebdriverStatus = E5SeleniumWebdriverStatus()

    ################################################## STATIC METHODS ##################################################
    # E5
    @staticmethod
    def log_info(message: str) -> None:
        logging.info(msg=message)

    # E5
    @staticmethod
    def log_warning(message: str) -> None:
        logging.warning(msg=message)

    ##################################################### METHODS ######################################################
    # E5
    def init(self) -> None:
        try:
            service: Service = Service()
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
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
    def exception(self, error_type: E5SeleniumWebdriverError, error_context: str, exception: Any) -> None:
        self.status.success = False
        self.status.error_type = error_type
        self.status.error_context = error_context
        self.status.exception = exception
        logging.warning(msg=f"{self.status.error_context} : {self.status.error_type} : {self.status.exception}")

    # E5
    def get(self, url: str, error_context: str):
        try:
            self.driver.get(url)
        except Exception as ex:
            self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                           error_context=error_context, exception=ex)

        if self.status.success:
            self.get_soup(error_context=error_context)

    # E5
    def get_soup(self, error_context: str) -> None:
        try:
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as ex:
            self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                           error_context=error_context, exception=ex)

    # E5
    def build_iframe(self, season: E5Season, stats_iframes: ResultSet[Tag], error_context: str, iframe_class):
        iframe: iframe_class = iframe_class()
        iframe.season = season
        for idx, stat_iframe in enumerate(stats_iframes):
            try:
                iframe_url: str = stat_iframe['src']
            except Exception as ex:
                self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED,
                               error_context=error_context, exception=ex)
                continue

            if isinstance(iframe, E5BttsIframes):
                if idx == 0:
                    iframe.btts_url = iframe_url
                elif idx == 1:
                    iframe.btts_1h_url = iframe_url
                elif idx == 2:
                    iframe.btts_2h_url = iframe_url
                elif idx == 3:
                    iframe.btts_bh_url = iframe_url
                elif idx == 4:
                    iframe.btts_25_url = iframe_url
            elif isinstance(iframe, E5Over05GoalsIframe):
                if idx == 0:
                    iframe.over_05_goals_url = iframe_url
                elif idx == 1:
                    iframe.over_05_goals_1h_url = iframe_url
                elif idx == 2:
                    iframe.over_05_goals_2h_url = iframe_url
                elif idx == 3:
                    iframe.over_05_goals_bh_url = iframe_url
            elif isinstance(iframe, E5Over15GoalsIframe):
                if idx == 0:
                    iframe.over_15_goals_url = iframe_url
                elif idx == 1:
                    iframe.over_15_goals_1h_url = iframe_url
                elif idx == 2:
                    iframe.over_15_goals_2h_url = iframe_url
                elif idx == 3:
                    iframe.over_15_goals_bh_url = iframe_url
            elif isinstance(iframe, E5Over25GoalsIframe):
                if idx == 0:
                    iframe.over_25_goals_url = iframe_url
                elif idx == 1:
                    iframe.over_25_goals_1h_url = iframe_url
                elif idx == 2:
                    iframe.over_25_goals_2h_url = iframe_url
                elif idx == 3:
                    iframe.over_25_goals_bh_url = iframe_url
            elif isinstance(iframe, E5Over35GoalsIframe):
                if idx == 0:
                    iframe.over_35_goals_url = iframe_url
                elif idx == 1:
                    iframe.over_35_goals_1h_url = iframe_url
                elif idx == 2:
                    iframe.over_35_goals_2h_url = iframe_url
                elif idx == 3:
                    iframe.over_35_goals_bh_url = iframe_url
            elif isinstance(iframe, E5CornersIframes):
                if idx == 0:
                    iframe.team_corners_for_1h_url = iframe_url
                elif idx == 1:
                    iframe.team_corners_against_1h_url = iframe_url
                elif idx == 2:
                    iframe.team_corners_for_2h_url = iframe_url
                elif idx == 3:
                    iframe.team_corners_against_2h_url = iframe_url
                elif idx == 4:
                    iframe.team_corners_for_ft_url = iframe_url
                elif idx == 5:
                    iframe.team_corners_against_ft_url = iframe_url
                elif idx == 6:
                    iframe.match_corners_1h_url = iframe_url
                elif idx == 7:
                    iframe.match_corners_2h_url = iframe_url
                elif idx == 8:
                    iframe.match_corners_ft_url = iframe_url
            elif isinstance(iframe, E5CardsIframes):
                if idx == 0:
                    iframe.yellow_cards_for_url = iframe_url
                elif idx == 1:
                    iframe.yellow_cards_against_url = iframe_url
                elif idx == 2:
                    iframe.red_cards_for_url = iframe_url
                elif idx == 3:
                    iframe.red_cards_against_url = iframe_url
            elif isinstance(iframe, E5ScoredBothHalfIframes):
                if idx == 0:
                    iframe.scored_both_half_url = iframe_url
                elif idx == 1:
                    iframe.conceded_both_half_url = iframe_url
            elif isinstance(iframe, E5WonBothHalfIframes):
                if idx == 0:
                    iframe.won_both_half_url = iframe_url
                elif idx == 1:
                    iframe.lost_both_half_url = iframe_url

        return iframe

    #################################################### GET LEAGUES ###################################################
    def get_leagues(self, error_context: str) -> None:
        # Check connection
        self.check_is_connected()

        # Get Url
        self.get(url="https://www.thestatsdontlie.com/football/leagues/", error_context=error_context)

        if self.status.success:
            selector: str = "div.fusion-column-wrapper.fusion-flex-column-wrapper-legacy a"
            leagues: ResultSet[Tag] = self.soup.select(selector=selector)

            # Get Leagues
            for league in leagues:
                # Get League Name and Url
                try:
                    league_name: str = league.text
                    league_url: str = league['href']
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_LEAGUE_NAME_OR_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    continue

                # Create League
                new_league: E5League = E5League()
                new_league.name = league_name
                new_league.url = league_url
                new_league.slug = slugify(value=league_name)

                if ("Colombia" in league_name or "Costa Rica" in league_name or "Ecuador" in league_name
                        or "Honduras" in league_name or "Mexico" in league_name or "Paraguay" in league_name
                        or "Peru" in league_name or "Tunisia" in league_name or "Uruguay" in league_name):
                    continue

                # Check if league already exists
                if new_league.exists():
                    # Update League
                    target_league: E5League = E5League.objects.get(name=league_name)
                    target_league.url = league_url
                    target_league.slug = slugify(value=league_name)
                    target_league.save()
                    self.log_info(message=f"League {league_name} updated in database")
                else:
                    # Save League
                    new_league.save()
                    self.log_info(message=f"League {league_name} created in database")

    ##################################################### GET IFRAME ###################################################
    # E5
    def get_iframes(self, endpoint: str, error_context: str, iframe_length: int, save_message: str, class_: Any):
        # Check Connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}{endpoint}", error_context=error_context)
                if not self.status.success:
                    continue

                # Get Iframes
                stat_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check Iframes Length
                if len(stat_iframes) != iframe_length:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=error_context, exception=None)
                    continue

                # Build Iframe
                iframe = self.build_iframe(season=season, stats_iframes=stat_iframes, error_context=error_context,
                                           iframe_class=class_)

                # Check Iframe Not Empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=error_context, exception=None)
                    continue

                # Save Iframe
                if not iframe.exists():
                    iframe.save()
                    self.log_info(message=f"League {season.league.name} : {save_message} created in database")
                else:
                    class_.update_iframe(season=season, iframe=iframe)
                    self.log_info(message=f"League {season.league.name} : {save_message} updated in database")

    # E5
    def get_iframe(self, endpoint: str, error_context: str, save_message: str, class_: Any):
        # Check Connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}{endpoint}", error_context=error_context)
                if not self.status.success:
                    continue

                # Get Iframes
                stat_iframe: Tag | None = self.soup.select_one(selector="div.fusion-text.fusion-text-2 iframe")

                # Check Iframes
                if stat_iframe is None:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_IFRAME_FAILED,
                                   error_context=error_context, exception=None)
                    continue

                # Get Iframe Url
                try:
                    iframe_url: str = stat_iframe['src']
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    continue

                # Build Iframe
                iframe: class_ = class_()
                iframe.season = season
                iframe.url = iframe_url

                # Check Iframe Not Empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=error_context, exception=None)
                    continue

                # Save Iframe
                if not iframe.exists():
                    iframe.save()
                    self.log_info(message=f"League {season.league.name} : {save_message} created in database")
                else:
                    class_.update_iframe(season=season, iframe=iframe)
                    self.log_info(message=f"League {season.league.name} : {save_message} updated in database")
