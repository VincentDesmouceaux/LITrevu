from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
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
        super().save(*args, **kwargs)
        if self.role == 'DEVELOPER':
            group, _ = Group.objects.get_or_create(name='developers')
            self.groups.add(group)
        else:
            group, _ = Group.objects.get_or_create(name='users')
            self.groups.add(group)
