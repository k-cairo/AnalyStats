from django.db import models


# E5
class E5Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    url = models.URLField()

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
class E5Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    championship = models.ForeignKey(E5Championship, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    url = models.URLField()

    objects = models.Manager()

    # E5
    def __str__(self):
        return self.name

    # E5
    def check_not_empty(self) -> bool:
        return self.name != "" and self.gender != "" and self.url != ""

    # E5
    def check_if_exists(self) -> bool:
        return E5Team.objects.filter(name=self.name, url=self.url, championship=self.championship).exists()
