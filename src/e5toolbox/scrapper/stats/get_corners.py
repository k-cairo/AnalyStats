import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet

from Website.models import E5Season, E5CornersIframes
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetCorners(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetCorners"
    ACTIVE_SEASONS: ClassVar[QuerySet[E5Season]] = E5Season.objects.filter(active=True)

    # E5
    def get_iframes(self) -> None:
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for season in self.ACTIVE_SEASONS:
                season: E5Season  # Type hinting for Intellij

                # Get Url
                self.get(url=f"{season.url}corners/", error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Soup
                self.get_soup(error_context=f"{self.ERROR_CONTEXT}.get_iframes()")
                if not self.status.success:
                    continue

                # Get Iframes
                corners_iframes: ResultSet[Tag] = self.soup.select(selector="div.tab-content iframe")

                # Check iframes length
                if len(corners_iframes) != 9:
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAMES_BAD_LENGTH,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Get Iframe
                iframe: E5CornersIframes = E5CornersIframes()
                iframe.season = season
                for idx, corner_iframe in enumerate(corners_iframes):
                    try:
                        iframe_url: str = corner_iframe['src']
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_GET_CORNER_IFRAME_URL_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=ex)
                        continue

                    if idx == 0:
                        iframe.team_corners_for_1h_url = iframe_url
                    elif idx == 1:
                        iframe.team_corners_against_1h_url = iframe_url
                    elif idx == 2:
                        iframe.team_corners_for_2h_url = iframe_url
                    elif idx == 3:
                        iframe.team_corners_against_2h_url = iframe_url
                    elif idx == 4:
                        iframe.team_corners_for_ft_url = iframe_url
                    elif idx == 5:
                        iframe.team_corners_against_ft_url = iframe_url
                    elif idx == 6:
                        iframe.match_corners_1h_url = iframe_url
                    elif idx == 7:
                        iframe.match_corners_2h_url = iframe_url
                    elif idx == 8:
                        iframe.match_corners_ft_url = iframe_url

                # Check iframe not empty
                if not iframe.not_empty():
                    self.exception(error_type=E5SeleniumWebdriverError.ERROR_TYPE_IFRAME_EMPTY,
                                   error_context=f"{self.ERROR_CONTEXT}.get_iframes()", exception=None)
                    continue

                # Check if iframe already exists before saving or updating
                if not iframe.exists():
                    iframe.save()
                    self.log_info(f"League {season.league.name} Corners Iframe created in database")
                else:
                    target_iframe: E5CornersIframes = E5CornersIframes.objects.get(season=season)
                    target_iframe.team_corners_for_1h_url = iframe.team_corners_for_1h_url
                    target_iframe.team_corners_against_1h_url = iframe.team_corners_against_1h_url
                    target_iframe.team_corners_for_2h_url = iframe.team_corners_for_2h_url
                    target_iframe.team_corners_against_2h_url = iframe.team_corners_against_2h_url
                    target_iframe.team_corners_for_ft_url = iframe.team_corners_for_ft_url
                    target_iframe.team_corners_against_ft_url = iframe.team_corners_against_ft_url
                    target_iframe.match_corners_1h_url = iframe.match_corners_1h_url
                    target_iframe.match_corners_2h_url = iframe.match_corners_2h_url
                    target_iframe.match_corners_ft_url = iframe.match_corners_ft_url
                    target_iframe.save()
                    self.log_info(f"League {season.league.name} Corners Iframe updated in database")
