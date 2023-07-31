from django.urls import path

from Website import views

urlpatterns = [
    # Index
    path('', views.index, name="Website-index"),
    # Match Stats
    path('match/<int:match_id>/', views.match_stats, name="Website-match")
]
