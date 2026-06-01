from django.shortcuts import render, get_object_or_404

from .models import Firma


def index(request):
    query = request.GET.get("q", "")

    firmy = Firma.objects.prefetch_related("sprawozdania").all()

    if query:
        firmy = firmy.filter(
            nazwa__icontains=query
        ) | firmy.filter(
            nip__icontains=query
        )

    firmy = firmy.order_by("nazwa")

    return render(request, "firmy_django/index.html", {
        "firmy": firmy,
        "query": query,
    })


def szczegoly_firmy(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.prefetch_related("sprawozdania"),
        id=firma_id
    )

    return render(request, "firmy_django/szczegoly_firmy.html", {
        "firma": firma,
    })
