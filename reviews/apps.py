from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration de l'application 'reviews'. Définit le nom de l'application et
    le type de clé primaire par défaut.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
