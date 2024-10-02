from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Si tu as besoin de champs supplémentaires, tu peux les ajouter ici
    pass
