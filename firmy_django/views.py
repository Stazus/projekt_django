import os
import re
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RejestracjaForm, FirmaForm
from .models import Firma, Mailing, SprawozdanieFinansowe, ProfilFirmy

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .serializers import FirmaSerializer, SprawozdanieFinansoweSerializer

from .tasks import wyslij_mailing_task

from drf_spectacular.utils import extend_schema

from .tasks import wyslij_mailing_task


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
        firmy = sorted(
            firmy,
            key=lambda f: f.sprawozdania.filter(zarchiwizowane=False).count(),
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


@login_required
def szczegoly_firmy(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.filter(owner=request.user)
        .prefetch_related("sprawozdania", "branze"),
        id=firma_id
    )

    profil = ProfilFirmy.objects.filter(firma=firma).first()

    return render(request, "firmy_django/szczegoly_firmy.html", {
        "firma": firma,
        "profil": profil,
    })


@login_required
def importuj_xml_ogolny(request):
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

                nazwa_z_xml = ""
                nip_z_xml = ""
                krs_z_xml = ""
                rok_z_xml = ""
                naleznosci_z_xml = Decimal("0")

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
                        
                    if (
                        "Naleznosci" in tag
                        or "Należności" in tag
                        or "Naleznosc" in tag
                        or "Należność" in tag
                    ) and element.text:
                        try:
                            naleznosci_z_xml = Decimal(
                                element.text.strip().replace(" ", "").replace(",", ".")
                            )
                        except InvalidOperation:
                            naleznosci_z_xml = Decimal("0")  
                            
                    if tag == "Aktywa_B_II":
                        for dziecko in element:
                            tag_dziecka = dziecko.tag.split("}")[-1]

                            if tag_dziecka == "KwotaA" and dziecko.text:
                                try:
                                    naleznosci_z_xml = Decimal(
                                        dziecko.text.strip().replace(" ", "").replace(",", ".")
                                    )

                                    if "WTysiacach" in zawartosc_xml:
                                        naleznosci_z_xml = naleznosci_z_xml * Decimal("1000")

                                except InvalidOperation:
                                    naleznosci_z_xml = Decimal("0")                        
                              

                firma_z_xml = Firma.objects.filter(
                    owner=request.user,
                    nip=nip_z_xml
                ).first()

                if not firma_z_xml and krs_z_xml:
                    firma_z_xml = Firma.objects.filter(
                        owner=request.user,
                        krs=krs_z_xml
                    ).first()

                if not firma_z_xml:
                    firma_z_xml = Firma.objects.create(
                        owner=request.user,
                        nazwa=nazwa_z_xml or "Nieznana firma",
                        nip=nip_z_xml,
                        krs=krs_z_xml,
                    )

                    komunikat = (
                        "Firma nie istniała w bazie. "
                        "Została utworzona automatycznie. "
                    )
                else:
                    komunikat = (
                        "Firma już istnieje w bazie. "
                    )

                if rok_z_xml:
                    sprawozdanie_z_roku = firma_z_xml.sprawozdania.filter(
                        rok=int(rok_z_xml)
                    ).first()

                    if not sprawozdanie_z_roku:                    
                        SprawozdanieFinansowe.objects.create(
                            firma=firma_z_xml,
                            rok=int(rok_z_xml),
                            naleznosci=naleznosci_z_xml
                        )
                        
                        komunikat += (
                            f"Dodano sprawozdanie za rok {rok_z_xml}. "
                        )
                            
                    else:
                        if sprawozdanie_z_roku.naleznosci == 0 and naleznosci_z_xml > 0:
                            sprawozdanie_z_roku.naleznosci = naleznosci_z_xml
                            sprawozdanie_z_roku.save()

                            komunikat += (
                                f"Sprawozdanie za rok {rok_z_xml} już istniało w bazie, "
                                f"ale miało należności 0. "
                                f"Należności zostały uzupełnione z XML. "
                            )
                        else:
                            komunikat += (
                                f"Sprawozdanie za rok {rok_z_xml} już istnieje w bazie. "
                                f"Może to być korekta albo ponowny import. "
                            )
                            
                            
                komunikat += (
                    f"Plik {plik_xml.name} został odebrany "
                    f"i poprawnie odczytany jako XML. "
                    f"Dane z XML: nazwa: {nazwa_z_xml or 'brak'}, "
                    f"NIP: {nip_z_xml or 'brak'}, "
                    f"KRS: {krs_z_xml or 'brak'}, "
                    f"Rok: {rok_z_xml or 'brak'}. "
                    f"Należności: {naleznosci_z_xml}."
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
def usun_sprawozdanie(request, sprawozdanie_id):
    sprawozdanie = get_object_or_404(
        SprawozdanieFinansowe.objects.filter(
            firma__owner=request.user
        ),
        id=sprawozdanie_id
    )

    if request.method == "POST":
        firma_id = sprawozdanie.firma.id
        sprawozdanie.delete()
        return redirect("szczegoly_firmy", firma_id=firma_id)

    return render(
        request,
        "firmy_django/potwierdz_usuniecie_sprawozdania.html",
        {
            "sprawozdanie": sprawozdanie,
        }
    )   
    
    
@login_required
def usun_firme(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.filter(owner=request.user),
        id=firma_id
    )

    if request.method == "POST":
        firma.delete()
        return redirect("home")

    return render(
        request,
        "firmy_django/potwierdz_usuniecie_firmy.html",
        {
            "firma": firma,
        }
    )
    

@login_required
def archiwizuj_sprawozdanie(request, sprawozdanie_id):
    sprawozdanie = get_object_or_404(
        SprawozdanieFinansowe.objects.filter(
            firma__owner=request.user
        ),
        id=sprawozdanie_id
    )

    sprawozdanie.czy_zarchiwizowane = True
    sprawozdanie.save()

    return redirect(
        "szczegoly_firmy",
        firma_id=sprawozdanie.firma.id
    )


@login_required
def archiwum_sprawozdan(request):
    sprawozdania = SprawozdanieFinansowe.objects.filter(
        firma__owner=request.user,
        czy_zarchiwizowane=True
    ).select_related("firma").order_by("firma__nazwa", "-rok")

    return render(request, "firmy_django/archiwum_sprawozdan.html", {
        "sprawozdania": sprawozdania,
    })


@login_required
def przywroc_sprawozdanie(request, sprawozdanie_id):
    sprawozdanie = get_object_or_404(
        SprawozdanieFinansowe.objects.filter(
            firma__owner=request.user,
            czy_zarchiwizowane=True
        ),
        id=sprawozdanie_id
    )

    sprawozdanie.czy_zarchiwizowane = False
    sprawozdanie.save()

    return redirect("archiwum_sprawozdan")


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
                naleznosci_z_xml = Decimal("0")

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
                        
                        
                    if (
                        "Naleznosci" in tag
                        or "Należności" in tag
                        or "Naleznosc" in tag
                        or "Należność" in tag
                    ) and element.text:
                        try:
                            naleznosci_z_xml = Decimal(
                                element.text.strip().replace(" ", "").replace(",", ".")
                            )
                        except InvalidOperation:
                            naleznosci_z_xml = Decimal("0")
                        

                    if tag == "Aktywa_B_II":
                        for dziecko in element:
                            tag_dziecka = dziecko.tag.split("}")[-1]

                            if tag_dziecka == "KwotaA" and dziecko.text:
                                try:
                                    naleznosci_z_xml = Decimal(
                                        dziecko.text.strip().replace(" ", "").replace(",", ".")
                                    )

                                    if "WTysiacach" in zawartosc_xml:
                                        naleznosci_z_xml = naleznosci_z_xml * Decimal("1000")

                                except InvalidOperation:
                                    naleznosci_z_xml = Decimal("0")

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
                    
                print("=" * 50)
                print("DEBUG IMPORT Z TABELI")
                print("Plik:", plik_xml.name)
                print("Rok:", rok_z_xml)
                print("Należności:", naleznosci_z_xml)
                print("=" * 50)

                print()
                print("=" * 60)
                print("DEBUG")
                print("Plik:", plik_xml.name)
                print("Rok:", rok_z_xml)
                print("Należności odczytane:", naleznosci_z_xml)
                print("=" * 60)
                print()



                if firma_z_xml:
                    status_firmy_w_bazie = (
                        f"Firma z XML istnieje już w bazie: {firma_z_xml.nazwa}."
                    )

                    sprawozdanie_z_roku = firma_z_xml.sprawozdania.filter(
                        rok=int(rok_z_xml)
                    ).first()

                    if sprawozdanie_z_roku:
                        if sprawozdanie_z_roku.naleznosci == 0 and naleznosci_z_xml > 0:
                            sprawozdanie_z_roku.naleznosci = naleznosci_z_xml
                            sprawozdanie_z_roku.save()

                            status_firmy_w_bazie += (
                                f" Sprawozdanie za rok {rok_z_xml} już istniało w bazie,"
                                f" ale miało należności 0."
                                f" Należności zostały uzupełnione z XML."
                            )
                        else:
                            status_firmy_w_bazie += (
                                f" Sprawozdanie za rok {rok_z_xml} już istnieje w bazie."
                                f" Możliwe, że importowany plik jest korektą istniejącego sprawozdania."
                                f" W przyszłości będzie można zastąpić istniejące sprawozdanie,"
                                f" zachować obie wersje, porównać je albo anulować import."
                            )

                    else:
                        SprawozdanieFinansowe.objects.create(
                            firma=firma_z_xml,
                            rok=int(rok_z_xml),
                            naleznosci=naleznosci_z_xml
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
                        rok=int(rok_z_xml),
                        naleznosci=naleznosci_z_xml
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

                komunikat = (
                    f"Plik {plik_xml.name} został odebrany, "
                    f"poprawnie odczytany jako XML "
                    f"i zapisany na dysku. "
                )

                if czy_xml_pasuje_do_firmy:
                    komunikat += "XML prawdopodobnie dotyczy wybranej firmy. "
                else:
                    komunikat += "Uwaga: XML prawdopodobnie nie dotyczy wybranej firmy. "

                komunikat += (
                    f"Dane z XML: nazwa: {nazwa_z_xml or 'brak'}, "
                    f"NIP: {nip_z_xml or 'brak'}, "
                    f"KRS: {krs_z_xml or 'brak'}, "
                    f"Rok: {rok_z_xml or 'brak'}, "
                    f"Należności: {naleznosci_z_xml}. "
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

        odbiorcy_z_bazy = [firma.email for firma in firmy]
        wszyscy_odbiorcy = list(dict.fromkeys(odbiorcy_z_bazy))

        temat = request.POST.get("temat", "")
        tresc = request.POST.get("tresc", "")
        akcja = request.POST.get("akcja", "")

        komunikat = ""

        if akcja == "wyslij_test":
            if temat and tresc and wszyscy_odbiorcy:
                wyslij_mailing_task.delay(
                    temat,
                    tresc,
                    wszyscy_odbiorcy
                )

                mailing = Mailing.objects.create(
                    owner=request.user,
                    temat=temat,
                    tresc=tresc,
                )

                mailing.firmy_odbiorcy.set(firmy)

                komunikat = (
                    f"Mailing został przekazany do wysłania w tle. "
                    f"Liczba odbiorców: {len(wszyscy_odbiorcy)}."
                )
            else:
                komunikat = (
                    "Nie wysłano mailingu. Uzupełnij temat, treść i wybierz przynajmniej jedną firmę z adresem e-mail."
                )

        return render(request, "firmy_django/podsumowanie_mailing.html", {
            "firmy": firmy,
            "liczba_firm": firmy.count(),
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

@login_required
def archiwum_sprawozdan(request):
    sprawozdania = SprawozdanieFinansowe.objects.filter(
        firma__owner=request.user,
        czy_zarchiwizowane=True
    ).select_related("firma").order_by("firma__nazwa", "-rok")

    return render(request, "firmy_django/archiwum_sprawozdan.html", {
        "sprawozdania": sprawozdania,
    })


@login_required
def przywroc_sprawozdanie(request, sprawozdanie_id):
    sprawozdanie = get_object_or_404(
        SprawozdanieFinansowe.objects.filter(
            firma__owner=request.user,
            czy_zarchiwizowane=True
        ),
        id=sprawozdanie_id
    )

    sprawozdanie.czy_zarchiwizowane = False
    sprawozdanie.save()

    return redirect("archiwum_sprawozdan")


@extend_schema(
    summary="Lista firm",
    description="""
Zwraca listę firm należących do zalogowanego użytkownika.

Możliwe jest wyszukiwanie po nazwie firmy przy pomocy parametru:

?search=nazwa

Endpoint wymaga uwierzytelnienia JWT lub sesji Django.
""",
)


class FirmaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FirmaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["nazwa", "nip", "regon", "krs", "miasto"]

    def get_queryset(self):
        return (
            Firma.objects.filter(owner=self.request.user)
            .prefetch_related("branze", "sprawozdania")
        )



@extend_schema(
    summary="Lista sprawozdań finansowych",
    description="""
Zwraca sprawozdania finansowe zalogowanego użytkownika.

Możliwe jest wyszukiwanie po roku:

?search=2024

Endpoint wymaga uwierzytelnienia JWT lub sesji Django.
""",
)


class SprawozdanieFinansoweViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SprawozdanieFinansoweSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["rok", "firma__nazwa", "firma__nip"]

    def get_queryset(self):
        return SprawozdanieFinansowe.objects.filter(
            firma__owner=self.request.user
        )
        
@login_required
def dodaj_firme(request):
    if request.method == "POST":
        form = FirmaForm(request.POST)

        if form.is_valid():
            firma = form.save(commit=False)
            firma.owner = request.user
            firma.save()

            return redirect("home")

    else:
        form = FirmaForm()

    return render(
        request,
        "firmy_django/dodaj_firme.html",
        {"form": form},
    )
    
    
@login_required
def edytuj_firme(request, firma_id):
    firma = get_object_or_404(
        Firma,
        id=firma_id,
        owner=request.user
    )

    if request.method == "POST":
        form = FirmaForm(request.POST, instance=firma)

        if form.is_valid():
            form.save()
            return redirect("szczegoly_firmy", firma_id=firma.id)

    else:
        form = FirmaForm(instance=firma)

    return render(request, "firmy_django/edytuj_firme.html", {
        "form": form,
        "firma": firma,
    })
    
    

        
