from django.db.models import QuerySet
from django.shortcuts import render

from .models import (E5League, E5Season, E5TeamRanking, E5Over05GoalsStats, E5Over15GoalsStats, E5Over25GoalsStats,
                     E5Over35GoalsStats, E5TeamCornerStats, E5MatchCornerStats, E5CardsStats, E5Team)


######################################################### INDEX ########################################################
# E5
def index(request):
    # Query Teams
    total_teams: int = E5Team.objects.distinct().count()

    # Query Leagues
    total_leagues: int = E5League.objects.all().count()

    # Context
    context = {'total_leagues': total_leagues, 'total_teams': total_teams}

    # Render
    return render(request=request, template_name='Website/index.html', context=context)


######################################################## LEAGUES #######################################################
# E5
def leagues(request):
    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

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


######################################################### STATS ########################################################
# E5
def league_details(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Season
    season: E5Season = E5Season.objects.get(league=league, active=True)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

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
def league_over_05_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

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
    leagues: QuerySet(E5League) = E5League.objects.all()

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
    leagues: QuerySet(E5League) = E5League.objects.all()

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
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Query Over 3.5 Goals Stats
    over_35_goals_stats: QuerySet(E5Over35GoalsStats) = E5Over35GoalsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'over_35_goals_stats': over_35_goals_stats}

    # Render
    return render(request=request, template_name='Website/league_over_35_goals.html', context=context)


# E5
def league_corners(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

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
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Query Cards Stats
    cards_stats: QuerySet(E5CardsStats) = E5CardsStats.objects.filter(
        team__season__league__slug=league_slug).order_by('team__name')

    # Context
    context = {'league': league, 'leagues': leagues, 'cards_stats': cards_stats}

    # Render
    return render(request=request, template_name='Website/league_cards.html', context=context)


# E5
def league_rescued_points(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Context
    context = {'league': league, 'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/league_rescued_points.html', context=context)


# E5
def league_clean_sheets(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Context
    context = {'league': league, 'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/league_clean_sheets.html', context=context)


# E5
def league_win_loss(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Context
    context = {'league': league, 'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/league_win_loss.html', context=context)


# E5
def league_scored_first(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Context
    context = {'league': league, 'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/league_scored_first.html', context=context)


# E5
def league_average_team_goals(request, league_slug: str):
    # Query League
    league: E5League = E5League.objects.get(slug=league_slug)

    # Query Leagues
    leagues: QuerySet(E5League) = E5League.objects.all()

    # Context
    context = {'league': league, 'leagues': leagues}

    # Render
    return render(request=request, template_name='Website/league_average_team_goals.html', context=context)
