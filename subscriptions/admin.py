from django.contrib import admin
from .models import UserFollows

# Enregistrement du modèle 'UserFollows' pour permettre la gestion des abonnements via l'interface admin.
admin.site.register(UserFollows)
