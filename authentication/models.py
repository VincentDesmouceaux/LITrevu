from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('USER', 'Utilisateur'),
        ('DEVELOPER', 'Développeur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_developer = models.BooleanField(default=False)  # Champ pour la distinction développeur/utilisateur

    follows = models.ManyToManyField('self', limit_choices_to={'role': 'USER'}, symmetrical=False, verbose_name='suit')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Gestion des utilisateurs et développeurs
        if self.role == 'DEVELOPER':
            group, _ = Group.objects.get_or_create(name='developers')
            self.groups.add(group)
        else:
            group, _ = Group.objects.get_or_create(name='users')
            self.groups.add(group)
