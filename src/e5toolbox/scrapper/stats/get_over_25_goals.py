import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5Over25GoalsIframe, E5Team, E5Over25GoalsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetOver25Goals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetOver25Goals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    OVER_25_GOALS_IFRAMES: ClassVar[QuerySet[E5Over25GoalsIframe]] = E5Over25GoalsIframe.objects.filter(
        season__active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}over-2-5-goals/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get BTTS Iframes
                over_25_goals_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check iframes length
                if len(over_25_goals_iframes) != 4:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get Overs 2.5 Goals Iframe
                iframe: E5Over25GoalsIframe = E5Over25GoalsIframe()
                iframe.season = season
                for idx, over_25_goals_iframe in enumerate(over_25_goals_iframes):
                    try:
                        iframe_url: str = over_25_goals_iframe['src']
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_OVER_25_GOALS_IFRAME_URL_FAILED,
                            error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                        continue

                    if idx == 0:
                        iframe.over_25_goals_url = iframe_url
                    elif idx == 1:
                        iframe.over_25_goals_1h_url = iframe_url
                    elif idx == 2:
                        iframe.over_25_goals_2h_url = iframe_url
                    elif idx == 3:
                        iframe.over_25_goals_bh_url = iframe_url

                # Check iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} Over 2.5 Goals Iframe created in database")
                else:
                    target_iframe: E5Over25GoalsIframe = E5Over25GoalsIframe.objects.get(season=season)
                    target_iframe.over_25_goals_url = iframe.over_25_goals_url
                    target_iframe.over_25_goals_1h_url = iframe.over_25_goals_1h_url
                    target_iframe.over_25_goals_2h_url = iframe.over_25_goals_2h_url
                    target_iframe.over_25_goals_bh_url = iframe.over_25_goals_bh_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} Over 2.5 Goals Iframe updated in database")

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.OVER_25_GOALS_IFRAMES:
                iframe: E5Over25GoalsIframe  # Type hinting for Intellij

                ########################################### Over 2.5 Goals #############################################
                # Get Url
                self.get(url=iframe.over_25_goals_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 2.5 Goals Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
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

                    # Create Over 2.5 Goals Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals Home Stats created in database")
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals Home Stats updated in database")

                    # Create Over 2.5 Goals Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals Away Stats created in database")
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals Away Stats updated in database")

                    # Create Over 2.5 Goals Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals Overall Stats created in database")
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals Overall Stats updated in database")

                ######################################### Over 2.5 Goals 1H ############################################
                # Get Url
                self.get(url=iframe.over_25_goals_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 2.5 Goals 1H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
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

                    # Create Over 2.5 Goals 1H Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_1h = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_1h_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals 1H Home Stats created in database")
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_1h = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_1h_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals 1H Home Stats updated in database")

                    # Create Over 2.5 Goals 1H Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_1h = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_1h_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals 1H Away Stats created in database")
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_1h = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_1h_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals 1H Away Stats updated in database")

                    # Create Over 2.5 Goals 1H Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_1h = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_1h_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals 1H Overall Stats created in database")
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_1h = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_1h_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals 1H Overall Stats updated in database")

                ######################################### Over 2.5 Goals 2H ############################################
                # Get Url
                self.get(url=iframe.over_25_goals_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 2.5 Goals 2H Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
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

                    # Create Over 2.5 Goals 2H Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_2h = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_2h_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals 2H Home Stats created in database")
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_2h = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_2h_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals 2H Home Stats updated in database")

                    # Create Over 2.5 Goals 2H Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_2h = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_2h_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals 2H Away Stats created in database")
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_2h = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_2h_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals 2H Away Stats updated in database")

                    # Create Over 2.5 Goals 2H Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_2h = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_2h_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals 2H Overall Stats created in database")
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_2h = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_2h_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals 2H Overall Stats updated in database")

                ######################################### Over 2.5 Goals BH ############################################
                # Get Url
                self.get(url=iframe.over_25_goals_bh_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.select(selector='table.waffle.no-grid tr')

                # Get Over 2.5 Goals BH Stats
                for table_tr in table_trs:
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.select(selector='td')[2].text)
                        home_over_25_goals: int = int(table_tr.select(selector='td')[3].text)
                        home_over_25_goals_percent: str = table_tr.select(selector='td')[4].text
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.select(selector='td')[7].text)
                        away_over_25_goals: int = int(table_tr.select(selector='td')[8].text)
                        away_over_25_goals_percent: str = table_tr.select(selector='td')[9].text
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.select(selector='td')[12].text)
                        overall_over_25_goals: int = int(table_tr.select(selector='td')[13].text)
                        overall_over_25_goals_percent: str = table_tr.select(selector='td')[14].text
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

                    # Create Over 2.5 Goals BH Home Stats
                    home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    home_over_25_goals_stats.team = home_team
                    home_over_25_goals_stats.home_matches_played = home_matches_played
                    home_over_25_goals_stats.home_over_25_goals_bh = home_over_25_goals
                    home_over_25_goals_stats.home_over_25_goals_bh_percent = home_over_25_goals_percent

                    # Check if home stats already exists before saving or updating
                    if not home_over_25_goals_stats.exists():
                        home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals BH Home Stats created in database")
                    else:
                        target_home_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=home_team)
                        target_home_over_25_goals_stats.home_matches_played = home_matches_played
                        target_home_over_25_goals_stats.home_over_25_goals_bh = home_over_25_goals
                        target_home_over_25_goals_stats.home_over_25_goals_bh_percent = home_over_25_goals_percent
                        target_home_over_25_goals_stats.save()
                        self.log_info(f"Team {home_team.name} Over 2.5 Goals BH Home Stats updated in database")

                    # Create Over 2.5 Goals BH Away Stats
                    away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    away_over_25_goals_stats.team = away_team
                    away_over_25_goals_stats.away_matches_played = away_matches_played
                    away_over_25_goals_stats.away_over_25_goals_bh = away_over_25_goals
                    away_over_25_goals_stats.away_over_25_goals_bh_percent = away_over_25_goals_percent

                    # Check if away stats already exists before saving or updating
                    if not away_over_25_goals_stats.exists():
                        away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals BH Away Stats created in database")
                    else:
                        target_away_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=away_team)
                        target_away_over_25_goals_stats.away_matches_played = away_matches_played
                        target_away_over_25_goals_stats.away_over_25_goals_bh = away_over_25_goals
                        target_away_over_25_goals_stats.away_over_25_goals_bh_percent = away_over_25_goals_percent
                        target_away_over_25_goals_stats.save()
                        self.log_info(f"Team {away_team.name} Over 2.5 Goals BH Away Stats updated in database")

                    # Create Over 2.5 Goals BH Overall Stats
                    overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats()
                    overall_over_25_goals_stats.team = overall_team
                    overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                    overall_over_25_goals_stats.overall_over_25_goals_bh = overall_over_25_goals
                    overall_over_25_goals_stats.overall_over_25_goals_bh_percent = overall_over_25_goals_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_over_25_goals_stats.exists():
                        overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals BH Overall Stats created in database")
                    else:
                        target_overall_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(
                            team=overall_team)
                        target_overall_over_25_goals_stats.overall_matches_played = overall_matches_played
                        target_overall_over_25_goals_stats.overall_over_25_goals_bh = overall_over_25_goals
                        target_overall_over_25_goals_stats.overall_over_25_goals_bh_percent = overall_over_25_goals_percent
                        target_overall_over_25_goals_stats.save()
                        self.log_info(f"Team {overall_team.name} Over 2.5 Goals BH Overall Stats updated in database")
