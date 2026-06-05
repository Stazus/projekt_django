from django.contrib import admin

from .models import Firma, SprawozdanieFinansowe, Mailing

class SprawozdanieFinansoweInline(admin.TabularInline):
    model = SprawozdanieFinansowe
    extra = 1


@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = (
        "nazwa",
        "nip",
        "email",
        "email_zrodlo",
        "email_zrodlo_opis",
        "regon",
        "miasto",
    )

    search_fields = (
        "nazwa",
        "nip",
        "email",
        "email_zrodlo_opis",
        "regon",
    )

    list_filter = ("miasto",)
    inlines = [SprawozdanieFinansoweInline]


@admin.register(SprawozdanieFinansowe)
class SprawozdanieFinansoweAdmin(admin.ModelAdmin):
    list_display = ("firma", "rok", "naleznosci", "aktywa", "przychody", "zysk_netto")
    search_fields = ("firma__nazwa", "firma__nip", "firma__regon")
    list_filter = ("rok",)
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "temat",
        "liczba_odbiorcow",
        "data_wyslania",
    )

    search_fields = ("temat", "tresc")
    list_filter = ("data_wyslania",)
