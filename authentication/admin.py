from django.contrib import admin
from .models import CustomUser

# Enregistrement des modèles 'CustomUser' et 'UserFollows' pour qu'ils soient gérés via l'interface d'administration.
admin.site.register(CustomUser)
