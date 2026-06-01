from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("firmy/<int:firma_id>/", views.szczegoly_firmy, name="szczegoly_firmy"),
]
