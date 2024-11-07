from django.contrib import admin
from .models import CustomUser

# Enregistrement du modèle 'CustomUser' pour l'accès via l'interface d'administration.
admin.site.register(CustomUser)
