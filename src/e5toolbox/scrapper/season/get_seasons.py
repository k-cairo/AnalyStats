import dataclasses
from typing import ClassVar

from bs4 import BeautifulSoup
from django.db.models import QuerySet

from Website.models import E5League, E5Season
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetSeasons(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetSeasons"
    LEAGUES: ClassVar[QuerySet[E5League]] = E5League.objects.all()

    # E5
    def get_active(self):
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for league in self.LEAGUES:
                league: E5League  # Type hinting for Intellij

                # Get Url
                try:
                    self.driver.get(league.url)
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                                   error_context=self.ERROR_CONTEXT, exception=ex)
                    continue

                # Get Soup
                try:
                    self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                                   error_context=self.ERROR_CONTEXT, exception=ex)
                    continue

                # Get Season Name and Url
                try:
                    season_details: str = self.soup.select(selector="div.textwidget.custom-html-widget p")[1].text
                except Exception as ex:
                    self.exception(
                        error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_NAME_OR_URL_FAILED,
                        error_context=self.ERROR_CONTEXT, exception=ex)
                    continue

                # Create Active Season
                active_season: E5Season = E5Season()
                active_season.name = season_details.split()[-1]
                active_season.league = league
                active_season.url = league.url
                active_season.active = True

                # Check if season already exists before saving or updating
                if not active_season.exists():
                    active_season.save()
                    self.log_info(f"League {active_season.league.name} Season {active_season.name} created in database")
                else:
                    target_active_season: E5Season = E5Season.objects.get(active=True, league=league,
                                                                          name=active_season.name)
                    target_active_season.url = league.url
                    target_active_season.save()
                    self.log_info(f"League {active_season.league.name} Season {active_season.name} updated in database")
