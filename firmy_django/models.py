from django.db import models

class Firma(models.Model):
    nazwa = models.CharField(max_length=255, default="brak")
    nip = models.CharField(max_length=20, blank=True, default="brak")
    kwota = models.FloatField(default=0.0)
    plik = models.CharField(max_length=255, blank=True, default="brak")

    def __str__(self):
        return self.nazwa