import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5Average1stGoalTimeIframe, E5Team, E5Average1stGoalTimeStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetAverageFirstGoalTime(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetAverage1stGoalTime"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    A1GT_IFRAMES: ClassVar[QuerySet[E5Average1stGoalTimeIframe]] = E5Average1stGoalTimeIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.A1GT_IFRAMES:
                iframe: E5Average1stGoalTimeIframe  # Type hinting for Intellij

                ####################################### Average First Goal Time ########################################
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
                        home_first_goal_time_scored_average: float = float(table_tr.find_all('td')[2].text)
                        home_first_goal_time_conceded_average: float = float(table_tr.find_all('td')[3].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_first_goal_time_scored_average: float = float(table_tr.find_all('td')[6].text)
                        away_first_goal_time_conceded_average: float = float(table_tr.find_all('td')[7].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_first_goal_time_scored_average: float = float(table_tr.find_all('td')[10].text)
                        overall_first_goal_time_conceded_average: float = float(table_tr.find_all('td')[11].text)
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
                    home_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats()
                    home_a1gt_stats.team = home_team
                    home_a1gt_stats.home_first_goal_time_scored_average = home_first_goal_time_scored_average
                    home_a1gt_stats.home_first_goal_time_conceded_average = home_first_goal_time_conceded_average

                    # Check if home stats already exists before saving or updating
                    if not home_a1gt_stats.exists():
                        home_a1gt_stats.save()
                        self.log_info(f"Team {home_team.name} Average First Goal Time Stats created in database")
                    else:
                        home_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats.objects.get(
                            team=home_team)
                        home_a1gt_stats.home_first_goal_time_scored_average = home_first_goal_time_scored_average
                        home_a1gt_stats.home_first_goal_time_conceded_average = home_first_goal_time_conceded_average
                        home_a1gt_stats.save()
                        self.log_info(f"Team {home_team.name} Average First Goal Time Stats updated in database")

                    # Create Away Stats
                    away_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats()
                    away_a1gt_stats.team = away_team
                    away_a1gt_stats.away_first_goal_time_scored_average = away_first_goal_time_scored_average
                    away_a1gt_stats.away_first_goal_time_conceded_average = away_first_goal_time_conceded_average

                    # Check if away stats already exists before saving or updating
                    if not away_a1gt_stats.exists():
                        away_a1gt_stats.save()
                        self.log_info(f"Team {away_team.name} Average First Goal Time Stats created in database")
                    else:
                        away_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats.objects.get(
                            team=away_team)
                        away_a1gt_stats.away_first_goal_time_scored_average = away_first_goal_time_scored_average
                        away_a1gt_stats.away_first_goal_time_conceded_average = away_first_goal_time_conceded_average
                        away_a1gt_stats.save()
                        self.log_info(f"Team {away_team.name} Average First Goal Time Stats updated in database")

                    # Create Overall Stats
                    overall_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats()
                    overall_a1gt_stats.team = overall_team
                    overall_a1gt_stats.overall_first_goal_time_scored_average = overall_first_goal_time_scored_average
                    overall_a1gt_stats.overall_first_goal_time_conceded_average = overall_first_goal_time_conceded_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_a1gt_stats.exists():
                        overall_a1gt_stats.save()
                        self.log_info(f"Team {overall_team.name} Average First Goal Time Stats created in database")
                    else:
                        overall_a1gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats.objects.get(
                            team=overall_team)
                        overall_a1gt_stats.overall_first_goal_time_scored_average = overall_first_goal_time_scored_average
                        overall_a1gt_stats.overall_first_goal_time_conceded_average = overall_first_goal_time_conceded_average
                        overall_a1gt_stats.save()
                        self.log_info(f"Team {overall_team.name} Average First Goal Time Stats updated in database")
