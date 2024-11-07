from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec un rôle (utilisateur ou développeur) et un système de suivi.

    Attributs:
        role (str): Rôle de l'utilisateur ('USER' ou 'DEVELOPER').
        is_developer (bool): Indique si l'utilisateur est développeur.
        follows (ManyToManyField): Relation de suivi entre utilisateurs.
    """

    ROLE_CHOICES = [
        ('USER', 'Utilisateur'),
        ('DEVELOPER', 'Développeur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_developer = models.BooleanField(default=False)

    follows = models.ManyToManyField(
        'self', through='subscriptions.UserFollows', related_name='is_followed_by', symmetrical=False
    )

    def save(self, *args, **kwargs):
        """
        Enregistre l'utilisateur et assigne le groupe en fonction du rôle.
        Si le rôle est 'DEVELOPER', l'utilisateur est ajouté au groupe 'developers'.
        Sinon, il est ajouté au groupe 'users'.
        """
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name='developers' if self.role == 'DEVELOPER' else 'users')
        self.groups.add(group)
