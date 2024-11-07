from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur personnalisé.
    Utilisé pour gérer l'inscription avec les champs username, email, password1 et password2.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
