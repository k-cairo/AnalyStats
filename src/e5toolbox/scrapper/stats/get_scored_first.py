import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5ScoredFirstIframe, E5Team, E5ScoredFirstStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetScoredFirst(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetScoredFirst"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    SF_IFRAMES: ClassVar[QuerySet[E5ScoredFirstIframe]] = E5ScoredFirstIframe.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.SF_IFRAMES:
                iframe: E5ScoredFirstIframe  # Type hinting for Intellij

                ######################################### Scored First ###########################################
                # Get Url
                self.get(url=iframe.scored_first_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                        home_scored_first: int = int(table_tr.find_all('td')[3].text)
                        home_scored_first_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_scored_first: int = int(table_tr.find_all('td')[8].text)
                        away_scored_first_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_scored_first: int = int(table_tr.find_all('td')[13].text)
                        overall_scored_first_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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
                    home_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    home_sf_stats.team = home_team
                    home_sf_stats.home_matches_played = home_matches_played
                    home_sf_stats.home_scored_first = home_scored_first
                    home_sf_stats.home_scored_first_percent = home_scored_first_percent

                    # Check if home stats already exists before saving or updating
                    if not home_sf_stats.exists():
                        home_sf_stats.save()
                        self.log_info(f"Team {home_team.name} Scored First Stats created in database")
                    else:
                        home_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=home_team)
                        home_sf_stats.home_matches_played = home_matches_played
                        home_sf_stats.home_scored_first = home_scored_first
                        home_sf_stats.home_scored_first_percent = home_scored_first_percent
                        home_sf_stats.save()
                        self.log_info(f"Team {home_team.name} Scored First Stats updated in database")

                    # Create Won Both Halves Away Stats
                    away_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    away_sf_stats.team = away_team
                    away_sf_stats.away_matches_played = away_matches_played
                    away_sf_stats.away_scored_first = away_scored_first
                    away_sf_stats.away_scored_first_percent = away_scored_first_percent

                    # Check if away stats already exists before saving or updating
                    if not away_sf_stats.exists():
                        away_sf_stats.save()
                        self.log_info(f"Team {away_team.name} Scored First Stats created in database")
                    else:
                        away_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=away_team)
                        away_sf_stats.away_matches_played = away_matches_played
                        away_sf_stats.away_scored_first = away_scored_first
                        away_sf_stats.away_scored_first_percent = away_scored_first_percent
                        away_sf_stats.save()
                        self.log_info(f"Team {away_team.name} Scored First Stats updated in database")

                    # Create Won Both Halves Overall Stats
                    overall_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    overall_sf_stats.team = overall_team
                    overall_sf_stats.overall_matches_played = overall_matches_played
                    overall_sf_stats.overall_scored_first = overall_scored_first
                    overall_sf_stats.overall_scored_first_percent = overall_scored_first_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_sf_stats.exists():
                        overall_sf_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored First Stats created in database")
                    else:
                        overall_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=overall_team)
                        overall_sf_stats.overall_matches_played = overall_matches_played
                        overall_sf_stats.overall_scored_first = overall_scored_first
                        overall_sf_stats.overall_scored_first_percent = overall_scored_first_percent
                        overall_sf_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored First Stats updated in database")

                ########################################### Conceded First #############################################
                # Get Url
                self.get(url=iframe.conceded_first_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
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
                        home_conceded_first: int = int(table_tr.find_all('td')[3].text)
                        home_conceded_first_percent: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_conceded_first: int = int(table_tr.find_all('td')[8].text)
                        away_conceded_first_percent: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_conceded_first: int = int(table_tr.find_all('td')[13].text)
                        overall_conceded_first_percent: int = int(table_tr.find_all('td')[14].text.strip('%'))
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
                    home_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    home_sf_stats.team = home_team
                    home_sf_stats.home_matches_played = home_matches_played
                    home_sf_stats.home_conceded_first = home_conceded_first
                    home_sf_stats.home_conceded_first_percent = home_conceded_first_percent

                    # Check if home stats already exists before saving or updating
                    if not home_sf_stats.exists():
                        home_sf_stats.save()
                        self.log_info(f"Team {home_team.name} Scored First Stats created in database")
                    else:
                        home_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=home_team)
                        home_sf_stats.home_matches_played = home_matches_played
                        home_sf_stats.home_conceded_first = home_conceded_first
                        home_sf_stats.home_conceded_first_percent = home_conceded_first_percent
                        home_sf_stats.save()
                        self.log_info(f"Team {home_team.name} Scored First Stats updated in database")

                    # Create Won Both Halves Away Stats
                    away_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    away_sf_stats.team = away_team
                    away_sf_stats.away_matches_played = away_matches_played
                    away_sf_stats.away_conceded_first = away_conceded_first
                    away_sf_stats.away_conceded_first_percent = away_conceded_first_percent

                    # Check if away stats already exists before saving or updating
                    if not away_sf_stats.exists():
                        away_sf_stats.save()
                        self.log_info(f"Team {away_team.name} Scored First Stats created in database")
                    else:
                        away_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=away_team)
                        away_sf_stats.away_matches_played = away_matches_played
                        away_sf_stats.away_conceded_first = away_conceded_first
                        away_sf_stats.away_conceded_first_percent = away_conceded_first_percent
                        away_sf_stats.save()
                        self.log_info(f"Team {away_team.name} Scored First Stats updated in database")

                    # Create Won Both Halves Overall Stats
                    overall_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats()
                    overall_sf_stats.team = overall_team
                    overall_sf_stats.overall_matches_played = overall_matches_played
                    overall_sf_stats.overall_conceded_first = overall_conceded_first
                    overall_sf_stats.overall_conceded_first_percent = overall_conceded_first_percent

                    # Check if overall stats already exists before saving or updating
                    if not overall_sf_stats.exists():
                        overall_sf_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored First Stats created in database")
                    else:
                        overall_sf_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=overall_team)
                        overall_sf_stats.overall_matches_played = overall_matches_played
                        overall_sf_stats.overall_conceded_first = overall_conceded_first
                        overall_sf_stats.overall_conceded_first_percent = overall_conceded_first_percent
                        overall_sf_stats.save()
                        self.log_info(f"Team {overall_team.name} Scored First Stats updated in database")
