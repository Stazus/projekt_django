import os
import re
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RejestracjaForm
from .models import Firma, Mailing, SprawozdanieFinansowe


def rejestracja(request):
    if request.method == "POST":
        form = RejestracjaForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RejestracjaForm()

    return render(request, "firmy_django/rejestracja.html", {
        "form": form,
    })


@login_required
def index(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "name_asc")
    min_naleznosci = request.GET.get("min_naleznosci", "")

    firmy = Firma.objects.filter(
        owner=request.user
    ).prefetch_related("sprawozdania")

    if query:
        firmy = firmy.filter(nazwa__icontains=query) | firmy.filter(nip__icontains=query)

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
        firmy = sorted(firmy, key=lambda f: f.sprawozdania.count(), reverse=True)
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


@login_required
def szczegoly_firmy(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.filter(owner=request.user).prefetch_related("sprawozdania"),
        id=firma_id
    )

    return render(request, "firmy_django/szczegoly_firmy.html", {
        "firma": firma,
    })


@login_required
def importuj_xml_ogolny(request):
    komunikat = ""

    if request.method == "POST":
        plik_xml = request.FILES.get("plik_xml")

        if plik_xml:
            try:
                ET.parse(plik_xml)

                komunikat = (
                    f"Plik {plik_xml.name} został odebrany "
                    f"i poprawnie odczytany jako XML."
                )

            except ET.ParseError:
                komunikat = (
                    f"Błąd: plik {plik_xml.name} "
                    f"nie jest poprawnym plikiem XML."
                )
        else:
            komunikat = "Nie wybrano pliku XML."

    return render(
        request,
        "firmy_django/importuj_xml_ogolny.html",
        {
            "komunikat": komunikat,
        }
    )


@login_required
def importuj_xml(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.filter(owner=request.user),
        id=firma_id
    )

    komunikat = ""

    if request.method == "POST":
        plik_xml = request.FILES.get("plik_xml")

        if plik_xml:
            try:
                ET.parse(plik_xml)

                plik_xml.seek(0)

                zawartosc_xml = plik_xml.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                czy_xml_pasuje_do_firmy = (
                    firma.nazwa.upper() in zawartosc_xml.upper()
                )

                nazwa_z_xml = ""
                nip_z_xml = ""
                krs_z_xml = ""
                rok_z_xml = ""

                root = ET.fromstring(zawartosc_xml)

                for element in root.iter():
                    tag = element.tag.split("}")[-1]

                    if tag == "NazwaFirmy" and element.text:
                        nazwa_z_xml = element.text.strip()

                    if tag == "P_1D" and element.text:
                        nip_z_xml = element.text.strip()

                    if tag == "P_1E" and element.text:
                        krs_z_xml = element.text.strip()

                    if tag == "OkresDo" and element.text:
                        rok_z_xml = element.text.strip()[:4]

                firma_z_xml = None

                if nip_z_xml:
                    firma_z_xml = Firma.objects.filter(
                        owner=request.user,
                        nip=nip_z_xml
                    ).first()

                if not firma_z_xml and krs_z_xml:
                    firma_z_xml = Firma.objects.filter(
                        owner=request.user,
                        krs=krs_z_xml
                    ).first()





                if firma_z_xml:
                    status_firmy_w_bazie = (
                        f"Firma z XML istnieje już w bazie: {firma_z_xml.nazwa}."
                    )

                    sprawozdanie_z_roku = firma_z_xml.sprawozdania.filter(
                        rok=rok_z_xml
                    ).first()

                    if sprawozdanie_z_roku:
                        status_firmy_w_bazie += (
                            f" Sprawozdanie za rok {rok_z_xml} już istnieje w bazie."
                            f" Możliwe, że importowany plik jest korektą istniejącego sprawozdania."
                            f" W przyszłości będzie można zastąpić istniejące sprawozdanie,"
                            f" zachować obie wersje, porównać je albo anulować import."
                        )

                    else:
                        SprawozdanieFinansowe.objects.create(
                            firma=firma_z_xml,
                            rok=int(rok_z_xml)
                        )

                        status_firmy_w_bazie += (
                            f" Sprawozdanie za rok {rok_z_xml} nie istniało jeszcze w bazie."
                            f" Zostało dodane jako nowe sprawozdanie tej firmy."
                        )
  
                else:
                    nowa_firma = Firma.objects.create(
                        owner=request.user,
                        nazwa=nazwa_z_xml or plik_xml.name,
                        nip=nip_z_xml,
                        krs=krs_z_xml
                    )

                    SprawozdanieFinansowe.objects.create(
                        firma=nowa_firma,
                        rok=int(rok_z_xml)
                    )

                    status_firmy_w_bazie = (
                        "Firma z XML nie istniała jeszcze w bazie."
                        f" Utworzono nową firmę: {nowa_firma.nazwa}."
                        f" Dodano sprawozdanie za rok {rok_z_xml}."
                    )

                katalog_importow = os.path.join(
                    "sprawozdania_xml",
                    "importy"
                )

                os.makedirs(
                    katalog_importow,
                    exist_ok=True
                )

                nazwa_pliku = (
                    f"firma_{firma.id}_{plik_xml.name}"
                )

                sciezka_pliku = os.path.join(
                    katalog_importow,
                    nazwa_pliku
                )

                plik_xml.seek(0)

                with open(
                    sciezka_pliku,
                    "wb+"
                ) as destination:
                    for chunk in plik_xml.chunks():
                        destination.write(chunk)

                if czy_xml_pasuje_do_firmy:
                    komunikat = (
                        f"Plik {plik_xml.name} został odebrany, "
                        f"poprawnie odczytany jako XML "
                        f"i zapisany na dysku. "
                        f"XML prawdopodobnie dotyczy wybranej firmy. "
                        f"Dane z XML: nazwa: {nazwa_z_xml or 'brak'}, "
                        f"NIP: {nip_z_xml or 'brak'}, "
                        f"KRS: {krs_z_xml or 'brak'}, "
                        f"Rok: {rok_z_xml or 'brak'}. "
                        f"{status_firmy_w_bazie}"

                    )

                else:
                    komunikat = (
                        f"Plik {plik_xml.name} został odebrany, "
                        f"poprawnie odczytany jako XML "
                        f"i zapisany na dysku. "
                        f"Uwaga: XML prawdopodobnie nie dotyczy wybranej firmy. "
                        f"Dane z XML: nazwa: {nazwa_z_xml or 'brak'}, "
                        f"NIP: {nip_z_xml or 'brak'}, "
                        f"KRS: {krs_z_xml or 'brak'}, "
                        f"Rok: {rok_z_xml or 'brak'}. "
                        f"{status_firmy_w_bazie}"
                    )

            except ET.ParseError:
                komunikat = (
                    f"Błąd: plik {plik_xml.name} "
                    f"nie jest poprawnym plikiem XML."
                )
        else:
            komunikat = "Nie wybrano pliku XML."

    return render(
        request,
        "firmy_django/importuj_xml.html",
        {
            "firma": firma,
            "komunikat": komunikat,
        }
    )


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


@login_required
def przygotuj_mailing(request):
    if request.method == "POST" and request.POST.getlist("firmy_ids"):
        wybrane_firmy_ids = request.POST.getlist("firmy_ids")

        firmy = Firma.objects.filter(
            owner=request.user,
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
                    owner=request.user,
                    temat=temat,
                    tresc=tresc,
                    liczba_odbiorcow=len(wszyscy_odbiorcy),
                    liczba_firm_z_bazy=firmy.count(),
                    liczba_dodatkowych_odbiorcow=len(dodatkowi_odbiorcy),
                    odbiorcy="\n".join(wszyscy_odbiorcy),
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
        owner=request.user,
        id__in=wybrane_firmy_ids,
        email__isnull=False
    ).exclude(email="")

    return render(request, "firmy_django/przygotuj_mailing.html", {
        "firmy": firmy,
        "liczba_firm": firmy.count(),
    })


@login_required
def historia_mailingow(request):
    mailingi = Mailing.objects.filter(owner=request.user).order_by("-data_wyslania")

    return render(request, "firmy_django/historia_mailingow.html", {
        "mailingi": mailingi,
    })


@login_required
def szczegoly_mailingu(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id, owner=request.user)

    return render(request, "firmy_django/szczegoly_mailingu.html", {
        "mailing": mailing,
    })
