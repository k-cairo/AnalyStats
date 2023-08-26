import dataclasses
from typing import ClassVar

from bs4 import ResultSet, Tag
from django.db.models import QuerySet
from django.utils.text import slugify

from Website.models import E5LeagueTableIframe, E5Team
from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver, E5SeleniumWebdriverError


# E5
@dataclasses.dataclass
class E5GetTeams(E5SeleniumWebDriver):
    ERROR_CONTEXT: ClassVar[str] = "E5GetTeams"
    ACTIVE_LEAGUE_TABLE_IFRAMES: ClassVar[QuerySet[E5LeagueTableIframe]] = E5LeagueTableIframe.objects.filter(
        season__active=True)

    # E5
    def get_active(self):
        # Check connection
        self.check_is_connected()

        if self.status.success:
            for league_table in self.ACTIVE_LEAGUE_TABLE_IFRAMES:
                league_table: E5LeagueTableIframe  # Type hinting for Intellij

                # Get Url
                self.get(url=league_table.url, error_context=f"{self.ERROR_CONTEXT}.get_active()")
                if not self.status.success:
                    continue

                # Get Soup
                self.get_soup(error_context=f"{self.ERROR_CONTEXT}.get_active()")
                if not self.status.success:
                    continue

                # Get Teams
                teams_a: ResultSet[Tag] = self.soup.select(selector="table.waffle.no-grid tr td a[target='_blank']")

                # Get Team
                for team_a in teams_a:
                    try:
                        team_name: str = team_a.text
                        team_url: str = team_a['href']
                    except Exception as ex:
                        self.exception(error_type=E5SeleniumWebdriverError.
                                       ERROR_TYPE_GET_ACTIVE_SEASON_TEAM_NAME_OR_TEAM_URL_FAILED,
                                       error_context=f"{self.ERROR_CONTEXT}.get_active", exception=ex)
                        continue

                    # Create Team
                    if team_name != "" and team_url != "":
                        team: E5Team = E5Team()
                        team.name = team_name
                        team.url = team_url
                        team.slug = slugify(value=team_name)
                        team.season = league_table.season

                        # Check if active season team already exists before saving or updating
                        if not team.exists():
                            team.save()
                            self.log_info(f"Team {team.name} created in database")
                        else:
                            target_team: E5Team = E5Team.objects.get(name=team_name, season=league_table.season)
                            target_team.url = team_url
                            target_team.slug = slugify(value=team_name)
                            target_team.save()
                            self.log_info(f"Team {team.name} updated in database")
