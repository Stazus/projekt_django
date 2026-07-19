import re

from django import forms
from .models import Firma, ProfilFirmy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        labels = {
            "username": "Nazwa użytkownika",
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not password:
            return password

        if len(password) < 8 or len(password) > 16:
            raise forms.ValidationError(
                "Hasło musi mieć od 8 do 16 znaków."
            )

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Hasło musi zawierać co najmniej jedną wielką literę."
            )

        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "Hasło musi zawierać co najmniej jedną cyfrę."
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            raise forms.ValidationError(
                "Hasło musi zawierać co najmniej jeden znak specjalny."
            )

        return password


class FirmaForm(forms.ModelForm):
    class Meta:
        model = Firma
        fields = [
            "nazwa",
            "nip",
            "regon",
            "krs",
            "miasto",
            "email",
            "email_zrodlo",
            "branze",
        ]
        
        widgets = {
            "branze": forms.CheckboxSelectMultiple(),
        }
        
class ProfilFirmyForm(forms.ModelForm):
    class Meta:
        model = ProfilFirmy
        fields = [
            "opis",
            "logo",
            "banner",
        ]

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        uploaded_logo = self.files.get("logo")

        if uploaded_logo:
            allowed_extensions = ["jpg", "jpeg", "png", "webp"]
            extension = uploaded_logo.name.rsplit(".", 1)[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Logo musi być plikiem JPG, PNG lub WebP."
                )

            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]

            if uploaded_logo.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Logo musi być prawidłowym obrazem JPG, PNG lub WebP."
                )

            if uploaded_logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "Logo nie może być większe niż 2 MB."
                )

        return logo

    def clean_banner(self):
        banner = self.cleaned_data.get("banner")
        uploaded_banner = self.files.get("banner")

        if uploaded_banner:
            allowed_extensions = ["jpg", "jpeg", "png", "webp"]
            extension = uploaded_banner.name.rsplit(".", 1)[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Banner musi być plikiem JPG, PNG lub WebP."
                )

            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]

            if uploaded_banner.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Banner musi być prawidłowym obrazem JPG, PNG lub WebP."
                )

            if uploaded_banner.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Banner nie może być większy niż 5 MB."
                )

        return banner