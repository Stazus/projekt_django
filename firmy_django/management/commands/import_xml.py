import os
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from firmy_django.models import Firma, SprawozdanieFinansowe


XML_DIR = "sprawozdania_xml"


def clean_amount_to_float(text):
    if not text:
        return 0.0

    s = str(text).strip().replace("\xa0", "").replace(" ", "")

    if "." in s and "," in s and s.find(".") < s.find(","):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return 0.0


def localname(elem):
    tag = elem.tag
    if isinstance(tag, str) and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def find_first_text_by_locals(root, localnames):
    for e in root.iter():
        if localname(e) in localnames:
            if e.text and e.text.strip():
                return e.text.strip()
    return None


def find_elements_by_local(root, local):
    return [e for e in root.iter() if localname(e) == local]


def find_kwotaA_in_Aktywa_B_II_3(root):
    aktywa_b_ii_3 = find_elements_by_local(root, "Aktywa_B_II_3")

    if aktywa_b_ii_3:
        for a in aktywa_b_ii_3:
            for descendant in a.iter():
                if localname(descendant) == "KwotaA":
                    return clean_amount_to_float(descendant.text)

    parent_map = {c: p for p in root.iter() for c in p}
    kwota_candidates = []

    for e in root.iter():
        if localname(e) == "KwotaA":
            ancestors = []
            current = e

            while current in parent_map:
                current = parent_map[current]
                ancestors.append(localname(current))

            if any(a == "Aktywa_B_II_3" for a in ancestors):
                kwota_candidates.append((e, 3))
            elif any(a == "Aktywa_B_II" for a in ancestors):
                kwota_candidates.append((e, 2))
            else:
                kwota_candidates.append((e, 0))

    if kwota_candidates:
        kwota_candidates.sort(key=lambda x: -x[1])
        chosen = kwota_candidates[0][0]
        return clean_amount_to_float(chosen.text)

    return 0.0


def parse_one_file(path):
    info = {
        "plik": os.path.basename(path),
        "nazwa": "brak",
        "nip": "",
        "naleznosci": 0.0,
    }

    tree = ET.parse(path)
    root = tree.getroot()

    nazwa = find_first_text_by_locals(
        root,
        ["NazwaFirmy", "NazwaPodmiotu", "PelnaNazwa", "NazwaJednostki", "Firma", "Nazwa"]
    )

    nip = find_first_text_by_locals(
        root,
        ["P_1D", "P_1E", "NIP", "NumerNIP", "IdentyfikatorPodatkowy"]
    )

    naleznosci = find_kwotaA_in_Aktywa_B_II_3(root)

    if nazwa:
        info["nazwa"] = nazwa

    if nip:
        info["nip"] = nip

    info["naleznosci"] = naleznosci

    return info


class Command(BaseCommand):
    help = "Importuje firmy i sprawozdania finansowe z plików XML."

    def handle(self, *args, **options):
        if not os.path.isdir(XML_DIR):
            self.stdout.write(self.style.ERROR(f"Brak katalogu: {XML_DIR}"))
            return

        scanned = 0
        saved_reports = 0

        for fname in sorted(os.listdir(XML_DIR)):
            if not fname.lower().endswith(".xml"):
                continue

            if "zone.identifier" in fname.lower():
                continue

            scanned += 1
            path = os.path.join(XML_DIR, fname)

            try:
                data = parse_one_file(path)

                firma, _ = Firma.objects.get_or_create(
                    nip=data["nip"],
                    defaults={
                        "nazwa": data["nazwa"],
                    }
                )

                if firma.nazwa == "brak" and data["nazwa"] != "brak":
                    firma.nazwa = data["nazwa"]
                    firma.save()

                SprawozdanieFinansowe.objects.update_or_create(
                    firma=firma,
                    rok=2024,
                    defaults={
                        "naleznosci": data["naleznosci"],
                        "plik_xml": data["plik"],
                    }
                )

                saved_reports += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"OK: {data['nazwa']} | NIP: {data['nip']} | należności: {data['naleznosci']}"
                    )
                )

            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"BŁĄD: {fname} -> {exc}")
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Przeskanowano plików XML: {scanned}"))
        self.stdout.write(self.style.SUCCESS(f"Zapisano/zaaktualizowano sprawozdań: {saved_reports}"))
