from django.contrib import admin

from Website import models


# E5
@admin.register(models.E5League)
class E5LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'logo', 'slug', 'date_updated')
    search_fields = ('name', 'date_updated')
    list_per_page = 15000


# E5
@admin.register(models.E5Season)
class E5SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league', 'url', 'active', 'date_added')
    search_fields = ('name', 'league', 'date_added')
    list_filter = ('league', 'active')
    list_per_page = 15000


# E5
@admin.register(models.E5Team)
class E5TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'logo', 'season', 'date_updated')
    search_fields = ('name', 'date_updated')
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5LeagueTableIframe)
class E5LeagueTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'url', 'date_updated')
    search_fields = ('season', 'url', 'date_updated')
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5TeamRanking)
class E5TeamRankingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ranking', 'team', 'matches_played', 'matches_won', 'matches_drawn', 'matches_lost',
                    'goals_scored', 'goals_conceded', 'goals_difference', 'points', 'date_updated')
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5BttsIframes)
class E5BttsIframeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'season', 'btts_url', 'btts_1h_url', 'btts_2h_url', 'btts_bh_url', 'btts_25_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5BttsStats)
class E5BttsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5BttsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over05GoalsIframe)
class E5Over05GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_05_goals_url', 'over_05_goals_1h_url', 'over_05_goals_2h_url',
                    'over_05_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over05GoalsStats)
class E5Over05GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Over05GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over15GoalsIframe)
class E5Over15GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_15_goals_url', 'over_15_goals_1h_url', 'over_15_goals_2h_url',
                    'over_15_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over15GoalsStats)
class E5Over15GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Over15GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over25GoalsIframe)
class E5Over25GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_25_goals_url', 'over_25_goals_1h_url', 'over_25_goals_2h_url',
                    'over_25_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over25GoalsStats)
class E5Over25GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Over25GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over35GoalsIframe)
class E5Over35GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_35_goals_url', 'over_35_goals_1h_url', 'over_35_goals_2h_url',
                    'over_35_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5Over35GoalsStats)
class E5Over35GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Over35GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5WinDrawLossPercentageIframe)
class E5WinDrawLossPercentageIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WinDrawLossPercentageIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5WinDrawLossPercentageStats)
class E5WinDrawLossPercentageStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WinDrawLossPercentageStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5CornersIframes)
class E5CornersIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'team_corners_for_1h_url', 'team_corners_against_1h_url', 'team_corners_for_2h_url',
                    'team_corners_against_2h_url', 'team_corners_for_ft_url', 'team_corners_against_ft_url',
                    "match_corners_1h_url", "match_corners_2h_url", 'match_corners_ft_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5TeamCornerStats)
class E5TeamCornerStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5TeamCornerStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5MatchCornerStats)
class E5MatchCornerStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5MatchCornerStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5CardsIframes)
class E5CardsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'yellow_cards_for_url', 'yellow_cards_against_url', 'red_cards_for_url',
                    'red_cards_against_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5CardsStats)
class E5CardsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5CardsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5HalfTimeFullTimeIframe)
class E5HalfTimeFullTimeIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5HalfTimeFullTimeIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5HalfTimeFullTimeStats)
class E5HalfTimeFullTimeStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5HalfTimeFullTimeStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5ScoredBothHalfIframes)
class E5ScoredBothHalfIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5ScoredBothHalfIframes._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5ScoredBothHalfStats)
class E5ScoredBothHalfStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5ScoredBothHalfStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5WonBothHalfIframes)
class E5WonBothHalfIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WonBothHalfIframes._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5WonBothHalfStats)
class E5WonBothHalfStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WonBothHalfStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E51st2ndHalfGoalsIframe)
class E51st2ndHalfGoalsIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E51st2ndHalfGoalsIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E51st2ndHalfGoalsStats)
class E51st2ndHalfGoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E51st2ndHalfGoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5RescuedPointsIframe)
class E5RescuedPointsIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5RescuedPointsIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5RescuedPointsStats)
class E5RescuedPointsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5RescuedPointsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5CleanSheetIframe)
class E5CleanSheetIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5CleanSheetIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5CleanSheetStats)
class E5CleanSheetStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5CleanSheetStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5WonToNilIframe)
class E5WonToNilIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WonToNilIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5WonToNilStats)
class E5WonToNilStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WonToNilStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5WinLossMarginIframe)
class E5WinLossMarginIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WinLossMarginIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5WinLossMarginStats)
class E5WinLossMarginStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5WinLossMarginStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5ScoredFirstIframe)
class E5ScoredFirstIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5ScoredFirstIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5ScoredFirstStats)
class E5ScoredFirstStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5ScoredFirstStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5Average1stGoalTimeIframe)
class E5Average1stGoalTimeIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Average1stGoalTimeIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5Average1stGoalTimeStats)
class E5Average1stGoalTimeStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5Average1stGoalTimeStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5AverageTeamGoalsIframe)
class E5AverageTeamGoalsIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5AverageTeamGoalsIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5AverageTeamGoalsStats)
class E5AverageTeamGoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5AverageTeamGoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5EarlyGoalsIframe)
class E5EarlyGoalsIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5EarlyGoalsIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5EarlyGoalsStats)
class E5EarlyGoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5EarlyGoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(models.E5LateGoalsIframe)
class E5LateGoalsIframeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5LateGoalsIframe._meta.get_fields()]
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(models.E5LateGoalsStats)
class E5LateGoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.E5LateGoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000
