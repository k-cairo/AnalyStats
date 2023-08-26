import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag, BeautifulSoup
from django.db.models import QuerySet
from django.utils.text import slugify

from Website.models import E5League, E5Season
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetLeagues(E5SeleniumWebDriver):
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)
    ERROR_CONTEXT: ClassVar[str] = "E5GetLeagues"

    # E5
    def get(self):
        # Check connection
        self.check_is_connected()

        # Get Url
        if self.status.success:
            try:
                self.driver.get("https://www.thestatsdontlie.com/football/leagues/")
            except Exception as ex:
                self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_URL_FAILED,
                               error_context=f"{self.ERROR_CONTEXT}.get_leagues()", exception=ex)

        # Get Soup
        if self.status.success:
            try:
                self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            except Exception as ex:
                self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_SOUP_FAILED,
                               error_context=f"{self.ERROR_CONTEXT}.get_leagues()", exception=ex)

        # Get Leagues Web Element
        if self.status.success and self.soup is not None:
            selector: str = "div.fusion-column-wrapper.fusion-flex-column-wrapper-legacy a"
            leagues: ResultSet[Tag] = self.soup.select(selector=selector)

            # Get Leagues
            for league in leagues:
                # Get League Name and Url
                try:
                    league_name: str = league.text
                    league_url: str = league['href']
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_LEAGUE_NAME_OR_URL_FAILED,
                                   error_context=f"{self.ERROR_CONTEXT}.get_leagues()", exception=ex)
                    continue

                # Create League
                new_league: E5League = E5League()
                new_league.name = league_name
                new_league.url = league_url
                new_league.slug = slugify(value=league_name)

                if ("Colombia" in league_name or "Costa Rica" in league_name or "Ecuador" in league_name
                        or "Honduras" in league_name or "Mexico" in league_name or "Paraguay" in league_name
                        or "Peru" in league_name or "Tunisia" in league_name or "Uruguay" in league_name):
                    continue

                # Check if league already exists
                if new_league.exists():
                    # Update League
                    target_league: E5League = E5League.objects.get(name=league_name)
                    target_league.url = league_url
                    target_league.slug = slugify(value=league_name)
                    target_league.save()
                    self.log_info(message=f"League {league_name} updated in database")
                else:
                    # Save League
                    new_league.save()
                    self.log_info(message=f"League {league_name} created in database")
