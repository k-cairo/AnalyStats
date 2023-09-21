import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5Over35GoalsIframe, E5Over35GoalsStats, E5Team
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetOver35Goals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetOver35Goals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    OVER_35_GOALS_IFRAMES: ClassVar[QuerySet[E5Over35GoalsIframe]] = E5Over35GoalsIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.OVER_35_GOALS_IFRAMES:
                iframe: E5Over35GoalsIframe  # Type hinting for Intellij

                ########################################### Over 3.5 Goals #############################################
                # Get Url
                self.get(url=iframe.over_35_goals_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 3.5 Goals Stats
                for table_tr in table_trs:
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_over_35_goals: int = 0
                    home_over_35_goals_percent: str = ""
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_over_35_goals: int = 0
                    away_over_35_goals_percent: str = ""
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_over_35_goals: int = 0
                    overall_over_35_goals_percent: str = ""
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
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
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
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {home_team.name} created")
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {home_team.name} updated")

                    # Create Over 3.5 Goals Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {away_team.name} created")
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {away_team.name} updated")

                    # Create Over 3.5 Goals Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {overall_team.name} created")
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals Stats : {overall_team.name} updated")

                ######################################### Over 3.5 Goals 1H ############################################
                # Get Url
                self.get(url=iframe.over_35_goals_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 3.5 Goals 1H Stats
                for table_tr in table_trs:
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_over_35_goals: int = 0
                    home_over_35_goals_percent: str = ""
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_over_35_goals: int = 0
                    away_over_35_goals_percent: str = ""
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_over_35_goals: int = 0
                    overall_over_35_goals_percent: str = ""
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
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
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
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {home_team.name} created")
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_1h = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_1h_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {home_team.name} updated")

                    # Create Over 3.5 Goals 1H Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_1h = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_1h_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {away_team.name} created")
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_1h = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_1h_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {away_team.name} updated")

                    # Create Over 3.5 Goals 1H Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_1h = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_1h_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {overall_team.name} created")
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_1h = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_1h_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 1H Stats : {overall_team.name} updated")

                ######################################### Over 3.5 Goals 2H ############################################
                # Get Url
                self.get(url=iframe.over_35_goals_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 3.5 Goals 2H Stats
                for table_tr in table_trs:
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_over_35_goals: int = 0
                    home_over_35_goals_percent: str = ""
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_over_35_goals: int = 0
                    away_over_35_goals_percent: str = ""
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_over_35_goals: int = 0
                    overall_over_35_goals_percent: str = ""
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
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
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
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {home_team.name} created")
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_2h = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_2h_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {home_team.name} updated")

                    # Create Over 3.5 Goals 2H Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_2h = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_2h_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {away_team.name} created")
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_2h = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_2h_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {away_team.name} updated")

                    # Create Over 3.5 Goals 2H Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_2h = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_2h_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {overall_team.name} created")
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_2h = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_2h_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals 2H Stats : {overall_team.name} updated")

                ######################################### Over 3.5 Goals BH ############################################
                # Get Url
                self.get(url=iframe.over_35_goals_bh_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 3.5 Goals BH Stats
                for table_tr in table_trs:
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_over_35_goals: int = 0
                    home_over_35_goals_percent: str = ""
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_over_35_goals: int = 0
                    away_over_35_goals_percent: str = ""
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_over_35_goals: int = 0
                    overall_over_35_goals_percent: str = ""
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
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                        overall_team: E5Team = E5Team.objects.get(name=overall_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
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
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {home_team.name} created")
                    else:
                        target_home_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_35_goals_stats.home_matches_played = home_matches_played
                        target_home_over_35_goals_stats.home_over_35_goals_bh = home_over_35_goals
                        target_home_over_35_goals_stats.home_over_35_goals_bh_percent = home_over_35_goals_percent
                        target_home_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {home_team.name} updated")

                    # Create Over 3.5 Goals BH Away Stats
                    away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    away_over_35_goals_stats.team = away_team
                    away_over_35_goals_stats.away_matches_played = away_matches_played
                    away_over_35_goals_stats.away_over_35_goals_bh = away_over_35_goals
                    away_over_35_goals_stats.away_over_35_goals_bh_percent = away_over_35_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_35_goals_stats.exists():
                        away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {away_team.name} created")
                    else:
                        target_away_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_35_goals_stats.away_matches_played = away_matches_played
                        target_away_over_35_goals_stats.away_over_35_goals_bh = away_over_35_goals
                        target_away_over_35_goals_stats.away_over_35_goals_bh_percent = away_over_35_goals_percent
                        target_away_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {away_team.name} updated")

                    # Create Over 3.5 Goals BH Overall Stats
                    overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats()
                    overall_over_35_goals_stats.team = overall_team
                    overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_35_goals_stats.overall_over_35_goals_bh = overall_over_35_goals
                    overall_over_35_goals_stats.overall_over_35_goals_bh_percent = overall_over_35_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_35_goals_stats.exists():
                        overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {overall_team.name} created")
                    else:
                        target_overall_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_35_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_35_goals_stats.overall_over_35_goals_bh = overall_over_35_goals
                        target_overall_over_35_goals_stats.overall_over_35_goals_bh_percent = overall_over_35_goals_percent
                        target_overall_over_35_goals_stats.save()
                        self.log_info(message=f"Parse Over 3.5 Goals BH Stats : {overall_team.name} updated")
