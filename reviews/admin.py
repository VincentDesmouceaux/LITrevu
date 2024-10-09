from django.contrib import admin
from .models import Ticket, Review

# Enregistrement des modèles 'Ticket' et 'Review' pour qu'ils soient gérés via l'interface d'administration.
admin.site.register(Ticket)
admin.site.register(Review)
