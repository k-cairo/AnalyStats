import dataclasses
from typing import ClassVar

from bs4 import Tag, ResultSet
from django.db.models import QuerySet

from Website.models import E5Season, E5BttsIframes, E5Team, E5BttsStats
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetBTTS(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetBtts"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    BTTS_IFRAMES: ClassVar[QuerySet[E5BttsIframes]] = E5BttsIframes.objects.filter(season__active=True)

    # E5
    def parse_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for iframe in self.BTTS_IFRAMES:
                iframe: E5BttsIframes  # Type hinting for Intellij

                ################################################ BTTS ##################################################
                # Get Url
                self.get(url=iframe.btts_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs: ResultSet[Tag] = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get Btts Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_team_url: str = table_tr.select(selector='td a[target="_blank"]')[0]['href']
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_btts: int = int(table_tr.find_all('td')[3].text)
                        home_btts_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_team_url: str = table_tr.select(selector='td a[target="_blank"]')[1]['href']
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_btts: int = int(table_tr.find_all('td')[8].text)
                        away_btts_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_team_url: str = table_tr.select(selector='td a[target="_blank"]')[2]['href']
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_btts: int = int(table_tr.find_all('td')[13].text)
                        overall_btts_percentage: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create BTTS Home Stats
                    home_btts_stats: E5BttsStats = E5BttsStats()
                    home_btts_stats.team = home_team
                    home_btts_stats.home_matches_played = home_matches_played
                    home_btts_stats.home_btts = home_btts
                    home_btts_stats.home_btts_percent = home_btts_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_btts_stats.exists():
                        home_btts_stats.save()
                    else:
                        target_home_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
                        target_home_btts_stats.home_matches_played = home_matches_played
                        target_home_btts_stats.home_btts = home_btts
                        target_home_btts_stats.home_btts_percent = home_btts_percentage
                        target_home_btts_stats.save()

                    # Create BTTS Away Stats
                    away_btts_stats: E5BttsStats = E5BttsStats()
                    away_btts_stats.team = away_team
                    away_btts_stats.away_matches_played = away_matches_played
                    away_btts_stats.away_btts = away_btts
                    away_btts_stats.away_btts_percent = away_btts_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_btts_stats.exists():
                        away_btts_stats.save()
                    else:
                        target_away_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)
                        target_away_btts_stats.away_matches_played = away_matches_played
                        target_away_btts_stats.away_btts = away_btts
                        target_away_btts_stats.away_btts_percent = away_btts_percentage
                        target_away_btts_stats.save()

                    # Create BTTS Overall Stats
                    overall_btts_stats: E5BttsStats = E5BttsStats()
                    overall_btts_stats.team = overall_team
                    overall_btts_stats.overall_matches_played = overall_matches_played
                    overall_btts_stats.overall_btts = overall_btts
                    overall_btts_stats.overall_btts_percent = overall_btts_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_btts_stats.exists():
                        overall_btts_stats.save()
                    else:
                        target_overall_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=overall_team)
                        target_overall_btts_stats.overall_matches_played = overall_matches_played
                        target_overall_btts_stats.overall_btts = overall_btts
                        target_overall_btts_stats.overall_btts_percent = overall_btts_percentage
                        target_overall_btts_stats.save()

                ############################################### BTTS 1H ################################################
                # Get Url
                self.get(url=iframe.btts_1h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get BTTS 1H Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_team_url: str = table_tr.select(selector='td a[target="_blank"]')[0]['href']
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_btts_1h: int = int(table_tr.find_all('td')[3].text)
                        home_btts_1h_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_team_url: str = table_tr.select(selector='td a[target="_blank"]')[1]['href']
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_btts_1h: int = int(table_tr.find_all('td')[8].text)
                        away_btts_1h_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_team_url: str = table_tr.select(selector='td a[target="_blank"]')[2]['href']
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_btts_1h: int = int(table_tr.find_all('td')[13].text)
                        overall_btts_1h_percentage: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create BTTS 1H Home Stats
                    home_btts_stats: E5BttsStats = E5BttsStats()
                    home_btts_stats.team = home_team
                    home_btts_stats.home_matches_played = home_matches_played
                    home_btts_stats.home_btts_1h = home_btts_1h
                    home_btts_stats.home_btts_1h_percent = home_btts_1h_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_btts_stats.exists():
                        home_btts_stats.save()
                    else:
                        target_home_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
                        target_home_btts_stats.home_matches_played = home_matches_played
                        target_home_btts_stats.home_btts_1h = home_btts_1h
                        target_home_btts_stats.home_btts_1h_percent = home_btts_1h_percentage
                        target_home_btts_stats.save()

                    # Create BTTS 1H Away Stats
                    away_btts_stats: E5BttsStats = E5BttsStats()
                    away_btts_stats.team = away_team
                    away_btts_stats.away_matches_played = away_matches_played
                    away_btts_stats.away_btts_1h = away_btts_1h
                    away_btts_stats.away_btts_1h_percent = away_btts_1h_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_btts_stats.exists():
                        away_btts_stats.save()
                    else:
                        target_away_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)
                        target_away_btts_stats.away_matches_played = away_matches_played
                        target_away_btts_stats.away_btts_1h = away_btts_1h
                        target_away_btts_stats.away_btts_1h_percent = away_btts_1h_percentage
                        target_away_btts_stats.save()

                    # Create BTTS 1H Overall Stats
                    overall_btts_stats: E5BttsStats = E5BttsStats()
                    overall_btts_stats.team = overall_team
                    overall_btts_stats.overall_matches_played = overall_matches_played
                    overall_btts_stats.overall_btts_1h = overall_btts_1h
                    overall_btts_stats.overall_btts_1h_percent = overall_btts_1h_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_btts_stats.exists():
                        overall_btts_stats.save()
                    else:
                        target_overall_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=overall_team)
                        target_overall_btts_stats.overall_matches_played = overall_matches_played
                        target_overall_btts_stats.overall_btts_1h = overall_btts_1h
                        target_overall_btts_stats.overall_btts_1h_percent = overall_btts_1h_percentage
                        target_overall_btts_stats.save()

                ############################################### BTTS 2H ################################################
                # Get Url
                self.get(url=iframe.btts_2h_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get BTTS 2H Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_team_url: str = table_tr.select(selector='td a[target="_blank"]')[0]['href']
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_btts_2h: int = int(table_tr.find_all('td')[3].text)
                        home_btts_2h_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_team_url: str = table_tr.select(selector='td a[target="_blank"]')[1]['href']
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_btts_2h: int = int(table_tr.find_all('td')[8].text)
                        away_btts_2h_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_team_url: str = table_tr.select(selector='td a[target="_blank"]')[2]['href']
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_btts_2h: int = int(table_tr.find_all('td')[13].text)
                        overall_btts_2h_percentage: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create BTTS 2H Home Stats
                    home_btts_stats: E5BttsStats = E5BttsStats()
                    home_btts_stats.team = home_team
                    home_btts_stats.home_matches_played = home_matches_played
                    home_btts_stats.home_btts_2h = home_btts_2h
                    home_btts_stats.home_btts_2h_percent = home_btts_2h_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_btts_stats.exists():
                        home_btts_stats.save()
                    else:
                        target_home_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
                        target_home_btts_stats.home_matches_played = home_matches_played
                        target_home_btts_stats.home_btts_2h = home_btts_2h
                        target_home_btts_stats.home_btts_2h_percent = home_btts_2h_percentage
                        target_home_btts_stats.save()

                    # Create BTTS 2H Away Stats
                    away_btts_stats: E5BttsStats = E5BttsStats()
                    away_btts_stats.team = away_team
                    away_btts_stats.away_matches_played = away_matches_played
                    away_btts_stats.away_btts_2h = away_btts_2h
                    away_btts_stats.away_btts_2h_percent = away_btts_2h_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_btts_stats.exists():
                        away_btts_stats.save()
                    else:
                        target_away_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)
                        target_away_btts_stats.away_matches_played = away_matches_played
                        target_away_btts_stats.away_btts_2h = away_btts_2h
                        target_away_btts_stats.away_btts_2h_percent = away_btts_2h_percentage
                        target_away_btts_stats.save()

                    # Create BTTS 2H Overall Stats
                    overall_btts_stats: E5BttsStats = E5BttsStats()
                    overall_btts_stats.team = overall_team
                    overall_btts_stats.overall_matches_played = overall_matches_played
                    overall_btts_stats.overall_btts_2h = overall_btts_2h
                    overall_btts_stats.overall_btts_2h_percent = overall_btts_2h_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_btts_stats.exists():
                        overall_btts_stats.save()
                    else:
                        target_overall_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=overall_team)
                        target_overall_btts_stats.overall_matches_played = overall_matches_played
                        target_overall_btts_stats.overall_btts_2h = overall_btts_2h
                        target_overall_btts_stats.overall_btts_2h_percent = overall_btts_2h_percentage
                        target_overall_btts_stats.save()

                ############################################### BTTS BH ################################################
                # Get Url
                self.get(url=iframe.btts_bh_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get BTTS BH Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_team_url: str = table_tr.select(selector='td a[target="_blank"]')[0]['href']
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_btts_bh: int = int(table_tr.find_all('td')[3].text)
                        home_btts_bh_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_team_url: str = table_tr.select(selector='td a[target="_blank"]')[1]['href']
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_btts_bh: int = int(table_tr.find_all('td')[8].text)
                        away_btts_bh_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_team_url: str = table_tr.select(selector='td a[target="_blank"]')[2]['href']
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_btts_bh: int = int(table_tr.find_all('td')[13].text)
                        overall_btts_bh_percentage: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create BTTS BH Home Stats
                    home_btts_stats: E5BttsStats = E5BttsStats()
                    home_btts_stats.team = home_team
                    home_btts_stats.home_matches_played = home_matches_played
                    home_btts_stats.home_btts_bh = home_btts_bh
                    home_btts_stats.home_btts_bh_percent = home_btts_bh_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_btts_stats.exists():
                        home_btts_stats.save()
                    else:
                        target_home_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
                        target_home_btts_stats.home_matches_played = home_matches_played
                        target_home_btts_stats.home_btts_bh = home_btts_bh
                        target_home_btts_stats.home_btts_bh_percent = home_btts_bh_percentage
                        target_home_btts_stats.save()

                    # Create BTTS bh Away Stats
                    away_btts_stats: E5BttsStats = E5BttsStats()
                    away_btts_stats.team = away_team
                    away_btts_stats.away_matches_played = away_matches_played
                    away_btts_stats.away_btts_bh = away_btts_bh
                    away_btts_stats.away_btts_bh_percent = away_btts_bh_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_btts_stats.exists():
                        away_btts_stats.save()
                    else:
                        target_away_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)
                        target_away_btts_stats.away_matches_played = away_matches_played
                        target_away_btts_stats.away_btts_bh = away_btts_bh
                        target_away_btts_stats.away_btts_bh_percent = away_btts_bh_percentage
                        target_away_btts_stats.save()

                    # Create BTTS bh Overall Stats
                    overall_btts_stats: E5BttsStats = E5BttsStats()
                    overall_btts_stats.team = overall_team
                    overall_btts_stats.overall_matches_played = overall_matches_played
                    overall_btts_stats.overall_btts_bh = overall_btts_bh
                    overall_btts_stats.overall_btts_bh_percent = overall_btts_bh_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_btts_stats.exists():
                        overall_btts_stats.save()
                    else:
                        target_overall_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=overall_team)
                        target_overall_btts_stats.overall_matches_played = overall_matches_played
                        target_overall_btts_stats.overall_btts_bh = overall_btts_bh
                        target_overall_btts_stats.overall_btts_bh_percent = overall_btts_bh_percentage
                        target_overall_btts_stats.save()

                ############################################### BTTS 25 ################################################
                # Get Url
                self.get(url=iframe.btts_25_url, error_context=f"{self.ERROR_CONTEXT}.parse_iframes()")
                if not self.status.success:
                    self.init_status()
                    continue

                # Get Table Trs
                table_trs = self.soup.find('table', class_='waffle no-grid').find_all('tr')

                # Get BTTS 25 Stats
                for table_tr in table_trs:
                    table_tr: Tag  # Type hinting for Intellij
                    try:
                        home_team_name: str = table_tr.select(selector='td a[target="_blank"]')[0].text
                        home_team_url: str = table_tr.select(selector='td a[target="_blank"]')[0]['href']
                        home_matches_played: int = int(table_tr.find_all('td')[2].text)
                        home_btts_25: int = int(table_tr.find_all('td')[3].text)
                        home_btts_25_percentage: int = int(table_tr.find_all('td')[4].text.strip('%'))
                        away_team_name: str = table_tr.select(selector='td a[target="_blank"]')[1].text
                        away_team_url: str = table_tr.select(selector='td a[target="_blank"]')[1]['href']
                        away_matches_played: int = int(table_tr.find_all('td')[7].text)
                        away_btts_25: int = int(table_tr.find_all('td')[8].text)
                        away_btts_25_percentage: int = int(table_tr.find_all('td')[9].text.strip('%'))
                        overall_team_name: str = table_tr.select(selector='td a[target="_blank"]')[2].text
                        overall_team_url: str = table_tr.select(selector='td a[target="_blank"]')[2]['href']
                        overall_matches_played: int = int(table_tr.find_all('td')[12].text)
                        overall_btts_25: int = int(table_tr.find_all('td')[13].text)
                        overall_btts_25_percentage: int = int(table_tr.find_all('td')[14].text.strip('%'))
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

                    # Create BTTS 25 Home Stats
                    home_btts_stats: E5BttsStats = E5BttsStats()
                    home_btts_stats.team = home_team
                    home_btts_stats.home_matches_played = home_matches_played
                    home_btts_stats.home_btts_25 = home_btts_25
                    home_btts_stats.home_btts_25_percent = home_btts_25_percentage

                    # Check if home stats already exists before saving or updating
                    if not home_btts_stats.exists():
                        home_btts_stats.save()
                    else:
                        target_home_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
                        target_home_btts_stats.home_matches_played = home_matches_played
                        target_home_btts_stats.home_btts_25 = home_btts_25
                        target_home_btts_stats.home_btts_25_percent = home_btts_25_percentage
                        target_home_btts_stats.save()

                    # Create BTTS 25 Away Stats
                    away_btts_stats: E5BttsStats = E5BttsStats()
                    away_btts_stats.team = away_team
                    away_btts_stats.away_matches_played = away_matches_played
                    away_btts_stats.away_btts_25 = away_btts_25
                    away_btts_stats.away_btts_25_percent = away_btts_25_percentage

                    # Check if away stats already exists before saving or updating
                    if not away_btts_stats.exists():
                        away_btts_stats.save()
                    else:
                        target_away_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)
                        target_away_btts_stats.away_matches_played = away_matches_played
                        target_away_btts_stats.away_btts_25 = away_btts_25
                        target_away_btts_stats.away_btts_25_percent = away_btts_25_percentage
                        target_away_btts_stats.save()

                    # Create BTTS 25 Overall Stats
                    overall_btts_stats: E5BttsStats = E5BttsStats()
                    overall_btts_stats.team = overall_team
                    overall_btts_stats.overall_matches_played = overall_matches_played
                    overall_btts_stats.overall_btts_25 = overall_btts_25
                    overall_btts_stats.overall_btts_25_percent = overall_btts_25_percentage

                    # Check if overall stats already exists before saving or updating
                    if not overall_btts_stats.exists():
                        overall_btts_stats.save()
                    else:
                        target_overall_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=overall_team)
                        target_overall_btts_stats.overall_matches_played = overall_matches_played
                        target_overall_btts_stats.overall_btts_25 = overall_btts_25
                        target_overall_btts_stats.overall_btts_25_percent = overall_btts_25_percentage
                        target_overall_btts_stats.save()
