import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5WinLossMarginIframe, E5Team, E5WinLossMarginStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetWinLossMargin(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetWinLossMargin"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    WLM_IFRAMES: ClassVar[QuerySet[E5WinLossMarginIframe]] = E5WinLossMarginIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.WLM_IFRAMES:
                iframe: E5WinLossMarginIframe  # Type hinting for Intellij

                ############################################# Winning Margins ##########################################
                # Get Url
                self.get(url=iframe.winning_margins_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                    home_games_won: int = 0
                    home_games_won_by_1: int = 0
                    home_games_won_by_2: int = 0
                    home_games_won_by_3: int = 0
                    home_games_won_by_4_or_more: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_games_won: int = 0
                    away_games_won_by_1: int = 0
                    away_games_won_by_2: int = 0
                    away_games_won_by_3: int = 0
                    away_games_won_by_4_or_more: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_games_won: int = int(table_tr.find_all('td')[3].text)
                        home_games_won_by_1: int = int(table_tr.find_all('td')[4].text)
                        home_games_won_by_2: int = int(table_tr.find_all('td')[5].text)
                        home_games_won_by_3: int = int(table_tr.find_all('td')[6].text)
                        home_games_won_by_4_or_more: int = int(table_tr.find_all('td')[7].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[10].text)
                        away_games_won: int = int(table_tr.find_all('td')[11].text)
                        away_games_won_by_1: int = int(table_tr.find_all('td')[12].text)
                        away_games_won_by_2: int = int(table_tr.find_all('td')[13].text)
                        away_games_won_by_3: int = int(table_tr.find_all('td')[14].text)
                        away_games_won_by_4_or_more: int = int(table_tr.find_all('td')[15].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Home Stats
                    home_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats()
                    home_wlm_stats.team = home_team
                    home_wlm_stats.home_matches_played = home_matches_played
                    home_wlm_stats.home_games_won = home_games_won
                    home_wlm_stats.home_games_won_by_1 = home_games_won_by_1
                    home_wlm_stats.home_games_won_by_2 = home_games_won_by_2
                    home_wlm_stats.home_games_won_by_3 = home_games_won_by_3
                    home_wlm_stats.home_games_won_by_4_or_more = home_games_won_by_4_or_more

                    # Check if home stats already exists before saving or updating
                    if not home_wlm_stats.exists():
                        home_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {home_team.name} created")
                    else:
                        home_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=home_team)
                        home_wlm_stats.home_matches_played = home_matches_played
                        home_wlm_stats.home_games_won = home_games_won
                        home_wlm_stats.home_games_won_by_1 = home_games_won_by_1
                        home_wlm_stats.home_games_won_by_2 = home_games_won_by_2
                        home_wlm_stats.home_games_won_by_3 = home_games_won_by_3
                        home_wlm_stats.home_games_won_by_4_or_more = home_games_won_by_4_or_more
                        home_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {home_team.name} updated")

                    # Create Away Stats
                    away_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats()
                    away_wlm_stats.team = away_team
                    away_wlm_stats.away_matches_played = away_matches_played
                    away_wlm_stats.away_games_won = away_games_won
                    away_wlm_stats.away_games_won_by_1 = away_games_won_by_1
                    away_wlm_stats.away_games_won_by_2 = away_games_won_by_2
                    away_wlm_stats.away_games_won_by_3 = away_games_won_by_3
                    away_wlm_stats.away_games_won_by_4_or_more = away_games_won_by_4_or_more

                    # Check if away stats already exists before saving or updating
                    if not away_wlm_stats.exists():
                        away_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {away_team.name} created")
                    else:
                        away_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=away_team)
                        away_wlm_stats.away_matches_played = away_matches_played
                        away_wlm_stats.away_games_won = away_games_won
                        away_wlm_stats.away_games_won_by_1 = away_games_won_by_1
                        away_wlm_stats.away_games_won_by_2 = away_games_won_by_2
                        away_wlm_stats.away_games_won_by_3 = away_games_won_by_3
                        away_wlm_stats.away_games_won_by_4_or_more = away_games_won_by_4_or_more
                        away_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {away_team.name} updated")

                ############################################# Losing Margins ###########################################
                # Get Url
                self.get(url=iframe.losing_margins_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                    home_games_loose: int = 0
                    home_games_loose_by_1: int = 0
                    home_games_loose_by_2: int = 0
                    home_games_loose_by_3: int = 0
                    home_games_loose_by_4_or_more: int = 0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_games_loose: int = 0
                    away_games_loose_by_1: int = 0
                    away_games_loose_by_2: int = 0
                    away_games_loose_by_3: int = 0
                    away_games_loose_by_4_or_more: int = 0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_games_loose: int = int(table_tr.find_all('td')[3].text)
                        home_games_loose_by_1: int = int(table_tr.find_all('td')[4].text)
                        home_games_loose_by_2: int = int(table_tr.find_all('td')[5].text)
                        home_games_loose_by_3: int = int(table_tr.find_all('td')[6].text)
                        home_games_loose_by_4_or_more: int = int(table_tr.find_all('td')[7].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[10].text)
                        away_games_loose: int = int(table_tr.find_all('td')[11].text)
                        away_games_loose_by_1: int = int(table_tr.find_all('td')[12].text)
                        away_games_loose_by_2: int = int(table_tr.find_all('td')[13].text)
                        away_games_loose_by_3: int = int(table_tr.find_all('td')[14].text)
                        away_games_loose_by_4_or_more: int = int(table_tr.find_all('td')[15].text)
                    except Exception:
                        continue

                    # Get Teams
                    try:
                        home_team: E5Team = E5Team.objects.get(name=home_team_name, season=iframe.season)
                        away_team: E5Team = E5Team.objects.get(name=away_team_name, season=iframe.season)
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_TEAM_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.parse_iframes()", exception=ex)
                        self.init_status()
                        continue

                    # Create Home Stats
                    home_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats()
                    home_wlm_stats.team = home_team
                    home_wlm_stats.home_matches_played = home_matches_played
                    home_wlm_stats.home_games_loose = home_games_loose
                    home_wlm_stats.home_games_loose_by_1 = home_games_loose_by_1
                    home_wlm_stats.home_games_loose_by_2 = home_games_loose_by_2
                    home_wlm_stats.home_games_loose_by_3 = home_games_loose_by_3
                    home_wlm_stats.home_games_loose_by_4_or_more = home_games_loose_by_4_or_more

                    # Check if home stats already exists before saving or updating
                    if not home_wlm_stats.exists():
                        home_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {home_team.name} created")
                    else:
                        home_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=home_team)
                        home_wlm_stats.home_matches_played = home_matches_played
                        home_wlm_stats.home_games_loose = home_games_loose
                        home_wlm_stats.home_games_loose_by_1 = home_games_loose_by_1
                        home_wlm_stats.home_games_loose_by_2 = home_games_loose_by_2
                        home_wlm_stats.home_games_loose_by_3 = home_games_loose_by_3
                        home_wlm_stats.home_games_loose_by_4_or_more = home_games_loose_by_4_or_more
                        home_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {home_team.name} updated")

                    # Create Away Stats
                    away_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats()
                    away_wlm_stats.team = away_team
                    away_wlm_stats.away_matches_played = away_matches_played
                    away_wlm_stats.away_games_loose = away_games_loose
                    away_wlm_stats.away_games_loose_by_1 = away_games_loose_by_1
                    away_wlm_stats.away_games_loose_by_2 = away_games_loose_by_2
                    away_wlm_stats.away_games_loose_by_3 = away_games_loose_by_3
                    away_wlm_stats.away_games_loose_by_4_or_more = away_games_loose_by_4_or_more

                    # Check if away stats already exists before saving or updating
                    if not away_wlm_stats.exists():
                        away_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {away_team.name} created")
                    else:
                        away_wlm_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=away_team)
                        away_wlm_stats.away_matches_played = away_matches_played
                        away_wlm_stats.away_games_loose = away_games_loose
                        away_wlm_stats.away_games_loose_by_1 = away_games_loose_by_1
                        away_wlm_stats.away_games_loose_by_2 = away_games_loose_by_2
                        away_wlm_stats.away_games_loose_by_3 = away_games_loose_by_3
                        away_wlm_stats.away_games_loose_by_4_or_more = away_games_loose_by_4_or_more
                        away_wlm_stats.save()
                        self.log_info(message=f"Parse Win Loss Margin Stats : {away_team.name} updated")
