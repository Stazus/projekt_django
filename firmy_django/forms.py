import re

from django import forms
from .models import Firma
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
        ]
        
