from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404

from .models import Firma


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

    if sort == "name_desc":
        firmy = firmy.order_by("-nazwa")
    elif sort == "reports_desc":
        firmy = sorted(
            firmy,
            key=lambda f: f.sprawozdania.count(),
            reverse=True
        )
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
