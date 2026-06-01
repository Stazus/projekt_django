from django.contrib import admin

from .models import Firma, SprawozdanieFinansowe


class SprawozdanieFinansoweInline(admin.TabularInline):
    model = SprawozdanieFinansowe
    extra = 1


@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ("nazwa", "nip", "regon", "miasto")
    search_fields = ("nazwa", "nip", "regon")
    list_filter = ("miasto",)
    inlines = [SprawozdanieFinansoweInline]


@admin.register(SprawozdanieFinansowe)
class SprawozdanieFinansoweAdmin(admin.ModelAdmin):
    list_display = ("firma", "rok", "naleznosci", "aktywa", "przychody", "zysk_netto")
    search_fields = ("firma__nazwa", "firma__nip", "firma__regon")
    list_filter = ("rok",)
