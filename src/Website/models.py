from django.db import models


#################################################### LEAGUE ############################################################
# E5
class E5League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    logo = models.URLField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=150, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"

    # E5
    def __str__(self):
        return self.name

    # E5
    def not_empty(self) -> bool:
        return self.name != "" and self.url != ""

    # E5
    def exists(self) -> bool:
        return E5League.objects.filter(name=self.name).exists()


#################################################### SEASON ############################################################
# E5
class E5Season(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(E5League, on_delete=models.CASCADE)
    url = models.URLField()
    active = models.BooleanField()
    date_added = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    # E5
    def __str__(self):
        return f"{self.league} - season:{self.name}"

    # E5
    def not_empty(self) -> bool:
        return self.name != "" and self.url != ""

    # E5
    def exists(self) -> bool:
        return E5Season.objects.filter(name=self.name, league=self.league).exists()


##################################################### TEAM #############################################################
# E5
class E5Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    logo = models.URLField(null=True, blank=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    # E5
    def __str__(self):
        return self.name

    # E5
    def not_empty(self) -> bool:
        return self.name != "" and self.url != ""

    # E5
    def exists(self) -> bool:
        return E5Team.objects.filter(name=self.name, season=self.season).exists()


#################################################### IFRAMES ###########################################################
# E5
class E5LeagueTableIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "League Table Iframe"
        verbose_name_plural = "League Tables Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"League Table - {self.season}"

    # E5
    def exists(self) -> bool:
        return E5LeagueTableIframe.objects.filter(season=self.season).exists()


# E5
class E5BttsIframes(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    btts_url = models.URLField(max_length=500)
    btts_1h_url = models.URLField(max_length=500)
    btts_2h_url = models.URLField(max_length=500)
    btts_bh_url = models.URLField(max_length=500)
    btts_25_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "BTTS Iframe"
        verbose_name_plural = "BTTS Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.btts_url = iframe.btts_url
        target_iframe.btts_1h_url = iframe.btts_1h_url
        target_iframe.btts_2h_url = iframe.btts_2h_url
        target_iframe.btts_bh_url = iframe.btts_bh_url
        target_iframe.btts_25_url = iframe.btts_25_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"BTTS Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.btts_url != "" and self.btts_1h_url != "" and self.btts_2h_url != "" and self.btts_bh_url != ""
                and self.btts_25_url != "")

    # E5
    def exists(self) -> bool:
        return E5BttsIframes.objects.filter(season=self.season).exists()


# E5
class E5Over05GoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    over_05_goals_url = models.URLField(max_length=500)
    over_05_goals_1h_url = models.URLField(max_length=500)
    over_05_goals_2h_url = models.URLField(max_length=500)
    over_05_goals_bh_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 0.5 Goals Iframe"
        verbose_name_plural = "Over 0.5 Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.over_05_goals_url = iframe.over_05_goals_url
        target_iframe.over_05_goals_1h_url = iframe.over_05_goals_1h_url
        target_iframe.over_05_goals_2h_url = iframe.over_05_goals_2h_url
        target_iframe.over_05_goals_bh_url = iframe.over_05_goals_bh_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Over 0.5 Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.over_05_goals_url != "" and self.over_05_goals_1h_url != "" and self.over_05_goals_2h_url != ""
                and self.over_05_goals_bh_url != "")

    # E5
    def exists(self) -> bool:
        return E5Over05GoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5Over15GoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    over_15_goals_url = models.URLField(max_length=500)
    over_15_goals_1h_url = models.URLField(max_length=500)
    over_15_goals_2h_url = models.URLField(max_length=500)
    over_15_goals_bh_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 1.5 Goals Iframe"
        verbose_name_plural = "Over 1.5 Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.over_15_goals_url = iframe.over_15_goals_url
        target_iframe.over_15_goals_1h_url = iframe.over_15_goals_1h_url
        target_iframe.over_15_goals_2h_url = iframe.over_15_goals_2h_url
        target_iframe.over_15_goals_bh_url = iframe.over_15_goals_bh_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Over 1.5 Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.over_15_goals_url != "" and self.over_15_goals_1h_url != "" and self.over_15_goals_2h_url != "" and self.over_15_goals_bh_url != ""

    # E5
    def exists(self) -> bool:
        return E5Over15GoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5Over25GoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    over_25_goals_url = models.URLField(max_length=500)
    over_25_goals_1h_url = models.URLField(max_length=500)
    over_25_goals_2h_url = models.URLField(max_length=500)
    over_25_goals_bh_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 2.5 Goals Iframe"
        verbose_name_plural = "Over 2.5 Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.over_25_goals_url = iframe.over_25_goals_url
        target_iframe.over_25_goals_1h_url = iframe.over_25_goals_1h_url
        target_iframe.over_25_goals_2h_url = iframe.over_25_goals_2h_url
        target_iframe.over_25_goals_bh_url = iframe.over_25_goals_bh_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Over 2.5 Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.over_25_goals_url != "" and self.over_25_goals_1h_url != "" and self.over_25_goals_2h_url != "" and self.over_25_goals_bh_url != ""

    # E5
    def exists(self) -> bool:
        return E5Over25GoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5Over35GoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    over_35_goals_url = models.URLField(max_length=500)
    over_35_goals_1h_url = models.URLField(max_length=500)
    over_35_goals_2h_url = models.URLField(max_length=500)
    over_35_goals_bh_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 3.5 Goals Iframe"
        verbose_name_plural = "Over 3.5 Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.over_35_goals_url = iframe.over_35_goals_url
        target_iframe.over_35_goals_1h_url = iframe.over_35_goals_1h_url
        target_iframe.over_35_goals_2h_url = iframe.over_35_goals_2h_url
        target_iframe.over_35_goals_bh_url = iframe.over_35_goals_bh_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Over 3.5 Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.over_35_goals_url != "" and self.over_35_goals_1h_url != "" and self.over_35_goals_2h_url != ""
                and self.over_35_goals_bh_url != "")

    # E5
    def exists(self) -> bool:
        return E5Over35GoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5CornersIframes(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    team_corners_for_1h_url = models.URLField(max_length=500)
    team_corners_against_1h_url = models.URLField(max_length=500)
    team_corners_for_2h_url = models.URLField(max_length=500)
    team_corners_against_2h_url = models.URLField(max_length=500)
    team_corners_for_ft_url = models.URLField(max_length=500)
    team_corners_against_ft_url = models.URLField(max_length=500)
    match_corners_1h_url = models.URLField(max_length=500)
    match_corners_2h_url = models.URLField(max_length=500)
    match_corners_ft_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Corners Iframe"
        verbose_name_plural = "Corners Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
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

    # E5
    def __str__(self):
        return f"Corners Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.team_corners_for_1h_url != "" and self.team_corners_against_1h_url != "" and
                self.team_corners_for_2h_url != "" and self.team_corners_against_2h_url != "" and
                self.team_corners_for_ft_url != "" and self.team_corners_against_ft_url != "" and
                self.match_corners_1h_url != "" and self.match_corners_2h_url != "" and self.match_corners_ft_url != "")

    # E5
    def exists(self) -> bool:
        return E5CornersIframes.objects.filter(season=self.season).exists()


# E5
class E5CardsIframes(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    yellow_cards_for_url = models.URLField(max_length=500)
    yellow_cards_against_url = models.URLField(max_length=500)
    red_cards_for_url = models.URLField(max_length=500)
    red_cards_against_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Cards Iframe"
        verbose_name_plural = "Cards Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.yellow_cards_for_url = iframe.yellow_cards_for_url
        target_iframe.yellow_cards_against_url = iframe.yellow_cards_against_url
        target_iframe.red_cards_for_url = iframe.red_cards_for_url
        target_iframe.red_cards_against_url = iframe.red_cards_against_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Cards Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.yellow_cards_for_url != "" and self.yellow_cards_against_url != "" and
                self.red_cards_for_url != "" and self.red_cards_against_url != "")

    # E5
    def exists(self) -> bool:
        return E5CardsIframes.objects.filter(season=self.season).exists()


# E5
class E5WinDrawLossPercentageIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Win Draw Loss Percentage Iframe"
        verbose_name_plural = "Win Draw Loss Percentage Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Win Draw Loss Percentage Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5WinDrawLossPercentageIframe.objects.filter(season=self.season).exists()


# E5
class E5HalfTimeFullTimeIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Half Time Full Time Iframe"
        verbose_name_plural = "Half Time Full Time Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Half Time Full Time Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5HalfTimeFullTimeIframe.objects.filter(season=self.season).exists()


# E5
class E5ScoredBothHalfIframes(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    scored_both_half_url = models.URLField(max_length=500)
    conceded_both_half_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Scored Both Half Iframe"
        verbose_name_plural = "Scored Both Half Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.scored_both_half_url = iframe.scored_both_half_url
        target_iframe.conceded_both_half_url = iframe.conceded_both_half_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Scored Both Half Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.scored_both_half_url != "" and self.conceded_both_half_url != ""

    # E5
    def exists(self) -> bool:
        return E5ScoredBothHalfIframes.objects.filter(season=self.season).exists()


# E5
class E5WonBothHalfIframes(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    won_both_half_url = models.URLField(max_length=500)
    lost_both_half_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Won Both Half Iframe"
        verbose_name_plural = "Won Both Half Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe) -> None:
        target_iframe = cls.objects.get(season=season)
        target_iframe.won_both_half_url = iframe.won_both_half_url
        target_iframe.lost_both_half_url = iframe.lost_both_half_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Won Both Half Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.won_both_half_url != "" and self.lost_both_half_url != ""

    # E5
    def exists(self) -> bool:
        return E5WonBothHalfIframes.objects.filter(season=self.season).exists()


#################################################### STATS #############################################################
# E5
class E5TeamRanking(models.Model):
    id = models.AutoField(primary_key=True)
    ranking = models.IntegerField()
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    matches_played = models.IntegerField()
    matches_won = models.IntegerField()
    matches_drawn = models.IntegerField()
    matches_lost = models.IntegerField()
    goals_scored = models.IntegerField()
    goals_conceded = models.IntegerField()
    goals_difference = models.IntegerField()
    points = models.IntegerField()
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Team Ranking"
        verbose_name_plural = "Team Rankings"

    # E5
    def __str__(self):
        return f"Ranking {self.team} - {self.team.season}"

    # E5
    def exists(self) -> bool:
        return E5TeamRanking.objects.filter(team=self.team).exists()


# E5
class E5Over05GoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_over_05_goals = models.IntegerField(null=True, blank=True)
    home_over_05_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_05_goals_1h = models.IntegerField(null=True, blank=True)
    home_over_05_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_05_goals_2h = models.IntegerField(null=True, blank=True)
    home_over_05_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_05_goals_bh = models.IntegerField(null=True, blank=True)
    home_over_05_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_over_05_goals = models.IntegerField(null=True, blank=True)
    away_over_05_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_05_goals_1h = models.IntegerField(null=True, blank=True)
    away_over_05_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_05_goals_2h = models.IntegerField(null=True, blank=True)
    away_over_05_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_05_goals_bh = models.IntegerField(null=True, blank=True)
    away_over_05_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_over_05_goals = models.IntegerField(null=True, blank=True)
    overall_over_05_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_05_goals_1h = models.IntegerField(null=True, blank=True)
    overall_over_05_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_05_goals_2h = models.IntegerField(null=True, blank=True)
    overall_over_05_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_05_goals_bh = models.IntegerField(null=True, blank=True)
    overall_over_05_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 0.5 Goals Stats"
        verbose_name_plural = "Over 0.5 Goals Stats"

    # E5
    def __str__(self):
        return f"Over 0.5 Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5Over05GoalsStats.objects.filter(team=self.team).exists()


# E5
class E5Over15GoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_over_15_goals = models.IntegerField(null=True, blank=True)
    home_over_15_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_15_goals_1h = models.IntegerField(null=True, blank=True)
    home_over_15_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_15_goals_2h = models.IntegerField(null=True, blank=True)
    home_over_15_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_15_goals_bh = models.IntegerField(null=True, blank=True)
    home_over_15_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_over_15_goals = models.IntegerField(null=True, blank=True)
    away_over_15_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_15_goals_1h = models.IntegerField(null=True, blank=True)
    away_over_15_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_15_goals_2h = models.IntegerField(null=True, blank=True)
    away_over_15_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_15_goals_bh = models.IntegerField(null=True, blank=True)
    away_over_15_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_over_15_goals = models.IntegerField(null=True, blank=True)
    overall_over_15_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_15_goals_1h = models.IntegerField(null=True, blank=True)
    overall_over_15_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_15_goals_2h = models.IntegerField(null=True, blank=True)
    overall_over_15_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_15_goals_bh = models.IntegerField(null=True, blank=True)
    overall_over_15_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 1.5 Goals Stats"
        verbose_name_plural = "Over 1.5 Goals Stats"

    # E5
    def __str__(self):
        return f"Over 1.5 Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5Over15GoalsStats.objects.filter(team=self.team).exists()


# E5
class E5Over25GoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_over_25_goals = models.IntegerField(null=True, blank=True)
    home_over_25_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_25_goals_1h = models.IntegerField(null=True, blank=True)
    home_over_25_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_25_goals_2h = models.IntegerField(null=True, blank=True)
    home_over_25_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_25_goals_bh = models.IntegerField(null=True, blank=True)
    home_over_25_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_over_25_goals = models.IntegerField(null=True, blank=True)
    away_over_25_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_25_goals_1h = models.IntegerField(null=True, blank=True)
    away_over_25_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_25_goals_2h = models.IntegerField(null=True, blank=True)
    away_over_25_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_25_goals_bh = models.IntegerField(null=True, blank=True)
    away_over_25_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_over_25_goals = models.IntegerField(null=True, blank=True)
    overall_over_25_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_25_goals_1h = models.IntegerField(null=True, blank=True)
    overall_over_25_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_25_goals_2h = models.IntegerField(null=True, blank=True)
    overall_over_25_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_25_goals_bh = models.IntegerField(null=True, blank=True)
    overall_over_25_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 2.5 Goals Stats"
        verbose_name_plural = "Over 2.5 Goals Stats"

    # E5
    def __str__(self):
        return f"Over 2.5 Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5Over25GoalsStats.objects.filter(team=self.team).exists()


# E5
class E5Over35GoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_over_35_goals = models.IntegerField(null=True, blank=True)
    home_over_35_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_35_goals_1h = models.IntegerField(null=True, blank=True)
    home_over_35_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_35_goals_2h = models.IntegerField(null=True, blank=True)
    home_over_35_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    home_over_35_goals_bh = models.IntegerField(null=True, blank=True)
    home_over_35_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_over_35_goals = models.IntegerField(null=True, blank=True)
    away_over_35_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_35_goals_1h = models.IntegerField(null=True, blank=True)
    away_over_35_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_35_goals_2h = models.IntegerField(null=True, blank=True)
    away_over_35_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    away_over_35_goals_bh = models.IntegerField(null=True, blank=True)
    away_over_35_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_over_35_goals = models.IntegerField(null=True, blank=True)
    overall_over_35_goals_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_35_goals_1h = models.IntegerField(null=True, blank=True)
    overall_over_35_goals_1h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_35_goals_2h = models.IntegerField(null=True, blank=True)
    overall_over_35_goals_2h_percent = models.CharField(max_length=10, null=True, blank=True)
    overall_over_35_goals_bh = models.IntegerField(null=True, blank=True)
    overall_over_35_goals_bh_percent = models.CharField(max_length=10, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Over 3.5 Goals Stats"
        verbose_name_plural = "Over 3.5 Goals Stats"

    # E5
    def __str__(self):
        return f"Over 3.5 Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5Over35GoalsStats.objects.filter(team=self.team).exists()


# E5
class E5TeamCornerStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_corners_for_1h = models.IntegerField(null=True, blank=True)
    home_corners_for_1h_average = models.FloatField(null=True, blank=True)
    home_corners_against_1h = models.IntegerField(null=True, blank=True)
    home_corners_against_1h_average = models.FloatField(null=True, blank=True)
    home_corners_for_2h = models.IntegerField(null=True, blank=True)
    home_corners_for_2h_average = models.FloatField(null=True, blank=True)
    home_corners_against_2h = models.IntegerField(null=True, blank=True)
    home_corners_against_2h_average = models.FloatField(null=True, blank=True)
    home_corners_for_ft = models.IntegerField(null=True, blank=True)
    home_corners_for_ft_average = models.FloatField(null=True, blank=True)
    home_corners_against_ft = models.IntegerField(null=True, blank=True)
    home_corners_against_ft_average = models.FloatField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_corners_for_1h = models.IntegerField(null=True, blank=True)
    away_corners_for_1h_average = models.FloatField(null=True, blank=True)
    away_corners_against_1h = models.IntegerField(null=True, blank=True)
    away_corners_against_1h_average = models.FloatField(null=True, blank=True)
    away_corners_for_2h = models.IntegerField(null=True, blank=True)
    away_corners_for_2h_average = models.FloatField(null=True, blank=True)
    away_corners_against_2h = models.IntegerField(null=True, blank=True)
    away_corners_against_2h_average = models.FloatField(null=True, blank=True)
    away_corners_for_ft = models.IntegerField(null=True, blank=True)
    away_corners_for_ft_average = models.FloatField(null=True, blank=True)
    away_corners_against_ft = models.IntegerField(null=True, blank=True)
    away_corners_against_ft_average = models.FloatField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_corners_for_1h = models.IntegerField(null=True, blank=True)
    overall_corners_for_1h_average = models.FloatField(null=True, blank=True)
    overall_corners_against_1h = models.IntegerField(null=True, blank=True)
    overall_corners_against_1h_average = models.FloatField(null=True, blank=True)
    overall_corners_for_2h = models.IntegerField(null=True, blank=True)
    overall_corners_for_2h_average = models.FloatField(null=True, blank=True)
    overall_corners_against_2h = models.IntegerField(null=True, blank=True)
    overall_corners_against_2h_average = models.FloatField(null=True, blank=True)
    overall_corners_for_ft = models.IntegerField(null=True, blank=True)
    overall_corners_for_ft_average = models.FloatField(null=True, blank=True)
    overall_corners_against_ft = models.IntegerField(null=True, blank=True)
    overall_corners_against_ft_average = models.FloatField(null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Team Corner Stats"
        verbose_name_plural = "Team Corner Stats"

    # E5
    def __str__(self):
        return f"Team Corner Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5TeamCornerStats.objects.filter(team=self.team).exists()


# E5
class E5MatchCornerStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_corners_1h = models.IntegerField(null=True, blank=True)
    home_corners_1h_average = models.FloatField(null=True, blank=True)
    home_corners_2h = models.IntegerField(null=True, blank=True)
    home_corners_2h_average = models.FloatField(null=True, blank=True)
    home_corners_ft = models.IntegerField(null=True, blank=True)
    home_corners_ft_average = models.FloatField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_corners_1h = models.IntegerField(null=True, blank=True)
    away_corners_1h_average = models.FloatField(null=True, blank=True)
    away_corners_2h = models.IntegerField(null=True, blank=True)
    away_corners_2h_average = models.FloatField(null=True, blank=True)
    away_corners_ft = models.IntegerField(null=True, blank=True)
    away_corners_ft_average = models.FloatField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_corners_1h = models.IntegerField(null=True, blank=True)
    overall_corners_1h_average = models.FloatField(null=True, blank=True)
    overall_corners_2h = models.IntegerField(null=True, blank=True)
    overall_corners_2h_average = models.FloatField(null=True, blank=True)
    overall_corners_ft = models.IntegerField(null=True, blank=True)
    overall_corners_ft_average = models.FloatField(null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Match Corner Stats"
        verbose_name_plural = "Match Corner Stats"

    # E5
    def __str__(self):
        return f"Match Corner Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5MatchCornerStats.objects.filter(team=self.team).exists()


# E5
class E5CardsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_yellow_cards_for = models.IntegerField(null=True, blank=True)
    home_yellow_cards_for_average = models.FloatField(null=True, blank=True)
    home_yellow_cards_against = models.IntegerField(null=True, blank=True)
    home_yellow_cards_against_average = models.FloatField(null=True, blank=True)
    home_red_cards_for = models.IntegerField(null=True, blank=True)
    home_red_cards_for_average = models.FloatField(null=True, blank=True)
    home_red_cards_against = models.IntegerField(null=True, blank=True)
    home_red_cards_against_average = models.FloatField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_yellow_cards_for = models.IntegerField(null=True, blank=True)
    away_yellow_cards_for_average = models.FloatField(null=True, blank=True)
    away_yellow_cards_against = models.IntegerField(null=True, blank=True)
    away_yellow_cards_against_average = models.FloatField(null=True, blank=True)
    away_red_cards_for = models.IntegerField(null=True, blank=True)
    away_red_cards_for_average = models.FloatField(null=True, blank=True)
    away_red_cards_against = models.IntegerField(null=True, blank=True)
    away_red_cards_against_average = models.FloatField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_yellow_cards_for = models.IntegerField(null=True, blank=True)
    overall_yellow_cards_for_average = models.FloatField(null=True, blank=True)
    overall_yellow_cards_against = models.IntegerField(null=True, blank=True)
    overall_yellow_cards_against_average = models.FloatField(null=True, blank=True)
    overall_red_cards_for = models.IntegerField(null=True, blank=True)
    overall_red_cards_for_average = models.FloatField(null=True, blank=True)
    overall_red_cards_against = models.IntegerField(null=True, blank=True)
    overall_red_cards_against_average = models.FloatField(null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Cards Stats"
        verbose_name_plural = "Cards Stats"

    # E5
    def __str__(self):
        return f"Cards Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5CardsStats.objects.filter(team=self.team).exists()
