from django.db import models
from django.contrib.auth.models import User


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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="firmy",
        null=True,
        blank=True,
    )
    nazwa = models.CharField(max_length=255)
    nip = models.CharField(max_length=20, blank=True)
    regon = models.CharField(max_length=20, blank=True)
    krs = models.CharField(max_length=20, blank=True)
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
    
    def liczba_aktywnych_sprawozdan(self):
        return self.sprawozdania.filter(czy_zarchiwizowane=False).count()


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
    czy_zarchiwizowane = models.BooleanField(default=False)

    class Meta:
        unique_together = ("firma", "rok")
        ordering = ["-rok"]

    def __str__(self):
        return f"{self.firma.nazwa} - {self.rok}"


class Mailing(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mailingi",
        null=True,
        blank=True,
    )
    temat = models.CharField(max_length=255)
    tresc = models.TextField()
    liczba_odbiorcow = models.IntegerField()
    liczba_firm_z_bazy = models.IntegerField(default=0)
    liczba_dodatkowych_odbiorcow = models.IntegerField(default=0)
    odbiorcy = models.TextField(blank=True)
    data_wyslania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temat} ({self.data_wyslania:%Y-%m-%d %H:%M})"
