from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser  # Correct


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
