import re
from decimal import Decimal, InvalidOperation

from django.core.mail import send_mail
from django.db.models import Max
from django.shortcuts import render, get_object_or_404

from .models import Firma, Mailing

def index(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "name_asc")
    min_naleznosci = request.GET.get("min_naleznosci", "")

    firmy = Firma.objects.prefetch_related("sprawozdania").all()

    if query:
        firmy = firmy.filter(
            nazwa__icontains=query
        ) | firmy.filter(
            nip__icontains=query
        )

    if min_naleznosci:
        try:
            min_value = Decimal(min_naleznosci.replace(" ", "").replace(",", "."))
            firmy = firmy.filter(sprawozdania__naleznosci__gte=min_value).distinct()
        except InvalidOperation:
            min_naleznosci = ""

    firmy = firmy.annotate(max_naleznosci=Max("sprawozdania__naleznosci"))

    if sort == "name_desc":
        firmy = firmy.order_by("-nazwa")
    elif sort == "reports_desc":
        firmy = sorted(
            firmy,
            key=lambda f: f.sprawozdania.count(),
            reverse=True
        )
    elif sort == "naleznosci_desc":
        firmy = firmy.order_by("-max_naleznosci", "nazwa")
    elif sort == "naleznosci_asc":
        firmy = firmy.order_by("max_naleznosci", "nazwa")
    else:
        firmy = firmy.order_by("nazwa")

    return render(request, "firmy_django/index.html", {
        "firmy": firmy,
        "query": query,
        "sort": sort,
        "min_naleznosci": min_naleznosci,
    })


def szczegoly_firmy(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.prefetch_related("sprawozdania"),
        id=firma_id
    )

    return render(request, "firmy_django/szczegoly_firmy.html", {
        "firma": firma,
    })


def rozdziel_adresy_email(tekst):
    if not tekst:
        return []

    kandydaci = re.split(r"[\s,;]+", tekst)
    adresy = []

    for adres in kandydaci:
        adres = adres.strip()
        if "@" in adres and "." in adres:
            adresy.append(adres)

    return list(dict.fromkeys(adresy))


def przygotuj_mailing(request):
    if request.method == "POST" and request.POST.getlist("firmy_ids"):
        wybrane_firmy_ids = request.POST.getlist("firmy_ids")

        firmy = Firma.objects.filter(
            id__in=wybrane_firmy_ids,
            email__isnull=False
        ).exclude(email="")

        dodatkowi_odbiorcy_tekst = request.POST.get("dodatkowi_odbiorcy", "")
        dodatkowi_odbiorcy = rozdziel_adresy_email(dodatkowi_odbiorcy_tekst)

        odbiorcy_z_bazy = [firma.email for firma in firmy]
        wszyscy_odbiorcy = list(dict.fromkeys(odbiorcy_z_bazy + dodatkowi_odbiorcy))

        temat = request.POST.get("temat", "")
        tresc = request.POST.get("tresc", "")
        akcja = request.POST.get("akcja", "")

        komunikat = ""

        if akcja == "wyslij_test":
            if temat and tresc and wszyscy_odbiorcy:
                send_mail(
                    subject=temat,
                    message=tresc,
                    from_email=None,
                    recipient_list=wszyscy_odbiorcy,
                    fail_silently=False,
                )

                Mailing.objects.create(
                    temat=temat,
                    tresc=tresc,
                    liczba_odbiorcow=len(wszyscy_odbiorcy),
                )

                komunikat = (
                    f"Test mailingu wykonany. "
                    f"Mailing został wysłany do {len(wszyscy_odbiorcy)} odbiorców."
                )
            else:
                komunikat = (
                    "Nie wysłano testu. Uzupełnij temat, treść i przynajmniej jednego odbiorcę."
                )

        return render(request, "firmy_django/podsumowanie_mailing.html", {
            "firmy": firmy,
            "liczba_firm": firmy.count(),
            "dodatkowi_odbiorcy": dodatkowi_odbiorcy,
            "liczba_dodatkowych": len(dodatkowi_odbiorcy),
            "wszyscy_odbiorcy": wszyscy_odbiorcy,
            "liczba_wszystkich": len(wszyscy_odbiorcy),
            "temat": temat,
            "tresc": tresc,
            "komunikat": komunikat,
        })

    wybrane_firmy_ids = request.POST.getlist("firmy")

    firmy = Firma.objects.filter(
        id__in=wybrane_firmy_ids,
        email__isnull=False
    ).exclude(email="")

    return render(request, "firmy_django/przygotuj_mailing.html", {
        "firmy": firmy,
        "liczba_firm": firmy.count(),
    })
