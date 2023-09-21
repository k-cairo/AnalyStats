import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E51st2ndHalfGoalsIframe, E5Team, E51st2ndHalfGoalsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5Get1st2ndHalfGoals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5Get1st2ndHalfGoals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    WTN_IFRAMES: ClassVar[QuerySet[E51st2ndHalfGoalsIframe]] = E51st2ndHalfGoalsIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.WTN_IFRAMES:
                iframe: E51st2ndHalfGoalsIframe  # Type hinting for Intellij

                ########################################## 1st 2nd Half Goals ##########################################
                # Get Url
                self.get(url=iframe.home_1st_2nd_half_goals_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')
                home_scored_team_name: str = ""
                home_matches_played: int = 0
                home_goals_scored: int = 0
                home_goals_scored_1h: int = 0
                home_goals_scored_1h_percent: int = 0
                home_goals_scored_1h_average: float = 0.0
                home_goals_scored_2h: int = 0
                home_goals_scored_2h_percent: int = 0
                home_goals_scored_2h_average: float = 0.0
                home_conceded_team_name: str = ""
                home_matches_conceded_played: int = 0
                home_goals_conceded: int = 0
                home_goals_conceded_1h: int = 0
                home_goals_conceded_1h_percent: int = 0
                home_goals_conceded_1h_average: float = 0.0
                home_goals_conceded_2h: int = 0
                home_goals_conceded_2h_percent: int = 0
                home_goals_conceded_2h_average: float = 0.0
                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_scored_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_goals_scored = int(table_tr.find_all('td')[3].text)
                        home_goals_scored_1h = int(table_tr.find_all('td')[4].text)
                        home_goals_scored_1h_percent = int(table_tr.find_all('td')[5].text.strip('%'))
                        home_goals_scored_1h_average = float(table_tr.find_all('td')[6].text)
                        home_goals_scored_2h = int(table_tr.find_all('td')[7].text)
                        home_goals_scored_2h_percent = int(table_tr.find_all('td')[8].text.strip('%'))
                        home_goals_scored_2h_average = float(table_tr.find_all('td')[9].text)
                        home_conceded_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        home_matches_conceded_played: int = int(table_tr.find_all('td')[12].text)
                        home_goals_conceded = int(table_tr.find_all('td')[13].text)
                        home_goals_conceded_1h = int(table_tr.find_all('td')[14].text)
                        home_goals_conceded_1h_percent = int(table_tr.find_all('td')[15].text.strip('%'))
                        home_goals_conceded_1h_average = float(table_tr.find_all('td')[16].text)
                        home_goals_conceded_2h = int(table_tr.find_all('td')[17].text)
                        home_goals_conceded_2h_percent = int(table_tr.find_all('td')[18].text.strip('%'))
                        home_goals_conceded_2h_average = float(table_tr.find_all('td')[19].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        scored_team: E5Team = E5Team.objects.get(name=home_scored_team_name, season=iframe.season)
                        conceded_team: E5Team = E5Team.objects.get(name=home_conceded_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Home Scored Stats
                    home_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    home_1st_2nd_half_goals_stats.team = scored_team
                    home_1st_2nd_half_goals_stats.home_matches_played = home_matches_played
                    home_1st_2nd_half_goals_stats.home_goals_scored = home_goals_scored
                    home_1st_2nd_half_goals_stats.home_goals_scored_1h = home_goals_scored_1h
                    home_1st_2nd_half_goals_stats.home_goals_scored_1h_percent = home_goals_scored_1h_percent
                    home_1st_2nd_half_goals_stats.home_goals_scored_1h_average = home_goals_scored_1h_average
                    home_1st_2nd_half_goals_stats.home_goals_scored_2h = home_goals_scored_2h
                    home_1st_2nd_half_goals_stats.home_goals_scored_2h_percent = home_goals_scored_2h_percent
                    home_1st_2nd_half_goals_stats.home_goals_scored_2h_average = home_goals_scored_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_1st_2nd_half_goals_stats.exists():
                        home_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} created")
                    else:
                        home_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=scored_team)
                        home_1st_2nd_half_goals_stats.home_matches_played = home_matches_played
                        home_1st_2nd_half_goals_stats.home_goals_scored = home_goals_scored
                        home_1st_2nd_half_goals_stats.home_goals_scored_1h = home_goals_scored_1h
                        home_1st_2nd_half_goals_stats.home_goals_scored_1h_percent = home_goals_scored_1h_percent
                        home_1st_2nd_half_goals_stats.home_goals_scored_1h_average = home_goals_scored_1h_average
                        home_1st_2nd_half_goals_stats.home_goals_scored_2h = home_goals_scored_2h
                        home_1st_2nd_half_goals_stats.home_goals_scored_2h_percent = home_goals_scored_2h_percent
                        home_1st_2nd_half_goals_stats.home_goals_scored_2h_average = home_goals_scored_2h_average
                        home_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} updated")

                    # Create Home Conceded Stats
                    home_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    home_1st_2nd_half_goals_stats.team = conceded_team
                    home_1st_2nd_half_goals_stats.home_matches_played = home_matches_played
                    home_1st_2nd_half_goals_stats.home_goals_conceded = home_goals_conceded
                    home_1st_2nd_half_goals_stats.home_goals_conceded_1h = home_goals_conceded_1h
                    home_1st_2nd_half_goals_stats.home_goals_conceded_1h_percent = home_goals_conceded_1h_percent
                    home_1st_2nd_half_goals_stats.home_goals_conceded_1h_average = home_goals_conceded_1h_average
                    home_1st_2nd_half_goals_stats.home_goals_conceded_2h = home_goals_conceded_2h
                    home_1st_2nd_half_goals_stats.home_goals_conceded_2h_percent = home_goals_conceded_2h_percent
                    home_1st_2nd_half_goals_stats.home_goals_conceded_2h_average = home_goals_conceded_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_1st_2nd_half_goals_stats.exists():
                        home_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} created")
                    else:
                        home_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=conceded_team)
                        home_1st_2nd_half_goals_stats.home_matches_played = home_matches_played
                        home_1st_2nd_half_goals_stats.home_goals_conceded = home_goals_conceded
                        home_1st_2nd_half_goals_stats.home_goals_conceded_1h = home_goals_conceded_1h
                        home_1st_2nd_half_goals_stats.home_goals_conceded_1h_percent = home_goals_conceded_1h_percent
                        home_1st_2nd_half_goals_stats.home_goals_conceded_1h_average = home_goals_conceded_1h_average
                        home_1st_2nd_half_goals_stats.home_goals_conceded_2h = home_goals_conceded_2h
                        home_1st_2nd_half_goals_stats.home_goals_conceded_2h_percent = home_goals_conceded_2h_percent
                        home_1st_2nd_half_goals_stats.home_goals_conceded_2h_average = home_goals_conceded_2h_average
                        home_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} updated")

                ########################################## 1st 2nd Half Goals ##########################################
                # Get Url
                self.get(url=iframe.away_1st_2nd_half_goals_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    away_scored_team_name: str = ""
                    away_matches_played: int = 0
                    away_goals_scored: int = 0
                    away_goals_scored_1h: int = 0
                    away_goals_scored_1h_percent: int = 0
                    away_goals_scored_1h_average: float = 0.0
                    away_goals_scored_2h: int = 0
                    away_goals_scored_2h_percent: int = 0
                    away_goals_scored_2h_average: float = 0.0
                    away_conceded_team_name: str = ""
                    away_matches_conceded_played: int = 0
                    away_goals_conceded: int = 0
                    away_goals_conceded_1h: int = 0
                    away_goals_conceded_1h_percent: int = 0
                    away_goals_conceded_1h_average: float = 0.0
                    away_goals_conceded_2h: int = 0
                    away_goals_conceded_2h_percent: int = 0
                    away_goals_conceded_2h_average: float = 0.0
                    try:
                        away_scored_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        away_matches_played: int = int(table_tr.find_all('td')[2].text)
                        away_goals_scored = int(table_tr.find_all('td')[3].text)
                        away_goals_scored_1h = int(table_tr.find_all('td')[4].text)
                        away_goals_scored_1h_percent = int(table_tr.find_all('td')[5].text.strip('%'))
                        away_goals_scored_1h_average = float(table_tr.find_all('td')[6].text)
                        away_goals_scored_2h = int(table_tr.find_all('td')[7].text)
                        away_goals_scored_2h_percent = int(table_tr.find_all('td')[8].text.strip('%'))
                        away_goals_scored_2h_average = float(table_tr.find_all('td')[9].text)
                        away_conceded_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_conceded_played: int = int(table_tr.find_all('td')[12].text)
                        away_goals_conceded = int(table_tr.find_all('td')[13].text)
                        away_goals_conceded_1h = int(table_tr.find_all('td')[14].text)
                        away_goals_conceded_1h_percent = int(table_tr.find_all('td')[15].text.strip('%'))
                        away_goals_conceded_1h_average = float(table_tr.find_all('td')[16].text)
                        away_goals_conceded_2h = int(table_tr.find_all('td')[17].text)
                        away_goals_conceded_2h_percent = int(table_tr.find_all('td')[18].text.strip('%'))
                        away_goals_conceded_2h_average = float(table_tr.find_all('td')[19].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        scored_team: E5Team = E5Team.objects.get(name=away_scored_team_name, season=iframe.season)
                        conceded_team: E5Team = E5Team.objects.get(name=away_conceded_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Away Scored Stats
                    away_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    away_1st_2nd_half_goals_stats.team = scored_team
                    away_1st_2nd_half_goals_stats.away_matches_played = away_matches_played
                    away_1st_2nd_half_goals_stats.away_goals_scored = away_goals_scored
                    away_1st_2nd_half_goals_stats.away_goals_scored_1h = away_goals_scored_1h
                    away_1st_2nd_half_goals_stats.away_goals_scored_1h_percent = away_goals_scored_1h_percent
                    away_1st_2nd_half_goals_stats.away_goals_scored_1h_average = away_goals_scored_1h_average
                    away_1st_2nd_half_goals_stats.away_goals_scored_2h = away_goals_scored_2h
                    away_1st_2nd_half_goals_stats.away_goals_scored_2h_percent = away_goals_scored_2h_percent
                    away_1st_2nd_half_goals_stats.away_goals_scored_2h_average = away_goals_scored_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_1st_2nd_half_goals_stats.exists():
                        away_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} created")
                    else:
                        away_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=scored_team)
                        away_1st_2nd_half_goals_stats.away_matches_played = away_matches_played
                        away_1st_2nd_half_goals_stats.away_goals_scored = away_goals_scored
                        away_1st_2nd_half_goals_stats.away_goals_scored_1h = away_goals_scored_1h
                        away_1st_2nd_half_goals_stats.away_goals_scored_1h_percent = away_goals_scored_1h_percent
                        away_1st_2nd_half_goals_stats.away_goals_scored_1h_average = away_goals_scored_1h_average
                        away_1st_2nd_half_goals_stats.away_goals_scored_2h = away_goals_scored_2h
                        away_1st_2nd_half_goals_stats.away_goals_scored_2h_percent = away_goals_scored_2h_percent
                        away_1st_2nd_half_goals_stats.away_goals_scored_2h_average = away_goals_scored_2h_average
                        away_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} updated")

                    # Create Away Conceded Stats
                    away_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    away_1st_2nd_half_goals_stats.team = conceded_team
                    away_1st_2nd_half_goals_stats.away_matches_played = away_matches_played
                    away_1st_2nd_half_goals_stats.away_goals_conceded = away_goals_conceded
                    away_1st_2nd_half_goals_stats.away_goals_conceded_1h = away_goals_conceded_1h
                    away_1st_2nd_half_goals_stats.away_goals_conceded_1h_percent = away_goals_conceded_1h_percent
                    away_1st_2nd_half_goals_stats.away_goals_conceded_1h_average = away_goals_conceded_1h_average
                    away_1st_2nd_half_goals_stats.away_goals_conceded_2h = away_goals_conceded_2h
                    away_1st_2nd_half_goals_stats.away_goals_conceded_2h_percent = away_goals_conceded_2h_percent
                    away_1st_2nd_half_goals_stats.away_goals_conceded_2h_average = away_goals_conceded_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_1st_2nd_half_goals_stats.exists():
                        away_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} created")
                    else:
                        away_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=conceded_team)
                        away_1st_2nd_half_goals_stats.away_matches_played = away_matches_played
                        away_1st_2nd_half_goals_stats.away_goals_conceded = away_goals_conceded
                        away_1st_2nd_half_goals_stats.away_goals_conceded_1h = away_goals_conceded_1h
                        away_1st_2nd_half_goals_stats.away_goals_conceded_1h_percent = away_goals_conceded_1h_percent
                        away_1st_2nd_half_goals_stats.away_goals_conceded_1h_average = away_goals_conceded_1h_average
                        away_1st_2nd_half_goals_stats.away_goals_conceded_2h = away_goals_conceded_2h
                        away_1st_2nd_half_goals_stats.away_goals_conceded_2h_percent = away_goals_conceded_2h_percent
                        away_1st_2nd_half_goals_stats.away_goals_conceded_2h_average = away_goals_conceded_2h_average
                        away_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} updated")

                ########################################## 1st 2nd Half Goals ##########################################
                # Get Url
                self.get(url=iframe.overall_1st_2nd_half_goals_url,
                         error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    overall_scored_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_goals_scored: int = 0
                    overall_goals_scored_1h: int = 0
                    overall_goals_scored_1h_percent: int = 0
                    overall_goals_scored_1h_average: float = 0.0
                    overall_goals_scored_2h: int = 0
                    overall_goals_scored_2h_percent: int = 0
                    overall_goals_scored_2h_average: float = 0.0
                    overall_conceded_team_name: str = ""
                    overall_matches_conceded_played: int = 0
                    overall_goals_conceded: int = 0
                    overall_goals_conceded_1h: int = 0
                    overall_goals_conceded_1h_percent: int = 0
                    overall_goals_conceded_1h_average: float = 0.0
                    overall_goals_conceded_2h: int = 0
                    overall_goals_conceded_2h_percent: int = 0
                    overall_goals_conceded_2h_average: float = 0.0
                    try:
                        overall_scored_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        overall_matches_played: int = int(table_tr.find_all('td')[2].text)
                        overall_goals_scored = int(table_tr.find_all('td')[3].text)
                        overall_goals_scored_1h = int(table_tr.find_all('td')[4].text)
                        overall_goals_scored_1h_percent = int(table_tr.find_all('td')[5].text.strip('%'))
                        overall_goals_scored_1h_average = float(table_tr.find_all('td')[6].text)
                        overall_goals_scored_2h = int(table_tr.find_all('td')[7].text)
                        overall_goals_scored_2h_percent = int(table_tr.find_all('td')[8].text.strip('%'))
                        overall_goals_scored_2h_average = float(table_tr.find_all('td')[9].text)
                        overall_conceded_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        overall_matches_conceded_played: int = int(table_tr.find_all('td')[12].text)
                        overall_goals_conceded = int(table_tr.find_all('td')[13].text)
                        overall_goals_conceded_1h = int(table_tr.find_all('td')[14].text)
                        overall_goals_conceded_1h_percent = int(table_tr.find_all('td')[15].text.strip('%'))
                        overall_goals_conceded_1h_average = float(table_tr.find_all('td')[16].text)
                        overall_goals_conceded_2h = int(table_tr.find_all('td')[17].text)
                        overall_goals_conceded_2h_percent = int(table_tr.find_all('td')[18].text.strip('%'))
                        overall_goals_conceded_2h_average = float(table_tr.find_all('td')[19].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        scored_team: E5Team = E5Team.objects.get(name=overall_scored_team_name, season=iframe.season)
                        conceded_team: E5Team = E5Team.objects.get(name=overall_conceded_team_name,
                                                                   season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Overall Scored Stats
                    overall_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    overall_1st_2nd_half_goals_stats.team = scored_team
                    overall_1st_2nd_half_goals_stats.overall_matches_played = overall_matches_played
                    overall_1st_2nd_half_goals_stats.overall_goals_scored = overall_goals_scored
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_1h = overall_goals_scored_1h
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_1h_percent = overall_goals_scored_1h_percent
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_1h_average = overall_goals_scored_1h_average
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_2h = overall_goals_scored_2h
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_2h_percent = overall_goals_scored_2h_percent
                    overall_1st_2nd_half_goals_stats.overall_goals_scored_2h_average = overall_goals_scored_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_1st_2nd_half_goals_stats.exists():
                        overall_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} created")
                    else:
                        overall_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=scored_team)
                        overall_1st_2nd_half_goals_stats.overall_matches_played = overall_matches_played
                        overall_1st_2nd_half_goals_stats.overall_goals_scored = overall_goals_scored
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_1h = overall_goals_scored_1h
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_1h_percent = overall_goals_scored_1h_percent
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_1h_average = overall_goals_scored_1h_average
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_2h = overall_goals_scored_2h
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_2h_percent = overall_goals_scored_2h_percent
                        overall_1st_2nd_half_goals_stats.overall_goals_scored_2h_average = overall_goals_scored_2h_average
                        overall_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {scored_team.name} updated")

                    # Create Overall Conceded Stats
                    overall_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats()
                    overall_1st_2nd_half_goals_stats.team = conceded_team
                    overall_1st_2nd_half_goals_stats.overall_matches_played = overall_matches_played
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded = overall_goals_conceded
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h = overall_goals_conceded_1h
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h_percent = overall_goals_conceded_1h_percent
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h_average = overall_goals_conceded_1h_average
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h = overall_goals_conceded_2h
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h_percent = overall_goals_conceded_2h_percent
                    overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h_average = overall_goals_conceded_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_1st_2nd_half_goals_stats.exists():
                        overall_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} created")
                    else:
                        overall_1st_2nd_half_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(
                            team=conceded_team)
                        overall_1st_2nd_half_goals_stats.overall_matches_played = overall_matches_played
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded = overall_goals_conceded
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h = overall_goals_conceded_1h
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h_percent = overall_goals_conceded_1h_percent
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_1h_average = overall_goals_conceded_1h_average
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h = overall_goals_conceded_2h
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h_percent = overall_goals_conceded_2h_percent
                        overall_1st_2nd_half_goals_stats.overall_goals_conceded_2h_average = overall_goals_conceded_2h_average
                        overall_1st_2nd_half_goals_stats.save()
                        self.log_info(message=f"Parse 1st 2nd Half Goals Stats : {conceded_team.name} updated")
