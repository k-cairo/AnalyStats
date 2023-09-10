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


################################################### FIXTURES ###########################################################
# E5
class E5Fixture(models.Model):
    id = models.AutoField(primary_key=True)
    home_team = models.ForeignKey(E5Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(E5Team, on_delete=models.CASCADE, related_name="away_team")
    date = models.DateField()
    kickoff_time = models.CharField(max_length=10)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Fixture"
        verbose_name_plural = "Fixtures"

    # E5
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.date} {self.kickoff_time}"

    # E5
    def exists(self) -> bool:
        return E5Fixture.objects.filter(home_team=self.home_team, away_team=self.away_team, date=self.date,
                                        kickoff_time=self.kickoff_time).exists()


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

    def not_empty(self) -> bool:
        return self.url != ""

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


# E5
class E51st2ndHalfGoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    overall_1st_2nd_half_goals_url = models.URLField(max_length=500)
    home_1st_2nd_half_goals_url = models.URLField(max_length=500)
    away_1st_2nd_half_goals_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "1st 2nd Half Goals Iframe"
        verbose_name_plural = "1st 2nd Half Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.overall_1st_2nd_half_goals_url = iframe.overall_1st_2nd_half_goals_url
        target_iframe.home_1st_2nd_half_goals_url = iframe.home_1st_2nd_half_goals_url
        target_iframe.away_1st_2nd_half_goals_url = iframe.away_1st_2nd_half_goals_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"1st 2nd Half Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return (self.overall_1st_2nd_half_goals_url != "" and self.home_1st_2nd_half_goals_url != "" and
                self.away_1st_2nd_half_goals_url != "")

    # E5
    def exists(self) -> bool:
        return E51st2ndHalfGoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5RescuedPointsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Rescued Points Iframe"
        verbose_name_plural = "Rescued Points Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Rescued Points Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5RescuedPointsIframe.objects.filter(season=self.season).exists()


# E5
class E5CleanSheetIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    clean_sheet_url = models.URLField(max_length=500)
    failed_to_score_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Clean Sheet Iframe"
        verbose_name_plural = "Clean Sheet Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.clean_sheet_url = iframe.clean_sheet_url
        target_iframe.failed_to_score_url = iframe.failed_to_score_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Clean Sheet Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.clean_sheet_url != "" and self.failed_to_score_url != ""

    # E5
    def exists(self) -> bool:
        return E5CleanSheetIframe.objects.filter(season=self.season).exists()


# E5
class E5WonToNilIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    won_to_nil_url = models.URLField(max_length=500)
    lost_to_nil_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Won To Nil Iframe"
        verbose_name_plural = "Won To Nil Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.won_to_nil_url = iframe.won_to_nil_url
        target_iframe.lost_to_nil_url = iframe.lost_to_nil_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Won To Nil Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.won_to_nil_url != "" and self.lost_to_nil_url != ""

    # E5
    def exists(self) -> bool:
        return E5WonToNilIframe.objects.filter(season=self.season).exists()


# E5
class E5WinLossMarginIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    winning_margins_url = models.URLField(max_length=500)
    losing_margins_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Win Loss Margin Iframe"
        verbose_name_plural = "Win Loss Margin Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.winning_margins_url = iframe.winning_margins_url
        target_iframe.losing_margins_url = iframe.losing_margins_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Win Loss Margin Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.winning_margins_url != "" and self.losing_margins_url != ""

    # E5
    def exists(self) -> bool:
        return E5WinLossMarginIframe.objects.filter(season=self.season).exists()


# E5
class E5ScoredFirstIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    scored_first_url = models.URLField(max_length=500)
    conceded_first_url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Scored First Iframe"
        verbose_name_plural = "Scored First Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.scored_first_url = iframe.scored_first_url
        target_iframe.conceded_first_url = iframe.conceded_first_url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Scored First Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.scored_first_url != "" and self.conceded_first_url != ""

    # E5
    def exists(self) -> bool:
        return E5ScoredFirstIframe.objects.filter(season=self.season).exists()


# E5
class E5Average1stGoalTimeIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Average 1st Goal Time Iframe"
        verbose_name_plural = "Average 1st Goal Time Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Average 1st Goal Time Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5Average1stGoalTimeIframe.objects.filter(season=self.season).exists()


# E5
class E5AverageTeamGoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Average Team Goals Iframe"
        verbose_name_plural = "Average Team Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Average Team Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5AverageTeamGoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5EarlyGoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Early Goals Iframe"
        verbose_name_plural = "Early Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Early Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5EarlyGoalsIframe.objects.filter(season=self.season).exists()


# E5
class E5LateGoalsIframe(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(E5Season, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Late Goals Iframe"
        verbose_name_plural = "Late Goals Iframes"

    # E5
    @classmethod
    def update_iframe(cls, season: E5Season, iframe):
        target_iframe = cls.objects.get(season=season)
        target_iframe.url = iframe.url
        target_iframe.save()

    # E5
    def __str__(self):
        return f"Late Goals Iframe - {self.season}"

    # E5
    def not_empty(self) -> bool:
        return self.url != ""

    # E5
    def exists(self) -> bool:
        return E5LateGoalsIframe.objects.filter(season=self.season).exists()


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
class E5BttsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_btts = models.IntegerField(null=True, blank=True)
    home_btts_percent = models.IntegerField(null=True, blank=True)
    home_btts_1h = models.IntegerField(null=True, blank=True)
    home_btts_1h_percent = models.IntegerField(null=True, blank=True)
    home_btts_2h = models.IntegerField(null=True, blank=True)
    home_btts_2h_percent = models.IntegerField(null=True, blank=True)
    home_btts_bh = models.IntegerField(null=True, blank=True)
    home_btts_bh_percent = models.IntegerField(null=True, blank=True)
    home_btts_25 = models.IntegerField(null=True, blank=True)
    home_btts_25_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_btts = models.IntegerField(null=True, blank=True)
    away_btts_percent = models.IntegerField(null=True, blank=True)
    away_btts_1h = models.IntegerField(null=True, blank=True)
    away_btts_1h_percent = models.IntegerField(null=True, blank=True)
    away_btts_2h = models.IntegerField(null=True, blank=True)
    away_btts_2h_percent = models.IntegerField(null=True, blank=True)
    away_btts_bh = models.IntegerField(null=True, blank=True)
    away_btts_bh_percent = models.IntegerField(null=True, blank=True)
    away_btts_25 = models.IntegerField(null=True, blank=True)
    away_btts_25_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_btts = models.IntegerField(null=True, blank=True)
    overall_btts_percent = models.IntegerField(null=True, blank=True)
    overall_btts_1h = models.IntegerField(null=True, blank=True)
    overall_btts_1h_percent = models.IntegerField(null=True, blank=True)
    overall_btts_2h = models.IntegerField(null=True, blank=True)
    overall_btts_2h_percent = models.IntegerField(null=True, blank=True)
    overall_btts_bh = models.IntegerField(null=True, blank=True)
    overall_btts_bh_percent = models.IntegerField(null=True, blank=True)
    overall_btts_25 = models.IntegerField(null=True, blank=True)
    overall_btts_25_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "BTTS Stats"
        verbose_name_plural = "BTTS Stats"

    # E5
    def __str__(self):
        return f"BTTS Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5BttsStats.objects.filter(team=self.team).exists()


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
class E5WinDrawLossPercentageStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_win_percent = models.IntegerField(null=True, blank=True)
    home_draw_percent = models.IntegerField(null=True, blank=True)
    home_loss_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_win_percent = models.IntegerField(null=True, blank=True)
    away_draw_percent = models.IntegerField(null=True, blank=True)
    away_loss_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_win_percent = models.IntegerField(null=True, blank=True)
    overall_draw_percent = models.IntegerField(null=True, blank=True)
    overall_loss_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Win Draw Loss Percentage Stats"
        verbose_name_plural = "Win Draw Loss Percentage Stats"

    # E5
    def __str__(self):
        return f"Win Draw Loss Percentage Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5WinDrawLossPercentageStats.objects.filter(team=self.team).exists()


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
    date_updated = models.DateTimeField(auto_now=True)

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
    date_updated = models.DateTimeField(auto_now=True)

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


# E5
class E5HalfTimeFullTimeStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_win_win = models.IntegerField(null=True, blank=True)
    home_win_draw = models.IntegerField(null=True, blank=True)
    home_win_loss = models.IntegerField(null=True, blank=True)
    home_draw_win = models.IntegerField(null=True, blank=True)
    home_draw_draw = models.IntegerField(null=True, blank=True)
    home_draw_loss = models.IntegerField(null=True, blank=True)
    home_loss_win = models.IntegerField(null=True, blank=True)
    home_loss_draw = models.IntegerField(null=True, blank=True)
    home_loss_loss = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_win_win = models.IntegerField(null=True, blank=True)
    away_win_draw = models.IntegerField(null=True, blank=True)
    away_win_loss = models.IntegerField(null=True, blank=True)
    away_draw_win = models.IntegerField(null=True, blank=True)
    away_draw_draw = models.IntegerField(null=True, blank=True)
    away_draw_loss = models.IntegerField(null=True, blank=True)
    away_loss_win = models.IntegerField(null=True, blank=True)
    away_loss_draw = models.IntegerField(null=True, blank=True)
    away_loss_loss = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Half Time Full Time Stats"
        verbose_name_plural = "Half Time Full Time Stats"

    # E5
    def __str__(self):
        return f"Half Time Full Time Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5HalfTimeFullTimeStats.objects.filter(team=self.team).exists()


# E5
class E5ScoredBothHalfStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_scored_both_halves = models.IntegerField(null=True, blank=True)
    home_scored_both_halves_percent = models.IntegerField(null=True, blank=True)
    home_conceded_both_halves = models.IntegerField(null=True, blank=True)
    home_conceded_both_halves_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_scored_both_halves = models.IntegerField(null=True, blank=True)
    away_scored_both_halves_percent = models.IntegerField(null=True, blank=True)
    away_conceded_both_halves = models.IntegerField(null=True, blank=True)
    away_conceded_both_halves_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_scored_both_halves = models.IntegerField(null=True, blank=True)
    overall_scored_both_halves_percent = models.IntegerField(null=True, blank=True)
    overall_conceded_both_halves = models.IntegerField(null=True, blank=True)
    overall_conceded_both_halves_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Scored Both Halves Stats"
        verbose_name_plural = "Scored Both Halves Stats"

    # E5
    def __str__(self):
        return f"Scored Both Halves Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5ScoredBothHalfStats.objects.filter(team=self.team).exists()


# E5
class E5WonBothHalfStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_won_both_halves = models.IntegerField(null=True, blank=True)
    home_won_both_halves_percent = models.IntegerField(null=True, blank=True)
    home_lost_both_halves = models.IntegerField(null=True, blank=True)
    home_lost_both_halves_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_won_both_halves = models.IntegerField(null=True, blank=True)
    away_won_both_halves_percent = models.IntegerField(null=True, blank=True)
    away_lost_both_halves = models.IntegerField(null=True, blank=True)
    away_lost_both_halves_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_won_both_halves = models.IntegerField(null=True, blank=True)
    overall_won_both_halves_percent = models.IntegerField(null=True, blank=True)
    overall_lost_both_halves = models.IntegerField(null=True, blank=True)
    overall_lost_both_halves_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Won Both Halves Stats"
        verbose_name_plural = "Won Both Halves Stats"

    # E5
    def __str__(self):
        return f"Won Both Halves Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5WonBothHalfStats.objects.filter(team=self.team).exists()


# E5
class E51st2ndHalfGoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_goals_scored = models.IntegerField(null=True, blank=True)
    home_goals_scored_1h = models.IntegerField(null=True, blank=True)
    home_goals_scored_1h_percent = models.IntegerField(null=True, blank=True)
    home_goals_scored_1h_average = models.FloatField(null=True, blank=True)
    home_goals_scored_2h = models.IntegerField(null=True, blank=True)
    home_goals_scored_2h_percent = models.IntegerField(null=True, blank=True)
    home_goals_scored_2h_average = models.FloatField(null=True, blank=True)
    home_goals_conceded = models.IntegerField(null=True, blank=True)
    home_goals_conceded_1h = models.IntegerField(null=True, blank=True)
    home_goals_conceded_1h_percent = models.IntegerField(null=True, blank=True)
    home_goals_conceded_1h_average = models.FloatField(null=True, blank=True)
    home_goals_conceded_2h = models.IntegerField(null=True, blank=True)
    home_goals_conceded_2h_percent = models.IntegerField(null=True, blank=True)
    home_goals_conceded_2h_average = models.FloatField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_goals_scored = models.IntegerField(null=True, blank=True)
    away_goals_scored_1h = models.IntegerField(null=True, blank=True)
    away_goals_scored_1h_percent = models.IntegerField(null=True, blank=True)
    away_goals_scored_1h_average = models.FloatField(null=True, blank=True)
    away_goals_scored_2h = models.IntegerField(null=True, blank=True)
    away_goals_scored_2h_percent = models.IntegerField(null=True, blank=True)
    away_goals_scored_2h_average = models.FloatField(null=True, blank=True)
    away_goals_conceded = models.IntegerField(null=True, blank=True)
    away_goals_conceded_1h = models.IntegerField(null=True, blank=True)
    away_goals_conceded_1h_percent = models.IntegerField(null=True, blank=True)
    away_goals_conceded_1h_average = models.FloatField(null=True, blank=True)
    away_goals_conceded_2h = models.IntegerField(null=True, blank=True)
    away_goals_conceded_2h_percent = models.IntegerField(null=True, blank=True)
    away_goals_conceded_2h_average = models.FloatField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_goals_scored = models.IntegerField(null=True, blank=True)
    overall_goals_scored_1h = models.IntegerField(null=True, blank=True)
    overall_goals_scored_1h_percent = models.IntegerField(null=True, blank=True)
    overall_goals_scored_1h_average = models.FloatField(null=True, blank=True)
    overall_goals_scored_2h = models.IntegerField(null=True, blank=True)
    overall_goals_scored_2h_percent = models.IntegerField(null=True, blank=True)
    overall_goals_scored_2h_average = models.FloatField(null=True, blank=True)
    overall_goals_conceded = models.IntegerField(null=True, blank=True)
    overall_goals_conceded_1h = models.IntegerField(null=True, blank=True)
    overall_goals_conceded_1h_percent = models.IntegerField(null=True, blank=True)
    overall_goals_conceded_1h_average = models.FloatField(null=True, blank=True)
    overall_goals_conceded_2h = models.IntegerField(null=True, blank=True)
    overall_goals_conceded_2h_percent = models.IntegerField(null=True, blank=True)
    overall_goals_conceded_2h_average = models.FloatField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "1st 2nd Half Goals Stats"
        verbose_name_plural = "1st 2nd Half Goals Stats"

    # E5
    def __str__(self):
        return f"1st 2nd Half Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E51st2ndHalfGoalsStats.objects.filter(team=self.team).exists()


# E5
class E5RescuedPointsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_conceded_first = models.IntegerField(null=True, blank=True)
    home_drawn_after_conceding_first = models.IntegerField(null=True, blank=True)
    home_won_after_conceding_first = models.IntegerField(null=True, blank=True)
    home_rescued_points = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_conceded_first = models.IntegerField(null=True, blank=True)
    away_drawn_after_conceding_first = models.IntegerField(null=True, blank=True)
    away_won_after_conceding_first = models.IntegerField(null=True, blank=True)
    away_rescued_points = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_conceded_first = models.IntegerField(null=True, blank=True)
    overall_drawn_after_conceding_first = models.IntegerField(null=True, blank=True)
    overall_won_after_conceding_first = models.IntegerField(null=True, blank=True)
    overall_rescued_points = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Rescued Points Stats"
        verbose_name_plural = "Rescued Points Stats"

    # E5
    def __str__(self):
        return f"Rescued Points Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5RescuedPointsStats.objects.filter(team=self.team).exists()


# E5
class E5CleanSheetStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_clean_sheet = models.IntegerField(null=True, blank=True)
    home_clean_sheet_percent = models.IntegerField(null=True, blank=True)
    home_failed_to_score = models.IntegerField(null=True, blank=True)
    home_failed_to_score_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_clean_sheet = models.IntegerField(null=True, blank=True)
    away_clean_sheet_percent = models.IntegerField(null=True, blank=True)
    away_failed_to_score = models.IntegerField(null=True, blank=True)
    away_failed_to_score_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_clean_sheet = models.IntegerField(null=True, blank=True)
    overall_clean_sheet_percent = models.IntegerField(null=True, blank=True)
    overall_failed_to_score = models.IntegerField(null=True, blank=True)
    overall_failed_to_score_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Clean Sheet Stats"
        verbose_name_plural = "Clean Sheet Stats"

    # E5
    def __str__(self):
        return f"Clean Sheet Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5CleanSheetStats.objects.filter(team=self.team).exists()


# E5
class E5WonToNilStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_won_to_nil = models.IntegerField(null=True, blank=True)
    home_won_to_nil_percent = models.IntegerField(null=True, blank=True)
    home_lost_to_nil = models.IntegerField(null=True, blank=True)
    home_lost_to_nil_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_won_to_nil = models.IntegerField(null=True, blank=True)
    away_won_to_nil_percent = models.IntegerField(null=True, blank=True)
    away_lost_to_nil = models.IntegerField(null=True, blank=True)
    away_lost_to_nil_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_won_to_nil = models.IntegerField(null=True, blank=True)
    overall_won_to_nil_percent = models.IntegerField(null=True, blank=True)
    overall_lost_to_nil = models.IntegerField(null=True, blank=True)
    overall_lost_to_nil_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Won To Nil Stats"
        verbose_name_plural = "Won To Nil Stats"

    # E5
    def __str__(self):
        return f"Won To Nil Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5WonToNilStats.objects.filter(team=self.team).exists()


# E5
class E5WinLossMarginStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_games_won = models.IntegerField(null=True, blank=True)
    home_games_won_by_1 = models.IntegerField(null=True, blank=True)
    home_games_won_by_2 = models.IntegerField(null=True, blank=True)
    home_games_won_by_3 = models.IntegerField(null=True, blank=True)
    home_games_won_by_4_or_more = models.IntegerField(null=True, blank=True)
    home_games_loose = models.IntegerField(null=True, blank=True)
    home_games_loose_by_1 = models.IntegerField(null=True, blank=True)
    home_games_loose_by_2 = models.IntegerField(null=True, blank=True)
    home_games_loose_by_3 = models.IntegerField(null=True, blank=True)
    home_games_loose_by_4_or_more = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_games_won = models.IntegerField(null=True, blank=True)
    away_games_won_by_1 = models.IntegerField(null=True, blank=True)
    away_games_won_by_2 = models.IntegerField(null=True, blank=True)
    away_games_won_by_3 = models.IntegerField(null=True, blank=True)
    away_games_won_by_4_or_more = models.IntegerField(null=True, blank=True)
    away_games_loose = models.IntegerField(null=True, blank=True)
    away_games_loose_by_1 = models.IntegerField(null=True, blank=True)
    away_games_loose_by_2 = models.IntegerField(null=True, blank=True)
    away_games_loose_by_3 = models.IntegerField(null=True, blank=True)
    away_games_loose_by_4_or_more = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Win Loss Margin Stats"
        verbose_name_plural = "Win Loss Margin Stats"

    # E5
    def __str__(self):
        return f"Win Loss Margin Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5WinLossMarginStats.objects.filter(team=self.team).exists()


# E5
class E5ScoredFirstStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_scored_first = models.IntegerField(null=True, blank=True)
    home_scored_first_percent = models.IntegerField(null=True, blank=True)
    home_conceded_first = models.IntegerField(null=True, blank=True)
    home_conceded_first_percent = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_scored_first = models.IntegerField(null=True, blank=True)
    away_scored_first_percent = models.IntegerField(null=True, blank=True)
    away_conceded_first = models.IntegerField(null=True, blank=True)
    away_conceded_first_percent = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_scored_first = models.IntegerField(null=True, blank=True)
    overall_scored_first_percent = models.IntegerField(null=True, blank=True)
    overall_conceded_first = models.IntegerField(null=True, blank=True)
    overall_conceded_first_percent = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Scored First Stats"
        verbose_name_plural = "Scored First Stats"

    # E5
    def __str__(self):
        return f"Scored First Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5ScoredFirstStats.objects.filter(team=self.team).exists()


# E5
class E5Average1stGoalTimeStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_first_goal_time_scored_average = models.FloatField(null=True, blank=True)
    home_first_goal_time_conceded_average = models.FloatField(null=True, blank=True)
    away_first_goal_time_scored_average = models.FloatField(null=True, blank=True)
    away_first_goal_time_conceded_average = models.FloatField(null=True, blank=True)
    overall_first_goal_time_scored_average = models.FloatField(null=True, blank=True)
    overall_first_goal_time_conceded_average = models.FloatField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Average 1st Goal Time Stats"
        verbose_name_plural = "Average 1st Goal Time Stats"

    # E5
    def __str__(self):
        return f"Average 1st Goal Time Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5Average1stGoalTimeStats.objects.filter(team=self.team).exists()


# E5
class E5AverageTeamGoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_goals_scored_average = models.FloatField(null=True, blank=True)
    home_goals_conceded_average = models.FloatField(null=True, blank=True)
    away_goals_scored_average = models.FloatField(null=True, blank=True)
    away_goals_conceded_average = models.FloatField(null=True, blank=True)
    overall_goals_scored_average = models.FloatField(null=True, blank=True)
    overall_goals_conceded_average = models.FloatField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Average Team Goals Stats"
        verbose_name_plural = "Average Team Goals Stats"

    # E5
    def __str__(self):
        return f"Average Team Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5AverageTeamGoalsStats.objects.filter(team=self.team).exists()


# E5
class E5EarlyGoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_scored_early = models.IntegerField(null=True, blank=True)
    home_conceded_early = models.IntegerField(null=True, blank=True)
    home_scored_or_conceded_early = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_scored_early = models.IntegerField(null=True, blank=True)
    away_conceded_early = models.IntegerField(null=True, blank=True)
    away_scored_or_conceded_early = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_scored_early = models.IntegerField(null=True, blank=True)
    overall_conceded_early = models.IntegerField(null=True, blank=True)
    overall_scored_or_conceded_early = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Early Goals Stats"
        verbose_name_plural = "Early Goals Stats"

    # E5
    def __str__(self):
        return f"Early Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5EarlyGoalsStats.objects.filter(team=self.team).exists()


# E5
class E5LateGoalsStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(E5Team, on_delete=models.CASCADE)
    home_matches_played = models.IntegerField(null=True, blank=True)
    home_scored_late = models.IntegerField(null=True, blank=True)
    home_conceded_late = models.IntegerField(null=True, blank=True)
    home_scored_or_conceded_late = models.IntegerField(null=True, blank=True)
    away_matches_played = models.IntegerField(null=True, blank=True)
    away_scored_late = models.IntegerField(null=True, blank=True)
    away_conceded_late = models.IntegerField(null=True, blank=True)
    away_scored_or_conceded_late = models.IntegerField(null=True, blank=True)
    overall_matches_played = models.IntegerField(null=True, blank=True)
    overall_scored_late = models.IntegerField(null=True, blank=True)
    overall_conceded_late = models.IntegerField(null=True, blank=True)
    overall_scored_or_conceded_late = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    # E5
    class Meta:
        verbose_name = "Late Goals Stats"
        verbose_name_plural = "Late Goals Stats"

    # E5
    def __str__(self):
        return f"Late Goals Stats - {self.team}"

    # E5
    def exists(self) -> bool:
        return E5LateGoalsStats.objects.filter(team=self.team).exists()
