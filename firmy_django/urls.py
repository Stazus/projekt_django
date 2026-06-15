from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("rejestracja/", views.rejestracja, name="rejestracja"),
    path("", views.index, name="home"),
    path("importuj-xml/", views.importuj_xml_ogolny, name="importuj_xml_ogolny"),
    path("firmy/<int:firma_id>/", views.szczegoly_firmy, name="szczegoly_firmy"),
    path(
        "sprawozdanie/<int:sprawozdanie_id>/usun/",
        views.usun_sprawozdanie,
        name="usun_sprawozdanie",
    ),    
    path(
        "sprawozdanie/<int:sprawozdanie_id>/archiwizuj/",
        views.archiwizuj_sprawozdanie,
        name="archiwizuj_sprawozdanie",
    ),    
    path("mailing/przygotuj/", views.przygotuj_mailing, name="przygotuj_mailing"),
    path("mailingi/", views.historia_mailingow, name="historia_mailingow"),
    path("mailingi/<int:mailing_id>/", views.szczegoly_mailingu, name="szczegoly_mailingu"),

   path(
       "firmy/<int:firma_id>/import-xml/",
       views.importuj_xml,
       name="importuj_xml"
   ),

    path("logowanie/", auth_views.LoginView.as_view(
        template_name="firmy_django/logowanie.html"
    ), name="login"),

    path("wylogowanie/", auth_views.LogoutView.as_view(), name="logout"),
]