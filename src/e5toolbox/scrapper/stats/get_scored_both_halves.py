import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5ScoredBothHalfStats, E5Team, E5ScoredBothHalfIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetScoredBothHalves(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetScoredBothHalves"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    SBH_IFRAMES: ClassVar[QuerySet[E5ScoredBothHalfIframes]] = E5ScoredBothHalfIframes.objects.filter(
        season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.SBH_IFRAMES:
                iframe: E5ScoredBothHalfIframes  # Type hinting for Intellij

                ######################################### Scored Both Halves ###########################################
                # Get Url
                self.get(url=iframe.scored_both_half_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Scored Both Halves Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_scored_both_halves: int = int(table_tr.find_all('td')[3].text)
                        home_scored_both_halves_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_scored_both_halves: int = int(table_tr.find_all('td')[8].text)
                        away_scored_both_halves_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_scored_both_halves: int = int(table_tr.find_all('td')[13].text)
                        overall_scored_both_halves_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create Scored Both Halves Home Stats
                    home_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    home_sbh_stats.team = home_team
                    home_sbh_stats.home_matches_played = home_matches_played
                    home_sbh_stats.home_scored_both_halves = home_scored_both_halves
                    home_sbh_stats.home_scored_both_halves_percent = home_scored_both_halves_percent

                    # Check if home stats already exists before saving or updating
                    if not home_sbh_stats.exists():
                        home_sbh_stats.save()
                        self.log_info(f"Team {home_team.name} Scored Both Halves Stats created in database")
                    else:
                        home_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=home_team)
                        home_sbh_stats.home_matches_played = home_matches_played
                        home_sbh_stats.home_scored_both_halves = home_scored_both_halves
                        home_sbh_stats.home_scored_both_halves_percent = home_scored_both_halves_percent
                        home_sbh_stats.save()
                        self.log_info(f"Team {home_team.name} Scored Both Halves Stats updated in database")

                    # Create Scored Both Halves Away Stats
                    away_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    away_sbh_stats.team = away_team
                    away_sbh_stats.away_matches_played = away_matches_played
                    away_sbh_stats.away_scored_both_halves = away_scored_both_halves
                    away_sbh_stats.away_scored_both_halves_percent = away_scored_both_halves_percent

                    # Check if away stats already exists before saving or updating
                    if not away_sbh_stats.exists():
                        away_sbh_stats.save()
                        self.log_info(f"Team {away_team.name} Scored Both Halves Stats created in database")
                    else:
                        away_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=away_team)
                        away_sbh_stats.away_matches_played = away_matches_played
                        away_sbh_stats.away_scored_both_halves = away_scored_both_halves
                        away_sbh_stats.away_scored_both_halves_percent = away_scored_both_halves_percent
                        away_sbh_stats.save()
                        self.log_info(f"Team {away_team.name} Scored Both Halves Stats updated in database")

                    # Create Scored Both Halves Overall Stats
                    overall_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    overall_sbh_stats.team = overall_team
                    overall_sbh_stats.overall_matches_played = overall_matches_played
                    overall_sbh_stats.overall_scored_both_halves = overall_scored_both_halves
                    overall_sbh_stats.overall_scored_both_halves_percent = overall_scored_both_halves_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_sbh_stats.exists():
                        overall_sbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored Both Halves Stats created in database")
                    else:
                        overall_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=overall_team)
                        overall_sbh_stats.overall_matches_played = overall_matches_played
                        overall_sbh_stats.overall_scored_both_halves = overall_scored_both_halves
                        overall_sbh_stats.overall_scored_both_halves_percent = overall_scored_both_halves_percent
                        overall_sbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored Both Halves Stats updated in database")

                ######################################### Conceded Both Halves ###########################################
                # Get Url
                self.get(url=iframe.conceded_both_half_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Conceded Both Halves Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_conceded_both_halves: int = int(table_tr.find_all('td')[3].text)
                        home_conceded_both_halves_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_conceded_both_halves: int = int(table_tr.find_all('td')[8].text)
                        away_conceded_both_halves_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_conceded_both_halves: int = int(table_tr.find_all('td')[13].text)
                        overall_conceded_both_halves_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create Conceded Both Halves Home Stats
                    home_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    home_sbh_stats.team = home_team
                    home_sbh_stats.home_matches_played = home_matches_played
                    home_sbh_stats.home_conceded_both_halves = home_conceded_both_halves
                    home_sbh_stats.home_conceded_both_halves_percent = home_conceded_both_halves_percent

                    # Check if home stats already exists before saving or updating
                    if not home_sbh_stats.exists():
                        home_sbh_stats.save()
                        self.log_info(f"Team {home_team.name} Scored Both Halves Stats created in database")
                    else:
                        home_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=home_team)
                        home_sbh_stats.home_matches_played = home_matches_played
                        home_sbh_stats.home_conceded_both_halves = home_conceded_both_halves
                        home_sbh_stats.home_conceded_both_halves_percent = home_conceded_both_halves_percent
                        home_sbh_stats.save()
                        self.log_info(f"Team {home_team.name} Scored Both Halves Stats updated in database")

                    # Create Scored Both Halves Away Stats
                    away_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    away_sbh_stats.team = away_team
                    away_sbh_stats.away_matches_played = away_matches_played
                    away_sbh_stats.away_conceded_both_halves = away_conceded_both_halves
                    away_sbh_stats.away_conceded_both_halves_percent = away_conceded_both_halves_percent

                    # Check if away stats already exists before saving or updating
                    if not away_sbh_stats.exists():
                        away_sbh_stats.save()
                        self.log_info(f"Team {away_team.name} Scored Both Halves Stats created in database")
                    else:
                        away_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=away_team)
                        away_sbh_stats.away_matches_played = away_matches_played
                        away_sbh_stats.away_conceded_both_halves = away_conceded_both_halves
                        away_sbh_stats.away_conceded_both_halves_percent = away_conceded_both_halves_percent
                        away_sbh_stats.save()
                        self.log_info(f"Team {away_team.name} Scored Both Halves Stats updated in database")

                    # Create Scored Both Halves Overall Stats
                    overall_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats()
                    overall_sbh_stats.team = overall_team
                    overall_sbh_stats.overall_matches_played = overall_matches_played
                    overall_sbh_stats.overall_conceded_both_halves = overall_conceded_both_halves
                    overall_sbh_stats.overall_conceded_both_halves_percent = overall_conceded_both_halves_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_sbh_stats.exists():
                        overall_sbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored Both Halves Stats created in database")
                    else:
                        overall_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=overall_team)
                        overall_sbh_stats.overall_matches_played = overall_matches_played
                        overall_sbh_stats.overall_conceded_both_halves = overall_conceded_both_halves
                        overall_sbh_stats.overall_conceded_both_halves_percent = overall_conceded_both_halves_percent
                        overall_sbh_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored Both Halves Stats updated in database")
