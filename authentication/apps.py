from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration de l'application d'authentification.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
