import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5CleanSheetStats, E5Team, E5CleanSheetIframe
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetCleanSheets(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCleanSheets"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    CS_IFRAMES: ClassVar[QuerySet[E5CleanSheetIframe]] = E5CleanSheetIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.CS_IFRAMES:
                iframe: E5CleanSheetIframe  # Type hinting for Intellij

                ############################################ Clean Sheets ##############################################
                # Get Url
                self.get(url=iframe.clean_sheet_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Clean Sheets Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_clean_sheet: int = 0
                    home_clean_sheet_percent: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_clean_sheet: int = 0
                    away_clean_sheet_percent: int = 0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_clean_sheet: int = 0
                    overall_clean_sheet_percent: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_clean_sheet: int = int(table_tr.find_all('td')[3].text)
                        home_clean_sheet_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_clean_sheet: int = int(table_tr.find_all('td')[8].text)
                        away_clean_sheet_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_clean_sheet: int = int(table_tr.find_all('td')[13].text)
                        overall_clean_sheet_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create Clean Sheet Home Stats
                    home_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    home_cs_stats.team = home_team
                    home_cs_stats.home_matches_played = home_matches_played
                    home_cs_stats.home_clean_sheet = home_clean_sheet
                    home_cs_stats.home_clean_sheet_percent = home_clean_sheet_percent

                    # Check if home stats already exists before saving or updating
                    if not home_cs_stats.exists():
                        home_cs_stats.save()
                    else:
                        home_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=home_team)
                        home_cs_stats.home_matches_played = home_matches_played
                        home_cs_stats.home_clean_sheet = home_clean_sheet
                        home_cs_stats.home_clean_sheet_percent = home_clean_sheet_percent
                        home_cs_stats.save()

                    # Create Clean Sheet Away Stats
                    away_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    away_cs_stats.team = away_team
                    away_cs_stats.away_matches_played = away_matches_played
                    away_cs_stats.away_clean_sheet = away_clean_sheet
                    away_cs_stats.away_clean_sheet_percent = away_clean_sheet_percent

                    # Check if away stats already exists before saving or updating
                    if not away_cs_stats.exists():
                        away_cs_stats.save()
                    else:
                        away_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=away_team)
                        away_cs_stats.away_matches_played = away_matches_played
                        away_cs_stats.away_clean_sheet = away_clean_sheet
                        away_cs_stats.away_clean_sheet_percent = away_clean_sheet_percent
                        away_cs_stats.save()

                    # Create Clean Sheet Overall Stats
                    overall_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    overall_cs_stats.team = overall_team
                    overall_cs_stats.overall_matches_played = overall_matches_played
                    overall_cs_stats.overall_clean_sheet = overall_clean_sheet
                    overall_cs_stats.overall_clean_sheet_percent = overall_clean_sheet_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_cs_stats.exists():
                        overall_cs_stats.save()
                    else:
                        overall_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=overall_team)
                        overall_cs_stats.overall_matches_played = overall_matches_played
                        overall_cs_stats.overall_clean_sheet = overall_clean_sheet
                        overall_cs_stats.overall_clean_sheet_percent = overall_clean_sheet_percent
                        overall_cs_stats.save()

                ######################################### Failed To Score ###########################################
                # Get Url
                self.get(url=iframe.failed_to_score_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                    home_failed_to_score: int = 0
                    home_failed_to_score_percent: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_failed_to_score: int = 0
                    away_failed_to_score_percent: int = 0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_failed_to_score: int = 0
                    overall_failed_to_score_percent: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_failed_to_score: int = int(table_tr.find_all('td')[3].text)
                        home_failed_to_score_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_failed_to_score: int = int(table_tr.find_all('td')[8].text)
                        away_failed_to_score_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_failed_to_score: int = int(table_tr.find_all('td')[13].text)
                        overall_failed_to_score_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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
                    home_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    home_cs_stats.team = home_team
                    home_cs_stats.home_matches_played = home_matches_played
                    home_cs_stats.home_failed_to_score = home_failed_to_score
                    home_cs_stats.home_failed_to_score_percent = home_failed_to_score_percent

                    # Check if home stats already exists before saving or updating
                    if not home_cs_stats.exists():
                        home_cs_stats.save()
                    else:
                        home_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=home_team)
                        home_cs_stats.home_matches_played = home_matches_played
                        home_cs_stats.home_failed_to_score = home_failed_to_score
                        home_cs_stats.home_failed_to_score_percent = home_failed_to_score_percent
                        home_cs_stats.save()

                    # Create Clean Sheet Away Stats
                    away_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    away_cs_stats.team = away_team
                    away_cs_stats.away_matches_played = away_matches_played
                    away_cs_stats.away_failed_to_score = away_failed_to_score
                    away_cs_stats.away_failed_to_score_percent = away_failed_to_score_percent

                    # Check if away stats already exists before saving or updating
                    if not away_cs_stats.exists():
                        away_cs_stats.save()
                    else:
                        away_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=away_team)
                        away_cs_stats.away_matches_played = away_matches_played
                        away_cs_stats.away_failed_to_score = away_failed_to_score
                        away_cs_stats.away_failed_to_score_percent = away_failed_to_score_percent
                        away_cs_stats.save()

                    # Create Clean Sheet Overall Stats
                    overall_cs_stats: E5CleanSheetStats = E5CleanSheetStats()
                    overall_cs_stats.team = overall_team
                    overall_cs_stats.overall_matches_played = overall_matches_played
                    overall_cs_stats.overall_failed_to_score = overall_failed_to_score
                    overall_cs_stats.overall_failed_to_score_percent = overall_failed_to_score_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_cs_stats.exists():
                        overall_cs_stats.save()
                    else:
                        overall_cs_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=overall_team)
                        overall_cs_stats.overall_matches_played = overall_matches_played
                        overall_cs_stats.overall_failed_to_score = overall_failed_to_score
                        overall_cs_stats.overall_failed_to_score_percent = overall_failed_to_score_percent
                        overall_cs_stats.save()
