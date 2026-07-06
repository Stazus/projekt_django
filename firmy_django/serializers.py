from rest_framework import serializers

from .models import Firma, SprawozdanieFinansowe, Branza, ProfilFirmy


class BranzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branza
        fields = ["id", "nazwa"]


class ProfilFirmySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilFirmy
        fields = [
            "opis",
            "logo",
            "banner",
        ]

class SprawozdanieFinansoweSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprawozdanieFinansowe
        fields = [
            "id",
            "rok",
            "naleznosci",
            "aktywa",
            "przychody",
            "zysk_netto",
            "plik_xml",
            "czy_zarchiwizowane",
        ]


class FirmaSerializer(serializers.ModelSerializer):
    branze = BranzaSerializer(many=True, read_only=True)
    profil = ProfilFirmySerializer(read_only=True)
    sprawozdania = SprawozdanieFinansoweSerializer(many=True, read_only=True)

    class Meta:
        model = Firma
        fields = [
            "id",
            "nazwa",
            "nip",
            "regon",
            "krs",
            "miasto",
            "email",
            "strona_www",
            "telefon",
            "email_zrodlo",
            "email_zrodlo_opis",
            "branze",
            "profil",
            "sprawozdania",
        ]
