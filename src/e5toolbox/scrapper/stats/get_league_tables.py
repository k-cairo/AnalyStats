import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5LeagueTableIframe, E5Team, E5TeamRanking
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetLeagueTables(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetLeagueTables"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    ACTIVE_LEAGUE_TABLE_IFRAMES: ClassVar[QuerySet[E5LeagueTableIframe]] = E5LeagueTableIframe.objects.filter(
        season__active=True)

    # E5
    def get_teams_ranking(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for league_table in self.ACTIVE_LEAGUE_TABLE_IFRAMES:
                league_table: E5LeagueTableIframe  # Type hinting for Intellij

                # Get Url
                self.get(url=league_table.url, error_context=f"{self.ERROR_CONTEXT}.get_active_seasons_teams_ranking()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Teams Ranking
                table_trs: ResultSet[Tag] = []
                table_trs: ResultSet[Tag] = self.soup.select(selector="table.waffle.no-grid tr")

                # Get Team Ranking
                for table_tr in table_trs:
                    ranking: int = 0
                    team_name: str = ""
                    matchs_played: int = 0
                    matchs_won: int = 0
                    matchs_drawn: int = 0
                    matchs_lost: int = 0
                    goals_scored: int = 0
                    goals_conceded: int = 0
                    goals_difference: int = 0
                    points: int = 0
                    try:
                        ranking: int = int(table_tr.select(selector="td")[1].text)
                        team_name: str = table_tr.select_one(selector="td a[target='_blank']").text
                        matchs_played: int = int(table_tr.select(selector="td")[3].text)
                        matchs_won: int = int(table_tr.select(selector="td")[4].text)
                        matchs_drawn: int = int(table_tr.select(selector="td")[5].text)
                        matchs_lost: int = int(table_tr.select(selector="td")[6].text)
                        goals_scored: int = int(table_tr.select(selector="td")[7].text)
                        goals_conceded: int = int(table_tr.select(selector="td")[8].text)
                        goals_difference: int = int(table_tr.select(selector="td")[9].text)
                        points: int = int(table_tr.select(selector="td")[10].text)
                    except Exception:
                        continue

                    # Get Team
                    try:
                        team: E5Team | None = None
                        team = E5Team.objects.get(name=team_name, season=league_table.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED, exception=ex,
                                       error_context=f"{self.ERROR_CONTEXT}.get_active_seasons_teams_ranking()")
                        self.init_status()
                        continue

                    # Create Team Ranking
                    team_ranking: E5TeamRanking = E5TeamRanking()
                    team_ranking.ranking = ranking
                    team_ranking.team = team
                    team_ranking.matches_played = matchs_played
                    team_ranking.matches_won = matchs_won
                    team_ranking.matches_drawn = matchs_drawn
                    team_ranking.matches_lost = matchs_lost
                    team_ranking.goals_scored = goals_scored
                    team_ranking.goals_conceded = goals_conceded
                    team_ranking.goals_difference = goals_difference
                    team_ranking.points = points

                    # Check if team ranking already exists before saving or updating
                    if not team_ranking.exists():
                        team_ranking.save()
                    else:
                        target_team_ranking: E5TeamRanking = E5TeamRanking.objects.get(team=team)
                        target_team_ranking.ranking = ranking
                        target_team_ranking.matches_played = matchs_played
                        target_team_ranking.matches_won = matchs_won
                        target_team_ranking.matches_drawn = matchs_drawn
                        target_team_ranking.matches_lost = matchs_lost
                        target_team_ranking.goals_scored = goals_scored
                        target_team_ranking.goals_conceded = goals_conceded
                        target_team_ranking.goals_difference = goals_difference
                        target_team_ranking.points = points
                        target_team_ranking.save()
