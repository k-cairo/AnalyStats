import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5WinDrawLossPercentageIframe, E5Team, E5WinDrawLossPercentageStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetWinDrawLossPercentage(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetWinDrawLossPercentage"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    WDLP_IFRAMES: ClassVar[QuerySet[E5WinDrawLossPercentageIframe]] = E5WinDrawLossPercentageIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.WDLP_IFRAMES:
                iframe: E5WinDrawLossPercentageIframe  # Type hinting for Intellij

                ###################################### Win Draw Loss Percentage ########################################
                # Get Url
                self.get(url=iframe.url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Win Draw Loss Percentage Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_win_percentage: int = int(table_tr.find_all('td')[3].text.strip('%'))
                        home_draw_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        home_loss_percentage: int = int(table_tr.find_all('td')[5].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[8].text)
                        away_win_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        away_draw_percentage: int = int(table_tr.find_all('td')[10].text.strip('%'))
                        away_loss_percentage: int = int(table_tr.find_all('td')[11].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[14].text)
                        overall_win_percentage: int = int(table_tr.find_all('td')[15].text.strip('%'))
                        overall_draw_percentage: int = int(table_tr.find_all('td')[16].text.strip('%'))
                        overall_loss_percentage: int = int(table_tr.find_all('td')[17].text.strip('%'))
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

                    # Create Win Draw Loss Percentage Home Stats
                    home_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats()
                    home_wdlp_stats.team = home_team
                    home_wdlp_stats.home_matches_played = home_matches_played
                    home_wdlp_stats.home_win_percent = home_win_percentage
                    home_wdlp_stats.home_draw_percent = home_draw_percentage
                    home_wdlp_stats.home_loss_percent = home_loss_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_wdlp_stats.exists():
                        home_wdlp_stats.save()
                        self.log_info(f"Team {home_team.name} Win Draw Loss Percentage Stats created in database")
                    else:
                        target_home_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats.objects.get(
                            team=home_team)
                        target_home_wdlp_stats.home_matches_played = home_matches_played
                        target_home_wdlp_stats.home_win_percent = home_win_percentage
                        target_home_wdlp_stats.home_draw_percent = home_draw_percentage
                        target_home_wdlp_stats.home_loss_percent = home_loss_percentage
                        target_home_wdlp_stats.save()
                        self.log_info(f"Team {home_team.name} Win Draw Loss Percentage Stats updated in database")

                    # Create Win Draw Loss Percentage Away Stats
                    away_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats()
                    away_wdlp_stats.team = away_team
                    away_wdlp_stats.away_matches_played = away_matches_played
                    away_wdlp_stats.away_win_percent = away_win_percentage
                    away_wdlp_stats.away_draw_percent = away_draw_percentage
                    away_wdlp_stats.away_loss_percent = away_loss_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_wdlp_stats.exists():
                        away_wdlp_stats.save()
                        self.log_info(f"Team {away_team.name} Win Draw Loss Percentage Stats created in database")
                    else:
                        target_away_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats.objects.get(
                            team=away_team)
                        target_away_wdlp_stats.away_matches_played = away_matches_played
                        target_away_wdlp_stats.away_win_percent = away_win_percentage
                        target_away_wdlp_stats.away_draw_percent = away_draw_percentage
                        target_away_wdlp_stats.away_loss_percent = away_loss_percentage
                        target_away_wdlp_stats.save()
                        self.log_info(f"Team {away_team.name} Win Draw Loss Percentage Stats updated in database")

                    # Create Win Draw Loss Percentage Overall Stats
                    overall_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats()
                    overall_wdlp_stats.team = overall_team
                    overall_wdlp_stats.overall_matches_played = overall_matches_played
                    overall_wdlp_stats.overall_win_percent = overall_win_percentage
                    overall_wdlp_stats.overall_draw_percent = overall_draw_percentage
                    overall_wdlp_stats.overall_loss_percent = overall_loss_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_wdlp_stats.exists():
                        overall_wdlp_stats.save()
                        self.log_info(f"Team {overall_team.name} Win Draw Loss Percentage Stats created in database")
                    else:
                        target_overall_wdlp_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats.objects.get(
                            team=overall_team)
                        target_overall_wdlp_stats.overall_matches_played = overall_matches_played
                        target_overall_wdlp_stats.overall_win_percent = overall_win_percentage
                        target_overall_wdlp_stats.overall_draw_percent = overall_draw_percentage
                        target_overall_wdlp_stats.overall_loss_percent = overall_loss_percentage
                        target_overall_wdlp_stats.save()
                        self.log_info(f"Team {overall_team.name} Win Draw Loss Percentage Stats updated in database")
