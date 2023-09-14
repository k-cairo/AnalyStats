import dataclasses
import datetime
import logging
import time
from enum import Enum
from typing import Any, ClassVar

from bs4 import BeautifulSoup, ResultSet, Tag
from django.db.models import QuerySet, Q
from django.utils.text import slugify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from Website.models import (E5Season, E5CardsIframes, E5BttsIframes, E5Over05GoalsIframe, E5ScoredFirstIframe,
                            E5Over15GoalsIframe, E5Over25GoalsIframe, E5Over35GoalsIframe, E5CornersIframes,
                            E5ScoredBothHalfIframes, E5WonBothHalfIframes, E5League, E5LeagueTableIframe, E5Team,
                            E51st2ndHalfGoalsIframe, E5CleanSheetIframe, E5WonToNilIframe, E5WinLossMarginIframe,
                            E5WinDrawLossPercentageIframe, E5HalfTimeFullTimeIframe, E5RescuedPointsIframe,
                            E5Average1stGoalTimeIframe, E5AverageTeamGoalsIframe, E5EarlyGoalsIframe, E5LateGoalsIframe,
                            E5Fixture)

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
    ERROR_TYPE_SEASON_NAME_OR_URL_FAILED = "get_season_name_or_url_failed"
    ERROR_TYPE_TEAM_NAME_OR_URL_FAILED = "get_team_name_or_url_failed"
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
    ERROR_TYPE_GET_TABLE_TRS_FAILED = "get_table_trs_failed"
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
    LEAGUES: ClassVar[QuerySet[E5League]] = E5League.objects.all()
    LEAGUE_TABLE_IFRAMES: ClassVar[QuerySet[E5LeagueTableIframe]] = E5LeagueTableIframe.objects.filter(
        season__active=True)

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
            # service: Service = Service()
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument('--disable-dev-shm-usage')
            # self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver = webdriver.Chrome(options=chrome_options)
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
    def init_status(self) -> None:
        self.status.success = True
        self.status.error_type = E5SeleniumWebdriverError.ERROR_TYPE_NONE
        self.status.error_context = ""
        self.status.exception = ""

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
    def get_only(self, url: str, error_context: str):
        try:
            self.driver.get(url)
        except Exception as ex:
            self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                           error_context=error_context, exception=ex)

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

    ####################################################### UTILS ######################################################
    # E5
    @staticmethod
    def convert_to_date(date_str: str) -> datetime.date:
        date_list = date_str.split()
        date_list[1] = date_list[1][:-2]
        date_format = "%A %d %B %Y"
        return datetime.datetime.strptime(' '.join(date_list), date_format).date()

    ####################################################### BUILD ######################################################
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
            elif isinstance(iframe, E51st2ndHalfGoalsIframe):
                if idx == 0:
                    iframe.overall_1st_2nd_half_goals_url = iframe_url
                elif idx == 1:
                    iframe.home_1st_2nd_half_goals_url = iframe_url
                elif idx == 2:
                    iframe.away_1st_2nd_half_goals_url = iframe_url
            elif isinstance(iframe, E5CleanSheetIframe):
                if idx == 0:
                    iframe.clean_sheet_url = iframe_url
                elif idx == 1:
                    iframe.failed_to_score_url = iframe_url
            elif isinstance(iframe, E5WonToNilIframe):
                if idx == 0:
                    iframe.won_to_nil_url = iframe_url
                elif idx == 1:
                    iframe.lost_to_nil_url = iframe_url
            elif isinstance(iframe, E5WinLossMarginIframe):
                if idx == 0:
                    iframe.winning_margins_url = iframe_url
                elif idx == 1:
                    iframe.losing_margins_url = iframe_url
            elif isinstance(iframe, E5ScoredFirstIframe):
                if idx == 0:
                    iframe.scored_first_url = iframe_url
                elif idx == 1:
                    iframe.conceded_first_url = iframe_url

        return iframe

    @staticmethod
    def get_urls(iframe: object) -> list[str]:
        urls: list[str] = []

        if isinstance(iframe, E5LeagueTableIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5BttsIframes):
            urls = [iframe.btts_url, iframe.btts_1h_url, iframe.btts_2h_url, iframe.btts_bh_url,
                    iframe.btts_25_url]
        elif isinstance(iframe, E5Over05GoalsIframe):
            urls = [iframe.over_05_goals_url, iframe.over_05_goals_1h_url, iframe.over_05_goals_2h_url,
                    iframe.over_05_goals_bh_url]
        elif isinstance(iframe, E5Over15GoalsIframe):
            urls = [iframe.over_15_goals_url, iframe.over_15_goals_1h_url, iframe.over_15_goals_2h_url,
                    iframe.over_15_goals_bh_url]
        elif isinstance(iframe, E5Over25GoalsIframe):
            urls = [iframe.over_25_goals_url, iframe.over_25_goals_1h_url, iframe.over_25_goals_2h_url,
                    iframe.over_25_goals_bh_url]
        elif isinstance(iframe, E5Over35GoalsIframe):
            urls = [iframe.over_35_goals_url, iframe.over_35_goals_1h_url, iframe.over_35_goals_2h_url,
                    iframe.over_35_goals_bh_url]
        elif isinstance(iframe, E5CornersIframes):
            urls = [iframe.team_corners_for_1h_url, iframe.team_corners_against_1h_url,
                    iframe.team_corners_for_2h_url, iframe.team_corners_against_2h_url,
                    iframe.team_corners_for_ft_url, iframe.team_corners_against_ft_url,
                    iframe.match_corners_1h_url, iframe.match_corners_2h_url, iframe.match_corners_ft_url]
        elif isinstance(iframe, E5CardsIframes):
            urls = [iframe.yellow_cards_for_url, iframe.yellow_cards_against_url, iframe.red_cards_for_url,
                    iframe.red_cards_against_url]
        elif isinstance(iframe, E5WinDrawLossPercentageIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5HalfTimeFullTimeIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5ScoredBothHalfIframes):
            urls = [iframe.scored_both_half_url, iframe.conceded_both_half_url]
        elif isinstance(iframe, E5WonBothHalfIframes):
            urls = [iframe.won_both_half_url, iframe.won_both_half_url]
        elif isinstance(iframe, E51st2ndHalfGoalsIframe):
            urls = [iframe.overall_1st_2nd_half_goals_url, iframe.home_1st_2nd_half_goals_url,
                    iframe.away_1st_2nd_half_goals_url]
        elif isinstance(iframe, E5RescuedPointsIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5CleanSheetIframe):
            urls = [iframe.clean_sheet_url, iframe.failed_to_score_url]
        elif isinstance(iframe, E5WonToNilIframe):
            urls = [iframe.won_to_nil_url, iframe.lost_to_nil_url]
        elif isinstance(iframe, E5WinLossMarginIframe):
            urls = [iframe.winning_margins_url, iframe.losing_margins_url]
        elif isinstance(iframe, E5ScoredFirstIframe):
            urls = [iframe.scored_first_url, iframe.conceded_first_url]
        elif isinstance(iframe, E5Average1stGoalTimeIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5AverageTeamGoalsIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5EarlyGoalsIframe):
            urls = [iframe.url]
        elif isinstance(iframe, E5LateGoalsIframe):
            urls = [iframe.url]

        # Return
        return urls

    ######################################################## GET #######################################################
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
                        or "Peru" in league_name or "Tunisia" in league_name or "Uruguay" in league_name
                        or "England – Northern Premier League" in league_name or "Moldova" in league_name
                        or "England – Southern League South" in league_name
                        or "England – Southern League Central" in league_name
                        or "England – Isthmian League" in league_name or "Nigeria" in league_name):
                    continue

                # Check if league already exists
                if new_league.exists():
                    # Update League
                    target_league: E5League = E5League.objects.get(name=league_name)
                    target_league.url = league_url
                    target_league.slug = slugify(value=league_name)
                    target_league.save()
                else:
                    # Save League
                    new_league.save()

    # E5
    def get_seasons(self, error_context: str) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for league in self.LEAGUES:
                league: E5League  # Type hinting for Intellij

                # Get Url
                self.get(url=league.url, error_context=error_context)
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Season Name and Url
                try:
                    season_details: str = ""
                    season_details = self.soup.select(selector="div.textwidget.custom-html-widget p")[1].text
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_SEASON_NAME_OR_URL_FAILED,
                                   error_context=error_context, exception=ex)
                    self.init_status()
                    continue

                # Create Active Season
                active_season: E5Season = E5Season()
                active_season.name = season_details.split()[-1]
                active_season.league = league
                active_season.url = league.url
                active_season.active = True

                # Check if season already exists before saving or updating
                if not active_season.exists():
                    active_season.save()
                else:
                    target_active_season: E5Season = E5Season.objects.get(active=True, league=league,
                                                                          name=active_season.name)
                    target_active_season.url = league.url
                    target_active_season.save()

    # E5
    def get_teams(self, error_context: str) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for league_table in self.LEAGUE_TABLE_IFRAMES:
                league_table: E5LeagueTableIframe  # Type hinting for Intellij

                # Get Url
                self.get(url=league_table.url, error_context=error_context)
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Teams
                teams_a: ResultSet[Tag] = []
                teams_a = self.soup.select(selector="table.waffle.no-grid tr td a[target='_blank']")

                # Get Team
                for team_a in teams_a:
                    team_name: str = ""
                    team_url: str = ""
                    try:
                        team_name = team_a.text
                        team_url = team_a['href']
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_TEAM_NAME_OR_URL_FAILED,
                                       error_context=error_context, exception=ex)
                        self.init_status()
                        continue

                    # Create Team
                    team: E5Team = E5Team()
                    team.name = team_name
                    team.url = team_url
                    team.slug = slugify(value=team_name)
                    team.season = league_table.season

                    # Check if team already exists before saving or updating
                    if not team.exists():
                        team.save()
                    else:
                        target_team: E5Team = E5Team.objects.get(name=team_name, season=league_table.season)
                        target_team.url = team_url
                        target_team.slug = slugify(value=team_name)
                        target_team.save()

    # E5
    def get_upcoming_matches(self, error_context: str) -> None:
        endpoints: tuple = ("saturday-uk/", "saturday/", "sunday/", "monday/", "tuesday/", "wednesday/",
                            "thursday/", "friday")

        # Check connection
        self.check_is_connected()

        if self.status.success:
            for endpoint in endpoints:
                # Get Url
                self.get_only(url=f"https://www.thestatsdontlie.com/football/predictions/{endpoint}",
                              error_context=error_context)
                if not self.status.success:
                    self.init_status()
                    continue

                # Check if user and pass required
                try:
                    self.driver.find_element(by=By.ID, value="user_login").send_keys("cairo.kevin72@gmail.com")
                    self.driver.find_element(by=By.ID, value="user_pass").send_keys("31Mars1988")
                    self.driver.find_element(by=By.ID, value="wp-submit").click()
                    self.driver.implicitly_wait(10)
                except Exception:
                    pass

                # Get Soup
                self.get_soup(error_context=error_context)
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Upcoming Matches Date
                date_str: str = self.soup.select_one(selector="div.fusion-text.fusion-text-2 h1").text
                date_str += f" {datetime.datetime.now().year}"
                date: datetime.date = self.convert_to_date(date_str=date_str)

                # Check if date if newer than today
                if date < datetime.date.today():
                    continue

                # Get Upcoming Matches
                time.sleep(10)
                table_upcoming_matchs = self.soup.select(selector="table.supsystic-table")[1]
                if table_upcoming_matchs is None:
                    self.log_warning(message=f"Table upcoming matches not found for date {date}")
                    continue

                upcoming_matches_trs: ResultSet[Tag] = table_upcoming_matchs.select(selector="tbody tr")

                for upcoming_match_tr in upcoming_matches_trs:
                    league_str: str = upcoming_match_tr.select(selector="td")[0].text
                    kick_off: str = upcoming_match_tr.select(selector="td")[1].text
                    home_team_str: str = upcoming_match_tr.select(selector="td")[2].next.text
                    away_team_str: str = upcoming_match_tr.select(selector="td")[2].next.next.next.text[1:] # Remove space

                    if ("Colombia" in league_str or "Costa Rica" in league_str or "Ecuador" in league_str
                    or "Honduras" in league_str or "Mexico" in league_str or "Paraguay" in league_str
                    or "Peru" in league_str or "Tunisia" in league_str or "Uruguay" in league_str
                    or "England NL" in league_str or "Moldova" in league_str
                    or "England SL" in league_str or "England Isthmian" in league_str or "Nigeria" in league_str
                    or "Southern League South" in league_str or "Southern League Central" in league_str):
                        continue

                    # Get Teams
                    league_list: list[str] = league_str.split(" ")

                    try:
                        home_team: E5Team | None = E5Team.objects.filter(
                            Q(name__contains=home_team_str) &
                            Q(season__league__name__icontains=league_list[0]) &
                            Q(season__league__name__icontains=league_list[1])).get()
                        away_team: E5Team | None = E5Team.objects.filter(
                            Q(name__contains=away_team_str) &
                            Q(season__league__name__icontains=league_list[0]) &
                            Q(season__league__name__icontains=league_list[1])).get()
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=error_context, exception=ex)
                        self.init_status()
                        continue

                    # Build Upcoming Match
                    fixture: E5Fixture = E5Fixture()
                    fixture.home_team = home_team
                    fixture.away_team = away_team
                    fixture.date = date
                    fixture.slug = slugify(value=f"{home_team.name}-{away_team.name}")
                    fixture.kickoff_time = kick_off

                    # Check if fixture already exists
                    if not fixture.exists():
                        fixture.save()

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
                    self.init_status()
                    continue

                # Get Iframes
                stat_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check Iframes Length
                if len(stat_iframes) != iframe_length:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=error_context, exception=None)
                    self.init_status()
                    continue

                # Build Iframe
                iframe = self.build_iframe(season=season, stats_iframes=stat_iframes, error_context=error_context,
                                           iframe_class=class_)

                # Check Iframe Not Empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=error_context, exception=None)
                    self.init_status()
                    continue

                # Save Iframe
                if not iframe.exists():
                    iframe.save()
                else:
                    class_.update_iframe(season=season, iframe=iframe)

    # E5
    def get_iframe(self, endpoint: str, error_context: str, save_message: str, class_: Any):
        # Check Connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Init Status
                self.init_status()

                # Get Url
                self.get(url=f"{season.url}{endpoint}", error_context=error_context)
                if not self.status.success:
                    continue

                # Get Iframes
                stat_iframe: Tag | None = self.soup.select_one(selector="div.fusion-text.fusion-text-2 iframe")

                if stat_iframe is None and endpoint == "amr/":
                    # Get Another Url
                    self.get(url=f"{season.url}atg/", error_context=error_context)
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
                else:
                    class_.update_iframe(season=season, iframe=iframe)
