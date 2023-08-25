from django.urls import path

from Website import views

urlpatterns = [
    path('', views.index, name="Website-index"),
    path('leagues', views.leagues, name="Website-leagues"),
    path('league/<slug:league_slug>', views.league_details, name="Website-league_details"),
    path('league/<slug:league_slug>/over-05-goals', views.league_over_05_goals, name="Website-league_over_05_goals"),
    path('league/<slug:league_slug>/over-15-goals', views.league_over_15_goals, name="Website-league_over_15_goals"),
    path('league/<slug:league_slug>/over-25-goals', views.league_over_25_goals, name="Website-league_over_25_goals"),
    path('league/<slug:league_slug>/over-35-goals', views.league_over_35_goals, name="Website-league_over_35_goals"),
    path('league/<slug:league_slug>/corners', views.league_corners, name="Website-corners"),
    path('league/<slug:league_slug>/cards', views.league_cards, name="Website-cards"),
    path('league/<slug:league_slug>/rescued-points', views.league_rescued_points, name="Website-rescued_points"),
    path('league/<slug:league_slug>/clean-sheets', views.league_clean_sheets, name="Website-clean_sheets"),
    path('league/<slug:league_slug>/winloss', views.league_win_loss, name="Website-win_loss"),
    path('league/<slug:league_slug>/scored-first', views.league_scored_first, name="Website-scored_first"),
    path('league/<slug:league_slug>/avg-team-goals', views.league_average_team_goals,
         name="Website-average_team_goals"),
    path('teams', views.teams, name="Website-teams"),
    path('team/<slug:league_slug>/<slug:team_slug>', views.team_details, name="Website-team_details"),
]
