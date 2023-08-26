import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5BttsIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetBtts(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetBtts"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}btts/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get BTTS Iframe
                btts_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                if len(btts_iframes) != 5:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get BTTS Iframe
                iframe: E5BttsIframes = E5BttsIframes()
                iframe.season = season
                for idx, btts_iframe in enumerate(btts_iframes):
                    try:
                        iframe_url: str = btts_iframe['src']
                    except Exception as ex:
                        self.exception(
                            error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_IFRAME_URL_FAILED,
                            error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                        continue

                    if idx == 0:
                        iframe.btts_url = iframe_url
                    elif idx == 1:
                        iframe.btts_1h_url = iframe_url
                    elif idx == 2:
                        iframe.btts_2h_url = iframe_url
                    elif idx == 3:
                        iframe.btts_bh_url = iframe_url
                    elif idx == 4:
                        iframe.btts_25_url = iframe_url

                # Check btt_iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} BTTS Iframe created in database")
                else:
                    target_iframe: E5BttsIframes = E5BttsIframes.objects.get(season=season)
                    target_iframe.btts_url = iframe.btts_url
                    target_iframe.btts_1h_url = iframe.btts_1h_url
                    target_iframe.btts_2h_url = iframe.btts_2h_url
                    target_iframe.btts_bh_url = iframe.btts_bh_url
                    target_iframe.btts_25_url = iframe.btts_25_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} BTTS Iframe updated in database")
