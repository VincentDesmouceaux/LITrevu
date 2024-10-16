from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUserForm(forms.Form):
    username = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Nom d'utilisateur",
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        initial_letter = kwargs.pop('initial_letter', None)  # Pour filtrer par lettre
        super(FollowUserForm, self).__init__(*args, **kwargs)

        # Si une lettre est fournie, on filtre les utilisateurs par cette lettre
        if initial_letter:
            self.fields['username'].queryset = User.objects.filter(
                username__istartswith=initial_letter).order_by('username')
        else:
            # Si aucune lettre n'est fournie, on affiche tous les utilisateurs
            self.fields['username'].queryset = User.objects.all().order_by('username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Veuillez sélectionner un utilisateur.")
        return username
