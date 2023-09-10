import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5LateGoalsIframe, E5Team, E5LateGoalsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetLateGoals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetLateGoals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    EG_IFRAMES: ClassVar[QuerySet[E5LateGoalsIframe]] = E5LateGoalsIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.EG_IFRAMES:
                iframe: E5LateGoalsIframe  # Type hinting for Intellij

                ############################################# Late Goals ##############################################
                # Get Url
                self.get(url=iframe.url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_scored_late: int = int(table_tr.find_all('td')[3].text)
                        home_conceded_late: int = int(table_tr.find_all('td')[4].text)
                        home_scored_or_conceded_late: int = int(table_tr.find_all('td')[5].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[8].text)
                        away_scored_late: int = int(table_tr.find_all('td')[9].text)
                        away_conceded_late: int = int(table_tr.find_all('td')[10].text)
                        away_scored_or_conceded_late: int = int(table_tr.find_all('td')[11].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[14].text)
                        overall_scored_late: int = int(table_tr.find_all('td')[15].text)
                        overall_conceded_late: int = int(table_tr.find_all('td')[16].text)
                        overall_scored_or_conceded_late: int = int(table_tr.find_all('td')[17].text)
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
                    home_lg_stats: E5LateGoalsStats = E5LateGoalsStats()
                    home_lg_stats.team = home_team
                    home_lg_stats.home_matches_played = home_matches_played
                    home_lg_stats.home_scored_late = home_scored_late
                    home_lg_stats.home_conceded_late = home_conceded_late
                    home_lg_stats.home_scored_or_conceded_late = home_scored_or_conceded_late

                    # Check if home stats already exists before saving or updating
                    if not home_lg_stats.exists():
                        home_lg_stats.save()
                    else:
                        home_lg_stats: E5LateGoalsStats = E5LateGoalsStats.objects.get(team=home_team)
                        home_lg_stats.home_matches_played = home_matches_played
                        home_lg_stats.home_scored_late = home_scored_late
                        home_lg_stats.home_conceded_late = home_conceded_late
                        home_lg_stats.home_scored_or_conceded_late = home_scored_or_conceded_late
                        home_lg_stats.save()

                    # Create Away Stats
                    away_lg_stats: E5LateGoalsStats = E5LateGoalsStats()
                    away_lg_stats.team = away_team
                    away_lg_stats.away_matches_played = away_matches_played
                    away_lg_stats.away_scored_late = away_scored_late
                    away_lg_stats.away_conceded_late = away_conceded_late
                    away_lg_stats.away_scored_or_conceded_late = away_scored_or_conceded_late

                    # Check if away stats already exists before saving or updating
                    if not away_lg_stats.exists():
                        away_lg_stats.save()
                    else:
                        away_lg_stats: E5LateGoalsStats = E5LateGoalsStats.objects.get(team=away_team)
                        away_lg_stats.away_matches_played = away_matches_played
                        away_lg_stats.away_scored_late = away_scored_late
                        away_lg_stats.away_conceded_late = away_conceded_late
                        away_lg_stats.away_scored_or_conceded_late = away_scored_or_conceded_late
                        away_lg_stats.save()

                    # Create Overall Stats
                    overall_lg_stats: E5LateGoalsStats = E5LateGoalsStats()
                    overall_lg_stats.team = overall_team
                    overall_lg_stats.overall_matches_played = overall_matches_played
                    overall_lg_stats.overall_scored_late = overall_scored_late
                    overall_lg_stats.overall_conceded_late = overall_conceded_late
                    overall_lg_stats.overall_scored_or_conceded_late = overall_scored_or_conceded_late

                    # Check if overall stats already exists before saving or updating
                    if not overall_lg_stats.exists():
                        overall_lg_stats.save()
                    else:
                        overall_lg_stats: E5LateGoalsStats = E5LateGoalsStats.objects.get(team=overall_team)
                        overall_lg_stats.overall_matches_played = overall_matches_played
                        overall_lg_stats.overall_scored_late = overall_scored_late
                        overall_lg_stats.overall_conceded_late = overall_conceded_late
                        overall_lg_stats.overall_scored_or_conceded_late = overall_scored_or_conceded_late
                        overall_lg_stats.save()
