import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5Over25GoalsIframe
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetOver25Goals(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetOver25Goals"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}over-2-5-goals/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Soup
                self.get_soup(error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get BTTS Iframes
                over_25_goals_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check iframes length
                if len(over_25_goals_iframes) != 4:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get Overs 2.5 Goals Iframe
                iframe: E5Over25GoalsIframe = E5Over25GoalsIframe()
                iframe.season = season
                for idx, over_25_goals_iframe in enumerate(over_25_goals_iframes):
                    try:
                        iframe_url: str = over_25_goals_iframe['src']
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_ACTIVE_SEASON_OVER_25_GOALS_IFRAME_URL_FAILED,
                            error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                        continue

                    if idx == 0:
                        iframe.over_25_goals_url = iframe_url
                    elif idx == 1:
                        iframe.over_25_goals_1h_url = iframe_url
                    elif idx == 2:
                        iframe.over_25_goals_2h_url = iframe_url
                    elif idx == 3:
                        iframe.over_25_goals_bh_url = iframe_url

                # Check iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} Over 2.5 Goals Iframe created in database")
                else:
                    target_iframe: E5Over25GoalsIframe = E5Over25GoalsIframe.objects.get(season=season)
                    target_iframe.over_25_goals_url = iframe.over_25_goals_url
                    target_iframe.over_25_goals_1h_url = iframe.over_25_goals_1h_url
                    target_iframe.over_25_goals_2h_url = iframe.over_25_goals_2h_url
                    target_iframe.over_25_goals_bh_url = iframe.over_25_goals_bh_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} Over 2.5 Goals Iframe updated in database")
