from django.db import models


EMAIL_ZRODLO_CHOICES = [
    ("", "Brak"),
    ("recznie", "Ręcznie"),
    ("xml", "XML"),
    ("strona_www", "Strona internetowa"),
    ("ceidg", "CEIDG / biznes.gov.pl"),
    ("gus_regon", "GUS REGON"),
    ("krs", "KRS"),
    ("inne", "Inne"),
]


class Firma(models.Model):
    nazwa = models.CharField(max_length=255)
    nip = models.CharField(max_length=20, blank=True)
    regon = models.CharField(max_length=20, blank=True)
    miasto = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    email_zrodlo = models.CharField(
        max_length=50,
        choices=EMAIL_ZRODLO_CHOICES,
        blank=True,
    )
    email_zrodlo_opis = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nazwa


class SprawozdanieFinansowe(models.Model):
    firma = models.ForeignKey(
        Firma,
        on_delete=models.CASCADE,
        related_name="sprawozdania"
    )
    rok = models.PositiveIntegerField()
    naleznosci = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    aktywa = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    przychody = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    zysk_netto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    plik_xml = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("firma", "rok")
        ordering = ["-rok"]

    def __str__(self):
        return f"{self.firma.nazwa} - {self.rok}"

class Mailing(models.Model):
    temat = models.CharField(max_length=255)
    tresc = models.TextField()
    liczba_odbiorcow = models.IntegerField()
    data_wyslania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temat} ({self.data_wyslania:%Y-%m-%d %H:%M})"
