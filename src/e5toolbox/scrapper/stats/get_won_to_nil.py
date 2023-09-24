import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5WonToNilStats, E5Team, E5WonToNilIframe
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetWonToNil(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCleanSheets"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    WTN_IFRAMES: ClassVar[QuerySet[E5WonToNilIframe]] = E5WonToNilIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.WTN_IFRAMES:
                iframe: E5WonToNilIframe  # Type hinting for Intellij

                ############################################## Won To Nil ##############################################
                # Get Url
                self.get(url=iframe.won_to_nil_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_won_to_nil: int = 0
                    home_won_to_nil_percent: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_won_to_nil: int = 0
                    away_won_to_nil_percent: int = 0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_won_to_nil: int = 0
                    overall_won_to_nil_percent: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_won_to_nil: int = int(table_tr.find_all('td')[3].text)
                        home_won_to_nil_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_won_to_nil: int = int(table_tr.find_all('td')[8].text)
                        away_won_to_nil_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_won_to_nil: int = int(table_tr.find_all('td')[13].text)
                        overall_won_to_nil_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Home Stats
                    home_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    home_wtn_stats.team = home_team
                    home_wtn_stats.home_matches_played = home_matches_played
                    home_wtn_stats.home_won_to_nil = home_won_to_nil
                    home_wtn_stats.home_won_to_nil_percent = home_won_to_nil_percent

                    # Check if home stats already exists before saving or updating
                    if not home_wtn_stats.exists():
                        home_wtn_stats.save()
                    else:
                        home_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=home_team)
                        home_wtn_stats.home_matches_played = home_matches_played
                        home_wtn_stats.home_won_to_nil = home_won_to_nil
                        home_wtn_stats.home_won_to_nil_percent = home_won_to_nil_percent
                        home_wtn_stats.save()

                    # Create Away Stats
                    away_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    away_wtn_stats.team = away_team
                    away_wtn_stats.away_matches_played = away_matches_played
                    away_wtn_stats.away_won_to_nil = away_won_to_nil
                    away_wtn_stats.away_won_to_nil_percent = away_won_to_nil_percent

                    # Check if away stats already exists before saving or updating
                    if not away_wtn_stats.exists():
                        away_wtn_stats.save()
                    else:
                        away_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=away_team)
                        away_wtn_stats.away_matches_played = away_matches_played
                        away_wtn_stats.away_won_to_nil = away_won_to_nil
                        away_wtn_stats.away_won_to_nil_percent = away_won_to_nil_percent
                        away_wtn_stats.save()

                    # Create Overall Stats
                    overall_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    overall_wtn_stats.team = overall_team
                    overall_wtn_stats.overall_matches_played = overall_matches_played
                    overall_wtn_stats.overall_won_to_nil = overall_won_to_nil
                    overall_wtn_stats.overall_won_to_nil_percent = overall_won_to_nil_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_wtn_stats.exists():
                        overall_wtn_stats.save()
                    else:
                        overall_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=overall_team)
                        overall_wtn_stats.overall_matches_played = overall_matches_played
                        overall_wtn_stats.overall_won_to_nil = overall_won_to_nil
                        overall_wtn_stats.overall_won_to_nil_percent = overall_won_to_nil_percent
                        overall_wtn_stats.save()

                ############################################ Lost To Nil ###############################################
                # Get Url
                self.get(url=iframe.lost_to_nil_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_lost_to_nil: int = 0
                    home_lost_to_nil_percent: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_lost_to_nil: int = 0
                    away_lost_to_nil_percent: int = 0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_lost_to_nil: int = 0
                    overall_lost_to_nil_percent: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_lost_to_nil: int = int(table_tr.find_all('td')[3].text)
                        home_lost_to_nil_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_lost_to_nil: int = int(table_tr.find_all('td')[8].text)
                        away_lost_to_nil_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_lost_to_nil: int = int(table_tr.find_all('td')[13].text)
                        overall_lost_to_nil_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Home Stats
                    home_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    home_wtn_stats.team = home_team
                    home_wtn_stats.home_matches_played = home_matches_played
                    home_wtn_stats.home_lost_to_nil = home_lost_to_nil
                    home_wtn_stats.home_lost_to_nil_percent = home_lost_to_nil_percent

                    # Check if home stats already exists before saving or updating
                    if not home_wtn_stats.exists():
                        home_wtn_stats.save()
                    else:
                        home_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=home_team)
                        home_wtn_stats.home_matches_played = home_matches_played
                        home_wtn_stats.home_lost_to_nil = home_lost_to_nil
                        home_wtn_stats.home_lost_to_nil_percent = home_lost_to_nil_percent
                        home_wtn_stats.save()

                    # Create Away Stats
                    away_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    away_wtn_stats.team = away_team
                    away_wtn_stats.away_matches_played = away_matches_played
                    away_wtn_stats.away_lost_to_nil = away_lost_to_nil
                    away_wtn_stats.away_lost_to_nil_percent = away_lost_to_nil_percent

                    # Check if away stats already exists before saving or updating
                    if not away_wtn_stats.exists():
                        away_wtn_stats.save()
                    else:
                        away_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=away_team)
                        away_wtn_stats.away_matches_played = away_matches_played
                        away_wtn_stats.away_lost_to_nil = away_lost_to_nil
                        away_wtn_stats.away_lost_to_nil_percent = away_lost_to_nil_percent
                        away_wtn_stats.save()

                    # Create Overall Stats
                    overall_wtn_stats: E5WonToNilStats = E5WonToNilStats()
                    overall_wtn_stats.team = overall_team
                    overall_wtn_stats.overall_matches_played = overall_matches_played
                    overall_wtn_stats.overall_lost_to_nil = overall_lost_to_nil
                    overall_wtn_stats.overall_lost_to_nil_percent = overall_lost_to_nil_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_wtn_stats.exists():
                        overall_wtn_stats.save()
                    else:
                        overall_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=overall_team)
                        overall_wtn_stats.overall_matches_played = overall_matches_played
                        overall_wtn_stats.overall_lost_to_nil = overall_lost_to_nil
                        overall_wtn_stats.overall_lost_to_nil_percent = overall_lost_to_nil_percent
                        overall_wtn_stats.save()
