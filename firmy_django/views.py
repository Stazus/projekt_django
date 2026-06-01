from django.shortcuts import render, get_object_or_404

from .models import Firma


def index(request):
    firmy = Firma.objects.prefetch_related("sprawozdania").all().order_by("nazwa")

    return render(request, "firmy_django/index.html", {
        "firmy": firmy,
    })


def szczegoly_firmy(request, firma_id):
    firma = get_object_or_404(
        Firma.objects.prefetch_related("sprawozdania"),
        id=firma_id
    )

    return render(request, "firmy_django/szczegoly_firmy.html", {
        "firma": firma,
    })
