import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5WonBothHalfStats, E5Team, E5WonBothHalfIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetWonBothHalves(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetWonBothHalves"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    WBH_IFRAMES: ClassVar[QuerySet[E5WonBothHalfIframes]] = E5WonBothHalfIframes.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.WBH_IFRAMES:
                iframe: E5WonBothHalfIframes  # Type hinting for Intellij

                ######################################### Won Both Halves ###########################################
                # Get Url
                self.get(url=iframe.won_both_half_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_won_both_halves: int = int(table_tr.find_all('td')[3].text)
                        home_won_both_halves_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_won_both_halves: int = int(table_tr.find_all('td')[8].text)
                        away_won_both_halves_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_won_both_halves: int = int(table_tr.find_all('td')[13].text)
                        overall_won_both_halves_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create Won Both Halves Home Stats
                    home_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    home_wbh_stats.team = home_team
                    home_wbh_stats.home_matches_played = home_matches_played
                    home_wbh_stats.home_won_both_halves = home_won_both_halves
                    home_wbh_stats.home_won_both_halves_percent = home_won_both_halves_percent

                    # Check if home stats already exists before saving or updating
                    if not home_wbh_stats.exists():
                        home_wbh_stats.save()
                        self.log_info(f"Team {home_team.name} Won Both Halves Stats created in database")
                    else:
                        home_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=home_team)
                        home_wbh_stats.home_matches_played = home_matches_played
                        home_wbh_stats.home_won_both_halves = home_won_both_halves
                        home_wbh_stats.home_won_both_halves_percent = home_won_both_halves_percent
                        home_wbh_stats.save()
                        self.log_info(f"Team {home_team.name} Won Both Halves Stats updated in database")

                    # Create Won Both Halves Away Stats
                    away_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    away_wbh_stats.team = away_team
                    away_wbh_stats.away_matches_played = away_matches_played
                    away_wbh_stats.away_won_both_halves = away_won_both_halves
                    away_wbh_stats.away_won_both_halves_percent = away_won_both_halves_percent

                    # Check if away stats already exists before saving or updating
                    if not away_wbh_stats.exists():
                        away_wbh_stats.save()
                        self.log_info(f"Team {away_team.name} Won Both Halves Stats created in database")
                    else:
                        away_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=away_team)
                        away_wbh_stats.away_matches_played = away_matches_played
                        away_wbh_stats.away_won_both_halves = away_won_both_halves
                        away_wbh_stats.away_won_both_halves_percent = away_won_both_halves_percent
                        away_wbh_stats.save()
                        self.log_info(f"Team {away_team.name} Won Both Halves Stats updated in database")

                    # Create Won Both Halves Overall Stats
                    overall_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    overall_wbh_stats.team = overall_team
                    overall_wbh_stats.overall_matches_played = overall_matches_played
                    overall_wbh_stats.overall_won_both_halves = overall_won_both_halves
                    overall_wbh_stats.overall_won_both_halves_percent = overall_won_both_halves_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_wbh_stats.exists():
                        overall_wbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Won Both Halves Stats created in database")
                    else:
                        overall_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=overall_team)
                        overall_wbh_stats.overall_matches_played = overall_matches_played
                        overall_wbh_stats.overall_won_both_halves = overall_won_both_halves
                        overall_wbh_stats.overall_won_both_halves_percent = overall_won_both_halves_percent
                        overall_wbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Won Both Halves Stats updated in database")

                ######################################### Lost Both Halves ###########################################
                # Get Url
                self.get(url=iframe.lost_both_half_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Lost Both Halves Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_lost_both_halves: int = int(table_tr.find_all('td')[3].text)
                        home_lost_both_halves_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_lost_both_halves: int = int(table_tr.find_all('td')[8].text)
                        away_lost_both_halves_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_lost_both_halves: int = int(table_tr.find_all('td')[13].text)
                        overall_lost_both_halves_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create Won Both Halves Home Stats
                    home_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    home_wbh_stats.team = home_team
                    home_wbh_stats.home_matches_played = home_matches_played
                    home_wbh_stats.home_lost_both_halves = home_lost_both_halves
                    home_wbh_stats.home_lost_both_halves_percent = home_lost_both_halves_percent

                    # Check if home stats already exists before saving or updating
                    if not home_wbh_stats.exists():
                        home_wbh_stats.save()
                        self.log_info(f"Team {home_team.name} Won Both Halves Stats created in database")
                    else:
                        home_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=home_team)
                        home_wbh_stats.home_matches_played = home_matches_played
                        home_wbh_stats.home_lost_both_halves = home_lost_both_halves
                        home_wbh_stats.home_lost_both_halves_percent = home_lost_both_halves_percent
                        home_wbh_stats.save()
                        self.log_info(f"Team {home_team.name} Won Both Halves Stats updated in database")

                    # Create Won Both Halves Away Stats
                    away_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    away_wbh_stats.team = away_team
                    away_wbh_stats.away_matches_played = away_matches_played
                    away_wbh_stats.away_lost_both_halves = away_lost_both_halves
                    away_wbh_stats.away_lost_both_halves_percent = away_lost_both_halves_percent

                    # Check if away stats already exists before saving or updating
                    if not away_wbh_stats.exists():
                        away_wbh_stats.save()
                        self.log_info(f"Team {away_team.name} Won Both Halves Stats created in database")
                    else:
                        away_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=away_team)
                        away_wbh_stats.away_matches_played = away_matches_played
                        away_wbh_stats.away_lost_both_halves = away_lost_both_halves
                        away_wbh_stats.away_lost_both_halves_percent = away_lost_both_halves_percent
                        away_wbh_stats.save()
                        self.log_info(f"Team {away_team.name} Won Both Halves Stats updated in database")

                    # Create Won Both Halves Overall Stats
                    overall_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats()
                    overall_wbh_stats.team = overall_team
                    overall_wbh_stats.overall_matches_played = overall_matches_played
                    overall_wbh_stats.overall_lost_both_halves = overall_lost_both_halves
                    overall_wbh_stats.overall_lost_both_halves_percent = overall_lost_both_halves_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_wbh_stats.exists():
                        overall_wbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Won Both Halves Stats created in database")
                    else:
                        overall_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=overall_team)
                        overall_wbh_stats.overall_matches_played = overall_matches_played
                        overall_wbh_stats.overall_lost_both_halves = overall_lost_both_halves
                        overall_wbh_stats.overall_lost_both_halves_percent = overall_lost_both_halves_percent
                        overall_wbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Won Both Halves Stats updated in database")
