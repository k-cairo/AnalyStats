import datetime

from django.db.models import QuerySet
from django.shortcuts import render

from .models import (E5League, E5Season, E5TeamRanking, E5Over05GoalsStats, E5Over15GoalsStats, E5Over25GoalsStats,
                     E5Over35GoalsStats, E5TeamCornerStats, E5MatchCornerStats, E5CardsStats, E5Team, E5BttsStats,
                     E5WinDrawLossPercentageStats, E5HalfTimeFullTimeStats, E5ScoredBothHalfStats, E5WonBothHalfStats,
                     E51st2ndHalfGoalsStats, E5RescuedPointsStats, E5CleanSheetStats, E5WonToNilStats,
                     E5WinLossMarginStats, E5ScoredFirstStats, E5Average1stGoalTimeStats, E5AverageTeamGoalsStats,
                     E5EarlyGoalsStats, E5LateGoalsStats, E5Fixture)


######################################################### INDEX ########################################################
# E5
def index(request):
    # Query Active Teams
    total_teams: int = E5Team.objects.filter(season__active=True).count()

    # Query Active Seasons
    seasons: QuerySet(E5Season) = E5Season.objects.filter(active=True).distinct()
    total_leagues = len(seasons)

    # Context
    context = {'total_leagues': total_leagues, 'total_teams': total_teams}

    # Render
    return render(request=request, template_name='Website/index.html', context=context)


######################################################## LEAGUES #######################################################
# E5
def leagues(request):
    # Query Active Seasons
    seasons: QuerySet(E5Season) = E5Season.objects.filter(active=True).distinct().order_by('league__name')

    # Get Active Leagues
    leagues: [E5League] = [season.league for season in seasons]

    # Context
    context = {'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/leagues.html', context=context)


######################################################### TEAMS ########################################################
# E5
def teams(request):
    # Query Teams
    teams: QuerySet(E5Team) = E5Team.objects.distinct().order_by('name')

    # Context
    context = {'teams': teams}

    # Render
    return render(request=request, template_name='Website/teams.html', context=context)


# E5
def team_details(request, league_slug: str, team_slug: str):
    # Query Team
    team: E5Team = E5Team.objects.get(slug=team_slug, season__league__slug=league_slug)

    # Query Team Over 0.5 Goals Stats
    over_05_goals_stats: QuerySet(E5Over05GoalsStats) = E5Over05GoalsStats.objects.get(team=team)

    # Query Team Over 1.5 Goals Stats
    over_15_goals_stats: QuerySet(E5Over15GoalsStats) = E5Over15GoalsStats.objects.get(team=team)

    # Query Team Over 2.5 Goals Stats
    over_25_goals_stats: QuerySet(E5Over25GoalsStats) = E5Over25GoalsStats.objects.get(team=team)

    # Query Team Over 3.5 Goals Stats
    over_35_goals_stats: QuerySet(E5Over35GoalsStats) = E5Over35GoalsStats.objects.get(team=team)

    # Query Team Cards Stats
    cards_stats: QuerySet(E5CardsStats) = E5CardsStats.objects.get(team=team)

    # Context
    context = {'team': team, 'over_05_goals_stats': over_05_goals_stats, 'over_15_goals_stats': over_15_goals_stats,
               'over_25_goals_stats': over_25_goals_stats, 'over_35_goals_stats': over_35_goals_stats,
               'cards_stats': cards_stats}
    print(context)

    # Render
    return render(request=request, template_name='Website/team_details.html', context=context)


######################################################## FIXTURES ######################################################
# E5
def fixtures(request):
    # Query Fixtures
    fixtures: QuerySet(E5Fixture) = E5Fixture.objects.filter(date__gte=datetime.date.today())

    # Get fixtures distinct dates & leagues
    leagues: dict[datetime.date: list[E5League]] = {}
    dates: [datetime.date] = []
    for fixture in fixtures:
        # Get distinct leagues for each date
        if fixture.date not in leagues:
            leagues[fixture.date] = []
        if fixture.home_team.season.league not in leagues[fixture.date]:
            leagues[fixture.date].append(fixture.home_team.season.league)
        # Get fixtures distinct dates
        if fixture.date not in dates:
            dates.append(fixture.date)

    dates.sort()

    # Context
    context = {'fixtures': fixtures, "dates": dates, "leagues": leagues}

    # Render
    return render(request=request, template_name='Website/fixtures.html', context=context)


# E5
def fixture_details(request, fixture_slug: str):
    # Query Fixture
    fixture: E5Fixture = E5Fixture.objects.get(slug=fixture_slug)

    # Teams
    home_team: E5Team = fixture.home_team
    away_team: E5Team = fixture.away_team

    # Query BTTS Stats
    ht_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=home_team)
    at_btts_stats: E5BttsStats = E5BttsStats.objects.get(team=away_team)

    # Query Over 0.5 Goals Stats
    ht_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(team=home_team)
    at_over_05_goals_stats: E5Over05GoalsStats = E5Over05GoalsStats.objects.get(team=away_team)

    # Query Over 1.5 Goals Stats
    ht_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(team=home_team)
    at_over_15_goals_stats: E5Over15GoalsStats = E5Over15GoalsStats.objects.get(team=away_team)

    # Query Over 2.5 Goals Stats
    ht_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(team=home_team)
    at_over_25_goals_stats: E5Over25GoalsStats = E5Over25GoalsStats.objects.get(team=away_team)

    # Query Over 3.5 Goals Stats
    ht_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(team=home_team)
    at_over_35_goals_stats: E5Over35GoalsStats = E5Over35GoalsStats.objects.get(team=away_team)

    # Query Win Draw Loss Percentage Stats
    ht_wdl_percent_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats.objects.get(team=home_team)
    at_wdl_percent_stats: E5WinDrawLossPercentageStats = E5WinDrawLossPercentageStats.objects.get(team=away_team)

    # Query Cards Stats
    ht_cards_stats: E5CardsStats = E5CardsStats.objects.get(team=home_team)
    at_cards_stats: E5CardsStats = E5CardsStats.objects.get(team=away_team)

    # Query Team Corner Stats
    ht_team_corners_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=home_team)
    at_team_corners_stats: E5TeamCornerStats = E5TeamCornerStats.objects.get(team=away_team)

    # Query Match Corner Stats
    ht_match_corners_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(team=home_team)
    at_match_corners_stats: E5MatchCornerStats = E5MatchCornerStats.objects.get(team=away_team)

    # Query Half Time Full Time Stats
    ht_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats.objects.get(team=home_team)
    at_ht_ft_stats: E5HalfTimeFullTimeStats = E5HalfTimeFullTimeStats.objects.get(team=away_team)

    # Query Scored Both Halves Stats
    ht_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=home_team)
    at_sbh_stats: E5ScoredBothHalfStats = E5ScoredBothHalfStats.objects.get(team=away_team)

    # Query Won Both Halves Stats
    ht_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=home_team)
    at_wbh_stats: E5WonBothHalfStats = E5WonBothHalfStats.objects.get(team=away_team)

    # Query 1st 2nd Half Goals Stats
    ht_fh_sh_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(team=home_team)
    at_fh_sh_goals_stats: E51st2ndHalfGoalsStats = E51st2ndHalfGoalsStats.objects.get(team=away_team)

    # Query Rescued Points Stats
    ht_rescued_points_stats: E5RescuedPointsStats = E5RescuedPointsStats.objects.get(team=home_team)
    at_rescued_points_stats: E5RescuedPointsStats = E5RescuedPointsStats.objects.get(team=away_team)

    # Query Clean Sheet Stats
    ht_clean_sheets_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=home_team)
    at_clean_sheets_stats: E5CleanSheetStats = E5CleanSheetStats.objects.get(team=away_team)

    # Query Won To Nil Stats
    ht_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=home_team)
    at_wtn_stats: E5WonToNilStats = E5WonToNilStats.objects.get(team=away_team)

    # Query Win Loss Margin Stats
    ht_wl_margin_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=home_team)
    at_wl_margin_stats: E5WinLossMarginStats = E5WinLossMarginStats.objects.get(team=away_team)

    # Query Scored First Stats
    ht_scored_first_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=home_team)
    at_scored_first_stats: E5ScoredFirstStats = E5ScoredFirstStats.objects.get(team=away_team)

    # Query Average First Goal Time Stats
    ht_avg_1st_gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats.objects.get(team=home_team)
    at_avg_1st_gt_stats: E5Average1stGoalTimeStats = E5Average1stGoalTimeStats.objects.get(team=away_team)

    # Query Average Team Goals Stats
    ht_avg_team_goals_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats.objects.get(team=home_team)
    at_avg_team_goals_stats: E5AverageTeamGoalsStats = E5AverageTeamGoalsStats.objects.get(team=away_team)

    # Query Early Goals Stats
    ht_early_goals_stats: E5EarlyGoalsStats = E5EarlyGoalsStats.objects.get(team=home_team)
    at_early_goals_stats: E5EarlyGoalsStats = E5EarlyGoalsStats.objects.get(team=away_team)

    # Query Late Goals Stats
    ht_late_goals_stats: E5LateGoalsStats = E5LateGoalsStats.objects.get(team=home_team)
    at_late_goals_stats: E5LateGoalsStats = E5LateGoalsStats.objects.get(team=away_team)

    # Context
    context = {
        'fixture': fixture, 'ht_btts_stats': ht_btts_stats, 'at_btts_stats': at_btts_stats,
        'ht_over_05_goals_stats': ht_over_05_goals_stats, 'at_over_05_goals_stats': at_over_05_goals_stats,
        'ht_over_15_goals_stats': ht_over_15_goals_stats, 'at_over_15_goals_stats': at_over_15_goals_stats,
        'ht_over_25_goals_stats': ht_over_25_goals_stats, 'at_over_25_goals_stats': at_over_25_goals_stats,
        'ht_over_35_goals_stats': ht_over_35_goals_stats, 'at_over_35_goals_stats': at_over_35_goals_stats,
        'ht_wdl_percent_stats': ht_wdl_percent_stats, 'at_wdl_percent_stats': at_wdl_percent_stats,
        'ht_cards_stats': ht_cards_stats, 'at_cards_stats': at_cards_stats,
        'ht_team_corners_stats': ht_team_corners_stats, 'at_team_corners_stats': at_team_corners_stats,
        'ht_match_corners_stats': ht_match_corners_stats, 'at_match_corners_stats': at_match_corners_stats,
        'ht_ht_ft_stats': ht_ht_ft_stats, 'at_ht_ft_stats': at_ht_ft_stats, 'ht_sbh_stats': ht_sbh_stats,
        'at_sbh_stats': at_sbh_stats, 'ht_wbh_stats': ht_wbh_stats, 'at_wbh_stats': at_wbh_stats,
        'ht_fh_sh_goals_stats': ht_fh_sh_goals_stats, 'at_fh_sh_goals_stats': at_fh_sh_goals_stats,
        'ht_rescued_points_stats': ht_rescued_points_stats, 'at_rescued_points_stats': at_rescued_points_stats,
        'ht_clean_sheets_stats': ht_clean_sheets_stats, 'at_clean_sheets_stats': at_clean_sheets_stats,
        'ht_wtn_stats': ht_wtn_stats, 'at_wtn_stats': at_wtn_stats, 'ht_wl_margin_stats': ht_wl_margin_stats,
        'at_wl_margin_stats': at_wl_margin_stats, 'ht_scored_first_stats': ht_scored_first_stats,
        'at_scored_first_stats': at_scored_first_stats, 'ht_avg_1st_gt_stats': ht_avg_1st_gt_stats,
        'at_avg_1st_gt_stats': at_avg_1st_gt_stats, 'ht_avg_team_goals_stats': ht_avg_team_goals_stats,
        'at_avg_team_goals_stats': at_avg_team_goals_stats, 'ht_early_goals_stats': ht_early_goals_stats,
        'at_early_goals_stats': at_early_goals_stats, 'ht_late_goals_stats': ht_late_goals_stats,
        'at_late_goals_stats': at_late_goals_stats
    }

    # Render
    return render(request=request, template_name='Website/fixture_details.html', context=context)


######################################################### STATS ########################################################
# E5
def league_details(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Season
    seasons: QuerySet(E5Season) = E5Season.objects.filter(league=league, active=True)

    season: E5Season | None = None
    if len(seasons) != 1:
        for element in seasons:
            element: E5Season
            if season is None:
                season = element
            elif element.date_added > season.date_added:
                season.active = False
                season.save()
                season = element
    elif len(seasons) == 1:
        season = seasons[0]

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query League Teams Ranking
    teams_ranking: QuerySet(E5TeamRanking) = E5TeamRanking.objects.filter(
        team__season__league__slug=league_slug).order_by('ranking')

    # Query Over 0.5 Goals Stats
    over_05_goals_stats: QuerySet(E5Over05GoalsStats) = E5Over05GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'season': season, 'teams_ranking': teams_ranking, 'leagues': leagues,
               'over_05_goals_stats': over_05_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_details.html', context=context)


# E5
def league_btts(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query BTTS Stats
    btts_stats: QuerySet(E5BttsStats) = E5BttsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'btts_stats': btts_stats}

    # Render
    return render(request=request, template_name='Website/league_btts.html', context=context)


# E5
def league_over_05_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Over 0.5 Goals Stats
    over_05_goals_stats: QuerySet(E5Over05GoalsStats) = E5Over05GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'over_05_goals_stats': over_05_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_over_05_goals.html', context=context)


# E5
def league_over_15_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Over 1.5 Goals Stats
    over_15_goals_stats: QuerySet(E5Over15GoalsStats) = E5Over15GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'over_15_goals_stats': over_15_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_over_15_goals.html', context=context)


# E5
def league_over_25_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Over 2.5 Goals Stats
    over_25_goals_stats: QuerySet(E5Over25GoalsStats) = E5Over25GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'over_25_goals_stats': over_25_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_over_25_goals.html', context=context)


# E5
def league_over_35_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Over 3.5 Goals Stats
    over_35_goals_stats: QuerySet(E5Over35GoalsStats) = E5Over35GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'over_35_goals_stats': over_35_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_over_35_goals.html', context=context)


# E5
def league_win_draw_loss_percentage(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Win Draw Loss Percentage Stats
    wdl_percent_stats: QuerySet(E5WinDrawLossPercentageStats) = E5WinDrawLossPercentageStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'wdl_percent_stats': wdl_percent_stats}

    # Render
    return render(request=request, template_name='Website/league_win_draw_loss_percentage.html', context=context)


# E5
def league_corners(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Team Corner Stats
    team_corners_stats: QuerySet(E5TeamCornerStats) = E5TeamCornerStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Query Match Corner Stats
    match_corners_stats: QuerySet(E5MatchCornerStats) = E5MatchCornerStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'team_corners_stats': team_corners_stats,
               'match_corners_stats': match_corners_stats}

    # Render
    return render(request=request, template_name='Website/league_corners.html', context=context)


# E5
def league_cards(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Cards Stats
    cards_stats: QuerySet(E5CardsStats) = E5CardsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'cards_stats': cards_stats}

    # Render
    return render(request=request, template_name='Website/league_cards.html', context=context)


# E5
def league_half_time_full_time(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Half Time Full Time Stats
    ht_ft_stats: QuerySet(E5HalfTimeFullTimeStats) = E5HalfTimeFullTimeStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'ht_ft_stats': ht_ft_stats}

    # Render
    return render(request=request, template_name='Website/league_half_time_full_time.html', context=context)


# E5
def league_scored_both_halves(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Scored Both Halves Stats
    sbh_stats: QuerySet(E5ScoredBothHalfStats) = E5ScoredBothHalfStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "sbh_stats": sbh_stats}

    # Render
    return render(request=request, template_name='Website/league_scored_both_halves.html', context=context)


# E5
def league_won_both_halves(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Won Both Halves Stats
    wbh_stats: QuerySet(E5WonBothHalfStats) = E5WonBothHalfStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "wbh_stats": wbh_stats}

    # Render
    return render(request=request, template_name='Website/league_won_both_halves.html', context=context)


# E5
def league_1st_2nd_half_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Won Both Halves Stats
    fh_sh_goals_stats: QuerySet(E51st2ndHalfGoalsStats) = E51st2ndHalfGoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "fh_sh_goals_stats": fh_sh_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_1st_2nd_half_goals.html', context=context)


# E5
def league_rescued_points(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Won Both Halves Stats
    rescued_points_stats: QuerySet(E5RescuedPointsStats) = E5RescuedPointsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "rescued_points_stats": rescued_points_stats}

    # Render
    return render(request=request, template_name='Website/league_rescued_points.html', context=context)


# E5
def league_clean_sheets(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Clean Sheets Stats
    clean_sheets_stats: QuerySet(E5CleanSheetStats) = E5CleanSheetStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "clean_sheets_stats": clean_sheets_stats}

    # Render
    return render(request=request, template_name='Website/league_clean_sheets.html', context=context)


# E5
def league_won_to_nil(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Won To Nil Stats
    wtn_stats: QuerySet(E5WonToNilStats) = E5WonToNilStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "wtn_stats": wtn_stats}

    # Render
    return render(request=request, template_name='Website/league_won_to_nil.html', context=context)


# E5
def league_win_loss(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Win Loss Margin Stats
    wl_margin_stats: QuerySet(E5WinLossMarginStats) = E5WinLossMarginStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "wl_margin_stats": wl_margin_stats}

    # Render
    return render(request=request, template_name='Website/league_win_loss.html', context=context)


# E5
def league_scored_first(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Scored First Stats
    scored_first_stats: QuerySet(E5ScoredFirstStats) = E5ScoredFirstStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "scored_first_stats": scored_first_stats}

    # Render
    return render(request=request, template_name='Website/league_scored_first.html', context=context)


# E5
def league_average_first_goal_time(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Average First Goal Time Stats
    avg_1st_gt_stats: QuerySet(E5Average1stGoalTimeStats) = E5Average1stGoalTimeStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "avg_1st_gt_stats": avg_1st_gt_stats}

    # Render
    return render(request=request, template_name='Website/league_average_first_goal_time.html', context=context)


# E5
def league_average_team_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Average Team Goals Stats
    avg_team_goals_stats: QuerySet(E5AverageTeamGoalsStats) = E5AverageTeamGoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "avg_team_goals_stats": avg_team_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_average_team_goals.html', context=context)


# E5
def league_early_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Early Goals Stats
    early_goals_stats: QuerySet(E5EarlyGoalsStats) = E5EarlyGoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "early_goals_stats": early_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_early_goals.html', context=context)


# E5
def league_late_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all().order_by('name')

    # Query Late Goals Stats
    late_goals_stats: QuerySet(E5LateGoalsStats) = E5LateGoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, "late_goals_stats": late_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_late_goals.html', context=context)
