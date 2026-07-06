from django.db import models
from django.contrib.auth.models import User


class EmailZrodlo(models.TextChoices):
    BRAK = "", "Brak"
    RECZNIE = "recznie", "Ręcznie"
    XML = "xml", "XML"
    STRONA_WWW = "strona_www", "Strona internetowa"
    CEIDG = "ceidg", "CEIDG / biznes.gov.pl"
    GUS_REGON = "gus_regon", "GUS REGON"
    KRS = "krs", "KRS"
    INNE = "inne", "Inne"

class Branza(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa  


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
    strona_www = models.URLField(blank=True)
    telefon = models.CharField(max_length=30, blank=True)
    branze = models.ManyToManyField(
        Branza,
        blank=True,
        related_name="firmy"
    )    
    email_zrodlo = models.CharField(
        max_length=50,
        choices=EmailZrodlo.choices,
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
    plik_xml = models.FileField(
        upload_to="sprawozdania_xml/importy/",
        blank=True
    )
    czy_zarchiwizowane = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["firma", "rok"],
                name="unique_sprawozdanie_firma_rok",
            )
        ]
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
    firmy_odbiorcy = models.ManyToManyField(
        Firma,
        blank=True,
        related_name="mailingi"
    )
    odbiorcy_zewnetrzni = models.TextField(blank=True)
    data_wyslania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temat} ({self.data_wyslania:%Y-%m-%d %H:%M})"
    
    @property
    def lista_odbiorcow_zewnetrznych(self):
        if not self.odbiorcy_zewnetrzni:
            return []

        return [
            email.strip()
            for email in self.odbiorcy_zewnetrzni.replace(";", ",").split(",")
            if email.strip()
        ]

    @property
    def liczba_firm_z_bazy(self):
        return self.firmy_odbiorcy.count()

    @property
    def liczba_dodatkowych_odbiorcow(self):
        return len(self.lista_odbiorcow_zewnetrznych)

    @property
    def liczba_odbiorcow(self):
        return self.liczba_firm_z_bazy + self.liczba_dodatkowych_odbiorcow


class ProfilFirmy(models.Model):
    firma = models.OneToOneField(
        Firma,
        on_delete=models.CASCADE,
        related_name="profil"
    )
    opis = models.TextField(blank=True)
    logo = models.FileField(
        upload_to="profile_firm/loga/",
        blank=True
    )
    banner = models.FileField(
        upload_to="profile_firm/bannery/",
        blank=True
    )

    def __str__(self):
        return f"Profil firmy: {self.firma.nazwa}"

