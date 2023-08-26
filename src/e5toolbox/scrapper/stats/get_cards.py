import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5CardsIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetCards(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCards"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}cards/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Soup
                self.get_soup(error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Iframes
                cards_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check iframes length
                if len(cards_iframes) != 4:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get Iframe
                iframe: E5CardsIframes = E5CardsIframes()
                iframe.season = season
                for idx, card_iframe in enumerate(cards_iframes):
                    try:
                        iframe_url: str = card_iframe['src']
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                        continue

                    if idx == 0:
                        iframe.yellow_cards_for_url = iframe_url
                    elif idx == 1:
                        iframe.yellow_cards_against_url = iframe_url
                    elif idx == 2:
                        iframe.red_cards_for_url = iframe_url
                    elif idx == 3:
                        iframe.red_cards_against_url = iframe_url

                # Check iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} Cards Iframe created in database")
                else:
                    target_iframe: E5CardsIframes = E5CardsIframes.objects.get(season=season)
                    target_iframe.yellow_cards_for_url = iframe.yellow_cards_for_url
                    target_iframe.yellow_cards_against_url = iframe.yellow_cards_against_url
                    target_iframe.red_cards_for_url = iframe.red_cards_for_url
                    target_iframe.red_cards_against_url = iframe.red_cards_against_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} Cards Iframe updated in database")
