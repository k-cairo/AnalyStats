from datetime import datetime, date, timedelta

from django.db.models import QuerySet, Q
from django.shortcuts import render

from Website.models import E5Match


# E5
def index(request):
    day1 = date.today().strftime("%Y-%m-%d")
    day2 = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    day3 = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    day4 = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    day5 = (date.today() + timedelta(days=4)).strftime("%Y-%m-%d")
    day6 = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    day7 = (date.today() + timedelta(days=6)).strftime("%Y-%m-%d")

    # Query next 7 days matchs
    matchs: QuerySet(E5Match) = E5Match.objects.filter(
        Q(date=day1) | Q(date=day2) | Q(date=day3) | Q(date=day4) | Q(date=day5) | Q(date=day6) | Q(date=day7))

    # Context
    context = {'matchs': matchs}

    # Render
    return render(request=request, template_name='Website/index.html', context=context)


# E5
def match_stats(request, match_id: int):
    # Query match
    match: E5Match = E5Match.objects.get(id=match_id)

    # Context
    context = {'match': match}

    # Render
    return render(request=request, template_name='Website/match_stats.html', context=context)
