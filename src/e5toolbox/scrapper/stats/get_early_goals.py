import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5EarlyGoalsIframe, E5Team, E5EarlyGoalsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetEarlyGoals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetEarlyGoals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    EG_IFRAMES: ClassVar[QuerySet[E5EarlyGoalsIframe]] = E5EarlyGoalsIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.EG_IFRAMES:
                iframe: E5EarlyGoalsIframe  # Type hinting for Intellij

                ############################################# Early Goals ##############################################
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
                        home_scored_early: int = int(table_tr.find_all('td')[3].text)
                        home_conceded_early: int = int(table_tr.find_all('td')[4].text)
                        home_scored_or_conceded_early: int = int(table_tr.find_all('td')[5].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[8].text)
                        away_scored_early: int = int(table_tr.find_all('td')[9].text)
                        away_conceded_early: int = int(table_tr.find_all('td')[10].text)
                        away_scored_or_conceded_early: int = int(table_tr.find_all('td')[11].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[14].text)
                        overall_scored_early: int = int(table_tr.find_all('td')[15].text)
                        overall_conceded_early: int = int(table_tr.find_all('td')[16].text)
                        overall_scored_or_conceded_early: int = int(table_tr.find_all('td')[17].text)
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
                    home_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats()
                    home_eg_stats.team = home_team
                    home_eg_stats.home_matches_played = home_matches_played
                    home_eg_stats.home_scored_early = home_scored_early
                    home_eg_stats.home_conceded_early = home_conceded_early
                    home_eg_stats.home_scored_or_conceded_early = home_scored_or_conceded_early

                    # Check if home stats already exists before saving or updating
                    if not home_eg_stats.exists():
                        home_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {home_team.name} created")
                    else:
                        home_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats.objects.get(team=home_team)
                        home_eg_stats.home_matches_played = home_matches_played
                        home_eg_stats.home_scored_early = home_scored_early
                        home_eg_stats.home_conceded_early = home_conceded_early
                        home_eg_stats.home_scored_or_conceded_early = home_scored_or_conceded_early
                        home_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {home_team.name} updated")

                    # Create Away Stats
                    away_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats()
                    away_eg_stats.team = away_team
                    away_eg_stats.away_matches_played = away_matches_played
                    away_eg_stats.away_scored_early = away_scored_early
                    away_eg_stats.away_conceded_early = away_conceded_early
                    away_eg_stats.away_scored_or_conceded_early = away_scored_or_conceded_early

                    # Check if away stats already exists before saving or updating
                    if not away_eg_stats.exists():
                        away_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {away_team.name} created")
                    else:
                        away_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats.objects.get(team=away_team)
                        away_eg_stats.away_matches_played = away_matches_played
                        away_eg_stats.away_scored_early = away_scored_early
                        away_eg_stats.away_conceded_early = away_conceded_early
                        away_eg_stats.away_scored_or_conceded_early = away_scored_or_conceded_early
                        away_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {away_team.name} updated")

                    # Create Overall Stats
                    overall_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats()
                    overall_eg_stats.team = overall_team
                    overall_eg_stats.overall_matches_played = overall_matches_played
                    overall_eg_stats.overall_scored_early = overall_scored_early
                    overall_eg_stats.overall_conceded_early = overall_conceded_early
                    overall_eg_stats.overall_scored_or_conceded_early = overall_scored_or_conceded_early

                    # Check if overall stats already exists before saving or updating
                    if not overall_eg_stats.exists():
                        overall_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {overall_team.name} created")
                    else:
                        overall_eg_stats: E5EarlyGoalsStats = E5EarlyGoalsStats.objects.get(team=overall_team)
                        overall_eg_stats.overall_matches_played = overall_matches_played
                        overall_eg_stats.overall_scored_early = overall_scored_early
                        overall_eg_stats.overall_conceded_early = overall_conceded_early
                        overall_eg_stats.overall_scored_or_conceded_early = overall_scored_or_conceded_early
                        overall_eg_stats.save()
                        self.log_info(message=f"Parse Early Goals Stats : {overall_team.name} updated")
