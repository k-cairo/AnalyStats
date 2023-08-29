import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5HalfTimeFullTimeIframe, E5Team, E5HalfTimeFullTimeStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetHalfTimeFullTime(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetHalfTimeFullTime"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    HT_FT_IFRAMES: ClassVar[QuerySet[E5HalfTimeFullTimeIframe]] = E5HalfTimeFullTimeIframe.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.HT_FT_IFRAMES:
                iframe: E5HalfTimeFullTimeIframe  # Type hinting for Intellij

                ######################################## Half Time Full Time ###########################################
                # Get Url
                self.get(url=iframe.url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Half Time Full Time Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_win_win: int = int(table_tr.find_all('td')[3].text)
                        home_win_draw: int = int(table_tr.find_all('td')[4].text)
                        home_win_loss: int = int(table_tr.find_all('td')[5].text)
                        home_draw_win: int = int(table_tr.find_all('td')[6].text)
                        home_draw_draw: int = int(table_tr.find_all('td')[7].text)
                        home_draw_loss: int = int(table_tr.find_all('td')[8].text)
                        home_loss_win: int = int(table_tr.find_all('td')[9].text)
                        home_loss_draw: int = int(table_tr.find_all('td')[10].text)
                        home_loss_loss: int = int(table_tr.find_all('td')[11].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[14].text)
                        away_win_win: int = int(table_tr.find_all('td')[15].text)
                        away_win_draw: int = int(table_tr.find_all('td')[16].text)
                        away_win_loss: int = int(table_tr.find_all('td')[17].text)
                        away_draw_win: int = int(table_tr.find_all('td')[18].text)
                        away_draw_draw: int = int(table_tr.find_all('td')[19].text)
                        away_draw_loss: int = int(table_tr.find_all('td')[20].text)
                        away_loss_win: int = int(table_tr.find_all('td')[21].text)
                        away_loss_draw: int = int(table_tr.find_all('td')[22].text)
                        away_loss_loss: int = int(table_tr.find_all('td')[23].text)
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

                    # Create Half Time Full Time Home Stats
                    home_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats()
                    home_ht_ft_stats.team = home_team
                    home_ht_ft_stats.home_matches_played = home_matches_played
                    home_ht_ft_stats.home_win_win = home_win_win
                    home_ht_ft_stats.home_win_draw = home_win_draw
                    home_ht_ft_stats.home_win_loss = home_win_loss
                    home_ht_ft_stats.home_draw_win = home_draw_win
                    home_ht_ft_stats.home_draw_draw = home_draw_draw
                    home_ht_ft_stats.home_draw_loss = home_draw_loss
                    home_ht_ft_stats.home_loss_win = home_loss_win
                    home_ht_ft_stats.home_loss_draw = home_loss_draw
                    home_ht_ft_stats.home_loss_loss = home_loss_loss

                    # Check if home stats already exists before saving or updating
                    if not home_ht_ft_stats.exists():
                        home_ht_ft_stats.save()
                        self.log_info(f"Team {home_team.name} Half Time Full Time Stats created in database")
                    else:
                        target_home_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats.objects.get(
                            team=home_team)
                        target_home_ht_ft_stats.home_matches_played = home_matches_played
                        target_home_ht_ft_stats.home_win_win = home_win_win
                        target_home_ht_ft_stats.home_win_draw = home_win_draw
                        target_home_ht_ft_stats.home_win_loss = home_win_loss
                        target_home_ht_ft_stats.home_draw_win = home_draw_win
                        target_home_ht_ft_stats.home_draw_draw = home_draw_draw
                        target_home_ht_ft_stats.home_draw_loss = home_draw_loss
                        target_home_ht_ft_stats.home_loss_win = home_loss_win
                        target_home_ht_ft_stats.home_loss_draw = home_loss_draw
                        target_home_ht_ft_stats.home_loss_loss = home_loss_loss
                        target_home_ht_ft_stats.save()
                        self.log_info(f"Team {home_team.name} Half Time Full Time Stats updated in database")

                    # Create Half Time Full Time Away Stats
                    away_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats()
                    away_ht_ft_stats.team = away_team
                    away_ht_ft_stats.away_matches_played = away_matches_played
                    away_ht_ft_stats.away_win_win = away_win_win
                    away_ht_ft_stats.away_win_draw = away_win_draw
                    away_ht_ft_stats.away_win_loss = away_win_loss
                    away_ht_ft_stats.away_draw_win = away_draw_win
                    away_ht_ft_stats.away_draw_draw = away_draw_draw
                    away_ht_ft_stats.away_draw_loss = away_draw_loss
                    away_ht_ft_stats.away_loss_win = away_loss_win
                    away_ht_ft_stats.away_loss_draw = away_loss_draw
                    away_ht_ft_stats.away_loss_loss = away_loss_loss

                    # Check if away stats already exists before saving or updating
                    if not away_ht_ft_stats.exists():
                        away_ht_ft_stats.save()
                        self.log_info(f"Team {away_team.name} Half Time Full Time Stats created in database")
                    else:
                        target_away_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats.objects.get(
                            team=away_team)
                        target_away_ht_ft_stats.away_matches_played = away_matches_played
                        target_away_ht_ft_stats.away_win_win = away_win_win
                        target_away_ht_ft_stats.away_win_draw = away_win_draw
                        target_away_ht_ft_stats.away_win_loss = away_win_loss
                        target_away_ht_ft_stats.away_draw_win = away_draw_win
                        target_away_ht_ft_stats.away_draw_draw = away_draw_draw
                        target_away_ht_ft_stats.away_draw_loss = away_draw_loss
                        target_away_ht_ft_stats.away_loss_win = away_loss_win
                        target_away_ht_ft_stats.away_loss_draw = away_loss_draw
                        target_away_ht_ft_stats.away_loss_loss = away_loss_loss
                        target_away_ht_ft_stats.save()
                        self.log_info(f"Team {away_team.name} Half Time Full Time Stats updated in database")
