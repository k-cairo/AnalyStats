import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5CardsIframes, E5Team, E5CardsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetCards(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCards"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    CARDS_IFRAMES: ClassVar[QuerySet[E5CardsIframes]] = E5CardsIframes.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.CARDS_IFRAMES:
                iframe: E5CardsIframes  # Type hinting for Intellij

                ########################################## Yellow Cards For ############################################
                # Get Url
                self.get(url=iframe.yellow_cards_for_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Yellow Cards For Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_yellow_cards_for: int = 0
                    home_yellow_cards_for_average: float = 0.0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_yellow_cards_for: int = 0
                    away_yellow_cards_for_average: float = 0.0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_yellow_cards_for: int = 0
                    overall_yellow_cards_for_average: float = 0.0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_yellow_cards_for: int = int(table_tr.find_all('td')[3].text)
                        home_yellow_cards_for_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_yellow_cards_for: int = int(table_tr.find_all('td')[8].text)
                        away_yellow_cards_for_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_yellow_cards_for: int = int(table_tr.find_all('td')[13].text)
                        overall_yellow_cards_for_average: float = float(table_tr.find_all('td')[14].text)
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

                    # Create Yellow Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_yellow_cards_for = home_yellow_cards_for
                    home_card_stats.home_yellow_cards_for_average = home_yellow_cards_for_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} created")
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_yellow_cards_for = home_yellow_cards_for
                        target_home_card_stats.home_yellow_cards_for_average = home_yellow_cards_for_average
                        target_home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} updated")

                    # Create Yellow Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_yellow_cards_for = away_yellow_cards_for
                    away_card_stats.away_yellow_cards_for_average = away_yellow_cards_for_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} created")
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_yellow_cards_for = away_yellow_cards_for
                        target_away_card_stats.away_yellow_cards_for_average = away_yellow_cards_for_average
                        target_away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} updated")

                    # Create Yellow Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_yellow_cards_for = overall_yellow_cards_for
                    overall_card_stats.overall_yellow_cards_for_average = overall_yellow_cards_for_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} created")
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_yellow_cards_for = overall_yellow_cards_for
                        target_overall_card_stats.overall_yellow_cards_for_average = overall_yellow_cards_for_average
                        target_overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} updated")

                ######################################## Yellow Cards Against ##########################################
                # Get Url
                self.get(url=iframe.yellow_cards_against_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Yellow Cards Against Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_yellow_cards_against: int = 0
                    home_yellow_cards_against_average: float = 0.0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_yellow_cards_against: int = 0
                    away_yellow_cards_against_average: float = 0.0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_yellow_cards_against: int = 0
                    overall_yellow_cards_against_average: float = 0.0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_yellow_cards_against: int = int(table_tr.find_all('td')[3].text)
                        home_yellow_cards_against_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_yellow_cards_against: int = int(table_tr.find_all('td')[8].text)
                        away_yellow_cards_against_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_yellow_cards_against: int = int(table_tr.find_all('td')[13].text)
                        overall_yellow_cards_against_average: float = float(table_tr.find_all('td')[14].text)
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

                    # Create Yellow Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_yellow_cards_against = home_yellow_cards_against
                    home_card_stats.home_yellow_cards_against_average = home_yellow_cards_against_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} created")
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_yellow_cards_against = home_yellow_cards_against
                        target_home_card_stats.home_yellow_cards_against_average = home_yellow_cards_against_average
                        target_home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} updated")

                    # Create Yellow Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_yellow_cards_against = away_yellow_cards_against
                    away_card_stats.away_yellow_cards_against_average = away_yellow_cards_against_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} created")
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_yellow_cards_against = away_yellow_cards_against
                        target_away_card_stats.away_yellow_cards_against_average = away_yellow_cards_against_average
                        target_away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} updated")

                    # Create Yellow Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_yellow_cards_against = overall_yellow_cards_against
                    overall_card_stats.overall_yellow_cards_against_average = overall_yellow_cards_against_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} created")
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_yellow_cards_against = overall_yellow_cards_against
                        target_overall_card_stats.overall_yellow_cards_against_average = (
                            overall_yellow_cards_against_average)
                        target_overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} updated")

                ############################################ Red Cards For #############################################
                # Get Url
                self.get(url=iframe.red_cards_for_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Red Cards For Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_red_cards_for: int = 0
                    home_red_cards_for_average: float = 0.0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_red_cards_for: int = 0
                    away_red_cards_for_average: float = 0.0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_red_cards_for: int = 0
                    overall_red_cards_for_average: float = 0.0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_red_cards_for: int = int(table_tr.find_all('td')[3].text)
                        home_red_cards_for_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_red_cards_for: int = int(table_tr.find_all('td')[8].text)
                        away_red_cards_for_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_red_cards_for: int = int(table_tr.find_all('td')[13].text)
                        overall_red_cards_for_average: float = float(table_tr.find_all('td')[14].text)
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

                    # Create Red Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_red_cards_for = home_red_cards_for
                    home_card_stats.home_red_cards_for_average = home_red_cards_for_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} created")
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_red_cards_for = home_red_cards_for
                        target_home_card_stats.home_red_cards_for_average = home_red_cards_for_average
                        target_home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} updated")

                    # Create Red Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = away_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_red_cards_for = away_red_cards_for
                    away_card_stats.away_red_cards_for_average = away_red_cards_for_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} created")
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_red_cards_for = away_red_cards_for
                        target_away_card_stats.away_red_cards_for_average = away_red_cards_for_average
                        target_away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} updated")

                    # Create Red Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = overall_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_red_cards_for = overall_red_cards_for
                    overall_card_stats.overall_red_cards_for_average = overall_red_cards_for_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} created")
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_red_cards_for = overall_red_cards_for
                        target_overall_card_stats.overall_red_cards_for_average = overall_red_cards_for_average
                        target_overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} updated")

                ########################################## Red Cards Against ###########################################
                # Get Url
                self.get(url=iframe.red_cards_against_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = []
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Red Cards Against Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    home_team_name: str = ""
                    home_matches_played: int = 0
                    home_red_cards_against: int = 0
                    home_red_cards_against_average: float = 0.0
                    away_team_name: str = ""
                    away_matches_played: int = 0
                    away_red_cards_against: int = 0
                    away_red_cards_against_average: float = 0.0
                    overall_team_name: str = ""
                    overall_matches_played: int = 0
                    overall_red_cards_against: int = 0
                    overall_red_cards_against_average: float = 0.0
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_red_cards_against: int = int(table_tr.find_all('td')[3].text)
                        home_red_cards_against_average: float = float(table_tr.find_all('td')[4].text)
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_red_cards_against: int = int(table_tr.find_all('td')[8].text)
                        away_red_cards_against_average: float = float(table_tr.find_all('td')[9].text)
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_red_cards_against: int = int(table_tr.find_all('td')[13].text)
                        overall_red_cards_against_average: float = float(table_tr.find_all('td')[14].text)
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

                    # Create Red Card Home Stats
                    home_card_stats: E5CardsStats = E5CardsStats()
                    home_card_stats.team = home_team
                    home_card_stats.home_matches_played = home_matches_played
                    home_card_stats.home_red_cards_against = home_red_cards_against
                    home_card_stats.home_red_cards_against_average = home_red_cards_against_average

                    # Check if home stats already exists before saving or updating
                    if not home_card_stats.exists():
                        home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} created")
                    else:
                        target_home_card_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
                        target_home_card_stats.home_matches_played = home_matches_played
                        target_home_card_stats.home_red_cards_against = home_red_cards_against
                        target_home_card_stats.home_red_cards_against_average = home_red_cards_against_average
                        target_home_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {home_team.name} updated")

                    # Create Red Card Away Stats
                    away_card_stats: E5CardsStats = E5CardsStats()
                    away_card_stats.team = home_team
                    away_card_stats.away_matches_played = away_matches_played
                    away_card_stats.away_red_cards_against = away_red_cards_against
                    away_card_stats.away_red_cards_against_average = away_red_cards_against_average

                    # Check if away stats already exists before saving or updating
                    if not away_card_stats.exists():
                        away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} created")
                    else:
                        target_away_card_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)
                        target_away_card_stats.away_matches_played = away_matches_played
                        target_away_card_stats.away_red_cards_against = away_red_cards_against
                        target_away_card_stats.away_red_cards_against_average = away_red_cards_against_average
                        target_away_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {away_team.name} updated")

                    # Create Red Card Overall Stats
                    overall_card_stats: E5CardsStats = E5CardsStats()
                    overall_card_stats.team = home_team
                    overall_card_stats.overall_matches_played = overall_matches_played
                    overall_card_stats.overall_red_cards_against = overall_red_cards_against
                    overall_card_stats.overall_red_cards_against_average = overall_red_cards_against_average

                    # Check if overall stats already exists before saving or updating
                    if not overall_card_stats.exists():
                        overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} created")
                    else:
                        target_overall_card_stats: E5CardsStats = E5CardsStats.objects.get(team=overall_team)
                        target_overall_card_stats.overall_matches_played = overall_matches_played
                        target_overall_card_stats.overall_red_cards_against = overall_red_cards_against
                        target_overall_card_stats.overall_red_cards_against_average = overall_red_cards_against_average
                        target_overall_card_stats.save()
                        self.log_info(message=f"Parse Cards Stats : {overall_team.name} updated")
