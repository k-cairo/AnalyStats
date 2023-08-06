from django.db import models


# E5
class E5Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    url = models.URLField()
    parse_country = models.BooleanField(default=False)
    logo = models.URLField(null=True, blank=True)

    objects = models.Manager()

    # E5
    def __str__(self):
        return self.name

    # E5
    def check_not_empty(self) -> bool:
        return self.name != "" and self.organisation != "" and self.url != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Country.objects.filter(name=self.name, url=self.url).exists()


# E5
class E5Championship(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(E5Country, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    url = models.URLField()
    logo = models.URLField(null=True, blank=True)

    objects = models.Manager()

    # E5
    def __str__(self):
        return self.name

    # E5
    def check_not_empty(self) -> bool:
        return self.name != "" and self.country != "" and self.url != "" and self.gender != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Championship.objects.filter(name=self.name, url=self.url, country=self.country).exists()


# E5
class E5Season(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    championship = models.ForeignKey(E5Championship, on_delete=models.CASCADE, blank=True, null=True)
    squads = models.IntegerField(default=None)
    url = models.URLField(default="")
    active = models.BooleanField(default=False)

    objects = models.Manager()

    # E5
    def __str__(self):
        return self.name

    # E5
    def check_not_empty(self) -> bool:
        return self.name != "" and self.squads is not None and self.url != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Season.objects.filter(
            name=self.name, url=self.url, championship=self.championship, squads=self.squads).exists()


# E5
class E5Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField()
    logo = models.URLField(null=True, blank=True)

    objects = models.Manager()

    # E5
    def __str__(self):
        return self.name

    # E5
    def check_not_empty(self) -> bool:
        return self.name != "" and self.url != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Team.objects.filter(name=self.name, url=self.url, season=self.season).exists()


# E5
class E5TeamStats(models.Model):
    id = models.AutoField(primary_key=True)
    goals = models.IntegerField()
    xg = models.FloatField(null=True, blank=True)
    shots = models.IntegerField()
    shots_on_target = models.IntegerField()
    corners = models.IntegerField(null=True, blank=True)
    tackles = models.IntegerField()
    fouls = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    offsides = models.IntegerField()


# E5
class E5Match(models.Model):
    id = models.AutoField(primary_key=True)
    championship = models.ForeignKey(E5Championship, on_delete=models.CASCADE)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    home_team = models.ForeignKey(E5Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(E5Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.CharField(max_length=40)
    ht_stats = models.ForeignKey(E5TeamStats, on_delete=models.CASCADE, blank=True, null=True, related_name='ht_stats')
    at_stats = models.ForeignKey(E5TeamStats, on_delete=models.CASCADE, blank=True, null=True, related_name='at_stats')

    objects = models.Manager()

    def __str__(self):
        return f"{self.home_team.name} - {self.away_team.name}"

    # E5
    def check_not_empty(self) -> bool:
        return self.home_team != "" and self.away_team != "" and self.date != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Match.objects.filter(home_team=self.home_team, away_team=self.away_team, date=self.date,
                                      season=self.season, championship=self.championship).exists()
