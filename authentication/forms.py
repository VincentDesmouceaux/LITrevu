from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        help_text="Requis. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.",
    )
    email = forms.EmailField(
        label="Adresse e-mail",
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        help_text=(
            "<ul>"
            "<li>Votre mot de passe ne doit pas être trop similaire à vos autres informations personnelles.</li>"
            "<li>Votre mot de passe doit contenir au moins 8 caractères.</li>"
            "<li>Votre mot de passe ne doit pas être un mot de passe couramment utilisé.</li>"
            "<li>Votre mot de passe ne doit pas être entièrement numérique.</li>"
            "</ul>"
        ),
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        help_text="Entrez le même mot de passe que précédemment, pour vérification.",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
