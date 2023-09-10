from django.contrib import admin

from Website.models import (E5League, E5Season, E5LeagueTableIframe, E5Team, E5TeamRanking, E5BttsIframes, \
                            E5Over05GoalsIframe, E5Over15GoalsIframe, E5Over25GoalsIframe, E5Over35GoalsIframe,
                            E5CornersIframes, E5CardsIframes, E5TeamCornerStats, E5MatchCornerStats,
                            E5Over05GoalsStats, E5Over15GoalsStats, E5Over25GoalsStats, E5Over35GoalsStats,
                            E5CardsStats)


# E5
@admin.register(E5League)
class E5LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'logo', 'slug', 'date_updated')
    search_fields = ('name', 'date_updated')
    list_per_page = 15000


# E5
@admin.register(E5Season)
class E5SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league', 'url', 'active', 'date_added')
    search_fields = ('name', 'league', 'date_added')
    list_filter = ('league', 'active')
    list_per_page = 15000


# E5
@admin.register(E5LeagueTableIframe)
class E5LeagueTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'url', 'date_updated')
    search_fields = ('season', 'url', 'date_updated')
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Team)
class E5TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'logo', 'season', 'date_updated')
    search_fields = ('name', 'date_updated')
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5TeamRanking)
class E5TeamRankingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ranking', 'team', 'matches_played', 'matches_won', 'matches_drawn', 'matches_lost',
                    'goals_scored', 'goals_conceded', 'goals_difference', 'points', 'date_updated')
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5BttsIframes)
class E5BttsIframeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'season', 'btts_url', 'btts_1h_url', 'btts_2h_url', 'btts_bh_url', 'btts_25_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Over05GoalsIframe)
class E5Over05GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_05_goals_url', 'over_05_goals_1h_url', 'over_05_goals_2h_url',
                    'over_05_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Over15GoalsIframe)
class E5Over15GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_15_goals_url', 'over_15_goals_1h_url', 'over_15_goals_2h_url',
                    'over_15_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Over25GoalsIframe)
class E5Over25GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_25_goals_url', 'over_25_goals_1h_url', 'over_25_goals_2h_url',
                    'over_25_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Over35GoalsIframe)
class E5Over35GoalsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'over_35_goals_url', 'over_35_goals_1h_url', 'over_35_goals_2h_url',
                    'over_35_goals_bh_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5CornersIframes)
class E5CornersIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'team_corners_for_1h_url', 'team_corners_against_1h_url', 'team_corners_for_2h_url',
                    'team_corners_against_2h_url', 'team_corners_for_ft_url', 'team_corners_against_ft_url',
                    "match_corners_1h_url", "match_corners_2h_url", 'match_corners_ft_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5CardsIframes)
class E5CardsIframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'yellow_cards_for_url', 'yellow_cards_against_url', 'red_cards_for_url',
                    'red_cards_against_url', 'date_updated')
    search_fields = ('season',)
    list_filter = ('season',)
    list_per_page = 15000


# E5
@admin.register(E5Over05GoalsStats)
class E5Over05GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5Over05GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5Over15GoalsStats)
class E5Over15GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5Over15GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5Over25GoalsStats)
class E5Over25GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5Over25GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5Over35GoalsStats)
class E5Over35GoalsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5Over35GoalsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5TeamCornerStats)
class E5TeamCornerStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5TeamCornerStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5MatchCornerStats)
class E5MatchCornerStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5MatchCornerStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000


# E5
@admin.register(E5CardsStats)
class E5CardsStatsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in E5CardsStats._meta.get_fields()]
    search_fields = ('team',)
    list_filter = ('team',)
    list_per_page = 15000
