import dataclasses
import logging
from enum import Enum
from typing import Any

from bs4 import BeautifulSoup, Tag, ResultSet
from django.db.models import QuerySet
from django.utils.text import slugify
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from Website.models import (E5League, E5Season, E5LeagueTableIframe, E5Team, E5TeamRanking, E5BttsIframes,
                            E5Over05GoalsIframe, E5Over15GoalsIframe, E5Over25GoalsIframe, E5Over35GoalsIframe,
                            E5CornersIframes, E5CardsIframes, E5Over05GoalsStats, E5Over15GoalsStats,
                            E5Over25GoalsStats, E5Over35GoalsStats, E5TeamCornerStats, E5MatchCornerStats, E5CardsStats)

logging.basicConfig(level=logging.INFO, filename="management_command.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


@dataclasses.dataclass
class E5SeleniumWebdriverError(Enum):
    ERROR_TYPE_NONE = ""

    # Failed
    ERROR_TYPE_INIT_FAILED = "init_failed"
    ERROR_TYPE_QUIT_FAILED = "quit_failed"
    ERROR_TYPE_SWITCH_TO_STATS_AGAINST_FAILED = "switch_to_stats_against_failed"
    ERROR_TYPE_GET_COUNTRY_FAILED = "get_country_failed"
    ERROR_TYPE_GET_TEAM_FAILED = "get_team_failed"
    ERROR_TYPE_GET_LEAGUES_WEB_ELEMENT_FAILED = "get_leagues_web_element_failed"
    ERROR_TYPE_GET_LEAGUE_NAME_OR_URL_FAILED = "get_league_name_or_url_failed"
    ERROR_TYPE_GET_URL_FAILED = "get_url_failed"
    ERROR_TYPE_GET_SOUP_FAILED = "get_soup_failed"
    ERROR_TYPE_GET_CHAMPIONSHIPS_FAILED = "get_championships_failed"
    ERROR_TYPE_GET_SEASONS_WEB_ELEMENT_FAILED = "get_seasons_web_element_failed"
    ERROR_TYPE_GET_SEASON_NAME_OR_URL_FAILED = "get_season_name_or_url_failed"
    ERROR_TYPE_GET_NAME_OR_URL_FAILED = "get_name_or_url_failed"
    ERROR_TYPE_GET_IFRAME_URL_FAILED = "get_iframe_url_failed"
    ERROR_TYPE_GET_OVER_05_GOALS_IFRAME_URL_FAILED = "get_over_05_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_15_GOALS_IFRAME_URL_FAILED = "get_over_15_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_25_GOALS_IFRAME_URL_FAILED = "get_over_25_goals_iframe_url_failed"
    ERROR_TYPE_GET_OVER_35_GOALS_IFRAME_URL_FAILED = "get_over_35_goals_iframe_url_failed"
    ERROR_TYPE_GET_CORNER_IFRAME_URL_FAILED = "get_corner_iframe_url_failed"
    ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED = "get_card_iframe_url_failed"
    ERROR_TYPE_IFRAME_EMPTY = "iframe_empty"
    ERROR_TYPE_GET_TEAMS_FAILED = "get_teams_failed"
    ERROR_TYPE_GET_TABLE_TR_FAILED = "get_table_tr_failed"
    ERROR_TYPE_GET_BTTS_IFRAMES_FAILED = "get_btts_iframes_failed"
    ERROR_TYPE_GET_CARDS_IFRAMES_FAILED = "get_cards_iframes_failed"
    ERROR_TYPE_IFRAMES_BAD_LENGTH = "iframes_bad_length"
    ERROR_TYPE_CORNERS_IFRAMES_BAD_LENGTH = "corners_iframes_bad_length"
    ERROR_TYPE_CARDS_IFRAMES_BAD_LENGTH = "cards_iframes_bad_length"
    ERROR_TYPE_GET_TEAM_NAME_OR_TEAM_URL_FAILED = "get_team_name_or_team_url_failed"
    ERROR_TYPE_GET_TEAM_RANKING_FAILED = "get_team_ranking_failed"
    ERROR_TYPE_GET_UPCOMING_MATCHS_FAILED = "get_upcoming_matchs_failed"
    ERROR_TYPE_GET_MATCHS_FAILED = "get_matchs_failed"

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
    soup: BeautifulSoup = None
    driver: WebDriver = None
    is_connected: bool = False
    status: E5SeleniumWebdriverStatus = E5SeleniumWebdriverStatus()

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

    # E5
    def get_soup(self, error_context: str) -> None:
        try:
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as ex:
            self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                           error_context=error_context, exception=ex)

    # E5
    @staticmethod
    def log_info(message: str) -> None:
        logging.info(msg=message)

    # E5
    @staticmethod
    def log_warning(message: str) -> None:
        logging.warning(msg=message)

    ####################################################### PARSE ######################################################
    # E5
    def parse_active_seasons_over_05_goals_iframes(self) -> None:
        # Query Over 0.5 Goals Iframe (Active Seasons)
        active_over_05_goals_iframes: QuerySet[E5Over05GoalsIframe] = E5Over05GoalsIframe.objects.filter(
            season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_over_05_goals_iframes()"
            for active_over_05_goals_iframe in active_over_05_goals_iframes:
                active_over_05_goals_iframe: E5Over05GoalsIframe  # Type hinting for Intellij

                ########################################### Over 0.5 Goals #############################################
                # Get Url
                try:
                    self.driver.get(active_over_05_goals_iframe.over_05_goals_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 0.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 0.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 0.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 0.5 Goals Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_05_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_05_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_05_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_05_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_05_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_05_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_05_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 0.5 Goals Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 0.5 Goals Home Stats
                    home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    home_over_05_goals_stats.team = home_team
                    home_over_05_goals_stats.home_matches_played = home_matches_played
                    home_over_05_goals_stats.home_over_05_goals = home_over_05_goals
                    home_over_05_goals_stats.home_over_05_goals_percent = home_over_05_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_05_goals_stats.exists():
                        home_over_05_goals_stats.save()
                    else:
                        target_home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_05_goals_stats.home_matches_played = home_matches_played
                        target_home_over_05_goals_stats.home_over_05_goals = home_over_05_goals
                        target_home_over_05_goals_stats.home_over_05_goals_percent = home_over_05_goals_percent
                        target_home_over_05_goals_stats.save()

                    # Create Over 0.5 Goals Away Stats
                    away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    away_over_05_goals_stats.team = away_team
                    away_over_05_goals_stats.away_matches_played = away_matches_played
                    away_over_05_goals_stats.away_over_05_goals = away_over_05_goals
                    away_over_05_goals_stats.away_over_05_goals_percent = away_over_05_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_05_goals_stats.exists():
                        away_over_05_goals_stats.save()
                    else:
                        target_away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_05_goals_stats.away_matches_played = away_matches_played
                        target_away_over_05_goals_stats.away_over_05_goals = away_over_05_goals
                        target_away_over_05_goals_stats.away_over_05_goals_percent = away_over_05_goals_percent
                        target_away_over_05_goals_stats.save()

                    # Create Over 0.5 Goals Overall Stats
                    overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    overall_over_05_goals_stats.team = overall_team
                    overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_05_goals_stats.overall_over_05_goals = overall_over_05_goals
                    overall_over_05_goals_stats.overall_over_05_goals_percent = overall_over_05_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_05_goals_stats.exists():
                        overall_over_05_goals_stats.save()
                    else:
                        target_overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_05_goals_stats.overall_over_05_goals = overall_over_05_goals
                        target_overall_over_05_goals_stats.overall_over_05_goals_percent = overall_over_05_goals_percent
                        target_overall_over_05_goals_stats.save()

                ######################################### Over 0.5 Goals 1H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_05_goals_iframe.over_05_goals_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except NoSuchElementException as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 0.5 Goals 1H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_05_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_05_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_05_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_05_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_05_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_05_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_05_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 0.5 Goals 1H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 0.5 Goals 1H Home Stats
                    home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    home_over_05_goals_stats.team = home_team
                    home_over_05_goals_stats.home_matches_played = home_matches_played
                    home_over_05_goals_stats.home_over_05_goals_1h = home_over_05_goals
                    home_over_05_goals_stats.home_over_05_goals_1h_percent = home_over_05_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_05_goals_stats.exists():
                        home_over_05_goals_stats.save()
                    else:
                        target_home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_05_goals_stats.home_matches_played = home_matches_played
                        target_home_over_05_goals_stats.home_over_05_goals_1h = home_over_05_goals
                        target_home_over_05_goals_stats.home_over_05_goals_1h_percent = home_over_05_goals_percent
                        target_home_over_05_goals_stats.save()

                    # Create Over 0.5 Goals 1H Away Stats
                    away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    away_over_05_goals_stats.team = away_team
                    away_over_05_goals_stats.away_matches_played = away_matches_played
                    away_over_05_goals_stats.away_over_05_goals_1h = away_over_05_goals
                    away_over_05_goals_stats.away_over_05_goals_1h_percent = away_over_05_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_05_goals_stats.exists():
                        away_over_05_goals_stats.save()
                    else:
                        target_away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_05_goals_stats.away_matches_played = away_matches_played
                        target_away_over_05_goals_stats.away_over_05_goals_1h = away_over_05_goals
                        target_away_over_05_goals_stats.away_over_05_goals_1h_percent = away_over_05_goals_percent
                        target_away_over_05_goals_stats.save()

                    # Create Over 0.5 Goals 1H Overall Stats
                    overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    overall_over_05_goals_stats.team = overall_team
                    overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_05_goals_stats.overall_over_05_goals_1h = overall_over_05_goals
                    overall_over_05_goals_stats.overall_over_05_goals_1h_percent = overall_over_05_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_05_goals_stats.exists():
                        overall_over_05_goals_stats.save()
                    else:
                        target_overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_05_goals_stats.overall_over_05_goals_1h = overall_over_05_goals
                        target_overall_over_05_goals_stats.overall_over_05_goals_1h_percent = overall_over_05_goals_percent
                        target_overall_over_05_goals_stats.save()

                ######################################### Over 0.5 Goals 2H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_05_goals_iframe.over_05_goals_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 0.5 Goals 2H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_05_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_05_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_05_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_05_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_05_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_05_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_05_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 0.5 Goals 2H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 0.5 Goals 2H Home Stats
                    home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    home_over_05_goals_stats.team = home_team
                    home_over_05_goals_stats.home_matches_played = home_matches_played
                    home_over_05_goals_stats.home_over_05_goals_2h = home_over_05_goals
                    home_over_05_goals_stats.home_over_05_goals_2h_percent = home_over_05_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_05_goals_stats.exists():
                        home_over_05_goals_stats.save()
                    else:
                        target_home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_05_goals_stats.home_matches_played = home_matches_played
                        target_home_over_05_goals_stats.home_over_05_goals_2h = home_over_05_goals
                        target_home_over_05_goals_stats.home_over_05_goals_2h_percent = home_over_05_goals_percent
                        target_home_over_05_goals_stats.save()

                    # Create Over 0.5 Goals 2H Away Stats
                    away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    away_over_05_goals_stats.team = away_team
                    away_over_05_goals_stats.away_matches_played = away_matches_played
                    away_over_05_goals_stats.away_over_05_goals_2h = away_over_05_goals
                    away_over_05_goals_stats.away_over_05_goals_2h_percent = away_over_05_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_05_goals_stats.exists():
                        away_over_05_goals_stats.save()
                    else:
                        target_away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_05_goals_stats.away_matches_played = away_matches_played
                        target_away_over_05_goals_stats.away_over_05_goals_2h = away_over_05_goals
                        target_away_over_05_goals_stats.away_over_05_goals_2h_percent = away_over_05_goals_percent
                        target_away_over_05_goals_stats.save()

                    # Create Over 0.5 Goals 2H Overall Stats
                    overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    overall_over_05_goals_stats.team = overall_team
                    overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_05_goals_stats.overall_over_05_goals_2h = overall_over_05_goals
                    overall_over_05_goals_stats.overall_over_05_goals_2h_percent = overall_over_05_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_05_goals_stats.exists():
                        overall_over_05_goals_stats.save()
                    else:
                        target_overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_05_goals_stats.overall_over_05_goals_2h = overall_over_05_goals
                        target_overall_over_05_goals_stats.overall_over_05_goals_2h_percent = overall_over_05_goals_percent
                        target_overall_over_05_goals_stats.save()

                ######################################### Over 0.5 Goals BH ############################################
                # Get Url
                try:
                    self.driver.get(active_over_05_goals_iframe.over_05_goals_bh_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 0.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")

                # Get Over 0.5 Goals BH Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_05_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_05_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_05_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_05_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_05_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_05_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_05_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_05_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 0.5 Goals BH Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 0.5 Goals BH Home Stats
                    home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    home_over_05_goals_stats.team = home_team
                    home_over_05_goals_stats.home_matches_played = home_matches_played
                    home_over_05_goals_stats.home_over_05_goals_bh = home_over_05_goals
                    home_over_05_goals_stats.home_over_05_goals_bh_percent = home_over_05_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_05_goals_stats.exists():
                        home_over_05_goals_stats.save()
                    else:
                        target_home_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_05_goals_stats.home_matches_played = home_matches_played
                        target_home_over_05_goals_stats.home_over_05_goals_bh = home_over_05_goals
                        target_home_over_05_goals_stats.home_over_05_goals_bh_percent = home_over_05_goals_percent
                        target_home_over_05_goals_stats.save()

                    # Create Over 0.5 Goals BH Away Stats
                    away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    away_over_05_goals_stats.team = away_team
                    away_over_05_goals_stats.away_matches_played = away_matches_played
                    away_over_05_goals_stats.away_over_05_goals_bh = away_over_05_goals
                    away_over_05_goals_stats.away_over_05_goals_bh_percent = away_over_05_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_05_goals_stats.exists():
                        away_over_05_goals_stats.save()
                    else:
                        target_away_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_05_goals_stats.away_matches_played = away_matches_played
                        target_away_over_05_goals_stats.away_over_05_goals_bh = away_over_05_goals
                        target_away_over_05_goals_stats.away_over_05_goals_bh_percent = away_over_05_goals_percent
                        target_away_over_05_goals_stats.save()

                    # Create Over 0.5 Goals BH Overall Stats
                    overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats()
                    overall_over_05_goals_stats.team = overall_team
                    overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_05_goals_stats.overall_over_05_goals_bh = overall_over_05_goals
                    overall_over_05_goals_stats.overall_over_05_goals_bh_percent = overall_over_05_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_05_goals_stats.exists():
                        overall_over_05_goals_stats.save()
                    else:
                        target_overall_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_05_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_05_goals_stats.overall_over_05_goals_bh = overall_over_05_goals
                        target_overall_over_05_goals_stats.overall_over_05_goals_bh_percent = overall_over_05_goals_percent
                        target_overall_over_05_goals_stats.save()

    # E5
    def parse_active_seasons_over_15_goals_iframes(self) -> None:
        # Query Over 1.5 Goals Iframe (Active Seasons)
        active_over_15_goals_iframes: QuerySet[E5Over15GoalsIframe] = E5Over15GoalsIframe.objects.filter(
            season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_over_15_goals_iframes()"
            for active_over_15_goals_iframe in active_over_15_goals_iframes:
                active_over_15_goals_iframe: E5Over15GoalsIframe  # Type hinting for Intellij

                ########################################### Over 1.5 Goals #############################################
                # Get Url
                try:
                    self.driver.get(active_over_15_goals_iframe.over_15_goals_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 1.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 1.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context,
                        exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 1.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 1.5 Goals Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_15_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_15_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_15_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_15_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_15_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_15_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_15_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 1.5 Goals Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 1.5 Goals Home Stats
                    home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    home_over_15_goals_stats.team = home_team
                    home_over_15_goals_stats.home_matches_played = home_matches_played
                    home_over_15_goals_stats.home_over_15_goals = home_over_15_goals
                    home_over_15_goals_stats.home_over_15_goals_percent = home_over_15_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_15_goals_stats.exists():
                        home_over_15_goals_stats.save()
                    else:
                        target_home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_15_goals_stats.home_matches_played = home_matches_played
                        target_home_over_15_goals_stats.home_over_15_goals = home_over_15_goals
                        target_home_over_15_goals_stats.home_over_15_goals_percent = home_over_15_goals_percent
                        target_home_over_15_goals_stats.save()

                    # Create Over 1.5 Goals Away Stats
                    away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    away_over_15_goals_stats.team = away_team
                    away_over_15_goals_stats.away_matches_played = away_matches_played
                    away_over_15_goals_stats.away_over_15_goals = away_over_15_goals
                    away_over_15_goals_stats.away_over_15_goals_percent = away_over_15_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_15_goals_stats.exists():
                        away_over_15_goals_stats.save()
                    else:
                        target_away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_15_goals_stats.away_matches_played = away_matches_played
                        target_away_over_15_goals_stats.away_over_15_goals = away_over_15_goals
                        target_away_over_15_goals_stats.away_over_15_goals_percent = away_over_15_goals_percent
                        target_away_over_15_goals_stats.save()

                    # Create Over 1.5 Goals Overall Stats
                    overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    overall_over_15_goals_stats.team = overall_team
                    overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_15_goals_stats.overall_over_15_goals = overall_over_15_goals
                    overall_over_15_goals_stats.overall_over_15_goals_percent = overall_over_15_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_15_goals_stats.exists():
                        overall_over_15_goals_stats.save()
                    else:
                        target_overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_15_goals_stats.overall_over_15_goals = overall_over_15_goals
                        target_overall_over_15_goals_stats.overall_over_15_goals_percent = overall_over_15_goals_percent
                        target_overall_over_15_goals_stats.save()

                ######################################### Over 1.5 Goals 1H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_15_goals_iframe.over_15_goals_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 1.5 Goals 1H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_15_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_15_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_15_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_15_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_15_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_15_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_15_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 1.5 Goals 1H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 1.5 Goals 1H Home Stats
                    home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    home_over_15_goals_stats.team = home_team
                    home_over_15_goals_stats.home_matches_played = home_matches_played
                    home_over_15_goals_stats.home_over_15_goals_1h = home_over_15_goals
                    home_over_15_goals_stats.home_over_15_goals_1h_percent = home_over_15_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_15_goals_stats.exists():
                        home_over_15_goals_stats.save()
                    else:
                        target_home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_15_goals_stats.home_matches_played = home_matches_played
                        target_home_over_15_goals_stats.home_over_15_goals_1h = home_over_15_goals
                        target_home_over_15_goals_stats.home_over_15_goals_1h_percent = home_over_15_goals_percent
                        target_home_over_15_goals_stats.save()

                    # Create Over 1.5 Goals 1H Away Stats
                    away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    away_over_15_goals_stats.team = away_team
                    away_over_15_goals_stats.away_matches_played = away_matches_played
                    away_over_15_goals_stats.away_over_15_goals_1h = away_over_15_goals
                    away_over_15_goals_stats.away_over_15_goals_1h_percent = away_over_15_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_15_goals_stats.exists():
                        away_over_15_goals_stats.save()
                    else:
                        target_away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_15_goals_stats.away_matches_played = away_matches_played
                        target_away_over_15_goals_stats.away_over_15_goals_1h = away_over_15_goals
                        target_away_over_15_goals_stats.away_over_15_goals_1h_percent = away_over_15_goals_percent
                        target_away_over_15_goals_stats.save()

                    # Create Over 1.5 Goals 1H Overall Stats
                    overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    overall_over_15_goals_stats.team = overall_team
                    overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_15_goals_stats.overall_over_15_goals_1h = overall_over_15_goals
                    overall_over_15_goals_stats.overall_over_15_goals_1h_percent = overall_over_15_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_15_goals_stats.exists():
                        overall_over_15_goals_stats.save()
                    else:
                        target_overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_15_goals_stats.overall_over_15_goals_1h = overall_over_15_goals
                        target_overall_over_15_goals_stats.overall_over_15_goals_1h_percent = overall_over_15_goals_percent
                        target_overall_over_15_goals_stats.save()

                ######################################### Over 1.5 Goals 2H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_15_goals_iframe.over_15_goals_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 1.5 Goals 2H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_15_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_15_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_15_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_15_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_15_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_15_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_15_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 1.5 Goals 2H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 1.5 Goals 2H Home Stats
                    home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    home_over_15_goals_stats.team = home_team
                    home_over_15_goals_stats.home_matches_played = home_matches_played
                    home_over_15_goals_stats.home_over_15_goals_2h = home_over_15_goals
                    home_over_15_goals_stats.home_over_15_goals_2h_percent = home_over_15_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_15_goals_stats.exists():
                        home_over_15_goals_stats.save()
                    else:
                        target_home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_15_goals_stats.home_matches_played = home_matches_played
                        target_home_over_15_goals_stats.home_over_15_goals_2h = home_over_15_goals
                        target_home_over_15_goals_stats.home_over_15_goals_2h_percent = home_over_15_goals_percent
                        target_home_over_15_goals_stats.save()

                    # Create Over 1.5 Goals 2H Away Stats
                    away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    away_over_15_goals_stats.team = away_team
                    away_over_15_goals_stats.away_matches_played = away_matches_played
                    away_over_15_goals_stats.away_over_15_goals_2h = away_over_15_goals
                    away_over_15_goals_stats.away_over_15_goals_2h_percent = away_over_15_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_15_goals_stats.exists():
                        away_over_15_goals_stats.save()
                    else:
                        target_away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_15_goals_stats.away_matches_played = away_matches_played
                        target_away_over_15_goals_stats.away_over_15_goals_2h = away_over_15_goals
                        target_away_over_15_goals_stats.away_over_15_goals_2h_percent = away_over_15_goals_percent
                        target_away_over_15_goals_stats.save()

                    # Create Over 1.5 Goals 2H Overall Stats
                    overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    overall_over_15_goals_stats.team = overall_team
                    overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_15_goals_stats.overall_over_15_goals_2h = overall_over_15_goals
                    overall_over_15_goals_stats.overall_over_15_goals_2h_percent = overall_over_15_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_15_goals_stats.exists():
                        overall_over_15_goals_stats.save()
                    else:
                        target_overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_15_goals_stats.overall_over_15_goals_2h = overall_over_15_goals
                        target_overall_over_15_goals_stats.overall_over_15_goals_2h_percent = overall_over_15_goals_percent
                        target_overall_over_15_goals_stats.save()

                ######################################### Over 1.5 Goals BH ############################################
                # Get Url
                try:
                    self.driver.get(active_over_15_goals_iframe.over_15_goals_bh_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 1.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 1.5 Goals BH Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_15_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_15_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_15_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_15_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_15_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_15_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_15_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_15_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 1.5 Goals BH Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 1.5 Goals BH Home Stats
                    home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    home_over_15_goals_stats.team = home_team
                    home_over_15_goals_stats.home_matches_played = home_matches_played
                    home_over_15_goals_stats.home_over_15_goals_bh = home_over_15_goals
                    home_over_15_goals_stats.home_over_15_goals_bh_percent = home_over_15_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_15_goals_stats.exists():
                        home_over_15_goals_stats.save()
                    else:
                        target_home_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_15_goals_stats.home_matches_played = home_matches_played
                        target_home_over_15_goals_stats.home_over_15_goals_bh = home_over_15_goals
                        target_home_over_15_goals_stats.home_over_15_goals_bh_percent = home_over_15_goals_percent
                        target_home_over_15_goals_stats.save()

                    # Create Over 1.5 Goals BH Away Stats
                    away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    away_over_15_goals_stats.team = away_team
                    away_over_15_goals_stats.away_matches_played = away_matches_played
                    away_over_15_goals_stats.away_over_15_goals_bh = away_over_15_goals
                    away_over_15_goals_stats.away_over_15_goals_bh_percent = away_over_15_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_15_goals_stats.exists():
                        away_over_15_goals_stats.save()
                    else:
                        target_away_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_15_goals_stats.away_matches_played = away_matches_played
                        target_away_over_15_goals_stats.away_over_15_goals_bh = away_over_15_goals
                        target_away_over_15_goals_stats.away_over_15_goals_bh_percent = away_over_15_goals_percent
                        target_away_over_15_goals_stats.save()

                    # Create Over 1.5 Goals BH Overall Stats
                    overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats()
                    overall_over_15_goals_stats.team = overall_team
                    overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_15_goals_stats.overall_over_15_goals_bh = overall_over_15_goals
                    overall_over_15_goals_stats.overall_over_15_goals_bh_percent = overall_over_15_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_15_goals_stats.exists():
                        overall_over_15_goals_stats.save()
                    else:
                        target_overall_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_15_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_15_goals_stats.overall_over_15_goals_bh = overall_over_15_goals
                        target_overall_over_15_goals_stats.overall_over_15_goals_bh_percent = overall_over_15_goals_percent
                        target_overall_over_15_goals_stats.save()

    # E5
    def parse_active_seasons_over_25_goals_iframes(self) -> None:
        # Query Over 2.5 Goals Iframe (Active Seasons)
        active_over_25_goals_iframes: QuerySet[E5Over25GoalsIframe] = E5Over25GoalsIframe.objects.filter(
            season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_over_25_goals_iframes()"
            for active_over_25_goals_iframe in active_over_25_goals_iframes:
                active_over_25_goals_iframe: E5Over25GoalsIframe  # Type hinting for Intellij

                ########################################### Over 2.5 Goals #############################################
                # Get Url
                try:
                    self.driver.get(active_over_25_goals_iframe.over_25_goals_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 2.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 2.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 2.5 Goals Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_25_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 2.5 Goals Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 2.5 Goals Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()

                    # Create Over 2.5 Goals Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()

                    # Create Over 2.5 Goals Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()

                ######################################### Over 2.5 Goals 1H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_25_goals_iframe.over_25_goals_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")

                # Get Over 2.5 Goals 1H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_25_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 2.5 Goals 1H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 2.5 Goals 1H Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_1h = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_1h_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_1h = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_1h_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()

                    # Create Over 2.5 Goals 1H Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_1h = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_1h_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_1h = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_1h_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()

                    # Create Over 2.5 Goals 1H Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_1h = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_1h_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_1h = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_1h_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()

                ######################################### Over 2.5 Goals 2H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_25_goals_iframe.over_25_goals_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 2.5 Goals 2H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_25_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 2.5 Goals 2H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 2.5 Goals 2H Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_2h = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_2h_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_2h = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_2h_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()

                    # Create Over 2.5 Goals 2H Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_2h = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_2h_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_2h = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_2h_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()

                    # Create Over 2.5 Goals 2H Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_2h = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_2h_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_2h = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_2h_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()

                ######################################### Over 2.5 Goals BH ############################################
                # Get Url
                try:
                    self.driver.get(active_over_25_goals_iframe.over_25_goals_bh_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 2.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 2.5 Goals BH Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_25_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_25_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 2.5 Goals BH Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 2.5 Goals BH Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_bh = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_bh_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_bh = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_bh_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()

                    # Create Over 2.5 Goals BH Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_bh = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_bh_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_bh = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_bh_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()

                    # Create Over 2.5 Goals BH Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_bh = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_bh_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_bh = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_bh_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()

    # E5
    def parse_active_seasons_over_35_goals_iframes(self) -> None:
        # Query Over 3.5 Goals Iframe (Active Seasons)
        active_over_35_goals_iframes: QuerySet[E5Over35GoalsIframe] = E5Over35GoalsIframe.objects.filter(
            season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_over_35_goals_iframes()"
            for active_over_35_goals_iframe in active_over_35_goals_iframes:
                active_over_35_goals_iframe: E5Over35GoalsIframe  # Type hinting for Intellij

                ########################################### Over 3.5 Goals #############################################
                # Get Url
                try:
                    self.driver.get(active_over_35_goals_iframe.over_35_goals_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 3.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(msg=f"Parse Active Seasons Over 3.5 Goals Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 3.5 Goals Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_35_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_35_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_35_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_35_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_35_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_35_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_35_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 3.5 Goals Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 3.5 Goals Home Stats
                    home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    home_over_35_goals_stats.team = home_team
                    home_over_35_goals_stats.home_matches_played = home_matches_played
                    home_over_35_goals_stats.home_over_35_goals = home_over_35_goals
                    home_over_35_goals_stats.home_over_35_goals_percent = home_over_35_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_35_goals_stats.exists():
                        home_over_35_goals_stats.save()
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()

                    # Create Over 3.5 Goals Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()

                    # Create Over 3.5 Goals Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()

                ######################################### Over 3.5 Goals 1H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_35_goals_iframe.over_35_goals_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 1H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 3.5 Goals 1H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_35_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_35_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_35_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_35_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_35_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_35_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_35_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 3.5 Goals 1H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 3.5 Goals 1H Home Stats
                    home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    home_over_35_goals_stats.team = home_team
                    home_over_35_goals_stats.home_matches_played = home_matches_played
                    home_over_35_goals_stats.home_over_35_goals_1h = home_over_35_goals
                    home_over_35_goals_stats.home_over_35_goals_1h_percent = home_over_35_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_35_goals_stats.exists():
                        home_over_35_goals_stats.save()
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_1h = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_1h_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()

                    # Create Over 3.5 Goals 1H Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_1h = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_1h_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_1h = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_1h_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()

                    # Create Over 3.5 Goals 1H Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_1h = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_1h_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_1h = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_1h_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()

                ######################################### Over 3.5 Goals 2H ############################################
                # Get Url
                try:
                    self.driver.get(active_over_35_goals_iframe.over_35_goals_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals 2H Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 3.5 Goals 2H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_35_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_35_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_35_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_35_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_35_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_35_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_35_goals_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 3.5 Goals 2H Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 3.5 Goals 2H Home Stats
                    home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    home_over_35_goals_stats.team = home_team
                    home_over_35_goals_stats.home_matches_played = home_matches_played
                    home_over_35_goals_stats.home_over_35_goals_2h = home_over_35_goals
                    home_over_35_goals_stats.home_over_35_goals_2h_percent = home_over_35_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_35_goals_stats.exists():
                        home_over_35_goals_stats.save()
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_2h = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_2h_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()

                    # Create Over 3.5 Goals 2H Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_2h = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_2h_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_2h = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_2h_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()

                    # Create Over 3.5 Goals 2H Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_2h = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_2h_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_2h = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_2h_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()

                ######################################### Over 3.5 Goals BH ############################################
                # Get Url
                try:
                    self.driver.get(active_over_35_goals_iframe.over_35_goals_bh_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Over 3.5 Goals BH Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Over 3.5 Goals BH Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_35_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_35_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_35_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_35_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_35_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_35_goals_percent: str = table_tr.select(selector='td')[14].text
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_over_35_goals_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_over_35_goals_iframe.season)
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                            error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Over 3.5 Goals BH Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Over 3.5 Goals BH Home Stats
                    home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    home_over_35_goals_stats.team = home_team
                    home_over_35_goals_stats.home_matches_played = home_matches_played
                    home_over_35_goals_stats.home_over_35_goals_bh = home_over_35_goals
                    home_over_35_goals_stats.home_over_35_goals_bh_percent = home_over_35_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_35_goals_stats.exists():
                        home_over_35_goals_stats.save()
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_bh = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_bh_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()

                    # Create Over 3.5 Goals BH Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_bh = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_bh_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_bh = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_bh_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()

                    # Create Over 3.5 Goals BH Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_bh = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_bh_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_bh = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_bh_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()

    # E5
    def parse_active_seasons_corners_iframes(self) -> None:
        # Query Corners Iframe (Active Seasons)
        active_corners_iframes: QuerySet[E5CornersIframes] = E5CornersIframes.objects.filter(season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_corners_iframes()"
            for active_corner_iframe in active_corners_iframes:
                active_corner_iframe: E5CornersIframes  # Type hinting for Intellij

                ######################################### Team Corner For 1H ###########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_for_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner For 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_1h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner For 1h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner 1h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_1h = home_corners_for_1h
                    home_team_corner_stats.home_corners_for_1h_average = home_corners_for_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_1h = home_corners_for_1h
                        target_home_team_corner_stats.home_corners_for_1h_average = home_corners_for_1h_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner 1h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_1h = away_corners_for_1h
                    away_team_corner_stats.away_corners_for_1h_average = away_corners_for_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_1h = away_corners_for_1h
                        target_away_team_corner_stats.away_corners_for_1h_average = away_corners_for_1h_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner 1h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_1h = overall_corners_for_1h
                    overall_team_corner_stats.overall_corners_for_1h_average = overall_corners_for_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_1h = overall_corners_for_1h
                        target_overall_team_corner_stats.overall_corners_for_1h_average = overall_corners_for_1h_average
                        target_overall_team_corner_stats.save()

                ######################################### Team Corner For 2H ###########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_for_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner For 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_2h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner For 2h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner 2h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_2h = home_corners_for_2h
                    home_team_corner_stats.home_corners_for_2h_average = home_corners_for_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_2h = home_corners_for_2h
                        target_home_team_corner_stats.home_corners_for_2h_average = home_corners_for_2h_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner 2h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_2h = away_corners_for_2h
                    away_team_corner_stats.away_corners_for_2h_average = away_corners_for_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_2h = away_corners_for_2h
                        target_away_team_corner_stats.away_corners_for_2h_average = away_corners_for_2h_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner 2h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_2h = overall_corners_for_2h
                    overall_team_corner_stats.overall_corners_for_2h_average = overall_corners_for_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_2h = overall_corners_for_2h
                        target_overall_team_corner_stats.overall_corners_for_2h_average = overall_corners_for_2h_average
                        target_overall_team_corner_stats.save()

                ######################################### Team Corner For Ft ###########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_for_ft_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner For Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner For Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_ft_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner For Ft Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner Ft Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_ft = home_corners_for_ft
                    home_team_corner_stats.home_corners_for_ft_average = home_corners_for_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_ft = home_corners_for_ft
                        target_home_team_corner_stats.home_corners_for_ft_average = home_corners_for_ft_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner Ft Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_ft = away_corners_for_ft
                    away_team_corner_stats.away_corners_for_ft_average = away_corners_for_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_ft = away_corners_for_ft
                        target_away_team_corner_stats.away_corners_for_ft_average = away_corners_for_ft_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner Ft Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_ft = overall_corners_for_ft
                    overall_team_corner_stats.overall_corners_for_ft_average = overall_corners_for_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_ft = overall_corners_for_ft
                        target_overall_team_corner_stats.overall_corners_for_ft_average = overall_corners_for_ft_average
                        target_overall_team_corner_stats.save()

                ####################################### Team Corner Against 1H #########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_against_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner Against 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_1h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner Against 1h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner 1h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_1h = home_corners_against_1h
                    home_team_corner_stats.home_corners_against_1h_average = home_corners_against_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_1h = home_corners_against_1h
                        target_home_team_corner_stats.home_corners_against_1h_average = home_corners_against_1h_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner 1h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_1h = away_corners_against_1h
                    away_team_corner_stats.away_corners_against_1h_average = away_corners_against_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_1h = away_corners_against_1h
                        target_away_team_corner_stats.away_corners_against_1h_average = away_corners_against_1h_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner 1h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_1h = overall_corners_against_1h
                    overall_team_corner_stats.overall_corners_against_1h_average = overall_corners_against_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_1h = overall_corners_against_1h
                        target_overall_team_corner_stats.overall_corners_against_1h_average = overall_corners_against_1h_average
                        target_overall_team_corner_stats.save()

                ######################################### Team Corner Against 2H ###########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_against_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Against For 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner Against 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_2h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner Against 2h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner 2h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_2h = home_corners_against_2h
                    home_team_corner_stats.home_corners_against_2h_average = home_corners_against_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_2h = home_corners_against_2h
                        target_home_team_corner_stats.home_corners_against_2h_average = home_corners_against_2h_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner 2h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_2h = away_corners_against_2h
                    away_team_corner_stats.away_corners_against_2h_average = away_corners_against_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_2h = away_corners_against_2h
                        target_away_team_corner_stats.away_corners_against_2h_average = away_corners_against_2h_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner 2h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_2h = overall_corners_against_2h
                    overall_team_corner_stats.overall_corners_against_2h_average = overall_corners_against_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_2h = overall_corners_against_2h
                        target_overall_team_corner_stats.overall_corners_against_2h_average = overall_corners_against_2h_average
                        target_overall_team_corner_stats.save()

                ######################################### Team Corner Against Ft ###########################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.team_corners_against_ft_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Team Corner Against Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Team Corner Against Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_ft_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Team Corner Against Ft Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Team Corner Ft Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_ft = home_corners_against_ft
                    home_team_corner_stats.home_corners_against_ft_average = home_corners_against_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_ft = home_corners_against_ft
                        target_home_team_corner_stats.home_corners_against_ft_average = home_corners_against_ft_average
                        target_home_team_corner_stats.save()

                    # Create Team Corner Ft Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_ft = away_corners_against_ft
                    away_team_corner_stats.away_corners_against_ft_average = away_corners_against_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_ft = away_corners_against_ft
                        target_away_team_corner_stats.away_corners_against_ft_average = away_corners_against_ft_average
                        target_away_team_corner_stats.save()

                    # Create Team Corner Ft Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_ft = overall_corners_against_ft
                    overall_team_corner_stats.overall_corners_against_ft_average = overall_corners_against_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_ft = overall_corners_against_ft
                        target_overall_team_corner_stats.overall_corners_against_ft_average = overall_corners_against_ft_average
                        target_overall_team_corner_stats.save()

                ########################################### Match Corner 1H ############################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.match_corners_1h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 1h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Match Corner 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_1h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Match Corner 1h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Match Corner 1h Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_1h = home_corners_1h
                    home_match_corner_stats.home_corners_1h_average = home_corners_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_1h = home_corners_1h
                        target_home_match_corner_stats.home_corners_1h_average = home_corners_1h_average
                        target_home_match_corner_stats.save()

                    # Create Match Corner 1h Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_1h = away_corners_1h
                    away_match_corner_stats.away_corners_1h_average = away_corners_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_1h = away_corners_1h
                        target_away_match_corner_stats.away_corners_1h_average = away_corners_1h_average
                        target_away_match_corner_stats.save()

                    # Create Match Corner 1h Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_1h = overall_corners_1h
                    overall_match_corner_stats.overall_corners_1h_average = overall_corners_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_1h = overall_corners_1h
                        target_overall_match_corner_stats.overall_corners_1h_average = overall_corners_1h_average
                        target_overall_match_corner_stats.save()

                ########################################### Match Corner 2H ############################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.match_corners_2h_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner 2h Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Match Corner 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_2h_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Match Corner 2h Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Match Corner 2h Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_2h = home_corners_2h
                    home_match_corner_stats.home_corners_2h_average = home_corners_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_2h = home_corners_2h
                        target_home_match_corner_stats.home_corners_2h_average = home_corners_2h_average
                        target_home_match_corner_stats.save()

                    # Create Match Corner 2h Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_2h = away_corners_2h
                    away_match_corner_stats.away_corners_2h_average = away_corners_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_2h = away_corners_2h
                        target_away_match_corner_stats.away_corners_2h_average = away_corners_2h_average
                        target_away_match_corner_stats.save()

                    # Create Match Corner 2h Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_2h = overall_corners_2h
                    overall_match_corner_stats.overall_corners_2h_average = overall_corners_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_2h = overall_corners_2h
                        target_overall_match_corner_stats.overall_corners_2h_average = overall_corners_2h_average
                        target_overall_match_corner_stats.save()

                ########################################### Match Corner Ft ############################################
                # Get Url
                try:
                    self.driver.get(active_corner_iframe.match_corners_ft_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs: ResultSet[Tag] = soup.select(selector='table.waffle.no-grid tr')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                                   error_context=error_context, exception=ex)
                    logging.warning(
                        msg=f"Parse Active Seasons Match Corner Ft Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Match Corner Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_ft_average: float = float(table_tr.select(selector='td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_corner_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_corner_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_corner_iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        logging.warning(
                            msg=f"Parse Active Seasons Match Corner Ft Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Match Corner Ft Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_ft = home_corners_ft
                    home_match_corner_stats.home_corners_ft_average = home_corners_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_ft = home_corners_ft
                        target_home_match_corner_stats.home_corners_ft_average = home_corners_ft_average
                        target_home_match_corner_stats.save()

                    # Create Match Corner Ft Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_ft = away_corners_ft
                    away_match_corner_stats.away_corners_ft_average = away_corners_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_ft = away_corners_ft
                        target_away_match_corner_stats.away_corners_ft_average = away_corners_ft_average
                        target_away_match_corner_stats.save()

                    # Create Match Corner Ft Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_ft = overall_corners_ft
                    overall_match_corner_stats.overall_corners_ft_average = overall_corners_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_ft = overall_corners_ft
                        target_overall_match_corner_stats.overall_corners_ft_average = overall_corners_ft_average
                        target_overall_match_corner_stats.save()

    # E5
    def parse_active_seasons_cards_iframes(self) -> None:
        # Query Cards Iframe (Active Seasons)
        active_cards_iframes: QuerySet[E5CardsIframes] = E5CardsIframes.objects.filter(season__active=True)

        # Check connection
        self.check_is_connected()

        if self.status.success:
            error_context: str = "parse_active_seasons_cards_iframes()"
            for active_card_iframe in active_cards_iframes:
                active_card_iframe: E5CardsIframes  # Type hinting for Intellij

                ########################################## Yellow Cards For ############################################
                # Get Url
                try:
                    self.driver.get(active_card_iframe.yellow_cards_for_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Yellow Card For Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Yellow Card For Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs = soup.find('table', class_='waffle no-grid').find_all('tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context,
                        exception=ex)
                    logging.warning(msg=f"Parse Active Yellow Card For Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")

                # Get Yellow Cards For Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_yellow_cards_for: int = int(table_tr.find_all('td')[3].text)
                        home_yellow_cards_for_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_yellow_cards_for: int = int(table_tr.find_all('td')[8].text)
                        away_yellow_cards_for_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_yellow_cards_for: int = int(table_tr.find_all('td')[13].text)
                        overall_yellow_cards_for_average: float = float(table_tr.find_all('td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_card_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_card_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_card_iframe.season)
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                            error_context=error_context,
                            exception=ex)
                        logging.warning(
                            msg=f"Parse Active Yellow Card For Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Yellow Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_yellow_cards_for = home_yellow_cards_for
                    home_card_stats.home_yellow_cards_for_average = home_yellow_cards_for_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_yellow_cards_for = home_yellow_cards_for
                        target_home_card_stats.home_yellow_cards_for_average = home_yellow_cards_for_average
                        target_home_card_stats.save()

                    # Create Yellow Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_yellow_cards_for = away_yellow_cards_for
                    away_card_stats.away_yellow_cards_for_average = away_yellow_cards_for_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_yellow_cards_for = away_yellow_cards_for
                        target_away_card_stats.away_yellow_cards_for_average = away_yellow_cards_for_average
                        target_away_card_stats.save()

                    # Create Yellow Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_yellow_cards_for = overall_yellow_cards_for
                    overall_card_stats.overall_yellow_cards_for_average = overall_yellow_cards_for_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_yellow_cards_for = overall_yellow_cards_for
                        target_overall_card_stats.overall_yellow_cards_for_average = overall_yellow_cards_for_average
                        target_overall_card_stats.save()

                ######################################## Yellow Cards Against ##########################################
                # Get Url
                try:
                    self.driver.get(active_card_iframe.yellow_cards_against_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Yellow Card Against Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Yellow Card Against Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs = soup.find('table', class_='waffle no-grid').find_all('tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context,
                        exception=ex)
                    logging.warning(msg=f"Parse Active Yellow Card Against Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")

                # Get Yellow Cards Against Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_yellow_cards_against: int = int(table_tr.find_all('td')[3].text)
                        home_yellow_cards_against_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_yellow_cards_against: int = int(table_tr.find_all('td')[8].text)
                        away_yellow_cards_against_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_yellow_cards_against: int = int(table_tr.find_all('td')[13].text)
                        overall_yellow_cards_against_average: float = float(table_tr.find_all('td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_card_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_card_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_card_iframe.season)
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                            error_context=error_context,
                            exception=ex)
                        logging.warning(
                            msg=f"Parse Active Yellow Card Against Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Yellow Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_yellow_cards_against = home_yellow_cards_against
                    home_card_stats.home_yellow_cards_against_average = home_yellow_cards_against_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_yellow_cards_against = home_yellow_cards_against
                        target_home_card_stats.home_yellow_cards_against_average = home_yellow_cards_against_average
                        target_home_card_stats.save()

                    # Create Yellow Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_yellow_cards_against = away_yellow_cards_against
                    away_card_stats.away_yellow_cards_against_average = away_yellow_cards_against_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_yellow_cards_against = away_yellow_cards_against
                        target_away_card_stats.away_yellow_cards_against_average = away_yellow_cards_against_average
                        target_away_card_stats.save()

                    # Create Yellow Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_yellow_cards_against = overall_yellow_cards_against
                    overall_card_stats.overall_yellow_cards_against_average = overall_yellow_cards_against_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_yellow_cards_against = overall_yellow_cards_against
                        target_overall_card_stats.overall_yellow_cards_against_average = overall_yellow_cards_against_average
                        target_overall_card_stats.save()

                ############################################ Red Cards For #############################################
                # Get Url
                try:
                    self.driver.get(active_card_iframe.red_cards_for_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Red Card For Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Red Card For Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs = soup.find('table', class_='waffle no-grid').find_all('tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context,
                        exception=ex)
                    logging.warning(msg=f"Parse Active Red Card For Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")

                # Get Red Cards For Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_red_cards_for: int = int(table_tr.find_all('td')[3].text)
                        home_red_cards_for_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_red_cards_for: int = int(table_tr.find_all('td')[8].text)
                        away_red_cards_for_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_red_cards_for: int = int(table_tr.find_all('td')[13].text)
                        overall_red_cards_for_average: float = float(table_tr.find_all('td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_card_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_card_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_card_iframe.season)
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                            error_context=error_context,
                            exception=ex)
                        logging.warning(
                            msg=f"Parse Active Red Card For Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Red Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_red_cards_for = home_red_cards_for
                    home_card_stats.home_red_cards_for_average = home_red_cards_for_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_red_cards_for = home_red_cards_for
                        target_home_card_stats.home_red_cards_for_average = home_red_cards_for_average
                        target_home_card_stats.save()

                    # Create Red Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_red_cards_for = away_red_cards_for
                    away_card_stats.away_red_cards_for_average = away_red_cards_for_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_red_cards_for = away_red_cards_for
                        target_away_card_stats.away_red_cards_for_average = away_red_cards_for_average
                        target_away_card_stats.save()

                    # Create Red Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_red_cards_for = overall_red_cards_for
                    overall_card_stats.overall_red_cards_for_average = overall_red_cards_for_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_red_cards_for = overall_red_cards_for
                        target_overall_card_stats.overall_red_cards_for_average = overall_red_cards_for_average
                        target_overall_card_stats.save()

                ########################################## Red Cards Against ###########################################
                # Get Url
                try:
                    self.driver.get(active_card_iframe.red_cards_against_url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Red Card Against Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Soup
                try:
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=error_context,
                                   exception=ex)
                    logging.warning(
                        msg=f"Parse Active Red Card Against Iframe - {self.status.error_context} : "
                            f"{self.status.error_type} : {self.status.exception}")
                    continue

                # Get Table Trs
                try:
                    table_trs = soup.find('table', class_='waffle no-grid').find_all('tr')
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_TABLE_TR_FAILED,
                        error_context=error_context,
                        exception=ex)
                    logging.warning(msg=f"Parse Active Red Card Against Iframe - {self.status.error_context} : "
                                        f"{self.status.error_type} : {self.status.exception}")

                # Get Red Cards Against Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_red_cards_against: int = int(table_tr.find_all('td')[3].text)
                        home_red_cards_against_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_red_cards_against: int = int(table_tr.find_all('td')[8].text)
                        away_red_cards_against_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_red_cards_against: int = int(table_tr.find_all('td')[13].text)
                        overall_red_cards_against_average: float = float(table_tr.find_all('td')[14].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name,
                                                               season=active_card_iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name,
                                                               season=active_card_iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name,
                                                                  season=active_card_iframe.season)
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                            error_context=error_context,
                            exception=ex)
                        logging.warning(
                            msg=f"Parse Active Red Card Against Iframe - {self.status.error_context} : "
                                f"{self.status.error_type} : {self.status.exception}")
                        continue

                    # Create Red Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_red_cards_against = home_red_cards_against
                    home_card_stats.home_red_cards_against_average = home_red_cards_against_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_red_cards_against = home_red_cards_against
                        target_home_card_stats.home_red_cards_against_average = home_red_cards_against_average
                        target_home_card_stats.save()

                    # Create Red Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = home_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_red_cards_against = away_red_cards_against
                    away_card_stats.away_red_cards_against_average = away_red_cards_against_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_red_cards_against = away_red_cards_against
                        target_away_card_stats.away_red_cards_against_average = away_red_cards_against_average
                        target_away_card_stats.save()

                    # Create Red Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = home_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_red_cards_against = overall_red_cards_against
                    overall_card_stats.overall_red_cards_against_average = overall_red_cards_against_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_red_cards_against = overall_red_cards_against
                        target_overall_card_stats.overall_red_cards_against_average = overall_red_cards_against_average
                        target_overall_card_stats.save()
