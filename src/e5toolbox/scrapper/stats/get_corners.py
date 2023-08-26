import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5CornersIframes, E5Team, E5TeamCornerStats, E5MatchCornerStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetCorners(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCorners"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    CORNERS_IFRAMES: ClassVar[QuerySet[E5CornersIframes]] = E5CornersIframes.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.CORNERS_IFRAMES:
                iframe: E5CornersIframes  # Type hinting for Intellij

                ######################################### Team Corner For 1H ###########################################
                # Get Url
                self.get(url=iframe.team_corners_for_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner For 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_1h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner 1h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_1h = home_corners_for_1h
                    home_team_corner_stats.home_corners_for_1h_average = home_corners_for_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner 1h Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_1h = home_corners_for_1h
                        target_home_team_corner_stats.home_corners_for_1h_average = home_corners_for_1h_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner 1h Stats updated in database")

                    # Create Team Corner 1h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_1h = away_corners_for_1h
                    away_team_corner_stats.away_corners_for_1h_average = away_corners_for_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner 1h Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_1h = away_corners_for_1h
                        target_away_team_corner_stats.away_corners_for_1h_average = away_corners_for_1h_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner 1h Stats updated in database")

                    # Create Team Corner 1h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_1h = overall_corners_for_1h
                    overall_team_corner_stats.overall_corners_for_1h_average = overall_corners_for_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner 1h Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_1h = overall_corners_for_1h
                        target_overall_team_corner_stats.overall_corners_for_1h_average = overall_corners_for_1h_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner 1h Stats updated in database")

                ######################################### Team Corner For 2H ###########################################
                # Get Url
                self.get(url=iframe.team_corners_for_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner For 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_2h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner 2h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_2h = home_corners_for_2h
                    home_team_corner_stats.home_corners_for_2h_average = home_corners_for_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner 2h Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_2h = home_corners_for_2h
                        target_home_team_corner_stats.home_corners_for_2h_average = home_corners_for_2h_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner 2h Stats updated in database")

                    # Create Team Corner 2h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_2h = away_corners_for_2h
                    away_team_corner_stats.away_corners_for_2h_average = away_corners_for_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner 2h Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_2h = away_corners_for_2h
                        target_away_team_corner_stats.away_corners_for_2h_average = away_corners_for_2h_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner 2h Stats updated in database")

                    # Create Team Corner 2h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_2h = overall_corners_for_2h
                    overall_team_corner_stats.overall_corners_for_2h_average = overall_corners_for_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner 2h Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_2h = overall_corners_for_2h
                        target_overall_team_corner_stats.overall_corners_for_2h_average = overall_corners_for_2h_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner 2h Stats updated in database")

                ######################################### Team Corner For Ft ###########################################
                # Get Url
                self.get(url=iframe.team_corners_for_ft_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner For Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_for_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_for_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_for_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_for_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_for_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_for_ft_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner Ft Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_for_ft = home_corners_for_ft
                    home_team_corner_stats.home_corners_for_ft_average = home_corners_for_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Ft Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_for_ft = home_corners_for_ft
                        target_home_team_corner_stats.home_corners_for_ft_average = home_corners_for_ft_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Ft Stats updated in database")

                    # Create Team Corner Ft Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_for_ft = away_corners_for_ft
                    away_team_corner_stats.away_corners_for_ft_average = away_corners_for_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Ft Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_for_ft = away_corners_for_ft
                        target_away_team_corner_stats.away_corners_for_ft_average = away_corners_for_ft_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Ft Stats updated in database")

                    # Create Team Corner Ft Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_for_ft = overall_corners_for_ft
                    overall_team_corner_stats.overall_corners_for_ft_average = overall_corners_for_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Ft Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_for_ft = overall_corners_for_ft
                        target_overall_team_corner_stats.overall_corners_for_ft_average = overall_corners_for_ft_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Ft Stats updated in database")

                ####################################### Team Corner Against 1H #########################################
                # Get Url
                self.get(url=iframe.team_corners_against_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner Against 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_1h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner 1h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_1h = home_corners_against_1h
                    home_team_corner_stats.home_corners_against_1h_average = home_corners_against_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against 1h Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_1h = home_corners_against_1h
                        target_home_team_corner_stats.home_corners_against_1h_average = home_corners_against_1h_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against 1h Stats updated in database")

                    # Create Team Corner 1h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_1h = away_corners_against_1h
                    away_team_corner_stats.away_corners_against_1h_average = away_corners_against_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against 1h Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_1h = away_corners_against_1h
                        target_away_team_corner_stats.away_corners_against_1h_average = away_corners_against_1h_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against 1h Stats updated in database")

                    # Create Team Corner 1h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_1h = overall_corners_against_1h
                    overall_team_corner_stats.overall_corners_against_1h_average = overall_corners_against_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against 1h Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_1h = overall_corners_against_1h
                        target_overall_team_corner_stats.overall_corners_against_1h_average = overall_corners_against_1h_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against 1h Stats updated in database")

                ######################################### Team Corner Against 2H ###########################################
                # Get Url
                self.get(url=iframe.team_corners_against_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner Against 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_2h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner 2h Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_2h = home_corners_against_2h
                    home_team_corner_stats.home_corners_against_2h_average = home_corners_against_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against 2h Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_2h = home_corners_against_2h
                        target_home_team_corner_stats.home_corners_against_2h_average = home_corners_against_2h_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against 2h Stats updated in database")

                    # Create Team Corner 2h Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_2h = away_corners_against_2h
                    away_team_corner_stats.away_corners_against_2h_average = away_corners_against_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against 2h Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_2h = away_corners_against_2h
                        target_away_team_corner_stats.away_corners_against_2h_average = away_corners_against_2h_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against 2h Stats updated in database")

                    # Create Team Corner 2h Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_2h = overall_corners_against_2h
                    overall_team_corner_stats.overall_corners_against_2h_average = overall_corners_against_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against 2h Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_2h = overall_corners_against_2h
                        target_overall_team_corner_stats.overall_corners_against_2h_average = overall_corners_against_2h_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against 2h Stats updated in database")

                ######################################### Team Corner Against Ft ###########################################
                # Get Url
                self.get(url=iframe.team_corners_against_ft_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Team Corner Against Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_against_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_against_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_against_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_against_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_against_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_against_ft_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Team Corner Ft Home Stats
                    home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    home_team_corner_stats.team = home_team
                    home_team_corner_stats.home_matches_played = home_matches_played
                    home_team_corner_stats.home_corners_against_ft = home_corners_against_ft
                    home_team_corner_stats.home_corners_against_ft_average = home_corners_against_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_team_corner_stats.exists():
                        home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against Ft Stats created in database")
                    else:
                        target_home_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
                        target_home_team_corner_stats.home_matches_played = home_matches_played
                        target_home_team_corner_stats.home_corners_against_ft = home_corners_against_ft
                        target_home_team_corner_stats.home_corners_against_ft_average = home_corners_against_ft_average
                        target_home_team_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Corner Against Ft Stats updated in database")

                    # Create Team Corner Ft Away Stats
                    away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    away_team_corner_stats.team = away_team
                    away_team_corner_stats.away_matches_played = away_matches_played
                    away_team_corner_stats.away_corners_against_ft = away_corners_against_ft
                    away_team_corner_stats.away_corners_against_ft_average = away_corners_against_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_team_corner_stats.exists():
                        away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against Ft Stats created in database")
                    else:
                        target_away_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)
                        target_away_team_corner_stats.away_matches_played = away_matches_played
                        target_away_team_corner_stats.away_corners_against_ft = away_corners_against_ft
                        target_away_team_corner_stats.away_corners_against_ft_average = away_corners_against_ft_average
                        target_away_team_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Corner Against Ft Stats updated in database")

                    # Create Team Corner Ft Overall Stats
                    overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats()
                    overall_team_corner_stats.team = overall_team
                    overall_team_corner_stats.overall_matches_played = overall_matches_played
                    overall_team_corner_stats.overall_corners_against_ft = overall_corners_against_ft
                    overall_team_corner_stats.overall_corners_against_ft_average = overall_corners_against_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_team_corner_stats.exists():
                        overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against Ft Stats created in database")
                    else:
                        target_overall_team_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_team_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_team_corner_stats.overall_corners_against_ft = overall_corners_against_ft
                        target_overall_team_corner_stats.overall_corners_against_ft_average = overall_corners_against_ft_average
                        target_overall_team_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Corner Against Ft Stats updated in database")

                ########################################### Match Corner 1H ############################################
                # Get Url
                self.get(url=iframe.match_corners_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Match Corner 1h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_1h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_1h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_1h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_1h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_1h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_1h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Match Corner 1h Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_1h = home_corners_1h
                    home_match_corner_stats.home_corners_1h_average = home_corners_1h_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner 1h Stats created in database")
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_1h = home_corners_1h
                        target_home_match_corner_stats.home_corners_1h_average = home_corners_1h_average
                        target_home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner 1h Stats updated in database")

                    # Create Match Corner 1h Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_1h = away_corners_1h
                    away_match_corner_stats.away_corners_1h_average = away_corners_1h_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner 1h Stats created in database")
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_1h = away_corners_1h
                        target_away_match_corner_stats.away_corners_1h_average = away_corners_1h_average
                        target_away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner 1h Stats updated in database")

                    # Create Match Corner 1h Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_1h = overall_corners_1h
                    overall_match_corner_stats.overall_corners_1h_average = overall_corners_1h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner 1h Stats created in database")
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_1h = overall_corners_1h
                        target_overall_match_corner_stats.overall_corners_1h_average = overall_corners_1h_average
                        target_overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner 1h Stats updated in database")

                ########################################### Match Corner 2H ############################################
                # Get Url
                self.get(url=iframe.match_corners_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Match Corner 2h Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_2h: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_2h_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_2h: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_2h_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_2h: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_2h_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Match Corner 2h Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_2h = home_corners_2h
                    home_match_corner_stats.home_corners_2h_average = home_corners_2h_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner 2h Stats created in database")
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_2h = home_corners_2h
                        target_home_match_corner_stats.home_corners_2h_average = home_corners_2h_average
                        target_home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner 2h Stats updated in database")

                    # Create Match Corner 2h Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_2h = away_corners_2h
                    away_match_corner_stats.away_corners_2h_average = away_corners_2h_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner 2h Stats created in database")
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_2h = away_corners_2h
                        target_away_match_corner_stats.away_corners_2h_average = away_corners_2h_average
                        target_away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner 2h Stats updated in database")

                    # Create Match Corner 2h Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_2h = overall_corners_2h
                    overall_match_corner_stats.overall_corners_2h_average = overall_corners_2h_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner 2h Stats created in database")
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_2h = overall_corners_2h
                        target_overall_match_corner_stats.overall_corners_2h_average = overall_corners_2h_average
                        target_overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner 2h Stats updated in database")

                ########################################### Match Corner Ft ############################################
                # Get Url
                self.get(url=iframe.match_corners_ft_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Match Corner Ft Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_corners_ft: int = int(table_tr.select(selector='td')[3].text)
                        home_corners_ft_average: float = float(table_tr.select(selector='td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_corners_ft: int = int(table_tr.select(selector='td')[8].text)
                        away_corners_ft_average: float = float(table_tr.select(selector='td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_corners_ft: int = int(table_tr.select(selector='td')[13].text)
                        overall_corners_ft_average: float = float(table_tr.select(selector='td')[14].text)
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
                        continue

                    # Create Match Corner Ft Home Stats
                    home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    home_match_corner_stats.team = home_team
                    home_match_corner_stats.home_matches_played = home_matches_played
                    home_match_corner_stats.home_corners_ft = home_corners_ft
                    home_match_corner_stats.home_corners_ft_average = home_corners_ft_average

                    # Check if home stats already exists before saving or updating
                    if not home_match_corner_stats.exists():
                        home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner Ft Stats created in database")
                    else:
                        target_home_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=home_team)
                        target_home_match_corner_stats.home_matches_played = home_matches_played
                        target_home_match_corner_stats.home_corners_ft = home_corners_ft
                        target_home_match_corner_stats.home_corners_ft_average = home_corners_ft_average
                        target_home_match_corner_stats.save()
                        self.log_info(f"Team {home_team.name} Match Corner Ft Stats updated in database")

                    # Create Match Corner Ft Away Stats
                    away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    away_match_corner_stats.team = away_team
                    away_match_corner_stats.away_matches_played = away_matches_played
                    away_match_corner_stats.away_corners_ft = away_corners_ft
                    away_match_corner_stats.away_corners_ft_average = away_corners_ft_average

                    # Check if away stats already exists before saving or updating
                    if not away_match_corner_stats.exists():
                        away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner Ft Stats created in database")
                    else:
                        target_away_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(
                            team=away_team)
                        target_away_match_corner_stats.away_matches_played = away_matches_played
                        target_away_match_corner_stats.away_corners_ft = away_corners_ft
                        target_away_match_corner_stats.away_corners_ft_average = away_corners_ft_average
                        target_away_match_corner_stats.save()
                        self.log_info(f"Team {away_team.name} Match Corner Ft Stats updated in database")

                    # Create Match Corner Ft Overall Stats
                    overall_match_corner_stats: E5MatchCornerStats = E5MatchCornerStats()
                    overall_match_corner_stats.team = overall_team
                    overall_match_corner_stats.overall_matches_played = overall_matches_played
                    overall_match_corner_stats.overall_corners_ft = overall_corners_ft
                    overall_match_corner_stats.overall_corners_ft_average = overall_corners_ft_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_match_corner_stats.exists():
                        overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner Ft Stats created in database")
                    else:
                        target_overall_match_corner_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(
                            team=overall_team)
                        target_overall_match_corner_stats.overall_matches_played = overall_matches_played
                        target_overall_match_corner_stats.overall_corners_ft = overall_corners_ft
                        target_overall_match_corner_stats.overall_corners_ft_average = overall_corners_ft_average
                        target_overall_match_corner_stats.save()
                        self.log_info(f"Team {overall_team.name} Match Corner Ft Stats updated in database")
