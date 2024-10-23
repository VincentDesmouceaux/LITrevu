from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUserForm(forms.Form):
    user_id = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Charger tous les utilisateurs
        label="Utilisateur",
        widget=forms.HiddenInput  # Champ caché pour soumettre l'ID utilisateur
    )

    def clean_user_id(self):
        user = self.cleaned_data.get('user_id')
        if not user:
            raise forms.ValidationError("Veuillez sélectionner un utilisateur.")
        return user
