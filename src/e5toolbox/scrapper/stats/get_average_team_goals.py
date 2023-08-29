import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5AverageTeamGoalsIframe, E5Team, E5AverageTeamGoalsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetAverageTeamGoals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetAverageTeamGoals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    ATG_IFRAMES: ClassVar[QuerySet[E5AverageTeamGoalsIframe]] = E5AverageTeamGoalsIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.ATG_IFRAMES:
                iframe: E5AverageTeamGoalsIframe  # Type hinting for Intellij

                ######################################### Average team Goals ###########################################
                # Get Url
                self.get(url=iframe.url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Won Both Halves Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_goals_scored_average: float = float(table_tr.find_all('td')[2].text)
                        home_goals_conceded_average: float = float(table_tr.find_all('td')[3].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_goals_scored_average: float = float(table_tr.find_all('td')[6].text)
                        away_goals_conceded_average: float = float(table_tr.find_all('td')[7].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_goals_scored_average: float = float(table_tr.find_all('td')[10].text)
                        overall_goals_conceded_average: float = float(table_tr.find_all('td')[11].text)
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
                    home_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats()
                    home_atg_stats.team = home_team
                    home_atg_stats.home_goals_scored_average = home_goals_scored_average
                    home_atg_stats.home_goals_conceded_average = home_goals_conceded_average

                    # Check if home stats already exists before saving or updating
                    if not home_atg_stats.exists():
                        home_atg_stats.save()
                        self.log_info(f"Team {home_team.name} Average Team Goals Stats created in database")
                    else:
                        home_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats.objects.get(team=home_team)
                        home_atg_stats.home_goals_scored_average = home_goals_scored_average
                        home_atg_stats.home_goals_conceded_average = home_goals_conceded_average
                        home_atg_stats.save()
                        self.log_info(f"Team {home_team.name} Average Team Goals Stats updated in database")

                    # Create Away Stats
                    away_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats()
                    away_atg_stats.team = away_team
                    away_atg_stats.away_goals_scored_average = away_goals_scored_average
                    away_atg_stats.away_goals_conceded_average = away_goals_conceded_average

                    # Check if away stats already exists before saving or updating
                    if not away_atg_stats.exists():
                        away_atg_stats.save()
                        self.log_info(f"Team {away_team.name} Average Team Goals Stats created in database")
                    else:
                        away_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats.objects.get(team=away_team)
                        away_atg_stats.away_goals_scored_average = away_goals_scored_average
                        away_atg_stats.away_goals_conceded_average = away_goals_conceded_average
                        away_atg_stats.save()
                        self.log_info(f"Team {away_team.name} Average Team Goals Stats updated in database")

                    # Create Overall Stats
                    overall_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats()
                    overall_atg_stats.team = overall_team
                    overall_atg_stats.overall_goals_scored_average = overall_goals_scored_average
                    overall_atg_stats.overall_goals_conceded_average = overall_goals_conceded_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_atg_stats.exists():
                        overall_atg_stats.save()
                        self.log_info(f"Team {overall_team.name} Average Team Goals Stats created in database")
                    else:
                        overall_atg_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats.objects.get(
                            team=overall_team)
                        overall_atg_stats.overall_goals_scored_average = overall_goals_scored_average
                        overall_atg_stats.overall_goals_conceded_average = overall_goals_conceded_average
                        overall_atg_stats.save()
                        self.log_info(f"Team {overall_team.name} Average Team Goals Stats updated in database")

