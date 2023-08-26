import dataclasses
from typing import ClassVar

from bs4 import Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5WinDrawLossPercentageIframe
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetWinDrawLossPercentage(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetWinDrawLossPercentage"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}wdl/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Iframes
                wdl_percent_iframe: Tag | None = self.soup.select_one(selector="div.fusion-text.fusion-text-2 iframe")

                # Check Iframes
                if wdl_percent_iframe is None:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_IFRAME_FAILED,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get Iframe Url
                try:
                    iframe_url: str = wdl_percent_iframe['src']
                except Exception as ex:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_CARD_IFRAME_URL_FAILED,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                    continue

                # Get Iframe
                iframe: E5WinDrawLossPercentageIframe = E5WinDrawLossPercentageIframe()
                iframe.season = season
                iframe.url = iframe_url

                # Check iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} Win Draw Loss Percentage Iframe created in database")
                else:
                    target_iframe: E5WinDrawLossPercentageIframe = E5WinDrawLossPercentageIframe.objects.get(
                        season=season)
                    target_iframe.url = iframe_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} Win Draw Loss Percentage Iframe updated in database")
