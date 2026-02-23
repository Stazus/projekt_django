from django.shortcuts import render
from django.http import FileResponse, Http404
from .models import Firma
import os
import csv
import xml.etree.ElementTree as ET

XML_DIR = "sprawozdania_xml"      # folder z plikami XML
CSV_NAME = "firmy_naleznosci.csv" # CSV do pobrania
DEFAULT_THRESHOLD = 100_000       # próg kwoty

# -----------------------------
# Funkcje pomocnicze
# -----------------------------
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
    except:
        return 0.0

def localname(elem):
    tag = elem.tag
    if isinstance(tag, str) and "}" in tag:
        return tag.split("}", 1)[1]
    return tag

def find_first_text_by_locals(root, localnames):
    for e in root.iter():
        if localname(e) in localnames and e.text and e.text.strip():
            return e.text.strip()
    return None

def find_elements_by_local(root, local):
    return [e for e in root.iter() if localname(e) == local]

def find_kwotaA_in_Aktywa_B_II_3(root):
    aktywa_b_ii_3 = find_elements_by_local(root, "Aktywa_B_II_3")
    debug_notes = []
    if aktywa_b_ii_3:
        for a in aktywa_b_ii_3:
            for descendant in a.iter():
                if localname(descendant) == "KwotaA":
                    debug_notes.append(f"Found KwotaA: '{(descendant.text or '').strip()}'")
                    return clean_amount_to_float(descendant.text), debug_notes
        debug_notes.append("Found Aktywa_B_II_3 but no KwotaA inside.")
    else:
        debug_notes.append("No Aktywa_B_II_3 elements found.")

    parent_map = {c: p for p in root.iter() for c in p}
    kwota_candidates = []
    for e in root.iter():
        if localname(e) == "KwotaA":
            anc = []
            cur = e
            while cur in parent_map:
                cur = parent_map[cur]
                anc.append(localname(cur))
            if any(a == "Aktywa_B_II_3" for a in anc):
                kwota_candidates.append((e, 3))
            elif any("Aktywa_B_II" in a for a in anc):
                kwota_candidates.append((e, 2))
            else:
                kwota_candidates.append((e, 0))

    if kwota_candidates:
        kwota_candidates.sort(key=lambda x: -x[1])
        chosen = kwota_candidates[0][0]
        debug_notes.append(f"Chosen KwotaA (fallback): '{(chosen.text or '').strip()}'")
        return clean_amount_to_float(chosen.text), debug_notes

    debug_notes.append("No KwotaA candidates found.")
    return 0.0, debug_notes

def parse_one_file(path):
    info = {"plik": os.path.basename(path), "nazwa": "brak", "nip": "brak", "kwota": 0.0, "debug": []}
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        name = find_first_text_by_locals(root, ["NazwaFirmy","NazwaPodmiotu","PelnaNazwa","NazwaJednostki","Firma","Nazwa"])
        if name:
            info["nazwa"] = name
            info["debug"].append(f"Found name: {name}")

        nip = find_first_text_by_locals(root, ["P_1D","P_1E","NIP","NumerNIP","IdentyfikatorPodatkowy"])
        if nip:
            info["nip"] = nip
            info["debug"].append(f"Found NIP: {nip}")

        kwota, notes = find_kwotaA_in_Aktywa_B_II_3(root)
        info["kwota"] = kwota
        info["debug"].extend(notes)

    except Exception as exc:
        info["debug"].append(f"Exception parsing file: {exc}")

    return info

def scan_folder(threshold):
    results = []
    scanned = 0
    os.makedirs(XML_DIR, exist_ok=True)
    for fname in sorted(os.listdir(XML_DIR)):
        if not fname.lower().endswith(".xml"):
            continue
        scanned += 1
        path = os.path.join(XML_DIR, fname)
        info = parse_one_file(path)
        if info["kwota"] >= float(threshold):
            results.append(info)
    results.sort(key=lambda x: x["kwota"], reverse=True)
    return results, scanned

def save_csv(rows, csv_path=CSV_NAME):
    headers = ["Nazwa firmy","NIP","Kwota (Aktywa_B_II_3/KwotaA)","Plik"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter=";")
        w.writeheader()
        for r in rows:
            kw = "{:,.2f}".format(r["kwota"]).replace(",", " ").replace(".", ",")
            w.writerow({"Nazwa firmy": r["nazwa"], "NIP": r["nip"], "Kwota (Aktywa_B_II_3/KwotaA)": kw, "Plik": r["plik"]})

# -----------------------------
# Widoki Django
# -----------------------------
def index(request):
    try:
        thr = float(request.GET.get("min", DEFAULT_THRESHOLD))
    except:
        thr = DEFAULT_THRESHOLD

    debug_mode = request.GET.get("debug", "0") in ("1","true","yes")

    results, scanned = scan_folder(thr)
    save_csv(results)

    # zapis do bazy Django
    Firma.objects.all().delete()
    for r in results:
        Firma.objects.create(nazwa=r["nazwa"], nip=r["nip"], kwota=r["kwota"], plik=r["plik"])

    debug_infos = []
    if debug_mode:
        for fname in sorted(os.listdir(XML_DIR)):
            if not fname.lower().endswith(".xml"):
                continue
            debug_infos.append(parse_one_file(os.path.join(XML_DIR, fname)))

    postgres_rows = Firma.objects.order_by('-kwota')[:20]

    return render(request, "firmy_django/index.html", {
        "firmy": results,
        "scanned": scanned,
        "matched": len(results),
        "min_thr": int(thr),
        "csv_name": CSV_NAME,
        "debug_mode": debug_mode,
        "debug_infos": debug_infos,
        "postgres_rows": postgres_rows
    })

def download_csv(request):
    if os.path.exists(CSV_NAME):
        return FileResponse(open(CSV_NAME,'rb'), as_attachment=True, filename=CSV_NAME)
    raise Http404("Plik CSV nie istnieje")
