from django.contrib import admin
from .models import Ticket, Review, UserFollows
from users.models import CustomUser  # Mise à jour de l'import

admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
