import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5RescuedPointsIframe, E5Team, E5RescuedPointsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetRescuedPoints(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetRescuedPoints"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    RP_IFRAMES: ClassVar[QuerySet[E5RescuedPointsIframe]] = E5RescuedPointsIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.RP_IFRAMES:
                iframe: E5RescuedPointsIframe  # Type hinting for Intellij

                ############################################# Rescued Points ###########################################
                # Get Url
                self.get(url=iframe.url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                    home_conceded_first: int = 0
                    home_drawn_after_conceding_first: int = 0
                    home_won_after_conceding_first: int = 0
                    home_rescued_points: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_conceded_first: int = 0
                    away_drawn_after_conceding_first: int = 0
                    away_won_after_conceding_first: int = 0
                    away_rescued_points: int = 0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_conceded_first: int = 0
                    overall_drawn_after_conceding_first: int = 0
                    overall_won_after_conceding_first: int = 0
                    overall_rescued_points: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_conceded_first: int = int(table_tr.find_all('td')[3].text)
                        home_drawn_after_conceding_first: int = int(table_tr.find_all('td')[4].text)
                        home_won_after_conceding_first: int = int(table_tr.find_all('td')[5].text)
                        home_rescued_points: int = int(table_tr.find_all('td')[6].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[9].text)
                        away_conceded_first: int = int(table_tr.find_all('td')[10].text)
                        away_drawn_after_conceding_first: int = int(table_tr.find_all('td')[11].text)
                        away_won_after_conceding_first: int = int(table_tr.find_all('td')[12].text)
                        away_rescued_points: int = int(table_tr.find_all('td')[13].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[16].text)
                        overall_conceded_first: int = int(table_tr.find_all('td')[17].text)
                        overall_drawn_after_conceding_first: int = int(table_tr.find_all('td')[18].text)
                        overall_won_after_conceding_first: int = int(table_tr.find_all('td')[19].text)
                        overall_rescued_points: int = int(table_tr.find_all('td')[20].text)
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
                    home_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats()
                    home_rp_stats.team = home_team
                    home_rp_stats.home_matches_played = home_matches_played
                    home_rp_stats.home_conceded_first = home_conceded_first
                    home_rp_stats.home_drawn_after_conceding_first = home_drawn_after_conceding_first
                    home_rp_stats.home_won_after_conceding_first = home_won_after_conceding_first
                    home_rp_stats.home_rescued_points = home_rescued_points

                    # Check if home stats already exists before saving or updating
                    if not home_rp_stats.exists():
                        home_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {home_team.name} created")
                    else:
                        home_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats.objects.get(team=home_team)
                        home_rp_stats.home_matches_played = home_matches_played
                        home_rp_stats.home_conceded_first = home_conceded_first
                        home_rp_stats.home_drawn_after_conceding_first = home_drawn_after_conceding_first
                        home_rp_stats.home_won_after_conceding_first = home_won_after_conceding_first
                        home_rp_stats.home_rescued_points = home_rescued_points
                        home_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {home_team.name} updated")

                    # Create Away Stats
                    away_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats()
                    away_rp_stats.team = away_team
                    away_rp_stats.away_matches_played = away_matches_played
                    away_rp_stats.away_conceded_first = away_conceded_first
                    away_rp_stats.away_drawn_after_conceding_first = away_drawn_after_conceding_first
                    away_rp_stats.away_won_after_conceding_first = away_won_after_conceding_first
                    away_rp_stats.away_rescued_points = away_rescued_points

                    # Check if away stats already exists before saving or updating
                    if not away_rp_stats.exists():
                        away_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {away_team.name} created")
                    else:
                        away_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats.objects.get(team=away_team)
                        away_rp_stats.away_matches_played = away_matches_played
                        away_rp_stats.away_conceded_first = away_conceded_first
                        away_rp_stats.away_drawn_after_conceding_first = away_drawn_after_conceding_first
                        away_rp_stats.away_won_after_conceding_first = away_won_after_conceding_first
                        away_rp_stats.away_rescued_points = away_rescued_points
                        away_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {away_team.name} updated")

                    # Create Overall Stats
                    overall_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats()
                    overall_rp_stats.team = overall_team
                    overall_rp_stats.overall_matches_played = overall_matches_played
                    overall_rp_stats.overall_conceded_first = overall_conceded_first
                    overall_rp_stats.overall_drawn_after_conceding_first = overall_drawn_after_conceding_first
                    overall_rp_stats.overall_won_after_conceding_first = overall_won_after_conceding_first
                    overall_rp_stats.overall_rescued_points = overall_rescued_points

                    # Check if overall stats already exists before saving or updating
                    if not overall_rp_stats.exists():
                        overall_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {overall_team.name} created")
                    else:
                        overall_rp_stats: E5RescuedPointsStats = E5RescuedPointsStats.objects.get(team=overall_team)
                        overall_rp_stats.overall_matches_played = overall_matches_played
                        overall_rp_stats.overall_conceded_first = overall_conceded_first
                        overall_rp_stats.overall_drawn_after_conceding_first = overall_drawn_after_conceding_first
                        overall_rp_stats.overall_won_after_conceding_first = overall_won_after_conceding_first
                        overall_rp_stats.overall_rescued_points = overall_rescued_points
                        overall_rp_stats.save()
                        self.log_info(message=f"Parse Rescued Points Stats : {overall_team.name} updated")
